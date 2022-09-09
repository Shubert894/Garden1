'''
This file is the orchestra conductor. It instantiates the program, thus
being it's entry point. It mediates and links the UI and the user input
with the model logic.
'''
from model import Model
from top_view import App, TopView

class Controller:
    def __init__(self) -> None:
        self.model = Model()
        self.tree = self.model.buildTree()
        self.fNode = None

        self.app = App()
        self.view = TopView(self)
        self.app.run()
    
    def getTree(self):
        return self.tree

    def setFocusNode(self, node):
        self.fNode = node
        print(self.fNode)

if __name__ == '__main__':
    controller = Controller()