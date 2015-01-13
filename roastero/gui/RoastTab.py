import random
import datetime
import matplotlib
matplotlib.use('Qt5Agg')
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from matplotlib.figure import Figure
import matplotlib.animation as animation
import matplotlib.dates as mdates
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)

class RoastTab(QWidget):
    def __init__(self):
        super(RoastTab, self).__init__()
        self.graphXValueList = []
        self.graphYValueList = []
        self.create_ui()

    def create_ui(self):
        self.create_graph()
        animateGraph = animation.FuncAnimation(self.graphFigure, self.graph_draw, interval=1000)
        self.graph_draw()

    def create_graph(self):
        self.graphWidget = QWidget(self)

        self.graphFigure = Figure((5.0, 4.0), dpi=100)
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
        self.graphCanvas.draw()

    def graph_get_data(self):
        currentTime = datetime.datetime.now()
        randomNumber = random.randint(1, 500)
        self.graphXValueList.append(matplotlib.dates.date2num(currentTime))
        self.graphYValueList.append(randomNumber)
