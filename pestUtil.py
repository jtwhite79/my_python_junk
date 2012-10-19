import re
import os
from datetime import datetime,timedelta
import shutil
import numpy as np 
import pandas
import pylab

prgp_reg = re.compile('\* parameter groups')
par_reg = re.compile('\* parameter data')
obgp_reg = re.compile('\* observation groups')
obs_reg = re.compile('\* observation data')
regul_reg = re.compile('regul')
prior_reg = re.compile('\* prior information')
reg_reg = re.compile('\* regularisation')
section_reg = re.compile('\*')
idx_reg = re.compile('index')
start_reg = re.compile('commencing')
end_reg = re.compile('completed')

vario_type_dict = {'spherical':'1','exponential':'2','gaussian':'3','power':'4'}
structure_list = [['STRUCTURE',['NUGGET','TRANSFORM','NUMVARIOGRAM',['VARNAME','CONTRIB']]],['VARIOGRAM',['VARTYPE','BEARING','A','ANISOTROPY']]]






def load_wrapped_format(nrow,ncol,filename):
	'''
	read 2darray from file
	file(str) = path and filename
	'''
	file_in = open(filename,'r')
	data = np.zeros((nrow*ncol),dtype='double')-1.0E+10
	d = 0
	while True:
		line = file_in.readline()
		if line is None or d == nrow*ncol:break
		raw = line.strip('\n').split()
		for a in raw:
			try:
				data[d] = float(a)
			except:
				print 'error casting to float on line: ',line
				sys.exit()
			if d == (nrow*ncol)-1:
				assert len(data) == (nrow*ncol)
				data.resize(nrow,ncol)
				return(data) 
			d += 1	
	file_in.close()
	data.resize(nrow,ncol)
	return(data)



def load_grid_spec(filename):
    f = open(filename)
    info = {}
    raw = f.readline().strip().split()
    nrow,ncol = int(raw[0]),int(raw[1])
    info['nrow'] = nrow
    info['ncol'] = ncol
    raw = f.readline().strip().split()
    xoff,yoff,rot = float(raw[0]),float(raw[1]),float(raw[2])
    info['xoffset'] = xoff
    info['ymax'] = yoff
    info['rotation'] = rot
    raw = f.readline()
    if '*' in raw:
        raw1 = raw.strip().split('*')
        assert int(raw1[0]) == ncol
        delr = np.zeros(ncol) + float(raw1[1])
        info['delr'] = delr
    else:
        raise NotImplementedError('too lazy')
    raw = f.readline()
    if '*' in raw:
        raw1 = raw.strip().split('*')
        assert int(raw1[0]) == nrow
        delc = np.zeros(nrow) + float(raw1[1])
        info['delc'] = delc
    else:
        raise NotImplementedError('too lazy')
    f.close()
    info['yoffset'] = info['ymax'] - np.cumsum(delc)[-1]
    return info


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


def load_smp_from_tsproc(filename):
    '''loads the time series from a tsproc output file to an smp instance
    '''
    f = open(filename,'r')
    s = smp(date_fmt='%m/%d/%Y')
    while True:
        line = f.readline()
        if line == '':
            break
        if 'TIME_SERIES' in line.upper():
            raw = line.strip().split()
            site_name = raw[1].replace('"','')
            record = []
            while True:
                line2 = f.readline()
                if line2.strip() == '':
                    break
                line2 = s.parse_line(line2)
                if line2[0] != site_name:
                    raise IndexError('site names dont match')
                record.append(line2[1:])
            s.records[site_name] = np.array(record)
    f.close()
    return s







