import argparse
import logging
import numpy as np
from numpy import genfromtxt
import pprint
import matplotlib.pyplot as plt
import threading

import model
import time
import view
import utils

#############################################################

def parse_arguments():
    parser = argparse.ArgumentParser(description='Sensing model')
    parser.add_argument('--verbose', action='store_true', default=False,
                        help='Verbose')
    parser.add_argument('--view', action='store_true', default=False,
                        help='Verbose')
    parser.add_argument('--mthread', action='store_true', default=False,
                        help='Verbose')
    parser.add_argument('map', nargs='?', default='', help='ndarray in .npy format')
    return parser.parse_args()

#############################################################
def run_multiple_cars():
    """Run multiple numbers of cars
    """

    TICKSNUM = 100
    TRIALS = 5
    AGENTSNUM = 3000
    CARSNUM = 10

    args = parse_arguments()
    fmt = '%(asctime)s %(funcName)s: %(message)s'
    lvl = logging.DEBUG if args.verbose else logging.CRITICAL
    logging.basicConfig(level=lvl, format=fmt, datefmt='%I:%M:%S')
    log = logging.getLogger(__name__)
    log.debug('Start.')
    filename = args.map if args.map else 'maps/toy3.png'
    #searchmap = np.load(filename)
    log.debug('{} loaded.'.format(filename))
    outdir = '/tmp/'

    crossings = utils.get_crossings_from_image(filename)
    #import pprint
    #pprint.pprint(crossings)
    searchmap = utils.get_adjmatrix_from_image(filename)
    #input()
    #ks = searchmap.keys()
    #import pprint
    #pprint.pprint(ks)
    #return
    ##h = 
    #h, w = searchmap.shape
    h, w = utils.get_mapshape_from_searchmap(searchmap)

    threads = []
    _means = np.full((TICKSNUM, CARSNUM - 1), 0.0)
    _stds = np.full((TICKSNUM, CARSNUM - 1), 0.0)
    if args.view: myview = view.View(searchmap, log)

    for carsnum in range(1, CARSNUM):
        err = np.full((TICKSNUM, TRIALS), 0.0)

        def one_run(AGENTSNUM, TICKSNUM, carsnum, _iter, searchmap, log, outdir):
            mymodel = model.SensingModel(AGENTSNUM, carsnum, searchmap, crossings, log)
            err = np.full((TICKSNUM), 0.0)

            for tick in range(TICKSNUM):
                mymodel.step(True)
                mymodel.update_density_error()
                err[tick] = mymodel.denserror

                if args.view:
                    tdens, sdens = mymodel.get_densities()
                    myview.plot_densities(tdens, sdens)

                np.save('{}/{}cars-{}iter.npy'.format(outdir, carsnum, _iter), err)
            return err

        for _iter in range(TRIALS):
            if args.mthread:
                threads.append(threading.Thread(target=one_run,
                                                args=(AGENTSNUM,TICKSNUM,
                                                      carsnum, _iter,
                                                      searchmap, log,
                                                      outdir,)))
            else:
                vv = one_run(AGENTSNUM, TICKSNUM, carsnum, _iter, searchmap, log, outdir)
                print('##########################################################')
                print('##########################################################')
                print('##########################################################')
                print('##########################################################')
                print(AGENTSNUM)
                print(carsnum)
                print(_iter)
                err[:, _iter] = vv


        if not args.mthread:
            _means[:, carsnum - 1] = np.mean(err, axis=1)
            _stds[:, carsnum - 1] = np.std(err, axis=1)

    for thread in threads: thread.start()

    if not args.mthread:
        np.save('{}/error-{}cars-{}ticks-{}agents.npy'. \
                format(outdir,CARSNUM,TICKSNUM, AGENTSNUM), _means)
        np.save('{}/error-variance-{}cars-{}ticks-{}agents.npy'. \
                format(outdir, CARSNUM, TICKSNUM, AGENTSNUM), _stds)
    log.debug('Finished.')

#############################################################
def run_once():
    ITERSNUM = 100
    AGENTSNUM = 30
    CARSNUM = 30

    #search = Cachedsearch(graph, crossings)
    #_path = search.get_path(start, goal)

    args = parse_arguments()
    fmt = '%(asctime)s %(funcName)s: %(message)s'
    lvl = logging.DEBUG if args.verbose else logging.CRITICAL
    logging.basicConfig(level=lvl, format=fmt)
    log = logging.getLogger(__name__)
    filename = args.map if args.map else 'maps/toy2.npy'
    t0 = time.time()

    crossings = utils.get_crossings_from_image(args.map)
    searchmap = utils.get_adjmatrix_from_image(args.map)

    #searchmap = np.load(filename)
    log.debug('Loading {} took {}.'.format(filename, time.time() - t0))

    h, w = searchmap.shape
    mymodel = model.SensingModel(AGENTSNUM, CARSNUM, searchmap, crossings, log)
    #myview = view.View(searchmap, log)

    for i in range(ITERSNUM):
        mymodel.step(True)
        mymodel.update_density_error()
        #print(mymodel.denserror)

#############################################################
def main():
    #run_once()
    run_multiple_cars()

if __name__ == '__main__':
    main()
