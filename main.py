#!/usr/bin/env python
# Name: main.py
# Authors: Mark Spicer, Caleb Coffie
# Purpose: Cross-Platform advanced roaster

# Import necessary modules.
import serial                   # Used for serial communications.
import binascii

# Open serial connection to roaster.
ser = serial.Serial(port='/dev/tty.wchusbserial1420',
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

start_string = b'\xAA\x55\x61\x74\x63\x00\x00\x00\x00\x00\x00\x00\xAA\xFA'
ser.write(start_string)

while(True):
    s = ser.read(14)
    print s.encode('hex')
    if (s.encode('hex')[3:5] == "af"):
        break

send_data = b'\xAA\xAA\x61\x74\x63\x02\x01\x01\x3B\x01\x00\x00\xAA\xFA'
ser.write(start_string)

ser.close()

#print binascii.b2a_uu(s)
