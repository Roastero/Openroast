#!/usr/bin/env python3

# Standard Library Imports
import sys

# PyQt imports
from PyQt5.QtWidgets import QApplication

# Local project imports
from modules.gui.MainWindow import MainWindow

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
