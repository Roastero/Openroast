#!/usr/bin/env python
# Name: FreshRoastSR700.py
# Authors: Mark Spicer, Caleb Coffie
# Purpose: A class to interface with the Fresh Roast SR700 coffee roaster.

# Import necessary modules.
import serial                       # Used for serial communications.
import threading                    # Used to create threads.
import struct                       # Used to convert ints to two hex bytes.
import time                         # Used for the count down timer.
from ..tools.SerialPortFinder import *    # Import Serial port finder
import binascii

# Define FreshRoastSR700 class.
class FreshRoastSR700:
    def __init__(self):
        # Define variables for roaster settings.
        self.header = ''            # 2 byte hex value
        self.id = b'\x61\x74'        # 2 byte hex value, does not change
        self.flags = ''             # 1 byte hex value
        self.currentState = ''      # 2 byte hex value
        self.fanSpeed = 0           # Int from 0 to 9
        self.time = 0.0             # Decimal from 0.0 to 9.9 minutes
        self.heatSetting = 0        # Int from 0 to 3
        self.currentTemp = 0        # Int in degrees Fahrenheit
        self.footer = b'\xAA\xFA'    # 2 byte hex value, does not change

        # Additional variables
        self.program = []           # A list used to hold the roast program

        # Control variables
        self.cont = True            # True or False, used to exit program
        self.threads = []           # A list used to keep track of threads

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
        int(self.time * 10).to_bytes(1, byteorder='big') +
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
            self.currentTemp = message[10:-2][1]
            print(message[10:-2][1])
        print(message)
        print(message[10:-2])

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
        self.currentTemp = struct.pack('>H', 0)

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

    def set_time(self,time):
        self.time = time

    def timer(self, threadNum):
        while(self.cont == True):
            time.sleep(6)
            if (self.time > 0.0 and
                  (self.currentState == b'\x04\x02' or
                  self.currentState == b'\x04\x04')):
                    self.time -= .1
            elif self.time == 0.0 and self.currentState == b'\x04\x04':
                self.idle()

    def comm(self, threadNum):
        while(self.cont == True):
            s = self.gen_packet()
            self.send_packet(s)
            r = self.recv_packet()
            self.open_packet(r)

            # Control rate at which packets are sent.
            time.sleep(.25)

    def run(self):
        for x in range(1,5):
            self.initialize()
        self.get_program()
        self.idle()

        commThread = threading.Thread(target=self.comm, args=(1,))
        self.threads.append(commThread)
        commThread.daemon = True
        commThread.start()

        timerThread = threading.Thread(target=self.timer, args=(2,))
        self.threads.append(timerThread)
        timerThread.daemon = True
        timerThread.start()

    def cooling_phase(self, time):
        self.cool()
        self.set_heat_setting(0)
        self.set_fan_speed(9)
        self.set_time(time)

    def __del__(self):
        self.cont = False
        self.threads[1].join()
        self.ser.close()
