from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class RecipeEditor(QDialog):
    def __init__(self):
        super(RecipeEditor, self).__init__()

        # Define main window for the application.
        self.setWindowTitle('Roastero')
        self.setMinimumSize(800,600)
        self.setContextMenuPolicy(Qt.NoContextMenu)
        #self.setWindowIcon(QIcon("icon.png"))

        # Open qss file.
        self.style = open('modules/gui/recipeEditorWindowStyle.css').read()
        self.setStyleSheet(self.style)
        
        self.textBrowser = QTextBrowser(self)
        self.textBrowser.append("This is a QTextBrowser!")

        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.addWidget(self.textBrowser)
