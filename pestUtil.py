import re
import os
import numpy as np 
from datetime import datetime


prgp_reg = re.compile('\* parameter groups')
par_reg = re.compile('\* parameter data')
obgp_reg = re.compile('\* observation groups')
obs_reg = re.compile('\* observation data')
regul_reg = re.compile('regul')
section_reg = re.compile('\*')
idx_reg = re.compile('index')
start_reg = re.compile('commencing')
end_reg = re.compile('completed')

vario_type_dict = {'spherical':'1','exponential':'2','gaussian':'3','power':'4'}
structure_list = [['STRUCTURE',['NUGGET','TRANSFORM','NUMVARIOGRAM',['VARNAME','CONTRIB']]],['VARIOGRAM',['VARTYPE','BEARING','A','ANISOTROPY']]]



def gslib_2_smp(fname,out_ftype='.dat',xname='X',yname='Y'):
    f = open(fname,'r')
    title = f.readline().strip()
    num_props = int(f.readline().strip())
    prop_names = []
    props = {}    
    for i in range(num_props):
        pname = f.readline().strip()
        prop_names.append(pname)
        props[pname] = []
    assert xname in prop_names
    assert yname in prop_names
    for line in f:
        raw = line.strip().split()
        for prop,pname in zip(raw,prop_names):
            props[pname].append(float(prop))
    f.close()

    #--check for duplicate points
    d_idx = []
    for i,[x,y] in enumerate(zip(props[xname],props[yname])):
        for ii,[xx,yy] in enumerate(zip(props[xname][i+1:],props[yname][i+1:])):
            if xx == x and yy == y:
                d_idx.append(i)
    #--remove duplicates
    for i in d_idx[::-1]:
        for pname in props.keys():
            props[pname].pop(i)

                
    xlist = props.pop(xname)
    ylist = props.pop(yname)            
    zonelist = np.ones(len(xlist))
    namelist = ['point'+str(i+1) for i in range(len(xlist))]
    for pname,plist in props.iteritems():
        fname = title+'_'+pname+'.smp'
        write_coords(fname,namelist,xlist,ylist,zonelist,plist)

def write_coords(fname,namelist,xlist,ylist,zonelist,vlist):
    f = open(fname,'w')
    for n,x,y,zone,v in zip(namelist,xlist,ylist,zonelist,vlist):
        f.write(n.ljust(25)+' {0:20.6e} {1:20.6e} {2:20.0f} {3:20.6e}\n'.format(x,y,zone,v))
    f.close()



class smp():
    '''simple, poorly designed class to handle site sample file types
    casts date and time fields to a single datetime object
    casts records to numpy arrays of [np.datetime64,np.float]
    '''
    def __init__(self,fname,date_fmt='%d/%m/%Y',load=False):
        assert os.path.exists(fname)
        self.fname = fname
        self.date_fmt = date_fmt
        self.site_index = 0
        self.date_index = 1
        self.time_index = 2
        self.value_index = 3
        if load:
            self.records = self.load('all')
        else:
            self.records = {}



 
    def load(self,site='all'):
        '''if site_name is 'all', loads all records
        '''        
                   
        if site.upper() != 'ALL':                        
            f = self.readto(self.site_index,site)
            record = []
            while True:
                line = self.parse_line(f.readline())
                if line[self.site_index] != site:
                    f.close()
                    return {site:np.array(record)}
                record.append(line[1:])
        else:            
            f = open(self.fname,'r')
            records = {}
            for line in f:
                #print line.strip()
                if line.strip() == '':
                    break
                line = self.parse_line(line)
                if line[self.site_index] not in records.keys():
                    records[line[0]] = [line[1:]]
                else:
                    records[line[0]].append(line[1:])
            f.close()
            #--cast each site record to a numpy array
            for site,record in records.iteritems():
                records[site] = np.array(record)
            return records
    
    def active(self,dt):
        active_list = [[],[]]
        for site,record in self.records.iteritems():
            act = record[np.where(record[:,0]==dt)]                                    
            if act.shape[0] > 0:                
                active_list[0].append(site)
                active_list[1].append(act[0,2])                
        return active_list
    
                                              
    def getunique(self,line_index):
        f = open(self.fname,'r')
        unique = []
        for line in f:
            if line.strip() == '':
                break
            u = self.parse_line(line)[line_index]
            if u not in unique:
                unique.append(u)
        f.close()
        return unique                  

    def parse_line(self,line):
        ''' parse the string line into [name,datetime,None,value]
        '''
        raw = line.strip().split()        
        site = raw[self.site_index]
        dt = datetime.strptime(raw[self.date_index]+' '+raw[self.time_index],self.date_fmt+' %H:%M:%S')
        val = float(raw[3])
        return [site,dt,None,val]

    def readto(self,line_index,value):
        f = open(self.fname,'r')
        while True:
            last = f.tell()
            line = f.readline()
            if line.strip() == '':
                raise IndexError,'value ',+str(value)+' not found in column '+str(line_index)
            line = self.parse_line(line)
            if line[line_index] == value:
                f.seek(last)
                return f
        
                
            




