from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid

import math
import matplotlib.pyplot as plt
import numpy as np
import random
import sys

import person
import world

#############################################################
class SensingModel(Model):
    def __init__(self, N, _map, log):
        self.num_agents = N
        self.schedule = RandomActivation(self)  # Heuristics of order of steps
        self.rng = random.SystemRandom()
        height, width = _map.shape
        self.grid = MultiGrid(width, height, False)
        world.World(width, height, False)
        self.searchmap = _map
        log.debug('Sensing model grid sizes w:{}, h:{}'. \
                 format(self.grid.width, self.grid.height))

        for i in range(self.num_agents):
            pos = (0+i, 2+i)
            destiny = (13, 8)
            a = person.Person(i, self, pos, destiny)
            self.schedule.add(a)
            a.create_path()
            self.grid.place_agent(a, pos)

    def print_map(self):
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                if self.grid.is_cell_empty((x,y)):
                    print('_ ', end='')
                else:
                    print('o ', end='')
            print()

    def step(self):
        self.schedule.step()
        self.print_map()
