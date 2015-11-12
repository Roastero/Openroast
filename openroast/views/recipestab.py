# -*- coding: utf-8 -*-
# Roastero, released under GPLv3

import os
import json
import time
import openroast
import webbrowser

from PyQt5 import QtCore
from PyQt5 import QtWidgets

from openroast.views import customqtwidgets
from openroast.views import recipeeditorwindow


class RecipesTab(QtWidgets.QWidget):
    def __init__(self, roastTabObject, MainWindowObject):
        super(RecipesTab, self).__init__()

        # Pass in recipe object

        self.roastTab = roastTabObject

        self.MainWindow = MainWindowObject

        self.create_ui()

    def create_ui(self):
        """A method used to create the basic ui for the Recipe Tab."""
        self.layout = QtWidgets.QGridLayout()

        # Create recipe browser.
        self.create_recipe_browser()
        self.layout.addWidget(openroast.recipes.rowser, 0, 0)
        self.layout.addWidget(self.createNewRecipeButton, 1, 0)

        # Create recipe window.
        self.create_recipe_window()
        self.create_recipe_buttons()
        self.layout.addLayout(openroast.recipes.indow, 0, 1)
        self.layout.addLayout(openroast.recipes.uttonsLayout, 1, 1)

        # Set stretch so items align correctly.
        self.layout.setColumnStretch(1, 2)
        self.layout.setRowStretch(0, 3)

        # Create label to cover recipe info.
        openroast.recipes.electionLabel = QtWidgets.QLabel()
        openroast.recipes.electionLabel.setObjectName("recipeSelectionLabel")
        openroast.recipes.electionLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(openroast.recipes.electionLabel, 0, 1)

        # Set main layout for widget.
        self.setLayout(self.layout)

    def create_recipe_browser(self):
        """Creates the side panel to browse all the files in the recipe folder.
        This method also adds a button to create new recipes to the layout."""
        # Creates model with all information about the files in ./recipes
        self.model = customqtwidgets.RecipeModel()
        self.model.setRootPath(os.path.expanduser('~/Documents/Openroast/Recipes/'))

        # Create a TreeView to view the information from the model
        openroast.recipes.rowser = QtWidgets.QTreeView()
        openroast.recipes.rowser.setModel(self.model)
        openroast.recipes.rowser.setRootIndex(self.model.index(os.path.expanduser('~/Documents/Openroast/Recipes/')))
        openroast.recipes.rowser.setFocusPolicy(QtCore.Qt.NoFocus)
        openroast.recipes.rowser.header().close()

        openroast.recipes.rowser.setAnimated(True)
        openroast.recipes.rowser.setIndentation(0)

        # Hides all the unecessary columns created by the model
        openroast.recipes.rowser.setColumnHidden(0, True)
        openroast.recipes.rowser.setColumnHidden(1, True)
        openroast.recipes.rowser.setColumnHidden(2, True)
        openroast.recipes.rowser.setColumnHidden(3, True)

        openroast.recipes.rowser.clicked.connect(self.on_recipeBrowser_clicked)

        # Add create new recipe button.
        self.createNewRecipeButton = QtWidgets.QPushButton("NEW RECIPE")
        self.createNewRecipeButton.clicked.connect(self.create_new_recipe)

    def create_recipe_window(self):
        """Creates the whole right-hand side of the recipe tab. These fields are
        populated when a recipe is chosen from the left column."""
        # Create all of the gui Objects
        openroast.recipes.indow = QtWidgets.QGridLayout()
        openroast.recipes.ameLabel = QtWidgets.QLabel("Recipe Name")
        openroast.recipes.reatorLabel = QtWidgets.QLabel("Created by ")
        openroast.recipes.otalTimeLabel = QtWidgets.QLabel("Total Time: ")
        openroast.recipes.oastTypeLabel = QtWidgets.QLabel("Roast Type: ")
        self.beanRegionLabel = QtWidgets.QLabel("Bean Region: ")
        self.beanCountryLabel = QtWidgets.QLabel("Bean Country: ")
        openroast.recipes.escriptionBox = QtWidgets.QTextEdit()
        openroast.recipes.escriptionBox.setReadOnly(True)
        openroast.recipes.tepsTable = QtWidgets.QTableWidget()

        # Set options for recipe table.
        openroast.recipes.tepsTable.setShowGrid(False)
        openroast.recipes.tepsTable.setAlternatingRowColors(True)
        openroast.recipes.tepsTable.setCornerButtonEnabled(False)
        openroast.recipes.tepsTable.horizontalHeader().setSectionResizeMode(1)
        openroast.recipes.tepsTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        openroast.recipes.tepsTable.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)

        # Assign Object Names for qss
        openroast.recipes.ameLabel.setObjectName("RecipeName")
        openroast.recipes.reatorLabel.setObjectName("RecipeCreator")
        openroast.recipes.otalTimeLabel.setObjectName("RecipeTotalTime")
        openroast.recipes.oastTypeLabel.setObjectName("RecipeRoastType")
        self.beanRegionLabel.setObjectName("RecipeBeanRegion")
        self.beanCountryLabel.setObjectName("RecipeBeanCountry")
        openroast.recipes.tepsTable.setObjectName("RecipeSteps")

        # Add objects to the layout
        openroast.recipes.indow.addWidget(openroast.recipes.ameLabel, 0, 0, 1, 2)
        openroast.recipes.indow.addWidget(openroast.recipes.reatorLabel, 1, 0)
        openroast.recipes.indow.addWidget(openroast.recipes.oastTypeLabel, 2, 0)
        openroast.recipes.indow.addWidget(openroast.recipes.otalTimeLabel, 3, 0)
        openroast.recipes.indow.addWidget(self.beanRegionLabel, 4, 0)
        openroast.recipes.indow.addWidget(self.beanCountryLabel, 5, 0)
        openroast.recipes.indow.addWidget(openroast.recipes.escriptionBox, 7, 0)
        openroast.recipes.indow.addWidget(openroast.recipes.tepsTable, 7, 1)

    def create_recipe_buttons(self):
        """Creates the button panel on the bottom to allow for the user to
        interact with the currently selected/viewed recipe."""
        openroast.recipes.uttonsLayout = QtWidgets.QGridLayout()
        openroast.recipes.uttonsLayout.setSpacing(0)
        openroast.recipes.oastButton = QtWidgets.QPushButton("ROAST NOW")
        self.editRecipeButton = QtWidgets.QPushButton("EDIT")
        self.beanLinkButton = QtWidgets.QPushButton("PURCHASE BEANS")

        # Assign object names for qss styling.
        openroast.recipes.oastButton.setObjectName("smallButton")
        self.beanLinkButton.setObjectName("smallButton")
        self.editRecipeButton.setObjectName("smallButton")
        self.createNewRecipeButton.setObjectName("smallButtonAlt")

        # Add spacer.
        self.spacer = QtWidgets.QWidget()
        self.spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        openroast.recipes.uttonsLayout.addWidget(self.spacer)

        openroast.recipes.oastButton.clicked.connect(self.load_recipe)
        self.editRecipeButton.clicked.connect(self.open_recipe_editor)
        self.beanLinkButton.clicked.connect(self.open_link_in_browser)

        openroast.recipes.uttonsLayout.addWidget(self.beanLinkButton, 0, 1)
        openroast.recipes.uttonsLayout.addWidget(self.editRecipeButton, 0, 2)
        openroast.recipes.uttonsLayout.addWidget(openroast.recipes.oastButton, 0, 3)

        # Disable buttons until recipe is selected.
        self.beanLinkButton.setEnabled(False)
        self.editRecipeButton.setEnabled(False)
        openroast.recipes.oastButton.setEnabled(False)

    def on_recipeBrowser_clicked(self, index):
        """This method is used when a recipe is selected in the left column.
        This method also enables the bottom button panel after a recipe has
        been selected."""
        indexItem = self.model.index(index.row(), 0, index.parent())

        self.selectedFilePath = self.model.filePath(indexItem)

        # Allow single click expanding of folders
        if os.path.isdir(self.selectedFilePath):
            if openroast.recipes.rowser.isExpanded(indexItem):
                openroast.recipes.rowser.collapse(indexItem)
            else:
                openroast.recipes.rowser.expand(indexItem)
        # Handles when a file is clicked
        else:
            # Load recipe information from file
            self.load_recipe_file(self.selectedFilePath)

            # Set bean link button enabled/disabled if it is available or not.
            if(self.currentBeanUrl):
                self.beanLinkButton.setEnabled(True)
            else:
                self.beanLinkButton.setEnabled(False)

            # Set lower buttons enabled once recipe is selected.
            self.editRecipeButton.setEnabled(True)
            openroast.recipes.oastButton.setEnabled(True)

            # Hide recipe selection label once a recipe is selected.
            openroast.recipes.electionLabel.setHidden(True)

    def load_recipe_file(self, filePath):
        """Used to load file from a path into selected recipe object."""
        with open(filePath) as json_data:
            recipeObject = json.load(json_data)
        self.currentlySelectedRecipe = recipeObject
        self.currentlySelectedRecipePath = filePath
        self.load_recipe_information(self.currentlySelectedRecipe)

    def load_recipe_information(self, recipeObject):
        """Loads recipe information the into the right hand column fields.
        This method also populates the recipe steps table."""
        openroast.recipes.ameLabel.setText(recipeObject["roastName"])
        openroast.recipes.reatorLabel.setText("Created by " +
            recipeObject["creator"])
        openroast.recipes.oastTypeLabel.setText("Roast Type: " +
            recipeObject["roastDescription"]["roastType"])
        self.beanRegionLabel.setText("Bean Region: " +
            recipeObject["bean"]["region"])
        self.beanCountryLabel.setText("Bean Country: " +
            recipeObject["bean"]["country"])
        openroast.recipes.escriptionBox.setText(recipeObject["roastDescription"]
            ["description"])
        self.currentBeanUrl = recipeObject["bean"]["source"]["link"]

        # Total Time
        t = time.strftime("%M:%S", time.gmtime(recipeObject["totalTime"]))
        openroast.recipes.otalTimeLabel.setText("Total Time: " + t + " minutes")

        # Steps spreadsheet
        openroast.recipes.tepsTable.setRowCount(len(recipeObject["steps"]))
        openroast.recipes.tepsTable.setColumnCount(3)
        openroast.recipes.tepsTable.setHorizontalHeaderLabels(["Temperature",
            "Fan Speed", "Section Time"])

        for row in range(len(recipeObject["steps"])):

            sectionTimeWidget = QtWidgets.QTableWidgetItem()
            sectionTempWidget = QtWidgets.QTableWidgetItem()
            sectionFanSpeedWidget = QtWidgets.QTableWidgetItem()

            sectionTimeWidget.setText(time.strftime("%M:%S",
                time.gmtime(recipeObject["steps"][row]["sectionTime"])))
            sectionFanSpeedWidget.setText(str(recipeObject["steps"][row]["fanSpeed"]))

            if 'targetTemp' in recipeObject["steps"][row]:
                sectionTempWidget.setText(str(recipeObject["steps"][row]["targetTemp"]))
            else:
                sectionTempWidget.setText("Cooling")

            # Set widget cell alignment.
            sectionTempWidget.setTextAlignment(QtCore.Qt.AlignCenter)
            sectionFanSpeedWidget.setTextAlignment(QtCore.Qt.AlignCenter)
            sectionTimeWidget.setTextAlignment(QtCore.Qt.AlignCenter)

            # Add widgets
            openroast.recipes.tepsTable.setItem(row, 0, sectionTempWidget)
            openroast.recipes.tepsTable.setItem(row, 1, sectionFanSpeedWidget)
            openroast.recipes.tepsTable.setItem(row, 2, sectionTimeWidget)

    def load_recipe(self):
        """Loads recipe into Roast tab."""
        if (openroast.recipes.check_recipe_loaded()):
            self.roastTab.clear_roast()

        openroast.recipes.load_recipe_json(self.currentlySelectedRecipe)
        self.roastTab.load_recipe_into_roast_tab()
        self.MainWindow.select_roast_tab()

    def open_link_in_browser(self):
        """Opens link to purchase the beans."""
        webbrowser.open(self.currentBeanUrl)

    def open_recipe_editor(self):
        """Method used to open Recipe Editor Window with an existing recipe."""
        self.editorWindow = recipeeditorwindow.RecipeEditor(recipeLocation = self.currentlySelectedRecipePath)
        self.editorWindow.exec_()

        # Used to update the recipe in the recipes tab after editing
        self.load_recipe_file(self.selectedFilePath)


    def create_new_recipe(self):
        """Method used to open Recipe Editor Window for a new recipe."""
        self.editorWindow = recipeeditorwindow.RecipeEditor()
        self.editorWindow.exec_()

        # Used to update the recipe in the recipes tab after creation
        try:
            self.load_recipe_file(self.selectedFilePath)
        except AttributeError:
            pass
        except IsADirectoryError:
            pass

    def get_currently_selected_recipe(self):
        """returns currently selected recipe for use in Recipe Editor Window."""
        return self.currentlySelectedRecipe
