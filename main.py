#!/usr/bin/env python
# Name: main.py
# Authors: Mark Spicer, Caleb Coffie
# Purpose: Cross-Platform advanced roaster

# Import necessary modules.
from FreshRoastSR700 import FreshRoastSR700 # Import the Fresh roast class

# Create a Fresh Roast object and run it.
r = FreshRoastSR700()
r.run()

# Print menu and accept input.
while(True):
    print "-------------------"
    print "-----Main Menu-----"
    print "-------------------"
    print "1.) Set Fan"
    print "2.) Set Heat"
    print "3.) Set Time"
    print "4.) Idle"
    print "5.) Roast"
    print "6.) Cool"
    print "7.) Sleep"
    print "8.) Exit"

    choice = raw_input('> ')

    if (choice == '1'):
        speed = raw_input('Enter fan speed 0-9: ')
        r.setFanSpeed(int(speed))
    elif (choice == '2'):
        heat = raw_input('Enter heat 0-3: ')
        r.setHeatSetting(int(heat))
    elif (choice == '3'):
        time = raw_input('Enter time 0.0-9.9: ')
        r.setTime(float(time))
    elif (choice == '4'):
        r.idle()
    elif (choice == '5'):
        r.roast()
    elif (choice == '6'):
        r.cool()
    elif (choice == '7'):
        r.sleep()
    else:
        r.cont = False
        break
