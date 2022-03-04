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
        self.neighbors = []
        
    def move(self):
        a = self.rotation()
        p = Physics.t(self.pos())
        x, y = p
        a2 = math.pi*a/180
        xtemp = x + math.cos(a2)
        ytemp =  y + math.sin(a2)
        if self.inside(xtemp, ytemp):
            self.setPos(xtemp, ytemp)
            self.setRotation((a + random.uniform(-5, 5))%360)
        else:
            a_fin = (a + random.uniform(-5, 5)+90)%360
            self.setRotation(a_fin)
            x_fin = x + math.cos(a_fin)
            y_fin = y + math.sin(a_fin)
            self.setPos(x_fin, y_fin)

    def inside(self, x, y):
        size = Globals.environmentSize # 200
        extent = size/2

        if y > (extent):
            return False
        elif x > (extent):
            return False
        elif y < (-extent):
            return False
        elif x < (-extent):
            return False
        else:
            return True

    def paint(self, painter, option, widget=None): 
        painter.setPen(self.color)
        painter.drawRect(Host.bounds)
    
    def boundingRect(self):
        return Host.bounds
    
    def distance(self, B):
        x1, y1 = Physics.t(self.pos())
        x2, y2 = Physics.t(B.pos())
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def detection(self, physics) :
        p1 = Physics.t(self.pos())
        x1, y1 = p1
        for host in physics.hosts:
            if host != self : # you cant be your own neighbor
                p2 = Physics.t(host.pos())
                x2, y2 = p2
                if self.distance(host) ** 2 <= Globals.min_dist ** 2: # if you are in the circle you become a neighbor
                    self.neighbors.append(host)
