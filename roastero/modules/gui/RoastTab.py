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
        self.layout.addWidget(self.graphWidget, 0, 0)
        self.layout.setColumnStretch(0, 1)

        # Create right pane.
        self.rightPane = self.create_right_pane()
        self.layout.addLayout(self.rightPane, 0, 1)

        # Set main layout for widget.
        self.setLayout(self.layout)

    def create_graph(self):
        # Load external matplotlib file
        self.graphWidget = QWidget(self)
        self.graphWidget.setObjectName("graph")

        plt.rcParams['lines.linewidth'] = 3
        plt.rcParams['lines.color'] = '#2a2a2a'
        plt.rcParams['font.size'] = 10.

        self.graphFigure = plt.figure(facecolor='#444952')
        self.graphCanvas = FigureCanvas(self.graphFigure)

        #self.graphToolbar = NavigationToolbar(self.graphCanvas, self.graphWidget)

        self.graphCanvas.mpl_connect('key_press_event', self.graph_on_key_press)

        graphVerticalBox = QVBoxLayout()
        graphVerticalBox.addWidget(self.graphCanvas)
        #graphVerticalBox.addWidget(self.graphToolbar)
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
        self.graphAxes.plot_date(self.graphXValueList, self.graphYValueList, '#85b63f')

        # Rotate the labels on the x-axis by 80 degrees
        #plt.xticks(rotation=80)

        # Format the graphs a little
        self.graphAxes.set_ylabel('TEMPERATURE (°F)')
        self.graphAxes.set_xlabel('TIME')
        self.graphFigure.subplots_adjust(bottom=0.2)

        ax = self.graphAxes.get_axes()
        ax.xaxis.set_major_formatter(DateFormatter('%M:%S'))
        ax.set_axis_bgcolor('#23252a')

        # Draw the graph
        self.graphCanvas.draw()

    def graph_get_data(self):
        self.counter += 1
        currentTime = datetime.datetime.fromtimestamp(self.counter)
        randomNumber = random.randint(1, 500)
        self.graphXValueList.append(matplotlib.dates.date2num(currentTime))
        self.graphYValueList.append(randomNumber)

    def create_right_pane(self):
        rightPane = QVBoxLayout()

        # Create guage window.
        guageWindow = self.create_gauge_window()
        rightPane.addLayout(guageWindow)

        # Create button panel.
        buttonPanel = self.create_button_panel()
        rightPane.addLayout(buttonPanel)

        # Create sliders.
        sliderPanel = self.create_slider_panel()
        rightPane.addLayout(sliderPanel)

        # Add a bottom spacer to keep sizing.
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        rightPane.addWidget(spacer)

        return rightPane

    def create_gauge_window(self):
        guageWindow = QGridLayout()

        # Create current temp gauge.
        currentTemp = self.create_info_box("CURRENT TEMP", "tempGuage")
        guageWindow.addLayout(currentTemp, 0, 0)

        # Create target temp gauge.
        targetTemp = self.create_info_box("TARGET TEMP", "tempGuage")
        guageWindow.addLayout(targetTemp, 0, 1)

        # Create current time.
        currentTime = self.create_info_box("CURRENT TIME", "timeWindow")
        guageWindow.addLayout(currentTime, 1, 0)

        # Create totalTime.
        totalTime = self.create_info_box("TOTAL TIME", "timeWindow")
        guageWindow.addLayout(totalTime, 1, 1)

        return guageWindow

    def create_button_panel(self):
        buttonPanel = QGridLayout()

        button01 = QPushButton("Hi")
        button01.setObjectName("mainButton")
        buttonPanel.addWidget(button01, 0, 0)

        button01 = QPushButton("Hi")
        button01.setObjectName("mainButton")
        buttonPanel.addWidget(button01, 0, 1)

        button01 = QPushButton("Hi")
        button01.setObjectName("mainButton")
        buttonPanel.addWidget(button01, 1, 0)

        button01 = QPushButton("Hi")
        button01.setObjectName("mainButton")
        buttonPanel.addWidget(button01, 1, 1)

        return buttonPanel

    def create_slider_panel(self):
        sliderPanel = QGridLayout()

        label01 = QLabel("ADJUST TARGET TEMP")
        sliderPanel.addWidget(label01, 0, 0)

        slider01 = QSlider(Qt.Horizontal)
        sliderPanel.addWidget(slider01, 1, 0)

        label01 = QLabel("ADJUST SECTION TIME")
        sliderPanel.addWidget(label01, 2, 0)

        slider01 = QSlider(Qt.Horizontal)
        sliderPanel.addWidget(slider01, 3, 0)

        return sliderPanel

    def create_info_box(self, labelText, objectName):
        infoBox = QVBoxLayout()
        infoBox.setSpacing(0)
        label = QLabel(labelText)
        label.setObjectName("label")
        info = QLabel("300")
        info.setAlignment(Qt.AlignCenter)
        info.setObjectName(objectName)
        infoBox.addWidget(label)
        infoBox.addWidget(info)
        return infoBox
