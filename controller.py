'''
This file is the orchestra conductor. It instantiates the program, thus
being it's entry point. It mediates and links the UI and the user input
with the model logic.
'''
from model import Model
from view.top_view import App, TopView

class Controller:
    def __init__(self) -> None:
        self.model = Model()
        self.app = App()
        self.view = TopView(self)
        self.app.run()
    
    def getTree(self):
        return self.model.getTree()

if __name__ == '__main__':
    controller = Controller()