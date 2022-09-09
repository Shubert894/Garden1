'''
The DrawArea is the main class for drawing the tree, the grid and everything
else on top and bottom. This class first initializes the DrawAreaVariables 
class that holds all the variables necessary for the drawing together with
some useful functions on this data. Then the Grid class is initialized which
contains the characteristics of the bacground grid together with the change
functionality upon receiving an input. Then the TreeDrawer class gets initialized
and it is in charge of drawing the main tree that it gets from the model through
the controller, also it performs all the change on a tree following user input.
'''
from PyQt6 import QtWidgets
from PyQt6 import QtCore
from PyQt6 import QtGui


class DrawArea(QtWidgets.QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.initDraw()
    
    def initDraw(self):
        self.drawAreaVars = DrawAreaVariables()
        self.grid = Grid(self.drawAreaVars)
        self.treeDrawer = TreeDrawer(self.drawAreaVars, self.controller)

    def paintEvent(self, e: QtGui.QPaintEvent):
        qp = QtGui.QPainter()
        qp.begin(self)
        #self.grid.drawGrid(qp)
        self.treeDrawer.drawTree(qp)
        self.update()
        qp.end()

    def resizeEvent(self, r: QtGui.QResizeEvent):
        self.drawAreaVars.setWidth(r.size().width())
        self.drawAreaVars.setHeight(r.size().height())
    
    def wheelEvent(self, e: QtGui.QWheelEvent):
        self.grid.changeGridOnWheelEvent(e.position().x(), e.position().y(), e.angleDelta().y())
    
    def mousePressEvent(self, e: QtGui.QMouseEvent):
        if e.type() == QtCore.QEvent.Type.MouseButtonPress:
            if e.button() == QtCore.Qt.MouseButton.LeftButton:
                self.grid.changeGridOnMousePressEvent(e.pos().x(), e.pos().y())
                self.treeDrawer.saveLocalClickPosition(e.pos().x(), e.pos().y())

    def mouseReleaseEvent(self, e: QtGui.QMouseEvent):
        if e.type() == QtCore.QEvent.Type.MouseButtonRelease:
            if e.button() == QtCore.Qt.MouseButton.LeftButton:
                self.treeDrawer.changeTreeDrawerOnMouseReleaseEvent(e.pos().x(), e.pos().y())

    def mouseMoveEvent(self, e: QtGui.QMouseEvent):     
        if e.type() == QtCore.QEvent.Type.MouseMove:
            if e.buttons() == QtCore.Qt.MouseButton.LeftButton:
                self.grid.changeGridOnMouseMoveEvent(e.pos().x(), e.pos().y())
  
    def keyPressEvent(self, e : QtGui.QKeyEvent):
        pass

class DrawAreaVariables:
    def __init__(self, scale = 40) -> None:
        self.scale = scale #the number of pixels that are between two discreet points in the DrawArea space
        self.width = 0
        self.height = 0
        self.originX = 0
        self.originY = 0
        self.circleDiameterAsPercentageOfScale = 0.8

        self.focusPen = QtGui.QPen(QtCore.Qt.GlobalColor.black, 2)
        self.focusBrush = QtGui.QBrush(QtCore.Qt.GlobalColor.blue)
        self.noFocusPen = QtGui.QPen(QtCore.Qt.GlobalColor.black, 2)
        self.noFocusBrush = QtGui.QBrush(QtCore.Qt.GlobalColor.green)
        self.linePen = QtGui.QPen(QtCore.Qt.GlobalColor.black, 4)

    def getGlobalCoordinates(self, localX ,localY):
        gX = (self.originX + localX) / self.scale
        gY = (self.originY + localY) / self.scale
        return gX, gY

    def getCircleRadius(self):
        return int(self.scale * self.circleDiameterAsPercentageOfScale / 2)

    def setCircleDiameterAsPercentageOfScale(self, r):
        self.circleDiameterAsPercentageOfScale = r

    def setScale(self, scale):
        self.scale = scale

    def setOriginX(self, newX):
        self.originX = newX
 
    def setOriginY(self, newY):
        self.originY = newY

    def setWidth(self, width):
        self.width = width
    
    def setHeight(self, height):
        self.height = height

class Grid:
    def __init__(self, drawAreaVars : DrawAreaVariables):
        self.dav = drawAreaVars
 
    def drawGrid(self, qp : QtGui.QPainter):
        pen = QtGui.QPen(QtCore.Qt.GlobalColor.black, 4)
        qp.setPen(pen)
 
        # ulX - local X and Y coordinates of the most upper left grid point generated
        ulX = self.dav.scale - self.dav.originX % self.dav.scale
        ulY = self.dav.scale - self.dav.originY % self.dav.scale
        # numPX - number of maximum visible grid points in X and Y direction
        numPX = self.dav.width // self.dav.scale + 1
        numPY = self.dav.height // self.dav.scale + 1
       
        for i in range(-1,numPY):
            for j in range(-1,numPX):
                qp.drawPoint(j * self.dav.scale + ulX, i * self.dav.scale + ulY)
 
    def changeGridOnMousePressEvent(self, x ,y):
        self.mouseX = x
        self.mouseY = y

    def changeGridOnWheelEvent(self, x, y, dz):
        if self.dav.scale <10 and dz<0:
            return

        nL = self.dav.scale + int(dz/30)
        zoom = nL / self.dav.scale

        newOriginX = zoom * (self.dav.originX + x) - x
        newOriginY = zoom * (self.dav.originY + y) - y

        self.dav.setScale(nL)
        self.dav.setOriginX(int(newOriginX))
        self.dav.setOriginY(int(newOriginY))

    def changeGridOnMouseMoveEvent(self, x ,y):
        try:
            dx = self.mouseX - x
            dy = self.mouseY - y
        except:
            dx = 0
            dy = 0

        self.dav.setOriginX(self.dav.originX + dx)
        self.dav.setOriginY(self.dav.originY + dy)

        self.mouseX = x
        self.mouseY = y

class TreeDrawer:
    def __init__(self, drawAreaVars : DrawAreaVariables, controller) -> None:
        self.dav = drawAreaVars
        self.controller = controller

        self.localClickX = 0
        self.localClickY = 0
        self.focusNode = None

    def drawTree(self, qp : QtGui.QPainter):        
        ulpX = self.dav.originX // self.dav.scale
        ulpY = self.dav.originY // self.dav.scale
        brpX = self.dav.originX // self.dav.scale + self.dav.width // self.dav.scale + 2
        brpY = self.dav.originY // self.dav.scale + self.dav.height // self.dav.scale + 2
        framePoints = [ulpX, ulpY, brpX, brpY]
        
        self.drawLines(self.controller.getTree(), qp)
        self.nodeDraw(self.controller.getTree(), framePoints, qp)

    def drawLines(self, node, qp : QtGui.QPainter):
        qp.setPen(self.dav.linePen)
        topNodeLocalX = node.x * self.dav.scale - self.dav.originX
        topNodeLocalY = node.y * self.dav.scale - self.dav.originY
        for child in node.children:
            bottomNodeLocalX = child.x * self.dav.scale - self.dav.originX
            bottomNodeLocalY = child.y * self.dav.scale - self.dav.originY
            qp.drawLine(topNodeLocalX,topNodeLocalY,bottomNodeLocalX,bottomNodeLocalY)
            self.drawLines(child, qp)

    def nodeDraw(self, node, framePoints, qp : QtGui.QPainter):
        qp.setPen(self.dav.noFocusPen)
        qp.setBrush(self.dav.noFocusBrush)
        #if node.x >= framePoints[0] and node.x <= framePoints[2] and node.y >= framePoints[1] and node.y <= framePoints[3]:  
        nodeLocalX = node.x * self.dav.scale - self.dav.originX
        nodeLocalY = node.y * self.dav.scale - self.dav.originY
        cR = self.dav.getCircleRadius()
        if node.isIdentical(self.focusNode):
            qp.setPen(self.dav.focusPen)
            qp.setBrush(self.dav.focusBrush)
        qp.drawEllipse(nodeLocalX - cR, nodeLocalY - cR, 2*cR, 2*cR)
        
        for child in node.children:
            self.nodeDraw(child, framePoints, qp)
    
    def changeTreeDrawerOnMouseReleaseEvent(self, x, y):
        if self.localClickX != x and self.localClickY != y:
            return   
        gX, gY = self.dav.getGlobalCoordinates(x, y)
        r = self.dav.getCircleRadius() / self.dav.scale
        clickedNode = self.nodeClicked(self.controller.getTree(), gX, gY, r)
        if clickedNode is None:
            self.focusNode = None
        else:
            if clickedNode.isIdentical(self.focusNode):
                self.focusNode = None
            else:    
                self.focusNode = clickedNode
        
        self.controller.setFocusNode(self.focusNode)
            

    def nodeClicked(self, node, x, y, cR):
        if (node.x - x)**2 + (node.y - y)**2 <= cR**2: 
            return node

        for child in node.children:
            res = self.nodeClicked(child, x, y, cR) 
            if res is not None:
                return res
        
        return None
    
    def saveLocalClickPosition(self, x, y):
        self.localClickX = x
        self.localClickY = y

if __name__ == '__main__':
    pass