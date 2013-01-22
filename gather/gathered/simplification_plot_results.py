import numpy as np
import pylab

import MFBinaryClass as mfb
from simple import grid

def plot_array(pname,arr):
    fig = pylab.figure(figsize=(8,8))
    ax = pylab.subplot(111)
    vmax,vmin = 98.0,94.0
    p = ax.imshow(arr,extent=grid.plot_extent,vmax=vmax,vmin=vmin)
    #ax.contour(np.flipud(arr),20,colors='k',vmax=vmax,vmin=vmin)
    pylab.colorbar(p)
    pylab.savefig(pname,fmt='png',bbox_inches='tight')
    pylab.close(fig)
    return ax


def plot():

    hds_file = grid.modelname+'.hds'
    hds_obj = mfb.MODFLOW_Head(grid.nlay,grid.nrow,grid.ncol,hds_file)
    htimes = hds_obj.get_time_list()
    q_args = []
    plot_dir = 'png\\'

    for htime in htimes:
        htime = htime[-1]
        totim,kper,kstp,arr,success = hds_obj.get_array(htime)
        for k in range(grid.nlay):
        
            ibnd = np.loadtxt(grid.ibound_names[k])
            arr_lay = arr[k,:,:]
            arr_lay = np.ma.masked_where(ibnd==0,arr_lay)
            print k, arr_lay.min(),arr_lay.max()
            pname = plot_dir+'head_'+str(k+1)+'.png'
            plot_array(pname,arr_lay)
        
        break

    totim,kper,kstp,arr,success = hds_obj.get_array(htimes[-1][-1])
    for k in range(grid.nlay):
        np.savetxt('ref\\strt_'+str(k+1)+'.ref',arr[k,:,:],fmt=' %15.5E')

if __name__ == '__main__':
    plot()

