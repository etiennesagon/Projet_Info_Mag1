from PyQt5.QtGui import QColor
import random

class Disease() :
    def __init__(self, color, virulence, duration, ID):
        self.color = color
        self.virulence = virulence
        self.duration = duration
        self.ID = ID
    
    def mutation(self):
        delta = [random.uniform(-0.01,0.01) for _ in range(5)]
        # mutations are random
        red = self.color.redF() + delta[0]
        green = self.color.greenF() + delta[1]
        blue = self.color.blueF() + delta[2]
        if (red >= 0 and red <= 1) and (green >= 0 and green <= 1) and (blue >= 0 and blue <= 1):
            self.color = QColor.fromRgb(red, green, blue)
        virulence = self.virulence + delta[3]
        if virulence >= 0 and virulence <= 1:
            self.virulence = virulence
        duration = self.duration + delta[4]
        if duration >= 0:
            self.duration = duration



