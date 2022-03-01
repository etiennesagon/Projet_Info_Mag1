import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtGui as QtGui
from PyQt5.QtCore import Qt

import Globals
import Misc
import Physics
import Hosts
import GUI

import random
#random.seed(34533)

app = QtWidgets.QApplication([])
physics = Physics.Physics()
view = Misc.AutoscaledGraphicsView(physics.scene)
q_timer = QtCore.QTimer()
"""q_timer = QtCore.QTimer()
q_timer.timeout.connect(physics.step)"""
view.resize(Globals.width-Globals.ctrl_size[0], Globals.ctrl_size[1])
view.move(Globals.ctrl_size[0], 0)

control_panel = GUI.ControlPanel(q_timer, app, view, physics)

if __name__ == '__main__':
    control_panel.show()
    app.exec()