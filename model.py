import math
import matplotlib.pyplot as plt
import numpy as np
import random
import sys

import person

#############################################################
class SensingModel():
    def __init__(self, npeople, ncars, searchmap, log):
        #self.schedule = RandomActivation(self)  # Heuristics of order of steps
        self.rng = random.SystemRandom()
        h, w = searchmap.shape
        self.maph = h
        self.mapw = w
        self.searchmap = searchmap
        self.lastid = -1
        self.people = []
        self.cars = []
        self.count = np.full(searchmap.shape, 0)
        #self.obstacles = obstacles
        self.place_agents(npeople, ncars)

        #log.debug('Sensing model grid sizes w:{}, h:{}'. \
                 #format(self.grid.width, self.grid.height))

    def get_random_pos(self):
        x = self.rng.randrange(0, self.mapw)
        y = self.rng.randrange(0, self.maph)
        return (y, x)

    def place_people(self, npeople):
        for i in range(npeople):
            pos = (2+i, 0+i)
            destiny = (7, 17)
            self.lastid += 1
            a = person.Person(self.lastid, self, pos, destiny, self.searchmap)
            self.people.append(a)
            a.create_path()
            self.place_person(a, pos)

    def place_cars(self, ncars):
        pass

    def place_agents(self, npeople, ncars):
        self.place_people(npeople)
        self.place_cars(ncars)

    def print_map(self):
        for y in range(self.maph):
            for x in range(self.mapw):
                #if self.grid.is_cell_empty((x,y)):
                if self.count[y][x] == 0:
                    print('_ ', end='')
                else:
                    print('o ', end='')
            print()

        #if self.status == 'reached':
            #self.find_new_destiny()
            #self.create_path()
            #self.update_status()
        #self.print_map()

    def place_person(self, person, pos):
        y, x = pos
        self.people.append(person)
        person.pos = pos
        self.count[y][x] += 1

    def move_person(self, person, pos):
        oldy, oldx = person.pos
        self.place_person(person, pos)
        self.count[oldy][oldx] -= 1

    def place_car(self, car, pos):
        y, x = pos
        self.cars.add(car)
        cars.pos = pos
        self.count[y][x] += 1

    def move_car(self, car, pos):
        oldy, oldx = car.pos
        self.place_car(car, pos)
        self.count[oldy][oldx] -= 1

    def step(self): #TODO: Change the order in which agents are called
        #self.schedule.step()
        for p in self.people:
            oldy, oldx = p.pos
            if not p.path:
                destiny = self.get_random_pos()
                p.destiny = destiny
                p.create_path()

                #print('no path!')
            p.step()
            newy, newx = p.pos
            self.count[oldy][oldx] -= 1
            self.count[newy][newx] += 1

        self.print_map()


