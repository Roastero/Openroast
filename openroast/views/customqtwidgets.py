# -*- coding: utf-8 -*-
# Roastero, released under GPLv3

import os
import json
import datetime

from PyQt5 import QtCore
from PyQt5 import QtWidgets

import matplotlib
matplotlib.use('Qt5Agg')
# import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib.dates import MinuteLocator, DateFormatter
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class RoastGraphWidget():
    def __init__(self, graphXValueList=None, graphYValueList=None,
            animated=False, updateMethod=None, animatingMethod=None):
        self.graphXValueList = graphXValueList or []
        self.graphYValueList = graphYValueList or []
        self.counter = 0
        self.updateMethod = updateMethod
        self.animated = animated
        # Check if graph should continue to graph.
        self.animatingMethod = animatingMethod

        self.widget = self.create_graph()

    def create_graph(self):
        # Create the graph widget.
        graphWidget = QtWidgets.QWidget()
        graphWidget.setObjectName("graph")

        # Style attributes of matplotlib.
        matplotlib.rcParams['lines.linewidth'] = 3
        matplotlib.rcParams['lines.color'] = '#2a2a2a'
        matplotlib.rcParams['font.size'] = 10.
        self.graphFigure = Figure(facecolor='#444952')
        self.graphCanvas = FigureCanvas(self.graphFigure)

        # Add graph widgets to layout for graph.
        graphVerticalBox = QtWidgets.QVBoxLayout()
        graphVerticalBox.addWidget(self.graphCanvas)
        graphWidget.setLayout(graphVerticalBox)

        # Animate the the graph with new data
        if self.animated:
            self.animateGraph = animation.FuncAnimation(self.graphFigure,
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

        self.graphAxes.get_xaxis().set_major_formatter(DateFormatter('%M:%S'))
        # self.graphAxes.set_axis_bgcolor('#23252a')
        self.graphAxes.set_facecolor('#23252a')

        # adding more visible text color
        self.graphAxes.get_xaxis().label.set_color('white')
        self.graphAxes.get_yaxis().label.set_color('white')
        self.graphAxes.tick_params(axis='x', colors='white')
        self.graphAxes.tick_params(axis='y', colors='white')

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
        try:
            file_name = QtWidgets.QFileDialog.getSaveFileName(
                QtWidgets.QWidget(),
                'Save Roast Graph',
                os.path.expanduser('~/'),
                'Graph (*.png);;All Files (*)')
            self.graphFigure.savefig(
                file_name[0],
                bbox_inches='tight',
                facecolor='#23252a',
                edgecolor='black')
        except FileNotFoundError:
            # Occurs if file browser is canceled
            pass
        else:
            pass

    def save_roast_graph_csv(self):
        try:
            file_name = QtWidgets.QFileDialog.getSaveFileName(
                QtWidgets.QWidget(),
                'Save Roast Graph CSV',
                os.path.expanduser('~/'),
                'CSV (*.csv);;All Files (*)')
            with open(file_name[0], 'w') as outfile:
                outfile.write("Seconds,Temperature\n")
                if not self.graphXValueList:
                    return
                init_time = matplotlib.dates.num2date(self.graphXValueList[0])
                for x_val,y_val in zip(self.graphXValueList,self.graphYValueList):
                    x_time = matplotlib.dates.num2date(x_val)
                    elapsed_seconds = (x_time - init_time).seconds
                    outfile.write("{0},{1}\n".format(elapsed_seconds, y_val))
        except FileNotFoundError:
            # Occurs if file browser is canceled
            pass
        else:
            pass

class ComboBoxNoWheel(QtWidgets.QComboBox):
    """A combobox with the wheel removed."""
    def __init__(self, *args, **kwargs):
        super(ComboBoxNoWheel, self).__init__()

    def wheelEvent(self, event):
        event.ignore()


class TimeEditNoWheel(QtWidgets.QTimeEdit):
    """A time edit combobox with the wheel removed."""
    def __init__(self, *args, **kwargs):
        super(TimeEditNoWheel, self).__init__()

    def wheelEvent(self, event):
        event.ignore()


class RecipeModel(QtWidgets.QFileSystemModel):
    """A Subclass of QFileSystemModel to add a column."""
    def __init__(self, *args, **kwargs):
        super(RecipeModel, self).__init__()

    def columnCount(self, parent = QtCore.QModelIndex()):
        return super(RecipeModel, self).columnCount()+1

    def data(self, index, role):
        if index.column() == self.columnCount() - 1:
            if role == QtCore.Qt.DisplayRole:
                filePath = self.filePath(index)
                if os.path.isfile(filePath):
                    with open(filePath) as json_data:
                        fileContents = json.load(json_data)
                    return fileContents["roastName"]
                else:
                    path = self.filePath(index)
                    position = path.rfind("/")
                    return path[position+1:]

        return super(RecipeModel, self).data(index, role)


class LogModel(QtWidgets.QFileSystemModel):
    """A Subclass of QFileSystemModel to add a column."""
    def __init__(self, *args, **kwargs):
        super(LogModel, self).__init__()

    def columnCount(self, parent = QtCore.QModelIndex()):
        return super(LogModel, self).columnCount()+1

    def data(self, index, role):
        if index.column() == self.columnCount() - 1:
            if role == Qt.DisplayRole:
                filePath = self.filePath(index)
                if os.path.isfile(filePath):
                    with open(filePath) as json_data:
                        fileContents = json.load(json_data)
                    return fileContents["recipeName"]
                else:
                    path = self.filePath(index)
                    position = path.rfind("/")
                    return path[position+1:]

        return super(LogModel, self).data(index, role)
