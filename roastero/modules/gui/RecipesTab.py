from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os, json, time, webbrowser

class RecipesTab(QWidget):
    def __init__(self, recipeObject, roastTabObject, MainWindowObject):
        super(RecipesTab, self).__init__()

        # Pass in recipe object
        self.recipe = recipeObject

        self.roastTab = roastTabObject

        self.MainWindow = MainWindowObject

        self.create_ui()

    def create_ui(self):
        self.layout = QGridLayout()

        # Create recipe browser.
        self.create_recipe_browser()
        self.layout.addWidget(self.recipeBrowser, 0, 0)
        self.layout.addWidget(self.createNewRecipeButton, 1, 0)

        # Create recipe window.
        self.create_recipe_window()
        self.create_recipe_buttons()
        self.layout.addLayout(self.recipeWindow, 0, 1)
        self.layout.addLayout(self.recipeButtonsLayout, 1, 1)

        # Set stretch so items align correctly.
        self.layout.setColumnStretch(1, 2)
        self.layout.setRowStretch(0, 3)

        # Set main layout for widget.
        self.setLayout(self.layout)

    def create_recipe_browser(self):
        self.model = RecipeModel()
        self.model.setRootPath('./recipes')

        self.recipeBrowser = QTreeView()
        self.recipeBrowser.setModel(self.model)
        self.recipeBrowser.setRootIndex(self.model.index("./recipes"))
        self.recipeBrowser.setFocusPolicy(Qt.NoFocus)
        self.recipeBrowser.header().close()

        self.recipeBrowser.setAnimated(True)
        self.recipeBrowser.setIndentation(0)
        # self.recipeBrowser.setSortingEnabled(True)
        self.recipeBrowser.setColumnHidden(0, True)
        self.recipeBrowser.setColumnHidden(1, True)
        self.recipeBrowser.setColumnHidden(2, True)
        self.recipeBrowser.setColumnHidden(3, True)

        self.recipeBrowser.clicked.connect(self.on_recipeBrowser_clicked)
        self.createNewRecipeButton = QPushButton("NEW RECIPE")

    def create_recipe_window(self):
        # Create all of the gui Objects
        self.recipeWindow = QGridLayout()
        self.recipeNameLabel = QLabel("Recipe Name")
        self.recipeCreatorLabel = QLabel("Created by ")
        self.recipeTotalTimeLabel = QLabel("Total Time: ")
        self.recipeRoastTypeLabel = QLabel("Roast Type: ")
        self.beanRegionLabel = QLabel("Bean Region: ")
        self.beanCountryLabel = QLabel("Bean Country: ")
        self.recipeDescriptionBox = QTextEdit()
        self.recipeDescriptionBox.setReadOnly(True)
        self.recipeStepsTable = QTableWidget()

        # Assign Object Names for qss
        self.recipeNameLabel.setObjectName("RecipeName")
        self.recipeCreatorLabel.setObjectName("RecipeCreator")
        self.recipeTotalTimeLabel.setObjectName("RecipeTotalTime")
        self.recipeRoastTypeLabel.setObjectName("RecipeRoastType")
        self.beanRegionLabel.setObjectName("RecipeBeanRegion")
        self.beanCountryLabel.setObjectName("RecipeBeanCountry")
        self.recipeStepsTable.setObjectName("RecipeSteps")

        # Add objects to the layout
        self.recipeWindow.addWidget(self.recipeNameLabel, 0, 0, 1, 2)
        self.recipeWindow.addWidget(self.recipeCreatorLabel, 1, 0)
        self.recipeWindow.addWidget(self.recipeRoastTypeLabel, 2, 0)
        self.recipeWindow.addWidget(self.recipeTotalTimeLabel, 3, 0)
        self.recipeWindow.addWidget(self.beanRegionLabel, 4, 0)
        self.recipeWindow.addWidget(self.beanCountryLabel, 5, 0)
        self.recipeWindow.addWidget(self.recipeDescriptionBox, 7, 0)
        self.recipeWindow.addWidget(self.recipeStepsTable, 7, 1)

    def create_recipe_buttons(self):
        self.recipeButtonsLayout = QGridLayout()
        self.recipeButtonsLayout.setSpacing(0)
        self.recipeRoastButton = QPushButton("ROAST NOW")
        self.saveRecipeButton = QPushButton("EDIT")
        self.beanLinkButton = QPushButton("PURCHASE BEANS")

        # Assign object names for qss styling.
        self.recipeRoastButton.setObjectName("smallButton")
        self.beanLinkButton.setObjectName("smallButton")
        self.saveRecipeButton.setObjectName("smallButton")
        self.createNewRecipeButton.setObjectName("smallButtonAlt")

        # Add spacer.
        self.spacer = QWidget()
        self.spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.recipeButtonsLayout.addWidget(self.spacer)

        self.recipeRoastButton.clicked.connect(self.load_recipe)

        self.recipeButtonsLayout.addWidget(self.beanLinkButton, 0, 1)
        self.recipeButtonsLayout.addWidget(self.saveRecipeButton, 0, 2)
        self.recipeButtonsLayout.addWidget(self.recipeRoastButton, 0, 3)

    def on_recipeBrowser_clicked(self, index):
        indexItem = self.model.index(index.row(), 0, index.parent())

        filePath = self.model.filePath(indexItem)

        # Allow single click expanding of folders
        if os.path.isdir(filePath):
            if self.recipeBrowser.isExpanded(indexItem):
                self.recipeBrowser.collapse(indexItem)
            else:
                self.recipeBrowser.expand(indexItem)
        # Handles when a file is clicked
        else:
            with open(filePath) as json_data:
                recipeObject = json.load(json_data)
            self.load_recipe_information(recipeObject)

    def load_recipe_information(self, recipeObject):
        self.currentlySelectedRecipe = recipeObject

        self.recipeNameLabel.setText(recipeObject["roastName"])
        self.recipeCreatorLabel.setText("Created by " + recipeObject["creator"])
        self.recipeRoastTypeLabel.setText("Roast Type: " + recipeObject["roastDescription"]["roastType"])
        self.beanRegionLabel.setText("Bean Region: " + recipeObject["bean"]["region"])
        self.beanCountryLabel.setText("Bean Country: " + recipeObject["bean"]["country"])

        self.recipeDescriptionBox.setText(recipeObject["roastDescription"]["description"])
        self.currentBeanUrl = recipeObject["bean"]["source"]["link"]  
        self.beanLinkButton.clicked.connect(self.open_link_in_browser)

        # Total Time
        t = time.strftime("%M:%S", time.gmtime(recipeObject["totalTime"]))
        self.recipeTotalTimeLabel.setText("Total Time: " + t + " minutes")

        # Steps spreadsheet
        self.recipeStepsTable.setRowCount(len(recipeObject["steps"]))
        self.recipeStepsTable.setColumnCount(3)
        self.recipeStepsTable.setHorizontalHeaderLabels(["Temperature", "Fan Speed", "Section Time"])
        fanSpeedChoices = [str(x) for x in range(1,10)]
        targetTempChoices = ["Cooling"] + [str(x) for x in range(150, 501, 10)]
        for row in range(len(recipeObject["steps"])):
            # Temperature Value
            sectionTempWidget = ComboBoxNoWheel()
            sectionTempWidget.addItems(targetTempChoices)
            sectionTempWidget.insertSeparator(1)
            if 'targetTemp' in recipeObject["steps"][row]:
                sectionTemp = recipeObject["steps"][row]["targetTemp"]
                # Accommodate for temperature not fitting in 10 increment list
                if str(recipeObject["steps"][row]["targetTemp"]) in targetTempChoices:
                    sectionTempWidget.setCurrentIndex(targetTempChoices.index(str(recipeObject["steps"][row]["targetTemp"]))+1)
                else:
                    roundedNumber = recipeObject["steps"][row]["targetTemp"] - (recipeObject["steps"][row]["targetTemp"] % 10)
                    sectionTempWidget.insertItem(targetTempChoices.index(str(roundedNumber))+2, str(recipeObject["steps"][row]["targetTemp"]))
                    sectionTempWidget.setCurrentIndex(targetTempChoices.index(str(roundedNumber))+2)

            elif 'cooling' in recipeObject["steps"][row]:
                sectionTemp = "Cooling"
                sectionTempWidget.setCurrentIndex(targetTempChoices.index("Cooling"))


            # Time Value
            sectionTimeWidget = TimeEditNoWheel()
            sectionTimeWidget.setDisplayFormat("mm:ss")
            # Set QTimeEdit to the right time from recipe
            sectionTimeStr = time.strftime("%M:%S", time.gmtime(recipeObject["steps"][row]["sectionTime"]))
            sectionTime = QTime().fromString(sectionTimeStr, "mm:ss")
            sectionTimeWidget.setTime(sectionTime)

            # Fan Speed Value
            sectionFanSpeedWidget = ComboBoxNoWheel()
            sectionFanSpeedWidget.addItems(fanSpeedChoices)
            sectionFanSpeedWidget.setCurrentIndex(fanSpeedChoices.index(str(recipeObject["steps"][row]["fanSpeed"])))

            # Add widgets
            self.recipeStepsTable.setCellWidget(row, 0, sectionTempWidget)
            self.recipeStepsTable.setCellWidget(row, 1, sectionFanSpeedWidget)
            self.recipeStepsTable.setCellWidget(row, 2, sectionTimeWidget)

    def load_recipe(self):
        self.recipe.load_recipe_json(self.currentlySelectedRecipe)
        self.roastTab.load_recipe_into_roast_tab()
        self.MainWindow.select_roast_tab()

    def open_link_in_browser(self):
        webbrowser.open(self.currentBeanUrl)

class RecipeModel(QFileSystemModel):
    """A Subclass of QFileSystemModel to add a column"""
    def columnCount(self, parent = QModelIndex()):
        return super(RecipeModel, self).columnCount()+1

    def data(self, index, role):
        if index.column() == self.columnCount() - 1:
            if role == Qt.DisplayRole:
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

class ComboBoxNoWheel(QComboBox):
    def wheelEvent (self, event):
        event.ignore()

class TimeEditNoWheel(QTimeEdit):
    def wheelEvent (self, event):
        event.ignore()
