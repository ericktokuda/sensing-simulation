import astar
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
        #self.crossings = crossings
        if Car.count == []: self.initialize_count()
        if not Car.search:
            Car.search = Cachedsearch(searchmap, crossings)

    def initialize_count(self):
        mapshape = utils.get_mapshape_from_searchmap(self.searchmap)
        Car.count = np.full(mapshape, 0)
        print('mapshape:')
        print(mapshape)
        #print(Car.count.shape)
        Car.samplesz = np.full(mapshape, 0)

    def create_path(self):
        heuristics = utils.compute_heuristics(self.searchmap, self.destiny)
        #search = astar.Astar(heuristics, self.pos, self.destiny)
        #self.path = search.get_shortest_path()
        self.path = self.search.get_path(self.pos, self.destiny)
        if not self.path:
            print('Could not find path from {} to {}'. \
                     format(self.pos, self.destiny))

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

        return (newx, newy)

    def update_status(self):
        if self.pos == self.destiny:
            self.status = 'reached'
        else:
            self.status = 'going'

    def step(self):
        #print('car step')
        self.pos = self.path.pop()
        #self.sense_region()
