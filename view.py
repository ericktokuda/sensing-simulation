import math
import matplotlib.pyplot as plt
import numpy as np
import utils


#############################################################
class View():
    def __init__(self, searchmap, log):
        plt.ion()
        h, w = searchmap.shape
        self.maph = h
        self.mapw = w
        self.obstacles = utils.get_symbol_positions(searchmap, -1)
        self.free = utils.get_difference(h, w, self.obstacles)

    def plot_ascii(self, densmap):
        for j in range(self.maph):
            for i in range(self.mapw):
                dens = densmap[j][i]
                if dens == -1:
                    print(' ', end='')
                else :
                    print(dens, end='')
            print()

    def plot_matplotlib(self, densmap):
        yy = []
        xx = []
        cc = []

        for j in range(self.maph):
            for i in range(self.mapw):
                dens = densmap[j][i]
                if dens == -1:
                    continue
                else :
                    yy.append(j)
                    xx.append(i)
                    cc.append(dens)
        plt.scatter(xx, yy, c=cc, cmap='hot', marker='s', s=25, vmin=0, vmax=2)
        plt.show()
