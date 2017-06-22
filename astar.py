#!/usr/bin/python3
""" A* implementation by tokudaek
"""

import sys
import heapq
import math
import numpy as np
import pprint

MAX = 9999999

##########################################################

class Astar:
    """Astar implementation
    Be careful because I invert the input to have first coordinate as horizontal axis
    (Thats why I need to invert the coordinates in some parts)
    """

    def __init__(self, heuristics, s, g):
        self.width, self.height = heuristics.shape
        sx, sy = s
        gx, gy = g
        self.closedset = set()
        self.openset = []
        self.start = (sy, sx)
        self.goal = (gy, gx)
        self.camefrom = {}
        self.h = heuristics
        self.g = np.full(heuristics.shape, MAX)
        self.g[sy][sx] = 0

    def get_neighbours(self, pos):
        neighbours = []

        def get_deltas_1d(x, lastpos):
            if x == 0:
                return [0, 1]
            elif x == lastpos:
                return [-1, 0]
            else:
                return [-1, 0, 1]

        dxs = get_deltas_1d(pos[0], self.width - 1)
        dys = get_deltas_1d(pos[1], self.height - 1)

        for dx in dxs:
            for dy in dys:
                if dx == 0 and dy == 0: continue
                node = (pos[0] + dx, pos[1] + dy)
                neighbours.append(node)
        return neighbours

    def recreate_path(self, current):
        cx, cy = current
        total_path = [(cy, cx)]
        v = current

        while v in self.camefrom.keys():
            v = self.camefrom[v]
            vx, vy = v
            total_path.append((vy, vx))

        return total_path

    def find_shortest_path(self):
        sx, sy = self.start
        #print(self.start)
        heapq.heappush(self.openset, (self.h[sx][sy], self.start))

        while self.openset:
            current = heapq.heappop(self.openset)[1]

            if current == self.goal:
                return self.recreate_path(current)

            self.closedset.add(current)

            for v in self.get_neighbours(current):
                vx, vy = v
                if v in self.closedset: continue

                nodes = [x[1] for x in self.openset]

                dist = self.g[current[0]][current[1]] + 1
                if dist >= self.g[vx][vy]:
                    if v not in nodes:
                        heapq.heappush(self.openset, (MAX, v))
                    continue

                self.camefrom[v] = current
                self.g[vx][vy] = dist

                neighcost = self.g[vx][vy] + self.h[vx][vy]

                if v not in nodes:
                    heapq.heappush(self.openset, (neighcost, v))
        return []
    
##########################################################
def compute_heuristics(searchmap, goal):
    s = searchmap

    gx, gy = goal
    height, width = s.shape

    h = np.empty(s.shape)

    for i in range(height):
        distx = math.fabs(i-gy)
        for j in range(width):
            if s[i][j] == 0:
                disty = math.fabs(j-gx)
                h[i][j] = distx + disty
            else:
                h[i][j] = MAX
    return h

##########################################################
def main():
    #start = (2, 0)
    #goal  = (8, 13)
    start = (0, 2)
    goal  = (13, 8)

    # x is vertical, y is horizontal
    searchmap = np.array([
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [1,1,1,1,1,1,1,1,1,1,1,1,0,1,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [1,1,1,1,1,1,1,1,1,1,1,1,0,1,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [1,1,1,1,1,1,1,1,1,1,1,1,0,1,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]])

    heuristics = compute_heuristics(searchmap, goal)
    pprint.pprint(heuristics)

    astar = Astar(heuristics, start, goal)
    final_path = astar.find_shortest_path()
    pprint.pprint(final_path)

if __name__ == "__main__":
    main()

