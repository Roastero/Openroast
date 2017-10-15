# -*- coding: utf-8 -*-
# Roastero, released under GPLv3

import os
import json
import shutil
import openroast

from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets

from openroast.views import roasttab
from openroast.views import recipestab
from openroast.views import aboutwindow
from openroast.version import __version__

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, recipes, roaster):
        super(MainWindow, self).__init__()

        # Define main window for the application.
        self.setWindowTitle('Openroast v%s' % __version__)
        self.setMinimumSize(800, 600)
        self.setContextMenuPolicy(QtCore.Qt.NoContextMenu)

        # keep a copy of roaster & recipes, needed here
        self.roaster = roaster
        self.recipes = recipes

        # Create toolbar.
        self.create_toolbar()

        # Create tabs.
        self.create_tabs(self.roaster, recipes)

        # Create menu.
        self.create_actions()
        self.create_menus()


    def create_actions(self):
        # File menu actions.
        self.clearRoastAct = QtWidgets.QAction(
            "&Clear",
            self,
            shortcut=QtGui.QKeySequence(
                QtCore.Qt.CTRL + QtCore.Qt.SHIFT + QtCore.Qt.Key_C),
            statusTip="Clear the roast window",
            triggered=self.roast.clear_roast)

        self.newRoastAct = QtWidgets.QAction("&Roast Again", self,
            shortcut=QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_R),
            statusTip="Roast recipe again",
            triggered=self.roast.reset_current_roast)

        self.importRecipeAct = QtWidgets.QAction("&Import Recipe", self,
            shortcut=QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_I),
            statusTip="Import a recipe file",
            triggered=self.import_recipe_file)

        self.exportRecipeAct = QtWidgets.QAction("&Export Recipe", self,
            shortcut=QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_E),
            statusTip="Export a recipe file",
            triggered=self.export_recipe_file)

        self.saveRoastGraphAct = QtWidgets.QAction("&Save Roast Graph", self,
            shortcut=QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_K),
            statusTip="Save an image of the roast graph",
            triggered=self.roast.save_roast_graph)

        self.saveRoastGraphCSVAct = QtWidgets.QAction("&Save Roast Graph CSV", self,
            statusTip="Save the roast graph as a csv",
            triggered=self.roast.save_roast_graph_csv)

        self.openAboutWindow = QtWidgets.QAction("&About", self,
            statusTip="About openroast",
            triggered=self.open_about_window)

    def create_menus(self):
        menubar = self.menuBar()

        # Create file menu.
        self.fileMenu = menubar.addMenu("&File")
        self.fileMenu.addAction(self.clearRoastAct)
        self.fileMenu.addAction(self.newRoastAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.importRecipeAct)
        self.fileMenu.addAction(self.exportRecipeAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.saveRoastGraphAct)
        self.fileMenu.addAction(self.saveRoastGraphCSVAct)
        self.fileMenu.addSeparator()

        # Create help menu.
        self.helpMenu = menubar.addMenu("&Help")
        self.helpMenu.addAction(self.openAboutWindow)

    def create_toolbar(self):
        # Create toolbar.
        self.mainToolBar = self.addToolBar('mainToolBar')
        self.mainToolBar.setMovable(False)
        self.mainToolBar.setFloatable(False)

        # Add logo.
        self.logo = QtWidgets.QLabel("openroast")
        self.logo.setObjectName("logo")
        self.mainToolBar.addWidget(self.logo)

        # Add roasting tab button.
        self.roastTabButton = QtWidgets.QPushButton("ROAST", self)
        self.roastTabButton.setObjectName("toolbar")
        self.roastTabButton.clicked.connect(self.select_roast_tab)
        self.mainToolBar.addWidget(self.roastTabButton)

        # Add recipes tab button.
        self.recipesTabButton = QtWidgets.QPushButton("RECIPES", self)
        self.recipesTabButton.setObjectName("toolbar")
        self.recipesTabButton.clicked.connect(self.select_recipes_tab)
        self.mainToolBar.addWidget(self.recipesTabButton)

        # Add spacer to set login button on the right.
        self.spacer = QtWidgets.QWidget()
        self.spacer.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.mainToolBar.addWidget(self.spacer)

        # Add buttons to array to be disabled on selection.
        self.tabButtons = [self.roastTabButton,
                           self.recipesTabButton]

    def create_tabs(self, roaster, recipes):
        self.tabs = QtWidgets.QStackedWidget()

        # Create widgets to add to tabs.
        self.roast = roasttab.RoastTab(
            roaster, recipes)
        self.recipes = recipestab.RecipesTab(
            roastTabObject=self.roast,
            MainWindowObject=self,
            recipes_object=self.recipes)

        # Add widgets to tabs.
        self.tabs.insertWidget(0, self.roast)
        self.tabs.insertWidget(1, self.recipes)

        # Set the tabs as the central widget.
        self.setCentralWidget(self.tabs)

        # Set the roast button disabled.
        self.roastTabButton.setEnabled(False)

    def select_roast_tab(self):
        self.tabs.setCurrentIndex(0)
        self.change_blocked_button(0)

    def select_recipes_tab(self):
        self.tabs.setCurrentIndex(1)
        self.change_blocked_button(1)

    def change_blocked_button(self, index):
        # Set all buttons enabled.
        for button in self.tabButtons:
            button.setEnabled(True)

        # Set selected button disabled.
        self.tabButtons[index].setEnabled(False)

    def import_recipe_file(self):
        try:
            recipeFile = QtWidgets.QFileDialog.getOpenFileName(self, 'Select Recipe',
                os.path.expanduser('~/'), 'Recipes (*.json);;All Files (*)')
            shutil.copy2(recipeFile[0],
                os.path.expanduser('~/Documents/Openroast/Recipes/My Recipes/'))
        except FileNotFoundError:
            # Occurs if file browser is canceled
            pass
        else:
            pass

    def export_recipe_file(self):
        try:
            recipeFile = QtWidgets.QFileDialog.getSaveFileName(self, 'Export Recipe',
                os.path.expanduser('~/'), 'Recipes (*.json);;All Files (*)')
            jsonObject = json.dumps(
                self.recipes.currentlySelectedRecipe, indent=4)

            file = open(recipeFile[0], 'w')
            file.write(jsonObject)
            file.close()
        except FileNotFoundError:
            # Occurs if file browser is canceled
            pass
        else:
            pass

    def open_about_window(self):
        self.aboutWindow = aboutwindow.About()
        self.aboutWindow.exec_()

    def closeEvent(self, event):
        self.roaster.disconnect()
