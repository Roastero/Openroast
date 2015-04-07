from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os, json, time
class RecipesTab(QWidget):
    def __init__(self):
        super(RecipesTab, self).__init__()

        self.create_ui()

    def create_ui(self):
        self.layout = QGridLayout()

        # Create recipe browser.
        self.create_recipe_browser()
        self.layout.addWidget(self.recipeBrowser, 0, 0)

        # Create recipe window.
        self.create_recipe_window()
        self.layout.addLayout(self.recipeWindow, 0, 1)
        self.layout.setColumnStretch(1, 2)

        # Set main layout for widget.
        self.setLayout(self.layout)


    def create_recipe_browser(self):
        self.model = RecipeModel()
        self.model.setRootPath('./recipes')
        #model.setIconProvider()
        self.recipeBrowser = QTreeView()
        self.recipeBrowser.setModel(self.model)
        self.recipeBrowser.setRootIndex(self.model.index("./recipes"))
        self.recipeBrowser.setFocusPolicy(Qt.NoFocus)
        self.recipeBrowser.header().close()

        self.recipeBrowser.setAnimated(True)
        self.recipeBrowser.setIndentation(0)
        self.recipeBrowser.setSortingEnabled(True)
        self.recipeBrowser.setColumnHidden(0, True)
        self.recipeBrowser.setColumnHidden(1, True)
        self.recipeBrowser.setColumnHidden(2, True)
        self.recipeBrowser.setColumnHidden(3, True)

        self.recipeBrowser.clicked.connect(self.on_recipeBrowser_clicked)

    def create_recipe_window(self):
        self.recipeWindow = QGridLayout()
        self.recipeNameLabel = QLabel("Recipe Name")
        self.recipeCreatorLabel = QLabel("Created by ")
        self.recipeTotalTimeLabel = QLabel("Total Time: ")
        self.recipeRoastTypeLabel = QLabel("Roast Type: ")
        self.beanRegionLabel = QLabel("Bean Region: ")
        self.beanCountryLabel = QLabel("Bean Country: ")
        self.beanLinkLabel = QLabel("Purchase the Beans here: ")
        self.recipeDescriptionBox = QTextEdit()
        self.recipeDescriptionBox.setReadOnly(True)
        self.recipeStepsTable = QTableWidget()
        self.recipeRoastButton = QPushButton("Roast Now")

        self.recipeWindow.addWidget(self.recipeNameLabel, 0, 0)
        self.recipeWindow.addWidget(self.recipeCreatorLabel, 1, 0)
        self.recipeWindow.addWidget(self.recipeRoastTypeLabel, 2, 0)
        self.recipeWindow.addWidget(self.recipeTotalTimeLabel, 3, 0)
        self.recipeWindow.addWidget(self.beanRegionLabel, 4, 0)
        self.recipeWindow.addWidget(self.beanCountryLabel, 5, 0)
        self.recipeWindow.addWidget(self.beanLinkLabel, 7, 0)
        self.recipeWindow.addWidget(self.recipeDescriptionBox, 8, 0)
        self.recipeWindow.addWidget(self.recipeStepsTable, 8, 1)
        self.recipeWindow.addWidget(self.recipeRoastButton, 9, 1)


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
            self.loadRecipeInformation(recipeObject)

    def loadRecipeInformation(self, recipeObject):
        self.recipeNameLabel.setText(recipeObject["roastName"])
        self.recipeCreatorLabel.setText("Created by " + recipeObject["creator"])
        self.recipeRoastTypeLabel.setText("Roast Type: " + recipeObject["roastDescription"]["roastType"])
        self.beanRegionLabel.setText("Bean Region: " + recipeObject["bean"]["region"])
        self.beanCountryLabel.setText("Bean Country: " + recipeObject["bean"]["country"])
        self.beanLinkLabel.setText("Purchase the Beans here: " + "<a href=\"" + \
        recipeObject["bean"]["source"]["link"] + "\">" + recipeObject["bean"]["source"]["reseller"] + "</a>")
        self.recipeDescriptionBox.setText(recipeObject["roastDescription"]["description"])

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
            sectionTime = time.strftime("%M:%S", time.gmtime(recipeObject["steps"][row]["sectionTime"]))
            sectionTimeWidget = QTableWidgetItem()
            sectionTimeWidget.setText(sectionTime)

            # Fan Speed Value
            sectionFanSpeedWidget = ComboBoxNoWheel()
            sectionFanSpeedWidget.addItems(fanSpeedChoices)
            sectionFanSpeedWidget.setCurrentIndex(fanSpeedChoices.index(str(recipeObject["steps"][row]["fanSpeed"])))

            # Add widgets
            self.recipeStepsTable.setCellWidget(row, 0, sectionTempWidget)
            self.recipeStepsTable.setCellWidget(row, 1, sectionFanSpeedWidget)
            self.recipeStepsTable.setItem(row, 2, sectionTimeWidget)

class RecipeModel(QFileSystemModel):
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
