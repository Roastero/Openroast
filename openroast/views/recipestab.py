# -*- coding: utf-8 -*-
# Roastero, released under GPLv3

import os
import json
import time
import webbrowser

from PyQt5 import QtCore
from PyQt5 import QtWidgets

from openroast.views import customqtwidgets
from openroast.views import recipeeditorwindow


class RecipesTab(QtWidgets.QWidget):
    def __init__(self, roastTabObject, MainWindowObject, recipes_object):
        super(RecipesTab, self).__init__()

        self.roastTab = roastTabObject
        self.MainWindow = MainWindowObject
        self.recipes_obj = recipes_object

        self.create_ui()

    def create_ui(self):
        """A method used to create the basic ui for the Recipe Tab."""
        self.layout = QtWidgets.QGridLayout()

        # Create recipe browser.
        self.browser = self.create_recipe_browser()
        self.layout.addWidget(self.browser, 0, 0)
        self.createNewRecipeButton = self.create_new_recipe_button()
        self.layout.addWidget(self.createNewRecipeButton, 1, 0)

        # Create recipe window.
        self.recipe_window = self.create_recipe_window()
        self.layout.addLayout(self.recipe_window, 0, 1)
        self.recipe_buttons = self.create_recipe_buttons()
        self.layout.addLayout(self.recipe_buttons, 1, 1)

        # Set stretch so items align correctly.
        self.layout.setColumnStretch(1, 2)
        self.layout.setRowStretch(0, 3)

        # Create label to cover recipe info.
        self.selectionLabel = QtWidgets.QLabel()
        self.selectionLabel.setObjectName("recipeSelectionLabel")
        self.selectionLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.selectionLabel, 0, 1)

        # Set main layout for widget.
        self.setLayout(self.layout)

    def create_recipe_browser(self):
        """Creates the side panel to browse all the files in the recipe folder.
        This method also adds a button to create new recipes to the layout."""
        # Creates model with all information about the files in ./recipes
        self.model = customqtwidgets.RecipeModel()
        self.model.setRootPath(os.path.expanduser('~/Documents/Openroast/Recipes/'))

        # Create a TreeView to view the information from the model
        browser = QtWidgets.QTreeView()
        browser.setModel(self.model)
        browser.setRootIndex(self.model.index(os.path.expanduser('~/Documents/Openroast/Recipes/')))
        browser.setFocusPolicy(QtCore.Qt.NoFocus)
        browser.header().close()

        browser.setAnimated(True)
        browser.setIndentation(0)

        # Hides all the unecessary columns created by the model
        browser.setColumnHidden(0, True)
        browser.setColumnHidden(1, True)
        browser.setColumnHidden(2, True)
        browser.setColumnHidden(3, True)

        browser.clicked.connect(self.on_recipeBrowser_clicked)

        return browser

    def create_new_recipe_button(self):

        # Add create new recipe button.
        createNewRecipeButton = QtWidgets.QPushButton("NEW RECIPE")
        createNewRecipeButton.clicked.connect(self.create_new_recipe)
        return createNewRecipeButton

    def create_recipe_window(self):
        """Creates the whole right-hand side of the recipe tab. These fields are
        populated when a recipe is chosen from the left column."""
        # Create all of the gui Objects
        window = QtWidgets.QGridLayout()
        self.nameLabel = QtWidgets.QLabel("Recipe Name")
        self.creatorLabel = QtWidgets.QLabel("Created by ")
        self.totalTimeLabel = QtWidgets.QLabel("Total Time: ")
        self.roastTypeLabel = QtWidgets.QLabel("Roast Type: ")
        self.beanRegionLabel = QtWidgets.QLabel("Bean Region: ")
        self.beanCountryLabel = QtWidgets.QLabel("Bean Country: ")
        self.descriptionBox = QtWidgets.QTextEdit()
        self.descriptionBox.setReadOnly(True)
        self.stepsTable = QtWidgets.QTableWidget()

        # Set options for recipe table.
        self.stepsTable.setShowGrid(False)
        self.stepsTable.setAlternatingRowColors(True)
        self.stepsTable.setCornerButtonEnabled(False)
        self.stepsTable.horizontalHeader().setSectionResizeMode(1)
        self.stepsTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.stepsTable.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)

        # Assign Object Names for qss
        self.nameLabel.setObjectName("RecipeName")
        self.creatorLabel.setObjectName("RecipeCreator")
        self.totalTimeLabel.setObjectName("RecipeTotalTime")
        self.roastTypeLabel.setObjectName("RecipeRoastType")
        self.beanRegionLabel.setObjectName("RecipeBeanRegion")
        self.beanCountryLabel.setObjectName("RecipeBeanCountry")
        self.stepsTable.setObjectName("RecipeSteps")

        # Add objects to the layout
        window.addWidget(self.nameLabel, 0, 0, 1, 2)
        window.addWidget(self.creatorLabel, 1, 0)
        window.addWidget(self.roastTypeLabel, 2, 0)
        window.addWidget(self.totalTimeLabel, 3, 0)
        window.addWidget(self.beanRegionLabel, 4, 0)
        window.addWidget(self.beanCountryLabel, 5, 0)
        window.addWidget(self.descriptionBox, 7, 0)
        window.addWidget(self.stepsTable, 7, 1)

        return window

    def create_recipe_buttons(self):
        """Creates the button panel on the bottom to allow for the user to
        interact with the currently selected/viewed recipe."""
        buttonsLayout = QtWidgets.QGridLayout()
        buttonsLayout.setSpacing(0)
        self.roastButton = QtWidgets.QPushButton("ROAST NOW")
        self.editRecipeButton = QtWidgets.QPushButton("EDIT")
        self.beanLinkButton = QtWidgets.QPushButton("PURCHASE BEANS")

        # Assign object names for qss styling.
        self.roastButton.setObjectName("smallButton")
        self.beanLinkButton.setObjectName("smallButton")
        self.editRecipeButton.setObjectName("smallButton")
        self.createNewRecipeButton.setObjectName("smallButtonAlt")

        # Add spacer.
        self.spacer = QtWidgets.QWidget()
        self.spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        buttonsLayout.addWidget(self.spacer)

        self.roastButton.clicked.connect(self.load_recipe)
        self.editRecipeButton.clicked.connect(self.open_recipe_editor)
        self.beanLinkButton.clicked.connect(self.open_link_in_browser)

        buttonsLayout.addWidget(self.beanLinkButton, 0, 1)
        buttonsLayout.addWidget(self.editRecipeButton, 0, 2)
        buttonsLayout.addWidget(self.roastButton, 0, 3)

        # Disable buttons until recipe is selected.
        self.beanLinkButton.setEnabled(False)
        self.editRecipeButton.setEnabled(False)
        self.roastButton.setEnabled(False)

        return buttonsLayout

    def on_recipeBrowser_clicked(self, index):
        """This method is used when a recipe is selected in the left column.
        This method also enables the bottom button panel after a recipe has
        been selected."""
        indexItem = self.model.index(index.row(), 0, index.parent())

        self.selectedFilePath = self.model.filePath(indexItem)

        # Allow single click expanding of folders
        if os.path.isdir(self.selectedFilePath):
            if self.browser.isExpanded(indexItem):
                self.browser.collapse(indexItem)
            else:
                self.browser.expand(indexItem)
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
            self.roastButton.setEnabled(True)

            # Hide recipe selection label once a recipe is selected.
            self.selectionLabel.setHidden(True)

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
        self.nameLabel.setText(recipeObject["roastName"])
        self.creatorLabel.setText("Created by " +
            recipeObject["creator"])
        self.roastTypeLabel.setText("Roast Type: " +
            recipeObject["roastDescription"]["roastType"])
        self.beanRegionLabel.setText("Bean Region: " +
            recipeObject["bean"]["region"])
        self.beanCountryLabel.setText("Bean Country: " +
            recipeObject["bean"]["country"])
        self.descriptionBox.setText(recipeObject["roastDescription"]
            ["description"])
        self.currentBeanUrl = recipeObject["bean"]["source"]["link"]

        # Total Time
        t = time.strftime("%M:%S", time.gmtime(recipeObject["totalTime"]))
        self.totalTimeLabel.setText("Total Time: " + t + " minutes")

        # Steps spreadsheet
        self.stepsTable.setRowCount(len(recipeObject["steps"]))
        self.stepsTable.setColumnCount(3)
        self.stepsTable.setHorizontalHeaderLabels(["Temperature",
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
            self.stepsTable.setItem(row, 0, sectionTempWidget)
            self.stepsTable.setItem(row, 1, sectionFanSpeedWidget)
            self.stepsTable.setItem(row, 2, sectionTimeWidget)

    def load_recipe(self):
        """Loads recipe into Roast tab."""
        if (self.recipes_obj.check_recipe_loaded()):
            self.roastTab.clear_roast()

        self.recipes_obj.load_recipe_json(self.currentlySelectedRecipe)
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
