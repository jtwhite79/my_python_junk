import numpy as np
from datetime import datetime,timedelta
import pandas
import shapefile


ds_1_h = ['#NREACHES','ISWRONLY','ISWRCBC','ISWRPRGF','ISWRPSTG','ISWRPQAQ','ISWRPQM','ISWRPSTR','ISWRFRN','ISWROPT']
ds_2_h = ['#DLENCONV','TIMECONV','RTINI','RTMIN','RTMAX','RTPRN','RTMULT','NTMULT','DMINGRAD','DMNDEPTH','DMAXRAI','DMAXSTG','DMAXINF']
ds_3_h = ['#ISOLVER','NOUTER','NINNER','IBT','TOLS','TOLR','TOLA','DAMPSS','DAMPTR','IPRSWR','MUTSWR','IPC','NLEVELS','DROPTOL','IBTPRT']

ds_13a_h = ['ISTRRCH','ISTRNUM','ISTRCONN','ISTRTYPE','NSTRPTS',\
             'STRCD','STRCD2','STRCD3','STRINV','STRINV2','STRWID',\
             'STRWID2','STRLEN','STRMAN','STRVAL','ISTRDIR']
ds_13b_h = ['CSTROTYP','ISTRORCH','ISTROQCON','CSTROLO','CSTRCRIT',\
             'STRCRITC','STRRT','STRMAX','CSTRVAL']             

ds_13a_english = ['reach','str_num','conn_reach','type','flow_pts',\
                  'q_coeff_1','q_coeff_2','q_coeff_3','invert1','invert2'\
                  'width_up','width_dw','culvt_len','culvt_mann','init_val'\
                  'bidirect']
ds_13b_english = ['operate_typ','cntl_reach','cntl_reach2','grt_or_les','start_at',\
                  'stop_at','op_rate','max','timeseries']                  

ds_13a_fmt = ['10d','10d','10d','10d','10d',\
              '10.3e','10.3e','10.3e','10.3e','10.3e','10.3e',\
              '10.3e','10.3e','10.3e','10.3e','10d']

ds_13b_fmt = ['10','10d','10d','10','10',\
              '10.3e','10.3e','10.3e','10']   

def write_profile(profile_name,profile,header):
    #--write the xsec profile to the SWR format - 
    #--add the num_pts,X,Y,and area to the header
    if len(profile) < 1:
        print 'Error = zero length xsection:',profile_name
        raise ValueError
    f = open(profile_name,'w')
    f.write('#       XB      ELEVB '+header+'\n')
    for entry in profile:
        f.write('{0:10.3f} {1:10.3f}\n'.format(entry[0],entry[1]))
    f.close()
    return

def load_xsec(filename):
    #--first get the header(s)
    f = open(filename,'r')
    headers = []
    while True:
        line = f.readline().strip()
        if line.startswith('#'):
            headers.append(line)
        else:
            break
    f.close()
    xsec = np.loadtxt(filename,skiprows=len(headers))
    return headers,xsec        
        

def load_ds4b(filename):
    ds4b = {}
    f = open(filename,'r')
    for line in f:
        if not line.startswith('#'):
            raw = line.strip().split()
            reach = int(raw[0])
            nconn = int(raw[1])
            conn = []
            for i in range(nconn):
                conn.append(int(raw[2+i]))
            ds4b[reach] = conn
    f.close()
    return ds4b       


class ds_3():
    def __init__(self,solver=1,nouter=50,ninner=100,ibt=10,tols=1.0e-3,tolr=1.0+3,tola=0.1,dampss=1.0,damptr=1.0,iprswr=0,mutswr=0,ipc=4,nlevels=7,droptol=1.0e-3,ibtprt=-1):
        self.solver = int(solver)
        self.nouter = int(nouter)
        self.ninner = int(ninner)
        self.ibt = int(ibt)
        self.tols = float(tols)
        self.tolr = float(tolr)
        self.tola = float(tola)
        self.dampss = float(dampss)
        self.damptr = float(damptr)
        self.iprswr = int(iprswr)
        self.mutswr = int(mutswr)
        self.ipc = int(ipc)
        self.nlevels = int(nlevels)
        self.droptol = float(droptol)
        self.ibtprt = int(ibtprt)
    
    def write(self,f,fmti=' {0:9.0f}',fmtf=' {0:9.3G}'):
        f.write('# DATASET 3 - SOLVER PARAMETERS\n')
        for h in ds_3_h:
            f.write(h.rjust(10))
        f.write('\n')
        f.write(fmti.format(self.solver))
        f.write(fmti.format(self.nouter))
        f.write(fmti.format(self.ninner))
        f.write(fmti.format(self.ibt))
        f.write(fmtf.format(self.tols))
        f.write(fmtf.format(self.tola))
        f.write(fmtf.format(self.tolr))
        f.write(fmtf.format(self.dampss))
        f.write(fmtf.format(self.damptr))
        f.write(fmti.format(self.iprswr))
        f.write(fmti.format(self.mutswr))
        f.write(fmti.format(self.ipc))
        f.write(fmti.format(self.nlevels))
        f.write(fmtf.format(self.droptol))
        f.write(fmti.format(self.ibtprt))
        f.write('\n\n')




