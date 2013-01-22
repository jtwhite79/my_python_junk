import os
import shutil
import numpy as np
import pandas
from simple import grid


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
    
    factors = {}       
    #--now load the interpolation factors
    for line in f:
        raw = line.strip().split()
        idx = int(raw[0])-1
        i,j = node2ij(idx,(nrow,ncol))        
        numfac = int(raw[2])
        idxs,facs = [],[]
        for n in range(0,numfac*2,2):
            pt_idx = int(raw[4+n]) - 1 
            pt_fac = float(raw[4+n+1])
            idxs.append(pt_idx)
            facs.append(pt_fac)          
        factors[(i,j)] = [np.array(idxs,dtype=np.dtype(np.int)),np.array(facs,dtype=np.dtype(np.float64))]            
    f.close()
    return pp_names,factors                

def node2ij(node,shape):
    i = int(node / shape[1])
    if (i * shape[1]) < node:
        i += 1
    j = node - ((i-1) * shape[1])    
    return i-1,j-1


#def fac_2_real(shape,factors,values):
#    arr = np.ones(shape)
#    for (i,j),[idxs,facs] in factors.iteritems():       
#        val = np.cumsum(values[idxs] * facs)[-1]
#        arr[i,j] = val       
#    return arr        




def apply():
    
    df_names = ['upper.csv','middle.csv','lower.csv']
    df_dir = '..\\par\\'

    fac_dir = '..\\factors\\'
    fac_files = os.listdir(fac_dir)
    fac_dict = {}
    for fac_file in fac_files:
        hydro = fac_file.split('.')[0].split('_')[-1]        
        pp_names,factors = load_factors(fac_dir+fac_file)
        fac_dict[hydro] = [pp_names,factors]
        df = pandas.read_csv(df_dir+hydro+'.csv',index_col=0,sep='|')
        for array_tup,values in df.iteritems():
            #--parse the array tuple
            in_name,out_name = array_tup.replace('"','').replace('\'','').replace('(','').replace(')','').split(',')
            in_name = str(in_name.strip())
            out_name = str(out_name.strip())
            print in_name,out_name
            shape = (grid.nrow,grid.ncol)
            mult = np.ones(shape)
            for (i,j),[idxs,facs] in factors.iteritems():       
                val = np.cumsum(values.values[idxs] * facs)[-1]
                mult[i,j] = val  
            base = np.loadtxt(in_name)
            print out_name
            np.savetxt(out_name,base*mult,fmt=' %15.5E')

def setup():
    pp_dir ='pp_locs\\'
    pp_files = os.listdir(pp_dir)
    out_dir = 'ref\\'   
    in_dir = 'ref\\base\\'
    property_suffixes = ['_k.ref','_sy.ref','_ss.ref','_thk_frac.ref']  
    rech_names = []
    #rech_dir = ref_dir+'mod\\rech_'
    #for i,sp in enumerate(grid.sp_start):
    #    rech_names.append(rech_dir+str(i+1)+'.ref')      
    
    par_dict = {}
    for pp_file in pp_files:        
        hydro = pp_file.split('.')[0].split('_')[-1]        
        f = open(pp_dir+pp_file,'r')
        pp_names = []
        pp_idx = []
        for line in f:
            raw = line.strip().split()
            pp_names.append(raw[0])
            pp_idx.append(int(raw[0].split('_')[2]))
        f.close()
        #par_names = []
        pp_dict = {}        
        for suffix in property_suffixes:
            tpl_entries = []
            prop = suffix.split('.')[0].split('_')[1]
            in_name = in_dir+hydro+suffix
            out_name = out_dir+hydro+suffix
            shutil.copy2('_model\\'+out_name,'_model\\'+in_name)
            for pp_name in pp_names:
                par_name = prop + pp_name[2:]
                par_grp = prop+'_'+hydro
                if par_grp  in par_dict.keys():
                    par_dict[par_grp].append(par_name)
                else:
                    par_dict[par_grp] = [par_name]
                tpl_entry = '~{0:25s}~'.format(par_name)
                #par_names.append(par_name)
                tpl_entries.append(tpl_entry)
            pp_dict[(in_name,out_name)] = tpl_entries
        #--recharge
        if hydro == 'upper':
            tpl_entries = []
            prop = 'rch'           
            in_name = in_dir+hydro+'_rechmult.ref'
            out_name = out_dir+hydro+'_rechmult.ref'            
            for pp_name in pp_names:
                par_name = prop + pp_name[2:]
                par_grp = prop+'_upper'
                if par_grp in par_dict.keys():
                    par_dict[par_grp].append(par_name)
                else:
                    par_dict[par_grp] = [par_name]
                tpl_entry = '~{0:25s}~'.format(par_name)
                #par_names.append(par_name)
                tpl_entries.append(tpl_entry)            
                pp_dict[(in_name,out_name)] = tpl_entries
                 
        df = pandas.DataFrame(pp_dict,index=pp_idx)
        tpl_name ='tpl\\'+hydro+'.tpl'
        f = open(tpl_name,'w',0) 
        f.write('ptf ~\n')
        df.to_csv(f,index_label='pp_number',sep='|')
        f.close()
        #--write a tester
        for col in df.columns:
            df[col] = 1.0
        df.to_csv('par\\'+hydro+'.csv',index_label='pp_number',sep='|')
        


    f_par = open('pst_components\\prop_pars.dat','w',0)
    f_grp = open('pst_components\\prop_grps.dat','w',0)
    par_grps = par_dict.keys()
    par_grps.sort()
    for prop in par_grps:
        
        f_grp.write('{0:20s}       relative     1.0000E-02   0.000      switch      2.000      parabolic\n'.format(prop))
        par_names = par_dict[prop]
        for par_name in par_names:            
            f_par.write('{0:20s}  log   factor  1.0  1.0e-10  1.0e+10  {1:20s}   1.0   0.0   1\n'.format(par_name,prop))


    f_par.close()
    f_grp.close()

    
    
        


if __name__ == '__main__':
    #setup()
    os.chdir('_model\\')
    apply()



