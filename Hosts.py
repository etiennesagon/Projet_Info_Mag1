import Globals
import math
import random
import Physics
import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore


class Host(QtWidgets.QGraphicsItem):
    length = Globals.hostsLength
    width = 2*length/9
    bounds = QtCore.QRectF(-.5*length, -.5*width, length, width)
    
    def __init__(self, color, health, infected, x, y, a):
        super().__init__()
        self.color = color
        self.health = health
        self.infected = infected
        self.setPos(x, y) 
        self.setRotation(a)
        
    def move(self):
        a = self.rotation()
        p = Physics.t(self.pos())
        x, y = p
        a2 = math.pi*a/180
        xtemp = x + math.cos(a2)
        ytemp =  y + math.sin(a2)
        verif_x, verif_y = self.bounce(xtemp, ytemp) # toroidal
        self.setPos(verif_x, verif_y)
        a_ = (a + random.uniform(-5, 5))%360 
        self.setRotation(a_)

    def paint(self, painter, option, widget=None): 
        painter.setPen(self.color)
        painter.drawRect(Host.bounds)
    
    def boundingRect(self):
        return Host.bounds
    
    def bounce(self, x, y):
        size = Globals.environmentSize # 200
        extent = size/2 # 100
        # toroidal rules
        # goes up
        if y > (extent):
            if x > (extent): 
                return x-1, y-1
            elif x < (-extent):
                return x+1, y-1
            else:
                return x, y-1
        # goes down
        elif y < (-extent):
            if x > (extent):
                return x-1, y+1
            elif x < (-extent):
                return x+1, y+1
            else:
                return x, y+1
        # goes right
        if x > (extent):
            return x, y-1
        # goes left
        elif x < (-extent):
            return x, y+1

        return x, y