class ds_2():
    def __init__(self,dlenconv=3.281,timeconv=86400.0,rtini=0.0,rtmin=0.0,rtmax=0.0,rtprn=0.0,tmult=1.0,nmult=1,dmingrad=1.0e-12,dmindepth=1.0e-3,dmaxrai=0.0,dmaxstg=0.0,dmaxinf=0.0):
        self.dlenconv = float(dlenconv)
        self.timeconv = float(timeconv)
        self.rtini = float(rtini)
        self.rtmin = float(rtmin)
        self.rtmax = float(rtmax)
        self.rtprn = float(rtprn)
        self.tmult = float(tmult)
        self.nmult = int(nmult)
        self.dmingrad = float(dmingrad)
        self.dmindepth = float(dmindepth)
        self.dmaxrai = float(dmaxrai)
        self.dmaxstg = float(dmaxstg)
        self.dmaxinf = float(dmaxinf)

    def write(self,f,fmti=' {0:9.0f}',fmtf=' {0:9.3G}'):
        f.write('# DATASET 2 - SOLUTION CONTROLS\n')
        for h in ds_2_h:
            f.write(h.rjust(10))
        f.write('\n')
        f.write(fmtf.format(self.dlenconv))
        f.write(fmtf.format(self.timeconv))
        f.write(fmtf.format(self.rtini))
        f.write(fmtf.format(self.rtmin))
        f.write(fmtf.format(self.rtmax))
        f.write(fmtf.format(self.rtprn))
        f.write(fmtf.format(self.tmult))
        f.write(fmti.format(self.nmult))
        f.write(fmtf.format(self.dmingrad))
        f.write(fmtf.format(self.dmindepth))
        f.write(fmtf.format(self.dmaxrai))
        f.write(fmtf.format(self.dmaxstg))
        f.write(fmtf.format(self.dmaxinf))
        f.write('\n\n')
        
           

class ds_1():
    def __init__(self,nreaches,iswronly=0,iswrcbc=0,iswrprgf=0,iswrpstg=0,iswrpqaq=0,iswrpqm=0,iswrpstr=0,iswrfrn=0,options=None):
        self.nreaches = int(nreaches)
        self.iswronly = int(iswronly)
        self.iswrcbc = int(iswrcbc)
        self.iswrprgf = int(iswrprgf)
        self.iswrpstg = int(iswrpstg)
        self.iswrpqaq = int(iswrpqaq)
        self.iswrpqm = int(iswrpqm)
        self.iswrpstr = int(iswrpstr)
        self.iswrfrn = int(iswrfrn)
        if options:
            self.options = options
            self.iswropt = 'SWROPTIONS'
    
    def add_2_namefile(self,modelname,fmti = ' {0:6.0f} '):        
        new_lines = []
        if self.iswrprgf < 0:
            new_lines.append('DATA(BINARY)'+fmti.format(-1*self.iswrprgf)+modelname+'.fls\n')
        if self.iswrprgf > 0:
            new_lines.append('DATA'+fmti.format(self.iswrprgf)+modelname+'.fls\n')        
        if self.iswrpstg < 0:
            new_lines.append('DATA(BINARY)'+fmti.format(-1*self.iswrpstg)+modelname+'.stg\n')
        if self.iswrpstg > 0:
            new_lines.append('DATA'+fmti.format(self.iswrpstg)+modelname+'.stg\n')
        if self.iswrpqaq < 0:
            new_lines.append('DATA(BINARY)'+fmti.format(-1*self.iswrpqaq)+modelname+'.aqx\n')
        if self.iswrpqaq > 0:
            new_lines.append('DATA'+fmti.format(self.iswrpqaq)+modelname+'.aqx\n')
        if self.iswrpqm < 0:
            new_lines.append('DATA(BINARY)'+fmti.format(-1*self.iswrpqm)+modelname+'.pqm\n')
        if self.iswrpqm > 0:
            new_lines.append('DATA'+fmti.format(self.iswrpqm)+modelname+'.pqm\n')
        if self.iswrpstr < 0:
            new_lines.append('DATA(BINARY)'+fmti.format(-1*self.iswrpstr)+modelname+'.str\n')
        if self.iswrpstr > 0:
            new_lines.append('DATA'+fmti.format(self.iswrpstr)+modelname+'.str\n')       
        namefile = modelname+'.nam'          
        f = open(namefile,'r')
        lines = []
        for line in f:
            lines.append(line)
        f.close()
        lines.insert(0,'# modified by swr generator on '+str(datetime.now())+'\n')
        lines.append('SWR 106 '+modelname+'.swr')
        for line in new_lines:
            lines.append(line)
        f = open(namefile,'w')
        for line in lines:
            f.write(line)
           




    def write(self,f_obj):
        self.write_1a(f_obj)
        if self.iswropt:
            self.write_1b(f_obj)
    
    def write_1a(self,f,fmti=' {0:9.0f}'):

        f.write('# DATASET 1A\n')
        line = ''
        for h in ds_1_h:
            line += h.rjust(10)
        f.write(line+'\n')
        f.write(fmti.format(self.nreaches))
        f.write(fmti.format(self.iswronly))
        f.write(fmti.format(self.iswrcbc))
        f.write(fmti.format(self.iswrprgf))
        f.write(fmti.format(self.iswrpstg))
        f.write(fmti.format(self.iswrpqaq))
        f.write(fmti.format(self.iswrpqm))
        f.write(fmti.format(self.iswrpstr))
        f.write(fmti.format(self.iswrfrn))
        if self.iswropt:
            f.write(' '+self.iswropt)
        f.write('\n\n')

    def write_1b(self,f):
        f.write('# DATASET 1B - SWR1 OPTIONS\n')
        for opt in self.options:
            f.write(opt+'\n')
        f.write('END\n\n')


