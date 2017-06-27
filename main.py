import argparse
import logging
import numpy as np
from numpy import genfromtxt
import pprint

import model
import time
import view

#############################################################
ITERSNUM = 20000
AGENTSNUM = 30
CARSNUM = 3

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
    myview = view.View(searchmap, log)

    for i in range(ITERSNUM):
        mymodel.step()
        #tdens = mymodel.get_true_density()
        sdens = mymodel.get_sensed_density()
        #pprint.pprint(sdens)
        #myview.plot_ascii(sdens)
        myview.plot_matplotlib(sdens)
        input('')

#############################################################
if __name__ == '__main__':
    main()
