import unittest, sys
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFontDatabase
from openroast.modules.gui.MainWindow import MainWindow

class MainWindowTest(unittest.TestCase):
    def setUp(self):
        self.app = QApplication(sys.argv)
        # Set application style.
        QFontDatabase.addApplicationFont("static/fonts/asap/asap-regular.ttf")
        QFontDatabase.addApplicationFont("static/fonts/asap/asap-bold.ttf")
        QFontDatabase.addApplicationFont("static/fonts/asap/asap-bold-italic.ttf")
        QFontDatabase.addApplicationFont("static/fonts/asap/asap-italic.ttf")
        style = open('static/mainStyle.css').read()
        QApplication.setStyleSheet(self.app, style)

        self.window = MainWindow()

    def test_creation(self):
        self.assertTrue(isinstance(self.window, MainWindow))
