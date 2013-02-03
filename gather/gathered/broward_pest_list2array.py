import shutil
import os
from datetime import datetime
import copy
import numpy as np
import pandas



def apply():
    lu_dir = 'ref\\lu\\'
    out_dir = 'bro.03\\calibration\\flowref\\lu\\'
    
    #--load the dataframe and extract the row with array names   
    df = pandas.read_csv('par\\lu_table.csv')   
    arr_names = df.ix[0][1:]
    df = df.drop([0],axis=0)
    
    #--process each lu mapping array  
    lu_files = os.listdir(lu_dir)
    dts,arrs = [],[]
    for lu_file in lu_files:
        year = int(lu_file.split('.')[0].split('_')[1])        
        map_arr = np.loadtxt(lu_dir+lu_file)        
        val_arr = np.zeros_like(map_arr).astype(np.float32)
        for pname,aname in arr_names.iteritems():
            values = df[pname]
            for blu_code,value in values.iteritems():
                val_arr[np.where(map_arr==blu_code)] = value
            aname = str(year)+'_'+aname
            print aname         
            val_arr.tofile(out_dir+aname)
    return  
   


def setup():
    #--make tpl file
    tbl_file = '..\\_landuse\\bro_landuse_parameters.dat'
    f = open(tbl_file,'r')
    header1,header2 = f.readline().strip().replace('KVEG','petm').split(),f.readline().strip().split()
    par_dict = {}
    tpl_entries = {}
    pval_dict = {}
    for h1,h2 in zip(header1[1:],header2[1:]):       
        if h2 != 'none':
            tpl_entries[h1] = [h2]
    blu_codes = [-999]
    fake_entries = copy.deepcopy(tpl_entries)
    for line in f:
        raw = line.strip().split()
        blu_codes.append(raw[0])
        pnames = []
        for h1,h2,r in zip(header1[1:],header2[1:],raw[1:]):
            if h2 != 'none':
               
                pname = h1+raw[0]
                pval_dict[pname] = float(r)
                assert len(pname) <= 10,pname                
                if h1 not in par_dict.keys():
                    par_dict[h1] = [pname]
                else:
                    par_dict[h1].append(pname)
                
                tpl_entry = '~{0:25s}~'.format(pname)
                if h1 in tpl_entries.keys():
                    tpl_entries[h1].append(tpl_entry)
                    fake_entries[h1].append(1.0)
                else:
                    tpl_entries[h1] = [tpl_entry]
    #for col,lst in tpl_entries.iteritems():
    #    print col,len(lst),len(blu_codes)
    df = pandas.DataFrame(tpl_entries,index=blu_codes)
    f = open('tpl\\lu_table.tpl','w',0)
    f.write('ptf ~\n')
    #f.write(','.join(header2)+'\n')
    df.to_csv(f,index_label='BLU')
    f.close()

    #for col in df.columns:
    #    df[col] = 1.0
    df = pandas.DataFrame(fake_entries,index=blu_codes)
    #f = open('par\\lu_table.csv','w',0)
    #f.write('ptf ~\n')
    #f.write(','.join(header2)+'\n')
    df.to_csv('par\\lu_table.csv',index_label='BLU')
    #f.close()


    #--write the pst components
    f_grp = open('pst_components\\landuse_grps.dat','w',0)
    f_par = open('pst_components\\landuse_pars.dat','w',0)
    pargps = par_dict.keys()
    pargps.sort()
    for pargp in pargps:
        pnames = par_dict[pargp]
        f_grp.write('{0:<20s} factor 0.01  0.001 switch  2.0 parabolic\n'.format(pargp))
        for pname in pnames:

            f_par.write('{0:<20s} log factor  {1:15.3E} 1.0e-10 1.0e+10 {2:<20s}  1.0 0.0  0\n'.format(pname,pval_dict[pname],pargp))
    f_grp.close()
    f_par.close()
    

    #--copy the landuse code arrays over
    in_dir = '..\\_landuse\\ref\\'
    out_dir = 'ref\\lu\\'
    files = os.listdir(in_dir)
    for f in files:
        if f.endswith('_c.ref'):
            shutil.copy(in_dir+f,out_dir+f)

if __name__ == '__main__':
    setup()
    #apply()
