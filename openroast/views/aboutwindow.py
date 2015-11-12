# -*- coding: utf-8 -*-
# Roastero, released under GPLv3

import functools
import webbrowser

from PyQt5 import QtCore
from PyQt5 import QtWidgets


class About(QtWidgets.QDialog):
    def __init__(self, recipeLocation=None):
        super(About, self).__init__()

        # Define main window for the application.
        self.setWindowTitle('About Openroast')
        self.setMinimumSize(600, 400)
        self.setContextMenuPolicy(QtCore.Qt.NoContextMenu)

        self.create_ui()

    def create_ui(self):
        """A method used to create the basic ui for the About Window"""
        # Create main layout for window.
        self.layout = QtWidgets.QGridLayout(self)

        # openroast Label
        self.openroastLabel = QtWidgets.QLabel("openroast")
        self.openroastLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.openroastLabel.setObjectName("logo")

        # License
        self.licenseLabel = QtWidgets.QLabel("License")
        self.licenseLabel.setAlignment(QtCore.Qt.AlignCenter)
        with open('LICENSE', 'r') as file:
             licenseText = file.read()
        self.licenseTextBox = QtWidgets.QTextEdit()
        self.licenseTextBox.setText(licenseText)
        self.licenseTextBox.setReadOnly(True)

        # Version
        versionLabelString = "Version - 1.0.0"
        self.versionLabel = QtWidgets.QLabel(versionLabelString)
        self.versionLabel.setObjectName("versionLabel")
        self.versionLabel.setAlignment(QtCore.Qt.AlignCenter)

        # Created by
        self.authorsLabel = QtWidgets.QLabel("Authors")
        self.authorsLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.authorButton1 = QtWidgets.QPushButton("Mark Spicer")
        self.author1Link = "https://markspicer.me"
        self.authorButton1.clicked.connect(functools.partial(self.open_link_in_browser, self.author1Link))

        self.authorButton2 = QtWidgets.QPushButton("Caleb Coffie")
        self.author2Link = "https://CalebCoffie.com"
        self.authorButton2.clicked.connect(functools.partial(self.open_link_in_browser, self.author2Link))

        # Add all the widgets
        self.layout.addWidget(self.openroastLabel, 0, 0, 1, 2)
        self.layout.addWidget(self.licenseLabel, 1, 0, 1, 2)
        self.layout.addWidget(self.licenseTextBox, 2, 0, 1, 2)
        self.layout.addWidget(self.versionLabel, 3, 0, 1, 2)
        self.layout.addWidget(self.authorsLabel, 4, 0, 1, 2)
        self.layout.addWidget(self.authorButton1, 5, 0, 1, 1)
        self.layout.addWidget(self.authorButton2, 5, 1, 1, 1)

    def close_about_window(self):
        """Method used to close the about Window."""
        self.close()

    def open_link_in_browser(self, link):
        """Opens link to purchase the beans."""
        webbrowser.open(link)
