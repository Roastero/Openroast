#!/usr/bin/env python3
# toggle a Tkinter button up/down
# using images and no button border
# tested with Python 2.7 and Python 3.2 by vegaseat
try:
    # Python2
    import Tkinter as tk
except ImportError:
    # Python3
    import tkinter as tk
def action(toggle=[True]):
    """
    toggle the button with up/down images,
    using a list element as static variable
    """
    if toggle[0]:
        button.config(image=image_down)
        toggle[0] = False
    else:
        button.config(image=image_up)
        toggle[0] = True

root = tk.Tk()
root.title("up/down button no border")
# pick GIF images you have in the working directory
# or give full path
image_up = tk.PhotoImage(file='../images/button.gif')
image_down = tk.PhotoImage(file='../images/button.gif')
# create a button to display the image
# use bd or borderwidth zero for no border
# start with button image up
button = tk.Button(root, image=image_up, bd=0, command=action)
# position the widgets
button.grid(row=0, column=0)
root.mainloop()
