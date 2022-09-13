'''
This file contains all the logic and binding to the algorithmic part of the project.
It makes the connection to "tree_related" folder and draws the bucheim algorithm,
the tree classes and other primitives from it. 
'''
import tree_related.tree as t
import tree_related.tree_drawing_alg as tda
import file_related.file_primitives as fp

class Model:
    def __init__(self) -> None:
        pass

    def buildBlankTree(self):
        tree = t.Node('root', None, [])
        tda.buchheim(tree)
        return tree

    def updateTree(self, tree : t.Node):
        return tda.buchheim(tree)

    def deleteNode(self, node: t.Node):

        def deleteNodeFromTree(node: t.Node):
            for child in node.children:
                deleteNodeFromTree(child)
            node.parent.removeChild(node.getID())

        def deleteNodeFromFolder(node: t.Node):
            for child in node.children:
                deleteNodeFromFolder(child)
            fp.deleteFile(node.getFileName())

        parent = node.getParent()
        if parent is not None:
            print(node.children)
            deleteNodeFromFolder(node)
            deleteNodeFromTree(node)


    def addBlankChildtoFocusNode(self, fNode : t.Node):
        node = t.Node('untitled',fNode,[])
        fNode.addChild(node)
        return node

if __name__ == '__main__':
    pass