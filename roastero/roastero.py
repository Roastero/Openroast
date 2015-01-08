#!/usr/bin/env python
# Name: roastero.py
# Authors: Mark Spicer, Caleb Coffie
# Purpose: Cross-Platform advanced roaster

# Import necessary modules.
import roaster_libraries    # Import the Fresh roast class
try:
    from tkinter import *
except ImportError:
    from Tkinter import *
from PIL import Image, ImageTk
import time


############################# Functions ########################################
r = ""

def adjustRoasterType(*args):
    roaster = roasterType.get()

    # Determine the appropriate roaster type.
    if(roaster == "Fresh Roast SR700"):
        global r
        r = roaster_libraries.FreshRoastSR700()
        r.run()

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

def idle(*args):
    r.idle()

def roast(*args):
    r.roast()

def cool(*args):
    r.cool()

def sleep(*args):
    r.sleep()

def disconnect(*args):
    r.__del__()

def update_timeText():
    # Get the current time, note you can change the format as you wish
    current = time.strftime("%H:%M:%S")
    # Update the timeText Label box with the current time
    timeText.configure(text=current)
    # Call the update_timeText() function after 1 second
    root.after(1000, update_timeText)

################################ GUI ###########################################
# Variables.
backgroundColor = "#4a4a4a"

# Set root window.
root = Tk()
root.title("Roastero")
root.configure(background=backgroundColor)
# root.geometry("500x500")

# im = Image.open('Test1.png')
# tkimage = ImageTk.PhotoImage(im)
# myvar= Label(root,image = tkimage)
# myvar.place(x=0, y=0, relwidth=1, relheight=1)


roasterTypeLabel = Label(root, text="Roaster Type", background=backgroundColor)
roasterTypeLabel.grid(row=0, column=0, sticky=W)

roasterType = StringVar(root)
roasterType.set("Fresh Roast SR700")

roasterTypeDrop = OptionMenu(root, roasterType, "Fresh Roast SR700")
roasterTypeDrop.grid(row=0, column=1, sticky=W)
roasterTypeDrop.configure(background=backgroundColor)

connectButton = Button(root, text="Connect", command=adjustRoasterType, highlightbackground=backgroundColor)
connectButton.grid(row=0, column=2)

disconnectButton = Button(root, text="Disconnect", command=disconnect, highlightbackground=backgroundColor)
disconnectButton.grid(row=0, column=3)

# Define roast setting label
roastLabel = Label(root, text="Roast Setting", background=backgroundColor)
roastLabel.grid(row=1, column=0, sticky=W)

# Set initial value of the roast dropdown
roastSetting = StringVar(root)
roastSetting.set("Cool")
roastSetting.trace("w", adjustRoastSetting)

# Configure roast setting dropdown
roastDrop = OptionMenu(root, roastSetting, "Cool", "Low", "Medium", "High")
roastDrop.grid(row=1, column=1, sticky=W)
roastDrop.configure(background=backgroundColor)

# Define the fan speed label
fanLabel = Label(root, text="Fan Speed", background=backgroundColor)
fanLabel.grid(row=2, column=0, sticky=W)

# Set variable of the fan speed dropdown.
fanSpeed = StringVar(root)
fanSpeed.set(1)
fanSpeed.trace("w", adjustFanSpeed)

# Configure the fan speed dropdown
fanDrop = OptionMenu(root, fanSpeed, 1, 2, 3, 4, 5, 6, 7, 8, 9)
fanDrop.grid(row=2, column=1, sticky=W)
fanDrop.configure(background=backgroundColor)

# Define the time speed label
timeLabel = Label(root, text="Time", background=backgroundColor)
timeLabel.grid(row=3, column=0, sticky=W)

# Define time text input
timeSetting = StringVar(root)
timeSetting.set(0)
timeSetting.trace("w", adjustTime)

timeDrop = OptionMenu(root, timeSetting, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
timeDrop.grid(row=3, column=1, sticky=E)
timeDrop.configure(background=backgroundColor)

# Define time text input
timeSetting02 = StringVar(root)
timeSetting02.set(0)
timeSetting02.trace("w", adjustTime)

timeDrop02 = OptionMenu(root, timeSetting02, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
timeDrop02.grid(row=3, column=1, sticky=W)
timeDrop02.configure(background=backgroundColor)

idleButton = Button(root, text="Idle", command=idle, highlightbackground=backgroundColor)
idleButton.grid(row=4, column=0)

roastButton = Button(root, text="Roast", command=roast, highlightbackground=backgroundColor)
roastButton.grid(row=4, column=1)

coolButton = Button(root, text="Cool", command=cool, highlightbackground=backgroundColor)
coolButton.grid(row=4, column=3)

standbyButton = Button(root, text="Standby", command=sleep, highlightbackground=backgroundColor)
standbyButton.grid(row=5, column=0)

quitButton = Button(root, text="Exit", command=root.quit, highlightbackground=backgroundColor)
quitButton.grid(row=5, column=1)


timeText = Label(root, text="", font=("Helvetica", 100), bg=backgroundColor)
timeText.grid(row=6, columnspan=4)
update_timeText()






# Run the main graphics loop.
root.mainloop()
