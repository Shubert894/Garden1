'''
Generates a tree for visualization and testing of the drawing algorithm.

Main function: generateRandomTree(depth, maxChildren)
'''

import random
import time

class Node:
    def __init__(self, data):
        self.data = data
        self.children = []
        self.id = str(random.randint(100000000, 999999999)) + str(time.time()).replace('.', '')
        self.parent = None
        self.x = 0
        self.y = 0

    def addChild(self, child):
        child.parent = self
        self.children.append(child)

    def isIdentical(self, other):
        if other is None:
            return False
        if self.id == other.id:
            return True
        return False

    def getLevel(self):
        level = 0
        p = self.parent
        while p:
            level += 1
            p = p.parent
        return level

    def printTree(self):
        indent = self.getLevel() * 2 * ' ' + '|-'
        print(f'{indent}({self.x};{self.y})')
        if self.children:
            for child in self.children:
                child.printTree()


def generateRandomTree(depth = 3, maxChildren = 3):
    if depth > 1:
        n = Node(depth)
        for i in range(random.randint(0, maxChildren)):
            n.addChild(generateRandomTree(depth - 1, maxChildren))
        return n
    else:
        return Node(depth)


if __name__ == '__main__':
    tree = generateRandomTree(4,3)
