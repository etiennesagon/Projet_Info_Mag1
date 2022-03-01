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

        #test etienne !!!!
