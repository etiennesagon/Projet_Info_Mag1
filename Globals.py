import sys
import PyQt5.QtWidgets as QtWidgets

app_s = QtWidgets.QApplication(sys.argv)
screen = app_s.primaryScreen()
height = screen.size().height()
width = screen.size().width() # monitor size

hostsLength = 15

ctrl_size = (500,height-150) # panel control size

environmentSize = 850

nbHosts = 15
proba_repro = 0.3

MaxnbHosts = 150 # the population cannot exceed 150% of the initial population !! too much !!

min_dist = 10
