#!/usr/bin/env python
# Name: FreshRoastSR700.py
# Authors: Mark Spicer, Caleb Coffie
# Purpose: A class to interface with the Fresh Roast SR700 coffee roaster.

# Import necessary modules.
import serial                       # Used for serial communications.
import threading                    # Used to create threads.
import struct                       # Used to convert ints to two hex bytes.
import time                         # Used for the count down timer.

# Define FreshRoastSR700 class.
class FreshRoastSR700:
    def __init__(self):
        # Define variables for roaster settings.
        self.header = ''            # 2 byte hex value
        self.id = '\x61\x74'        # 2 byte hex value, does not change
        self.flags = ''             # 1 byte hex value
        self.currentState = ''      # 2 byte hex value
        self.fanSpeed = 0           # Int from 0 to 9
        self.time = 0.0             # Decimal from 0.0 to 9.9 minutes
        self.heatSetting = 0        # Int from 0 to 3
        self.CurrentTemp = 0        # Int in degrees Fahrenheit
        self.footer = '\xAA\xFA'    # 2 byte hex value, does not change

        # Additional variables
        self.program = []           # A list used to hold the roast program

        # Control variables
        self.cont = True            # True or False, used to exit program
        self.threads = []           # A list used to keep track of threads

        # Open serial connection to roaster.
        self.ser = serial.Serial(port='/dev/tty.wchusbserial1420',
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

    def genPacket(self):
        # Return packet in byte format.
        return (self.header + self.id + self.flags + self.currentState +
        chr(self.fanSpeed) + chr(int(self.time * 10)) + chr(self.heatSetting) +
        '\x00\x00' + self.footer)

    def openPacket(self, message):
        message = message.encode('hex')
        # self.flags = message[8:-18]
        # self.currentState = message[10:-14]
        # self.fanSpeed = message[14:-12]
        # self.time = message[16:-10]
        # self.heatSetting = message[16:-10]
        if (message[20:-6] == "ff"):
            self.temp = 0
        else:
            self.temp = int(message[20:-4],16)

    def sendPacket(self, message):
        self.ser.write(message)

    def recvPacket(self):
        return self.ser.read(14)

    def initialize(self):
        # Set initial values of the roaster.
        self.header = '\xAA\x55'
        self.flags = '\x63'
        self.currentState = '\x00\x00'
        self.fanSpeed = 0
        self.time = 0.0
        self.heatSetting = 0
        self.currentTemp = struct.pack('>H', 0)

        # Generate the initial message and send it
        message = self.genPacket()
        self.sendPacket(message)

        # Set the header back to the regular header for comm
        self.header = '\xAA\xAA'

    def getProgram(self):
        r = '\xAA'
        while(r.encode('hex')[8:-18] != "af"):
            r = self.recvPacket()
            self.program.append(r)

    def idle(self):
        self.currentState = '\x02\x01'

    def roast(self):
        self.currentState = '\x04\x02'

    def cool(self):
        self.currentState = '\x04\x04'

    def sleep(self):
        self.currentState = '\x08\x01'

    def setFanSpeed(self,speed):
        self.fanSpeed = speed

    def setHeatSetting(self,setting):
        self.heatSetting = setting

    def setTime(self,time):
        self.time = time

    def timer(self, threadNum):
        while(True):
            if (self.time > 0.0 and
                  (self.currentState == '\x04\x02' or
                  self.currentState == '\x04\x04')):
                    print "We are sleeping!!"
                    time.sleep(6)
                    self.time -= .1

            if(self.cont == False):
                break

    def comm(self, threadNum):
        while(True):
            s = self.genPacket()
            self.sendPacket(s)
            r = self.recvPacket()
            print "revieve!"
            self.openPacket(r)
            if(self.cont == False):
                break

    def run(self):
        self.initialize()
        self.getProgram()
        self.idle()

        commThread = threading.Thread(target=self.comm, args=(1,))
        self.threads.append(commThread)
        commThread.start()

        timerThread = threading.Thread(target=self.timer, args=(2,))
        self.threads.append(timerThread)
        timerThread.start()
