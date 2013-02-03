import os
from datetime import datetime
import calendar
import numpy as np
import pandas
'''setup and apply monthly factors to the tidal canals and intercoastal
'''

SSM_FILES = ['..\\_model\\bro.03\\seawat.ssm','..\\_prediction\\bro.03.pred\\seawat.ssm']
LIST_DIRS = ['bro.03\\calibration\\seawatlistbin\\','bro.03\\prediction\\seawatlistbin\\']
SSM_LOGICALS = 'T F T T T T F F F F \n'
ssm_dtype_formal = np.dtype([('layer','i4'),('row','i4'),('column','i4'),('concentration','f4'),('itype','i4')])
ssm_dtype_extend = np.dtype([('layer','i4'),('row','i4'),('column','i4'),('concentration','f4'),('itype','i4'),('aux','a20')])
#ssm_dtype_formal = np.dtype([('layer', np.int32),('row', np.int32),('column', np.int32),('concentration', np.float32),('itype', np.int32)])





def parse_ssm_line(line):
    raw = line.strip().split()
    l,r,c = int(raw[0]),int(raw[1]),int(raw[2])
    conc = float(raw[3])
    itype = int(raw[4])    
    return [l,r,c,conc,itype,'']

def apply():

    #--load the key files into a dict
    itype_dict = {'riv':4,'ghb':5}
    files = os.listdir('misc\\')
    key_files = []
    for f in files:
        if 'key' in f and 'ssm' in f:
            key_files.append(f)
    key_dict = {}
    for key_file in key_files:
        ptype = key_file.split('.')[0].split('_')[1]
        itype = itype_dict[ptype]
        f = open('misc\\'+key_file,'r')
        header = f.readline()
        for line in f:
            raw = line.strip().split(',')
            r,c = int(raw[1]),int(raw[2])       
            key_dict[(r,c,itype)] = raw[0]
        f.close()


    #--load the factors
    factor_mn_dict = {}
    f = open('par\\ghbwell_ssm.csv','r')
    header = f.readline().strip().split(',')
    for line in f:
        raw = line.strip().split(',')
        mn_dict = {}
        for par,factor in zip(header[1:],raw[1:]):
            mn_dict[par] = float(factor)
        factor_mn_dict[int(raw[0])] = mn_dict

    #--build each ssm file
    for ssm_file,list_dir in zip(SSM_FILES,LIST_DIRS):
        files = os.listdir(list_dir)
        ssm_list_files = []
        for f in files:
            if 'ssm' in f:
                ssm_list_files.append(f)
        ssm_list_files.sort()

        #--parse the filenames
        nss_list = []
        for f in ssm_list_files:
            nss = int(f.split('.')[0].split('_')[2])
            nss_list.append(nss)
        mxss = max(nss_list)
        f = open('test.ssm','w')
        f.write(SSM_LOGICALS)
        #--initial rch and ets stuff
        f.write('{0:10d}\n'.format(1))
        f.write('{0:10d}{1:10.1f}{2:>20s}{3:10d}\n'.format(0,0.0,'FREE',0))
        f.write('{0:10d}\n'.format(1))
        f.write('{0:10d}{1:10.1f}{2:>20s}{3:10d}\n'.format(0,0.0,'FREE',0))
        #--start the sp loop
        for ssm_file,nss in zip(ssm_list_files,nss_list):
            f.write('{0:10d}\n'.format(nss))
            dt = datetime.strptime(ssm_file.split('_')[1],'%Y%m%d')
            mn = dt.month            
            print 'processing',dt
            arr = np.fromfile(list_dir+ssm_file,dtype=ssm_dtype_extend)
            factors = factor_mn_dict[mn]
            for name,factor in factors.iteritems():
                arr['concentration'][np.where(arr['aux']==name)] *= factor
            arr = arr[['layer','row','column','concentration','itype']]              
            np.savetxt(f,arr,fmt=' %9d %9d %9d %9.3E %9d')
            f.write('{0:10d}\n{1:10d}\n'.format(-1,-1))
        f.close()
    return    

