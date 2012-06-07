import re
import numpy as np 


prgp_reg = re.compile('\* parameter groups')
par_reg = re.compile('\* parameter data')
obgp_reg = re.compile('\* observation groups')
obs_reg = re.compile('\* observation data')
regul_reg = re.compile('regul')
section_reg = re.compile('\*')
idx_reg = re.compile('index')
start_reg = re.compile('commencing')
end_reg = re.compile('completed')

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
 
    
    
class c_node():
    
    def __init__(self,n_idx,work_dir,init_time):
        self.n_idx = n_idx
        self.work_dir = work_dir
        self.init_time = init_time
        self.start_times = []
        self.end_times = []
        self.run_times = []
        self.avg_run = None
        self.std_run = None
    def __repr__(self):
        return self.n_idx
    def __eq__(self,val):
        if isinstance(val,int):
            if self.n_idx == val:
                return True
            return False
        elif instance(val,str):
            if self.wd == val:
                return True
            return False
    
    def calc_run_stats(self):
        #for i,s in enumerate(self.start_times):            
        for e,s in zip(self.end_times,self.start_times):
            #rtime = self.end_times[i] - s
            rtime = e - s
            self.run_times.append(rtime)
        tot = 0.0
        for r in self.run_times:
            tot += r            
        self.avg_run = tot / len(self.run_times)
        
        var = 0.0
        for r in self.run_times:
            var += (r - self.avg_run)**2
        var /= len(self.run_times)
        self.std_run = var**0.5            
        
        
#--need python 2.7       
#def get_control_dict(ctl_file='pest_control.dat'):
#    control = OrderedDict()
#    
#    line_pos = OrderedDict()   
#    f = open(ctl_file,'r')
#    pcf = f.readline()    
#    line_count = 0
#    for line in f: 
#        raw = line.strip().split()
#        for r in raw:            
#            control[r] = ''
#            line_pos[r] = line_count
#        line_count += 1
#    f.close()
#    return control,line_pos
                    
#def load_control(pst_file,control=None):
#     
#    if control == None:
#        sections,control = get_control_dict()
#    
#    f = open(pst_file,'r')
#    pcf = f.readline()
#    
#    for ctl_sec in control:
#        for 
        
            
    

#--for testing
#pst_file = 'pest_struct.pst'
#par_groups = load_par_groups(pst_file,cast=True)
#par = load_par(pst_file)
#print par[6]
#obs_groups = load_obs_groups(pst_file)
#obs = load_obs(pst_file,cast=True)

               

                
   
    
        