class ds_13a():
    def __init__(self,filename):
        self.filename = filename
        self.structures = []                
    
    def load_structures(self):
        f = open(self.filename)
        structures = []
                
        while True:        
            s = {}
            comments = []
            while True:
                line = f.readline()
                if line == '':
                    break
                raw = line.strip().split()                
                if not raw[0].startswith('#') and line[0] != '#':                    
                    break
                else:
                    comments.extend(raw)
            if line == '':
                break               
            s['istrrch'] = int(raw[0])
            s['istrnum'] = int(raw[1])
            s['istrconn'] = int(raw[2])
            s['istrtype'] = int(raw[3])
                        
            if s['istrtype'] == 1:
                comments.extend(raw[4:])    
                while True:
                    line = f.readline()
                    raw = line.strip().split()
                    if not raw[0].startswith('#') and line[0] != '#':
                        break
                    else:
                        comments.extend(raw)                    
                s['cstrotyp'] = raw[0].upper()
                s['istrorch'] = int(raw[1])
                s['cstrolo'] = (raw[2])
                if 'TABDATA' in raw[3]:
                    s['cstrcrit'] = raw[3]
                else:
                    s['cstrcrit'] = float(raw[3])
                s['strmax'] = float(raw[4])
                try:
                    if 'TABDATA' in raw[5].upper():
                        s['cstrval'] = raw[5].upper()
                        comments.extend(raw[6:])                                                                                   
                    else:
                         comments.extend(raw[5:])                            
                except IndexError:
                    pass                                
            
            #--uncontrolled
            elif s['istrtype'] == 2:
                raise NotImplementedError('uncontrolled structure type not implemented')
                
            
            #--pump
            elif s['istrtype'] == 3:                
                s['strval'] = float(raw[4])
                comments.extend(raw[5:])                   
                while True:
                    line = f.readline() 
                    raw = line.strip().split()
                    if not raw[0].startswith('#') and line[0] != '#':
                        break
                    else:                         
                         comments.extend(raw)
                                                   
                s['cstrotyp'] = raw[0].upper()
                s['istrorch'] = int(raw[1])
                if s['cstrotyp'] == 'FLOW':
                    raise NotImplementedError('cstrotyp=FLOW not supported'+str(s))
                s['cstrolo'] = (raw[2])
                if 'TABDATA' in raw[3]:
                    s['cstrcrit'] = raw[3]
                else:
                    s['cstrcrit'] = float(raw[3])
                s['strcritc'] = float(raw[4])
                s['strrt'] = float(raw[5])
                s['strmax'] = float(raw[6])               
                try:
                    if 'TABDATA' in raw[7].upper():
                        s['cstrval'] = raw[7].upper()
                        comments.extend(raw[8:])                                               
                    else:
                        comments.extend(raw[7:])
                except IndexError:
                    pass                 
            
            #--stage-discharge
            elif s['istrtype'] == 4:
                s['nstrpts'] = int(raw[4])
                comments.extend(raw[5:])
                sd_pts = []
                for i in range(s['nstrpts']):
                    raw = f.readline().strip().split()
                    sd_pts.append([float(raw[0]),float(raw[1])])
            
            #--culvert
            elif s['istrtype'] == 5:
                s['strcd'] = float(raw[4])
                s['strcd2'] = float(raw[5])
                s['strinv'] = float(raw[6])
                s['strinv2'] = float(raw[7])
                s['strwid'] = float(raw[8])
                
                #--rectangular
                if s['strwid'] < 0:
                    s['strwid2'] = float(raw[9])
                    s['strlen'] = float(raw[10])
                    s['strman'] = float(raw[11])
                    s['istrdir'] = int(raw[12])
                    try:
                        comments.extend(raw[13:])
                    except IndexError:
                        pass
                #--circular
                else:
                    s['strlen'] = float(raw[9])
                    s['strman'] = float(raw[10])
                    s['istrdir'] = int(raw[11])
                    try:
                        comments.extend(raw[12:])
                    except IndexError:
                        pass
                        
            
            
            #--fixed crest weir
            elif s['istrtype'] == 6:                
                s['strcd'] = float(raw[4])
                s['strcd3'] = float(raw[5])
                s['strinv'] = float(raw[6])
                s['strwid'] = float(raw[7])
                s['strval'] = float(raw[8])
                s['istrdir'] = int(raw[9])
                try:
                    comments.extend(raw[10:])
                except IndexError:
                    pass                      
            
            #--fixed underflow                                                                            
            elif s['istrtype'] == 7:
                s['strcd'] = float(raw[4])
                s['strcd2'] = float(raw[5])
                s['strcd3'] = float(raw[6])
                s['strinv'] = float(raw[7])
                s['strwid'] = float(raw[8])
                s['strval'] = float(raw[9])                
                s['istrdir'] = int(raw[10])
                try:
                    comments.extend(raw[11:])
                except IndexError:
                    pass                   
                
            #--overflow
            elif s['istrtype'] == 8:
                s['strcd'] = float(raw[4])            
                s['strcd3'] = float(raw[5])
                s['strinv'] = float(raw[6])
                s['strwid'] = float(raw[7])
                s['strval'] = float(raw[8])
                s['istrdir'] = int(raw[9])
                try:
                    comments.extend(raw[10:])
                except IndexError:
                    pass
                while True:
                    line = f.readline() 
                    raw = line.strip().split()
                    if not raw[0].startswith('#') and line[0] != '#':
                        break
                    else:
                        comments.extend(raw)                    
                s['cstrotyp'] = raw[0].upper()
                s['istrorch'] = int(raw[1])
                if s['cstrotyp'] == 'FLOW':
                    raise SystemError, 'cstrotyp=FLOW not supported',s
                s['cstrolo'] = (raw[2])
                if 'TABDATA' in raw[3]:
                    s['cstrcrit'] = raw[3]
                else:
                    s['cstrcrit'] = float(raw[3])
                s['strcritc'] = float(raw[4])
                s['strrt'] = float(raw[5])
                s['strmax'] = float(raw[6])
                try:
                    if 'TABDATA' in raw[7].upper():
                        s['cstrval'] = raw[7].upper()
                        comments.extend(raw[8:])
                    else:
                        comments.extend(raw[7:])
                except IndexError:
                    pass                       
                                                
            
            #--underflow
            elif s['istrtype'] == 9:
                s['strcd'] = float(raw[4])            
                s['strcd2'] = float(raw[5])
                s['strcd3'] = float(raw[6])
                s['strinv'] = float(raw[7])
                s['strwid'] = float(raw[8])
                s['strval'] = float(raw[9])
                s['istrdir'] = int(raw[10])
                try:
                    comments.extend(raw[11:])
                except IndexError:
                    pass
                                       
                while True:
                    line = f.readline()   
                    raw = line.strip().split()
                    if not raw[0].startswith('#') and line[0] != '#':
                        break
                    else:
                        comments.extend(raw)                        
                                      
                s['cstrotyp'] = raw[0].upper()
                s['istrorch'] = int(raw[1])
                if s['cstrotyp'] == 'FLOW':
                    raise SystemError, 'cstrotyp=FLOW not supported',s
                s['cstrolo'] = (raw[2])
                if 'TABDATA' in raw[3]:
                    s['cstrcrit'] = raw[3]
                else:
                    s['cstrcrit'] = float(raw[3])
                s['strcritc'] = float(raw[4])
                s['strrt'] = float(raw[5])
                s['strmax'] = float(raw[6])
                try:
                    if 'TABDATA' in raw[7].upper():
                        s['cstrval'] = raw[7].upper()
                        comments.extend(raw[8:])
                    else:
                        comments.extend(raw[7:])
                except IndexError:
                    pass
            com = []
            for a in comments:
                if a not in ds_13a_h and a not in ds_13b_h:
                    #a_new = a.replace('#',' ')                
                    if a != '#':
                        #com.append(a_new)
                        com.append(a)
                
            s['comments'] = comments                                    
            structures.append(s)
            line = f.readline()
            if line == '':
                break
        self.structures = structures                                                                           
 
    def scale_offset(self,prop_name,scale,offset,istrtype=[1,2,3,4,5,6,7,8,9]):                
            
        if not isinstance(istrtype,list):
            istrtype = [istrtype]        
        for s in self.structures:            
            if prop_name.lower() in s.keys() and s['istrtype'] in istrtype:                                
                s[prop_name.lower()] = (s[prop_name.lower()]*scale) + offset                       
        return        

    def filt(self,istrtype):
        filtered = []
        istrrch = []
        nstruct = []
        for s in self.structures:
            if s['istrtype'] != istrtype:
                filtered.append(s)
                if s['istrrch'] in istrrch:
                    nstruct[istrrch.index(s['istrrch'])] += 1
                    filtered[-1]['istrnum'] = nstruct[istrrch.index(s['istrrch'])]
                else:
                    istrrch.append(s['istrrch'])
                    nstruct.append(1)
                    filtered[-1]['istrnum'] = 1
        
        #--now reset                         
        self.structures = filtered
                                        
                    
    def write_structures(self,filename,byreach=False):       
        f_out = open(filename,'w')       
        #--loop over each structure type - for organization
        c = 0
        if byreach:
            #--first setup a flag array
            done = []
            done_istrrch = []
            for s in self.structures:
                done.append(False)
                done_istrrch.append(s['istrrch'])
            
            #--now start the main loop
            while False in done:
                #--find the lowest numbered remaining reach
                min = 1.0e+32    
                min_idx = None
                for i,s in enumerate(self.structures):
                    if s['istrrch'] < min and done[i] is False:
                        min_idx = i
                        min = s['istrrch']
                
                #--now find all structures at this reach
                istrrch_idxs = []
                for i,s in enumerate(self.structures):
                    if s['istrrch'] == min:
                        istrrch_idxs.append(i)
                
                #--now write the structures
                for i in istrrch_idxs:
                    self.write_struct(self.structures[i],f_out)
                    done[i] = True
                    c += 1
                               
        else:
            for i in [1,2,3,4,5,6,7,8,9]:
                for s in self.structures:
                    if s['istrtype'] == i:                    
                        self.write_struct(s,f_out)               
                        c += 1
        f_out.close()                                                      
        print 'dataset 13a written for '+str(c)+' structures'
                             
    
    def write_struct(self,s,f_out,debug=False):
        f_out.write('#\n')
        if 'a_com' in s.keys():
                f_out.write('# '+' '.join(s['a_com'])+'\n')
        if 'b_com' in s.keys():
                    f_out.write('# '+' '.join(s['b_com'])+'\n')                   
        self.write_header(ds_13a_h,f_out)                   
        for h in ds_13a_h:
            if h.lower() in s.keys():
                fmt = ds_13a_fmt[ds_13a_h.index(h)]
                val = s[h.lower()]
                #print val,fmt 
                fmt_string = ' {0:>'+fmt+'}'                    
                f_out.write(fmt_string.format(val))
            else:
                f_out.write('           ')        
        f_out.write('\n')
        if s['istrtype'] in [1,3,8,9]:
            self.write_header(ds_13b_h,f_out)                       
            for h in ds_13b_h:
                if h.lower() in s.keys():
                    fmt = ds_13b_fmt[ds_13b_h.index(h)]
                    val = s[h.lower()]                        
                    fmt_string = ' {0:>'+fmt+'}'
                    #print fmt_string,val
                    f_out.write(fmt_string.format(val))
                else:
                    f_out.write('           ')                                                                
            f_out.write('\n')
        f_out.write('')                   
        
                    
    def write_header(self,header,f_out):
        f_out.write('#')
        f_out.write(header[0].rjust(10)+' ')
        for h in header[1:]:
            f_out.write(h.rjust(10)+' ')
        f_out.write('\n')
                                

    def op_2_weir(self):
        '''
        very crude conversion from operable structures
        to weirs.  pumps get a width equal to the average width
        of other weirs if avaiable, otherwise 10.0
        '''
        t_width = 0.0
        c = 0
        for s in self.structures:
            if s['istrtype'] == 6:
                t_width += s['strwid']
                c += 1
        if c == 0:
            pump_width = 10.0
        else:
            pump_width = t_width / c
                
        new_structures = []
        for s in (self.structures):
            if s['istrtype'] in [3,8,9]:                
                ss = {}
                ss['istrrch'] = s['istrrch']
                ss['istrnum'] = s['istrnum']
                ss['istrconn'] = s['istrconn']
                ss['istrtype'] = 6
                ss['strcd'] = 0.61
                ss['strcd3'] = 0.5
                if s['istrtype'] == 3:
                    ss['strwid'] = pump_width
                else:
                    ss['strwid'] = s['strwid']
                if s['cstrotyp'] == 'FLOW':
                    raise TypeError,'cstrotyp=FLOW not supported'
                try:
                    if 'TABDATA' in s['cstrcrit'] :
                        raise TypeError,'cannot convert TABDATA to strval'    
                except:
                    pass
                ss['strinv'] = s['cstrcrit']
                ss['strval'] = s['cstrcrit']
                ss['istrdir'] = 0 
                ss['a_com'] = s['a_com']                
                new_structures.append(ss)
        
        #--remove original op structures
        while True:        
            found = False
            for i,s in enumerate(self.structures):
                if s['istrtype'] in [3,8,9]:
                    self.structures.pop(i)
                    found = True
                    break
            if found is False:
                break
        self.structures.extend(new_structures)            
       
               
    def write_ds12(self,filename):
        ismodrch,nstruct = [],[]        
        for s in self.structures:
            
            if s['istrrch'] in ismodrch:
                nstruct[ismodrch.index(s['istrrch'])] += 1
            else:
                ismodrch.append(s['istrrch'])
                nstruct.append(1)
        c = 0                                
        f_out = open(filename,'w')
        f_out.write('#  ISMODRCH    NSTRUCT\n')                
        done = []
        for i in ismodrch:
            done.append(False)
        while False in done:    
            #--first find the next lowest numbered reach
            min = 1.0e+32
            min_idx = None
            for i,rch in enumerate(ismodrch):                
                if rch < min and done[i] is False:
                    min = rch
                    min_idx = i
             
            f_out.write('{0:10d} {1:10d}\n'.format(ismodrch[min_idx],nstruct[min_idx]))
            done[min_idx] = True            
            c += nstruct[min_idx]   
        #for i,n in zip(ismodrch,nstruct):
        #    c += n
        #    f_out.write('{0:10d} {1:10d}\n'.format(i,n))
        f_out.close()           
        print 'dataset 12 written for '+str(c)+' structures'
            
    def add_wcd3_2_weirs(self):
        for s in self.structures:
            if s['istrtype'] == 6 and 'strcd3' not in s.keys():
                s['strcd3'] = 0.5                   
                                    

