from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os, json
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
        self.layout.addWidget(self.recipeWindow, 0, 1)
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
        self.recipeWindow = QPlainTextEdit()
        text=open('./recipes/Favorites/test01.json').read()
        self.recipeWindow.setPlainText(text)

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
            self.recipeWindow.setPlainText(recipeObject["roastName"])

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
