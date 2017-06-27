import argparse
import logging
import numpy as np
from numpy import genfromtxt
import pprint

import model
import time
import view

#############################################################
ITERSNUM = 100
AGENTSNUM = 300
CARSNUM = 300

#############################################################
def main():
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
        tdens, sdens = mymodel.get_densities()
        #myview.plot_densities(tdens, sdens)
        print(mymodel.denserror)
        input('')

#############################################################
if __name__ == '__main__':
    main()
