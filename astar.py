#!/usr/bin/python3
"""A* implementation by tokudaek

"""

import sys
import heapq
import math

class Cost:
    def __init__(self, x, y, heuristic=0):
        self.pos = (x, y)
        self.cost =  sys.maxsize
        self.g =  sys.maxsize
        self.h = sys.maxsize

    def __lt__(self, other):
        return self.cost < other.cost

    def __gt__(self, other):
        return self.cost > other.cost

    def __eq__(self, other):
        return self.cost == other.cost

    def equalpos(self, other):
        return self.pos == other.pos

    def dist(self, other, metric='manhattan'):
        dx = self.pos[0] - other.pos[0]
        dy = self.pos[1] - other.pos[1]
        return math.fabs(dx) + math.fabs(dy)

class Grid:
    def __init__(self, width, height, goal):
        self.grid = []
        self.width = width
        self.height = height
        self.goal = goal
        for i in range(width):
            self.grid.append([])
            for j in range(height):
                node = Cost(i, j)
                node.h = node.dist(goal)
                self.grid[i].append(node)

    def get_neighbours(self, pos):
        neighbours = []

        if pos[0] == 0:
            dxs = [0, 1]
        elif pos[0] == self.width - 1:
            dxs = [-1, 0]
        else:
            dxs = [-1, 0, 1]

        if pos[1] == 0:
            dys = [0, 1]
        elif pos[1] == self.height - 1:
            dys = [-1, 0]
        else:
            dys = [-1, 0, 1]

        for dx in dxs:
            for dy in dys:
                if dx == 0 and dy == 0: continue
                node = (pos[0] + dx, pos[1] + dy)
                neighbours.append(node)
        return neighbours


class Astar:
    """Astar implementation
    Cost(v) = CostFromStartToV + EstimateCostFromVToGoal

    """

    def __init__(self, s, g):
        self.closedset = []
        self.openset = []
        self.startnode = Cost(s[0], s[1])
        self.startnode.g = 0
        self.goal = Cost(g[0], g[1])
        self.grid = Grid(2000, 2000, self.goal)
        self.camefrom = {}
        heapq.heappush(self.openset, self.startnode)

    def recreate_path(self):
        print('Got destination!')
        print('should recreate path')


    def find_shortest_path(self):
        ii = -1 

        while self.openset:
            ii += 1
            #current = heapq.nsmallest(1, self.openset)[0]
            current = heapq.heappop(self.openset)

            if current.equalpos(self.goal):
                self.recreate_path()
                return 1
            print('current:({},{})'.format(current.pos[0], current.pos[1]))

            heapq.heappush(self.closedset, current)

            for v in self.grid.get_neighbours(current.pos):
                nodes = [x.pos for x in self.closedset]
                if v in nodes: continue

                nodes = [x.pos for x in self.openset]

                if v not in nodes:
                    heapq.heappush(self.openset, self.grid.grid[v[0]][v[1]])
                    #heapself.openset

                dist = current.g + 1
                if dist >= self.grid.grid[v[0]][v[1]].g: continue

                self.camefrom[v] = current.pos
                self.grid.grid[v[0]][v[1]].g = dist

                self.grid.grid[v[0]][v[1]].cost = self.grid.grid[v[0]][v[1]].g + self.grid.grid[v[0]][v[1]].h
                print('closed len:{}, openlen: {}'.format(len(self.closedset),len(self.openset)))
        return 0

    
def main():
    astar = Astar((0, 0), (500, 1100))
    astar.find_shortest_path()

if __name__ == "__main__":
    main()

