import os
from typing import Container

from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtPrintSupport import *

def splitext(p):
    return os.path.splitext(p)[1].lower()

HTML_EXTENSIONS = ['.htm', '.html']

class TextEdit(QTextEdit):
    pass

class EditArea(QWidget):
    def __init__(self, controller, width, height):
        super().__init__()
        self.controller = controller
        self.eWidth = width
        self.eHeight = height
        self.initEditArea()
    
    def initEditArea(self):
        vbox = QVBoxLayout()
        vbox.setContentsMargins(0,0,0,0)
        vbox.setSpacing(0)

        self.editToolbar = QToolBar('Edit')
        self.editor = TextEdit()
        
        #self.editToolbar.setContentsMargins(0,0,0,0)
        self.editToolbar.setIconSize(QSize(20, 20))
        self.editToolbar.setStyleSheet('''QWidget{background-color: "grey";}''')

        self.aSave = QAction(QIcon(os.path.join('assets', 'images', 'save.png')), "", self)

        self.aBold = QAction(QIcon(os.path.join('assets', 'images', 'bold.png')), "", self)
        self.aItalic = QAction(QIcon(os.path.join('assets', 'images', 'italic.png')), "", self)
        self.aUnderline = QAction(QIcon(os.path.join('assets', 'images', 'underline.png')), "", self)
        self.aBold.setCheckable(True)
        self.aItalic.setCheckable(True)
        self.aUnderline.setCheckable(True)
        self.aBold.toggled.connect(lambda x: self.editor.setFontWeight(QFont.Weight.Bold if x else QFont.Weight.Normal))
        self.aItalic.toggled.connect(self.editor.setFontItalic)
        self.aUnderline.toggled.connect(self.editor.setFontUnderline)
        
        
        self.aLeft = QAction(QIcon(os.path.join('assets', 'images', 'left.png')), "", self)
        self.aRight = QAction(QIcon(os.path.join('assets', 'images', 'right.png')), "", self)
        self.aCenter = QAction(QIcon(os.path.join('assets', 'images', 'center.png')), "", self)
        self.aJusitfy = QAction(QIcon(os.path.join('assets', 'images', 'justify.png')), "", self)
        self.aLeft.setCheckable(True)
        self.aRight.setCheckable(True)
        self.aCenter.setCheckable(True)
        self.aJusitfy.setCheckable(True)
        self.aLeft.triggered.connect(lambda: self.editor.setAlignment(Qt.AlignmentFlag.AlignLeft))
        self.aRight.triggered.connect(lambda: self.editor.setAlignment(Qt.AlignmentFlag.AlignRight))
        self.aCenter.triggered.connect(lambda: self.editor.setAlignment(Qt.AlignmentFlag.AlignCenter))
        self.aJusitfy.triggered.connect(lambda: self.editor.setAlignment(Qt.AlignmentFlag.AlignJustify))

        self.aSave.triggered.connect(lambda: self.controller.saveNode(self.controller.fNode))

        format_group = QActionGroup(self)
        format_group.setExclusive(True)
        format_group.addAction(self.aLeft)
        format_group.addAction(self.aRight)
        format_group.addAction(self.aCenter)
        format_group.addAction(self.aJusitfy)
        
        self.aBullet = QAction(QIcon(os.path.join('assets', 'images', 'bullet.png')), "", self)
        self.aChecklist = QAction(QIcon(os.path.join('assets', 'images', 'checklist.png')), "", self)
        self.aNumbered = QAction(QIcon(os.path.join('assets', 'images', 'numbered.png')), "", self)
   
        self.editToolbar.addAction(self.aSave)

        self.editToolbar.addAction(self.aBold)
        self.editToolbar.addAction(self.aItalic)
        self.editToolbar.addAction(self.aUnderline)
        
        self.editToolbar.addAction(self.aLeft)
        self.editToolbar.addAction(self.aCenter)
        self.editToolbar.addAction(self.aRight)
        self.editToolbar.addAction(self.aJusitfy)

        self.editToolbar.addAction(self.aBullet)
        self.editToolbar.addAction(self.aChecklist)
        self.editToolbar.addAction(self.aNumbered)

        vbox.addWidget(self.editToolbar)

        #self.editor.setContentsMargins(0,0,0,0)
        self.editor.setFrameStyle(0)
        self.editor.setStyleSheet('''QWidget{background-color: "grey";
                                        padding: 20px;}''')
        
        self.editor.setAutoFormatting(QTextEdit.AutoFormattingFlag.AutoAll)
        self.editor.selectionChanged.connect(self.updateFormat)

        font = QFont('Times',12)
        self.editor.setFont(font)
        self.editor.setFontPointSize(12)

        vbox.addWidget(self.editor)
        self.setLayout(vbox)

        self.formatActions = [
            # self.fontsize,
            self.aBold,
            self.aItalic,
            self.aUnderline,
        ]

        self.updateFormat()

    def block_signals(self, objects, b):
        for o in objects:
            o.blockSignals(b)

    def updateFormat(self):
        self.block_signals(self.formatActions, True)

        # self.fontsize.setCurrentText(str(int(self.editor.fontPointSize())))

        self.aItalic.setChecked(self.editor.fontItalic())
        self.aUnderline.setChecked(self.editor.fontUnderline())
        self.aBold.setChecked(self.editor.fontWeight() == QFont.Weight.Bold)


        self.aLeft.setChecked(self.editor.alignment() == Qt.AlignmentFlag.AlignLeft)
        self.aRight.setChecked(self.editor.alignment() == Qt.AlignmentFlag.AlignRight)
        self.aCenter.setChecked(self.editor.alignment() == Qt.AlignmentFlag.AlignCenter)
        self.aJusitfy.setChecked(self.editor.alignment() == Qt.AlignmentFlag.AlignJustify)

        self.block_signals(self.formatActions, False)

    def dialog_critical(self, s):
        dlg = QMessageBox(self)
        dlg.setText(s)
        dlg.setIcon(QMessageBox.Icon.Critical)
        dlg.show()


        


        