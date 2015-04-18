#!/usr/bin/env python3

# Standard Library Imports
import sys, os, shutil

# PyQt imports
from PyQt5.QtWidgets import QApplication

# Local project imports
from modules.gui.MainWindow import MainWindow

def check_for_user_recipe_folder():
    roasteroRecipeFolder = os.path.expanduser('~/Documents/Roastero/recipes/')
    if not os.path.isdir(roasteroRecipeFolder):
        shutil.copytree("recipes", roasteroRecipeFolder)

check_for_user_recipe_folder()
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
