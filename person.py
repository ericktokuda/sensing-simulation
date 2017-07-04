import astar
import utils
from cachedsearch import Cachedsearch
import search

#############################################################
class Person():
    search = []

    def __init__(self, _id, model, pos, destiny, searchmap, crossings):
        #super().__init__(uid, model)
        self.id = _id
        self.destiny = destiny
        self.pos = pos
        self.status = 'going'
        self.speed = 1
        self.path = []
        self.searchmap = searchmap

        if not Person.search:
            Person.search = Cachedsearch(searchmap, crossings)

    def create_path(self):
        #heuristics = utils.compute_heuristics(self.searchmap, self.destiny)
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
        if self.pos[0] == self.destiny[0] and self.pos[1] == self.destiny[1]:
            self.status = 'reached'
        else:
            self.status = 'going'

    def step(self):
        #pass
        #print('person step')
        self.pos = self.path.pop()
        #nx, ny = newpos
        #self.model.move_person(self, newpos)
        #self.update_status()

        #if self.status == 'reached':
            #self.find_new_destiny()
            #self.create_path()
            #self.update_status()
