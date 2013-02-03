import numpy as np
from simple import grid


def build():
    f = open('_model\\'+grid.modelname+'.mpbas','w',0)
    f.write(' 1.0E+30  1.0E+20\n')
    f.write(' 1\nRECHARGE\n   6  DefaultIFACE\n')
    for k in range(grid.nlay):
        f.write(' 0')
    f.write('\n')
    for ibname in grid.ibound_names:
        f.write('OPEN/CLOSE  '+ibname+'  1 (FREE)\n')
    for k in range(grid.nlay):
        f.write('CONSTANT  0.3\n')
    f.close()

if __name__ == '__main__':
    build()

