from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid

import argparse
import astar
import logging
import math
import matplotlib.pyplot as plt
import numpy as np
import random
import sys


logging.basicConfig(level=logging.CRITICAL)
lg = logging.getLogger(__name__)

#############################################################
class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def dist(self, other, metric='euclidean'):
        if metric == 'euclidean':
            xpart = (math.pow(self.x-other.x, 2))
            ypart = (math.pow(sely.x-other.y, 2))
            return math.sqrt(xpart + ypart)
        elif metric == 'squared':
            xpart = (math.pow(self.x-other.x, 2))
            ypart = (math.pow(sely.x-other.y, 2))
            return xpart + ypart
        elif metric == 'manhattan':
            xpart = (math.abs(self.x-other.x))
            ypart = (math.abs(sely.x-other.y))
            return xpart + ypart
        else:
            return 0

    def equal(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False

#############################################################
class Person(Agent):
    """An agent with fixed initial wealth

    Attributes:

    Methods:
    step: what he is supposed to do
    """

    def __init__(self, uid, model, pos, destiny):
        super().__init__(uid, model)
        self.destiny = destiny
        self.pos = pos
        self.status = 'going'
        self.speed = 2
        self.path = []

    def create_path(self):
        heuristics = astar.compute_heuristics(self.model.searchmap, self.destiny)
        search = astar.Astar(heuristics, self.pos, self.destiny)
        self.path = search.find_shortest_path()
        if not self.path:
            lg.debug('Could not find path from {} to {}'. \
                     format(self.pos, self.destiny))

    def find_new_destiny(self):
        x = self.model.rng.randrange(0, self.model.grid.width)
        y = self.model.rng.randrange(0, self.model.grid.height)
        self.destiny = (x, y)

    def get_next_pos_naively(self):
        newx = self.pos[0]
        newy = self.pos[1]

        if self.destiny[0] > self.pos[0]:
            newx += 1
        elif self.destiny[0] < self.pos[0]:
            newx -= 1

        if self.destiny[1] > self.pos[1]:
            newy += 1
        elif self.destiny[1] < self.pos[1]:
            newy -= 1

        #return Point(newx, newy)
        return (newx, newy)

    def update_status(self):
        if self.pos[0] == self.destiny[0] and self.pos[1] == self.destiny[1]:
            self.status = 'reached'
        else:
            self.status = 'going'

    def step(self):
        newpos = self.path.pop()
        nx, ny = newpos
        self.model.grid.move_agent(self, newpos)
        self.update_status()

        if self.status == 'reached':
            self.find_new_destiny()
            self.create_path()
            self.update_status()
    
#############################################################
class Car(Agent):
    """An agent with fixed initial wealth

    Attributes:

    Methods:
    step: what he is supposed to do
    """

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.wealth = 1

    def step(self):
        if self.wealth == 0:
            return
        other_agent = random.SystemRandom.choice(self.model.schedule.agents)
        other_agent.wealth += 1
        self.wealth -= 1
    
#############################################################
class SensingModel(Model):
    """A model with some number of agents

    Attributes:

    Methods:
    step: what happens in the model in each step
    """

    def __init__(self, N, width, height, world):
        self.num_agents = N
        self.schedule = RandomActivation(self)  # Heuristics of order of steps
        self.rng = random.SystemRandom()
        self.grid = MultiGrid(width, height, False)
        self.searchmap = world
        lg.debug('Sensing model grid sizes w:{}, h:{}'. \
                 format(self.grid.width, self.grid.height))

        for i in range(self.num_agents):
            pos = (0+i, 2+i)
            destiny = (13, 8)
            a = Person(i, self, pos, destiny)
            self.schedule.add(a)
            a.create_path()
            self.grid.place_agent(a, pos)

    def print_map(self):
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                if self.grid.is_cell_empty((x,y)):
                    print('_ ', end='')
                else:
                    print('o ', end='')
            print()

    def step(self):
        self.schedule.step()
        self.print_map()

#############################################################
def main():
    parser = argparse.ArgumentParser(description='Sensing model')
    parser.add_argument('-v', action='store_true', default=False)
    args = parser.parse_args()
    if args.v: lg.setLevel(logging.DEBUG)

    searchmap = np.array([
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [1,1,1,1,1,1,1,1,1,1,1,1,0,1,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [1,1,1,1,1,1,1,1,1,1,1,1,0,1,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [1,1,1,1,1,1,1,1,1,1,1,1,0,1,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]])

    h, w = searchmap.shape
    mymodel = SensingModel(1, w, h, searchmap)

    for i in range(200):
        mymodel.step()
        input('')

if __name__ == '__main__':
    main()