class smp():
    '''simple, poorly designed class to handle site sample file types
    casts date and time fields to a single datetime object    
    '''
    def __init__(self,fname=None,date_fmt='%d/%m/%Y',load=False,pandas=False):
        #assert os.path.exists(fname)
        self.fname = fname
        self.date_fmt = date_fmt
        self.site_index = 0
        self.date_index = 1
        self.time_index = 2
        self.value_index = 3
        self.pandas = pandas
        if load is True:            
            self.records = self.load('all')            
        else:
            self.records = {}
       

    def make_unique(self):
        '''looks for multiple entries on the same day and averages them
        '''
        assert self.pandas is False, 'to use make_unique, records must not be loaded as pandas objects'
        for site,record in self.records.iteritems():
            unique_dates = np.unique(record[:,0])
            if unique_dates.shape[0] != record.shape[0]:
                unique = []                
                for udt in unique_dates:
                    vals = record[np.where(record[:,0]==udt),1]
                    unique.append([udt,np.mean(vals)])                    
                self.records[site] = np.array(unique)
                print


    def merge(self,other,how='average'):
        '''combines the records of two smp class instances based on site names
           for places where the data overlap, use how
           how = average,left,right
        '''
        for site,record in self.records.iteritems():
            if site in other.records.keys():
                other_record = other.records[site]
                                
                for other_dt,other_val in other_record:
                    if other_dt in record[:,0]:
                        if how == 'average':
                            record[np.where(record[:,0]==other_dt),1] = (record[np.where(record[:,0]==other_dt),1] + other_val) / 2.0
                        elif how == 'right':
                            record[np.where(record[:,0]==other_dt),1] = other_val
                        elif how == 'left':
                            pass
                    else:                        
                        record = np.vstack((record,np.array([other_dt,other_val])))
                        #print record[-1]                        
                #--sort the record - probably out of order
                
                sidx = np.argsort(record[:,0])
                record = record[sidx]                
                self.records[site] = record                               

    def plot(self,plt_name):
        fig = pylab.figure()
        ax = pylab.subplot(111)
        for site,record in self.records.iteritems():
            ax.plot(record[:,0],record[:,1],label=site)
        ax.grid()
        ax.legend()
        if plt_name:
            pylab.savefig(plt_name,dpi=300,format=plt_name.split('.')[-1],bbox_inches='tight')
            pylab.close('all')
            return
        else:
            return ax


    def load(self,site='all'):
        '''if site_name is 'all', loads all records
        if self.pandas, then load('all') returns a pandas datafram
        and load() returns a pandas series indexed by date
        '''                           
        if site.upper() != 'ALL':                        
            f = self.read_to(self.site_index,site)
            record = []
            while True:
                line = f.readline()
                if line.strip() == '':
                    break                        
                pline = self.parse_line(line)                                   
                if pline[self.site_index] != site:
                    break
                record.append(pline[1:])
            f.close()
            record = np.array(record)
            if self.pandas:                
                return pandas.Series(record[:,1],index=record[:,0],name=site)
            else:
                return {site:np.array(record)}
        else:  
            l_count = 0          
            f = open(self.fname,'r')
            records = {}
            for line in f:
                #print line.strip()
                l_count += 1
                if line.strip() == '':
                    break                             
                pline = self.parse_line(line)
                if pline[self.site_index] not in records.keys():
                    records[pline[0]] = [pline[1:]]
                else:
                    records[pline[0]].append(pline[1:])                
            f.close()
            #--cast each site record to a numpy array
            for site,record in records.iteritems():
                records[site] = np.array(record)
            if self.pandas:
                return self.records2dataframe(records)
            else:
                return records
    
    
    def records2dataframe(self,records):
        ''' to cast the dict records to a pandas dataframe
        '''
        #--use the first record as the seed for the dataframe        
        sites = records.keys()
        if sites:
            r1 = records[sites[0]]        
            dict = {'date':r1[:,0],sites[0]:r1[:,1]}
            df = pandas.DataFrame(dict)
            for site in sites[1:]:
                record = records[site]            
                dict = {'date':record[:,0],site:record[:,1]}
                df2 = pandas.DataFrame(dict)                
                df = pandas.merge(df,df2,how='outer',right_on='date',left_on='date')
            df.index = df['date']
            df.pop('date')
            return df
        else:
            return pandas.DataFrame()

    def active(self,dt):
        if self.pandas:       
            try:
                slice = self.records.xs(dt)
            except KeyError:
                return [[],[]]
            slice2 = slice.dropna()
            return slice2.index.tolist(),slice2.values.tolist()
        else:
            active_list = [[],[]]
            for site,record in self.records.iteritems():
                act = record[np.where(record[:,0]==dt)]                                    
                if act.shape[0] > 0:                
                    active_list[0].append(site)
                    active_list[1].append(act[0,1])                
            return active_list

    
    def get_site(self,findsite):                        
        if self.pandas:
            try:
                s = self.records[findsite].dropna()                
                return findsite,s.index.tolist(),s.values.tolist()
                #return findsite,self.records['date'].dropna().tolist(),self.records[findsite].dropna().tolist()
            except:
                raise IndexError('site '+str(findsite)+' not found in self.records')                   
        else:           
            if findsite not in self.records.keys():
                raise IndexError('site '+str(findsite)+' not found in self.records')                   
            for site,record in self.records.iteritems():
                if site == findsite:                
                    d = record[:,0].tolist()
                    v = record[:,1].tolist()                            
                    return site, d, v
            
                                              
    def get_unique_from_file(self,line_index,needindices=False):
        '''if needindices, then will also return a 0-based 
        index offset the first occurence in the file of unique value
        '''
        f = open(self.fname,'r')
        unique = []
        indices = []
        l_count = 0
        for line in f:
            if line.strip() == '':
                break            
            u = self.parse_line(line)[line_index]
            if u not in unique:
                unique.append(u)
                indices.append(l_count)
            l_count += 1
        f.close()
        if needindices:
            return unique,indices
        else:
            return unique                  

    def set_daterange(self,start,end,site_name=None):
        if site_name != None:
            rec = []
            for dt,val in self.records[site_name]:
                if dt >=start and dt <=end:
                    rec.append([dt,val])
            self.records[site_name] = np.array(rec)
        else:
            for site,record in self.records.iteritems():
                rec = []
                for dt,val in record:
                    if dt >=start and dt <=end:
                        rec.append([dt,val])
                self.records[site] = np.array(rec)

    
    def write_daterange(self,site_name,file_name,start,end,step):
        f = open(file_name,'w')
        sec = timedelta(seconds=1)
        day = start
        record = self.records[site_name]
        while day < record[0,0]:
            day += step

        while day < end:
            entries = record[np.where(np.logical_and(record[:,0]>=day,record[:,0]<day+step))]
            if entries.shape[0] > 0:
                if day < record[0,0]:
                    f.write((record[0,0]+sec).strftime(self.date_fmt+' %H:%M:%S')+' '+(start).strftime(self.date_fmt+' %H:%M:%S')+'\n')
                elif day + step > end:
                    f.write((day+sec).strftime(self.date_fmt+' %H:%M:%S')+' '+(end).strftime(self.date_fmt+' %H:%M:%S')+'\n')
                    break
            day += step
        f.close()


    def get_daterange(self,site_name=None,startmin=datetime(year=1,month=1,day=1,hour=12),endmax=datetime(year=2200,month=12,day=31,hour=12)):
        '''get the date range of records
        if site_name == None - get the total date range
        if site_name == 'all' - get a dictionary of the date range for each record
        records must be loaded
        '''

        if site_name.upper() == 'ALL':
            start_dict = {}
            end_dict = {}
            for site,record in self.records.iteritems():
                start,end = datetime(year=2200,month=1,day=1),datetime(year=1,month=1,day=1)        
                for dt,val in record:
                    if dt < start and dt >= startmin:
                        start = dt
                    if dt > end and dt <= endmax:
                        end = dt
                start_dict[site] = start
                end_dict[site] = end                                                                
            return start_dict,end_dict


        else:
            start,end = datetime(year=2200,month=1,day=1),datetime(year=1,month=1,day=1)        
            if site_name != None:
                for dt,val in self.records[site_name]:
                    if dt < start and dt >= startmin:
                        start = dt
                    if dt > end and dt <= endmax:
                        end = dt
                return start,end
            else:
                for site,record in self.records.iteritems():
                    for dt,val in record:
                        if dt < start and dt >= startmin:
                            start = dt
                        if dt > end and dt <= endmax:
                            end = dt
                return start,end
            #f = open(self.fname,'r')
            #for line in f:
            #    line = self.parse_line(line)
            #    if line[0] == site_name or site_name == None:
            #        if line[1] < start and line[1] >= startmin:
            #            start = line[1]
            #        if line[1] > end and line[1] <= endmax:
            #            end = line[1] 
            return start,end              


    def parse_line(self,line):
        ''' parse the string line into [name,datetime,None,value]
        '''        
        #print line
        raw = line.strip().split() 
        if len(raw) != 4:
            print raw
        site = raw[self.site_index]
        dt = datetime.strptime(raw[self.date_index]+' '+raw[self.time_index],self.date_fmt+' %H:%M:%S')
        val = float(raw[3])
        return [site,dt,val]

    def read_to(self,line_index,value):
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
        
    def save(self,fname):
        if len(self.records) > 0:
            f = open(fname,'w')
            for site,data in self.records.iteritems():
                if self.pandas:                                        
                    for dt,value in zip(data.index,data.values):                
                        f.write(str(site).ljust(10)+' '+dt.strftime(self.date_fmt+' %H:%M:%S')+'  {0:25.8e}\n'.format(value))              
                else:
                    for dt,value in data:                
                        f.write(str(site).ljust(10)+' '+dt.strftime(self.date_fmt+' %H:%M:%S')+'  {0:25.8e}\n'.format(value))              

            f.close()            




