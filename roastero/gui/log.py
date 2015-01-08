from tkinter import *
import tkinter as tk
class logTab(tk.Frame):
    def __init__(self, parent, root):
        tk.Frame.__init__(self,parent)
        label = Label(self, text="log")
        label.pack(pady=10,padx=10)
