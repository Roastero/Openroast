# Import necessary modules.
from tkinter import *
import tkinter as tk

# Import classes
from .log import logTab
from .recipes import recipesTab
from .roast import roastTab

class gui:
    def __init__(self):
        # Define class variables.
        self.bgColor = "white"

        # Define root window.
        self.root = Tk()
        self.root.title("Roastero")
        self.root.config(bg=self.bgColor)
        self.root.geometry("800x500")

        # Create the widgets to fill root window.
        self.createWidgets()

        # Run the gui.
        self.root.mainloop()

    def createWidgets(self):
        # Call each tab class.
        self.roast = roastTab(self.root, self)
        self.recipes = recipesTab(self.root, self)
        self.log = logTab(self.root, self)

        # Add each tab to the main window.
        self.roast.grid(row=1, column=0, sticky="nsew")
        self.recipes.grid(row=1, column=0, sticky="nsew")
        self.log.grid(row=1, column=0, sticky="nsew")

        # Create tab buttons.
        self.roastButton = Button(self.root, text="Roast", command=lambda: self.show_frame(self.roast))
        self.roastButton.grid(row=0, column=0)
        self.recipeButton = Button(self.root, text="Recipe", command=lambda: self.show_frame(self.recipes))
        self.recipeButton.grid(row=0, column=1)
        self.logButton = Button(self.root, text="Log", command=lambda: self.show_frame(self.log))
        self.logButton.grid(row=0, column=2)

        # Show the default tab.
        self.show_frame(self.roast)

    def show_frame(self, tab):
        tab.tkraise()
