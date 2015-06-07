# Standard Library Imports
import datetime, time, math, os, json

# PyQt imports
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# Local project imports
from ..gui.CustomQtWidgets import LogModel
from .RoastGraphWidget import RoastGraphWidget

# Matplotlib imports
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.dates import MinuteLocator, DateFormatter
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)


class LogTab(QWidget):
    def __init__(self):
        super(LogTab, self).__init__()

        # Class variables.
        # self.graphXValueList = []
        # self.graphYValueList = []
        # self.counter = 0

        self.currentlySelectedRoastLog = {}
        self.currentlySelectedRoastLogPath = ""

        # Create the tab ui.
        self.create_ui()

    def create_ui(self):
        # Create the main layout for the roast tab.
        self.layout = QGridLayout()

        # Create log browser.
        self.logBrowser = self.create_log_browser()
        self.layout.addWidget(self.logBrowser, 0, 0)

        # Create right pane.
        self.rightPane = self.create_right_pane()
        self.layout.addLayout(self.rightPane, 0, 1)

        # Set main layout for widget.
        self.setLayout(self.layout)

    def create_log_browser(self):
        """Creates the side panel to browse all the files in the log folder."""
        # Creates model with all information about the files in ./recipes
        self.model = LogModel()
        self.model.setRootPath(os.path.expanduser('~/Documents/Roastero/log/'))

        # Create a TreeView to view the information from the model
        logBrowser = QTreeView()
        logBrowser.setModel(self.model)
        logBrowser.setRootIndex(self.model.index(os.path.expanduser('~/Documents/Roastero/log/')))
        logBrowser.setFocusPolicy(Qt.NoFocus)
        logBrowser.header().close()

        logBrowser.setAnimated(True)
        logBrowser.setIndentation(0)

        # Hides all the unecessary columns created by the model
        logBrowser.setColumnHidden(0, True)
        logBrowser.setColumnHidden(1, True)
        logBrowser.setColumnHidden(2, True)
        logBrowser.setColumnHidden(3, True)

        logBrowser.clicked.connect(self.on_logBrowser_clicked)

        return logBrowser

    def on_logBrowser_clicked(self, index):
        """
        This method is used when a log is selected in the left column.
        """
        indexItem = self.model.index(index.row(), 0, index.parent())

        self.selectedFilePath = self.model.filePath(indexItem)

        # Allow single click expanding of folders
        if os.path.isdir(self.selectedFilePath):
            if self.logBrowser.isExpanded(indexItem):
                self.logBrowser.collapse(indexItem)
            else:
                self.logBrowser.expand(indexItem)
        # Handles when a file is clicked
        else:
            # Load roast log information from file
            self.load_roast_log_file(self.selectedFilePath)

    def create_right_pane(self):
        """
        Creates the right pane of the log browser.
        """
        # Create right pane layout
        rightPaneLayout = QGridLayout()

        # Create Graph
        # Create graph widget.
        self.graphWidget = RoastGraphWidget()
        rightPaneLayout.addWidget(self.graphWidget.widget, 0, 0)

        return rightPaneLayout


    def load_roast_log_file(self, filePath):
        """Used to load file from a path into selected log object."""
        with open(filePath) as json_data:
            roastLogObject = json.load(json_data)
        self.currentlySelectedRoastLog = roastLogObject
        self.currentlySelectedRoastLogPath = filePath

        # TODO: Load roast log information
        # self.load_recipe_information(self.currentlySelectedRecipe)
