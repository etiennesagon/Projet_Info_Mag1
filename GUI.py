import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtGui as QtGui
from PyQt5.QtCore import Qt

import Globals
import Misc
import Physics
import Hosts

import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class ControlPanel(QtWidgets.QWidget):
    def __init__(self, q_timer, app, view, physics):
        super(ControlPanel, self).__init__()
        self.setWindowTitle("Control Panel")
        self.setFixedSize(Globals.ctrl_size[0], Globals.ctrl_size[1])
        # fix size

        self._q_timer = q_timer
        self._app = app
        self._view = view
        self._physics = physics

        self.btn_exit = QtWidgets.QPushButton(self)
        self.btn_exit.setText('Exit')
        self.btn_exit.setObjectName('exit')
        self.btn_exit.setStyleSheet("background-color: red")
        self.btn_exit.move(int(0.8*Globals.ctrl_size[0]),int(0.95*Globals.ctrl_size[1]))
        self.btn_exit.clicked.connect(self._app.exit)

        self.btn_start = QtWidgets.QPushButton(self)
        self.btn_start.setText('Start New Simulation')
        self.btn_start.setObjectName("start")
        self.btn_start.resize(200,100)
        self.btn_start.move(int(0.5*Globals.ctrl_size[0]-100),int(0.25*Globals.ctrl_size[1]))
        self.btn_start.clicked.connect(self.start_sim)

        self.btn_exp = QtWidgets.QPushButton(self)
        self.btn_exp.setText('Export Data')
        self.btn_exp.setStyleSheet("background-color: green")
        self.btn_exp.resize(200,100)
        self.btn_exp.move(int(0.5*Globals.ctrl_size[0]-100),int(0.45*Globals.ctrl_size[1]))
        self.btn_exp.clicked.connect(self.exp_data)

        self.btn_play = QtWidgets.QPushButton(self)
        self.btn_play.setText("Play")
        self.btn_play.move(int(0.5*Globals.ctrl_size[0]-75), int(0.38*Globals.ctrl_size[1]))
        self.btn_play.clicked.connect(self.play)

        self.btn_pause = QtWidgets.QPushButton(self)
        self.btn_pause.setText("Pause")
        self.btn_pause.move(int(0.5*Globals.ctrl_size[0]), int(0.38*Globals.ctrl_size[1]))
        self.btn_pause.clicked.connect(self.pause)

        self.btn_val = QtWidgets.QPushButton(self)
        self.btn_val.setText('Confirm')
        self.btn_val.move(int(0.75*Globals.ctrl_size[0]),70)
        self.btn_val.resize(100,50)
        self.btn_val.clicked.connect(self.change_values)

        self.btn_plot = QtWidgets.QPushButton(self)
        self.btn_plot.setText('Plot Data\n(export first)')
        self.btn_plot.resize(200,100)
        self.btn_plot.move(int(0.5*Globals.ctrl_size[0]-100),int(0.65*Globals.ctrl_size[1]))
        self.btn_plot.clicked.connect(self.plot_data)

        self.lbl_hosts = QtWidgets.QLabel(self, text="Number of Hosts (max 200): ")
        self.lbl_hosts.move(10, 30)
        self.nb_hosts = QtWidgets.QLineEdit(self)
        self.nb_hosts.setText(str(Globals.nbHosts))
        self.nb_hosts.move(int(0.40*Globals.ctrl_size[0]), 30)
        self.nb_hosts.resize(45,20)

        self.lbl_proba = QtWidgets.QLabel(self, text="Probability of reproduction\n(between 0 and 1): ")
        self.lbl_proba.move(10, 60)
        self.value_proba = QtWidgets.QLineEdit(self)
        self.value_proba.setText(str(Globals.proba_repro))
        self.value_proba.move(int(0.40*Globals.ctrl_size[0]), 75)
        self.value_proba.resize(45,20)

        self.lbl_viru = QtWidgets.QLabel(self, text="Virulence rate\n(between 0 and 1): ")
        self.lbl_viru.move(10, 90)
        self.value_viru = QtWidgets.QLineEdit(self)
        self.value_viru.setText(str(Globals.virulence))
        self.value_viru.move(int(0.40*Globals.ctrl_size[0]), 100)
        self.value_viru.resize(45,20)

        self.data = None

        with open('info_sim.txt', 'r') as f:
            nb_sim_txt = f.readlines()[0]

        self.nb_sim = int(nb_sim_txt.split('=')[1].strip())


    def pause(self):
        self._q_timer.stop()

    def play(self):
        self._q_timer.start(1000//25)

    def change_values(self):
        Globals.nbHosts = int(self.nb_hosts.text())
        Globals.proba_repro = float(self.value_proba.text())
        Globals.virulence = float(self.value_viru.text())

    def start_sim(self):
        self._physics.stats_hosts = {
            'nb_alive':[], 
            'nb_infected':[], 
            'nb_healthy':[] 
            }
        while len(self._physics.hosts) > 0: # clear all previous hosts before starting a new sim
            self._physics.remove_host()
        for ID in range(Globals.nbHosts):
            self._physics.add_host_rnd(ID)
        self._physics.make_host_sick(Globals.nb_infect)
        self.nb_sim += 1
        with open('info_sim.txt', 'w') as f:
            f.write(f'nb_sim = {self.nb_sim}')
        
        try:
            os.makedirs(f'Simulation_{self.nb_sim}') 
        except FileExistsError:
            pass
        with open(f'Simulation_{self.nb_sim}/Config_sim{self.nb_sim}.txt', 'w') as f:
            text = f'nbHosts = {int(self.nb_hosts.text())}\nproba_repro = {self.value_proba.text()}\nvirulence = {self.value_viru.text()}'
            f.write(text)

        self._q_timer.start(1000//25)
        self._view.show()
    
    def exp_data(self):
        self.data = pd.DataFrame.from_dict(self._physics.stats_hosts)
        self.data.to_csv(f'Simulation_{self.nb_sim}/Data_hosts_sim{self.nb_sim}.csv', index_label='time')

    def plot_data(self):
        if self.data is not None:
            plt.figure(figsize=(12,6))
            plt.plot(self.data.index, self.data['nb_alive'])
            plt.xlabel('Time')
            plt.ylabel('Number of hosts')
            plt.title('Evolution of the system')
            plt.show()
