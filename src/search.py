#!/usr/bin/env python
""" A* implementation by tokudaek
"""

import sys
import heapq
import math
import numpy as np
import pprint

import utils

##########################################################
def recreate_path(current, camefrom, skipstart=True):
    """Recreate A* path

    Args:
    current(2uple): current position, generally start position
    skiplast(bool): should include @current in the list

    Returns:
    list: positions ordered in the path

    """
    _path = [current]
    v = current

    while v in camefrom.keys():
        v = camefrom[v]
        _path.append(v)

    if skipstart: return _path[:-1]
    else: return _path

def get_astar_path(graph, start, goal):
    """Get A* path

    Args:
    graph(dict): keys are positions and values are lists of neighbours
    heuristics(dict): keys are positions and values are lists of neighbours
    s(tuple): starting position
    goal(tuple): goal position
    avoided(list): list of positions we do not want to discover

    Returns:
    list: list from end to beginning of the path
    """

    visitted = set()
    discovered = []
    camefrom = {}
    goalsset = goal if type(goal) == list else [goal]
    h = utils.compute_heuristics(graph, goal)
    g = dict.fromkeys(h.keys(), sys.maxsize)
    g[start] = 0

    heapq.heappush(discovered, (h[start], start))

    while discovered:
        current = heapq.heappop(discovered)[1]

        if current in goalsset:
            return recreate_path(current, camefrom)

        visitted.add(current)

        for cost, v in graph[current]:
            if v in visitted: continue

            nodes = [x[1] for x in discovered]

            dist = g[current] + cost

            if dist >= g[v]:
                if v not in nodes:
                    heapq.heappush(discovered, (sys.maxsize, v))
                continue

            camefrom[v] = current
            g[v] = dist

            neighcost = g[v] + h[v]

            if v not in nodes:
                heapq.heappush(discovered, (neighcost, v))
    return []

def get_dfs_path(graph, start, goal, avoided=[]):
    """Get DFS path

    Args:
    graph(dict): keys are positions and values are lists of neighbours
    s(tuple): starting position
    goal(tuple): goal position
    avoided(list): list of positions we do not want to discover

    Returns:
    list: list from end to beginning of the path
    """

    visitted = set()
    discovered = [start]
    goalsset = goal if type(goal) == list or type(goal) == set else [goal]
    camefrom = {}

    i = 0
    while discovered:
        current = discovered.pop()

        if current in goalsset:
            return recreate_path(current, camefrom)

        visitted.add(current)

        i += 1
        for cost, v in graph[current]:
            if v in visitted: continue
            if v in avoided: continue
            discovered.append(v)
            camefrom[v] = current

    return []

##########################################################
def main():
    start = (4, 10)
    goal  = (4, 22)
    image = 'maps/toy1.png'
    graph = utils.get_adjmatrix_from_image(image)
    #heuristics = utils.compute_heuristics(graph, goal)
    _path = get_astar_path(graph, start, goal)
    #_path = get_dfs_path(graph, start, goal)
    print(_path)

if __name__ == "__main__":
    main()