def setup():
    '''write an ssm key file and extract stress period nss lists to binary
    '''
    from bro import seawat as cal
    from bro_pred import seawat as pred

    
    
    #--build a swr reach tidal key
    f = open('..\\_BCDPEP\\BCDPEP_reach_conc.dat','r')
    f.readline()
    tidal_conc = {}
    for line in f:
        raw = line.strip().split(',')
        tidal_conc[int(raw[0])] = float(raw[1])
    f.close()

    #--group the tidal source reaches if the conc is the same
    tidal_rc,tidal_names = [],[]  
    concs,groups = [],[]
    for sreach,conc in tidal_conc.iteritems():
        if conc in concs:
            groups[concs.index(conc)].append(sreach)
        else:
            groups.append([sreach])
            concs.append(conc)
            tidal_rc.append([])
            tidal_names.append([])
    
    import shapefile
    shapename = '..\\_gis\\scratch\\sw_reaches_conn_swrpolylines_2'
    recs = shapefile.load_as_dict(shapename,loadShapes=False)
    
    for r,c,sreach,sstruct,sname in zip(recs['ROW'],recs['COLUMN'],recs['SRC_reach'],recs['SRC_struct'],recs['SRC_name']):
        if sstruct == -1:
            for i,group in enumerate(groups):
                if sreach in group:
                    tidal_rc[i].append((r,c))
                    if sname not in tidal_names[i]:
                        tidal_names[i].append(sname)

    f = open('misc\\ssm_riv.key','w',0)
    f.write('group_name,row,col,names\n')
    for i,[tups,names] in enumerate(zip(tidal_rc,tidal_names)):
        name = '_'.join(names).replace(' ','_').replace(',','_')
        for (r,c) in tups:
            f.write('riv_cn_#'+str(i+1)+','+str(r)+','+str(c)+','+name+'\n')
    f.close()        


    #--build intercoastal ghb tidal key
    ibound = np.loadtxt('..\\_model\\bro.03\\seawatref\\ibound_CS.ref',dtype=np.int)
    ic_groups = {}
    for i in range(ibound.shape[0]):
        for j in range(ibound.shape[1]):            
            name = 'ghb_cn_#'+str(ibound[i,j])
            if name in ic_groups.keys():
                ic_groups[name].append((i+1,j+1))
            else:
                ic_groups[name] = [(i+1,j+1)]
    f = open('misc\\ssm_ghb.key','w',0)
    f.write('name,row,col\n')
    for name,tups in ic_groups.iteritems():
        for (r,c) in tups:
            f.write(name+','+str(r)+','+str(c)+'\n')
    f.close()
    
    #--write an ssm template file - monthly
    par_dict = {}
    tpl_entries = {}
    months = calendar.month_abbr
    pnames = []
    tpl_dict = {}        
    for riv_grp in range(len(tidal_rc)):
        tpl_entries = []
        for mn in months[1:]:    
            pname = 'rcn_'+str(riv_grp+1)+'_'+mn
            assert len(pname) <= 10,pname
            pnames.append(pname)
            tpl_entry = '~{0:25s}~'.format(pname)
            tpl_entries.append(tpl_entry)
        tpl_dict['riv_cn_#'+str(riv_grp+1)] = tpl_entries
    par_dict['riv_conc'] = pnames
    pnames = []
    for ghb_grp in ic_groups.keys():
        grp_num = int(ghb_grp.split('#')[1])
        tpl_entries = []
        for mn in months[1:]:    
            pname = 'gcn_'+str(grp_num)+'_'+mn
            assert len(pname) <= 10,pname
            pnames.append(pname)
            tpl_entry = '~{0:25s}~'.format(pname)
            tpl_entries.append(tpl_entry)
            tpl_dict['ghb_cn_#'+str(ghb_grp)] = tpl_entries
    par_dict['ghb_conc'] = pnames

    #--save the template file
    df = pandas.DataFrame(tpl_dict)
    df.index = df.index + 1
    f = open('tpl\\ghbwel_ssm.tpl','w',0)
    f.write('ptf ~\n')
    df.to_csv(f,index_label='month')
    f.close()

    #--save a generic par file for testing
    for col in df.columns:
        df[col] = 1.0
    df.to_csv('par\\ghbwell_ssm.csv',index_label='month')

    #--write the pst components
    f_grp = open('pst_components\\ghbwel_ssm_grps.dat','w',0)
    f_par = open('pst_components\\ghbwel_ssm_pars.dat','w',0)
    pargps = par_dict.keys()
    pargps.sort()
    for pargp in pargps:
        pnames = par_dict[pargp]
        f_grp.write('{0:<20s} factor 0.01  0.001 switch  2.0 parabolic\n'.format(pargp))
        for pname in pnames:

            f_par.write('{0:<20s} log factor  1.0 1.0e-10 1.0e+10 {1:<20s}  1.0 0.0  0\n'.format(pname,pargp))
    f_grp.close()
    f_par.close()

    #--extract sp data and zip to binary   
    #--load the key files into a dict
    itype_dict = {'riv':4,'ghb':5}
    files = os.listdir('misc\\')
    key_files = []
    for f in files:
        if 'key' in f and 'ssm' in f:
            key_files.append(f)
    key_dict = {}
    for key_file in key_files:
        ptype = key_file.split('.')[0].split('_')[1]
        itype = itype_dict[ptype]
        f = open('misc\\'+key_file,'r')
        header = f.readline()
        for line in f:
            raw = line.strip().split(',')
            r,c = int(raw[1]),int(raw[2])       
            key_dict[(r,c,itype)] = raw[0]
        f.close()
    
         
    sp_lists = [cal.sp_start,pred.sp_start]    
    for ssm_file,list_dir,sp_list in zip(SSM_FILES,LIST_DIRS,sp_lists):
        f = open(ssm_file,'r')
        #--read the header info
        logicals = f.readline()
        maxssm = int(f.readline().strip())
        #--read the rch,ets junk
        rchets_lines = []
        for i in range(4):
            rchets_lines.append(f.readline().strip())
        #--start the sp loop
        kper = 0
        while True:
            try:
                nss = int(f.readline().strip())
            except:
                break
            lines = []
            #line_str = ''
            for i in range(nss):
                line = parse_ssm_line(f.readline())
                try:
                    line[-1] = key_dict[(line[1],line[2],line[4])]
                except:
                    pass
                #line_str += line                
                lines.append(tuple(line))                                
            arr = np.array(lines,dtype=ssm_dtype_extend) 
            dt = sp_list[kper]
            fname = list_dir+'ssm_'+dt.strftime('%Y%m%d')+'_'+str(nss)+'.dat'
            print 'writing',fname
            #--for testing
            #np.savetxt('test.dat',arr,fmt=' %9d %9d %9d %15.6E %9d %20s')
            arr.tofile(fname)
            #--read the repeat rch and ets lines
            rch = f.readline()
            rch = f.readline()
            kper += 1
            
                                                



if __name__ == '__main__':
    #setup()
    apply()
    
