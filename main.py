import argparse
import logging
import numpy as np
from numpy import genfromtxt

import model
import time

#############################################################
def main():

    NUMITER = 2000
    parser = argparse.ArgumentParser(description='Sensing model')
    parser.add_argument('-v', action='store_true', default=False)
    #parser.add_argument('map', default='')
    parser.add_argument('map', nargs='?', default='')
    args = parser.parse_args()
    lvl = logging.DEBUG if args.v else logging.CRITICAL
    logging.basicConfig(level=lvl)
    log = logging.getLogger(__name__)
    filename = args.map if args.map else 'maps/toy1.npy'
    t0 = time.time()
    searchmap = np.load(filename)
    log.debug('Loading {} took {}.'.format(filename, time.time() - t0))

    h, w = searchmap.shape
    mymodel = model.SensingModel(5, 1, searchmap, log)

    for i in range(NUMITER):
        mymodel.step()
        input('')

#############################################################
if __name__ == '__main__':
    main()
