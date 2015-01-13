from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from .RoastTab import RoastTab
from .RecipesTab import RecipesTab
from .LogTab import LogTab
from .BrowseTab import BrowseTab

class MainWindow(QMainWindow):
    def __init__(self):
        # Define main window for the application.
        super(MainWindow, self).__init__()
        self.setWindowTitle('Roastero')
        self.setMinimumSize(800,500)
        #self.setWindowIcon(QIcon("icon.png"))

        # Open qss file.
        self.style = open('mainWindowStyle.css').read()
        self.setStyleSheet(self.style)

        # Create menu.
        self.create_menu()

        # Create toolbar.
        self.create_toolbar()

        # Set the default widget.
        self.roast = RoastTab()
        self.roastTabButton.setEnabled(False)
        self.setCentralWidget(self.roast)

    def create_menu(self):
        self.menuBar = QMenuBar()

        # Create file menu.
        self.fileMenu = self.menuBar.addMenu("File")
        self.fileMenu.addAction("Test")

    def create_toolbar(self):
        self.mainToolBar = self.addToolBar('mainToolBar')
        self.mainToolBar.setMovable(False)

        # Add logo.
        self.logo = QLabel("ROASTERO")
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

        # Add browse tab button.
        self.browseTabButton = QPushButton("BROWSE", self)
        self.browseTabButton.setObjectName("toolbar")
        self.browseTabButton.clicked.connect(self.select_browse_tab)
        self.mainToolBar.addWidget(self.browseTabButton)

        # Add log tab button.
        self.logTabButton = QPushButton("LOG", self)
        self.logTabButton.setObjectName("toolbar")
        self.logTabButton.clicked.connect(self.select_log_tab)
        self.mainToolBar.addWidget(self.logTabButton)

        self.loginButton = QPushButton("SIGN IN", self)
        self.loginButton.setObjectName("loginButton")
        self.loginButton.clicked.connect(self.test)
        self.mainToolBar.addWidget(self.loginButton)

    def select_roast_tab(self):
        self.roast = RoastTab()
        self.setCentralWidget(self.roast)

    def select_recipes_tab(self):
        self.recipes = RecipesTab()
        self.setCentralWidget(self.recipes)

    def select_browse_tab(self):
        self.browse = BrowseTab()
        self.setCentralWidget(self.browse)

    def select_log_tab(self):
        self.log = LogTab()
        self.setCentralWidget(self.log)

    def test(self):
        print("test")
