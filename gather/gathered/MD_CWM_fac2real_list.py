import sys
import os
import numpy as np

'''writes K arrays from list file using pp factors
assumes a single zone for the whole model domain
and uses existing K arrays with multiplier parameters to form new K arrays
'''

def load_factors(filename):
    f = open(filename,'r')
    #--read the header info
    pp_filename = f.readline().strip()
    zone_filename = f.readline().strip()
    raw = f.readline().strip().split()
    nrow,ncol = int(raw[0]),int(raw[1])
    npp = int(f.readline().strip())
    pp_names = []
    for i in range(npp):
        pp_names.append(f.readline().strip())

    #--create a structure to store the factors in 
    factors = {}
    #for i in range(nrow):
    #    for j in range(ncol):
    #        cellnum = (i*ncol) + j
    #        factors[cellnum] = []
    
    #--now load the interpolation factors
    for line in f:
        raw = line.strip().split()
        idx = int(raw[0])-1
        numfac = int(raw[2])
        idxs,facs = [],[]
        for n in range(0,numfac*2,2):
            pt_idx = int(raw[4+n]) - 1 
            pt_fac = float(raw[4+n+1])
            idxs.append(pt_idx)
            facs.append(pt_fac)          
        factors[idx] = [np.array(idxs,dtype=np.dtype(np.int)),np.array(facs,dtype=np.dtype(np.float64))]        
    f.close()
    return pp_names,factors                


def fac2real_list():
    list_filename = 'par\\k_parameters.dat'
    factor_filename = 'fac\\pp_fac.dat'

    #--check for existence
    assert os.path.exists(list_filename),'list file not found: '+str(list_filename)
    assert os.path.exists(factor_filename),'factor file not found: '+str(factor_filename)


    #--load the factors file
    pp_names,factor_map = load_factors(factor_filename)
    pass

    #--load the parameter list file
    f = open(list_filename,'r')
    header1 = f.readline().strip().split()
    header2 = f.readline().strip().split()
    pt_data = np.loadtxt(f,usecols=[1,2,3])
    #usecols = []
    #for i,h in enumerate(header2):
    #    if h.upper() != 'NONE':
    #        usecols.append(i)
    #pt_data = np.loadtxt(f,usecols=usecols)
    model_dir = 'UMD.03\\ref\\'
    model_input_names = ['UMD_HK_L1.ref','UMD_HK_L2.ref','UMD_HK_L3.ref']
    base_names = ['ref\\UMD_HK_L1_base.ref','ref\\UMD_HK_L2_base.ref','ref\\UMD_HK_L3_base.ref']
    t = 1
    for params,base_name,input_name in zip(pt_data.transpose(),base_names,model_input_names):
        #--load the base K array
        base = np.loadtxt(base_name)
        nrow,ncol = base.shape
        #--interpolate points to multiplier array
        mult = np.zeros_like(base) - 1.0E+30
        for i in range(nrow):
            for j in range(ncol):
                cellnum = (i*ncol) + j
                idxs,facs = factor_map[cellnum]                        
                val = np.cumsum(params[idxs] * facs)[-1]
                mult[i,j] = val        
        mult *= base
        #np.savetxt(model_dir+'test'+str(t)+'.ref',mult,fmt=' %20.8E')                            
        np.savetxt(model_dir+input_name,mult,fmt=' %20.8E')                            
        t += 1    
    pass

if __name__ == '__main__':
    fac2real_list()