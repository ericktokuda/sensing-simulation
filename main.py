import argparse
import logging
import numpy as np
from numpy import genfromtxt
import pprint
import matplotlib.pyplot as plt

import model
import time
import view

#############################################################

#############################################################
def parse_arguments():
    parser = argparse.ArgumentParser(description='Sensing model')
    parser.add_argument('-v', action='store_true', default=False,
                        help='Verbose')
    parser.add_argument('map', nargs='?', default='', help='ndarray in .npy format')
    return parser.parse_args()

def run_multiple_cars():
    """Run multiple numbers of cars
    """

    TICKSNUM = 100
    TRIALS = 5
    AGENTSNUM = 30
    CARSNUM = 10

    args = parse_arguments()
    fmt = '%(funcName)s: %(message)s'
    lvl = logging.DEBUG if args.v else logging.CRITICAL
    logging.basicConfig(level=lvl, format=fmt)
    log = logging.getLogger(__name__)
    filename = args.map if args.map else 'maps/toy2.npy'
    t0 = time.time()
    searchmap = np.load(filename)
    log.debug('Loading {} took {}.'.format(filename, time.time() - t0))

    h, w = searchmap.shape

    _means = np.full((TICKSNUM, CARSNUM - 1), 0.0)
    _vars = np.full((TICKSNUM, CARSNUM - 1), 0.0)

    for carsnum in range(1, CARSNUM):
        err = np.full((TICKSNUM, TRIALS), 0.0)

        for _iter in range(TRIALS):
            mymodel = model.SensingModel(AGENTSNUM, carsnum, searchmap, log)
            if args.v: myview = view.View(searchmap, log)

            for tick in range(TICKSNUM):
                mymodel.step(True)
                mymodel.update_density_error()
                err[tick][_iter] = mymodel.denserror

                if args.v:
                    myview.plot_densities(tdens, sdens)
                    input('Type for next step')

        _means[:, carsnum - 1] = np.mean(err, axis=1)
        _vars[:, carsnum - 1] = np.var(err, axis=1)
        np.savetxt('{}.csv'.format(carsnum), err, delimiter=",")

    for carsnum in range(1, CARSNUM):
        plt.errorbar(range(TICKSNUM), _means[:, carsnum - 1],
                     _vars[:, carsnum - 1], label='{}cars'.format(carsnum))
    plt.show()
    np.save('error-{}cars-{}ticks-{}agents.npy'.format(CARSNUM, TICKSNUM, AGENTSNUM), _means)
    np.save('error-variance-{}cars-{}ticks-{}agents.npy'.format(CARSNUM, TICKSNUM, AGENTSNUM), _vars)
    plt.legend()
    input('Press any key to exit')

#############################################################
def run_once():
    ITERSNUM = 100
    AGENTSNUM = 30
    CARSNUM = 30

    parser = argparse.ArgumentParser(description='Sensing model')
    parser.add_argument('-v', action='store_true', default=False,
                        help='Verbose')
    parser.add_argument('map', nargs='?', default='', help='ndarray in .npy format')
    args = parser.parse_args()
    lvl = logging.DEBUG if args.v else logging.CRITICAL
    logging.basicConfig(level=lvl)
    log = logging.getLogger(__name__)
    filename = args.map if args.map else 'maps/toy2.npy'
    t0 = time.time()
    searchmap = np.load(filename)
    log.debug('Loading {} took {}.'.format(filename, time.time() - t0))

    h, w = searchmap.shape
    mymodel = model.SensingModel(AGENTSNUM, CARSNUM, searchmap, log)
    #myview = view.View(searchmap, log)

    for i in range(ITERSNUM):
        mymodel.step(True)
        mymodel.update_density_error()
        print(mymodel.denserror)

def main():
    run_once()
    #run_multiple_cars()

#############################################################
if __name__ == '__main__':
    main()