def write_structure_from_dict(file_name,structure_name,s_dict):
    try:
        f_out = open(file_name,'w')
    except TypeError:
        f_out = file_name
    f_out.write('STRUCTURE '+s_dict['STRUCTNAME']+'\n')
    f_out.write(' NUGGET '+s_dict['NUGGET']+'\n')
    
    if 'TRANSFORM' in s_dict.keys():
        f_out.write(' TRANSFORM '+s_dict['TRANSFORM']+'\n')
    else:
        f_out.write(' TRANSFORM NONE\n')
    f_out.write(' NUMVARIOGRAM '+str(s_dict['NUMVARIOGRAM'])+'\n')    
    s_dict.pop('NUGGET')
    s_dict.pop('NUMVARIOGRAM')
    s_dict.pop('STRUCTNAME')
    vario_strings = []
    for v_name,v_dict in s_dict.iteritems():
        f_out.write(' VARIOGRAM '+v_name+' '+v_dict['CONTRIBUTION']+'\n')
        vario_strings.append(write_vario(v_dict))

    f_out.write('END STRUCTURE\n\n\n')
    for v in vario_strings:
        f_out.write(v)
   
    return


def write_vario(v_dict):    
           
    vstr = ''
    vstr += 'VARIOGRAM '+v_dict['VARNAME']+'\n'
    vstr += ' VARTYPE '+v_dict['VARTYPE']+'\n'
    vstr += ' BEARING '+v_dict['BEARING']+'\n'
    vstr += ' A '+v_dict['A']+'\n'
    vstr += ' ANISOTROPY '+v_dict['ANISOTROPY']+'\n'
    vstr += 'END VARIOGRAM\n\n'
    
    return vstr


