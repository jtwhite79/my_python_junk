import sys
import os
import shutil
import numpy as np
import pylab
import MFBinaryClass as mfb


nrow,ncol,nlay = 411,501,6
delr,delc = 500,500
offset = [728600.0,577350.0,0.0]
results = 'results\\'

tol = 0.0001

for iter in range(100):

    
     
    hds_handle = mfb.MODFLOW_Head(nlay,nrow,ncol,results+'bro_6lay.hds')
    totim,kstp,kper,h,success = hds_handle.get_record()
    
    conc_handle = mfb.MT3D_Concentration(nlay,nrow,ncol,'MT3D001.UCN')
    totim_c,kstp_c,kper_c,c,success = conc_handle.get_record()
    
    #--get max concentration difference
    prev_c = np.zeros_like(c)
    for l in range(nlay):
        this_ref = 'ref\\initial_conc_layer'+str(l+1)+'.ref'
        shutil.copy(this_ref,this_ref+str(iter))
        this_lay_conc = np.loadtxt(this_ref)
        prev_c[l,:,:] = this_lay_conc
    
    max_diff = (np.abs(c-prev_c)).max()
    max_diff_idx = np.argmax(np.abs(c-prev_c))
    print 'iteration max_conc_diff,index_loc: ',iter+1,max_diff,max_diff_idx
    if max_diff <= tol:
        break            
    for l in range(nlay):
        np.savetxt('ref\\init_heads_'+str(l+1)+'.ref',h[l,:,:],fmt='%15.6e')
        np.savetxt('ref\\initial_conc_layer'+str(l+1)+'.ref',c[l,:,:],fmt='%15.6e')
        #au.plotArray(h[l,:,:],500,500,output=None,title='heads'+str(l+1))
        #au.plotArray(c[l,:,:],500,500,output=None,title='conc'+str(l+1)
    os.system('swt_v4x64.exe bro_6lay.nam_swt >nul')        
#pylab.show()