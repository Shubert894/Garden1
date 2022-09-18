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
            self.saveNode(self.tree)
            self.model.createStructureFile(self.tree)
        else:
            self.tree = self.model.assembleTree(treeStructure)

        self.centerTreeOverCenterOfMass()
        # center tree over the centre of mass
        # center tree over the focused node

    def centerTreeOverCenterOfMass(self):
        tWidth, tHeight, rootCoord = self.model.getTreeParameters(self.tree)
        self.view.drawArea.treeDrawer.centerTreeOverCenter(tWidth, tHeight, rootCoord)
        print(f'{tWidth} - {tHeight} - {rootCoord}')
    
    def centerTreeOverFocusNode(self, oldX, oldY, newX, newY):
        self.view.drawArea.treeDrawer.centerTreeOverFocus(oldX,oldY,newX,newY)

    def getTree(self):
        return self.tree

    def openNode(self, node):
        if node is None: 
            return
        folderPath = os.path.abspath('notes')
        path = os.path.join(folderPath, node.getFileName())
        
        files = os.listdir(folderPath)
        if node.getFileName() not in files:
            self.saveNode(node)

        try:
            with open(path, 'r') as f:
                text = f.read()

        except Exception as e:
            self.view.editArea.dialog_critical(str(e))

        else:
            self.view.editArea.editor.setText(text)

    def saveNode(self, node):
        if node is None: 
            return  
        folderPath = os.path.abspath('notes')
        path = os.path.join(folderPath, node.getFileName())
        
        print(path)
        text = self.view.editArea.editor.toHtml()

        try:
            with open(path, 'w') as f:
                f.write(text)

        except Exception as e:
            self.view.editArea.dialog_critical(str(e))

    def addNode(self):
        if self.fNode is not None:
            node = self.model.addBlankChildtoFocusNode(self.fNode)
            #self.view.editArea.saveNode(node)
            self.model.createStructureFile(self.tree)

            x, y = self.fNode.x, self.fNode.y
            self.model.updateTree(self.tree)
            self.centerTreeOverFocusNode(x, y, self.fNode.x, self.fNode.y)

    def deleteFocusNode(self):
        if self.fNode is not None:
            self.model.deleteNode(self.fNode)
            self.model.updateTree(self.tree)
            self.centerTreeOverCenterOfMass()
    
    def setFocusNode(self, node):
        # When a node is clicked, the TreeDrawer in draw_area calls this method
        # and sets the focus node in the controller. After that is done, the method
        # opens the right editor file by tapping into the editArea opneNode method.
        
        self.fNode = node
        self.view.editArea.editor.clear()
        if self.fNode is not None:
            self.openNode(node)

        self.view.editArea.editor.clearFocus()
        self.view.drawArea.setFocus()

if __name__ == '__main__':
    controller = Controller()