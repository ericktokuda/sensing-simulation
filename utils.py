import itertools
import math
import matplotlib.pyplot as plt
import numpy as np
import random
import time

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

