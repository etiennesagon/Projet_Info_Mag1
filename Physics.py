# Copyright Killian Steunou
import math
import random
import numpy as np
import pandas as pd

import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtGui as QtGui

from PyQt5.QtCore import Qt
from typing import Tuple

import Globals
from Hosts import Host
from Disease import Disease

Point = Tuple[float, float]

def t(p: QtCore.QPointF) -> Point:
    return p.x(), p.y()

class Physics(QtWidgets.QGraphicsRectItem):
    size = Globals.environmentSize
    extent = size / 2
    bounds = QtCore.QRectF(-extent, -extent, size, size)
    var_stats_hosts = {'nb_alive':[], 
                 'nb_infected':[], 
                 'nb_healthy':[] 
                 }

    def __init__(self):
        super().__init__(self.bounds)
        self.setZValue(-1)
        self.scene = QtWidgets.QGraphicsScene()
        self.scene.setItemIndexMethod(self.scene.NoIndex)
        self.hosts = []
        self.stats_hosts = Physics.var_stats_hosts

        self.scene.addItem(self)
        al = .5 * Host.length
        self.scene.setSceneRect(Physics.bounds.adjusted(-al, -al, al, al))
        self.scene.setBackgroundBrush(QtGui.QColor(0,30,75))
    
    def add_host(self, c, h, inf, x, y, a, timer, ID):
        host = Host(c, h, inf, x, y, a, timer, ID)
        self.hosts.append(host)
        self.scene.addItem(host)

    def add_host_rnd(self, ID):
        # random values of x, y, rotation, and velocity
        a = random.uniform(-self.extent, self.extent)
        b = random.uniform(-self.extent, self.extent)
        a2 = random.uniform(0, 360)
        color = QtGui.QColor.fromRgbF(random.random(),random.random(),random.random())
        health = random.random()
        infected = False
        self.add_host(color, health, infected, a, b, a2, 0, ID)

    def create_disease_rnd(self, ID):
        r = random.uniform(0,1)
        g = random.uniform(0,1)
        b = random.uniform(0,1)
        virulence = Globals.virulence
        duration = random.randint(100,1000)
        return Disease(QtGui.QColor.fromRgbF(r,g,b), virulence, duration, ID)
    
    def make_host_sick(self, n):
        list_h = self.hosts.copy()
        for j in range(n):
            ID = random.choice(list_h).ID
            for i, guy in enumerate(self.hosts):
                    if guy.ID == ID:
                        d = self.create_disease_rnd(j)
                        self.hosts[i].infected = True
                        self.hosts[i].disease = d
                        self.hosts[i].time_before_recovery = d.duration
                        list_h.remove(self.hosts[i])

    def remove_host(self):
        last = self.hosts[-1]
        self.scene.removeItem(last)
        del self.hosts[-1]
    
    def __in_bounds(self, i, j):
        return 0 <= i < self.size and 0 <= j < self.size

    def step(self):
        baby_list =[]
        for a in self.hosts:
            # if infected: mutation, decrease recovery time
            if a.infected:
                a.disease.mutation()
                if a.time_before_recovery > 0:
                    a.time_before_recovery -= 1
                else:
                    a.infected = False
                    a.disease = None
            
            a.move()
            a.detection(self)
            a.infection(self)
            baby_list.append(a.reproduction(self))

            if a.timer > 0:
                a.timer -= 1

        

        for i in baby_list :
            if i is not None :
                self.add_host(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7])

        

        # Update stats:
        self.stats_hosts['nb_infected'].append(sum([1 for a in self.hosts if a.infected==True]))
        self.stats_hosts['nb_alive'].append(len(self.hosts))
        self.stats_hosts['nb_healthy'].append(self.stats_hosts['nb_alive'][-1] - self.stats_hosts['nb_infected'][-1])
            
