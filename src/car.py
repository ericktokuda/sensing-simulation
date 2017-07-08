#!/usr/bin/env python3

import numpy as np

import utils
from cachedsearch import Cachedsearch

#############################################################
class Car():
    search = []
    count = []
    samplesz = []
    clicks = 0

    def __init__(self, _id, model, pos, destiny, searchmap, crossings, rangerad):
        self.id = _id
        self.destiny = destiny
        self.pos = pos
        self.status = 'going'
        self.speed = 4
        self.path = []
        self.searchmap = searchmap
        self.rangerad = rangerad
        if Car.count == []: self.initialize_count()
        if not Car.search:
            Car.search = Cachedsearch(searchmap, crossings)

    def initialize_count(self):
        mapshape = utils.get_mapshape_from_searchmap(self.searchmap)
        Car.count = np.full(mapshape, 0)
        Car.samplesz = np.full(mapshape, 0)

    def create_path(self):
        if self.destiny == self.pos: return []
        heuristics = utils.compute_heuristics(self.searchmap, self.destiny)
        self.path = self.search.get_path(self.pos, self.destiny)

        if not self.path:
            print('Could not find path from {} to {}'. \
                     format(self.pos, self.destiny))

    def update_status(self):
        if self.pos == self.destiny:
            self.status = 'reached'
        else:
            self.status = 'going'

    def get_cells_in_range(self, maph, mapw):
        y0, x0 = self.pos
        rad = self.rangerad
        cells = set()

        t = y0 - rad
        b = y0 + rad
        l = x0 - rad
        r = x0 + rad

        if t < 0: t = 0
        if b >= maph: b = maph - 1
        if l < 0: l = 0
        if r >= mapw: r = mapw - 1

        for y in range(t, b + 1):
            for x in range(l, r + 1):
                cells.add((y, x))
        return cells

    def step(self, freepos):
        if not self.path:
            self.destiny = freepos.pop()
            self.create_path()

        if self.path:
            self.pos = self.path.pop()

