from PyQt5.QtWidgets import *
from PyQt5.QtGui import QStandardItem, QStandardItemModel
class RecipesTab(QWidget):
    def __init__(self):
        super(RecipesTab, self).__init__()

        self.create_ui()

    def create_ui(self):
        self.layout = QGridLayout()

        # Create recipe browser.
        self.browser = self.create_recipe_browser()
        self.layout.addWidget(self.browser, 0, 0)

        # Set main layout for widget.
        self.setLayout(self.layout)


    def create_recipe_browser(self):
        recipeBrowser = QTextEdit()

        foods = [
            'Cookie dough', # Must be store-bought
            'Hummus', # Must be homemade
            'Spaghetti', # Must be saucy
            'Dal makhani', # Must be spicy
            'Chocolate whipped cream' # Must be plentiful
        ]

        return recipeBrowser
