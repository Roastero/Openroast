#!/usr/bin/env python
# Name: FreshRoastSR700.py
# Authors: Mark Spicer, Caleb Coffie
# Purpose: A class to interface with the Fresh Roast SR700 coffee roaster.

# Import necessary modules.
import threading
import sys
import serial                       # Used for serial communications.
import struct                       # Used to convert ints to two hex bytes.
import time                         # Used for the count down timer.
from ..tools.SerialPortFinder import *    # Import Serial port finder
from ..tools.pid import *
import binascii
from .Roaster import Roaster


# Define FreshRoastSR700 class.
class FreshRoastSR700(Roaster):
    def __init__(self):
        super().__init__()

        # Define variables for roaster settings.
        self.header = ''            # 2 byte hex value
        self.id = b'\x61\x74'       # 2 byte hex value, does not change
        self.flags = ''             # 1 byte hex value
        self.currentState = ''      # 2 byte hex value
        self.fanSpeed = 0           # Int from 0 to 9
        self.heatSetting = 0        # Int from 0 to 3
        self.footer = b'\xAA\xFA'   # 2 byte hex value, does not change
        self.time = 0.0             # Decimal of minutes to be sent to roaster

        # Additional variables
        self.program = []           # A list used to hold the roast program

        autoConnectThread = threading.Thread(target=self.auto_connect_thread, args=(5,))
        self.threads.append(autoConnectThread)
        autoConnectThread.daemon = True
        autoConnectThread.start()

    def gen_packet(self):
        # Return packet in byte format.
        return (self.header + self.id + self.flags + self.currentState +
        self.fanSpeed.to_bytes(1, byteorder='big') +
        int(float(self.time * 10)).to_bytes(1, byteorder='big') +
        self.heatSetting.to_bytes(1, byteorder='big') +
        b'\x00\x00' + self.footer)

    def open_packet(self, message):
        # Check if the temperature is lower than 150 and set accordingly.
        if(bytes(message[10:-2]) == (b'\xff\x00')):
            self.currentTemp = 150
        else:
            self.currentTemp = int.from_bytes(bytes(message[10:-2]), byteorder='big')

    def send_packet(self, message):
        self.ser.write(message)

    def recv_packet(self):
        return self.ser.read(14)

    def initialize(self):
        # Set initial values of the roaster.
        self.header = b'\xAA\x55'
        self.flags = b'\x63'
        self.currentState = b'\x00\x00'
        self.fanSpeed = 0
        self.time = 0.0
        self.heatSetting = 0
        self.currentTemp = 150

        # Generate the initial message and send it
        message = self.gen_packet()
        self.send_packet(message)

        # Set the header back to the regular header for comm
        self.header = b'\xAA\xAA'

    def get_program(self):
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
            self.send_packet(s)
            r = self.recv_packet()
            self.open_packet(r)

            # Control rate at which packets are sent.
            time.sleep(.25)

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

        # Begin roast phase.
        self.roast()
        self.cool()
        self.set_heat_setting(0)
        self.set_target_temp(150)
        self.set_fan_speed(9)
        self.set_section_time(coolTime)

    def thermostat(self, p):
        while(True):
            # Get updated output from PID function.
            output = p.update(self.currentTemp, self.targetTemp)

            # Add additional settings so that there are seven isntead of four.
            if(output >= 3.0):
                self.set_heat_setting(3)
            elif(output >= 2.5):
                self.set_heat_setting(3)
                time.sleep(.25)
                self.set_heat_setting(2)
            elif(output >= 2.0):
                self.set_heat_setting(2)
            elif(output >= 1.5):
                self.set_heat_setting(2)
                time.sleep(.25)
                self.set_heat_setting(1)
            elif(output >= 1.0):
                self.set_heat_setting(1)
            elif(output >= 0.5):
                self.set_heat_setting(1)
                time.sleep(.25)
                self.set_heat_setting(0)
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
                                timeout=None,
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
