#!/usr/bin/python3
""" A* implementation by tokudaek
"""

import sys
import heapq
import math
import numpy as np
import pprint
import utils
import dfs

MAX = 9999999

##########################################################

class Astar:
    """Astar implementation by tokudaek
    """

    def __init__(self, graph, heuristics, s, g):
        #print(s)
        self.visitted = set()
        self.discovered = []
        self.start = s
        self.goal = g
        self.camefrom = {}
        self.h = heuristics
        self.g = dict.fromkeys(heuristics.keys(), MAX)
        self.g[s] = 0
        self.graph = graph

    def get_neighbours(self, pos):
        """Abstract method to find neighbourhood
    
        Args:
        pos(2uple): (y,x) position

        Returns:
        set: neighbours
        """
        return self.get_4conn_neighbours(pos)

    def get_4conn_neighbours(self, pos, yourself=False):
        """ Get diamond neighbours. Do _not_ take into account borders conditions

        Args:
        pos(2uple): (y,x) position
        yourself(bool): True if should include pos

        Returns:
        set: neighbours
        """

        neighbours = []
        y, x = pos
        neighbours.append((y, x-1), (y, x+1), (y-1, x), (y+1, x)) 
        if yourself: neighbours.append((y, x))
        return neighbours

    def recreate_path(self, current, skiplast=True):
        """Recreate A* path
    
        Args:
        current(2uple): current position, generally start position
        skiplast(bool): should include @current in the list
    
        Returns:
        list: positions ordered in the path
    
        """
        if skiplast:
            _path = []
        else:
            _path = [current]
        v = current

        while v in self.camefrom.keys():
            v = self.camefrom[v]
            _path.append(v)

        return _path[:-1]

    def get_path(self):
        """Compute A* path
    
        Returns:
        list: positions ordered in the path
        """
    
        heapq.heappush(self.discovered, (self.h[self.start], self.start))

        while self.discovered:
            current = heapq.heappop(self.discovered)[1]

            if current == self.goal:
                return self.recreate_path(current, False)

            self.visitted.add(current)

            for cost, v in self.graph[current]:
                if v in self.visitted: continue

                nodes = [x[1] for x in self.discovered]

                dist = self.g[current] + cost

                if dist >= self.g[v]:
                    if v not in nodes:
                        heapq.heappush(self.discovered, (MAX, v))
                    continue

                self.camefrom[v] = current
                self.g[v] = dist

                neighcost = self.g[v] + self.h[v]

                if v not in nodes:
                    heapq.heappush(self.discovered, (neighcost, v))
        return []
    
##########################################################
def get_n_reachable_crossings(graph, start, crossings, maxcrossings=2):
    ncrossings = []
    visitted = set()
    _crossings = crossings.copy()

    if start in _crossings: _crossings.discard(start)

    for i in range(maxcrossings):
        _dfs = dfs.Dfs(graph, start, _crossings, visitted)
        _path = _dfs.get_path()

        if not _path: break

        v = _path[0]
        cost = len(_path)
        #print(visitted)
        visitted.add(v)
        ncrossings.append((cost, v))
        _dfs.update_avoided(visitted)
        _crossings.discard(v)

    return ncrossings


##########################################################
def get_paths_from_all_crossings(graph, crossings):
    crossingneighbour = {}
    for crss in crossings:
        neighbours = get_n_reachable_crossings(graph, crss, crossings, 10)
        crossingneighbour[crss] = neighbours

    paths = {}
    crossingpaths = {}
    for crss1 in crossings: # Dummy way, I am recomputing many times
        crossingpaths[crss1] = {}
        for crss2 in crossings:
            if crss1 == crss2: continue
            heuristics = utils.compute_heuristics(graph, crss2)
            astar = Astar(graph, heuristics, crss1, crss2)
            finalpath = astar.get_path()
            crossingpaths[crss1][crss2] = finalpath

    return crossingpaths

##########################################################
def main_old():
    import time
    t0 = time.time()

    start = (4, 7)
    goal  = (13, 30)
    image = 'maps/toy3.png'

    graph = utils.get_adjmatrix_from_image(image)
    heuristics = utils.compute_heuristics(graph, goal)
    astar = Astar(graph, heuristics, start, goal)
    final_path = astar.get_path()
    print(final_path)

    print('Total time:{}'.format(time.time() - t0))


##########################################################
def main():
    import time
    t0 = time.time()

    #start = (4, 10)
    #goal  = (4, 20)
    #start = (4, 10)
    #goal  = (4, 18)
    start = (4, 10)
    goal  = (4, 11)
    image = 'maps/toy3.png'
    print(start)
    print(goal)

    crossings = utils.get_crossings_from_image(image)
    graph = utils.get_adjmatrix_from_image(image)
    crossingpaths = get_paths_from_all_crossings(graph, crossings)
    #pprint.pprint(crossingpaths)

    # find the path between start and end crossings
    startcrossings = get_n_reachable_crossings(graph, start, crossings)
    goalcrossings = get_n_reachable_crossings(graph, goal, crossings)
    #startcrossing = startcrossings[0]
    #goalcrossing = goalcrossings[0]
    sss = [ x[1] for x in startcrossings ]
    ggg = [ x[1] for x in startcrossings ]

    common = []
    for v in sss:
        if v in ggg: common.append(v)

    if len(common) == 0:
        # path from start to startcrossing
        heuristics = utils.compute_heuristics(graph, startcrossing[1])
        astar = Astar(graph, heuristics, start, startcrossing[1])
        final_path = astar.get_path()
        print(final_path)


        print(crossingpaths[startcrossing[1]][goalcrossing[1]])
        # path from endcrossing to end
        heuristics = utils.compute_heuristics(graph, goal)
        astar = Astar(graph, heuristics, goalcrossing[1], goal)
        final_path = astar.get_path()
        print(final_path)
    elif len(common) == 1:
        # path from start to startcrossing
        heuristics = utils.compute_heuristics(graph, common[0])
        astar = Astar(graph, heuristics, start, common[0])
        final_path = astar.get_path()
        print(final_path)

        # path from endcrossing to end
        heuristics = utils.compute_heuristics(graph, goal)
        astar = Astar(graph, heuristics, common[0], goal)
        final_path = astar.get_path()
        print(final_path)
    elif len(common) == 2:
        heuristics = utils.compute_heuristics(graph, goal)
        astar = Astar(graph, heuristics, start, goal)
        final_path = astar.get_path()
        print(final_path)
        



    print('Total time:{}'.format(time.time() - t0))
if __name__ == "__main__":
    main()

