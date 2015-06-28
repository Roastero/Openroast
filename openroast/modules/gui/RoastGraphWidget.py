# Standard Library Imports
import datetime

# PyQt imports
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# Matplotlib imports
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.dates import MinuteLocator, DateFormatter
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class RoastGraphWidget():
    def __init__(self, graphXValueList = None, graphYValueList = None, animated = False, updateMethod = None, animatingMethod = None):
        self.graphXValueList = graphXValueList or []
        self.graphYValueList = graphYValueList or []
        self.counter = 0
        self.updateMethod = updateMethod
        self.animated = animated
        self.animatingMethod = animatingMethod # Check if graph should continue to graph

        self.widget = self.create_graph()

    def create_graph(self):
        # Create the graph widget.
        graphWidget = QWidget()
        graphWidget.setObjectName("graph")

        # Style attributes of matplotlib.
        plt.rcParams['lines.linewidth'] = 3
        plt.rcParams['lines.color'] = '#2a2a2a'
        plt.rcParams['font.size'] = 10.

        self.graphFigure = plt.figure(facecolor='#444952')
        self.graphCanvas = FigureCanvas(self.graphFigure)

        # Add graph widgets to layout for graph.
        graphVerticalBox = QVBoxLayout()
        graphVerticalBox.addWidget(self.graphCanvas)
        graphWidget.setLayout(graphVerticalBox)

        # Animate the the graph with new data
        if self.animated:
            animateGraph = animation.FuncAnimation(self.graphFigure,
                self.graph_draw, interval=1000)
        else:
            self.graph_draw()

        return graphWidget

    def graph_draw(self, *args, **kwargs):
        # Start graphing the roast if the roast has started.
        if self.animatingMethod is not None:
            if self.animatingMethod():
                self.updateMethod()

        self.graphFigure.clear()

        self.graphAxes = self.graphFigure.add_subplot(111)
        self.graphAxes.plot_date(self.graphXValueList, self.graphYValueList,
            '#8ab71b')

        # Add formatting to the graphs.
        self.graphAxes.set_ylabel('TEMPERATURE (°F)')
        self.graphAxes.set_xlabel('TIME')
        self.graphFigure.subplots_adjust(bottom=0.2)

        ax = self.graphAxes.get_axes()
        ax.xaxis.set_major_formatter(DateFormatter('%M:%S'))
        ax.set_axis_bgcolor('#23252a')

        self.graphCanvas.draw()

    def append_x(self, xCoord):
        self.counter += 1
        currentTime = datetime.datetime.fromtimestamp(self.counter)
        self.graphXValueList.append(matplotlib.dates.date2num(currentTime))
        self.graphYValueList.append(xCoord)

    def clear_graph(self):
        self.graphXValueList = []
        self.graphYValueList = []
        self.counter = 0
        self.graphFigure.clear()

    def save_roast_graph(self):
        userDesktop =  os.path.expanduser('~/Desktop')
        fileName = os.path.join(userDesktop + "/Roast_Graph")

        i = 0
        while os.path.exists('{}{:d}.png'.format(fileName, i)):
            i += 1
        self.graphFigure.savefig('{}{:d}.png'.format(fileName, i))
