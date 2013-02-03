import os
import shutil
import calendar
import numpy as np
import pandas


def load_factors(filename):
    f = open(filename,'r')
    #--read the header info
    pp_filename = f.readline().strip()
    zone_filename = f.readline().strip()
    raw = f.readline().strip().split()
    ncol,nrow = int(raw[0]),int(raw[1])
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
    return (nrow,ncol),pp_names,factors                

def node2ij(node,shape):
    i = int(node / shape[1])
    if (i * shape[1]) < node:
        i += 1
    j = node - ((i-1) * shape[1])    
    return i-1,j-1



def apply():
    
    df_files = ['par\\coarse_properties.csv','par\\fine_properties.csv']
    factor_files = ['factors\\pp_fac_coarse.fac','factors\\pp_fac_fine.fac']    
    for fac_file,df_file in zip(factor_files,df_files):        
        shape,pp_names,factors = load_factors(fac_file)       
        df = pandas.read_csv(df_file,index_col=0,sep='|')
        for arr_name,values in df.iteritems():                        
            print arr_name
            arr = np.zeros(shape)
            for (i,j),[idxs,facs] in factors.iteritems():       
                val = np.cumsum(values.values[idxs] * facs)[-1]
                arr[i,j] = val              
            np.savetxt(arr_name,arr,fmt=' %15.5E')

