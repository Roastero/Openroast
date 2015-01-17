import time
import threading

class Roaster:
    def __init__(self):
        self.currentTemp = 0        # Int in degrees Fahrenheit
        self.targetTemp = 0         # Int in degrees Fahrenheit
        self.sectionTime = 0        # Int in seconds
        self.totalTime = 0          # Int in seconds
        self.connected = False      # Determines if roaster is connected.

        # Thread control variables
        self.cont = True            # True or False, used to exit program
        self.threads = []           # A list used to keep track of threads

    def run(self):
        # Start thread to communicate with the roasters serial connection.
        commThread = threading.Thread(target=self.comm, args=(1,))
        self.threads.append(commThread)
        commThread.daemon = True
        commThread.start()

        # Start thread to keep track of time.
        timerThread = threading.Thread(target=self.timer_thread, args=(2,))
        self.threads.append(timerThread)
        timerThread.daemon = True
        timerThread.start()

        # Start a thread to control the thermostat of the roaster.
        thermostatThread = threading.Thread(target=self.thermostat_thread, args=(3,))
        self.threads.append(thermostatThread)
        thermostatThread.daemon = True
        thermostatThread.start()

    def timer(self):
        # Count down during roast and cool phase.
        if(self.get_current_status() == 1 or self.get_current_status() == 2):
            time.sleep(1)
            self.totalTime += 1
            if(self.sectionTime > 0):
                self.sectionTime -= 1

        # When the roast is finished cooling, set roaster to idle.
        if(self.get_current_status() == 2 and self.sectionTime <= 0):
            self.idle()

    def set_section_time(self,time):
        self.sectionTime = time

    def get_section_time(self):
        return self.sectionTime

    def get_total_time(self):
        return self.totalTime

    def get_connection_status(self):
        return self.connected

    def timer_thread(self, threadNum):
        while(True):
            self.timer()

    def thermostat_thread(self, threadNum):
        while(True):
            time.sleep(.25)
            self.thermostat()

    def initialize(self):
        pass

    def get_current_temp(self):
        pass

    def get_target_temp(self):
        pass

    def set_target_temp(self):
        pass

    def idle(self):
        pass

    def get_current_status(self):
        pass

    def comm(self, threadNum):
        pass

    def thermostat(self):
        pass

    def __del__(self):
        self.cont = False
        self.threads[1].join()
