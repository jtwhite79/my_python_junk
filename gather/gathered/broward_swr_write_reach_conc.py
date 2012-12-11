import sys
import os
from datetime import datetime
import numpy as np
import shapefile
from bro import seawat
'''very simple for now, might need a timeseries of concs at some point
'''

#--load a list of RIV locs and concentrtaions
#--into a dict that is keyed in the row-col tuple
print 'loading swr reach - concentration info'
shapename = '..\\_gis\\scratch\\sw_reaches_conn_swrpolylines_2'
records = shapefile.load_as_dict(shapename,loadShapes=False)
fnames = shapefile.get_fieldnames(shapename)
#print fnames
swr_conc = []
#for r,c,strnum in zip(records['ROW'],records['COLUMN'],records['SRC_struct']):
for reach,row,col,strnum in zip(records['REACH'],records['ROW'],records['COLUMN'],records['SRC_struct']):
    #--tidal=brackish
    if strnum == -1:
        swr_conc.append([reach,row,col,seawat.brackish_conc])
    #--fresh
    else:
        swr_conc.append([reach,row,col,seawat.fresh_conc])
swr_conc = np.array(swr_conc)
np.savetxt('swr_conc.dat',swr_conc,fmt=' %d %d %d %15.6E')

#--check for reaches in the same cell with difference concentrations
for cnum,[i,j,conc] in enumerate(swr_conc[:,[1,2,3]]):

    for cnum2,[ii,jj,conc2] in enumerate(swr_conc[cnum+1:,[1,2,3]]):
        if ii == i and jj == j and conc != conc2:
            print i,j 