def load_res(res_file,skipRegul=True):
    name_idx,grp_idx = 0,1
    meas_idx,mod_idx = 2,3
    wght_idx = 5
    
    grp_tracker = []
    
    name,grp = [],[]
    meas,mod = [],[]
    wght = []
    #if skipRegul is False:    
    #    regul_reg = re.compile('SaNdWiTcH')
    #else:
    #    regul_reg = regul_reg
    f = open(res_file,'r')
    #header = f.readline()
    while True:
        
        line = f.readline().strip().split()
        #print line
        if 'Name' in line:
            header = line
            line = f.readline().strip().split()
            break 
    #line = f.readline().strip().split()
    this_name,this_grp = [line[name_idx]],[line[grp_idx]]
    this_meas,this_mod = [float(line[meas_idx])],[float(line[mod_idx])]
    this_wght = [float(line[wght_idx])]
    
    for line in f:
        
        if regul_reg.search(line) == None:
            line = line.strip().split() 
            #print line[0]
            #--if the group name has changed
            if line[grp_idx] != this_grp[-1]:
                
                #--if this group name exists
                if this_grp[-1] in grp_tracker:
                    #print line[0],this_name
                    this_idx = grp_tracker.index(this_grp[-1])
                    name[this_idx].extend(this_name) 
                    grp[this_idx].extend(this_grp)
                    meas[this_idx] = np.vstack((meas[this_idx],this_meas))
                    mod[this_idx] = np.vstack((mod[this_idx],this_mod))
                    wght[this_idx] = np.vstack((wght[this_idx],this_wght))
                    
                else:
                   
                    name.append(this_name)
                    grp.append(this_grp)
                    meas.append(np.array(this_meas))
                    mod.append(np.array(this_mod))
                    wght.append(np.array(this_wght))
                    grp_tracker.append(this_grp[-1])
                
                #--reset the lists        
                this_name,this_grp = [line[name_idx]],[line[grp_idx]]
                this_meas,this_mod = [float(line[meas_idx])],[float(line[mod_idx])]
                this_wght = [float(line[wght_idx])]
                
            else:
               
                this_name.append(line[name_idx])
                this_grp.append(line[grp_idx])
                this_meas.append(float(line[meas_idx]))
                this_mod.append(float(line[mod_idx]))
                this_wght.append(float(line[wght_idx]))
    
   
    if this_grp[-1] in grp_tracker:
        #print line[0],this_name
        this_idx = grp_tracker.index(this_grp[-1])
        name[this_idx].extend(this_name) 
        grp[this_idx].extend(this_grp)
        meas[this_idx] = np.vstack((meas[this_idx],this_meas))
        mod[this_idx] = np.vstack((mod[this_idx],this_mod))
        wght[this_idx] = np.vstack((wght[this_idx],this_wght))
               
    else:
       
        name.append(this_name)
        grp.append(this_grp)
        meas.append(np.array(this_meas))
        mod.append(np.array(this_mod))
        wght.append(np.array(this_wght))
        grp_tracker.append(this_grp[-1])
    
          
    return name,grp_tracker,meas,mod,wght



def load_par_groups(pst_file,cast=False):
    f = open(pst_file,'r')
    par_groups = []
    for i in range(6):
        par_groups.append([])
    while True:
        line = f.readline()
        if line == '':
            break
        if prgp_reg.search(line) != None:
            while True:
                line2 = f.readline()
                
                if section_reg.search(line2) != None:
                    break
                raw = line2.strip().split()
                if cast:
                    raw[2] = float(raw[2])
                    raw[3] = float(raw[3])
                    raw[5] = float(raw[5])
                for r,p in zip(raw,par_groups):
                    p.append(r)
                                                        
                
    f.close()
    return par_groups            



def load_par(pst_file,group=None,cast=False):
    '''group is a specific par group or list of par groups'''
    f = open(pst_file,'r')    
    par = []
    for i in range(10):
        par.append([])
    while True:
        line = f.readline()
        if line == '':
            break
        if par_reg.search(line) != None:
            while True:
                line2 = f.readline()
                if section_reg.search(line2) != None:
                    break
                raw = line2.strip().split()
                if cast:
                    raw[3] = float(raw[3])
                    raw[4] = float(raw[4])
                    raw[5] = float(raw[5])
                    raw[7] = float(raw[7])
                    raw[8] = float(raw[8])
                    raw[9] = int(raw[9])
                if group != None:
                    try:
                        if raw[6] in group:
                            for r,p in zip(raw,par):
                                p.append(r)                            
                    except:                          
                        if raw[6] == group:  
                            for r,p in zip(raw,par):
                                 p.append(r)
                else:                          
                    for r,p in zip(raw,par):
                         p.append(r)                        
    f.close()            
    return par

   

def load_obs_groups(pst_file):
    f = open(pst_file,'r')
    obs_groups = []
    while True:
        line = f.readline()
        if line == '':
            break
        if obgp_reg.search(line) != None:
            while True:
                line2 = f.readline()
                if obs_reg.search(line2) != None:
                    break
                obs_groups.append(line2.strip())
                
    f.close()
    return obs_groups            
    
def load_obs(pst_file,group=None,cast=False):
    '''group is a specific obs group or list of obs groups'''
    f = open(pst_file,'r')    
    obs = []
    while True:
        line = f.readline()
        if line == '':
            break
        if obs_reg.search(line) != None:
            while True:
                line2 = f.readline()
                if section_reg.search(line2) != None:
                    break
                raw = line2.strip().split()
                if cast:
                    raw[1] = float(raw[1])
                    raw[2] = float(raw[2])
                if group != None:
                    try:
                        if raw[3] in group:
                            obs.append(raw)                            
                    except:  
                        
                        if raw[3] == group:  
                            obs.append(raw)
                else:                
                    obs.append(raw)
    f.close()
    return obs
                

