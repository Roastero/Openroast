# -*- coding: utf-8 -*-
# Roastero, released under GPLv3

import os
import time
import math
import datetime
import openroast

from PyQt5 import QtCore
from PyQt5 import QtWidgets

from openroast.views import customqtwidgets


class RoastTab(QtWidgets.QWidget):
    def __init__(self):
        super(RoastTab, self).__init__()

        # Class variables.
        self.sectTimeSliderPressed = False
        self.tempSliderPressed = False

        # Create the tab ui.
        self.create_ui()

        # Update initial GUI information
        self.update_section_time()
        self.update_total_time()

        # Create timer to update gui data.
        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_data)
        self.timer.start()

        # Set the roast tab diabled when starting.
        self.setEnabled(False)

    def create_ui(self):
        # Create the main layout for the roast tab.
        self.layout = QtWidgets.QGridLayout()

        # Create graph widget.
        self.graphWidget = customqtwidgets.RoastGraphWidget(
            animated = True,
            updateMethod = self.graph_get_data,
            animatingMethod = self.check_roaster_status)
        self.layout.addWidget(self.graphWidget.widget, 0, 0)
        self.layout.setColumnStretch(0, 1)

        # Create right pane.
        self.rightPane = self.create_right_pane()
        self.layout.addLayout(self.rightPane, 0, 1)

        # Create progress bar.
        self.progressBar = self.create_progress_bar()
        self.layout.addLayout(self.progressBar, 1, 0, 1, 2, QtCore.Qt.AlignCenter)

        # Create not connected label.
        self.connectionStatusLabel = QtWidgets.QLabel("Please connect your roaster.")
        self.connectionStatusLabel.setObjectName("connectionStatus")
        self.connectionStatusLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.connectionStatusLabel, 0, 0)

        # Set main layout for widget.
        self.setLayout(self.layout)

    def check_roaster_status(self):
        if (openroast.roaster.get_roaster_state() == 'roasting' or
                openroast.roaster.get_roaster_state() == 'cooling'):
            return True
        else:
            return False

    def graph_get_data(self):
        self.graphWidget.append_x(openroast.roaster.current_temp)

    def save_roast_graph(self):
        self.graphWidget.save_roast_graph()

    def update_data(self):
        # Update temperature widgets.
        self.currentTempLabel.setText(str(openroast.roaster.current_temp))

        # Update timers.
        self.update_section_time()
        self.update_total_time()

        # Update current section progress bar.
        if(openroast.recipes.check_recipe_loaded()):
            value = openroast.recipes.get_current_section_time() - openroast.roaster.time_remaining

            value = value / openroast.recipes.get_current_section_time()
            value = round(value * 100)

            self.sectionBars[openroast.recipes.get_current_step_number()].setValue(value)

        # Check connection status of the openroast.roaster.
        if (openroast.roaster.connected):
            self.connectionStatusLabel.setHidden(True)
            self.setEnabled(True)
        else:
            self.connectionStatusLabel.setHidden(False)
            self.setEnabled(False)

    def create_right_pane(self):
        rightPane = QtWidgets.QVBoxLayout()

        # Create guage window.
        guageWindow = self.create_gauge_window()
        rightPane.addLayout(guageWindow)

        # Create sliders.
        sliderPanel = self.create_slider_panel()
        rightPane.addLayout(sliderPanel)

        # Create button panel.
        buttonPanel = self.create_button_panel()
        rightPane.addLayout(buttonPanel)

        # Add a bottom spacer to keep sizing.
        spacer = QtWidgets.QWidget()
        spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        rightPane.addWidget(spacer)

        return rightPane

    def create_progress_bar(self):
        progressBar = QtWidgets.QGridLayout()
        progressBar.setSpacing(0)

        # An array to hold all progress bars.
        self.sectionBars = []

        if(openroast.recipes.check_recipe_loaded()):
            counter = 0

            for i in range(0, openroast.recipes.get_num_recipe_sections()):
                # Calculate display time and generate label text.
                time = openroast.recipes.get_section_time(i)
                minutes, seconds = self.calc_display_time(time)
                labelText = (str(minutes) +  ":" + str(seconds) + "@" +
                    str(openroast.recipes.get_section_temp(i)))

               # Create label for section.
                label = QtWidgets.QLabel(labelText)
                label.setObjectName("progressLabel")
                label.setAlignment(QtCore.Qt.AlignCenter)
                progressBar.addWidget(label, 0, i)

               # Create progress bar for section.
                bar = QtWidgets.QProgressBar(self)
                bar.setTextVisible(False)

                # Add css styling based upon the order of the progress bars.
                if(i == 0):
                    bar.setObjectName("firstProgressBar")
                elif(i == openroast.recipes.get_num_recipe_sections() - 1):
                    bar.setObjectName("lastProgressBar")
                else:
                    bar.setObjectName("middleProgressBar")

                # Add progress bar to layout and array.
                self.sectionBars.append(bar)
                progressBar.addWidget(bar, 0, i)

                # Add stretch factor to column based upon minutes.
                progressBar.setColumnStretch(i, time)

                # Make the counter equal to i.
                counter = i

           # Create next button.
            nextButton = QtWidgets.QPushButton("NEXT")
            nextButton.setObjectName("nextButton")
            nextButton.clicked.connect(self.next_section)
            progressBar.addWidget(nextButton, 0, (counter + 1))

        return progressBar

    def recreate_progress_bar(self):
        # Remove all existing widgets from progressbar layout
        for i in reversed(range(self.progressBar.count())):
            self.progressBar.itemAt(i).widget().setParent(None)

        self.progressBar = self.create_progress_bar()
        self.layout.addLayout(self.progressBar, 1, 0, 1, 2, QtCore.Qt.AlignCenter)

    def calc_display_time(self, time):
        time = time / 60
        minutes = math.floor((time))
        seconds = int((time - math.floor(time)) * 60)

        if(seconds == 0):
            seconds = '00'

        return(minutes, seconds)

    def create_gauge_window(self):
        guageWindow = QtWidgets.QGridLayout()

        # Create current temp gauge.
        self.currentTempLabel = QtWidgets.QLabel("150")
        currentTemp = self.create_info_box("CURRENT TEMP", "tempGuage",
            self.currentTempLabel)
        guageWindow.addLayout(currentTemp, 0, 0)

        # Create target temp gauge.
        self.targetTempLabel = QtWidgets.QLabel()
        targetTemp = self.create_info_box("TARGET TEMP", "tempGuage", self.targetTempLabel)
        guageWindow.addLayout(targetTemp, 0, 1)

        # Create current time.
        self.sectionTimeLabel = QtWidgets.QLabel()
        currentTime = self.create_info_box("CURRENT SECTION TIME", "timeWindow", self.sectionTimeLabel)
        guageWindow.addLayout(currentTime, 1, 0)

        # Create totalTime.
        self.totalTimeLabel = QtWidgets.QLabel()
        totalTime = self.create_info_box("TOTAL TIME", "timeWindow", self.totalTimeLabel)
        guageWindow.addLayout(totalTime, 1, 1)

        return guageWindow

    def create_button_panel(self):
        buttonPanel = QtWidgets.QGridLayout()

        # Create start roast button.
        self.startButton = QtWidgets.QPushButton("ROAST")
        self.startButton.clicked.connect(openroast.roaster.roast)
        buttonPanel.addWidget(self.startButton, 0, 0)

        # Create cool button.
        self.coolButton = QtWidgets.QPushButton("COOL")
        self.coolButton.clicked.connect(openroast.roaster.cool)
        buttonPanel.addWidget(self.coolButton, 0, 1)

        # Create stop roast button.
        self.stopButton = QtWidgets.QPushButton("STOP")
        self.stopButton.clicked.connect(openroast.roaster.idle)
        buttonPanel.addWidget(self.stopButton, 0, 2)

        return buttonPanel

    def create_slider_panel(self):
        sliderPanel = QtWidgets.QGridLayout()
        sliderPanel.setColumnStretch(0, 3)

        # Create temperature slider label.
        tempSliderLabel = QtWidgets.QLabel("TARGET TEMP")
        sliderPanel.addWidget(tempSliderLabel, 0, 0)

        # Create temperature slider.
        self.tempSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.tempSlider.setRange(150, 550)
        self.tempSlider.valueChanged.connect(self.update_target_temp_slider)
        sliderPanel.addWidget(self.tempSlider, 1, 0)

        # Create temperature spin box.
        self.tempSpinBox = QtWidgets.QSpinBox()
        self.tempSpinBox.setObjectName("miniSpinBox")
        self.tempSpinBox.setButtonSymbols(2)      # Remove arrows.
        self.tempSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.tempSpinBox.setRange(150, 550)
        self.tempSpinBox.valueChanged.connect(self.update_target_temp_spin_box)
        self.tempSpinBox.setAttribute(QtCore.Qt.WA_MacShowFocusRect, 0)
        sliderPanel.addWidget(self.tempSpinBox, 1, 1)

        # Update temperature data.
        self.update_target_temp()

        # Create timer slider label.
        timeSliderLabel = QtWidgets.QLabel("SECTION TIME")
        sliderPanel.addWidget(timeSliderLabel, 2, 0)

        # Create timer slider.
        self.sectTimeSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.sectTimeSlider.setRange(0, 900)
        self.sectTimeSlider.valueChanged.connect(self.update_sect_time_slider)
        sliderPanel.addWidget(self.sectTimeSlider, 3, 0)

        # Create mini timer spin box.
        self.sectTimeSpinBox = customqtwidgets.TimeEditNoWheel()
        self.sectTimeSpinBox.setObjectName("miniSpinBox")
        self.sectTimeSpinBox.setButtonSymbols(2)      # Remove arrows.
        self.sectTimeSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.sectTimeSpinBox.setAttribute(QtCore.Qt.WA_MacShowFocusRect, 0)
        self.sectTimeSpinBox.setDisplayFormat("mm:ss")
        self.sectTimeSpinBox.timeChanged.connect(self.update_sect_time_spin_box)
        sliderPanel.addWidget(self.sectTimeSpinBox, 3, 1)

        # Create fan speed slider.
        fanSliderLabel = QtWidgets.QLabel("FAN SPEED")
        sliderPanel.addWidget(fanSliderLabel, 4, 0)

        # Create fan speed slider.
        self.fanSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.fanSlider.setRange(1, 9)
        self.fanSlider.valueChanged.connect(self.update_fan_speed_slider)
        sliderPanel.addWidget(self.fanSlider, 5, 0)

        # Create mini fan spin box
        self.fanSpeedSpinBox = QtWidgets.QSpinBox()
        self.fanSpeedSpinBox.setObjectName("miniSpinBox")
        self.fanSpeedSpinBox.setButtonSymbols(2)      # Remove arrows.
        self.fanSpeedSpinBox.setRange(1, 9)
        self.fanSpeedSpinBox.setAttribute(QtCore.Qt.WA_MacShowFocusRect, 0)
        self.fanSpeedSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.fanSpeedSpinBox.valueChanged.connect(self.update_fan_spin_box)
        sliderPanel.addWidget(self.fanSpeedSpinBox, 5, 1)

        return sliderPanel

    def create_info_box(self, labelText, objectName, valueLabel):
        # Create temp/time info boxes.
        infoBox = QtWidgets.QVBoxLayout()
        infoBox.setSpacing(0)
        label = QtWidgets.QLabel(labelText)
        label.setObjectName("label")
        valueLabel.setAlignment(QtCore.Qt.AlignCenter)
        valueLabel.setObjectName(objectName)
        infoBox.addWidget(label)
        infoBox.addWidget(valueLabel)
        return infoBox

    def update_target_temp(self):
        self.targetTempLabel.setText(str(openroast.roaster.target_temp))
        self.tempSlider.setValue(openroast.roaster.target_temp)
        self.tempSpinBox.setValue(openroast.roaster.target_temp)

    def update_target_temp_spin_box(self):
        self.targetTempLabel.setText(str(self.tempSpinBox.value()))
        self.tempSlider.setValue(self.tempSpinBox.value())
        openroast.roaster.target_temp = self.tempSpinBox.value()

    def update_target_temp_slider(self):
        self.targetTempLabel.setText(str(self.tempSlider.value()))
        self.tempSpinBox.setValue(self.tempSlider.value())
        openroast.roaster.target_temp = self.tempSlider.value()

    def update_fan_info(self):
        self.fanSlider.setValue(openroast.roaster.fan_speed)
        self.fanSpeedSpinBox.setValue(openroast.roaster.fan_speed)

    def update_fan_speed_slider(self):
        self.fanSpeedSpinBox.setValue(self.fanSlider.value())
        openroast.roaster.fan_speed = self.fanSlider.value()

    def update_fan_spin_box(self):
        self.fanSlider.setValue(self.fanSpeedSpinBox.value())
        openroast.roaster.fan_speed = self.fanSpeedSpinBox.value()

    def set_section_time(self):
        self.sectionTimeLabel.setText(time.strftime("%M:%S",
            time.gmtime(self.sectTimeSlider.value())))
        openroast.roaster.time_remaining = self.sectTimeSlider.value()

    def update_section_time(self):
        self.sectTimeSlider.setValue(openroast.roaster.time_remaining)

        self.sectTimeSpinBox.setTime(QtCore.QTime.fromString(str(time.strftime("%H:%M:%S",
            time.gmtime(openroast.roaster.time_remaining)))))

        self.sectionTimeLabel.setText(str(time.strftime("%M:%S",
            time.gmtime(openroast.roaster.time_remaining))))

    def update_sect_time_spin_box(self):
        self.sectionTimeLabel.setText(str(time.strftime("%M:%S",
            time.gmtime(QtCore.QTime(0, 0, 0).secsTo(self.sectTimeSpinBox.time())))))

        self.sectTimeSlider.setValue(QtCore.QTime(0, 0, 0).secsTo(self.sectTimeSpinBox.time()))

        openroast.roaster.time_remaining = QtCore.QTime(0, 0, 0).secsTo(self.sectTimeSpinBox.time())

    def update_sect_time_slider(self):
        self.sectionTimeLabel.setText(str(time.strftime("%M:%S",
            time.gmtime(self.sectTimeSlider.value()))))

        self.sectTimeSpinBox.setTime(QtCore.QTime.fromString(str(time.strftime("%H:%M:%S",
            time.gmtime(self.sectTimeSlider.value())))))

        openroast.roaster.time_remaining = self.sectTimeSlider.value()

    def update_total_time(self):
        self.totalTimeLabel.setText(str(time.strftime("%M:%S",
            time.gmtime(openroast.roaster.total_time))))

    def clear_roast(self):
        """ This method will clear the openroast.roaster, recipe, and reset the gui back
        to their original state. """

        # Reset openroast.roaster.
        openroast.recipes.reset_roaster_settings()

        # Clear the recipe.
        openroast.recipes.clear_recipe()

        # Clear roast tab gui.
        self.clear_roast_tab_gui()

    def reset_current_roast(self):
        """ Used to reset the current loaded recipe """

        # Verify that the recipe is loaded and reset it.
        if(openroast.recipes.check_recipe_loaded()):
            openroast.recipes.restart_current_recipe()
            self.recreate_progress_bar()

        # Clear roast tab gui.
        self.clear_roast_tab_gui()

    def clear_roast_tab_gui(self):
        """ Clears all of the graphical elements on the roast tab """

        # Recreate the progress bar or remove it.
        self.recreate_progress_bar()

        # Clear sliders.
        self.update_section_time()
        self.update_fan_info()
        self.update_target_temp()

        # Set totalTime to zero.
        openroast.roaster.total_time = 0
        self.update_total_time()

        # Clear roast graph.
        self.graphWidget.clear_graph()

    def load_recipe_into_roast_tab(self):
        openroast.recipes.load_current_section()
        self.recreate_progress_bar()
        self.update_section_time()
        self.update_target_temp()
        self.update_fan_info()

    def next_section(self):
        openroast.recipes.move_to_next_section()
        self.update_controllers()

    def update_controllers(self):
        self.update_section_time()
        self.update_target_temp()
        self.update_fan_info()

    def get_recipe_object(self):
        return openroast.recipes
