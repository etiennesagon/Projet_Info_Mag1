from PyQt5.QtGui import QColor
import random

class Disease() :
    def __init__(self, color, virulence, duration, ID):
        self.color = color
        self.virulence = virulence
        self.duration = duration
        self.ID = ID
    
    def mutation(self):
        delta = [random.uniform(-0.01,0.01) for _ in range(4)]
        # mutations are random
        assert self.color[0] != 0
        red = self.color[0] + delta[0]
        green = self.color[1] + delta[1]
        blue = self.color[2] + delta[2]
        if (red >= 0 and red <= 1) and (green >= 0 and green <= 1) and (blue >= 0 and blue <= 1):
            self.color = [red, green, blue]
        virulence = self.virulence + delta[3]
        if virulence >= 0 and virulence <= 1:
            self.virulence = virulence
        duration = self.duration + random.randint(-5,5) #duration is 500 times higher than the other parameters
        if duration >= 0:
            self.duration = duration



