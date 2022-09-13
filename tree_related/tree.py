'''
The file that contains the building blocks of the main tree structure.
One can create a tree from scratch (reference to the main) or add/remove
nodes to/from an already existing tree.

Node
- children
- parent
- data

- id
- position in the tree

+ add node (parent node, node)
+ remove node (parent node)

'''
import time
import random

class Node:
    def __init__(self, name = 'untitled' ,parent = None, children : list = []) -> None:
        self.id = str(random.randint(100000000, 999999999)) + str(time.time()).replace('.', '')
        self.name = name
        self.parent = parent
        self.children = children

    def getName(self):
        return self.name

    def getID(self):
        return self.id

    def getFileName(self):
        return f'{self.name}_{self.id}.html'
    
    def getParent(self):
        return self.parent
    
    def isIdentical(self, other):
        if other is None:
            return False
        if self.id == other.id:
            return True
        return False

    def addChild(self, node):
        if self is None:
            return

        self.children.append(node)

    def removeChild(self, id):
        for i, node in enumerate(self.children):
            if node.id == id:
                self.children.pop(i)
                del node
                
    def __del__(self):
        pass
        #print(f'Node disposed. Id : {self.id}')


def dfs(node : Node):
    print(node.id)
    if len(node.children) == 0:
        return

    for c in enumerate(node.children):
        dfs(c)
    


def main():
    t = Node(children=[Node(Node(children=[Node(),Node()])),Node()])
    dfs(t)


if __name__ == '__main__':
    main()