import sys
import os
import numpy as np
import arrayUtil as au
import pylab 


def prolongate(org,new):
    array = np.zeros_like(new)-1.0e+32
    
    nrow_org,ncol_org = org.shape
    nrow_new,ncol_new = new.shape
    
    row_fac = nrow_new/nrow_org
    col_fac = ncol_new/ncol_org
    
    for r in range(nrow_org):
        s_idx_r = r * row_fac
        e_idx_r = (r * row_fac) + row_fac
        for c in range(ncol_org):
            s_idx_c = c * col_fac
            e_idx_c = (c * col_fac) + col_fac
            array[s_idx_r:e_idx_r,s_idx_c:e_idx_c] = org[r,c]            
    return array

def make_map(org,new):        
    nrow_org,ncol_org = org.shape
    nrow_new,ncol_new = new.shape
    map_array = np.zeros((nrow_new,ncol_new))
    row_fac = nrow_new/nrow_org
    col_fac = ncol_new/ncol_org
    demon = (10**np.ceil(np.log10(ncol_org)))
    for r in range(nrow_org):
        s_idx_r = r * row_fac
        e_idx_r = (r * row_fac) + row_fac
        
        for c in range(ncol_org):
            s_idx_c = c * col_fac
            e_idx_c = (c * col_fac) + col_fac
           
            this_frac = (c+1) / demon
            #if c==0:
            #    print demon,this_frac
            this_map = float(r+1) + this_frac
            #print r,c,demon,this_frac,this_map
            map_array[s_idx_r:e_idx_r,s_idx_c:e_idx_c] = this_map
            
    return map_array
    

    
    
ibound_500 = np.loadtxt('ref_500\\ibound.ref')   


nrow_c,ncol_c = 411,501

nrow_f,ncol_f = 822,1002
new_array = np.zeros((nrow_f,ncol_f))
print ibound_500.shape
#map_array = make_map(ibound_500,new_array)
#np.savetxt('ref\\map_array.ref',map_array,fmt='%15.3f')
#sys.exit()
dir_500 = 'ref_500\\'
refs_500 = os.listdir(dir_500)

dir_250 = 'ref\\'
try:
    os.mkdir(dir_250)
except:
    pass

    
    
#for r in refs_500:
#    print r
#    this_500_ref = np.loadtxt(dir_500+r)
#    this_250_ref = prolongate(this_500_ref,new_array)
#    np.savetxt(dir_250+r,this_250_ref,fmt='%15.4e')
#    #break
     
ibound_500 = np.loadtxt('ref_500\\ibound.ref') 
ibound_500[np.where(ibound_500<0)] = 0           
ibound_250 = prolongate(ibound_500,new_array) 
print ibound_500.min(),ibound_500.max()
print ibound_250.min(),ibound_250.max()
np.savetxt(dir_250+'ibound.ref',ibound_250,fmt='%3.0f')


#au.plotArray(ibound_500,500,500,output=None)     
#au.plotArray(ibound_250,250,250,output=None)
#pylab.show()

    