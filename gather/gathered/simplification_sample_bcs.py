import os
import sys
from datetime import datetime
import numpy as np
import pandas
from simple import grid

ghb_dtype = np.dtype([('layer','i4'),('row','i4'),('column','i4'),('stage','f4'),('conductance','f4')])
wel_dtype = np.dtype([('layer','i4'),('row','i4'),('column','i4'),('flux','f4'),('aux','a20')])

ghb_fmt = ' %9d %9d %9d %15.6G %15.6G'
wel_fmt = ' %9d %9d %9d %15.6G %20s'


def parse_ghb_line(line):
    raw = line.strip().split()
    l,r,c = int(raw[0]),int(raw[1]),int(raw[2])
    stage,cond = float(raw[3]),float(raw[4])
    return (l,r,c,stage,cond)

                              


def sample():
    ghb_locs = pandas.read_csv('_misc\\ghb_locs.csv',index_col=0)
    wel_locs = pandas.read_csv('_misc\\well_locs.csv',index_col=0)

      #--ghbs - layers
    mapped_entries = []
    #base_entries = []
    for idx,entry in ghb_locs.iterrows():
        #print entry[1]
        #entry['row'] = int(entry['row'] / grid.sample_stride)
        #entry['column'] = int(entry['column'] / grid.sample_stride)
        layer = np.ceil(entry['layer'] / grid.sample_stride)
        if layer == 0:
            layer = 1
        tup = (layer,entry['row'],entry['column'],entry['stage'],entry['conductance'])
        mapped_entries.append(tup)
        #tup = (entry['layer'],entry['row'],entry['column'],entry['stage'],entry['conductance'])
        #base_entries.append(tup)
    mapped_entries = np.array(mapped_entries)
    #base_entries = np.array(base_entries)
    unique_lrcs = []
    for l,r,c in zip(mapped_entries[:,0],mapped_entries[:,1],mapped_entries[:,2]):
        if (l,r,c) not in unique_lrcs:
            unique_lrcs.append((l,r,c))
    rows,cols,layers = [],[],[]
    stages,conds = [],[]
    for l,r,c in unique_lrcs:
        stage = mapped_entries[np.where(np.logical_and(np.logical_and(mapped_entries[:,0]==l,mapped_entries[:,1]==r),mapped_entries[:,2]==c)),3].mean()
        cond = mapped_entries[np.where(np.logical_and(np.logical_and(mapped_entries[:,0]==l,mapped_entries[:,1]==r),mapped_entries[:,2]==c)),4].sum() 
        idxs = np.argwhere(np.logical_and(np.logical_and(mapped_entries[:,0]==l,mapped_entries[:,1]==r),mapped_entries[:,2]==c))        
        layers.append(int(l))
        rows.append(int(r))
        cols.append(int(c))
        stages.append(stage)
        conds.append(cond)     
    df = pandas.DataFrame({'layer':layers,'row':rows,'column':cols,'stage':stages,'conductance':conds})
    df.to_csv('_misc\\ghb_locs_layer.csv')

    #--ghbs - rowcol
    mapped_entries = []
    for idx,entry in ghb_locs.iterrows():
        print entry[1]
        row = np.ceil(entry['row'] / grid.sample_stride)
        if row == 0: row = 1
        column = np.ceil(entry['column'] / grid.sample_stride)
        if column == 0: column = 1
            
        tup = (entry['layer'],row,column,entry['stage'],entry['conductance'])
        mapped_entries.append(tup)
    mapped_entries = np.array(mapped_entries)
    unique_lrcs = []
    for l,r,c in zip(mapped_entries[:,0],mapped_entries[:,1],mapped_entries[:,2]):
        if (l,r,c) not in unique_lrcs:
            unique_lrcs.append((l,r,c))
    rows,cols,layers = [],[],[]
    stages,conds = [],[]
    for l,r,c in unique_lrcs:
        stage = mapped_entries[np.where(np.logical_and(np.logical_and(mapped_entries[:,0]==l,mapped_entries[:,1]==r),mapped_entries[:,2]==c)),3].mean()
        cond = mapped_entries[np.where(np.logical_and(np.logical_and(mapped_entries[:,0]==l,mapped_entries[:,1]==r),mapped_entries[:,2]==c)),4].sum() 
        cond /= float(grid.sample_stride)
        layers.append(int(l))
        rows.append(int(r))
        cols.append(int(c))
        stages.append(stage)
        conds.append(cond)     
    df = pandas.DataFrame({'layer':layers,'row':rows,'column':cols,'stage':stages,'conductance':conds})
    df.to_csv('_misc\\ghb_locs_rc.csv')
    
   




    #--wells - rowcol
    wel_rc = wel_locs.copy()
    mapped_entries = []
    for idx,entry in wel_locs.iterrows():        
        row = int(entry['row'] / grid.sample_stride)
        if row == 0: row = 1
        column = int(entry['column'] / grid.sample_stride)
        if column == 0: column = 1
        wel_rc['row'][idx] = row
        wel_rc['column'][idx] = column
    wel_rc.to_csv('_misc\\well_locs_rc.csv')



    #--wells - layer
    wel_layer = wel_locs.copy()
    mapped_entries = []
    for idx,entry in wel_locs.iterrows():        
        layer = int(entry['layer'] / grid.sample_stride)
        if layer == 0:
            layer = 1
        wel_layer['layer'][idx] = layer
    wel_layer.to_csv('_misc\\well_locs_layer.csv')
    



   


    
    


if __name__ == '__main__':
    sample()
