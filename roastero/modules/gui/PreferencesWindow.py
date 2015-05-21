# PyQt imports
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class PreferencesWindow(QDialog):
    def __init__(self):
        super(PreferencesWindow, self).__init__()

        # Define main window for the application.
        self.setWindowTitle('Roastero Preferences')
        self.setMinimumSize(800,600)
        self.setContextMenuPolicy(Qt.NoContextMenu)
        #self.setWindowIcon(QIcon("icon.png"))

        self.create_ui()

    def create_ui(self):
        """A method used to create the basic ui for the Recipe Editor Window"""
        # Create main layout for window.
        self.layout = QGridLayout(self)

        # Create Bottom Buttons.
        self.create_bottom_buttons()
        self.layout.addLayout(self.bottomButtonLayout, 2, 0, 1, 2)

    def create_bottom_buttons(self):
        """Creates the button panel on the bottom of the Recipe Editor
        Window."""
        # Set bottom button layout.
        self.bottomButtonLayout = QHBoxLayout()
        self.bottomButtonLayout.setSpacing(0)

        # Create buttons.
        self.saveButton = QPushButton("SAVE")
        self.closeButton = QPushButton("CLOSE")

        # Assign object names to the buttons.
        self.saveButton.setObjectName("smallButton")
        self.saveButton.clicked.connect(self.save_preferences)
        self.closeButton.setObjectName("smallButton")
        self.closeButton.clicked.connect(self.close_window)

        # Create Spacer.
        self.spacer = QWidget()
        self.spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Add widgets to the layout.
        self.bottomButtonLayout.addWidget(self.spacer)
        self.bottomButtonLayout.addWidget(self.closeButton)
        self.bottomButtonLayout.addWidget(self.saveButton)

    def save_preferences(self):
        pass

    def close_window(self):
        """Method used to close the Preferences Window."""
        self.close()
