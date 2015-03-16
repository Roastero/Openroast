import datetime
import matplotlib
import threading
import time
import math
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
from ..roaster_libraries.FreshRoastSR700 import FreshRoastSR700

class RoastTab(QWidget):
    def __init__(self):
        super(RoastTab, self).__init__()

        # Class variables.
        self.graphXValueList = []
        self.graphYValueList = []
        self.counter = 0
        self.roaster = FreshRoastSR700()
        self.timeSliderPressed = False
        self.tempSliderPressed = False

        # Create the tab ui.
        self.create_ui()

        # Create timer to update gui data.
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_data)
        self.timer.start()

    def create_ui(self):
        # Create the main layout for the roast tab.
        self.layout = QGridLayout()

        # Create graph widget.
        self.create_graph()
        self.layout.addWidget(self.graphWidget, 0, 0)
        self.layout.setColumnStretch(0, 1)

        # Create right pane.
        self.rightPane = self.create_right_pane()
        self.layout.addLayout(self.rightPane, 0, 1)

        # Create progress bar.
        self.progressBar = self.create_progress_bar()
        self.layout.addLayout(self.progressBar, 1, 0, 1, 2, Qt.AlignCenter)

        # Create not connected label.
        self.connectionStatusLabel = QLabel("Please connect your roaster.")
        self.connectionStatusLabel.setObjectName("connectionStatus")
        self.connectionStatusLabel.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.connectionStatusLabel, 0, 0)

#        self.p = QDoubleSpinBox()
#        self.p.setRange(0.000, 0.900)
#        self.p.valueChanged.connect(self.change_p)
#        self.layout.addWidget(self.p, 1, 0)
#
#        self.i = QDoubleSpinBox()
#        self.i.setRange(0.000, 0.900)
#        self.i.valueChanged.connect(self.change_p)
#        self.layout.addWidget(self.i, 1, 1)
#
#        self.d = QDoubleSpinBox()
#        self.d.setRange(0.000, 0.900)
#        self.d.valueChanged.connect(self.change_p)
#        self.layout.addWidget(self.d, 1, 2)



        # Set main layout for widget.
        self.setLayout(self.layout)

#    def change_p(self):
#        self.roaster.set_p(self.p.value())
#
#    def change_i(self):
#        self.roaster.set_i(self.d.value())
#
#    def change_d(self):
#        self.roaster.set_d(self.d.value())

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

        # Animate the the graph with new data
        animateGraph = animation.FuncAnimation(self.graphFigure,
            self.graph_draw, interval=1000)

    def graph_draw(self, *args, **kwargs):
        # Start graphing the roast if the roast has started.
        if (self.roaster.get_current_status() == 1 or
                self.roaster.get_current_status() == 2):
            self.graph_get_data()

        self.graphFigure.clear()

        self.graphAxes = self.graphFigure.add_subplot(111)
        self.graphAxes.plot_date(self.graphXValueList, self.graphYValueList,
            '#85b63f')

        # Add formatting to the graphs.
        self.graphAxes.set_ylabel('TEMPERATURE (°F)')
        self.graphAxes.set_xlabel('TIME')
        self.graphFigure.subplots_adjust(bottom=0.2)

        ax = self.graphAxes.get_axes()
        ax.xaxis.set_major_formatter(DateFormatter('%M:%S'))
        ax.set_axis_bgcolor('#23252a')

        self.graphCanvas.draw()

    def graph_get_data(self):
        self.counter += 1
        currentTime = datetime.datetime.fromtimestamp(self.counter)
        self.graphXValueList.append(matplotlib.dates.date2num(currentTime))
        self.graphYValueList.append(self.roaster.get_current_temp())

    def update_data(self):
        self.targetTempLabel.setText(str(self.roaster.get_target_temp()))
        self.change_target_temp_slider(self.roaster.get_target_temp())
        self.update_fan_box()

        self.currentTempLabel.setText(str(self.roaster.get_current_temp()))
        if (self.roaster.get_current_status() == 1 or
                self.roaster.get_current_status() == 2):
            self.update_section_time()
            self.update_total_time()

            # Update current section progress bar.
            currentTime = (self.roaster.get_specific_section_time(self.roaster.get_current_section()) - self.roaster.get_section_time())
            value = (currentTime / self.roaster.get_specific_section_time(self.roaster.get_current_section()))

            value = round(value * 100)