def replace_obs(pst_file,new_pst,obs):
    f = open(pst_file,'r')
    f_out = open(new_pst,'w')
    re_obs = obs_reg
    re_mod = section_reg
    re_grp = obgp_reg
    
    #--get a list of obsgroups
    obs_groups = []
    for o in obs:
        if o[3] not in obs_groups:
            obs_groups.append(o[3])
    
    
    #--first 3 lines
    for l in range(3):
        f_out.write(f.readline())
    #--change nobs  and nobsgrps  
    raw = f.readline().strip().split()
    raw[1] = str(len(obs))
    raw[4] = str(len(obs_groups))
    f_out.write('   ')
    for r in raw:
        f_out.write(r+'  ')
    f_out.write('\n')
    
    #--now replace the obs groups and obs 
    while True:
        line = f.readline()
        if line == '':
            break
        if obgp_reg.search(line) != None:
            f_out.write(line)
            while True:
                line2 = f.readline()
                if obs_reg.search(line2) != None:
                    line = line2
                    break
            for og in obs_groups:
                f_out.write(og+'\n')
            
        if obs_reg.search(line) != None:
            f_out.write(line)
            #--read the original pst past the obs groups section
            while True:
                line2 = f.readline()
                if section_reg.search(line2) != None:
                    
                    break
            for o in obs:
                write_obs_line(o,f_out) 
            f_out.write(line2)              
        else:
            f_out.write(line)

    
def write_obs_line(o,f_out):
    #print o
    f_out.write(o[0].ljust(13)+'  ')
    f_out.write('{0:15.3e}  {1:15.3e}  '.format(o[1],o[2]))
    f_out.write(o[3]+'\n')            



def load_matrix(file_name):
    f = open(file_name,'r')
    
    raw = f.readline().strip().split()
    nrow,ncol = int(raw[0]),int(raw[1])
    vals = np.zeros((nrow,ncol))
    for i in range(nrow):
        j = 0
        while j < ncol:
            raw = f.readline().strip().split()
            for r in raw:
                vals[i,j] = float(r)
                j += 1
    row_header = f.readline()
    row_names = []
    for i in range(nrow):
        row_names.append(f.readline().strip())
    col_header = f.readline()
    col_names = []
    for j in range(ncol):
        col_names.append(f.readline().strip())
    f.close()
    return vals,row_names,col_names                     

def write_structure(file_name,structure_name,nugget=0.0,\
                    transform='none',numvariogram=1,\
                    variogram_name='var1',sill=1.0,\
                    vartype=2,bearing=90.0,a=1.0,anisotropy=1.0):
    f_out = open(file_name,'w')
    f_out.write('STRUCTURE '+structure_name+'\n')
    f_out.write(' NUGGET {0:15.6e}\n'.format(nugget))
    f_out.write(' TRANSFORM '+transform+'\n')
    f_out.write(' NUMVARIOGRAM '+str(numvariogram)+'\n')
    f_out.write(' VARIOGRAM '+variogram_name+' {0:15.6e}\n'.format(sill))
    f_out.write('END STRUCTURE\n\n')
    f_out.write('VARIOGRAM '+variogram_name+'\n')
    f_out.write(' VARTYPE '+str(vartype)+'\n')
    f_out.write(' BEARING {0:15.6e}\n'.format(bearing))
    f_out.write(' A {0:15.6e}\n'.format(a))
    f_out.write(' ANISOTROPY {0:15.6e}\n'.format(anisotropy))
    f_out.write('END VARIOGRAM\n')
    f_out.close()
    return

