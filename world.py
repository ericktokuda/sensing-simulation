from mesa.space import MultiGrid

import itertools
import numpy as np
import random
import math



#def accept_tuple_argument(wrapped_function):
    #""" Decorator to allow grid methods that take a list of (x, y) position tuples
    #to also handle a single position, by automatically wrapping tuple in
    #single-item list rather than forcing user to do it.

    #"""
    #def wrapper(*args):
        #if isinstance(args[1], tuple) and len(args[1]) == 2:
            #return wrapped_function(args[0], [args[1]])
        #else:
            #return wrapped_function(*args)
    #return wrapper

class World(MultiGrid):
    pass
    #@staticmethod
    #def default_val():
        #""" Default value for new cell elements. """
        #return set()

    #def _place_agent(self, pos, agent):
        #""" Place the agent at the correct location. """
        #x, y = pos
        #self.grid[x][y].add(agent)
        #if pos in self.empties:
            #self.empties.remove(pos)

    #def _remove_agent(self, pos, agent):
        #""" Remove the agent from the given location. """
        #x, y = pos
        #self.grid[x][y].remove(agent)
        #if self.is_cell_empty(pos):
            #self.empties.append(pos)

    #@accept_tuple_argument
    #def iter_cell_list_contents(self, cell_list):
        #"""
        #Args:
            #cell_list: Array-like of (x, y) tuples, or single tuple.

        #Returns:
            #A iterator of the contents of the cells identified in cell_list

        #"""
        #return itertools.chain.from_iterable(
            #self[x][y] for x, y in cell_list if not self.is_cell_empty((x, y)))
