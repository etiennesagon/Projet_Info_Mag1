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
    
    def add_host(self, c, h, inf, x, y, a):
        host = Host(c, h, inf, x, y, a)
        self.hosts.append(host)
        self.scene.addItem(host)

    def add_host_rnd(self):
        # random values of x, y, rotation, and velocity
        a = random.uniform(-self.extent, self.extent)
        b = random.uniform(-self.extent, self.extent)
        a2 = random.uniform(0, 360)
        color = QtGui.QColor.fromRgbF(random.random(),random.random(),random.random())
        health = random.random()
        infected = False
        self.add_host(color, health, infected, a, b, a2)

    def remove_host(self):
        last = self.hosts[-1]
        self.scene.removeItem(last)
        del self.hosts[-1]
    
    def __in_bounds(self, i, j):
        return 0 <= i < self.size and 0 <= j < self.size

    def step(self):
        for a in self.hosts:
            a.move()
            a.detection(self)
        self.stats_hosts['nb_infected'].append(sum([1 for a in self.hosts if a.infected==True]))
            # a.repro()
            # a.infection()