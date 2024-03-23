import sys
from mainwindow import MyMainWindow
from PyQt5.QtWidgets import QApplication

class Main():
    
    def run(self):
        app = QApplication(sys.argv)
        mainWindow = MyMainWindow()
        mainWindow.show()
        sys.exit(app.exec_())