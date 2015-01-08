from tkinter import *
import tkinter as tk
class recipesTab(tk.Frame):
    def __init__(self, parent, root):
        tk.Frame.__init__(self,parent)
        label = Label(self, text="recipes")
        label.pack(pady=10,padx=10)
