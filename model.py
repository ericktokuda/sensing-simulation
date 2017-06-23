import math
import matplotlib.pyplot as plt
import numpy as np
import random
import sys
import itertools
import time

import person
import car

#############################################################
class SensingModel():
    def __init__(self, npeople, ncars, searchmap, log):
        self.rng = random.SystemRandom()
        h, w = searchmap.shape
        self.carrange = 3
        self.log = log
        self.maph = h
        self.mapw = w
        self.searchmap = searchmap
        self.lastid = -1
        self.people = []
        self.cars = []
        self.count = np.full(searchmap.shape, 0)
        self.obstacles = self.parse_obstacles(searchmap, -1)
        self.free = self.get_free_list(h, w, self.obstacles)
        self.place_agents(npeople, ncars)

        #log.debug('Sensing model grid sizes w:{}, h:{}'. \
                 #format(self.grid.width, self.grid.height))

##########################################################
    def parse_obstacles(self, searchmap, symbol=-1):
        t0 = time.time()
        origind = np.where(searchmap == symbol)
        ind = map(tuple, np.transpose(origind))
        self.log.debug('Parse obstacles took {}.'.format(time.time() - t0))
        return set(ind)

    def get_free_list(self, h, w, obstacles):
        """Return set of free positions. Free just means it doesnt
        contain obstacles.
    
        Args:
        h(int): height
        w(int): width
        obstables(list(list)): 
    
        Returns:
        list: set of positions with no obstacles
        """
        
        t0 = time.time()
        yy = list(range(h))
        xx = list(range(w))
        all = set(list(itertools.product(yy,xx)))
        self.log.debug('Get free list took {}.'.format(time.time() - t0))
        return list(all.difference(obstacles))

    def get_free_pos(self, avoided=[]):
        nfree = len(self.free)
        while True:
            rndidx = self.rng.randrange(0, nfree)
            chosen = self.free[rndidx]
            if chosen != avoided: break
        return chosen

    def place_people(self, npeople):
        for i in range(npeople):
            pos = self.get_free_pos()
            destiny = self.get_free_pos(pos)
            self.lastid += 1
            a = person.Person(self.lastid, self, pos, destiny, self.searchmap)
            self.people.append(a)
            t0 = time.time()
            a.create_path()
            self.log.debug('Create_path of person {} took {}.'. \
                      format(self.lastid, time.time() - t0))
            self.place_person(a, pos)

    def place_cars(self, ncars, _range):
        for i in range(ncars):
            pos = self.get_free_pos()
            destiny = self.get_free_pos(pos)
            self.lastid += 1
            a = car.Car(self.lastid, self, pos, destiny,
                        self.searchmap, _range)
            self.cars.append(a)
            t0 = time.time()
            a.create_path()
            self.log.debug('Create_path of car {} took {}.'. \
                      format(self.lastid, time.time() - t0))
            self.place_car(a, pos)

    def place_agents(self, npeople, ncars):
        self.place_people(npeople)
        self.place_cars(ncars, self.carrange)

    def print_map(self):
        for y in range(self.maph):
            for x in range(self.mapw):
                pos = (y,x)
                if self.searchmap[y][x] == -1:
                    print('x', end='')
                elif pos in [c.pos for c in self.cars]:
                    print('⚀', end='')
                elif pos in [p.pos for p in self.people]:
                    print('☺', end='')
                else:
                    print(' ', end='')
            print()

    def print_sensed_density(self):
        for y in range(self.maph):
            for x in range(self.mapw):
                #pos = (y,x)
                #print(car.Car.count.shape)
                count = float(car.Car.count[y][x])
                s = car.Car.samplesz[y][x]
                if s == 0:
                    print(' ', end='')
                else :
                    print(count/s, end='')
            print()
    def add_agents_count(self, pos, delta=1):
        y, x = pos
        self.count[y][x] += delta

    def place_person(self, person, pos):
        self.people.append(person)
        person.pos = pos
        self.add_agents_count(pos, +1)

    def move_person(self, person, pos):
        oldpos = person.pos
        self.place_person(person, pos)
        self.add_agents_count(oldpos, -1)

    def place_car(self, car, pos):
        #y, x = pos
        self.cars.append(car)
        car.pos = pos
        self.add_agents_count(pos, +1)

    def move_car(self, car, pos):
        oldpos = car.pos
        self.place_car(car, pos)
        self.add_agents_count(oldpos, -1)

    def get_enclosing_square(self, _car):
        d = _car.range
        y0, x0 = _car.pos
        cells = set()

        t = y0 - d
        b = y0 + d
        l = x0 - d
        r = x0 + d
        if t < 0: t = 0 #trying to save somec omputations
        elif b > self.maph: b = self.maph
        if l < 0: l = 0
        elif r > self.mapw: r = self.mapw

        for y in range(t, b):
            for x in range(l, r):
                cells.add((y, x))
                #cells.append((y, x))
        return cells

    def update_car_sensing(self, nearby):
        peoplepos = set([p.pos for p in self.people])
        for p in nearby:
            y, x = p
            print(car.Car.samplesz.shape)
            car.Car.samplesz[y][x] += 1
            if p in peoplepos:
                car.Car.count[y][x] += 1
        car.Car.clicks += 1

    def sense_region(self, _car):
        nearby = self.get_enclosing_square(_car)
        self.update_car_sensing(nearby)

    def step(self): #TODO: Change the order in which agents are called
        for p in self.people:
            oldpos = p.pos
            if not p.path:
                destiny = self.get_free_pos(p.pos)
                p.destiny = destiny
                #print('pos:{}, destiny:{}'.format(p.pos, destiny))
                p.create_path()
            p.step()
            #newy, newx = p.pos
            self.add_agents_count(oldpos, -1)
            self.add_agents_count(p.pos, +1)

        for c in self.cars:
            oldpos = c.pos
            if not c.path:
                destiny = self.get_free_pos(c.pos)
                c.destiny = destiny
                #print('pos:{}, destiny:{}'.format(p.pos, destiny))
                c.create_path()
            c.step()
            newy, newx = c.pos
            self.add_agents_count(oldpos, -1)
            self.add_agents_count(c.pos, +1)
            self.sense_region(c)
        self.print_map()
        self.print_sensed_density()
        print('##########################################################')


