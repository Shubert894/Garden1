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
        #tda.buchheim(tree)
        return tree

    def updateTree(self, tree : t.Node):
        return tda.buchheim(tree)

    def deleteNode(self, node: t.Node):

        def deleteNodeFromTree(node: t.Node):
            for child in node.children:
                deleteNodeFromTree(child)
            node.parent.removeChild(node.getId())

        def deleteNodeFromFolder(node: t.Node):
            for child in node.children:
                deleteNodeFromFolder(child)
            fp.deleteFile(node.getFileName())
            fp.deleteNodeFromStructure(node.getId())

        parent = node.getParent()
        if parent is not None:
            print(node.children)
            deleteNodeFromFolder(node)
            deleteNodeFromTree(node)

    def getTreeStructure(self):
        file = fp.hasStructureFile()
        if file:
            return fp.getStructure()
        else:
            return None
    
    def createStructureFile(self, tree):

        def introduceNodeToStructure(node, tS):
            data = {'name' : node.getName(),
                    'parentId' : None if node.getParent() is None else node.getParent().getId()}
            tS[node.getId()] = data
            
            for child in node.children:
                introduceNodeToStructure(child, tS)
            
        treeStructure = {}
        introduceNodeToStructure(tree, treeStructure)
        fp.saveStructure(treeStructure)     
    
    def assembleTree(self, treeStructure : dict):
        def attachChildren(node):
            for key in treeStructure.keys():
                if treeStructure[key]['parentId'] == node.getId():
                    childNode = t.Node(treeStructure[key]['name'],node,[])
                    childNode.setId(key)
                    node.addChild(childNode)
                    attachChildren(childNode)
                        
        tree = None
        for key in treeStructure.keys():
            if treeStructure[key]['parentId'] is None:
                tree = t.Node(treeStructure[key]['name'],None,[])
                tree.setId(key)
                treeStructure.pop(key)
                break

        attachChildren(tree)
        self.updateTree(tree)
        return tree

    def addBlankChildtoFocusNode(self, fNode : t.Node):
        node = t.Node('untitled',fNode,[])
        fNode.addChild(node)
        return node

if __name__ == '__main__':
    pass