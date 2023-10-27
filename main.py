from PyQt5 import uic, QtWidgets
from PyQt5.Qt import Qt
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtPrintSupport import *
import os, sys

app=QtWidgets.QApplication([])
tela=uic.loadUi("UI/login.ui")
tela.show()
app.exec()