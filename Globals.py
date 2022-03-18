import sys
import PyQt5.QtWidgets as QtWidgets

app_s = QtWidgets.QApplication(sys.argv)
screen = app_s.primaryScreen()
height = screen.size().height()
width = screen.size().width() # monitor size

hostsLength = 15

ctrl_size = (500,height-150) # panel control size

environmentSize = 600

nbHosts = 10
proba_repro = 0.5

MaxnbHosts = 150 

min_dist = 10

virulence = 0.1
nb_infect = 1