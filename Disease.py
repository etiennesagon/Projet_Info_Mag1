from PyQt5.QtGui import QColor

class Disease() :
    def __init__(self, color, virulence, duration, ID):
        self.color = color
        self.virulence = virulence
        self.duration = duration
        self.ID = ID
    
    def mutation(self):
        delta = random.uniform(-0.01,0.01)
        # mutations are random
        red = self.color.redF()
        green = self.color.greenF()
        blue = self.color.blueF()

        self.color = QColor.fromRgbF(red + delta, green + delta, blue + delta)
        self.virulence += delta
        self.duration += delta

# next: 
#  add a property in class Host to contain the disease
#  create n diseases in Physics (n given by user) attached to n Hosts ? or random: 
#   create a function like add_hosts_rnd but to create n hosts infected


