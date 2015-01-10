# Import necessary modules.
import tkinter as tk
from tkinter import ttk

# Import classes
from .log import logTab
from .recipes import recipesTab
from .roast import roastTab

class gui:
    def __init__(self):
        # Define class variables.
        self.bgColor = "#2e3138"
        #self.bgColor = "white"

        # Define root window.
        self.root = tk.Tk()
        self.root.title("Roastero")
        self.root.config(bg=self.bgColor)
        self.root.geometry("800x500")
        
        # Define images to be used.
        self.miniButton = tk.PhotoImage(file="../images/button.gif")

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
        self.roastButton = self.makeTabButton("Roast", self.roast)
        self.roastButton.grid(row=0, column=0)
        self.recipeButton = self.makeTabButton("Recipes", self.recipes)
        self.recipeButton.grid(row=0, column=1)
        self.logButton = self.makeTabButton("Log", self.log)
        self.logButton.grid(row=0, column=2)

        # Show the default tab.
        self.showFrame(self.roast)

    def showFrame(self, tab):
        tab.tkraise()

    def makeTabButton(self, buttonText, showFrame):
        return tk.Button(self.root,
                        activebackground="#f00",
                        activeforeground=self.bgColor,
                        anchor="center",
                        background=self.bgColor,
                        bg=self.bgColor,
                        borderwidth=-2,
                        bd=-2,
                        disabledforeground=self.bgColor,
                        foreground=self.bgColor,
                        fg=self.bgColor,
                        highlightbackground=self.bgColor,
                        highlightcolor=self.bgColor,
                        highlightthickness=0,
                        justify="center",
                        repeatdelay=10,
                        text=buttonText,
                        command=lambda: self.showFrame(showFrame),
                        image=self.miniButton,
                        compound="center",
                        height=36,
                        width=140,
                        padx=3,
                        pady=3)
