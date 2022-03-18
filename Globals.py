import sys
import PyQt5.QtWidgets as QtWidgets

app_s = QtWidgets.QApplication(sys.argv)
screen = app_s.primaryScreen()
height = screen.size().height()
width = screen.size().width() # monitor size

hostsLength = 15

ctrl_size = (500,height-150) # panel control size

environmentSize = 850

nbHosts = 45
proba_repro = 0.3

MaxnbHosts = 150 

min_dist = 10

virulence = 0.3
nb_infect = 5