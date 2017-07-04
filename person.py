import utils
from cachedsearch import Cachedsearch
import search

#############################################################
class Person():
    search = []

    def __init__(self, _id, model, pos, destiny, searchmap, crossings):
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
        self.path = self.search.get_path(self.pos, self.destiny)
        if not self.path:
            print('Could not find path from {} to {}'. \
                     format(self.pos, self.destiny))

    def update_status(self):
        if self.pos[0] == self.destiny[0] and self.pos[1] == self.destiny[1]:
            self.status = 'reached'
        else:
            self.status = 'going'

    def step(self):
        self.pos = self.path.pop()
