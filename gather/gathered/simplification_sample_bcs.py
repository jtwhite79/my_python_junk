import os
import numpy as np
import pandas
from simple import grid

def sample():
    ghb_locs = pandas.read_csv('..\\_misc\\ghb_locs.csv',index_col=0)
    wel_locs = pandas.read_csv('..\\_misc\\well_locs.csv',index_col=0)

    #--layer sampling

    layer_dfs = []
    coarse_k = 0
    for k in range(0,grid.nlay,grid.sample_stride):
        if k % grid.sample_stride == 0:
            df = ghb_locs[ghb_locs['layer'] == k+1]
            df['layer'] = coarse_k
            df['conductance'] *= grid.sample_stride
            coarse_k += 1
            layer_dfs.append(df)
    df = pandas.concat(layer_dfs)
    df.to_csv('..\\_misc\\ghb_locs_layer.csv')

    layer_dfs = []
    coarse_k = 0
    for k in range(0,grid.nlay,grid.sample_stride):
        if k % grid.sample_stride == 0:
            df = wel_locs[wel_locs['layer'] == k+1]
            df['layer'] = coarse_k
            df['flux'] *= grid.sample_stride
            coarse_k += 1
            layer_dfs.append(df)
    df = pandas.concat(layer_dfs)
    df.to_csv('..\\_misc\\well_locs_layer.csv')

    #--rc sampling

if __name__ == '__main__':
    sample()