#                print(value)
#
#                if(value >= 0 or value < 100):
#                    self.sectionBars[self.roaster.get_current_section()].setValue(value)
#                else:
#                    self.sectionBars[self.roaster.get_current_section()].setValue(100)

        # Check connection status of the roaster.
        if (self.roaster.get_connection_status()):
            self.connectionStatusLabel.setHidden(True)
            self.setEnabled(True)
        else:
            self.connectionStatusLabel.setHidden(False)
            self.setEnabled(False)

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

    def create_progress_bar(self):
        progressBar = QGridLayout()
        progressBar.setHorizontalSpacing(0)

        # An array to hold all progress bars.
        self.sectionBars = []

        for i in range(0, self.roaster.get_num_recipe_sections()):
            # Calculate display time and generate label text.
            time = self.roaster.get_specific_section_time(i)
            minutes, seconds = self.calc_display_time(time)
            labelText = (str(minutes) +  ":" + str(seconds) + "@" +
                str(self.roaster.get_specific_section_temp(i)))

            # Create label for section.
            label = QLabel(labelText)
            label.setObjectName("progressLabel")
            label.setAlignment(Qt.AlignCenter)
            progressBar.addWidget(label, 0, i)

            # Create progress bar for section.
            bar = QProgressBar(self)
            bar.setTextVisible(False)

            # Add css styling based upon the order of the progress bars.
            if(i == 0):
                bar.setObjectName("firstProgressBar")
            elif(i == self.roaster.get_num_recipe_sections() - 1):
                bar.setObjectName("lastProgressBar")
            else:
                bar.setObjectName("middleProgressBar")

            # Add progress bar to layout and array.
            self.sectionBars.append(bar)
            progressBar.addWidget(bar, 0, i)

            # Add stretch factor to column based upon minutes.
            progressBar.setColumnStretch(i, time)

        return progressBar

    def calc_display_time(self, time):
        time = time / 60
        minutes = math.floor((time))
        seconds = int((time - math.floor(time)) * 60)

        if(seconds == 0):
            seconds = '00'

        return(minutes, seconds)

    def create_gauge_window(self):
        guageWindow = QGridLayout()

        # Create current temp gauge.
        self.currentTempLabel = QLabel()
        currentTemp = self.create_info_box("CURRENT TEMP", "tempGuage",
            self.currentTempLabel)
        guageWindow.addLayout(currentTemp, 0, 0)

        # Create target temp gauge.
        self.targetTempLabel = QLabel()
        targetTemp = self.create_info_box("TARGET TEMP", "tempGuage", self.targetTempLabel)
        guageWindow.addLayout(targetTemp, 0, 1)

        # Create current time.
        self.sectionTimeLabel = QLabel()
        currentTime = self.create_info_box("CURRENT SECTION TIME", "timeWindow", self.sectionTimeLabel)
        guageWindow.addLayout(currentTime, 1, 0)

        # Create totalTime.
        self.totalTimeLabel = QLabel()
        totalTime = self.create_info_box("TOTAL TIME", "timeWindow", self.totalTimeLabel)
        guageWindow.addLayout(totalTime, 1, 1)

        return guageWindow

    def create_button_panel(self):
        buttonPanel = QGridLayout()

        # Create start roast button.
        self.startButton = QPushButton("START")
        self.startButton.setObjectName("mainButton")
        self.startButton.clicked.connect(self.roaster.roast)
        buttonPanel.addWidget(self.startButton, 0, 0)

        # Create stop roast button.
        self.stopButton = QPushButton("STOP")
        self.stopButton.setObjectName("mainButton")
        self.stopButton.clicked.connect(self.roaster.idle)
        buttonPanel.addWidget(self.stopButton, 0, 1)

        # Create fan label.
        fanLabel = QLabel("FAN SPEED")
        fanLabel.setAlignment(Qt.AlignCenter)
        buttonPanel.addWidget(fanLabel, 0, 2)

        # Create cool button.
        self.coolButton = QPushButton("COOL")
        self.coolButton.setObjectName("mainButton")
        self.coolButton.clicked.connect(self.cooling_phase)
        buttonPanel.addWidget(self.coolButton, 1, 0)

        # Create next button.
        self.nextButton = QPushButton("NEXT")
        self.nextButton.setObjectName("mainButton")
        self.nextButton.clicked.connect(self.next_section)
        buttonPanel.addWidget(self.nextButton, 1, 1)

        # Create fan speed spin box.
        self.fanSpeedSpinBox = QSpinBox()
        self.fanSpeedSpinBox.setRange(1, 9)
        self.fanSpeedSpinBox.setFocusPolicy(Qt.NoFocus)
        self.fanSpeedSpinBox.setAlignment(Qt.AlignCenter)
        self.fanSpeedSpinBox.lineEdit().setReadOnly(True)
        self.fanSpeedSpinBox.lineEdit().deselect()
        self.fanSpeedSpinBox.valueChanged.connect(self.change_fan_speed)
        buttonPanel.addWidget(self.fanSpeedSpinBox, 1, 2)

        return buttonPanel

    def create_slider_panel(self):
        sliderPanel = QGridLayout()

        # Create temperature slider label.
        tempSliderLabel = QLabel("ADJUST TARGET TEMP")
        sliderPanel.addWidget(tempSliderLabel, 0, 0)

        # Create temperature slider.
        self.tempSlider = QSlider(Qt.Horizontal)
        self.tempSlider.setRange(150, 500)
        self.tempSlider.sliderMoved.connect(self.change_target_temp)
        self.tempSlider.sliderPressed.connect(self.toggle_temp_slider_status)
        self.tempSlider.sliderReleased.connect(self.toggle_temp_slider_status)
        self.change_target_temp()
        sliderPanel.addWidget(self.tempSlider, 1, 0)

        # Create timer slider.
        timeSliderLabel = QLabel("ADJUST SECTION TIME")
        sliderPanel.addWidget(timeSliderLabel, 2, 0)

        # Create timer slider.
        self.timeSlider = QSlider(Qt.Horizontal)
        self.timeSlider.setRange(0, 720)
        self.timeSlider.sliderMoved.connect(self.set_section_time)
        self.timeSlider.sliderPressed.connect(self.toggle_time_slider_status)
        self.timeSlider.sliderReleased.connect(self.toggle_time_slider_status)
        sliderPanel.addWidget(self.timeSlider, 3, 0)

        return sliderPanel

    def create_info_box(self, labelText, objectName, valueLabel):
        # Create temp/time info boxes.
        infoBox = QVBoxLayout()
        infoBox.setSpacing(0)
        label = QLabel(labelText)
        label.setObjectName("label")
        valueLabel.setAlignment(Qt.AlignCenter)
        valueLabel.setObjectName(objectName)
        infoBox.addWidget(label)
        infoBox.addWidget(valueLabel)
        return infoBox

    def change_target_temp(self):
        self.targetTempLabel.setText(str(self.tempSlider.value()))
        self.roaster.set_target_temp(self.tempSlider.value())

    def change_target_temp_slider(self, temp):
        self.tempSlider.setValue(temp)

    def change_fan_speed(self):
        self.roaster.set_fan_speed(self.fanSpeedSpinBox.value())

    def update_fan_box(self):
        self.fanSpeedSpinBox.setValue(self.roaster.get_fan_speed())

    def set_section_time(self):
        self.sectionTimeLabel.setText(time.strftime("%M:%S",
            time.gmtime(self.timeSlider.value())))
        self.roaster.set_section_time(self.timeSlider.value())

    def update_section_time(self):
        self.timeSlider.setValue(self.roaster.get_section_time())
        self.sectionTimeLabel.setText(str(time.strftime("%M:%S",
            time.gmtime(self.roaster.get_section_time()))))

    def update_total_time(self):
        self.totalTimeLabel.setText(str(time.strftime("%M:%S",
            time.gmtime(self.roaster.get_total_time()))))

    def cooling_phase(self):
        self.roaster.cooling_phase()

    def toggle_temp_slider_status(self):
        self.tempSliderPressed = not self.tempSliderPressed

    def toggle_time_slider_status(self):
        self.timeSliderPressed = not self.timeSliderPressed

    # def connect_roaster(self):
    #     self.roaster.run()

    def start_new_roast(self):
        self.graphXValueList = []
        self.graphYValueList = []
        self.counter = 0
        self.graphFigure.clear()
        self.roaster.set_section_time(0)
        self.update_section_time()
        self.roaster.set_total_time(0)
        self.update_total_time()
        self.roaster.set_target_temp(150)
        self.change_target_temp_slider(150)
        self.change_target_temp()
        self.roaster.set_fan_speed(1)
        self.fanSpeedSpinBox.setValue(1)

    def current_section(self):
        self.roaster.load_current_section()
        self.update_section_time()
        self.targetTempLabel.setText(str(self.roaster.get_target_temp()))
        self.change_target_temp_slider(self.roaster.get_target_temp())
        self.update_fan_box()

    def next_section(self):
        self.roaster.load_next_section()
        self.update_section_time()
        self.targetTempLabel.setText(str(self.roaster.get_target_temp()))
        self.change_target_temp_slider(self.roaster.get_target_temp())
        self.update_fan_box()
