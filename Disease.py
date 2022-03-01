from PyQt5.QtGui import QColor

class Disease() :
    def __init__(self, color, virulence, duration):
        self.color = color
        self.virulence = virulence
        self.duration = duration

#test de maladie pour voir si ça marche
couleur1 = QColor.fromRgbF(0.5, 0.5, 0.5, 1)
maladie = Disease(couleur1, 1, 30)

