#!/usr/bin/env python3

import itertools
import math
import numpy as np
import random
import time
import scipy.misc
import scipy.signal

OBSTACLE = -1

def get_symbol_positions(searchmap, symbol=OBSTACLE):
    """Return the set of positions that has the symbol

    Args:
    searchmap(np.ndarray): navigation map

    Returns:
    set: set of positions with the symbol
    """
    t0 = time.time()
    origind = np.where(searchmap == symbol)
    ind = map(tuple, np.transpose(origind))
    return set(ind)

def get_fullmatrix_difference(Aheight, Awidth, B):
    """Return A-B, as a set of positions. *Free just means it doesnt
    contain obstacles.

    Args:
    h(int): height
    w(int): width
    obstables(list(list)): 

    Returns:
    set: set of positions with no obstacles
    """
    
    if Aheight * Awidth == 0: return set()
    t0 = time.time()
    yy = list(range(Aheight))
    xx = list(range(Awidth))
    all = set(list(itertools.product(yy, xx)))
    return all.difference(B)

def get_manhattan_difference(pos1, pos2):
    """Compute manhattan difference tween @pos1 and @pos2

    Args:
    pos1(tuple): position 1
    pos2(tuple): position 2

    Returns:
    float: manhattan difference
    """
    disty = math.fabs(pos1[0]-pos2[0])
    distx = math.fabs(pos1[1]-pos2[1])
    return distx + disty

def get_streets_from_image(imagefile, thresh=128):
    """Parse the streets from image and return a numpy ndarray,
    with 0 as streets and OBSTACLE as non-streets. Assumes a 
    BW image as input, with pixels in white representing streets.

    Args:
    imagefile(str): image path

    Returns:
    numpy.ndarray: structure of the image
    """
    img = scipy.misc.imread(imagefile)
    if img.ndim > 2: img = img[:, :, 0]
    return (img > thresh).astype(int) - 1

def find_crossings_crossshape(npmap):
    """Convolve with kernel considering input with
    0 as streets and OBSTACLE as non-streets. Assumes a 
    BW image as input, with pixels in black representing streets.

    Args:
    npmap(numpy.ndarray): ndarray with two dimensions composed of -1 (obstacles)
    and 0 (travesable paths)

    Returns:
    list: set of indices that contains the nodes
    """
    ker = np.array([[0,1,0], [1, 1, 1], [0, 1, 0]])
    convolved = scipy.signal.convolve2d(npmap, ker, mode='same',
                                        boundary='fill', fillvalue=OBSTACLE)
    inds = np.where(convolved >= OBSTACLE)
    return set([ (a,b) for a,b in zip(inds[0], inds[1]) ])

def find_crossings_squareshape(npmap, supressredundant=True):
    """Convolve with kernel considering input with
    0 as streets and -1 as non-streets. Assumes a 
    BW image as input, with pixels in black representing streets.

    Args:
    npmap(numpy.ndarray): ndarray with two dimensions composed of -1 (obstacles)
    and 0 (travesable paths)

    Returns:
    list: set of indices that contains the nodes
    """

    ker = np.array([[1,1], [1, 1]])
    convolved = scipy.signal.convolve2d(npmap, ker, mode='same',
                                        boundary='fill', fillvalue=OBSTACLE)
    inds = np.where(convolved >= 0)
    crossings = set([ (a,b) for a,b in zip(inds[0], inds[1]) ])
    if supressredundant: return filter_by_distance(crossings)
    else: return crossings

def filter_by_distance(points, mindist=5):
    """Evaluate the distance between each pair os points in @points 
    and return just the ones with distance gt @mindist

    Args:
    points(set of tuples): set of positions
    mindist(int): minimum distance

    Returns:
    set: set of points with a minimum distance between each other
    """
    cr = list(points)
    npoints = len(points)
    redundant = set()

    for i in range(npoints):
        if cr[i] in redundant: continue
        for j in range(i + 1, npoints):
            dist = get_manhattan_difference(cr[i], cr[j])
            if dist < mindist: redundant.add(cr[j])

    return points.difference(redundant)
    
def get_adjacency_dummy(nodes, npmap):
    return set([ (a,b) for a,b in zip(ind[0], ind[1]) ])

##########################################################
def compute_heuristics(adjmatrix, goal):
    """Compute heuristics based on the adjcency matrix provided and on the goal. If the guy is in the adjmatrix, then it is not an obstacle

    Args:
    adjmatrix(dict of list of neighbours): posiitons as keys and neighbours as values
    goal(tuple): goal position
    
    Returns:
    dict of heuristics: heuristic for each position
    """

    gy, gx = goal
    h = {}
    for j, i in adjmatrix.keys():
        distx = math.fabs(i - gx)
        disty = math.fabs(j - gy)
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
            if v == OBSTACLE:
                h[(j, i)] = MAX
            else:
                distx = math.fabs(j-gx)
                h[(j, i)] = distx + disty + v
    return h

##########################################################
def get_adjmatrix_from_npy(_map):
    """Easiest approach, considering 1 for each neighbour.
    """

    h, w = _map.shape
    adj = {}

    for j in range(0, h):
        for i in range(0, w):
            if _map[j][i] == OBSTACLE: continue
            adj[(j, i)] = set()
            ns = get_neighbours_coords(j, i, 8)
            ns = eliminate_nonvalid_coords(ns, h, w)

            for jj, ii in ns:
                if _map[jj][ii] != OBSTACLE:
                    adj[(j, i)].add((1, (jj, ii)))
    return adj

##########################################################
def get_neighbours_coords(j, i, connectedness=4, yourself=False):
    """ Get diamond neighbours. Do _not_ take whether it is a valid coordinate

    Args:
    j(int): y coordinate
    i(int): x coordinate
    connectedness(int): how consider the neighbourhood, 4 or 8
    yourself(bool): the point itself is included in the return
    """

    neighbours = [ (j, i-1), (j, i+1), (j-1, i), (j+1, i) ] 

    if connectedness != 4:
        neighbours += [ (j-1, i-1), (j-1, i+1), (j+1, i-1), (j+1, i+1) ] 

    if yourself: neighbours.append((j, i))

    return neighbours

##########################################################
def eliminate_nonvalid_coords(coords, h, w):
    """ Eliminate nonvalid indices

    Args:
    coords(set of tuples): input set of positions
    h(int): height
    w(int): width

    Returns:
    set of valid coordinates
    """

    valid = set()
    for j, i in coords:
        if j < 0 or j >= h: continue
        if i < 0 or i >= w: continue
        valid.add((j, i))

    return valid

##########################################################
def get_adjmatrix_from_image(image):
    """Get the adjacenty matrix from image

    Args:
    searchmap(np.ndarray): our structure of searchmap

    Returns:
    set of tuples: set of the crossing positions
    """

    searchmap = get_streets_from_image(image)
    return get_adjmatrix_from_npy(searchmap)

##########################################################
def get_crossings_from_image(imagefile):
    """Get crossings from image file

    Args:
    searchmap(np.ndarray): our structure of searchmap

    Returns:
    set of tuples: set of the crossing positions
    """

    searchmap = get_streets_from_image(imagefile)
    return find_crossings_squareshape(searchmap)

##########################################################
def get_mapshape_from_searchmap(hashtable):
    """Suppose keys have the form (x, y). We want max(x), max(y)
    such that not necessarily the key (max(x), max(y)) exists

    Args:
    hashtable(dict): key-value pairs

    Returns:
    int, int: max values for the keys
    """

    ks = hashtable.keys()
    h = max([y[0] for y in ks])
    w = max([x[1] for x in ks])
    return h+1, w+1
