import sys
import pylab
import numpy as np

import MFBinaryClass as mfb
import arrayUtil as au 

import coarse_config
#--get dimensions
x_len = coarse_config.x_len
z_len = coarse_config.z_len
nrow = coarse_config.nrow 
ncol = coarse_config.ncol 
nlay = coarse_config.nlay 

delr = x_len/ncol
delc =1.0
delz = z_len/nlay

try:
    plt = [sys.argv[1]]
except:
    plt = ['h','c']

xsec_row = 0

cmap_heads = pylab.get_cmap('Spectral_r')
cmap_conc = cmap_heads
figsize = (4.67,2.57)
axes = []
if 'h' in plt:
    hds_obj = mfb.MODFLOW_Head(nlay,nrow,ncol,'henry_coarse.hds')
    while True:
        totim,kstp,kper,hd,success = hds_obj.next()
        print 'head',totim
        if success == False:
            break        
        fig = pylab.figure()       
        ax = pylab.subplot(111,aspect='equal')
        p = ax.pcolor(np.flipud(hd[:,xsec_row,:]),cmap=cmap_heads,vmin=hd.min(),vmax=hd.max())        
        ax.set_yticklabels([])
        ax.set_xticklabels([])        
        cax = pylab.colorbar(p,orientation='horizontal')
        cax.ax.set_title('heads '+str(totim))
        axes.append(ax)    
if 'c' in plt:
    conc_handle = mfb.MT3D_Concentration(nlay,nrow,ncol,'MT3D001.UCN')
    while True:
        totim_c,kstp_c,kper_c,c,success = conc_handle.next()    
        print 'conc',totim_c
        if success == False:
            break       
        fig = pylab.figure()       
        ax = pylab.subplot(111,aspect='equal')
        p = ax.pcolor(np.flipud(c[:,xsec_row,:]),cmap=cmap_conc,vmin=c.min(),vmax=c.max())      
        ax.set_yticklabels([])
        ax.set_xticklabels([])       
        cax = pylab.colorbar(p,orientation='horizontal')
        cax.ax.set_title('conc '+str(totim_c))
        axes.append(ax)              
    
pylab.show()