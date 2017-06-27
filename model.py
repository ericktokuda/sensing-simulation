import math
import matplotlib.pyplot as plt
import numpy as np
import random
import sys
import itertools
import time

import person
import car
import utils

#############################################################
class SensingModel():
    def __init__(self, npeople, ncars, searchmap, log):
        self.rng = random.SystemRandom()
        plt.ion()
        h, w = searchmap.shape
        self.tick = 0
        self.carrange = 3
        self.log = log
        self.maph = h
        self.mapw = w
        self.searchmap = searchmap
        self.lastid = -1
        self.people = []
        self.cars = []
        self.count = np.full(searchmap.shape, 0)
        self.obstacles = utils.get_symbol_positions(searchmap, -1)
        self.free = utils.get_difference(h, w, self.obstacles)
        self.place_agents(npeople, ncars)
        self.denserror = -1

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

    def compute_true_density(self):
        if self.tick == 0: return np.full(self.searchmap.shape, -1)
        tdens = np.full(self.searchmap.shape, 0)

        for j in range(self.maph):
            for i in range(self.mapw):
                count = float(self.count[j][i])
                tdens[j][i] = count / float(self.tick)
        return tdens

    def update_true_density(self):
        self.tdens = self.compute_true_density()

    def compute_sensed_density(self):
        sdens = np.full(self.searchmap.shape, -1)

        for j in range(self.maph):
            for i in range(self.mapw):
                count = float(car.Car.count[j][i])
                s = car.Car.samplesz[j][i]

                if s != 0: sdens[j][i] = count / float(s)
        return sdens

    def update_sensed_density(self):
        self.sdens = self.compute_sensed_density()

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

    def place_car(self, car, pos):
        self.cars.append(car)
        car.pos = pos

    def move_car(self, car, pos):
        oldpos = car.pos
        self.place_car(car, pos)

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

    def get_densities(self):
        return self.tdens, self.sdens

    def update_car_sensing(self, nearby):
        peoplepos = [p.pos for p in self.people]
        for p in nearby:
            y, x = p
            car.Car.samplesz[y][x] += 1
            car.Car.count[y][x] += peoplepos.count(p)
        car.Car.clicks += 1

    def sense_region(self, _car):
        nearby = self.get_enclosing_square(_car)
        self.update_car_sensing(nearby)

    def get_people_map(self):
        tdens = np.full(self.searchmap.shape, 0)

        for p in self.people:
            y, x = p.pos
            tdens[y][x] += 1
        return tdens

    def compute_density_error(self):
        sdens = self.sdens
        tdens = self.tdens
        acc = 0
        error = 0

        for y in range(self.maph):
            for x in range(self.mapw):
                pos = (y,x)
                sensed = sdens[y][x]

                if sensed != -1:
                    true = tdens[y][x]
                    error += math.fabs(sensed - true)
                    acc += 1
        return error / float(acc)

    def update_density_error(self):
        self.denserror = self.compute_density_error()

    def step(self, update_densities=True): #TODO: Change the order in which agents are called
        for p in self.people:
            oldpos = p.pos

            if not p.path:
                destiny = self.get_free_pos(p.pos)
                p.destiny = destiny
                p.create_path()

            p.step()
            self.add_agents_count(p.pos, +1)

        for c in self.cars:
            oldpos = c.pos

            if not c.path:
                c.destiny = self.get_free_pos(c.pos)
                c.create_path()

            c.step()
            newy, newx = c.pos
            self.sense_region(c)
        self.tick += 1

        if update_densities:
            self.update_true_density()
            self.update_sensed_density()
            self.update_density_error()
