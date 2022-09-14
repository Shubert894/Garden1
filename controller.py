'''
This file is the orchestra conductor. It instantiates the program, thus
being it's entry point. It mediates and links the UI and the user input
with the model logic.
'''
import os

from model import Model
from top_view import App, TopView

class Controller:
    def __init__(self) -> None:
        self.model = Model()
        self.tree = None
        self.fNode = None

        self.app = App()
        self.view = TopView(self)

        self.initTree()

        self.app.run()
    

    def initTree(self):
        treeStructure = self.model.getTreeStructure()

        if treeStructure is None:
            self.tree = self.model.buildBlankTree()
            self.view.editArea.saveNode(self.tree)
            self.model.createStructureFile(self.tree)
        else:
            self.tree = self.model.assembleTree(treeStructure)

    def getTree(self):
        return self.tree

    def addNode(self):
        if self.fNode is not None:
            node = self.model.addBlankChildtoFocusNode(self.fNode)
            self.view.editArea.saveNode(node)
            self.model.createStructureFile(self.tree)
            self.model.updateTree(self.tree)

    def deleteFocusNode(self):
        if self.fNode is not None:
            self.model.deleteNode(self.fNode)
            self.model.updateTree(self.tree)

    def setFocusNode(self, node):
        # When a node is clicked, the TreeDrawer in draw_area calls this method
        # and sets the focus node in the controller. After that is done, the method
        # opens the right editor file by tapping into the editArea opneNode method.
        
        self.fNode = node
        if self.fNode is None:
            self.view.editArea.editor.clear()
        else:
            self.view.editArea.openNode(node)
        
        self.view.editArea.editor.clearFocus()
        self.view.drawArea.setFocus()
        print(self.fNode)

if __name__ == '__main__':
    controller = Controller()