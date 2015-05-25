# Standard Library Imports
import datetime, time, math, os, json

# PyQt imports
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# Local project imports
from ..gui.CustomQtWidgets import LogModel

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
        self.create_log_browser()
        self.layout.addWidget(self.logBrowser, 0, 0)

        # Create graph widget.
        self.create_graph()
        self.layout.addWidget(self.graphWidget, 0, 0)
        self.layout.setColumnStretch(0, 1)

        # Create right pane.
        # self.rightPane = self.create_right_pane()
        # self.layout.addLayout(self.rightPane, 0, 1)

        # Set main layout for widget.
        self.setLayout(self.layout)

    def create_log_browser(self):
        """Creates the side panel to browse all the files in the log folder."""
        # Creates model with all information about the files in ./recipes
        self.model = LogModel()
        self.model.setRootPath(os.path.expanduser('~/Documents/Roastero/log/'))

        # Create a TreeView to view the information from the model
        self.logBrowser = QTreeView()
        self.logBrowser.setModel(self.model)
        self.logBrowser.setRootIndex(self.model.index(os.path.expanduser('~/Documents/Roastero/log/')))
        self.logBrowser.setFocusPolicy(Qt.NoFocus)
        self.logBrowser.header().close()

        self.logBrowser.setAnimated(True)
        self.logBrowser.setIndentation(0)

        # Hides all the unecessary columns created by the model
        self.logBrowser.setColumnHidden(0, True)
        self.logBrowser.setColumnHidden(1, True)
        self.logBrowser.setColumnHidden(2, True)
        self.logBrowser.setColumnHidden(3, True)

        self.logBrowser.clicked.connect(self.on_logBrowser_clicked)

    def create_graph(self):
        # Create the graph widget.
        self.graphWidget = QWidget(self)
        self.graphWidget.setObjectName("graph")

        # Style attributes of matplotlib.
        plt.rcParams['lines.linewidth'] = 3
        plt.rcParams['lines.color'] = '#2a2a2a'
        plt.rcParams['font.size'] = 10.

        self.graphFigure = plt.figure(facecolor='#444952')
        self.graphCanvas = FigureCanvas(self.graphFigure)

        # Add graph widgets to layout for graph.
        graphVerticalBox = QVBoxLayout()
        graphVerticalBox.addWidget(self.graphCanvas)
        self.graphWidget.setLayout(graphVerticalBox)

        # # Animate the the graph with new data
        # animateGraph = animation.FuncAnimation(self.graphFigure,
        #     self.graph_draw, interval=1000)

    def graph_draw(self, graphXValueList = None, graphYValueList = None):
        self.graphFigure.clear()

        self.graphAxes = self.graphFigure.add_subplot(111)
        self.graphAxes.plot_date(graphXValueList, graphYValueList,
            '#8ab71b')

        # Add formatting to the graphs.
        self.graphAxes.set_ylabel('TEMPERATURE (°F)')
        self.graphAxes.set_xlabel('TIME')
        self.graphFigure.subplots_adjust(bottom=0.2)

        ax = self.graphAxes.get_axes()
        ax.xaxis.set_major_formatter(DateFormatter('%M:%S'))
        ax.set_axis_bgcolor('#23252a')

        self.graphCanvas.draw()

    def on_logBrowser_clicked(self, index):
        """This method is used when a log is selected in the left column."""
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

    def load_roast_log_file(self, filePath):
        """Used to load file from a path into selected roast log object."""
        with open(filePath) as json_data:
            roastLogObject = json.load(json_data)
        self.currentlySelectedRoastLog = roastLogObject
        self.currentlySelectedRoastLogPath = filePath

        # TODO: Load roast log information
        # self.load_recipe_information(self.currentlySelectedRecipe)
