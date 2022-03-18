import Globals
import math
import random
import Physics
import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui

def toss(x, y):
     flip = random.randint(0, 1)
     if flip == 0:
         return x
     else:
         return y

class Host(QtWidgets.QGraphicsItem):
    length = Globals.hostsLength
    width = 2*length/9
    bounds = QtCore.QRectF(-.5*length, -.5*width, length, width)
    
    def __init__(self, color, health, infected, x, y, a, timer, ID):
        super().__init__()
        self.color = color
        self.health = health
        self.infected = infected
        self.setPos(x, y) 
        self.setRotation(a)
        self.neighbors = []
        self.timer = timer
        self.ID = ID
        self.disease = None
        self.time_before_recovery = 0
        
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
        if not self.infected:
            
            painter.drawRect(Host.bounds)
        if self.infected:
            #painter.setPen(QtGui.QColor.fromRgb(0,0,0))
            painter.fillRect(Host.bounds, self.color)
    
    def boundingRect(self):
        return Host.bounds
    
    def distance(self, B):
        x1, y1 = Physics.t(self.pos())
        x2, y2 = Physics.t(B.pos())
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def detection(self, physics) :
        self.neighbors = []
        p1 = Physics.t(self.pos())
        x1, y1 = p1
        for host in physics.hosts:
            if host != self : # you cant be your own neighbor
                p2 = Physics.t(host.pos())
                x2, y2 = p2
                if self.distance(host) ** 2 <= Globals.min_dist ** 2: # if you are in the circle you become a neighbor
                    self.neighbors.append(host)
                    
    def reproduction(self,physics):
        if len(physics.hosts) < Globals.MaxnbHosts and len(self.neighbors) > 0 and self.timer == 0:
            partner = random.choice(self.neighbors)
            proba_repro = 0.3
            P = random.uniform(0, 1)
            if P < proba_repro:
                x_partner, y_partner = Physics.t(partner.pos())
                x_self, y_self = Physics.t(self.pos())
                x_mean = (x_partner + x_self)/2
                y_mean = (y_partner + y_self) / 2
                baby = (QtGui.QColor.fromRgbF(toss(self.color.redF(), partner.color.redF()),
                                                       toss(self.color.greenF(), partner.color.greenF()),
                                                       toss(self.color.blueF(),partner.color.blueF())),
                                                        1,
                                                        False,
                                                        x_mean, 
                                                        y_mean, 
                                                        random.uniform(0, 360), 500, 
                                                        len(physics.hosts) + 1)
               
                self.timer = 100
                for i, guy in enumerate(physics.hosts):
                    if guy.ID == partner.ID:
                        physics.hosts[i].timer = 100
                #partner.timer = 100

                return baby


    def susceptibility(self, disease):
        red1 = self.color.redF()
        green1 = self.color.greenF()
        blue1 = self.color.blueF()

        red2 = disease.color.redF()
        green2 = disease.color.greenF()
        blue2 = disease.color.blueF()

        dist = math.sqrt((red1-red2)**2 + (green1-green2)**2 + (blue1-blue2)**2)
        return (1-dist)/math.sqrt(3) # normalization (divide by dist max)

#TODO:
# si infecté, la health du host diminue de 0.01 * la virulence de la maladie 
# (pour durer au minimum 100 pas de temps) 

    def infection(self, physics):
        if self.infected and len(self.neighbors)>0:
            for neighbor in self.neighbors:
                if not neighbor.infected:
                    p = random.uniform(0,1)
                    if p < neighbor.susceptibility(self.disease)*self.disease.virulence:
                        ID = neighbor.ID
                        for i, guy in enumerate(physics.hosts):
                            if guy.ID == ID:
                                physics.hosts[i].infected = True
                                physics.hosts[i].disease = self.disease
                                physics.hosts[i].time_before_recovery = self.disease.duration