class swr_timestep():
    def __init__(self,f_obj,reaches,rain_entries,evap_entries,lat_entries,igeonumr,igeo,sp_dates,datadir='.\\'):        
        '''sp_start is a list of datetimes marking the start of each stress period
        '''
        self.f_obj = f_obj
        self.reaches = reaches
        self.nreach = len(reaches)
        self.ds_5 = ds_5()
        self.ds_6 = ds_6(reaches,filename_prefix=datadir+'ds_6_')
        self.ds_7b = ds_7b(rain_entries)
        self.ds_8b = ds_8b(evap_entries)
        self.ds_10 = ds_10(igeonumr,filename_prefix=datadir+'ds_10_')
        self.ds_11 = ds_11(igeo,filename_prefix=datadir+'ds_11_')
        self.ds_14 = df_14(reaches,filename_prefix=datadir+'ds_14_')        
        self.sp_num = 1
        self.sp_dates = sp_dates        
                        
    def write_transient_sequence(self):                
        f_obj = self.f_obj
        for start in self.sp_dates:             
            #print 'stress period',self.sp_num,' date ',start
            self.ds_5.irdbnd,e6 = self.ds_6.get_entry(start)        
            
            self.ds_5.irdrai,e7b = self.ds_7b.get_entry(start)        
            
            self.ds_5.irdevp,e8b = self.ds_8b.get_entry(start) 
            
            self.ds_5.irdlin = 0 
            self.ds_5.irdstr = 0 
            self.ds_5.irdaux = 0                 
            
            irdgeo_10,e10 = self.ds_10.get_entry(start)
            irdgeo_11,e11 = self.ds_11.get_entry(start)
            if irdgeo_10 > 0 or irdgeo_11 > 0:
                self.ds_5.irdgeo = irdgeo_10
            else:
                self.ds_5.irdgeo = 0

            self.ds_5.irdstg,e14 = self.ds_14.get_entry(start)            
            
            #--write the entries for this stress period
            e5 = self.ds_5.get_entry(self.sp_num,start)            
            f_obj.write(e5)
            if self.ds_5.irdbnd != 0:
                f_obj.write(e6)                                           
            if self.ds_5.irdrai != 0:
                f_obj.write(e7b)              
            if self.ds_5.irdevp != 0:
                f_obj.write(e8b)
            if self.ds_5.irdlin != 0:
                raise NotImplementedError('latereal inflow not supported yet..')
            if self.ds_5.irdgeo != 0:               
                f_obj.write(e10)
                f_obj.write(e11)
            if self.ds_5.irdstg != 0:
                f_obj.write(e14)                       
            self.sp_num += 1                
        f_obj.close()
        return    

