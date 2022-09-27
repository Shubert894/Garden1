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
from editor.edit_area import EditArea 

from view.draw_area import DrawArea
import styles

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
        self.sWidth = geometry.width()
        self.sHeight = geometry.height()
        print(f'{self.sWidth} - {self.sHeight}')

        self.setStyleSheet(styles.drawAreaStyle)

        hbox = QtWidgets.QHBoxLayout()
        hbox.setContentsMargins(0,0,0,0)
        hbox.setSpacing(0) 
        
        self.drawArea = DrawArea(self.controller, int(self.sWidth*0.5), self.sHeight)
        self.editArea = EditArea(self.controller, int(self.sWidth*0.5), self.sHeight)
        hbox.addWidget(self.drawArea)
        hbox.addWidget(self.editArea)

        self.setFocus()
        self.setLayout(hbox)
        self.showMaximized()
       
    def resizeEvent(self, r: QtGui.QResizeEvent):
        self.sWidth = r.size().width()
        self.sHeight = r.size().height()
        self.drawArea.drawAreaVars.setWidth(int(self.sWidth/2))
        self.drawArea.drawAreaVars.setHeight(self.sHeight)
        self.editArea.setFixedWidth(int(self.sWidth/2))

if __name__ == '__main__':
    pass