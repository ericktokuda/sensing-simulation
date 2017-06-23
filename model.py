import math
import matplotlib.pyplot as plt
import numpy as np
import random
import sys
import itertools

import person

#############################################################
class SensingModel():
    def __init__(self, npeople, ncars, searchmap, log):
        self.rng = random.SystemRandom()
        h, w = searchmap.shape
        self.maph = h
        self.mapw = w
        self.searchmap = searchmap
        self.lastid = -1
        self.people = []
        self.cars = []
        self.count = np.full(searchmap.shape, 0)
        self.obstacles = self.parse_obstacles(searchmap)
        self.place_agents(npeople, ncars)
        self.free = self.get_free(h, w, self.obstacles)

        #log.debug('Sensing model grid sizes w:{}, h:{}'. \
                 #format(self.grid.width, self.grid.height))

##########################################################
    def parse_obstacles(self, searchmap):
        origind = np.where(searchmap == -1)
        ind = map(tuple, np.transpose(origind))
        return set(ind)

    def get_free(self, h, w, obstacles):
        yy = list(range(h))
        xx = list(range(w))
        all = set(list(itertools.product(yy,xx)))
        return list(all.difference(obstacles))
        #return all.difference(obstacles)

    def get_random_pos(self):
        x = self.rng.randrange(0, self.mapw)
        y = self.rng.randrange(0, self.maph)
        return (y, x)

    def get_free_pos(self):
        nfree = len(self.free)
        rndidx = self.rng.randrange(0, nfree)
        return self.free[rndidx]

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
                #if self.count[y][x] == 0:
                if self.searchmap[y][x] == -1:
                    print('x ', end='')
                elif self.count[y][x] == 0:
                    print('_ ', end='')
                else:
                    print('o ', end='')
            print()

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
        for p in self.people:
            oldy, oldx = p.pos
            if not p.path:
                destiny = self.get_free_pos()
                p.destiny = destiny
                print('pos:{}, destiny:{}'.format(p.pos, destiny))
                p.create_path()
                #print('no path!')
            p.step()
            newy, newx = p.pos
            self.count[oldy][oldx] -= 1
            self.count[newy][newx] += 1

        self.print_map()