class df_14():
    def __init__(self,reaches,filename_prefix='df_14'):
        self.reaches = reaches
        self.filename_prefix = filename_prefix
        self.stage = []
    
    def get_stage(self,dt):
        '''gets a stage record
        '''
        reaches,vals = [],[]
        for r in self.reaches:
            if r.ibnd != 0 and r.isactive(dt):
                if r.stage_series is not None and dt in r.stage_series.index:
                    val = r.stage_series[dt]
                    #stage.append([r.reach,val])
                    vals.append(val)
                    reaches.append(r.reach)
                else:
                    raise Exception('active reach '+str(r.reach)+' has no entry on date'+str(dt))                    
        
        for r in self.reaches:
            if r.ibnd != 0 and r.isactive(dt) and r.reach not in reaches:            
                raise Exception('active reach '+str(r.reach)+' has no entry on date'+str(dt))                    
        return zip(reaches,vals)

    def get_entry(self,dt):
        '''gets a ds_14 entry
        might also write a new stage record file'''
        stage = self.get_stage(dt)
        if stage == self.stage:
            return 0,None
        else:
            print '  --stage change - ',dt
            fname = self.filename_prefix+dt.strftime('%Y%m%d')+'.dat'
            entry = '#DATASET 14 - IRDSTG\nOPEN/CLOSE  '+fname+'\n'
            self.stage = stage
            self.write(fname)            
            return len(stage),entry

            
    def write(self,fname):
        f = open(fname,'w')
        f.write('#  IRCHSTG     STAGE\n')
        for reach,stage in self.stage:
            f.write('{0:10.0f} {1:20.8E}\n'.format(reach,stage))
        f.close()
                       



