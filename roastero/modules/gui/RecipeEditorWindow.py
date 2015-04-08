from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import json, time

class RecipeEditor(QDialog):
    def __init__(self, recipeLocation):
        super(RecipeEditor, self).__init__()

        # Define main window for the application.
        self.setWindowTitle('Roastero')
        self.setMinimumSize(800,600)
        self.setContextMenuPolicy(Qt.NoContextMenu)
        #self.setWindowIcon(QIcon("icon.png"))

        # Open qss file.
        self.style = open('modules/gui/recipeEditorWindowStyle.css').read()
        self.setStyleSheet(self.style)

        self.load_recipe_file(recipeLocation)

        self.create_ui()

    def create_ui(self):
        self.layout = QGridLayout(self)

        recipeNameLabel = QLabel("Recipe Name: ")
        recipeCreatorLabel = QLabel("Created by: ")
        recipeTotalTimeLabel = QLabel("Total Time: ")
        recipeRoastTypeLabel = QLabel("Roast Type: ")
        beanRegionLabel = QLabel("Bean Region: ")
        beanCountryLabel = QLabel("Bean Country: ")
        beanLinkLabel = QLabel("Bean Link: ")
        beanStoreLabel = QLabel("Bean Store Name: ")
        recipeDescriptionBoxLabel = QLabel("Description: ")
        recipeStepsLabel = QLabel("Steps: ")

        self.recipeName = QLineEdit()
        self.recipeCreator = QLineEdit()
        self.recipeTotalTime = QLineEdit()
        self.recipeRoastType = QLineEdit()
        self.beanRegion = QLineEdit()
        self.beanCountry = QLineEdit()
        self.beanLink = QLineEdit()
        self.beanStore = QLineEdit()
        self.recipeDescriptionBox = QTextEdit()

        self.recipeSteps = self.create_steps_speadsheet()

        self.preload_recipe_information()

        # Add objects to the layout
        self.layout.addWidget(recipeNameLabel, 0, 0)
        self.layout.addWidget(self.recipeName, 0, 1)
        self.layout.addWidget(recipeCreatorLabel, 1, 0)
        self.layout.addWidget(self.recipeCreator, 1, 1)
        self.layout.addWidget(recipeRoastTypeLabel, 2, 0)
        self.layout.addWidget(self.recipeRoastType, 2, 1)
        self.layout.addWidget(recipeTotalTimeLabel, 3, 0)
        self.layout.addWidget(self.recipeTotalTime, 3, 1)
        self.layout.addWidget(beanRegionLabel, 4, 0)
        self.layout.addWidget(self.beanRegion, 4, 1)
        self.layout.addWidget(beanCountryLabel, 5, 0)
        self.layout.addWidget(self.beanCountry, 5, 1)
        self.layout.addWidget(recipeDescriptionBoxLabel, 7, 0)
        self.layout.addWidget(self.recipeDescriptionBox, 8, 0)
        self.layout.addWidget(recipeStepsLabel, 7, 1)
        self.layout.addWidget(self.recipeSteps, 8, 1)


    def create_steps_speadsheet(self):
        recipeStepsTable = QTableWidget()
        # Steps spreadsheet
        recipeStepsTable.setRowCount(len(self.recipe["steps"]))
        recipeStepsTable.setColumnCount(3)
        recipeStepsTable.setHorizontalHeaderLabels(["Temperature", "Fan Speed", "Section Time"])

        # Create spreadsheet choices
        fanSpeedChoices = [str(x) for x in range(1,10)]
        targetTempChoices = ["Cooling"] + [str(x) for x in range(150, 501, 10)]

        # loop through recipe and load each step
        for row in range(len(self.recipe["steps"])):
            # Temperature Value
            sectionTempWidget = ComboBoxNoWheel()
            sectionTempWidget.addItems(targetTempChoices)
            sectionTempWidget.insertSeparator(1)
            if 'targetTemp' in self.recipe["steps"][row]:
                sectionTemp = self.recipe["steps"][row]["targetTemp"]
                # Accommodate for temperature not fitting in 10 increment list
                if str(self.recipe["steps"][row]["targetTemp"]) in targetTempChoices:
                    sectionTempWidget.setCurrentIndex(targetTempChoices.index(str(self.recipe["steps"][row]["targetTemp"]))+1)
                else:
                    roundedNumber = self.recipe["steps"][row]["targetTemp"] - (self.recipe["steps"][row]["targetTemp"] % 10)
                    sectionTempWidget.insertItem(targetTempChoices.index(str(roundedNumber))+2, str(self.recipe["steps"][row]["targetTemp"]))
                    sectionTempWidget.setCurrentIndex(targetTempChoices.index(str(roundedNumber))+2)

            elif 'cooling' in self.recipe["steps"][row]:
                sectionTemp = "Cooling"
                sectionTempWidget.setCurrentIndex(targetTempChoices.index("Cooling"))


            # Time Value
            sectionTimeWidget = TimeEditNoWheel()
            sectionTimeWidget.setDisplayFormat("mm:ss")
            # Set QTimeEdit to the right time from recipe
            sectionTimeStr = time.strftime("%M:%S", time.gmtime(self.recipe["steps"][row]["sectionTime"]))
            sectionTime = QTime().fromString(sectionTimeStr, "mm:ss")
            sectionTimeWidget.setTime(sectionTime)

            # Fan Speed Value
            sectionFanSpeedWidget = ComboBoxNoWheel()
            sectionFanSpeedWidget.addItems(fanSpeedChoices)
            sectionFanSpeedWidget.setCurrentIndex(fanSpeedChoices.index(str(self.recipe["steps"][row]["fanSpeed"])))

            # Add widgets
            recipeStepsTable.setCellWidget(row, 0, sectionTempWidget)
            recipeStepsTable.setCellWidget(row, 1, sectionFanSpeedWidget)
            recipeStepsTable.setCellWidget(row, 2, sectionTimeWidget)

        return recipeStepsTable

    def load_recipe_file(self, recipeFile):
        # Load recipe file
        recipeFileHandler = open(recipeFile)
        self.recipe = json.load(recipeFileHandler)
        recipeFileHandler.close()

    def preload_recipe_information(self):
        self.recipeName.setText(self.recipe["roastName"])
        self.recipeCreator.setText(self.recipe["creator"])
        self.recipeTotalTime.setText(str(self.recipe["totalTime"]))
        self.recipeRoastType.setText(self.recipe["roastDescription"]["roastType"])
        self.beanRegion.setText(self.recipe["bean"]["region"])
        self.beanCountry.setText(self.recipe["bean"]["country"])
        self.beanLink.setText(self.recipe["bean"]["source"]["link"])
        self.beanStore.setText(self.recipe["bean"]["source"]["reseller"])
        self.recipeDescriptionBox.setText(self.recipe["roastDescription"]["description"])

class ComboBoxNoWheel(QComboBox):
    def wheelEvent (self, event):
        event.ignore()

class TimeEditNoWheel(QTimeEdit):
    def wheelEvent (self, event):
        event.ignore()
