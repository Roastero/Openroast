from tkinter import *
import tkinter as tk
class roastTab(tk.Frame):
    def __init__(self, parent, root):
        tk.Frame.__init__(self,parent)
        label = Label(self, text="roast")
        label.pack(pady=10,padx=10)
