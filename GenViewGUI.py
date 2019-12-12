from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys


def window():
    # this will inform the Q engine on system specifications
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setGeometry(200, 200, 800, 600)
    win.setWindowTitle("GenView")

    win.show()
    sys.exit(app.exec_())


window()
