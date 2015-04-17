from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import json, time, os
from functools import partial
from ..gui.CustomQtWidgets import TimeEditNoWheel, ComboBoxNoWheel
from ..tools.fileNameFormatter import format_filename

class RecipeEditor(QDialog):
    def __init__(self, recipeLocation=None):
        super(RecipeEditor, self).__init__()

        # Define main window for the application.
        self.setWindowTitle('Roastero')
        self.setMinimumSize(800,600)
        self.setContextMenuPolicy(Qt.NoContextMenu)
        #self.setWindowIcon(QIcon("icon.png"))

        # Open qss file.
        self.style = open('static/mainStyle.css').read()
        self.setStyleSheet(self.style)

        self.create_ui()

        self.recipe = {}
        self.recipe["steps"] = [{'fanSpeed': 5, 'targetTemp': 150, 'sectionTime': 0}]

        if recipeLocation:
            self.load_recipe_file(recipeLocation)
            self.preload_recipe_information()
        else:
            self.preload_recipe_steps(self.recipeSteps)

    def create_ui(self):
        """A method used to create the basic ui for the Recipe Editor Window"""
        # Create main layout for window.
        self.layout = QGridLayout(self)
        self.layout.setRowStretch(1, 3)

        # Create input fields.
        self.create_input_fields()
        self.layout.addLayout(self.inputFieldLayout, 0, 0, 1, 2)

        # Create big edit boxes.
        self.create_big_edit_boxes()
        self.layout.addLayout(self.bigEditLayout, 1, 0, 1, 2)

        # Create Bottom Buttons.
        self.create_bottom_buttons()
        self.layout.addLayout(self.bottomButtonLayout, 2, 0, 1, 2)


    def create_input_fields(self):
        """Creates all of the UI components for the top of the Recipe Editor
        Window."""
        # Create layout for section.
        self.inputFieldLayout = QGridLayout()

        # Create labels for fields.
        recipeNameLabel = QLabel("Recipe Name: ")
        recipeCreatorLabel = QLabel("Created by: ")
        recipeRoastTypeLabel = QLabel("Roast Type: ")
        beanRegionLabel = QLabel("Bean Region: ")
        beanCountryLabel = QLabel("Bean Country: ")
        beanLinkLabel = QLabel("Bean Link: ")
        beanStoreLabel = QLabel("Bean Store Name: ")

        # Create input fields.
        self.recipeName = QLineEdit()
        self.recipeCreator = QLineEdit()
        self.recipeRoastType = QLineEdit()
        self.beanRegion = QLineEdit()
        self.beanCountry = QLineEdit()
        self.beanLink = QLineEdit()
        self.beanStore = QLineEdit()

        # Remove focus from input boxes.
        self.recipeName.setAttribute(Qt.WA_MacShowFocusRect, 0)
        self.recipeCreator.setAttribute(Qt.WA_MacShowFocusRect, 0)
        self.recipeRoastType.setAttribute(Qt.WA_MacShowFocusRect, 0)
        self.beanRegion.setAttribute(Qt.WA_MacShowFocusRect, 0)
        self.beanCountry.setAttribute(Qt.WA_MacShowFocusRect, 0)
        self.beanLink.setAttribute(Qt.WA_MacShowFocusRect, 0)
        self.beanStore.setAttribute(Qt.WA_MacShowFocusRect, 0)

        # Add objects to the inputFieldLayout
        self.inputFieldLayout.addWidget(recipeNameLabel, 0, 0)
        self.inputFieldLayout.addWidget(self.recipeName, 0, 1)
        self.inputFieldLayout.addWidget(recipeCreatorLabel, 1, 0)
        self.inputFieldLayout.addWidget(self.recipeCreator, 1, 1)
        self.inputFieldLayout.addWidget(recipeRoastTypeLabel, 2, 0)
        self.inputFieldLayout.addWidget(self.recipeRoastType, 2, 1)
        self.inputFieldLayout.addWidget(beanRegionLabel, 3, 0)
        self.inputFieldLayout.addWidget(self.beanRegion, 3, 1)
        self.inputFieldLayout.addWidget(beanCountryLabel, 4, 0)
        self.inputFieldLayout.addWidget(self.beanCountry, 4, 1)
        self.inputFieldLayout.addWidget(beanLinkLabel, 5, 0)
        self.inputFieldLayout.addWidget(self.beanLink, 5, 1)
        self.inputFieldLayout.addWidget(beanStoreLabel, 6, 0)
        self.inputFieldLayout.addWidget(self.beanStore, 6, 1)

    def create_big_edit_boxes(self):
        """Creates the Bottom section of the Recipe Editor Window. This method
        creates the Description box and calls another method to make the
        recipe steps table."""
        # Create big edit box layout.
        self.bigEditLayout = QGridLayout()

        # Create labels for the edit boxes.
        recipeDescriptionBoxLabel = QLabel("Description: ")
        recipeStepsLabel = QLabel("Steps: ")

        # Create widgets.
        self.recipeDescriptionBox = QTextEdit()
        self.recipeSteps = self.create_steps_spreadsheet()

        # Add widgets to layout.
        self.bigEditLayout.addWidget(recipeDescriptionBoxLabel, 0, 0)
        self.bigEditLayout.addWidget(self.recipeDescriptionBox, 1, 0)
        self.bigEditLayout.addWidget(recipeStepsLabel, 0, 1)
        self.bigEditLayout.addWidget(self.recipeSteps, 1, 1)

    def create_bottom_buttons(self):
        """Creates the button panel on the bottom of the Recipe Editor
        Window."""
        # Set bottom button layout.
        self.bottomButtonLayout = QHBoxLayout()
        self.bottomButtonLayout.setSpacing(0)

        # Create buttons.
        self.saveButton = QPushButton("SAVE")
        self.closeButton = QPushButton("CLOSE")

        # Assign object names to the buttons.
        self.saveButton.setObjectName("smallButton")
        self.saveButton.clicked.connect(self.save_recipe)
        self.closeButton.setObjectName("smallButton")
        self.closeButton.clicked.connect(self.close_edit_window)

        # Create Spacer.
        self.spacer = QWidget()
        self.spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Add widgets to the layout.
        self.bottomButtonLayout.addWidget(self.spacer)
        self.bottomButtonLayout.addWidget(self.closeButton)
        self.bottomButtonLayout.addWidget(self.saveButton)

    def create_steps_spreadsheet(self):
        """Creates Recipe Steps table. It does not populate the table in this
        method."""
        recipeStepsTable = QTableWidget()
        recipeStepsTable.setShowGrid(False)
        recipeStepsTable.setAlternatingRowColors(True)
        recipeStepsTable.setCornerButtonEnabled(False)
        recipeStepsTable.horizontalHeader().setSectionResizeMode(1)

        # Steps spreadsheet
        recipeStepsTable.setColumnCount(4)
        recipeStepsTable.setHorizontalHeaderLabels(["Temperature", "Fan Speed", "Section Time", "Modify"])

        return recipeStepsTable

    def close_edit_window(self):
        """Method used to close the Recipe Editor Window."""
        self.close()

    def preload_recipe_steps(self, recipeStepsTable):
        """Method that just calls load_recipe_steps() with a table specified and
        uses the pre-existing loaded recipe steps in the object."""
        steps = self.recipe["steps"]
        self.load_recipe_steps(recipeStepsTable, steps)

    def load_recipe_steps(self, recipeStepsTable, steps):
        """Takes two arguments. One being the table and the second being the
        rows you'd like to add. It does not clear the table and simply adds the
        rows on the bottom if there are exiting rows."""
        # Create spreadsheet choices
        fanSpeedChoices = [str(x) for x in range(1,10)]
        targetTempChoices = ["Cooling"] + [str(x) for x in range(150, 501, 10)]

        # loop through recipe and load each step
        for row in range(len(steps)):
            recipeStepsTable.insertRow(recipeStepsTable.rowCount())
            # Temperature Value
            sectionTempWidget = ComboBoxNoWheel()
            sectionTempWidget.addItems(targetTempChoices)
            sectionTempWidget.insertSeparator(1)
            if 'targetTemp' in steps[row]:
                sectionTemp = steps[row]["targetTemp"]
                # Accommodate for temperature not fitting in 10 increment list
                if str(steps[row]["targetTemp"]) in targetTempChoices:
                    sectionTempWidget.setCurrentIndex(targetTempChoices.index(str(steps[row]["targetTemp"]))+1)
                else:
                    roundedNumber = steps[row]["targetTemp"] - (steps[row]["targetTemp"] % 10)
                    sectionTempWidget.insertItem(targetTempChoices.index(str(roundedNumber))+2, str(steps[row]["targetTemp"]))
                    sectionTempWidget.setCurrentIndex(targetTempChoices.index(str(roundedNumber))+2)

            elif 'cooling' in steps[row]:
                sectionTemp = "Cooling"
                sectionTempWidget.setCurrentIndex(targetTempChoices.index("Cooling"))


            # Time Value
            sectionTimeWidget = TimeEditNoWheel()
            sectionTimeWidget.setDisplayFormat("mm:ss")
            # Set QTimeEdit to the right time from recipe
            sectionTimeStr = time.strftime("%M:%S", time.gmtime(steps[row]["sectionTime"]))
            sectionTime = QTime().fromString(sectionTimeStr, "mm:ss")
            sectionTimeWidget.setTime(sectionTime)

            # Fan Speed Value
            sectionFanSpeedWidget = ComboBoxNoWheel()
            sectionFanSpeedWidget.addItems(fanSpeedChoices)
            sectionFanSpeedWidget.setCurrentIndex(fanSpeedChoices.index(str(steps[row]["fanSpeed"])))

            # Modify Row field
            upArrow = QPushButton()
            upArrow.setIcon(QIcon('modules/gui/images/upArrow.png'))
            upArrow.clicked.connect(partial(self.move_recipe_step_up, row))
            downArrow = QPushButton()
            downArrow.setIcon(QIcon('modules/gui/images/downArrow.png'))
            downArrow.clicked.connect(partial(self.move_recipe_step_down, row))
            deleteRow = QPushButton("X")
            deleteRow.clicked.connect(partial(self.delete_recipe_step, row))
            insertRow = QPushButton("+")
            insertRow.clicked.connect(partial(self.insert_recipe_step, row))

            # Create a grid layout to add all the widgets to
            modifyRowWidgetLayout = QGridLayout()
            modifyRowWidgetLayout.setSpacing(0)
            modifyRowWidgetLayout.addWidget(upArrow, 0, 0)
            modifyRowWidgetLayout.addWidget(downArrow, 1, 0)
            modifyRowWidgetLayout.addWidget(deleteRow, 0, 1)
            modifyRowWidgetLayout.addWidget(insertRow, 1, 1)

            # Assign Layout to a QWidget to add to a single column
            modifyRowWidget = QWidget()
            modifyRowWidget.setLayout(modifyRowWidgetLayout)

            # Add widgets
            recipeStepsTable.setCellWidget(row, 0, sectionTempWidget)
            recipeStepsTable.setCellWidget(row, 1, sectionFanSpeedWidget)
            recipeStepsTable.setCellWidget(row, 2, sectionTimeWidget)
            recipeStepsTable.setCellWidget(row, 3, modifyRowWidget)

    def load_recipe_file(self, recipeFile):
        """Takes a file location and opens that file. It then loads the contents
        which should be JSON and makes a python dictionary from the contents.
        The python dictionary is created as self.recipe."""
        # Load recipe file
        recipeFileHandler = open(recipeFile)
        self.recipe = json.load(recipeFileHandler)
        self.recipe["file"] = recipeFile
        recipeFileHandler.close()

    def preload_recipe_information(self):
        """Loads information from self.recipe and prefills all the fields in the
        form."""
        self.recipeName.setText(self.recipe["roastName"])
        self.recipeCreator.setText(self.recipe["creator"])
        self.recipeRoastType.setText(self.recipe["roastDescription"]["roastType"])
        self.beanRegion.setText(self.recipe["bean"]["region"])
        self.beanCountry.setText(self.recipe["bean"]["country"])
        self.beanLink.setText(self.recipe["bean"]["source"]["link"])
        self.beanStore.setText(self.recipe["bean"]["source"]["reseller"])
        self.recipeDescriptionBox.setText(self.recipe["roastDescription"]["description"])

        self.preload_recipe_steps(self.recipeSteps)

    def move_recipe_step_up(self, row):
        """This method will take a row and swap it the row above it."""
        if row != 0:
            steps = self.get_current_table_values()
            newSteps = steps

            # Swap the steps
            newSteps[row], newSteps[row-1] = newSteps[row-1], newSteps[row]

            # Rebuild table with new steps
            self.rebuild_recipe_steps_table(newSteps)

    def move_recipe_step_down(self, row):
        """This method will take a row and swap it the row below it."""
        if row != self.recipeSteps.rowCount()-1:
            steps = self.get_current_table_values()
            newSteps = steps

            # Swap the steps
            newSteps[row], newSteps[row+1] = newSteps[row+1], newSteps[row]

            # Rebuild table with new steps
            self.rebuild_recipe_steps_table(newSteps)

    def delete_recipe_step(self, row):
        """This method will take a row delete it."""
        steps = self.get_current_table_values()
        newSteps = steps

        # Delete step
        newSteps.pop(row)

        # Rebuild table with new steps
        self.rebuild_recipe_steps_table(newSteps)

    def insert_recipe_step(self, row):
        """Inserts a row below the specified row wit generic values."""
        steps = self.get_current_table_values()
        newSteps = steps

        # insert step
        newSteps.insert(row+1, {'fanSpeed': 5, 'targetTemp': 150, 'sectionTime': 0})

        # Rebuild table with new steps
        self.rebuild_recipe_steps_table(newSteps)

    def get_current_table_values(self):
        """Used to read all the current table values from the recipeSteps table
        and build a dictionary of all the values."""
        recipeSteps = []
        for row in range(0, self.recipeSteps.rowCount()):
            currentRow = {}
            currentRow["sectionTime"] = QTime(0, 0, 0).secsTo(self.recipeSteps.cellWidget(row, 2).time())
            currentRow["fanSpeed"] = int(self.recipeSteps.cellWidget(row, 1).currentText())

            # Get Temperature or cooling
            if self.recipeSteps.cellWidget(row, 0).currentText() == "Cooling":
                currentRow["cooling"] = True
            else:
                currentRow["targetTemp"] = int(self.recipeSteps.cellWidget(row, 0).currentText())

            recipeSteps.append(currentRow)

        # Return copied rows
        return recipeSteps

    def rebuild_recipe_steps_table(self, newSteps):
        """Used to reload all the rows in the recipe steps table with new steps.
        """
        # Alert user if they try to delete all the steps
        if len(newSteps) < 1:
            alert = QMessageBox()
            alert.setWindowTitle('Roastero')
            alert.setStyleSheet(self.style)
            alert.setText("You must have atleast one step!")
            alert.exec_()

        else:
            # Delete all the current rows
            while self.recipeSteps.rowCount() > 0:
                self.recipeSteps.removeRow(0)
            # Add the new step sequence
            self.load_recipe_steps(self.recipeSteps, newSteps)

    def save_recipe(self):
        """Pulls in all of the information in the window and creates a new
        recipe file with the specified contents."""
        # Determine Recipe File Name
        if "file" in self.recipe:
            filePath = self.recipe["file"]
        else:
            filePath = os.path.abspath("./recipes/local") + "/" + format_filename(self.recipeName.text()) + ".json"
            # TODO: Account for existing file with same name

        # Create Dictionary with all the new recipe information
        self.newRecipe = {}
        self.newRecipe["roastName"] = self.recipeName.text()
        self.newRecipe["steps"] = self.get_current_table_values()
        self.newRecipe["roastDescription"] = {}
        self.newRecipe["roastDescription"]["roastType"] = self.recipeRoastType.text()
        self.newRecipe["roastDescription"]["description"] = self.recipeDescriptionBox.toPlainText()
        self.newRecipe["creator"] = self.recipeCreator.text()
        self.newRecipe["bean"] = {}
        self.newRecipe["bean"]["region"] = self.beanRegion.text()
        self.newRecipe["bean"]["country"] = self.beanCountry.text()
        self.newRecipe["bean"]["source"] = {}
        self.newRecipe["bean"]["source"]["reseller"] = self.beanStore.text()
        self.newRecipe["bean"]["source"]["link"] = self.beanLink.text()
        self.newRecipe["totalTime"] = 0
        for step in self.newRecipe["steps"]:
            self.newRecipe["totalTime"] += step["sectionTime"]

        # Write the recipe to a file
        jsonObject = json.dumps(self.newRecipe, indent=4)
        file = open(filePath, 'w')
        file.write(jsonObject)
        file.close()
