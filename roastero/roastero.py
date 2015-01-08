#!/usr/bin/env python3
# Name: roastero.py
# Authors: Mark Spicer, Caleb Coffie
# Purpose: Cross-Platform advanced roaster

# Import necessary modules.
from tkinter import *
from tkinter import ttk

class gui:
    def __init__(self):
        # Define class variables.
        self.bgColor = "#2e3138"

        # Define root window.
        self.root = Tk()
        self.root.title("Roastero")
        self.root.geometry("800x500")

        # Create the widgets to fill root window.
        self.createWidgets()

        # Run the gui.
        self.root.mainloop()

    def createWidgets(self):
        # Create tab widget.
        self.tabs = ttk.Notebook(self.root, width=800, height=500)

        # Define tab pages.
        self.roast = ttk.Frame(self.tabs)
        self.recipes = ttk.Frame(self.tabs)
        self.log = ttk.Frame(self.tabs)

        # Label the tabs.
        self.tabs.add(self.roast, text='Roast')
        self.tabs.add(self.recipes, text='Recipes')
        self.tabs.add(self.log, text='Log')

        # Load the content of each tab.
        self.recipesTab()
        self.logTab()
        self.roastTab()

        # Add the tabs to the main window.
        self.tabs.pack(fill=BOTH, expand=True)

    def roastTab(self):
        self.button = Button(self.roast, text="Roast!")
        self.button.grid()

    def recipesTab(self):
        self.button = Button(self.recipes, text="recipes!")
        self.button.grid()

    def logTab(self):
        self.button = Button(self.log, text="log!")
        self.button.grid()


roastero = gui()
