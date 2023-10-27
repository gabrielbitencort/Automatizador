import sys
# from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi


class MyApplication(QMainWindow):
    def __init__(self):
        super(MyApplication, self).__init__()
        # Load the user interface
        loadUi('', self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApplication()
    window.show()
    sys.exit(app.exec_())
