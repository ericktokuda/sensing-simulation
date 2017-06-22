from mesa import Agent

import astar

#############################################################
class Person(Agent):

    def __init__(self, uid, model, pos, destiny):
        super().__init__(uid, model)
        self.destiny = destiny
        self.pos = pos
        self.status = 'going'
        self.speed = 2
        self.path = []

    def create_path(self):
        heuristics = astar.compute_heuristics(self.model.searchmap, self.destiny)
        search = astar.Astar(heuristics, self.pos, self.destiny)
        self.path = search.find_shortest_path()
        if not self.path:
            lg.debug('Could not find path from {} to {}'. \
                     format(self.pos, self.destiny))

    def find_new_destiny(self):
        x = self.model.rng.randrange(0, self.model.grid.width)
        y = self.model.rng.randrange(0, self.model.grid.height)
        self.destiny = (x, y)

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

        #return Point(newx, newy)
        return (newx, newy)

    def update_status(self):
        if self.pos[0] == self.destiny[0] and self.pos[1] == self.destiny[1]:
            self.status = 'reached'
        else:
            self.status = 'going'

    def step(self):
        newpos = self.path.pop()
        nx, ny = newpos
        self.model.grid.move_agent(self, newpos)
        self.update_status()

        if self.status == 'reached':
            self.find_new_destiny()
            self.create_path()
            self.update_status()
