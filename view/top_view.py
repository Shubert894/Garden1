'''
This file has the app initialization code as well as the top layer of the UI
The main class called TopView initializes a horizontal layout and puts two
widgets in it. The first one is called DrawArea and represents the part of 
the garden that is drawn. The second one represent the EditArea and contains
the editor and the tools to modify the text inside it. 
'''
import sys

from PyQt6 import QtWidgets
from PyQt6 import QtCore
from PyQt6 import QtGui 

from view.draw_area import DrawArea

class App:
    def __init__(self) -> None:
        self.app = QtWidgets.QApplication(sys.argv)

    def run(self):
        sys.exit(self.app.exec())

class TopView(QtWidgets.QWidget):
    def __init__(self, controller) -> None:
        super().__init__()
        self.controller = controller
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Garden')
        geometry = self.screen().availableGeometry()
        self.setGeometry(geometry)
        
        hbox = QtWidgets.QHBoxLayout()
        hbox.setContentsMargins(0,0,0,0)
        hbox.setSpacing(0) 
        
        drawArea = DrawArea(controller = self.controller)
        # editArea = ...
        hbox.addWidget(drawArea)
        # hbox.addWidget(editArea)


        self.setLayout(hbox)
        self.showMaximized()

if __name__ == '__main__':
    pass