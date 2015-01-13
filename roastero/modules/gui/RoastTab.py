import random
import datetime
import matplotlib
matplotlib.use('Qt5Agg')
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.dates import MinuteLocator, DateFormatter
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)

# Import Fresh Roast SR700 TODO: Make this more dynamic
from ..roaster_libraries.FreshRoastSR700 import FreshRoastSR700

class RoastTab(QWidget):
    def __init__(self):
        super(RoastTab, self).__init__()
        self.graphXValueList = []
        self.graphYValueList = []
        self.counter = 0
        self.create_ui()

    def create_ui(self):
        # Create a new layout to add everything to
        self.layout = QGridLayout()

        # Create graph widget.
        self.create_graph()

        # Add graph widget to main layout.
        self.layout.addWidget(self.graphWidget, 0, 0)

        # Add another side widget for testing
        self.recipeBrowser = QTextEdit()
        self.layout.addWidget(self.recipeBrowser, 0, 1)

        # Set main layout for widget.
        self.setLayout(self.layout)

    def create_graph(self):
        self.graphWidget = QWidget(self)

        self.graphFigure = plt.figure()
        self.graphCanvas = FigureCanvas(self.graphFigure)
        self.graphCanvas.setParent(self.graphWidget)
        self.graphCanvas.setFocusPolicy(Qt.StrongFocus)
        self.graphCanvas.setFocus()

        self.graphToolbar = NavigationToolbar(self.graphCanvas, self.graphWidget)

        self.graphCanvas.mpl_connect('key_press_event', self.graph_on_key_press)

        graphVerticalBox = QVBoxLayout()
        graphVerticalBox.addWidget(self.graphCanvas)
        graphVerticalBox.addWidget(self.graphToolbar)
        self.graphWidget.setLayout(graphVerticalBox)

        # Animate the the graph with new data
        animateGraph = animation.FuncAnimation(self.graphFigure, self.graph_draw, interval=1000)

    def graph_on_key_press(self, event):
        print('you pressed', event.key)
        # implement the default mpl key press events described at
        # http://matplotlib.org/users/navigation_toolbar.html#navigation-keyboard-shortcuts
        key_press_handler(event, self.graphCanvas, self.graphToolbar)

    def graph_draw(self, *args, **kwargs):
        self.graph_get_data()
        self.graphFigure.clear()
        self.graphAxes = self.graphFigure.add_subplot(111)
        self.graphAxes.plot_date(self.graphXValueList, self.graphYValueList, '-')

        # Rotate the labels on the x-axis by 80 degrees
        plt.xticks(rotation=80)

        # Format the graphs a little
        self.graphAxes.set_ylabel('Temperature (°F)')
        self.graphAxes.set_xlabel('Time')
        self.graphFigure.subplots_adjust(bottom=0.2)

        ax = self.graphAxes.get_axes()
        ax.xaxis.set_major_formatter(DateFormatter('%M:%S'))

        # Draw the graph
        self.graphCanvas.draw()

    def graph_get_data(self):
        self.counter += 1
        currentTime = datetime.datetime.fromtimestamp(self.counter)
        randomNumber = random.randint(1, 500)
        self.graphXValueList.append(matplotlib.dates.date2num(currentTime))
        self.graphYValueList.append(randomNumber)
