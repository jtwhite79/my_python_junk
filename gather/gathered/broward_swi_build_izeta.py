import numpy as np
import shapefile
import pylab
import bro



#--write isource arrays

#--find swr reaches that are tidal
shapename = '..\\..\\_gis\\scratch\\sw_reaches_conn_swrpolylines'
records = shapefile.load_as_dict(shapename,loadShapes=False)
fnames = shapefile.get_fieldnames(shapename)
#print fnames
trow,tcol = [],[]
for r,c,strnum in zip(records['ROW'],records['COLUMN'],records['SRC_struct_']):
    if strnum == -1:
        trow.append(r)
        tcol.append(c)

isource = np.zeros((bro.nrow,bro.ncol))
isource[np.where(bro.ibound==5)] = -2
isource[np.where(bro.ibound==2)] = -2
np.savetxt('ref\\isource_L2+.ref',isource,fmt=' %3.0f')
for r,c in zip(trow,tcol):
    isource[r-1,c-1] = -2
np.savetxt('ref\\isource_L1.ref',isource,fmt=' %3.0f')

#pylab.imshow(isource)
#pylab.show()


#--write the izeta arrays

#--load avg water levels - written by process_hds.py
#avg_wl = np.loadtxt('ref\\initial_avg_wl.ref')
#avg_wl = np.ma.masked_where(avg_wl==0,avg_wl)

#avg_sl = -1.5
#avg_wl -= avg_sl 

##--gyb-htz depths - 40.0 to salt, 35 to brackish
#gh_depth_mult = [40.0,35.0]

#odir = 'ref\\'
#for i,gd in enumerate(gh_depth_mult):
#    idepth = -1.0 * (avg_wl * gd)
#    idepth[np.where(idepth>-gd)] = -gd   
#    np.savetxt(odir+'izeta_'+str(i+1)+'.ref',idepth,fmt=' %15.6E')





