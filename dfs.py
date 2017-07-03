#!/usr/bin/python3
""" DFS implementation by tokudaek
"""

import sys
import heapq
import math
import numpy as np
import pprint

MAX = 9999999

##########################################################

class Dfs:
    """DFS implementation
    """

    def __init__(self, graph, s, g, avoided=[]):
        self.closedset = set()
        self.openset = []
        self.start = s
        self.goal = g
        self.camefrom = {}
        self.graph = graph
        self.avoided = avoided

    def update_avoided(self, avoided):
        self.avoided = avoided

    def get_neighbours(self, pos):
        return self.get_4conn_neighbours(pos)

    def get_4conn_neighbours(self, pos, yourself=False):
        """ Get diamong neighbours. Do _not_ take into account borders conditions
        """
        neighbours = []

        y, x = pos
        neighbours.append((y, x-1), (y, x+1), (y-1, x), (y+1, x)) 
        if yourself:
            neighbours.append((y, x))

        return neighbours

    def get_8conn_neighbours(self, pos):
        neighbours = []

        y, x = pos
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

    def recreate_path(self, current, skiplast=True):
        if skiplast:
            _path = []
        else:
            _path = [current]
        v = current

        while v in self.camefrom.keys():
            v = self.camefrom[v]
            _path.append(v)

        return _path

    def get_path(self):
        #print('start:{}'.format(self.start))
        #print('goal:{}'.format(self.goal))
        self.openset = [self.start]

        i = 0
        while self.openset:
            #print('iter ' + str(i))
            current = self.openset.pop()

            if current in self.goal:
                return self.recreate_path(current, False)

            self.closedset.add(current)

            i += 1
            #print(self.graph)
            for cost, v in self.graph[current]:
                if v in self.closedset: continue
                if v in self.avoided: continue
                self.openset.append(v)
                self.camefrom[v] = current

        return []
    
##########################################################
def compute_heuristics(adjmatrix, goal):
    '''If the guy is in the adjmatrix, then it is not an
    obstacle'''

    gy, gx = goal
    h = {}
    for j, i in adjmatrix.keys():
        distx = math.fabs(i-gx)
        disty = math.fabs(j-gy)
        h[(j, i)] = distx + disty
    return h

##########################################################
def compute_heuristics_from_map(searchmap, goal):
    s = searchmap

    gy, gx = goal
    height, width = s.shape

    h = {}

    for j in range(height):
        disty = math.fabs(j-gy)
        for i in range(width):
            v = s[j][i]
            if v == -1: # obstacle
                h[(j, i)] = MAX
            elif v == 0: # normal
                distx = math.fabs(i-gx)
                h[(j, i)] = distx + disty
            else: # more difficult place
                distx = math.fabs(j-gx)
                h[(j, i)] = distx + disty + v
    return h

##########################################################
def get_adjmatrix_from_map(_map):
    '''Easiest approach, considering 1 for each neighbour.'''
    h, w = _map.shape
    adj = {}

    for j in range(0, h):
        for i in range(0, w):
            if _map[j][i] == -1: continue
            adj[(j, i)] = set()
            ns = get_neighbours_coords(j, i)
            ns = eliminate_nonvalid_coords(ns, h, w)

            for jj, ii in ns:
                if _map[jj][ii] != -1:
                    adj[(j, i)].add((jj, ii))
    return adj

##########################################################
def get_neighbours_coords(j, i, yourself=False):
    """ Get diamond neighbours. Do _not_ take into account borders conditions
    """
    neighbours = [ (j, i-1), (j, i+1), (j-1, i), (j+1, i) ] 

    if yourself: neighbours.append((j, i))

    return neighbours

##########################################################
def eliminate_nonvalid_coords(ns, h, w):
    """ Eliminate nonvalid indices
    """
    neighbours = []
    for j, i in ns:
        if j < 0 or j >= h: continue
        if i < 0 or i >= w: continue
        neighbours.append((j, i))

    return neighbours
