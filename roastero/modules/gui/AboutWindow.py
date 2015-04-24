# PyQt imports
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

# Standard Library Imports
import webbrowser
from functools import partial

class About(QDialog):
    def __init__(self, recipeLocation=None):
        super(About, self).__init__()

        # Define main window for the application.
        self.setWindowTitle('About Roastero')
        self.setMinimumSize(600,400)
        self.setContextMenuPolicy(Qt.NoContextMenu)
        #self.setWindowIcon(QIcon("icon.png"))

        # Open qss file.
        self.style = open('static/mainStyle.css').read()
        self.setStyleSheet(self.style)

        self.create_ui()

    def create_ui(self):
        """A method used to create the basic ui for the About Window"""
        # Create main layout for window.
        self.layout = QGridLayout(self)

        # Roastero Label
        self.roasteroLabel = QLabel("Roastero")
        self.roasteroLabel.setAlignment(Qt.AlignCenter)
        self.roasteroLabel.setObjectName("logo")

        # License
        self.licenseLabel = QLabel("License")
        self.licenseLabel.setAlignment(Qt.AlignCenter)
        with open('LICENSE', 'r') as file:
             licenseText = file.read()
        self.licenseTextBox = QTextEdit()
        self.licenseTextBox.setText(licenseText)
        self.licenseTextBox.setReadOnly(True)

        # Version
        self.versionLabel = QLabel("Version - 0.1.2")
        self.versionLabel.setObjectName("versionLabel")
        self.versionLabel.setAlignment(Qt.AlignCenter)

        # Created by
        self.authorsLabel = QLabel("Authors")
        self.authorsLabel.setAlignment(Qt.AlignCenter)

        self.authorButton1 = QPushButton("Caleb Coffie")
        self.author1Link = "https://CalebCoffie.com"
        self.authorButton1.clicked.connect(partial(self.open_link_in_browser, self.author1Link))

        self.authorButton2 = QPushButton("Mark Spicer")
        self.author2Link = "https://markspicer.me"
        self.authorButton2.clicked.connect(partial(self.open_link_in_browser, self.author2Link))

        # Add all the widgets
        self.layout.addWidget(self.roasteroLabel, 0, 0, 1, 2)
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
