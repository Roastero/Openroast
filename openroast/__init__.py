# -*- coding: utf-8 -*-
# Roastero, released under GPLv3

import os
import sys
import shutil
import freshroastsr700

from PyQt5 import QtWidgets
from PyQt5 import QtGui

from openroast import tools
from openroast.views import mainwindow
from openroast.controllers import recipe


recipes = recipe.Recipe()
roaster = freshroastsr700.freshroastsr700(
    thermostat=True, state_transition_func=recipes.move_to_next_section)


class Openroast(object):
    """Main application class."""
    def __init__(self):
        """Set up application, styles, fonts, and global object."""
        self.app = QtWidgets.QApplication(sys.argv)
        QtGui.QFontDatabase.addApplicationFont(
            "static/fonts/asap/asap-regular.ttf")
        QtGui.QFontDatabase.addApplicationFont(
            "static/fonts/asap/asap-bold.ttf")
        QtGui.QFontDatabase.addApplicationFont(
            "static/fonts/asap/asap-bold-italic.ttf")
        QtGui.QFontDatabase.addApplicationFont(
            "static/fonts/asap/asap-italic.ttf")
        style = open('static/mainStyle.css').read()
        QtWidgets.QApplication.setStyleSheet(self.app, style)

        self.check_user_folder()

    def check_user_folder(self):
        """Checks copies user folder if no user folder exists."""
        user_folder = os.path.expanduser('~/Documents/Openroast/')

        if not os.path.isdir(user_folder):
            shutil.copytree("static/Recipes", 
                os.path.join(user_folder, "Recipes"))

    def run(self):
        """Turn everything on."""
        roaster.auto_connect()
        self.window = mainwindow.MainWindow()
        self.window.show()
        sys.exit(self.app.exec_())