##########################################################
def main():
    #start = (0, 2)
    #goal  = (13, 9)

    searchmap1 = np.array([
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

    # With obstacles
    searchmap2 = np.array([ 
        # 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0],
        [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #0
        [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #1
        [ 0, 0, 0,-1,-1,-1,-1,-1, 0,-1,-1,-1,-1,-1,-1, 0, 0,-1, 0, 0], #2
        [ 0, 0, 0,-1,-1,-1,-1,-1, 0,-1,-1,-1,-1,-1,-1, 0, 0,-1, 0, 0], #3
        [ 0, 0, 0,-1,-1,-1,-1,-1, 0,-1,-1,-1,-1,-1,-1, 0, 0,-1, 0, 0], #4
        [ 0, 0, 0,-1,-1,-1,-1,-1, 0,-1,-1,-1,-1,-1,-1, 0, 0,-1, 0, 0], #5
        [ 0, 0, 0,-1,-1,-1,-1,-1, 0,-1,-1,-1,-1,-1,-1, 0, 0,-1, 0, 0], #6
        [ 0, 0, 0,-1,-1,-1,-1,-1, 0,-1,-1,-1,-1,-1,-1, 0, 0,-1, 0, 0], #7
        [ 0, 0, 0,-1,-1,-1,-1,-1, 0,-1,-1,-1,-1,-1,-1, 0, 0,-1, 0, 0], #8
        [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #9
        [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]) #0

    searchmap3 = np.array([
        # 0, 1, 2, 3, 4, 5, 6, 7, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0],
        [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #0
        [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #1
        [ 0, 0, 0,-1,-1,-1,-1,-1, 0,-1,-1,-1,-1,-1,-1, 0, 0,-1,-1,-1,-1,-1,-1, 0, 0,-1,-1,-1,-1,-1,-1, 0, 0,-1,-1,-1,-1,-1,-1, 0, 0,-1,-1,-1,-1,-1,-1, 0, 0,-1,-1,-1,-1,-1,-1, 0, 0,-1, 0, 0], #2
        [ 0, 0, 0,-1,-1,-1,-1,-1, 0,-1,-1,-1,-1,-1,-1, 0, 0,-1,-1,-1,-1,-1,-1, 0, 0,-1,-1,-1,-1,-1,-1, 0, 0,-1,-1,-1,-1,-1,-1, 0, 0,-1,-1,-1,-1,-1,-1, 0, 0,-1,-1,-1,-1,-1,-1, 0, 0,-1, 0, 0], #3
        [ 0, 0, 0,-1,-1,-1,-1,-1, 0,-1,-1,-1,-1,-1,-1, 0, 0,-1,-1,-1,-1,-1,-1, 0, 0,-1,-1,-1,-1,-1,-1, 0, 0,-1,-1,-1,-1,-1,-1, 0, 0,-1,-1,-1,-1,-1,-1, 0, 0,-1,-1,-1,-1,-1,-1, 0, 0,-1, 0, 0], #4
        [ 0, 0, 0,-1,-1,-1,-1,-1, 0,-1,-1,-1,-1,-1,-1, 0, 0,-1,-1,-1,-1,-1,-1, 0, 0,-1,-1,-1,-1,-1,-1, 0, 0,-1,-1,-1,-1,-1,-1, 0, 0,-1,-1,-1,-1,-1,-1, 0, 0,-1,-1,-1,-1,-1,-1, 0, 0,-1, 0, 0], #5
        [ 0, 0, 0,-1,-1,-1,-1,-1, 0,-1,-1,-1,-1,-1,-1, 0, 0,-1,-1,-1,-1,-1,-1, 0, 0,-1,-1,-1,-1,-1,-1, 0, 0,-1,-1,-1,-1,-1,-1, 0, 0,-1,-1,-1,-1,-1,-1, 0, 0,-1,-1,-1,-1,-1,-1, 0, 0,-1, 0, 0], #6
        [ 0, 0, 0,-1,-1,-1,-1,-1, 0,-1,-1,-1,-1,-1,-1, 0, 0,-1,-1,-1,-1,-1,-1, 0, 0,-1,-1,-1,-1,-1,-1, 0, 0,-1,-1,-1,-1,-1,-1, 0, 0,-1,-1,-1,-1,-1,-1, 0, 0,-1,-1,-1,-1,-1,-1, 0, 0,-1, 0, 0], #7
        [ 0, 0, 0,-1,-1,-1,-1,-1, 0,-1,-1,-1,-1,-1,-1, 0, 0,-1,-1,-1,-1,-1,-1, 0, 0,-1,-1,-1,-1,-1,-1, 0, 0,-1,-1,-1,-1,-1,-1, 0, 0,-1,-1,-1,-1,-1,-1, 0, 0,-1,-1,-1,-1,-1,-1, 0, 0,-1, 0, 0], #8
        [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #9
        [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]) #0

    #TODO: FIX BORDERS start = (2, 0)
    start = (2, 1)
    goal  = (6, 16)

    graph = get_adjmatrix_from_map(searchmap2)
    avoided = [(7,15)]
    dfs = Dfs(graph, start, goal, avoided)
    final_path = dfs.get_path()
    print(final_path)

if __name__ == "__main__":
    main()

