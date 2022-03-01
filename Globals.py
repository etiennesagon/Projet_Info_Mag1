import sys
import PyQt5.QtWidgets as QtWidgets

app_s = QtWidgets.QApplication(sys.argv)
screen = app_s.primaryScreen()
height = screen.size().height()
width = screen.size().width() # monitor size

ctrl_size = (500,height-150) # panel control size

environmentSize = 850

nbHosts = 100
