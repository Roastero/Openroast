from PyQt5.QtWidgets import *
class RoastTab(QWidget):
    def __init__(self):
        super(RoastTab, self).__init__()
        button = QPushButton("Test", self)
        button.setObjectName("mainButton")
