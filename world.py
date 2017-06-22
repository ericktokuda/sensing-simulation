from mesa.space import MultiGrid

import itertools
import numpy as np
import random
import math

class World():
    def __init__(self, width, height, obstacles=set()):
        #super().__init__(width, height, False)
        self.width = width
        self.height = height
        self.people = set() # set of positions
        self.cars = set() 
        self.count = np.full((height, width), 0)
        self.obstacles = obstacles
        #self.obstacles = 

    def place_person(self, person, pos):
        x, y = pos
        self.people.add(person)
        person.pos = pos
        self.count[y][x] += 1

    def move_person(self, person, pos):
        oldx, oldy = person.pos
        self.place_person(person, pos)
        self.count[oldy][oldx] -= 1

    def place_car(self, car, pos):
        x, y = pos
        oldpos = car.pos
        oldx, oldy = oldpos
        self.cars.add(car)
        car.pos = pos
        self.count[oldy][oldx] -= 1
        self.count[y][x] += 1
