#!/usr/bin/env python
# Name: FreshRoastSR700.py
# Authors: Mark Spicer, Caleb Coffie
# Purpose: A class to interface with the Fresh Roast SR700 coffee roaster.

# Standard Library Imports
import threading, sys, serial, struct, time, binascii

# Local project imports
from ..tools.SerialPortFinder import *
from ..tools.pid import *
from .Roaster import Roaster

# Define FreshRoastSR700 class.
class FreshRoastSR700(Roaster):
    def __init__(self):
        super().__init__()

        # Define variables for roaster settings.
        self.header = b'\xAA\xAA'   # 2 byte hex value
        self.id = b'\x61\x74'       # 2 byte hex value, does not change
        self.flags = b'\x63'        # 1 byte hex value
        self.currentState = b''     # 2 byte hex value
        self.fanSpeed = 0           # Int from 0 to 9
        self.heatSetting = 0        # Int from 0 to 3
        self.footer = b'\xAA\xFA'   # 2 byte hex value, does not change
        self.time = 0.0             # Decimal of minutes to be sent to roaster
        self.currentTemp = 150      # Set base temp

        # Additional variables
        self.program = []           # A list used to hold the roast program

        autoConnectThread = threading.Thread(target=self.auto_connect_thread, args=(5,))
        self.threads.append(autoConnectThread)
        autoConnectThread.daemon = True
        autoConnectThread.start()

    def gen_packet(self, header=None, id=None, flags=None, currentState=None,
        fanSpeed=None, time=None, heatSetting=None, footer=None):

        header = header or self.header
        id = id or self.id
        flags = flags or self.flags
        currentState = currentState or self.currentState
        fanSpeed = fanSpeed or self.fanSpeed
        time = time or self.time
        heatSetting = heatSetting or self.heatSetting
        footer = footer or self.footer

        # Return packet in byte format.
        # print(type(footer))
        return (header + id + flags + currentState +
            fanSpeed.to_bytes(1, byteorder='big') +
            int(float(time * 10)).to_bytes(1, byteorder='big') +
            heatSetting.to_bytes(1, byteorder='big') +
            b'\x00\x00' + footer)

    def open_packet(self, message):
        # Check if the temperature is lower than 150 and set accordingly.
        if(bytes(message[10:-2]) == (b'\xff\x00')):
            self.currentTemp = 150
        else:
            self.currentTemp = int.from_bytes(bytes(message[10:-2]), byteorder='big')
            # print(int.from_bytes(bytes(message[10:-2]), byteorder='big'))

    def send_packet(self, message):
        # try:
        self.ser.write(message)
        # except:
        #     autoConnectThread = threading.Thread(target=self.auto_connect_thread, args=(5,))
        #     self.threads.append(autoConnectThread)
        #     autoConnectThread.daemon = True
        #     autoConnectThread.start()

    def recv_packet(self):
        # try:
        return self.ser.read(14)
        # except:
        #     autoConnectThread = threading.Thread(target=self.auto_connect_thread, args=(5,))
        #     self.threads.append(autoConnectThread)
        #     autoConnectThread.daemon = True
        #     autoConnectThread.start()

    def initialize(self):
        # Set initial values of the roaster.
        header = b'\xAA\x55'
        flags = b'\x63'
        currentState = b'\x00\x00'
        fanSpeed = 0
        time = 0.0
        heatSetting = 0

        # Generate the initial message and send it
        message = self.gen_packet(header=header, flags=flags,
            currentState=currentState, fanSpeed=fanSpeed, time=time,
            heatSetting=heatSetting)
        # print(' '.join(map('{:02X}'.format, message))) # Print Statement to debug comm
        self.send_packet(message)

    def get_program(self):
        self.program = []
        r = self.recv_packet()
        while(str(r)[14:-35] != "af"):
            r = self.recv_packet()
            self.program.append(r)

    def get_current_temp(self):
        return self.currentTemp

    def get_target_temp(self):
        return self.targetTemp

    def set_target_temp(self, temp):
        self.targetTemp = temp

    def idle(self):
        self.currentState = b'\x02\x01'

    def roast(self):
        self.currentState = b'\x04\x02'

    def cool(self):
        self.currentState = b'\x04\x04'

    def sleep(self):
        self.currentState = b'\x08\x01'

    def set_fan_speed(self,speed):
        self.fanSpeed = speed

    def get_fan_speed(self):
        return self.fanSpeed

    def set_heat_setting(self,setting):
        self.heatSetting = setting

    def get_current_status(self):
        if(self.currentState == b'\x04\x02'):
            return 1 # Roasting

        elif(self.currentState == b'\x04\x04'):
            return 2 # Cooling

        elif(self.currentState == b'\x08\x01' or
            self.currentState == b'\x02\x01'):
            return 3 # Idle or Sleeping

    def comm(self, threadNum):
        while(self.cont == True):
            s = self.gen_packet()
            # print(' '.join(map('{:02X}'.format, s))) # Print Statement to debug comm
            self.send_packet(s)
            r = self.recv_packet()

            # Check if valid packet
            if len(r) == 14:
                # The packet is good
                self.open_packet(r)

                # Control rate at which packets are sent.
                time.sleep(.25)
            else:
                # Bad packet reintialize
                print("Yo Hardware bad.")
                self.initialize()
                self.get_program()


    def run(self):
        # Attempt to make a serial connection several times.
        for x in range(1,6):
            self.initialize()

        # Get the program from the roaster.
        self.get_program()

        # Set the inital state of the roaster to idle.
        self.idle()
        self.set_fan_speed(1)

        # Run the parents class run method.
        super().run()

    def timer(self):
        super().timer()

        # Set timer on roaster
        if (self.sectionTime <= 594):
            self.time = self.sectionTime / 60
        else:
            self.time = 9.9

    def cooling_phase(self, coolTime=180):
        # Set to roast phase briefly to allow cooling phase to begin.
        if(self.get_current_status() == 3):
            self.roast()
            time.sleep(.25)

        # Begin cooling phase.
        self.cool()
        self.set_heat_setting(0)
        self.set_target_temp(150)
        self.set_fan_speed(9)
        self.set_section_time(coolTime)

    def thermostat(self, p):
        while(True):
            # Get updated output from PID function.
            output = p.update(self.currentTemp, self.targetTemp)

            #print("P:", self.pro, "I:", self.i, "D:", self.d, " - ", output)

            """ This is the core roasting logic. Handle with care! The top
            level if case checks to see what the target temperature is, and
            then determines what the lowest heatsetting the roaster should be
            set at to handle that temperature. The next level will then handle
            the PID values to determine a heat setting. """
            if(self.targetTemp >= 460):
                if(output >= 30):
                    self.set_heat_setting(3)
                else:
                    if(self.heatSetting == 2):
                        self.set_heat_setting(3)
                    else:
                        self.set_heat_setting(2)
            elif(self.targetTemp >= 430):
                if(output >= 30):
                    self.set_heat_setting(3)
                elif(output >= 20):
                    self.set_heat_setting(2)
                else:
                    if(self.heatSetting == 1):
                        self.set_heat_setting(2)
                    else:
                        self.set_heat_setting(1)
            elif(self.targetTemp >= 350):
                if(output >= 30):
                    self.set_heat_setting(3)
                elif(output >= 20):
                    self.set_heat_setting(2)
                elif(output >= 10):
                    self.set_heat_setting(1)
                else:
                    if(self.heatSetting == 0):
                        self.set_heat_setting(1)
                    else:
                        self.set_heat_setting(0)
            else:
                if(output >= 30):
                    self.set_heat_setting(3)
                elif(output >= 20):
                    self.set_heat_setting(2)
                elif(output >= 10):
                    self.set_heat_setting(1)
                else:
                    self.set_heat_setting(0)

            time.sleep(.25)

    def auto_connect_thread(self, threadNum):
        # Attempt to make a connection to the roaster until it finds the device.
        while(True):
            try:
                vid_pid_to_serial_url("1A86:5523")
                break
            except LookupError:
                continue

            time.sleep(1)

        # Open serial connection to roaster.
        self.ser = serial.Serial(port=vid_pid_to_serial_url("1A86:5523"),
                                baudrate=9600,
                                bytesize=8,
                                parity='N',
                                stopbits=1.5,
                                timeout=.25,
                                xonxoff=False,
                                rtscts=False,
                                writeTimeout=None,
                                dsrdtr=False,
                                interCharTimeout=None
        )

        # Set the connected variable to true if a serial connection is made.
        if self.ser:
            self.connected = True

        self.run()

    def __del__(self):
        self.sleep()
        time.sleep(1)
        try:
            self.ser.close()
        except:
            pass
