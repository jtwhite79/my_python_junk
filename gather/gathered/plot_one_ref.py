import os, sys
import subprocess as sp
import numpy as np
from os.path import normpath
import pylab
import arrayUtil as au





nrow, ncol, nlay = 411, 501, 1

top = np.loadtxt('ref\\top_filter_35_edge.ref')
au.plotArray(top,500,500)

