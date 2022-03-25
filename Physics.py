# Copyright Killian Steunou
import math
import random
import numpy as np
import pandas as pd
from copy import copy

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

    def __init__(self):
        super().__init__(self.bounds)
        self.setZValue(-1)
        self.scene = QtWidgets.QGraphicsScene()
        self.scene.setItemIndexMethod(self.scene.NoIndex)
        self.hosts = []
        self.time = 0
        self.stats = {'nb_alive':[], 
                 'nb_infected':[], 
                 'nb_healthy':[],
                 'r_hosts':[],
                 'g_hosts':[],
                 'b_hosts':[],
                 'r':[], 
                 'g':[], 
                 'b':[], 
                 'v':[], 
                 'd':[]
                 }

        self.scene.addItem(self)
        al = .5 * Host.length
        self.scene.setSceneRect(Physics.bounds.adjusted(-al, -al, al, al))
        self.scene.setBackgroundBrush(QtGui.QColor(255,255,255))
    
    def add_host(self, c, h, inf, x, y, a, timer, ID, life_exp):
        host = Host(c, h, inf, x, y, a, timer, ID, life_exp)
        self.hosts.append(host)
        self.scene.addItem(host)

    def add_host_rnd(self, ID):
        # random values of x, y, rotation, and velocity
        a = random.uniform(-self.extent, self.extent)
        b = random.uniform(-self.extent, self.extent)
        a2 = random.uniform(0, 360)
        color = QtGui.QColor.fromRgbF(random.random(),random.random(),random.random())
        health = random.uniform(0.7, 1)
        infected = False
        life_exp = random.randint(1000, 1500)
        self.add_host(color, health, infected, a, b, a2, 0, ID, life_exp)

    def create_disease_rnd(self, ID):
        r = random.random()
        g = random.random()
        b = random.random()
        virulence = Globals.virulence
        duration = random.randint(100,500)
        return Disease([r,g,b], virulence, duration, ID)
    
    def make_host_sick(self, n):
        list_h = self.hosts.copy()
        for j in range(n):
            ID = random.choice(list_h).ID
            for i, guy in enumerate(self.hosts):
                    if guy.ID == ID:
                        d = self.create_disease_rnd(j)
                        self.hosts[i].infected = True
                        self.hosts[i].disease = copy(d)
                        self.hosts[i].time_before_recovery = copy(d.duration)
                        list_h.remove(self.hosts[i])

    def remove_host(self):
        last = self.hosts[-1]
        self.scene.removeItem(last)
        del self.hosts[-1]
    
    def __in_bounds(self, i, j):
        return 0 <= i < self.size and 0 <= j < self.size

    def step(self):
        self.time += 1
        baby_list =[]
        dead_list = []
        for a in self.hosts:
            if a.life_expectancy > 0:
                a.life_expectancy -= 1
            else:
                dead_list.append(a)
            # if infected: mutation, decrease recovery time
            if a.infected:
                a.disease.mutation()
                if a.time_before_recovery > 0:
                    a.affect_health()
                    a.time_before_recovery -= 1
                else:
                    a.infected = False
                    a.disease = None
            if a.health <= 0:
                dead_list.append(a)
            a.move()
            a.detection(self)
            a.infection(self)
            baby_list.append(a.reproduction(self))

            if a.timer > 0:
                a.timer -= 1

        for i in baby_list :
            if i is not None :
                self.add_host(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8])
            
        for host in dead_list:
            self.hosts.remove(host)
            self.scene.removeItem(host)

        
        # Update stats:
        self.stats['nb_infected'].append(sum([1 for a in self.hosts if a.infected==True]))
        self.stats['nb_alive'].append(len(self.hosts))
        self.stats['nb_healthy'].append(self.stats['nb_alive'][-1] - self.stats['nb_infected'][-1])

        self.stats['r_hosts'].append([h.color.redF() for h in self.hosts])
        self.stats['g_hosts'].append([h.color.greenF() for h in self.hosts])
        self.stats['b_hosts'].append([h.color.blueF() for h in self.hosts])

        self.stats['r'].append([h.disease.color[0] for h in self.hosts if h.infected==True])
        self.stats['g'].append([h.disease.color[1] for h in self.hosts if h.infected==True])
        self.stats['b'].append([h.disease.color[2] for h in self.hosts if h.infected==True])
        self.stats['v'].append([h.disease.virulence for h in self.hosts if h.infected==True])
        self.stats['d'].append([h.disease.duration for h in self.hosts if h.infected==True])
            