def write_structure_from_dict(file_name,structure_name,s_dict):
    try:
        f_out = open(file_name,'w')
    except TypeError:
        f_out = file_name
    f_out.write('STRUCTURE '+s_dict['STRUCTNAME']+'\n')
    s_dict.pop('STRUCTNAME')
    f_out.write(' NUGGET '+s_dict['NUGGET']+'\n')
    s_dict.pop('NUGGET')
    if 'TRANSFORM' in s_dict.keys():
        f_out.write(' TRANSFORM '+s_dict['TRANSFORM']+'\n')
        s_dict.pop('TRANSFORM')
    else:
        f_out.write(' TRANSFORM NONE\n')
    f_out.write(' NUMVARIOGRAM '+str(s_dict['NUMVARIOGRAM'])+'\n')        
    s_dict.pop('NUMVARIOGRAM')
    
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

def load_res_pandas(res_file):
    #f = open(res_file,'r')
    #header = f.readline().split()
    df = pandas.read_csv(res_file,sep='\s+',index_col=0)
    return df


def set_2_pareto(pst_name,res_name):
    '''sets up a generic pareto run from a regularization pst'''
    #--first update the prior information values and wghts
    regul = load_regul(pst_name)
    res = load_res_pandas(res_name)
    for i,r in enumerate(regul):        
        regul[i][-2] = '{0:15.6e}'.format(res['Weight'][r[0]])
        regul[i][-3] = '{0:15.6e}'.format(res['Modelled'][r[0]]) 
        regul[i][-1] = 'regul'                
    replace_prior(regul,pst_name)
    
    #--build a list of obs names
    o_names = []
    for name,group in zip(res.index,res['Group']):
        if re.search('regul',group,re.I) == None:
            o_names.append(name)


    #--set pareto control sections
    f = open(pst_name,'r')
    f_out = open('temp.pst','w')
    #--set the model to pareto
    f_out.write(f.readline())
    f_out.write(f.readline())
    line = f.readline().strip().split()
    line[-1] = 'pareto\n'    
    f_out.write(' '.join(line))
    #line = f.readline().strip().split()
    #line[2] = '1'
    #f_out.write(' '.join(line)+'\n')   
    #wght_start = float(regul[1][-2]) * 0.5
    #wght_final = wght_start * 10
    wght_start = 0.0
    wght_final = 4
    num_steps = 20
    while True:
        line = f.readline()
        if line == '':
            break
        #--set FORCEN to always_2
        if prgp_reg.search(line) != None:
            f_out.write(line)
            line = f.readline().strip().split()
            line[4] = 'always_2'
            f_out.write(' '.join(line)+'\n')
            line = f.readline().strip().split()
            line[4] = 'always_2'
            f_out.write(' '.join(line)+'\n')

        #--set a new obs group for all prior info
        elif obgp_reg.search(line) != None:
            f_out.write(line)
            f_out.write('regul\n')
            line = f.readline()

        elif reg_reg.search(line) != None:
            f_out.write('* pareto\n')
            f_out.write(' regul\n')
            f_out.write(' {0:10.3f} {1:10.3f} {2:10.0f}\n'.format(wght_start,wght_final,num_steps))
            f_out.write(' 3 3 3\n')
            f_out.write(' 0\n')
            f_out.write(' '+str(len(o_names))+'\n')
            f_out.write(' '.join(o_names)+'\n')
            f_out.close()
            break
        else:
            f_out.write(line)
    shutil.copy('temp.pst',pst_name)
    

 
