import astar
import numpy as np

#############################################################
class Car():
    count = []
    samplesz = []
    clicks = 0

    def __init__(self, _id, model, pos, destiny, searchmap, _range):
        self.id = _id
        self.destiny = destiny
        self.pos = pos
        self.status = 'going'
        self.speed = 4
        self.path = []
        self.searchmap = searchmap
        self.range = _range
        if Car.count == []: self.initialize_count()

    def initialize_count(self):
        Car.count = np.full(self.searchmap.shape, 0)
        Car.samplesz = np.full(self.searchmap.shape, 0)

    def create_path(self):
        heuristics = astar.compute_heuristics(self.searchmap, self.destiny)
        search = astar.Astar(heuristics, self.pos, self.destiny)
        self.path = search.get_shortest_path()
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

        #print('el:{}, first:{}, last:{}'.format(self.pos, nearby[0], nearby[-1]))
        

    def step(self):
        self.pos = self.path.pop()
        #self.sense_region()
