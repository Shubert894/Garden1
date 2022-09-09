'''
This file contains all the logic and binding to the algorithmic part of the project.
It makes the connection to "tree_related" folder and draws the bucheim algorithm,
the tree classes and other primitives from it. 
'''
import tree_related.tree_test as tt
import tree_related.tree_drawing_alg as tda


class Model:
    def __init__(self) -> None:
        pass

    def buildTree(self):
        tree = tt.generateRandomTree(7,2)
        tda.buchheim(tree)
        tree.printTree()    
        return tree


if __name__ == '__main__':
    pass