class ds_6():
    def __init__(self,reaches,filename_prefix='ds_6_'):
        self.reaches = reaches
        self.filename_prefix = filename_prefix
        self.ibnd = []

    def get_ibnd(self,dt,val=-1):
        ibnd = []
        for r in self.reaches:
            if r.isactive(dt) and r.ibnd != 0:
                ibnd.append(val)
            else:
                ibnd.append(0)
        return ibnd
    
    def get_entry(self,dt):
        '''gets the current filename and also might write a new ds6 file
        '''
        
        #--get an ibnd for this dt
        ibnd = self.get_ibnd(dt)
        if self.ibnd == ibnd:            
            return 0,None

        else:
            print '  --ibnd change - ',dt
            fname = self.filename_prefix+dt.strftime('%Y%m%d')+'.dat'
            entry = '#DATASET 6 - IRDBND\nOPEN/CLOSE  '+fname+'\n'
            self.ibnd = ibnd
            self.write(fname)            
            return len(ibnd),entry

    def write(self,fname):
        
        f = open(fname,'w')
        f.write('#  IBNDRCH   ISWRBND\n')
        for r,ibnd in zip(self.reaches,self.ibnd):
            f.write('{0:10.0f}{1:10.0f}\n'.format(r.reach,ibnd))
        f.close()


