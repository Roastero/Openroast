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
        self.setMinimumSize(800,600)
        #self.setWindowIcon(QIcon("icon.png"))

        # Open qss file.
        self.style = open('modules/gui/mainWindowStyle.css').read()
        self.setStyleSheet(self.style)

        # Create menu.
        self.create_menu()

        # Create toolbar.
        self.create_toolbar()

        # Create tabs.
        self.create_tabs()

    def create_menu(self):
        self.menuBar = QMenuBar()

        # Create file menu.
        self.fileMenu = self.menuBar.addMenu("File")
        self.fileMenu.addAction("Test")

    def create_toolbar(self):
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

        # Add spacer to set login button on the right.
        self.spacer = QWidget()
        self.spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.mainToolBar.addWidget(self.spacer)

        # Add login button.
        self.loginButton = QPushButton("SIGN IN", self)
        self.loginButton.setObjectName("loginButton")
        self.loginButton.clicked.connect(self.test)
        self.mainToolBar.addWidget(self.loginButton)

        # Add buttons to array to be disabled on selection.
        self.tabButtons = [self.roastTabButton,
                           self.recipesTabButton,
                           self.browseTabButton,
                           self.logTabButton]

    def create_tabs(self):
        self.tabs = QStackedWidget()

        # Create widgets to add to tabs.
        self.roast = RoastTab()
        self.recipes = RecipesTab()
        self.browse = BrowseTab()
        self.log = LogTab()

        # Add widgets to tabs.
        self.tabs.insertWidget(0, self.roast)
        self.tabs.insertWidget(1, self.recipes)
        self.tabs.insertWidget(2, self.browse)
        self.tabs.insertWidget(3, self.log)

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

    def select_browse_tab(self):
        self.tabs.setCurrentIndex(2)
        self.change_blocked_button(2)

    def select_log_tab(self):
        self.tabs.setCurrentIndex(3)
        self.change_blocked_button(3)

    def change_blocked_button(self, index):
        # Set all buttons enabled.
        for button in self.tabButtons:
            button.setEnabled(True)

        # Set selected button disabled.
        self.tabButtons[index].setEnabled(False)

    def test(self):
        print("test")
