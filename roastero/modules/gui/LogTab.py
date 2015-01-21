from PyQt5.QtWidgets import *
class LogTab(QWidget):
    def __init__(self):
        super(LogTab, self).__init__()

        self.create_ui()

    def create_ui(self):
        self.layout = QGridLayout()


        # Set main layout for widget.
        self.setLayout(self.layout)
