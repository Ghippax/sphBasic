# Import core modules
import h5py
import numpy as np
import matplotlib.pyplot as plt
import math

# Helping functions to print HDF5 file estructure
def h5printR(item, leading = ''):
    for key in item:
        if isinstance(item[key], h5py.Dataset):
            print(leading + key + ': ' + str(item[key].shape))
        else:
            print(leading + key)
            h5printR(item[key], leading + '  ')
        
def h5print(filename):
    h5printR(filename, '  ')

# Finds the closest value in a list to a given number, and returns position
from bisect import bisect_left
def take_closest(myList, myNumber):
    """
    Assumes myList is sorted. Returns closest value to myNumber.

    If two numbers are equally close, return the smallest number.
    """
    pos = bisect_left(myList, myNumber)
    if pos == 0:
        return 0
    if pos == len(myList):
        return len(myList)-1
    before = myList[pos - 1]
    after = myList[pos]
    if after - myNumber < myNumber - before:
        return pos
    else:
        return pos-1

# C4 Kernel 
def c4Kernel(q):
    if abs(q) > 1:
        return 0
    else:
        return 1365/(64*math.pi)*((1-q)**8 * (32*q**3 + 25*q**2 + 8*q + 1))

# Import snapshot for fields to be constructed
f = h5py.File("./out/snap_0.hdf5","r")

# Checking file structure if needed
h5print(f)

# Importing
x = np.array(f["sph"]["x"])
print(x)