def setup():    
    #pp_files = ['misc\\pp_locs_coarse.dat','mics\\pp_locs_fine.dat']
    param_prefixes = ['hk','pr']
    param_names = ['hk','prsity']
    pest_dict = {}

    temp_dir = 'ref\\mult\\'   
    #--coarse
    tpl_dict = {}
    coarse_names = ['upr','prd','lwr']
    coarse_prefixes = ['up','pd','lw']
    pp_file = 'misc\\pp_locs_coarse.dat'
    f = open(pp_file,'r')
    pp_names = []
    pp_numbers = []
    for line in f:
        pp_name = line.strip().split()[0]
        pp_names.append(pp_name)
        pp_number = int(pp_name.split('_')[1])
        pp_numbers.append(pp_number)
    f.close()
    for pprefix,pname in zip(param_prefixes,param_names):
        for cprefix,cname in zip(coarse_prefixes,coarse_names):
            tpl_entries = []
            pest_names = []
            for pp_number in pp_numbers:
                name = pprefix+'_'+cprefix+'_{0:04d}'.format(pp_number)
                pest_names.append(name)
                tpl_entry = '~{0:25s}~'.format(name)
                tpl_entries.append(tpl_entry)
            grp_name = pname+'_'+cname
            pest_dict[grp_name] = pest_names
            arr_name = temp_dir+grp_name+'.ref'
            tpl_dict[arr_name] = tpl_entries


    #--ets rate wet and dry, pt and nexrad
    
    #for mn in calendar.month_abbr[1:]:
    for period in ['pt','nx']:
        for mn in ['dr','wt']:
            tpl_entries = []
            pest_names = []
            for pp_number in pp_numbers:
                name = 'et_'+mn+period+'_{0:03d}'.format(pp_number)
                pest_names.append(name)
                tpl_entry = '~{0:25s}~'.format(name)
                tpl_entries.append(tpl_entry)
            grp_name = 'ets_'+mn+'_'+period
            pest_dict[grp_name] = pest_names
            arr_name = temp_dir+grp_name+'.ref'
            tpl_dict[arr_name] = tpl_entries


    f = open('tpl\\coarse_properties.tpl','w',0)
    f.write('ptf ~\n')

    tpl_df = pandas.DataFrame(tpl_dict,index=pp_names)
    tpl_df.to_csv(f,sep='|',index_label = 'pp_names')
    f.close()
    for col in tpl_df.columns:
        tpl_df[col] = 1.0
    tpl_df.to_csv('par\\coarse_properties.csv',index_label='pp_names',sep='|')



    #--fine
    tpl_dict = {}
    fine_names = ['pd1','pd2']
    fine_prefixes = ['p1','p2']
    pp_file = 'misc\\pp_locs_fine.dat'
    f = open(pp_file,'r')
    pp_names = []
    pp_numbers = []
    for line in f:
        pp_name = line.strip().split()[0]
        pp_names.append(pp_name)
        pp_number = int(pp_name.split('_')[1])
        pp_numbers.append(pp_number)
    f.close()
    for pprefix,pname in zip(param_prefixes,param_names):
        for fprefix,fname in zip(fine_prefixes,fine_names):
            tpl_entries = []
            pest_names = []
            for pp_number in pp_numbers:
                name = pprefix+'_'+fprefix+'_{0:04d}'.format(pp_number)
                pest_names.append(name)
                tpl_entry = '~{0:25s}~'.format(name)
                tpl_entries.append(tpl_entry)
            grp_name = pname+'_'+fname
            pest_dict[grp_name] = pest_names
            arr_name = temp_dir+grp_name+'.ref'
            tpl_dict[arr_name] = tpl_entries

    f = open('tpl\\fine_properties.tpl','w',0)
    f.write('ptf ~\n')

    tpl_df = pandas.DataFrame(tpl_dict,index=pp_names)
    tpl_df.to_csv(f,sep='|',index_label = 'pp_names')
    f.close()
    for col in tpl_df.columns:
        tpl_df[col] = 1.0
    tpl_df.to_csv('par\\fine_properties.csv',index_label='pp_names',sep='|')

    f_par = open('pst_components\\prop_pars.dat','w',0)
    f_grp = open('pst_components\\prop_grps.dat','w',0)

    par_grps = pest_dict.keys()
    par_grps.sort()

    for prop in par_grps:            
        f_grp.write('{0:20s}       relative     1.0000E-02   0.000      switch      2.000      parabolic\n'.format(prop))
        par_names = pest_dict[prop]
        for par_name in par_names:            
            f_par.write('{0:20s}  log   factor  1.0  1.0e-10  1.0e+10  {1:20s}   1.0   0.0   1\n'.format(par_name,prop))


    f_par.close()
    f_grp.close()            



    #par_dict = {}
    #for pp_file in pp_files:        
    #    hydro = pp_file.split('.')[0].split('_')[-1]        
    #    f = open(pp_dir+pp_file,'r')
    #    pp_names = []
    #    pp_idx = []
    #    for line in f:
    #        raw = line.strip().split()
    #        pp_names.append(raw[0])
    #        pp_idx.append(int(raw[0].split('_')[2]))
    #    f.close()
    #    #par_names = []
    #    pp_dict = {}        
    #    for suffix in property_suffixes:
    #        tpl_entries = []
    #        prop = suffix.split('.')[0].split('_')[1]
    #        in_name = in_dir+hydro+suffix
    #        out_name = out_dir+hydro+suffix
    #        shutil.copy2('_model\\'+out_name,'_model\\'+in_name)
    #        for pp_name in pp_names:
    #            par_name = prop + pp_name[2:]
    #            par_grp = prop+'_'+hydro
    #            if par_grp  in par_dict.keys():
    #                par_dict[par_grp].append(par_name)
    #            else:
    #                par_dict[par_grp] = [par_name]
    #            tpl_entry = '~{0:25s}~'.format(par_name)
    #            #par_names.append(par_name)
    #            tpl_entries.append(tpl_entry)
    #        pp_dict[(in_name,out_name)] = tpl_entries
        
    #    df = pandas.DataFrame(pp_dict,index=pp_idx)
    #    tpl_name ='tpl\\'+hydro+'.tpl'
    #    f = open(tpl_name,'w',0) 
    #    f.write('ptf ~\n')
    #    df.to_csv(f,index_label='pp_number',sep='|')
    #    f.close()
    #    #--write a tester
    #    for col in df.columns:
    #        df[col] = 1.0
    #    df.to_csv('par\\'+hydro+'.csv',index_label='pp_number',sep='|')
        


    #f_par = open('pst_components\\prop_pars.dat','w',0)
    #f_grp = open('pst_components\\prop_grps.dat','w',0)
    #par_grps = par_dict.keys()
    #par_grps.sort()
    #for prop in par_grps:
        
    #    f_grp.write('{0:20s}       relative     1.0000E-02   0.000      switch      2.000      parabolic\n'.format(prop))
    #    par_names = par_dict[prop]
    #    for par_name in par_names:            
    #        f_par.write('{0:20s}  log   factor  1.0  1.0e-10  1.0e+10  {1:20s}   1.0   0.0   1\n'.format(par_name,prop))


    #f_par.close()
    #f_grp.close()

    
    
        


if __name__ == '__main__':
    setup()
    #os.chdir('_model\\')
    apply()



