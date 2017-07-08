import argparse
import logging
import numpy as np
from numpy import genfromtxt
import pprint
import matplotlib.pyplot as plt
import threading
import os
import json
from datetime import datetime

import model
import time
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
    parser.add_argument('config', nargs='?', default='config/simple.json',
                        help='Config file in json format')
    return parser.parse_args()

def setup_log(verbose):
    lvl = logging.DEBUG if verbose else logging.CRITICAL
    logging.basicConfig(level=lvl,
                        format= '%(asctime)s %(funcName)s: %(message)s',
                        datefmt='%I:%M:%S')
    log = logging.getLogger(__name__)
    return log

#############################################################
def run_one_experiment(npeople, nticks, fleetsz, sensorrad, sensorfreq, fleetspeed, 
                       repeatid, searchmap, crossings, log,
                       outdir, viewer=[]):

    mymodel = model.SensingModel(npeople, fleetsz, searchmap, crossings, log)
    err = np.full((nticks), 0.0)

    filenamesuffix = 'npeople{}_fleetsz{}_rad{}_freq{}_speed{}_repeat{}'. \
        format(npeople, fleetsz, sensorrad, sensorfreq, fleetspeed, repeatid)

    _maxdens =  2*npeople / float(len(searchmap.keys()))

    for tick in range(nticks):
        log.debug('{}-tick{}'.format(filenamesuffix, tick))
        mymodel.step(True)
        err[tick] = mymodel.denserror
        log.debug('dens error:{}'.format(mymodel.denserror))

        if viewer:
            tdens, sdens = mymodel.get_densities()
            viewer.plot_densities(tdens, sdens, _maxdens, tick)

    filename = os.path.join(outdir, filenamesuffix + '.npy')
    np.save(filename, err)

#############################################################
def main():

    args = parse_arguments()
    log = setup_log(args.verbose)
    with open(args.config, 'r') as jsonfh: config = json.load(jsonfh)

    nticks = config['nticks']
    nrepeats = config['nrepeats']
    minnpeople, maxnpeople = config['npeople']
    minfleetsz, maxfleetsz = config['fleetsize']
    minsensorrad, maxsensorrad = config['fleetsensorrange']
    minsensorfreq, maxsensorfreq = config['fleetsensorfreq']
    minfleetspd, maxfleetspd = config['fleetspeed']
    outdir = os.path.join(config['outputdir'], datetime.now().strftime('%Y%m%d-%H%M'))
    filename = config['map']

    if not os.path.exists(outdir): os.makedirs(outdir)

    crossings = utils.get_crossings_from_image(filename)
    searchmap = utils.get_adjmatrix_from_image(filename)
    h, w = utils.get_mapshape_from_searchmap(searchmap)
    log.debug(filename + ' loaded.')

    threads = []
    _means = np.full((nticks, maxfleetsz - minfleetsz + 1), 0.0)
    _stdds = np.full((nticks, maxfleetsz - minfleetsz + 1), 0.0)
    viewer = []

    if args.view:
        import view
        viewer = view.View(searchmap, log)

    for fleetsz in range(minfleetsz, maxfleetsz + 1):
        for npeople in range(minnpeople, maxnpeople + 1):
            for sensorrad in range(minsensorrad, maxsensorrad + 1):
                for sensorfreq in range(minsensorfreq, maxsensorfreq + 1):
                    for fleetspeed in range(minfleetspd, maxfleetspd + 1):
                        for _iter in range(nrepeats):
                            if args.mthread:
                                threads.append(threading.Thread(target=run_one_experiment,
                                                                args=(npeople, nticks, fleetsz,
                                                                      sensorrad, sensorfreq,
                                                                      fleetspeed, _iter,
                                                                      searchmap, crossings,
                                                                      log, outdir,viewer,)))
                            else:
                                run_one_experiment(npeople, nticks, fleetsz, sensorrad,
                                                   sensorfreq, fleetspeed, _iter, searchmap,
                                                   crossings, log, outdir, viewer)

    for thread in threads: thread.start()
    log.debug('Finished.')

#############################################################
if __name__ == '__main__':
    main()
