# PyQt imports
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# Local project imports
from .RoastTab import RoastTab
from .RecipesTab import RecipesTab
from .RoastLogTab import RoastLogTab
from .AboutWindow import About
from .PreferencesWindow import PreferencesWindow
from ..roaster_libraries.FreshRoastSR700 import FreshRoastSR700
from ..roaster_libraries.Recipe import Recipe

# Standard Library Imports
import json, os
from shutil import copy2

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Define main window for the application.
        self.setWindowTitle('Roastero')
        self.setMinimumSize(800,600)
        self.setContextMenuPolicy(Qt.NoContextMenu)
        #self.setWindowIcon(QIcon("icon.png"))

        # Open qss file.
        QFontDatabase.addApplicationFont("static/fonts/asap/asap-regular.ttf")
        QFontDatabase.addApplicationFont("static/fonts/asap/asap-bold.ttf")
        QFontDatabase.addApplicationFont("static/fonts/asap/asap-bold-italic.ttf")
        QFontDatabase.addApplicationFont("static/fonts/asap/asap-italic.ttf")
        self.style = open('static/mainStyle.css').read()
        self.setStyleSheet(self.style)

        # Create toolbar.
        self.create_toolbar()

        # Create Recipe and Roaster objects
        self.roaster = FreshRoastSR700()
        self.recipe = Recipe(self.roaster)

        # Create tabs.
        self.create_tabs()

        # Create menu.
        self.createActions()
        self.create_menus()

    def createActions(self):
        # File menu actions.
        self.clearRoastAct = QAction("&Clear", self, shortcut=QKeySequence(
            Qt.CTRL + Qt.SHIFT + Qt.Key_C),
            statusTip="Clear the roast window",
            triggered=self.roast.clear_roast)

        self.newRoastAct = QAction("&Roast Again", self,
            shortcut=QKeySequence(Qt.CTRL + Qt.Key_R),
            statusTip="Roast recipe again",
            triggered=self.roast.reset_current_roast)

        self.importRecipeAct = QAction("&Import Recipe", self,
            shortcut=QKeySequence(Qt.CTRL + Qt.Key_I),
            statusTip="Import a recipe file",
            triggered=self.import_recipe_file)

        self.exportRecipeAct = QAction("&Export Recipe", self,
            shortcut=QKeySequence(Qt.CTRL + Qt.Key_E),
            statusTip="Export a recipe file",
            triggered=self.export_recipe_file)

        self.saveRoastGraphAct = QAction("&Save Roast Graph", self,
            shortcut=QKeySequence(Qt.CTRL + Qt.Key_K),
            statusTip="Save an image of the roast graph",
            triggered=self.roast.save_roast_graph)

        self.openAboutWindow = QAction("&About", self,
            statusTip="About Roastero",
            triggered=self.open_about_window)

        self.openPreferencesWindow = QAction("&Preferences", self,
            statusTip="Change Roastero settings",
            triggered=self.open_preferences_window)

    def create_menus(self):
        menubar = self.menuBar()

        # Create file menu.
        self.fileMenu = menubar.addMenu("&File")
        self.fileMenu.addAction(self.clearRoastAct)
        self.fileMenu.addAction(self.newRoastAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.importRecipeAct)
        self.fileMenu.addAction(self.exportRecipeAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.saveRoastGraphAct)
        self.fileMenu.addSeparator()

        # Create edit menu.
        self.editMenu = menubar.addMenu("&Edit")
        self.editMenu.addAction(self.openPreferencesWindow)

        # Create help menu.
        self.helpMenu = menubar.addMenu("&Help")
        self.helpMenu.addAction(self.openAboutWindow)

    def create_toolbar(self):
        # Create toolbar.
        self.mainToolBar = self.addToolBar('mainToolBar')
        self.mainToolBar.setMovable(False)
        self.mainToolBar.setFloatable(False)

        # Add logo.
        self.logo = QLabel("ROASTERO")
        self.logo.setObjectName("logo")
        self.mainToolBar.addWidget(self.logo)

        # Add roasting tab button.
        self.roastTabButton = QPushButton("ROAST", self)
        self.roastTabButton.setObjectName("toolbar")
        self.roastTabButton.clicked.connect(self.select_roast_tab)
        self.mainToolBar.addWidget(self.roastTabButton)

        # Add recipes tab button.
        self.recipesTabButton = QPushButton("RECIPES", self)
        self.recipesTabButton.setObjectName("toolbar")
        self.recipesTabButton.clicked.connect(self.select_recipes_tab)
        self.mainToolBar.addWidget(self.recipesTabButton)

        # Add roast log tab button.
        self.roastLogTabButton = QPushButton("ROAST LOG", self)
        self.roastLogTabButton.setObjectName("toolbar")
        self.roastLogTabButton.clicked.connect(self.select_roastLog_tab)
        self.mainToolBar.addWidget(self.roastLogTabButton)

        # Add spacer to set login button on the right.
        self.spacer = QWidget()
        self.spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.mainToolBar.addWidget(self.spacer)

        # Add buttons to array to be disabled on selection.
        self.tabButtons = [self.roastTabButton,
                           self.recipesTabButton,
                           self.roastLogTabButton]

    def create_tabs(self):
        self.tabs = QStackedWidget()

        # Create widgets to add to tabs.
        self.roast = RoastTab(roasterObject = self.roaster, recipeObject = self.recipe)
        self.recipes = RecipesTab(recipeObject = self.recipe, roastTabObject = self.roast, MainWindowObject = self)
        self.roastLog = RoastLogTab()

        # Add widgets to tabs.
        self.tabs.insertWidget(0, self.roast)
        self.tabs.insertWidget(1, self.recipes)
        self.tabs.insertWidget(2, self.roastLog)

        # Set the tabs as the central widget.
        self.setCentralWidget(self.tabs)

        # Set the roast button disabled.
        self.roastTabButton.setEnabled(False)

    def select_roast_tab(self):
        self.tabs.setCurrentIndex(0)
        self.change_blocked_button(0)

    def select_recipes_tab(self):
        self.tabs.setCurrentIndex(1)
        self.change_blocked_button(1)

    def select_roastLog_tab(self):
        self.tabs.setCurrentIndex(2)
        self.change_blocked_button(2)

    def change_blocked_button(self, index):
        # Set all buttons enabled.
        for button in self.tabButtons:
            button.setEnabled(True)

        # Set selected button disabled.
        self.tabButtons[index].setEnabled(False)

    def import_recipe_file(self):
        try:
            recipeFile = QFileDialog.getOpenFileName(self, 'Select Recipe',
                os.path.expanduser('~/'), 'Recipes (*.json);;All Files (*)')
            copy2(recipeFile[0], os.path.expanduser('~/Documents/Roastero/recipes/local'))
        except FileNotFoundError:
            # Occurs if file browser is canceled
            pass
        else:
            pass

    def export_recipe_file(self):
        try:
            recipeFile = QFileDialog.getSaveFileName(self, 'Export Recipe',
                os.path.expanduser('~/'), 'Recipes (*.json);;All Files (*)')
            jsonObject = json.dumps(self.roast.get_recipe_object().get_current_recipe(), indent=4)

            file = open(recipeFile[0], 'w')
            file.write(jsonObject)
            file.close()
        except FileNotFoundError:
            # Occurs if file browser is canceled
            pass
        else:
            pass

    def open_about_window(self):
        self.aboutWindow = About()
        self.aboutWindow.exec_()

    def open_preferences_window(self):
        self.preferencesWindow = PreferencesWindow()
        self.preferencesWindow.exec_()
