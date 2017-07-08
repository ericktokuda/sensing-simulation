#!/usr/bin/python3

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from src.utils import *
import numpy as np
import random
import scipy

def test_get_symbol_positions():
    pos = [(0, 0), (1, 1), (1, 2), (2, 0)]
    mymap1 = np.full((3, 3), 0)
    mymap2 = np.copy(mymap1)
    for p in pos: mymap1[p] = -1
    mymap3 = mymap1 * 3

    assert(get_symbol_positions(mymap1) == set(pos))
    assert(get_symbol_positions(mymap2) == set())
    assert(get_symbol_positions(mymap3, -3) == set(pos))

def test_get_fullmatrix_difference():
    B = [(0, 0), (1, 1), (1, 2), (2, 0)]
    C = [(0, 1), (0, 2), (1, 0), (2, 1), (2, 2)]

    assert(get_fullmatrix_difference(3, 3, B) == set(C))
    assert(get_fullmatrix_difference(3, 3, []) == set(B+C))
    assert(get_fullmatrix_difference(0, 3, []) == set())

def test_get_manhattan_difference():
    p1 = ( 0, 0)
    p2 = ( 3, 2)
    p3 = (-2, 1)
    assert(get_manhattan_difference(p1, p2) == 5)
    assert(get_manhattan_difference(p1, p3) == 3)
    assert(get_manhattan_difference(p2, p3) == 6)
    assert(get_manhattan_difference(p2, p2) == 0)

def test_get_streets_from_image():
    tmpimage = '/tmp/tmp.png'
    streetpos = [(0, 0), (1, 1), (1, 2), (2, 0)]
    blackpx = 128

    mymap1 = np.random.randint(0, blackpx - 50, (3, 3))
    for p in streetpos: mymap1[p] = random.randint(blackpx + 50, 255)
    scipy.misc.imsave(tmpimage, mymap1)

    gndtruthmap = np.full((3, 3), -1)
    for p in streetpos: gndtruthmap[p] = 0

    streets = get_streets_from_image(tmpimage, blackpx)
    assert((streets == gndtruthmap).all())

    mymap2 = np.full((3, 3), 0)
    scipy.misc.imsave(tmpimage, mymap2)
    streets2 = get_streets_from_image(tmpimage, blackpx)
    assert((np.full((3, 3), -1) == streets2).all())

def test_find_crossings_crossshape():
    streetspos = [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)]
    mymap1 = np.full((3, 3), -1)
    for p in streetspos: mymap1[p] = 0
    crossings = find_crossings_crossshape(mymap1)
    assert(set([(1, 1)]) == crossings)

    mymap2 = np.full((3, 3), -1)
    crossings2 = find_crossings_crossshape(mymap2)
    assert(set() == crossings2)

def test_find_crossings_squareshape():
    streetspos = [(0, 1), (1, 0), (1, 1), (2, 0), (2, 1)]
    mymap1 = np.full((3, 3), -1)
    for p in streetspos: mymap1[p] = 0
    crossings = find_crossings_squareshape(mymap1)
    assert(set([(2, 1)]) == crossings)

    mymap2 = np.full((3, 3), 0)
    crossings2 = find_crossings_squareshape(mymap2, True)
    assert(1 == len(crossings2))

def main():
    test_get_symbol_positions()
    test_get_fullmatrix_difference()
    test_get_manhattan_difference()
    test_get_streets_from_image()
    test_find_crossings_crossshape()
    test_find_crossings_squareshape()

if __name__ == "__main__":
    main()

