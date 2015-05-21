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
from PyQt5.QtGui import QFontDatabase

# Local project imports
from modules.gui.MainWindow import MainWindow

def check_for_user_folder():
    roasteroUserFolder = os.path.expanduser('~/Documents/Roastero/')
    if not os.path.isdir(roasteroUserFolder):
        shutil.copytree("recipes", os.path.join(roasteroUserFolder, "recipes"))
        shutil.copytree("log", os.path.join(roasteroUserFolder, "log"))

check_for_user_folder()
app = QApplication(sys.argv)

# Set application style.
QFontDatabase.addApplicationFont("static/fonts/asap/asap-regular.ttf")
QFontDatabase.addApplicationFont("static/fonts/asap/asap-bold.ttf")
QFontDatabase.addApplicationFont("static/fonts/asap/asap-bold-italic.ttf")
QFontDatabase.addApplicationFont("static/fonts/asap/asap-italic.ttf")
style = open('static/mainStyle.css').read()
QApplication.setStyleSheet(app, style)

window = MainWindow()
window.show()
sys.exit(app.exec_())
