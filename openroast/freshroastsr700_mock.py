import time
import datetime
import serial
import threading
import logging
import threading
import multiprocessing as mp
from multiprocessing import sharedctypes
import struct
import binascii
import math

from freshroastsr700 import pid
from freshroastsr700 import exceptions

class freshroastsr700(object):
    """A class to interface with a freshroastsr700 coffee roaster."""
    def __init__(self,
                 update_data_func=None,
                 state_transition_func=None,
                 thermostat=False,
                 kp=0.06, ki=0.0075, kd=0.01,
                 heater_segments=8):
        """Create variables used to send in packets to the roaster. The update
        data function is called when a packet is opened. The state transistion
        function is used by the timer thread to know what to do next. See wiki
        for more information on packet structure and fields."""

        # for mock
        self._connect_attempts = 0;
        
        self.create_update_data_system(update_data_func)
        self.create_state_transition_system(state_transition_func)

        self._header = sharedctypes.Array('c', b'\xAA\xAA')
        self._temp_unit = sharedctypes.Array('c', b'\x61\x74')
        self._flags = sharedctypes.Array('c', b'\x63')
        self._current_state = sharedctypes.Array('c', b'\x02\x01')
        self._footer = b'\xAA\xFA'

        self._fan_speed = sharedctypes.Value('i', 1)
        self._heat_setting = sharedctypes.Value('i', 0)
        self._target_temp = sharedctypes.Value('i', 150)
        self._current_temp = sharedctypes.Value('i', 150)
        self._time_remaining = sharedctypes.Value('i', 0)
        self._total_time = sharedctypes.Value('i', 0)

        self._cont = sharedctypes.Value('i', 1)

        # for SW PWM heater setting
        self._heater_level = sharedctypes.Value('i', 0)
        # the following vars are not process-safe, do not access them
        # from the comm or timer threads, nor from the callbacks.
        self._thermostat = thermostat
        self._pid_kp = kp
        self._pid_ki = ki
        self._pid_kd = kd
        self._heater_bangbang_segments = heater_segments

        # constants for protocol decoding
        self.LOOKING_FOR_HEADER_1 = 0
        self.LOOKING_FOR_HEADER_2 = 1
        self.PACKET_DATA = 2
        self.LOOKING_FOR_FOOTER_2 = 3

        # initialize to 'not connected'
        self._connected = sharedctypes.Value('i', 0)
        # initialize to 'not trying to connect'
        self._attempting_connect = sharedctypes.Value('i', 0)
        
        # create comm process
        self.comm_process = mp.Process(
            target=self.comm,
            args=(
                self._thermostat,
                self._pid_kp,
                self._pid_ki,
                self._pid_kd,
                self._heater_bangbang_segments,
                self.update_data_event,))
        self.comm_process.daemon = True
        self.comm_process.start()
        # create timer process that counts down time_remaining
        self.time_process = mp.Process(
            target=self.timer,
            args=(
                self.state_transition_event,))
        self.time_process.daemon = True
        self.time_process.start()

    def create_update_data_system(self,update_data_func,
        setFunc=True, createThread=False):
        # these callbacks cannot be called from another process in Windows.
        # Therefore, spawn a thread belonging to the calling process
        # instead.
        # the comm and timer processes will set events that the threads
        # will listen for to initiate the callbacks

        # only create the mp.Event once -  to miic create_state_transition_system,
        # for future-proofing
        # (in this case, currently, this is only called at __init__() time) 
        if not hasattr(self, 'update_data_event'):
            self.update_data_event = mp.Event()
        if setFunc:
            self.update_data_func = update_data_func
        if self.update_data_func is not None:
            if createThread:
                self.update_data_thread = threading.Thread(
                    name='sr700_update_data',
                    target=self.update_data_run,
                    args=(self.update_data_event,),
                    daemon=True
                    )
        else:
            self.update_data_thread = None

    def create_state_transition_system(self,state_transition_func, 
        setFunc=True, createThread=False):
        # these callbacks cannot be called from another process in Windows.
        # Therefore, spawn a thread belonging to the calling process
        # instead.
        # the comm and timer processes will set events that the threads
        # will listen for to initiate the callbacks

        # only create the mp.Event once - this fn can get called more 
        # than once, by __init__() and by set_state_transition_func()
        if not hasattr(self, 'state_transition_event'):
            self.state_transition_event = mp.Event()
        if setFunc:
            self.state_transition_func = state_transition_func
        if self.state_transition_func is not None:
            if createThread:
                self.state_transition_thread = threading.Thread(
                    name='sr700_state_transition',
                    target=self.state_transition_run,
                    args=(self.state_transition_event,),
                    daemon=True
                    )
        else:
            self.state_transition_thread = None

    @property
    def fan_speed(self):
        """A getter method for _fan_speed."""
        return self._fan_speed.value

    @fan_speed.setter
    def fan_speed(self, value):
        """Verifies the value is between 1 and 9 inclusively."""
        if value not in range(1, 10):
            raise exceptions.RoasterValueError

        self._fan_speed.value = value

    @property
    def heat_setting(self):
        """A getter method for _heat_setting."""
        return self._heat_setting.value

    @heat_setting.setter
    def heat_setting(self, value):
        """Verifies that the heat setting is between 0 and 3."""
        if value not in range(0, 4):
            raise exceptions.RoasterValueError

        self._heat_setting.value = value

    @property
    def target_temp(self):
        return self._target_temp.value

    @target_temp.setter
    def target_temp(self, value):
        if value not in range(150, 551):
            raise exceptions.RoasterValueError

        self._target_temp.value = value

    @property
    def current_temp(self):
        return self._current_temp.value

    @current_temp.setter
    def current_temp(self, value):
        if value not in range(150, 551):
            raise exceptions.RoasterValueError

        self._current_temp.value = value

    @property
    def time_remaining(self):
        return self._time_remaining.value

    @time_remaining.setter
    def time_remaining(self, value):
        self._time_remaining.value = value

    @property
    def total_time(self):
        return self._total_time.value

    @total_time.setter
    def total_time(self, value):
        self._total_time.value = value

    @property
    def heater_level(self):
        """A getter method for _heater_level. Only used when
           thermostat=True.  Driven by built-in PID controller.
           Min will always be zero, max will be heater_segments
           (optional instantiation parameter, defaults to 8)."""
        return self._heater_level.value

    @property
    def connected(self):
        """A getter method for _connected. Indicates that the
        this software is currently communicating with FreshRoast SR700
        hardware."""
        return self._connected.value

    def set_state_transition_func(self, func):
        """Set, or re-set, the state transition function callback.
           This function will be called from a separate thread within
           freshroastsr700, as triggered by a separate process.
           It's important that any data touched by this
           function be process-safe.
           This function will fail if the freshroastsr700 device is already
           connected to hardware, because by that time, the timer process
           and threads have already been spawned.
           THIS FUNCTION MUST BE CALLED BEFORE freshroastsr700.auto_connect().
           """
        if self._connected.value:
            logging.error("freshroastsr700.set_state_transition_func must be "
                          "called before freshroastsr700.auto_connect()."
                          " Not registering func.")
            return False
        # no connection yet. so OK to set func pointer
        self.create_state_transition_system(func)
        return True

    def update_data_run(self, event_to_wait_on):
        """This is the thread that listens to an event from
           the comm process to execute the update_data_func callback
           in the context of the main process.
           """
        # with the daemon=Turue setting, this thread should
        # quit 'automatically'
        while event_to_wait_on.wait():
            event_to_wait_on.clear()
            self.update_data_func()

    def state_transition_run(self, event_to_wait_on):
        """This is the thread that listens to an event from
           the timer process to execute the state_transition_func callback
           in the context of the main process.
           """
        # with the daemon=Turue setting, this thread should
        # quit 'automatically'
        while event_to_wait_on.wait():
            event_to_wait_on.clear()
            self.state_transition_func()

    def _connect(self):
        """Connects to the roaster and creates communication thread."""
        """Do not call this directly - call auto_connect(), which will call
        connect() for you.

        Connects to the roaster and creates communication thread."""
        # for mock, pretend to puke on utils.find_device for the first 20 attempts,
        # then succeed
        self._connect_attempts += 1
        if self._connect_attempts < 20:
            raise exceptions.RoasterLookupError
        self._connect_attempts = 0
        
        # port = utils.find_device('1A86:5523')
        # self._ser = serial.Serial(
            # port=port,
            # baudrate=9600,
            # bytesize=8,
            # parity='N',
            # stopbits=1.5,
            # timeout=0.25,
            # xonxoff=False,
            # rtscts=False,
            # dsrdtr=False)

        # self._initialize()

        # # create comm process
        # self.comm_process = mp.Process(
            # target=self.comm,
            # args=(
                # self._thermostat,
                # self._pid_kp,
                # self._pid_ki,
                # self._pid_kd,
                # self._heater_bangbang_segments,
                # self.update_data_event,))
        # self.comm_process.daemon = True
        # self.comm_process.start()
        # # create timer process that counts down time_remaining
        # self.time_process = mp.Process(
            # target=self.timer,
            # args=(
                # self.state_transition_event,))
        # self.time_process.daemon = True
        # self.time_process.start()
        # # EXTREMELY IMPORTANT - for this to work at all in Windows,
        # # where the above processes are spawned (vs forked in Unix),
        # # the thread objects (as sattributes of this object) must be
        # # assigned to this object AFTER we have spawned the processes.
        # # That way, multiprocessing can pickle the freshroastsr700 
        # # successfully. (It can't pickle thread-related stuff.)
        # if self.update_data_func is not None:
            # # Need to launch the thread that will listen to the event
            # self.create_update_data_system(None, setFunc=False, createThread=True)
            # self.update_data_thread.start()
        # if self.state_transition_func is not None:
            # # Need to launch the thread that will listen to the event
            # self.create_state_transition_system(None, setFunc=False, createThread=True)
            # self.state_transition_thread.start()

    def auto_connect(self):
        """Starts a thread that will automatically connect to the roaster when
        it is plugged in."""
        self._connected.value = 0
        # self.auto_connect_thread = threading.Thread(target=self._auto_connect)
        # self.auto_connect_thread.start()
        # tell comm process to attempt connection
        self._attempting_connect.value = 1

        # EXTREMELY IMPORTANT - for this to work at all in Windows,
        # where the above processes are spawned (vs forked in Unix),
        # the thread objects (as sattributes of this object) must be
        # assigned to this object AFTER we have spawned the processes.
        # That way, multiprocessing can pickle the freshroastsr700 
        # successfully. (It can't pickle thread-related stuff.)
        if self.update_data_func is not None:
            # Need to launch the thread that will listen to the event
            self.create_update_data_system(None, setFunc=False, createThread=True)
            self.update_data_thread.start()
        if self.state_transition_func is not None:
            # Need to launch the thread that will listen to the event
            self.create_state_transition_system(None, setFunc=False, createThread=True)
            self.state_transition_thread.start()
        
    def _auto_connect(self):
        """Attempts to connect to the roaster every quarter of a second."""
        while(self._cont.value):
            try:
                self._connect()
                self._connected.value = 1
                break
            except exceptions.RoasterLookupError:
                time.sleep(.25)
       
    def disconnect(self):
        """Stops the communication loop to the roaster. Note that this will not
        actually stop the roaster itself, but will allow the program to exit
        cleanly."""
        self._cont.value = 0

    def comm(self, thermostat=False,
             kp=0.06, ki=0.0075, kd=0.01,
             heater_segments=8, update_data_event=None):
        """Main communications loop to the roaster. If the packet is not 14
        bytes exactly, the packet will not be opened. If an update data
        function is available, it will be called when the packet is opened."""
        # waiting for command to attempt connect
        while self._attempting_connect.value == 0:
            time.sleep(0.25)
        # we got the command to attempt to connect
        # reset flag
        self._attempting_connect.value = 0
        # attempt connection
        # this call will block until a connection is achieved
        self._auto_connect()
        
        # we are connected!
        
        # initialize thermal model
        model = ThermalModel()
        # Initialize PID controller if thermostat function was specified at
        # init time
        pidc = None
        heater = None
        if(thermostat):
            pidc = pid.PID(kp, ki, kd,
                           Output_max=heater_segments,
                           Output_min=0
                           )
            heater = heat_controller(number_of_segments=heater_segments)

        # loop for as long as no one calls disconnect()
        while(self._cont.value):
            start = datetime.datetime.now()
            # write to device
            if self.get_roaster_state() == 'roasting':
                self.current_temp = int(round(model.update(self.heat_setting)))
            else:
                self.current_temp = int(round(model.update(0)))

            # read from device
            # done, pulled current_temp from model

            # next, PID controller calcs when roasting.
            if thermostat:
                if 'roasting' == self.get_roaster_state():
                    if heater.about_to_rollover():
                        # it's time to use the PID controller value
                        # and set new output level on heater!
                        output = pidc.update(
                            self.current_temp, self.target_temp)
                        heater.heat_level = output
                        # make this number visible to other processes...
                        self._heater_level.value = heater.heat_level
                    # read bang-bang heater output array element and apply it
                    if heater.generate_bangbang_output():
                        # ON
                        self.heat_setting = 3
                    else:
                        # OFF
                        self.heat_setting = 0
                else:
                    # for all other states, heat_level = OFF
                    heater.heat_level = 0
                    # make this number visible to other processes...
                    self._heater_level.value = heater.heat_level
                    self.heat_setting = 0

            # calculate sleep time to stick to 0.25sec period
            comp_time = datetime.datetime.now() - start
            sleep_duration = 0.25 - comp_time.total_seconds()
            if sleep_duration > 0:
                time.sleep(sleep_duration)

    def timer(self, state_transition_event=None):
        """Timer loop used to keep track of the time while roasting or
        cooling. If the time remaining reaches zero, the roaster will call the
        supplied state transistion function or the roaster will be set to
        the idle state."""
        while(self._cont.value):
            state = self.get_roaster_state()
            if(state == 'roasting' or state == 'cooling'):
                time.sleep(1)
                self.total_time += 1
                if(self.time_remaining > 0):
                    self.time_remaining -= 1
                else:
                    if(state_transition_event is not None):
                        state_transition_event.set()
                    else:
                        self.idle()
            else:
                time.sleep(0.01)

    def get_roaster_state(self):
        """Returns a string based upon the current state of the roaster. Will
        raise an exception if the state is unknown."""
        value = self._current_state.value
        if(value == b'\x02\x01'):
            return 'idle'
        elif(value == b'\x04\x04'):
            return 'cooling'
        elif(value == b'\x08\x01'):
            return 'sleeping'
        # handle null bytes as empty strings
        elif(value == b'\x00\x00' or value == b''):
            return 'connecting'
        elif(value == b'\x04\x02'):
            return 'roasting'
        else:
            return 'unknown'

    def idle(self):
        """Sets the current state of the roaster to idle."""
        self._current_state.value = b'\x02\x01'

    def roast(self):
        """Sets the current state of the roaster to roast and begins
        roasting."""
        self._current_state.value = b'\x04\x02'

    def cool(self):
        """Sets the current state of the roaster to cool. The roaster expects
        that cool will be run after roast, and will not work as expected if ran
        before."""
        self._current_state.value = b'\x04\x04'

    def sleep(self):
        """Sets the current state of the roaster to sleep. Different than idle
        in that this will set double dashes on the roaster display rather than
        digits."""
        self._current_state.value = b'\x08\x01'


