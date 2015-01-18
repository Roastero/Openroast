from PyQt5.QtWidgets import *
from PyQt5.QtCore import QUrl
from PyQt5.QtWebKitWidgets import QWebView
class BrowseTab(QWidget):
    def __init__(self):
        super(BrowseTab, self).__init__()

        self.create_ui()

    def create_ui(self):
        self.layout = QGridLayout()

        view = QWebView()
        view.load(QUrl('http://google.com'))
        self.layout.addWidget(view, 0, 0)

        # Set main layout for widget.
        self.setLayout(self.layout)
