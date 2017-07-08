#!/usr/bin/env python3

import math
import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import utils
import argparse
import mpld3
import mpld3.plugins


#############################################################
class View():
    def __init__(self, searchmap, log):
        #plt.ion()
        h, w = utils.get_mapshape_from_searchmap(searchmap)
        self.maph = h
        self.mapw = w
        self.f, self.axarr = plt.subplots(2, sharex=True)
        self.axarr[0].set_xlim(0, w)
        self.axarr[0].set_ylim(0, h)
        self.axarr[1].set_xlim(0, w)
        self.axarr[1].set_ylim(0, h)
        self.f.set_size_inches(10, 12)

        self.axarr[0].invert_yaxis()
        self.axarr[1].invert_yaxis()

    def plot_ascii(self, densmap):
        for j in range(self.maph):
            for i in range(self.mapw):
                dens = densmap[j][i]
                if dens == -1:
                    print(' ', end='')
                else :
                    print(dens, end='')
            print()

    def plot_matplotlib(self, densmap, subplot, _max, show=True):
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
        if subplot:
            subplot.scatter(xx, yy, c=cc, cmap='hot', marker='s', s=25, vmin=0, vmax=_max)
        else:
            plt.scatter(xx, yy, c=cc, cmap='hot', marker='s', s=25, vmin=0, vmax=0.5)

        if show: plt.show()

    def plot_densities(self, density1, density2, _max=10, keyword='out'):
        self.plot_matplotlib(density1, self.axarr[0], _max, False)
        self.plot_matplotlib(density2, self.axarr[1], _max, False)
        #self.plot_ascii(density1)
        #self.plot_ascii(density2)
        #self.f.show()
        plt.show()
        input()
        #plt.savefig('/tmp/{}.png'.format(str(keyword)))


#############################################################
def parse_arguments():
    parser = argparse.ArgumentParser(description='Sensing viewer')
    parser.add_argument('indir', help='input dir')
    parser.add_argument('maxcars', help='maximum number of cars')
    parser.add_argument('runs', help='number of runs')
    return parser.parse_args()

def main():
    parser = argparse.ArgumentParser(description='Sensing model')
    args = parse_arguments()

    indir = args.indir
    maxcars = int(args.maxcars)
    runs = int(args.runs)
    ntrials = 100

    fig, ax = plt.subplots(figsize=(12,8))
    ax.grid(True, alpha=0.3)

    for carsnum in range(1, maxcars +1):
        err = np.ndarray((ntrials, runs))
        for run in range(runs):
            err[:, run] = np.load('{}/{}cars-{}iter.npy'.format(indir, carsnum, run))

        _means = np.mean(err, axis=1)
        _stds = np.std(err, axis=1)
        ax.errorbar(range(_means.shape[0]), _means,
                     _stds, alpha=0.4, label='{}cars'.format(carsnum))
    ax.set_title('Error between real and sensed density')
    ax.set_xlabel('Ticks')
    ax.set_ylabel('Error')
    #ax.set_yscale("log", nonposy='clip')
    ax.legend()
    plt.show()

def old_main():
    parser = argparse.ArgumentParser(description='Sensing model')
    args = parse_arguments()

    _means = np.load(args.means)
    _stds = np.load(args.stds)

    fig, ax = plt.subplots(figsize=(12,8))
    ax.grid(True, alpha=0.3)
    for carsnum in range(_means.shape[1]):
        ax.errorbar(range(_means.shape[0]), _means[:, carsnum],
                     _stds[:, carsnum], alpha=0.6, label='{}cars'.format(carsnum+1))

    #handles, labels = ax.get_legend_handles_labels() # return lines and labels
    #interactive_legend = mpld3.plugins.InteractiveLegendPlugin(zip(handles, ax.collections),
                                                         #labels,
                                                         #alpha_unsel=0.5,
                                                         #alpha_over=1.5, 
                                                         #start_visible=True)
    #mpld3.plugins.connect(fig, interactive_legend)


    ax.set_title('Error between real and sensed density')
    ax.set_xlabel('Ticks')
    ax.set_ylabel('Error')
    #ax.set_yscale("log", nonposy='clip')
    ax.legend()
    plt.show()
    #mpld3.show()

if __name__ == '__main__':
    main()
