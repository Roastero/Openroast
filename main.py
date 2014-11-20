#!/usr/bin/env python
# Name: main.py
# Authors: Mark Spicer, Caleb Coffie
# Purpose: Cross-Platform advanced roaster

# Import necessary modules.
import serial                   # Used for serial communications.

# Open serial connection to roaster.
ser = serial.Serial(port=None,
                    baudrate=9600,
                    bytesize=EIGHTBITS,
                    parity=PARITY_NONE,
                    stopbits=STOPBITS_ONE_POINT_FIVE,
                    timeout=None,
                    xonxoff=True,
                    rtscts=False,
                    writeTimeout=None,
                    dsrdtr=False,
                    interCharTimeout=None
)
