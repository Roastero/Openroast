from PyQt5.QtWidgets import *
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtCore import *
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
        self.recipeBrowser = QListWidget(self)

        foods = [
            'Cookie dough', # Must be store-bought
            'Hummus', # Must be homemade
            'Spaghetti', # Must be saucy
            'Dal makhani', # Must be spicy
            'Chocolate whipped cream' # Must be plentiful
        ]

        for row in foods:
            self.recipeBrowser.addItem(row)

    def create_recipe_window(self):
        self.recipeWindow = QWidget()
