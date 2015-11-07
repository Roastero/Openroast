# -*- coding: utf-8 -*-
# Roastero, released under GPLv3

import sys

from PyQt5 import QtWidgets
from PyQt5 import QtGui

from openroast import tools
from openroast.views import mainwindow


class Openroast(object):
    def __init__(self):
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

    def run(self):
        self.window = mainwindow.MainWindow()
        self.window.show()
        sys.exit(self.app.exec_())
