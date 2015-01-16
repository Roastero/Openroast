#!/usr/bin/env python
# Name: FreshRoastSR700.py
# Authors: Mark Spicer, Caleb Coffie
# Purpose: A class to interface with the Fresh Roast SR700 coffee roaster.

# Import necessary modules.
import serial                       # Used for serial communications.
import struct                       # Used to convert ints to two hex bytes.
import time                         # Used for the count down timer.
from ..tools.SerialPortFinder import *    # Import Serial port finder
import binascii
from .Roaster import Roaster


# Define FreshRoastSR700 class.
class FreshRoastSR700(Roaster):
    def __init__(self):
        super().__init__()
        # Define variables for roaster settings.
        self.header = ''            # 2 byte hex value
        self.id = b'\x61\x74'        # 2 byte hex value, does not change
        self.flags = ''             # 1 byte hex value
        self.currentState = ''      # 2 byte hex value
        self.fanSpeed = 0           # Int from 0 to 9
        self.heatSetting = 0        # Int from 0 to 3
        self.footer = b'\xAA\xFA'    # 2 byte hex value, does not change
        self.time = 0.0             # Decimal of minutes to be sent to roaster

        # Additional variables
        self.program = []           # A list used to hold the roast program

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

        # Run communications loop
        self.run()

    def gen_packet(self):
        # Return packet in byte format.
        return (self.header + self.id + self.flags + self.currentState +
        self.fanSpeed.to_bytes(1, byteorder='big') +
        int(float(self.time * 10)).to_bytes(1, byteorder='big') +
        self.heatSetting.to_bytes(1, byteorder='big') +
        b'\x00\x00' + self.footer)

    def open_packet(self, message):
        # self.flags = message[8:-18]
        # self.currentState = message[10:-14]
        # self.fanSpeed = message[14:-12]
        # self.time = message[16:-10]
        # self.heatSetting = message[16:-10]
        if (message[10:-2] == b'\xff\x00'):
            self.currentTemp = 150
        else:
            #self.currentTemp = int(re.sub('[^a-uy-z0-9]+', '', str(message[10:-2])[2:-1]), 16)
            #print (256*ord(message[10:-2]))
            print(message)

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
        self.currentTemp = b'\x00\x00'

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
            time.sleep(.20)

    def run(self):
        for x in range(1,6):
            self.initialize()
        self.get_program()
        self.idle()
        super().run()

    def timer(self):
        super().timer()
        # Set timer on roaster
        if (self.sectionTime <= 594):
            self.time = self.sectionTime / 60
        else:
            self.time = 9.9

    def cooling_phase(self, time=180):
        self.cool()
        self.set_heat_setting(0)
        self.set_fan_speed(9)
        self.set_section_time(time)

    def thermostat(self):
        if (self.get_current_status() == 1):
            if (self.currentTemp < self.targetTemp):
                self.set_heat_setting(3)
            elif (self.targetTemp < self.currentTemp):
                self.set_heat_setting(0)
            else:
                self.set_heat_setting(2)

    def __del__(self):
        self.ser.close()
