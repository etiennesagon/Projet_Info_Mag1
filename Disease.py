from PyQt5.QtGui import QColor

class Disease() :
    def __init__(self, color, virulence, duration, ID):
        self.color = color
        self.virulence = virulence
        self.duration = duration
        self.ID = ID
    
    def mutation(self):
        delta_list = [random.uniform(-0.01,0.01) for _ in range(5)]
        # mutations are random
        red = self.color.redF() + delta[0]
        green = self.color.greenF() + delta[1]
        blue = self.color.blueF() + delta[2]
        self.color = QColor.fromRgb(red, green, blue)
        self.virulence += delta[3]
        self.duration += delta[4]



