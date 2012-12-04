import os,re
import numpy as np
import gslibUtil as gu
import arrayUtil as au

prefix = 'Q2'
nrow,ncol = 197,116
delc,delr = 2650.,2650.
offset = 668350.,288415.

#--load hard data
harddata_file = 'tbl_29.dat'
title,harddata_names,harddata = gu.loadGslibFile(harddata_file)

hard_xy = np.zeros((len(harddata),2),dtype='float')
hard_xy[:,0] = harddata[:,0].copy()
hard_xy[:,1] = harddata[:,1].copy()

#--load omni probs
omni_file = 'reals\\'+prefix+'_thkcdf_omni_probs.dat'
otitle,ovar_names,omni_array = gu.loadGslibFile(omni_file)

#-load aniso probs
aniso_file = 'reals\\'+prefix+'_thkcdf_aniso_probs.dat'
atitle,avar_names,aniso_array = gu.loadGslibFile(aniso_file)

assert len(ovar_names) == len(avar_names)

for var in range(0,len(ovar_names)):
    print ovar_names[var]
    thisO = omni_array[:,var].copy()
    print np.shape(thisO)
    thisO.resize(nrow,ncol)
    au.plotArray(np.flipud(thisO),delr,delc,offset=offset,gpts=hard_xy,title=prefix+'_omni_'+ovar_names[var],outputFlag='save')
    thisA = aniso_array[:,var].copy()
    thisA.resize(nrow,ncol)
    au.plotArray(np.flipud(thisA),delr,delc,offset=offset,gpts=hard_xy,title=prefix+'_aniso_'+ovar_names[var],outputFlag='save')
    diff = thisO - thisA
    print np.mean(diff),np.std(diff)
    au.plotArray(np.flipud(diff),delr,delc,offset=offset,gpts=hard_xy,title='diff_'+ovar_names[var],outputFlag='save')


