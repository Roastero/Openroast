import time                         # Used for the count down timer.
import threading                    # Used to create threads.


class Roaster:
    def __init__(self):
        self.currentTemp = 0        # Int in degrees Fahrenheit
        self.targetTemp = 0
        self.sectionTime = 0
        self.totalTime = 0
        self.connected = False

        # Thread control variables
        self.cont = True            # True or False, used to exit program
        self.threads = []           # A list used to keep track of threads

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

    def timer(self):
        if(self.get_current_status() == 1 or self.get_current_status() == 2):
            time.sleep(1)
            self.totalTime += 1
            if(self.sectionTime > 0):
                self.sectionTime -= 1
        if(self.get_current_status() == 2 and self.sectionTime == 0):
            self.idle()
        #RoastTab.update_section_time(self.sectionTime)

    def get_current_status(self):
        pass

    def comm(self, threadNum):
        pass

    def run(self):
        commThread = threading.Thread(target=self.comm, args=(1,))
        self.threads.append(commThread)
        commThread.daemon = True
        commThread.start()

        timerThread = threading.Thread(target=self.timer_thread, args=(2,))
        self.threads.append(timerThread)
        timerThread.daemon = True
        timerThread.start()

        thermostatThread = threading.Thread(target=self.thermostat_thread, args=(3,))
        self.threads.append(thermostatThread)
        thermostatThread.daemon = True
        thermostatThread.start()

    def thermostat_thread(self, threadNum):
        while(True):
            self.thermostat()

    def thermostat(self):
        pass

    def __del__(self):
        self.cont = False
        self.threads[1].join()
