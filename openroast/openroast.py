#!/usr/bin/env python3
# Authors: Mark Spicer, Caleb Coffie
# License: openroast is released under GPLv3. Please see the license file for a
#          copy of the license.
# Contact: For additional information, please email admin@roastero.com

# Standard Library Imports
import sys, os, shutil, inspect

def get_script_dir(follow_symlinks=True):
    """ Checks where the script is being executed from to verify the imports
    will work properly. """
    if getattr(sys, 'frozen', False): # py2exe, PyInstaller, cx_Freeze
        path = os.path.abspath(sys.executable)
    else:
        path = inspect.getabsfile(get_script_dir)
    if follow_symlinks:
        path = os.path.realpath(path)
    return os.path.dirname(path)

# Change execution directory to file location before importing PyQt.
os.chdir(get_script_dir())

# PyQt imports
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFontDatabase

# Local project imports
from modules.gui.MainWindow import MainWindow

def check_for_user_folder():
    """ Verify that a user folder exists and create one if it does not before
    launching the application """
    openroastUserFolder = os.path.expanduser('~/Documents/openroast/')
    if not os.path.isdir(openroastUserFolder):
        shutil.copytree("recipes", os.path.join(openroastUserFolder, "recipes"))
        shutil.copyfile("config.ini", os.path.join(openroastUserFolder, "config.ini"))

# Check for user folder.
check_for_user_folder()

# Create application.
app = QApplication(sys.argv)

# Set application style.
QFontDatabase.addApplicationFont("static/fonts/asap/asap-regular.ttf")
QFontDatabase.addApplicationFont("static/fonts/asap/asap-bold.ttf")
QFontDatabase.addApplicationFont("static/fonts/asap/asap-bold-italic.ttf")
QFontDatabase.addApplicationFont("static/fonts/asap/asap-italic.ttf")
style = open('static/mainStyle.css').read()
QApplication.setStyleSheet(app, style)

# Create main window and show.
window = MainWindow()
window.show()
sys.exit(app.exec_())