def replace_prior(regul,pst_name):
    #--load the existing pst into a nested list
    f = open(pst_name,'r')
    f_out = open('temp.pst','w')
    lines = []
    while True:
        line = f.readline()
        if line == '':
            break
        if prior_reg.search(line) != None:
            f_out.write(line)
            #--read the pst past the existing prior information
            while True:
                line2 = f.readline()
                if section_reg.match(line2) or line2 == '':
                    break
            #--write in the new prior info
            for r in regul:
                f_out.write(' '.join(r)+'\n')
            f_out.write(line2)
        else:
            f_out.write(line)
    f.close()
    f_out.close()
    shutil.copy('temp.pst',pst_name)

            
       

def load_regul(pst_file,group=None,cast=False):
    f = open(pst_file,'r')    
    obs = []
    while True:
        line = f.readline()
        if line == '':
            break
        if prior_reg.search(line) != None:
            while True:
                line2 = f.readline()
                if section_reg.match(line2) != None or line2 == '':
                    break
                raw = line2.strip().split()                
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
                    vartype=2,bearing=90.0,a=1.0,anisotropy=1.0,mean=None):
    f_out = open(file_name,'w')
    f_out.write('STRUCTURE '+structure_name+'\n')
    f_out.write(' NUGGET {0:15.6e}\n'.format(nugget))
    f_out.write(' TRANSFORM '+transform+'\n')
    if mean:
        f_out.write(' MEAN {0:15.6e}\n'.format(mean))
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
 
    
    

               

                
   
    
        