import numpy as np

import utils
from cachedsearch import Cachedsearch

#############################################################
class Car():
    search = []
    count = []
    samplesz = []
    clicks = 0

    def __init__(self, _id, model, pos, destiny, searchmap, crossings, _range):
        self.id = _id
        self.destiny = destiny
        self.pos = pos
        self.status = 'going'
        self.speed = 4
        self.path = []
        self.searchmap = searchmap
        self.range = _range
        if Car.count == []: self.initialize_count()
        if not Car.search:
            Car.search = Cachedsearch(searchmap, crossings)

    def initialize_count(self):
        mapshape = utils.get_mapshape_from_searchmap(self.searchmap)
        Car.count = np.full(mapshape, 0)
        Car.samplesz = np.full(mapshape, 0)

    def create_path(self):
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

    def step(self):
        self.pos = self.path.pop()
