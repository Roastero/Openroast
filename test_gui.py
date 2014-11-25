#!/usr/bin/env python

# Import neccessary modules.
from Tkinter import *

# Set root window.
master = Tk()
master.title("Roastero")

# Define roast setting label
Label(master, text="Roast Setting").grid(row=0, column=0, sticky=W)

# Set initial value of the roast dropdown
roastInitial = StringVar(master)
roastInitial.set("Cool")

# Configure roast setting dropdown
roastSetting = OptionMenu(master, roastInitial, "Cool", "Low", "Medium", "High")
roastSetting.grid(row=0, column=1, sticky=W)

# Define the fan speed label
fanLabel = Label(master, text="Fan Speed")
fanLabel.grid(row=1, column=0, sticky=W)

# Set initial values of the fan speed dropdown
fanInitial = StringVar(master)
fanInitial.set(1)

# Configure the fan speed dropdown
fanSpeed = OptionMenu(master, fanInitial, 1, 2, 3, 4, 5, 6, 7, 8, 9)
fanSpeed.grid(row=1, column=1, sticky=W)

# Define the time speed label
timeLabel = Label(master, text="Time")
timeLabel.grid(row=2, column=0, sticky=W)

# Define time text input
timeSetting = Entry(master)
timeSetting.grid(row=2, column=1, sticky=W)

def startRoast():
    print "click!"

roastButton = Button(master, text="Submit", command=startRoast)
roastButton.grid(row=3, column=0)

roastButton = Button(master, text="Idle", command=startRoast)
roastButton.grid(row=3, column=1)

roastButton = Button(master, text="Roast", command=startRoast)
roastButton.grid(row=4, column=0)

roastButton = Button(master, text="Cool", command=startRoast)
roastButton.grid(row=4, column=1)

roastButton = Button(master, text="Standby", command=startRoast)
roastButton.grid(row=5, column=0)

roastButton = Button(master, text="Exit", command=startRoast)
roastButton.grid(row=5, column=1)


# Run the main graphics loop.
mainloop()
