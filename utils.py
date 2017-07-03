import itertools
import math
import numpy as np
import random
import time
import scipy.misc
import scipy.signal

#class Utils
    #@staticmethod
def get_symbol_positions(searchmap, symbol=-1):
    t0 = time.time()
    origind = np.where(searchmap == symbol)
    ind = map(tuple, np.transpose(origind))
    return set(ind)

    #@staticmethod
def get_difference(Aheight, Awidth, B):
    """Return set of free positions. Free just means it doesnt
    contain obstacles.

    Args:
    h(int): height
    w(int): width
    obstables(list(list)): 

    Returns:
    list: set of positions with no obstacles
    """
    
    t0 = time.time()
    yy = list(range(Aheight))
    xx = list(range(Awidth))
    all = set(list(itertools.product(yy,xx)))
    return list(all.difference(B))

def parse_streets_from_image(imagefile):
    """Parse the streets from image and return a numpy ndarray,
    with 0 as streets and -1 as non-streets. Assumes a 
    BW image as input, with pixels in black representing streets.

    Args:
    imagefile(str): image path

    Returns:
    numpy.ndarray: structure of the image
    """
    img = scipy.misc.imread(imagefile)
    if img.ndim > 2: img = img[:, :, 0]
    return (img < 200).astype(int)  - 1

def find_crossings_dummy(npmap):
    """Convolve with kernel considering input with
    0 as streets and -1 as non-streets. Assumes a 
    BW image as input, with pixels in black representing streets.

    Args:
    npmap(numpy.ndarray): ndarray with two dimensions composed of -1 (obstacles)
    and 0 (travesable paths)

    Returns:
    list: set of indices that contains the nodes
    """
    ker = np.array([[0,1,0], [1, 1, 1], [0, 1, 0]])
    convolved = scipy.signal.convolve2d(npmap, ker, mode='same')
    inds = np.where(convolved >= -1)
    return set([ (a,b) for a,b in zip(inds[0], inds[1]) ])

def get_adjacency_dummy(nodes, npmap):
    #if nodes
    return set([ (a,b) for a,b in zip(ind[0], ind[1]) ])

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
def get_adjmatrix_from_npy(_map):
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
                    adj[(j, i)].add((1, (jj, ii)))
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
def get_adjmatrix_from_image(image):
    searchmap = parse_streets_from_image(image)
    #import pprint
    #pprint.pprint(searchmap)
    return get_adjmatrix_from_npy(searchmap)

##########################################################
def get_crossings_from_image(image):
    searchmap = parse_streets_from_image(image)
    return find_crossings_dummy(searchmap)

