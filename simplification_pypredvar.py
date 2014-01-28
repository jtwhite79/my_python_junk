import copy
import numpy as np
from scipy import linalg
import mat_handler as mhand
import pst_handler as phand
import pypredvar as pvar

def main(in_filename,verbose=False):   
    #--load the parms from the infile
    f = open(in_filename,'r')
    pst_name = f.readline().strip()
    jco_name = pst_name.replace('.pst','.jco')
    ref_var = float(f.readline().strip())
    unc_filename = f.readline().strip()
    pv_list_file = f.readline().strip()
    sing_file = f.readline().strip()
    try:
        struct_file = f.readline().strip()
    except:
        struct_file = None
    f.close()

    
    #pv_list_file = 'biweekly\\biweekly_scaled.list'
    pv_dict = {}
    pvec = mhand.matrix()
    f = open(pv_list_file,'r')
    for line in f:
        if not line.startswith('#'):
            raw = line.strip().split()   
            print 'loading pred vector',raw[0] 
            pvec.from_ascii(raw[0])
            pv_dict[raw[1]] = copy.deepcopy(pvec.x)
    f.close()

    #sing_vals = np.loadtxt('singular_values.dat',dtype=np.int32)
    sing_vals = np.loadtxt(sing_file,dtype=np.int32)
    #sing_vals = [2]

    print 'loading pest control file',pst_name
    pst = phand.pst(pst_name)        

    print 'loading jco file',jco_name
    jco = mhand.matrix()
    jco.from_binary(jco_name)
        
    print 'dropping zero-weight obs from jco'
    drop_row_names = []
    nz_weights,nz_names = [],[]
    for name,weight in zip(pst.observation_data.obsnme,pst.observation_data.weight):
        if weight == 0.0:
            drop_row_names.append(name)
        else:
            nz_weights.append(weight)
            nz_names.append(name)
    jco.drop(drop_row_names)

    print 'building obs cov matrix'
    obs_unc = mhand.uncert(nz_names)
    obs_unc.from_uncfile('simple_obs.unc')    
    
    print 'inverting obs cov matrix = q'
    print 'and square root of q'
    #q = np.linalg.inv(obs_unc.x)
    #qhalf= linalg.sqrtm(q).real    

    u,s,vt = linalg.svd(obs_unc.x)    
    for i in range(u.shape[0]):
        u[:,i] *= s[i]**(-0.5)
    qhalf = np.dot(u,vt)
    
    print 'build q^(1/2)X'   
    qX = np.dot(qhalf,jco.x)
    if verbose:
        np.savetxt('qX_py.mat',qX,fmt='%15.6E')    
        np.savetxt('qhalf_py.mat',qhalf,fmt='%15.6E')
        np.savetxt('X_py.mat',jco.x,fmt='%15.6E')
             
    jco_struct = None
    spv_dict = None
    if struct_file:
        print 'loading structural parameter list'
        spar_names,idxs = [],[]
        #f = open('struct_pars.dat','r')
        f = open(struct_file,'r')
        for line in f:
            name = line.strip()
            if name in jco.col_names:
                spar_names.append(name)
                idxs.append(jco.col_names.index(name))
        f.close()

        print 'extracting omitted elements from q^(1/2)X'
        jco_struct_q = qX[:,idxs]
        jco_struct = jco.x[:,idxs]
        qX = np.delete(qX,idxs,1)                        
        X = np.delete(jco.x,idxs,1) 
        print 'forming omitted pred vectors'
        spv_dict = {}
        for out_name,pv in pv_dict.iteritems():
            spv = np.atleast_2d(pv[idxs])                 
            pv = np.atleast_2d(np.delete(pv,idxs)).transpose()
            pv_dict[out_name] = pv
            spv_dict[out_name] = spv

        if 'halfscaled' in in_filename:
            raise        
            print 'loading param uncert file for unscaled struct parameters'
            unc = mhand.uncert(spar_names)
            unc.from_uncfile('simple.unc')
            #unc_struct = unc.x[idxs:idxs]
            print unc_struct.shape
          
    par_cov = None
    struct_cov = None
    if 'scaled' not in pst_name:       
        print 'building par cov matrix'
        nspar_names = []
        for name in jco.col_names:
            if name not in spar_names:
                nspar_names.append(name)
        par_unc = mhand.uncert(nspar_names)
        par_unc.from_uncfile('simple.unc')        
        if verbose:
            np.savetxt('pycp.mat',par_unc.x,fmt='%15.6E')              
        print 'building structual par cov matrix'
        struct_unc = mhand.uncert(spar_names)
        struct_unc.from_uncfile('simple.unc')
        par_cov = par_unc.x
        struct_cov = struct_unc.x
    
    pv = pvar.predvar(qX,pv_dict,sing_vals,verbose=verbose,jco_struct=jco_struct_q,\
        pred_vectors_struct=spv_dict,struct_cov=struct_cov,par_cov=par_cov)
    #pv = pvar.predvar(X,pv_dict,sing_vals,verbose=verbose,jco_struct=jco_struct,\
    #    pred_vectors_struct=spv_dict,struct_cov=struct_cov,par_cov=par_cov,obs_cov=obs_unc.x)
    pv.calc()

if __name__ == '__main__':
    main('in_files\\predvar1b\\biweekly_cull_scaled.in')
