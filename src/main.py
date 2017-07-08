import argparse
import logging
import numpy as np
from numpy import genfromtxt
import pprint
import matplotlib.pyplot as plt
import threading
import os
import json

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
    parser.add_argument('config', nargs='?', default='config/simple.json', help='Config file in json format')
    return parser.parse_args()

#############################################################
def run_multiple_cars():
    """Run multiple numbers of cars
    """

    args = parse_arguments()
    with open(args.config, 'r') as jsonfh: config = json.load(jsonfh)

    nticks = config['nticks']
    nrepeats = config['nrepeats']
    npeople = config['npeople']
    ncars = config['ncars']
    outdir = config['outputdir']

    fmt = '%(asctime)s %(funcName)s: %(message)s'
    lvl = logging.DEBUG if args.verbose else logging.CRITICAL
    logging.basicConfig(level=lvl, format=fmt, datefmt='%I:%M:%S')
    log = logging.getLogger(__name__)
    log.debug('Start.')

    filename = config['map']
    log.debug('{} loaded.'.format(filename))
    if not os.path.exists(outdir): os.makedirs(outdir)

    crossings = utils.get_crossings_from_image(filename)
    searchmap = utils.get_adjmatrix_from_image(filename)
    h, w = utils.get_mapshape_from_searchmap(searchmap)

    threads = []
    _means = np.full((nticks, ncars - 1), 0.0)
    _stds = np.full((nticks, ncars - 1), 0.0)
    if args.view: myview = view.View(searchmap, log)

    for carsnum in range(1, ncars):
        err = np.full((nticks, nrepeats), 0.0)

        def one_run(npeople, nticks, carsnum, _iter, searchmap, log, outdir):
            mymodel = model.SensingModel(npeople, carsnum, searchmap, crossings, log)
            err = np.full((nticks), 0.0)

            _maxdens =  2*npeople / float(len(searchmap.keys()))
            for tick in range(nticks):
                log.debug('Cars: {}, Iter:{}, tick:{}'.format(carsnum, _iter, tick))
                mymodel.step(True)
                err[tick] = mymodel.denserror
                log.debug('dens error:{}'.format(mymodel.denserror))

                if args.view:
                    tdens, sdens = mymodel.get_densities()
                    myview.plot_densities(tdens, sdens, _maxdens, tick)

            np.save('{}/{}cars-{}iter.npy'.format(outdir, carsnum, _iter), err)
            return err

        for _iter in range(nrepeats):
            if args.mthread:
                threads.append(threading.Thread(target=one_run,
                                                args=(npeople,nticks,
                                                      carsnum, _iter,
                                                      searchmap, log,
                                                      outdir,)))
            else:
                vv = one_run(npeople, nticks, carsnum, _iter, searchmap, log, outdir)
                err[:, _iter] = vv


        if not args.mthread:
            _means[:, carsnum - 1] = np.mean(err, axis=1)
            _stds[:, carsnum - 1] = np.std(err, axis=1)

    for thread in threads: thread.start()

    if not args.mthread:
        np.save('{}/error-{}cars-{}ticks-{}agents.npy'. \
                format(outdir,ncars,nticks, npeople), _means)
        np.save('{}/error-variance-{}cars-{}ticks-{}agents.npy'. \
                format(outdir, ncars, nticks, npeople), _stds)
    log.debug('Finished.')

#############################################################
def main():
    run_multiple_cars()

if __name__ == '__main__':
    main()
