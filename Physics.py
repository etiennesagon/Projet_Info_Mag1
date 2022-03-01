# Copyright Killian Steunou
import Hosts

import math
import random
import numpy as np

import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtGui as QtGui

from PyQt5.QtCore import Qt
from typing import Tuple

import Globals

Point = Tuple[float, float]

def t(p: QtCore.QPointF) -> Point:
    return p.x(), p.y()

class Physics(QtWidgets.QGraphicsRectItem):
    size = Globals.environmentSize
    extent = size / 2
    bounds = QtCore.QRectF(-extent, -extent, size, size)

    def __init__(self):
        super().__init__(self.bounds)
        self.setZValue(-1)
        self.scene = QtWidgets.QGraphicsScene()
        self.scene.setItemIndexMethod(self.scene.NoIndex)
        self.hosts = []
    
    def add_host(self, x, y, a, v):
        boid = Host(x, y, a, v)
        self.hosts.append(boid)
        self.scene.addItem(boid)

    def add_host_rnd(self, r=Globals.boidsLength):
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
    
    def step(self):
        for a in self.boids:
            a.move()
            # a.detection()
            # a.repro()
            # a.infection()
