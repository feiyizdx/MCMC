import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import unittest
import random



#define a class that generates a 2D grid,size=m*, dx=dy=1, x, y start from 0
class init_grid(object):
    def __init__(self, m):
        self.nodes = m
    #generate grid
    def generate(self):
        self.nxx, self.nyy = (self.nodes, self.nodes)
        self.x = np.linspace(0, self.nodes-1, self.nxx)
        self.y = np.linspace(0, self.nodes-1, self.nyy)
        self.xv, self.yv = np.meshgrid(self.x, self.y)
    #used to define node/vertex index in a grid
    #pick up m points in the grid as nodes. e.g. #0 (0,0) #1 (1,2) #2 (1,3) #3 (3,2) #4 (4,4)
    #xrange denotes nodes' x index in the grid
    #yrange denotes nodes' y index in the grid
    def coord(self, xrange, yrange):
        self.xrange=xrange
        self.yrange=yrange