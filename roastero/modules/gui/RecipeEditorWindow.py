from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import json, time
from ..gui.CustomQtWidgets import TimeEditNoWheel, ComboBoxNoWheel, TableWidgetDragRows

class RecipeEditor(QDialog):
    def __init__(self, recipeLocation=None):
        super(RecipeEditor, self).__init__()

        # Define main window for the application.
        self.setWindowTitle('Roastero')
        self.setMinimumSize(800,600)
        self.setContextMenuPolicy(Qt.NoContextMenu)
        #self.setWindowIcon(QIcon("icon.png"))

        # Open qss file.
        self.style = open('modules/gui/mainStyle.css').read()
        self.setStyleSheet(self.style)

        self.create_ui()

        if recipeLocation:
            self.load_recipe_file(recipeLocation)
            self.preload_recipe_information()

    def create_ui(self):
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
        # Set bottom button layout.
        self.bottomButtonLayout = QHBoxLayout()
        self.bottomButtonLayout.setSpacing(0)
        
        # Create buttons.
        self.saveButton = QPushButton("SAVE")
        self.closeButton = QPushButton("CLOSE")
        
        # Assign object names to the buttons.
        self.saveButton.setObjectName("smallButton")
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
        recipeStepsTable = TableWidgetDragRows()
        recipeStepsTable.setShowGrid(False)
        recipeStepsTable.setAlternatingRowColors(True)
        recipeStepsTable.setCornerButtonEnabled(False)
        recipeStepsTable.horizontalHeader().setSectionResizeMode(1)
        # print(dir(recipeStepsTable))

        # Steps spreadsheet
        recipeStepsTable.setColumnCount(4)
        recipeStepsTable.setHorizontalHeaderLabels(["Temperature", "Fan Speed", "Section Time", "Reorder"])

        return recipeStepsTable

    def close_edit_window(self):
        self.close()

    def preload_recipe_steps(self, recipeStepsTable):
        # Create spreadsheet choices
        fanSpeedChoices = [str(x) for x in range(1,10)]
        targetTempChoices = ["Cooling"] + [str(x) for x in range(150, 501, 10)]

        # loop through recipe and load each step
        for row in range(len(self.recipe["steps"])):
            recipeStepsTable.insertRow(recipeStepsTable.rowCount())
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

            # Move QIcon
            moveIconItem = QTableWidgetItem()
            moveIconItem.setIcon(QIcon('modules/gui/images/downArrow.png'))

            # Add widgets
            recipeStepsTable.setCellWidget(row, 0, sectionTempWidget)
            recipeStepsTable.setCellWidget(row, 1, sectionFanSpeedWidget)
            recipeStepsTable.setCellWidget(row, 2, sectionTimeWidget)
            recipeStepsTable.setItem(row, 3, moveIconItem)

    def load_recipe_file(self, recipeFile):
        # Load recipe file
        recipeFileHandler = open(recipeFile)
        self.recipe = json.load(recipeFileHandler)
        recipeFileHandler.close()

    def preload_recipe_information(self):
        self.recipeName.setText(self.recipe["roastName"])
        self.recipeCreator.setText(self.recipe["creator"])
        self.recipeRoastType.setText(self.recipe["roastDescription"]["roastType"])
        self.beanRegion.setText(self.recipe["bean"]["region"])
        self.beanCountry.setText(self.recipe["bean"]["country"])
        self.beanLink.setText(self.recipe["bean"]["source"]["link"])
        self.beanStore.setText(self.recipe["bean"]["source"]["reseller"])
        self.recipeDescriptionBox.setText(self.recipe["roastDescription"]["description"])

        self.preload_recipe_steps(self.recipeSteps)
