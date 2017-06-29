#!/usr/bin/python3
"""Sensing class

"""
import numpy as np

class Sensor:
    def __init__(self, _shape):
        self.count = np.full(_shape, 0)
        self.samplesz = np.full(_shape, 0)

if __name__ == "__main__":
    main()