class heat_controller(object):
    """A class to do gross-level pulse modulation on a bang-bang interface."""
    def __init__(self, number_of_segments=8):
        # num_segments determines how many time samples are used to produce
        # the output.  This effectively translates to a number of output
        # levels on the bang-bang controller.  If number_of_segments == 8,
        # for example, then, possible output 'levels' are 0,1,2,...7.
        # Depending on the output
        # rate and the load's time constant, the result could be perceived
        # as discrete lumps rather than an effective average output.
        # higer rate of output is better than slower.
        # This code does not attempt to control the rate of output,
        # that is left to the caller.
        self._num_segments = number_of_segments
        self._output_array = [[0 for x in range(self._num_segments)]
                              for x in range(1+self._num_segments)]
        # I'm sure there's a great way to do this algorithmically for
        # all possible num_segments...
        if 4 == self._num_segments:
            self._output_array[0] = [False, False, False, False]
            self._output_array[1] = [True, False, False, False]
            self._output_array[2] = [True, False, True, False]
            self._output_array[3] = [True, True, True, False]
            self._output_array[4] = [True, True, True, True]
        elif 8 == self._num_segments:
            self._output_array[0] = [False, False, False, False,
                                     False, False, False, False]
            self._output_array[1] = [True, False, False, False,
                                     False, False, False, False]
            self._output_array[2] = [True, False, False, False,
                                     True, False, False, False]
            self._output_array[3] = [True, False, False, True,
                                     False, False, True, False]
            self._output_array[4] = [True, False, True, False,
                                     True, False, True, False]
            self._output_array[5] = [True, True, False, True,
                                     True, False, True, False]
            self._output_array[6] = [True, True, True, False,
                                     True, True, True, False]
            self._output_array[7] = [True, True, True, True,
                                     True, True, True, False]
            self._output_array[8] = [True, True, True, True,
                                     True, True, True, True]
        else:
            # note that the most effective pulse modulation is one where
            # ones and zeroes are as temporarily spread as possible.
            # Example, for a 4-segment output,
            # [1,1,0,0] is not as effective as/lumpier than
            # [1,0,1,0], even though they supply the same energy.
            # If the output rate is much greater than the load's time constant,
            # this difference will not be percpetible.
            # Here, we're just stuffing early slots with ones... lumpier
            for i in range(1+self._num_segments):
                for j in range(self._num_segments):
                    self._output_array[i][j] = j < i
        # prepare for output
        self._heat_level = 0
        self._heat_level_now = 0
        self._current_index = 0

    @property
    def heat_level(self):
        """The desired output level."""
        return self._heat_level

    @heat_level.setter
    def heat_level(self, value):
        """Set the desired output level. """
        if value < 0:
            self._heat_level = 0
        elif round(value) > self._num_segments:
            self._heat_level = self._num_segments
        else:
            self._heat_level = int(round(value))

    def generate_bangbang_output(self):
        """Generates the latest on or off pulse in
           the string of on (True) or off (False) pulses
           according to the desired heat_level.  Successive calls
           to this function will return the next value in the
           on/off array series.  Call this at control loop rate to
           obtain the necessary on/off pulse train.
           This system will not work if the caller expects to be able
           to specify a new heat_level at every control loop iteration.
           Only the value set at every number_of_segments iterations
           will be picked up for output!"""
        if self._current_index >= self._num_segments:
            # we're due to switch over to the next
            # commanded heat_level
            self._heat_level_now = self._heat_level
            # reset array index
            self._current_index = 0
        # return output
        out = self._output_array[self._heat_level_now][self._current_index]
        self._current_index += 1
        return out

    def about_to_rollover(self):
        """This method indicates that the next call to generate_bangbang_output
           is a wraparound read.  Use this to determine if it's time to
           run the PID controller iteration again."""
        return self._current_index >= self._num_segments


class ThermalModel(object):

    def __init__(self,sample_period=0.25,tau=30.0):
        self.A = math.exp(-sample_period/tau)
        self.B = 1.0 - self.A
        self.pv = 72.0
        self.pv_last = 72.0
        pass

    def update(self, heat_level):
        """ call this at the sample rate."""
        # super-simple thermal model for the bang-bang controller, of the form
        # PV(n+1) = A * PV(n) + (1-A) * (550 or 72)
        # A = e^(sample_period/tau)
        if heat_level == 3:
            target = 550.0
        elif heat_level == 2:
            target = 480.0
        elif heat_level == 1:
            target = 425.0
        else:
            target = 72.0
        self.pv = self.A * self.pv_last + self.B * target
        self.pv_last = self.pv
        if self.pv < 150.0:
            return 150.0
        else:
            return self.pv
