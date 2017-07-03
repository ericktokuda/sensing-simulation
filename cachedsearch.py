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
from astar import Astar

MAX = 9999999

class Cachedsearch:
    """Caches crossings paths

    Attributes:
        attr(type):description

    Methods:
        method():description
    """

    def __init__(self, graph, waypoints):
        self.graph = graph
        self.waypoints = waypoints
        self.waypointspaths = self.get_paths_from_all_waypoints(graph, waypoints)
    
    def choose_waypoint(self, waypoints):
        return waypoints[0][1]

    def get_path(self, start, goal):
        if start == goal: return []

        startiscrossing = goaliscrossing = False
        if start in self.waypoints: startiscrossing = True
        if goal in self.waypoints: goaliscrossing = True

        if startiscrossing and goaliscrossing:
            return self.waypointspaths[start][goal]

        startcrossings = self.get_n_reachable_crossings(self.graph,
                                                        start, self.waypoints)
        goalcrossings = self.get_n_reachable_crossings(self.graph,
                                                       goal, self.waypoints)

        #print(startcrossings)
        if startiscrossing and not goaliscrossing:
            swayp = self.choose_waypoint(startcrossings)
            wayppath = self.waypointspaths[start][swayp]
            heuristics = utils.compute_heuristics(self.graph, swayp)
            astar = Astar(self.graph, heuristics, swayp, goal)
            finalpath = astar.get_path()
            return  finalpath + wayppath
        elif not startiscrossing and not goaliscrossing:
            swayps = [ s[1] for s in startcrossings ]
            gwayps = [ g[1] for g in goalcrossings ]
            #swayp = self.choose_waypoint(startcrossings)
            #gwayp = self.choose_waypoint(goalcrossings)
            common = []
            for aux in swayps:
                if aux in gwayps: common.append(aux)
            
            print(common)
            if len(common) == 0:
                swayp = self.choose_waypoint(startcrossings)
                gwayp = self.choose_waypoint(goalcrossings)

                print('check')
                heuristics = utils.compute_heuristics(self.graph, swayp)
                astar = Astar(self.graph, heuristics, start, swayp)
                startpath = astar.get_path()

                wayppath = self.waypointspaths[swayp][gwayp]

                heuristics = utils.compute_heuristics(self.graph, goal)
                astar = Astar(self.graph, heuristics, gwayp, goal)
                goalpath = astar.get_path()

                return  goalpath + wayppath + startpath
            else:
                heuristics = utils.compute_heuristics(self.graph, goal)
                astar = Astar(self.graph, heuristics, start, goal)
                goalpath = astar.get_path()
                return  goalpath
        elif startiscrossing and not goaliscrossing:
            gwayp = self.choose_waypoint(goalcrossings)
            wayppath = self.waypointspaths[start][gwayp]
            heuristics = utils.compute_heuristics(self.graph, goal)
            astar = Astar(self.graph, heuristics, gwayp, goal)
            finalpath = astar.get_path()
            return  finalpath + wayppath



        sss = [ x[1] for x in startcrossings ]
        ggg = [ x[1] for x in startcrossings ]

        common = []
        for c, v in startcrossings:
            if v in ggg: common.append(v)

        if len(common) == 0:
            # path from start to startcrossing
            heuristics = utils.compute_heuristics(self.graph, startcrossing[1])
            astar = Astar(self.graph, heuristics, start, startcrossing[1])
            final_path = astar.get_path()
            print(final_path)


            print(crossingpaths[startcrossing[1]][goalcrossing[1]])
            # path from endcrossing to end
            heuristics = utils.compute_heuristics(self.graph, goal)
            astar = Astar(self.graph, heuristics, goalcrossing[1], goal)
            final_path = astar.get_path()
            print(final_path)
        elif len(common) == 1:
            # path from start to startcrossing
            heuristics = utils.compute_heuristics(self.graph, common[0])
            astar = Astar(self.graph, heuristics, start, common[0])
            final_path = astar.get_path()
            print(final_path)

            # path from endcrossing to end
            heuristics = utils.compute_heuristics(self.graph, goal)
            astar = Astar(self.graph, heuristics, common[0], goal)
            final_path = astar.get_path()
            print(final_path)
        elif len(common) == 2:
            heuristics = utils.compute_heuristics(self.graph, goal)
            astar = Astar(self.graph, heuristics, start, goal)
            final_path = astar.get_path()
            print(final_path)
        
    
    ##########################################################
    def get_n_reachable_crossings(self, graph, start, crossings, maxcrossings=2):
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
            visitted.add(v)
            ncrossings.append((cost, v))
            _dfs.update_avoided(visitted)
            _crossings.discard(v)

        return ncrossings


    ##########################################################
    def get_paths_from_all_waypoints(self, graph, crossings):
        crossingneighbour = {}
        for crss in crossings:
            neighbours = self.get_n_reachable_crossings(graph, crss, crossings, 10)
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
def main():
    import time
    t0 = time.time()

    #start = (4, 10)
    #goal  = (7, 20)
    start = (4, 9)
    goal  = (7, 20)
    image = 'maps/toy3.png'
    print(start)
    print(goal)

    crossings = utils.get_crossings_from_image(image)
    graph = utils.get_adjmatrix_from_image(image)
    search = Cachedsearch(graph, crossings)
    _path = search.get_path(start, goal)
    pprint.pprint(_path)

    print('Total time:{}'.format(time.time() - t0))
if __name__ == "__main__":
    main()

