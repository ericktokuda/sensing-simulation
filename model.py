from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
import random
import matplotlib.pyplot as plt
import math

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

    def find_new_destiny(self):
        # Fixed
        if self.destiny and self.destiny[0] == 10:
            #self.destiny = Point(10, 10)
            self.destiny = (0, 0)
        else:
            self.destiny = (10, 10)

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

    #def move(self):
        #newpos = self.get_next_pos_naively()
        #self.pos = newpos
        #self.update_status()

    def step(self):
        #if not self.destiny: self.find_new_destiny()
        #self.grid
        newpos = self.get_next_pos_naively()
        self.model.grid.move_agent(self, newpos)
        self.update_status()

        if self.status == 'reached':
            self.find_new_destiny()
            self.update_status()
    
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
    
class SensingModel(Model):
    """A model with some number of agents

    Attributes:

    Methods:
    step: what happens in the model in each step
    """

    def __init__(self, N, width, height):
        self.num_agents = N
        self.schedule = RandomActivation(self)  # Heuristics of order of steps
        self.rng = random.SystemRandom()
        self.grid = MultiGrid(width, height, False)

        for i in range(self.num_agents):
            pos = (5+i, 5+i)
            destiny = (0, 0)
            a = Person(i, self, pos, destiny)
            self.schedule.add(a)
            pos = self.grid.find_empty()
            self.grid.place_agent(a, pos)

    def step(self):
        self.schedule.step()

        for x in range(self.grid.width):
            for y in range(self.grid.height):
                if self.grid.is_cell_empty((x,y)):
                    print('___ ', end='')
                else:
                    print('*** ', end='')
            print('\n')

if __name__ == '__main__':
    mymodel = SensingModel(10, 20, 20)
    for i in range(200):
        mymodel.step()
        input('')
