#!/usr/bin/env python3

# Standard Library Imports
import sys, os, shutil, inspect

# Change execution directory to file location
def get_script_dir(follow_symlinks=True):
    if getattr(sys, 'frozen', False): # py2exe, PyInstaller, cx_Freeze
        path = os.path.abspath(sys.executable)
    else:
        path = inspect.getabsfile(get_script_dir)
    if follow_symlinks:
        path = os.path.realpath(path)
    return os.path.dirname(path)

os.chdir(get_script_dir())

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