class ds_10():
    def __init__(self,entries,filename_prefix='ds_10_'):
        '''entries should be dict keyed with datetimes
        '''
        self.entries = entries
        self.filename_prefix = filename_prefix
        self.header = '# IGMODRCH  IGEONUMR   GZSHIFT\n'
    
    def get_entry(self,dt):
        fname = self.filename_prefix+dt.strftime('%Y%m%d')+'.dat'
        #--if the datetime is not found, return the last datetime
        if dt not in self.entries.keys():
            return 0,None
        else:
            self.write(dt,fname) 
            nentries = len(self.entries[dt])           
            return nentries,'#DATASET 10 - IGEONUMR\nOPEN/CLOSE  ' + fname + '\n'

    def write(self,dt,filename):
        f_obj = open(filename,'w')
        f_obj.write(self.header)        
        data = self.entries[dt]
        for d in data:
            f_obj.write('{0:10.0f}{1:10.0f}{2:10.2f}\n'.format(d[0],d[1],d[2]))
        f_obj.close()


class ds_11():
    def __init__(self,entries,filename_prefix='ds_11_'):
        '''entries should be dict keyed with datetimes
        '''
        self.entries = entries
        self.filename_prefix = filename_prefix
        self.header = '#  IGEONUM  IGEOTYPE   IGCNDOP  GMANNING   NGEOPTS    GWIDTH    GBELEV   GSSLOPE      GCND       GLK    GCNDLN   GETEXTD\n'   
    def get_entry(self,dt):
        fname = self.filename_prefix+dt.strftime('%Y%m%d')+'.dat'
        #--if the datetime is not found, return the last datetime
        if dt not in self.entries.keys():
            return 0,None
        else:
            self.write(dt,fname)                        
            return 1,'#DATASET 11 - IGEONUM\nOPEN/CLOSE  ' + fname + '\n'

    def write(self,dt,filename):
        f_obj = open(filename,'w')
        f_obj.write(self.header)                
        for e in self.entries[dt]:
            f_obj.write(e)
        f_obj.close()



class ds_4a():
    def __init__(self,reaches):
        self.reaches = reaches
    
    def get_entry(self,filename='swr_ds4a.dat'):
        self.write(filename)
        return '#DATASET 4A - REACH INFORMTAION\nOPEN/CLOSE  '+filename

    def write(self,filename):        
        f_obj = open(filename,'w')
        f_obj.write('#                                        LAY        ROW        COL\n')
        f_obj.write('#    IRCH4A IROUTETYPE     IRGNUM       KRCH       IRCH       JRCH           RLEN\n')
        for r in self.reaches:            
            f_obj.write(' {0:10.0f} {1:10.0f} {2:10.0f} {3:10.0f} {4:10.0f} {5:10.0f} {6:15.6e}\n' \
               .format(r.reach,r.iroute,r.reachgroup,1,r.row,r.column,r.length))    


