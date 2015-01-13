#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import QApplication
from gui.MainWindow import MainWindow

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
