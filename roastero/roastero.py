#!/usr/bin/env python
# Name: main.py
# Authors: Mark Spicer, Caleb Coffie
# Purpose: Cross-Platform advanced roaster

# Import necessary modules.
from roaster_libraries.FreshRoastSR700 import FreshRoastSR700 # Import the Fresh roast class
try:
    import tkinter
except ImportError:
    import Tkinter as tkinter
from PIL import Image, ImageTk

def adjustFanSpeed(*args):
    r.setFanSpeed(int(fanSpeed.get()))

def adjustRoastSetting(*args):
    if(roastSetting.get() == "Low"):
        heat = 1
    elif(roastSetting.get() == "Medium"):
        heat = 2
    elif(roastSetting.get() == "High"):
        heat = 3
    else:
        heat = 0

    r.setHeatSetting(int(heat))

def adjustTime(*args):
    time = timeSetting.get() + "." + timeSetting02.get()
    r.setTime(float(time))

# Create a Fresh Roast object and run it.
r = FreshRoastSR700()
r.run()

backgroundColor = "#4a4a4a"

# Set root window.
master = Tk()
master.title("Roastero")
master.configure(background=backgroundColor)
# master.geometry("500x500")

# im = Image.open('Test1.png')
# tkimage = ImageTk.PhotoImage(im)
# myvar= Label(master,image = tkimage)
# myvar.place(x=0, y=0, relwidth=1, relheight=1)


# Define roast setting label
roastLabel = Label(master, text="Roast Setting", background=backgroundColor)
roastLabel.grid(row=0, column=0, sticky=W)

# Set initial value of the roast dropdown
roastSetting = StringVar(master)
roastSetting.trace("w", adjustRoastSetting)
roastSetting.set("Cool")

# Configure roast setting dropdown
roastDrop = OptionMenu(master, roastSetting, "Cool", "Low", "Medium", "High")
roastDrop.grid(row=0, column=1, sticky=W)
roastDrop.configure(background=backgroundColor)

# Define the fan speed label
fanLabel = Label(master, text="Fan Speed", background=backgroundColor)
fanLabel.grid(row=1, column=0, sticky=W)

# Set variable of the fan speed dropdown.
fanSpeed = StringVar(master)
fanSpeed.trace("w", adjustFanSpeed)
fanSpeed.set(1)

# Configure the fan speed dropdown
fanDrop = OptionMenu(master, fanSpeed, 1, 2, 3, 4, 5, 6, 7, 8, 9)
fanDrop.grid(row=1, column=1, sticky=W)
fanDrop.configure(background=backgroundColor)

# Define the time speed label
timeLabel = Label(master, text="Time", background=backgroundColor)
timeLabel.grid(row=2, column=0, sticky=W)

# Define time text input
timeSetting = StringVar(master)
timeSetting.set(0)
timeSetting.trace("w", adjustTime)

timeDrop = OptionMenu(master, timeSetting, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
timeDrop.grid(row=2, column=1, sticky=W)
timeDrop.configure(background=backgroundColor)

# Define time text input
timeSetting02 = StringVar(master)
timeSetting02.set(0)
timeSetting02.trace("w", adjustTime)

timeDrop02 = OptionMenu(master, timeSetting02, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
timeDrop02.grid(row=2, column=3, sticky=W)
timeDrop02.configure(background=backgroundColor)




idleButton = Button(master, text="Idle", command=r.idle, highlightbackground=backgroundColor)
idleButton.grid(row=3, column=0)

roastButton = Button(master, text="Roast", command=r.roast, highlightbackground=backgroundColor)
roastButton.grid(row=3, column=1)

coolButton = Button(master, text="Cool", command=r.cool, highlightbackground=backgroundColor)
coolButton.grid(row=3, column=3)

standbyButton = Button(master, text="Standby", command=r.sleep, highlightbackground=backgroundColor)
standbyButton.grid(row=4, column=0)

quitButton = Button(master, text="Exit", command=master.quit, highlightbackground=backgroundColor)
quitButton.grid(row=4, column=1)

# Run the main graphics loop.
master.mainloop()