class ds_4b():
    def __init__(self,reaches):
        self.reaches = reaches    

    def get_entry(self,filename='swr_ds4b.dat'):
        self.write(filename)
        return '#DATASET 4B - CONNECTIVITY DATA\nOPEN/CLOSE  '+filename

    def write(self,filename):              
        f_obj = open(filename,'w')
        f_obj.write('#    IRCH4B      NCONN      ICONN(1)...ICONN(NCONN)\n')
        for r in self.reaches:
            f_obj.write(' {0:10.0f} {1:10.0f} '.format(r.reach,r.nconn))
            for c in r.conn:
                f_obj.write(' {0:10.0f}'.format(c))           
            f_obj.write('\n')

    
class ds_5():
    def __init__(self):                                
        self.itmp,self.irdbnd,self.irdrai = 1,1,1
        self.irdevp,self.irdlin,self.irdgeo = 1,1,1
        self.irdstr,self.irdstg,self.iptflg,self.irdaux = 1,1,0,0
        self.header = '#   ITMP  IRDBND  IRDRAI  IRDEVP  IRDLIN  IRDGEO  IRDSTR  IRDSTG  IPTFLG  IRDAUX\n'
            
    def get_entry(self,sp_num,dt):
        entry = '#\n# -- Stress Period ' + str(sp_num) +  '  Date ' + dt.strftime('%Y%m%d') + '\n'
        entry += self.header
        entry += '{0:8.0f}{1:8.0f}{2:8.0f}{3:8.0f}{4:8.0f}{5:8.0f}{6:8.0f}{7:8.0f}{8:8.0f}{9:8.0f}\n'\
            .format(self.itmp,self.irdbnd,self.irdrai,self.irdevp,self.irdlin,self.irdgeo,self.irdstr,self.irdstg,self.iptflg,self.irdaux)
        return entry





                                     
class ds_7b():
    def __init__(self,entries):
        '''entries should be dict keyed with datetimes
        setup for 2-D arrays only
        '''
        self.entries = entries
    
    def get_entry(self,dt):        
        if dt not in self.entries.keys():
            return 0,None
        else:
            return -1,self.entries[dt]


class ds_8b():
    def __init__(self,entries):
        '''entries should be dict keyed with datetimes
        setup for 2-D arrays only
        '''
        self.entries = entries
    
    def get_entry(self,dt):        
        if dt not in self.entries.keys():
            return 0,None
        else:
            return -1,self.entries[dt]


class reach():
    def __init__(self,reach,iroute,reachgroup,row,column,length,conn,nconn,active_dt,ibnd=1):
        '''if ibnd == 0, the reach is permenatly disabled'''
        #--required attibutes
        self.reach = int(reach)
        self.iroute = int(iroute)
        self.reachgroup = int(reachgroup)
        self.row = int(row)
        self.column = int(column)
        self.length = float(length)
        self.nconn = int(nconn)
        if not isinstance(conn,list):
            conn = conn.strip().split()
        self.conn = conn
        if not isinstance(active_dt,datetime):
            raise TypeError('active_dt must be a datetime instance')
        self.active_dt = active_dt
        self.active = False   
        self.ibnd = int(ibnd)
        self.stage_series = None
    
    def __eq__(self,other):
        if isinstance(other,self.__class__) and self.__dict__ == other.__dict__:
            return True
        return False
    def set_stage_series(self,series):
        self.stage_series = series

    def isactive(self,dt):
        if self.active_dt <= dt:
            return True
        return False


def load_reaches_from_shape(shapename,idx_dict,active=False):
    
    
    reaches = []
    shp = shapefile.Reader(shapename)
    header = shp.dbfHeader()
    records = []
    for i in range(shp.numRecords):
        rec = shp.record(i)
        #for ii,item in enumerate(header):
        #    print ii,item[0],rec[ii]
        #for name,idx in idx_dict.iteritems():
        #    print name,idx,rec[idx]
        conn = rec[idx_dict['conn']].split()
        for i,c in enumerate(conn):
            conn[i] = int(c)
        yr = int(rec[idx_dict['active']])
        dt = datetime(year=yr,month=1,day=1)        
        # def __init__(self,reach,iroute,reachgroup,row,column,length,conn,nconn,active_dt):
        r = reach(rec[idx_dict['reach']],rec[idx_dict['iroute']],rec[idx_dict['reachgroup']],rec[idx_dict['row']],rec[idx_dict['column']],rec[idx_dict['length']],conn,rec[idx_dict['nconn']],dt,ibnd=rec[idx_dict['ibnd']])
        reaches.append(r)
        records.append(rec)
    return reaches,records           
