import sys
import PyQt5.QtWidgets as QtWidgets

app_s = QtWidgets.QApplication(sys.argv)
screen = app_s.primaryScreen()
height = screen.size().height()
width = screen.size().width() # monitor size

hostsLength = 15

ctrl_size = (500,height-150) # panel control size

environmentSize = 600

nbHosts = 40
proba_repro = 0.8

MaxnbHosts = 100 

min_dist = 10

virulence = 0.7
nb_infect = 6