def load_jco(file_name,nespar=None,nobs=None):
    integer = np.int32
    double = np.float64
    char = np.uint8
    f = open(file_name,'rb')
    #--the header datatype
    header_dt = np.dtype([('itemp1',integer),('itemp2',integer),('icount',integer)])
    itemp1,itemp2,icount = np.fromfile(f,header_dt,1)[0]
    
    if itemp1 >= 0:
        raise TypeError, 'Jco produced by deprecated version of PEST,'+\
                         'Use JCOTRANS to convert to new format'
    
    #--error checking if desired
    if nespar is not None:
        if abs(itemp1) != nespar:
            raise ValueError,'nespar value not equal to jco dimensions'\
                             +str(nespar)+' '+str(abs(itemp1))
    if nobs is not None:
        if abs(itemp2) != nobs:
            raise ValueError,'nobs value not equal to jco dimensions'\
                             +str(nobs)+' '+str(abs(itemp2))
   
    nespar,nobs = abs(itemp1),abs(itemp2)                                  
    x = np.zeros((nobs,nespar))    
    
    #--the record datatype
    rec_dt = np.dtype([('j',integer),('dtemp',double)])
    
    #--read all data records
    data = np.fromfile(f,rec_dt,icount) 
    
    #--uncompress the data into x    
    for i in data:
        j = i[0]
        dtemp = i[1]
        ies = ((j-1) / nobs) + 1
        irow = j - ((ies - 1) * nobs)
        #print i,ies,irow
        
        #--zero-based indexing translation
        x[irow-1,ies-1] = dtemp
        
    #--read parameter names
    par_names = []
    for i in range(nespar):
        pn = np.fromfile(f,char, count=12).tostring()
        par_names.append(pn)
        #print 'par:',pn
    
    #--read obs names
    obs_names = []
    for i in range(nobs):
        on = np.fromfile(f,char, count=20).tostring()
        obs_names.append(on)
        #print 'obs:',on
                
    return x,par_names,obs_names

def write_matrix(file_name,x,row_names,col_names,icode=2):
    nrow,ncol = x.shape
    assert nrow == len(row_names)
    assert ncol == len(col_names)
    
    f_out = open(file_name,'w')
    f_out.write(' {0:7.0f} {1:7.0f} {2:7.0f}\n'.format(nrow,ncol,icode))
    for r in range(nrow):
        i = 0
        for c in range(ncol):
            f_out.write(' {0:15.7e} '.format(x[r,c]))      
            i += 1
            if i % 7 == 0:
                f_out.write('\n')
        f_out.write('\n')
    
    f_out.write('* row names\n')
    for r in row_names:
        f_out.write(r+'\n')
    
    f_out.write('* column names\n')
    for c in col_names:
        f_out.write(c+'\n')
    f_out.close()

def time2sec(time_str):
    raw = time_str.split(':')
    hr = float(raw[0])
    min = float(raw[1])
    sec = float(raw[2])
    return sec + (min * 60.0) + (hr * 60.0 * 60.0)


def load_rmr_results(filename,byRoot=False):
    nodes = []
    
    f = open(filename,'r')
    #-- find first node instance
    #while True:
    #    line = f.readline()
    #    if wd_reg.search(line) is not None:
    #        raw = line.strip().split()
    #        sec = 
             
    for line in f:
        raw = line.strip().split()
        if idx_reg.search(line) is not None:
           #print line
           wd = line.split('"')[1]
           if byRoot:
            wd = wd.split('\\\\')[0]           
           n_idx = int(raw[3])
           init_time = time2sec(raw[0])
           #print n_idx,wd,init_time
           nodes.append(c_node(n_idx,wd,init_time)) 
        elif start_reg.search(line):
            raw = line.strip().split()           
            n_idx = int(raw[-1][:-1])
            c_idx = nodes.index(n_idx)
            #print line            
            nodes[c_idx].start_times.append(time2sec(raw[0]))
        elif end_reg.search(line):
            raw = line.strip().split()                     
            n_idx = int(raw[-1][:-1])
            c_idx = nodes.index(n_idx)            
            nodes[c_idx].end_times.append(time2sec(raw[0]))    
    f.close()
    results = [[],[],[]]
    for n in nodes:
        n.calc_run_stats()
        results[0].append(n.n_idx)
        results[1].append(n.avg_run)
        results[2].append(n.std_run)
    return results
 
    
    

               

                
   
    
        