import argparse
import logging
import numpy as np

import model

#############################################################
def main():
    parser = argparse.ArgumentParser(description='Sensing model')
    parser.add_argument('-v', action='store_true', default=False)
    args = parser.parse_args()
    lvl = logging.DEBUG if args.v else logging.CRITICAL

    logging.basicConfig(level=lvl)
    log = logging.getLogger(__name__)

    searchmap = np.array([ 
        # 0, 1, 2, 3, 4, 5, 6, 7, 9, 0, 1, 2, 3, 4, 5, 6, 9, 0, 1, 2],
        [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #0
        [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #1
        [ 0, 0, 0,-1,-1,-1,-1,-1, 0,-1,-1,-1,-1,-1,-1, 0, 0,-1, 0, 0], #2
        [ 0, 0, 0,-1,-1,-1,-1,-1, 0,-1,-1,-1,-1,-1,-1, 0, 0,-1, 0, 0], #3
        [ 0, 0, 0,-1,-1,-1,-1,-1, 0,-1,-1,-1,-1,-1,-1, 0, 0,-1, 0, 0], #4
        [ 0, 0, 0,-1,-1,-1,-1,-1, 0,-1,-1,-1,-1,-1,-1, 0, 0,-1, 0, 0], #5
        [ 0, 0, 0,-1,-1,-1,-1,-1, 0,-1,-1,-1,-1,-1,-1, 0, 0,-1, 0, 0], #6
        [ 0, 0, 0,-1,-1,-1,-1,-1, 0,-1,-1,-1,-1,-1,-1, 0, 0,-1, 0, 0], #7
        [ 0, 0, 0,-1,-1,-1,-1,-1, 0,-1,-1,-1,-1,-1,-1, 0, 0,-1, 0, 0], #8
        [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #9
        [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]) #0

    #h, w = searchmap.shape
    mymodel = model.SensingModel(1, searchmap, log)

    for i in range(200):
        mymodel.step()
        input('')

#############################################################
if __name__ == '__main__':
    main()
