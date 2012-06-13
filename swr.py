
import numpy as np

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
           

class ds_13a():
    def __init__(self,filename):
        self.filename = filename
                        
    
    def load_structures(self):
        f = open(self.filename)
        structures = []
        #header_lines = []
        #while True:
        #    line = f.readline()
        #    if line.startswith('#'):
        #        header_lines.append(line)
        #    else:
        #        break
        
        while True:        
            s = {}
            a_com = []
            while True:
                line = f.readline()
                if line == '':
                    break
                raw = line.strip().split()                
                if not raw[0].startswith('#') and line[0] != '#':
                    #print raw[0]
                    break
                else:
                    a_com.extend(raw)
            if line == '':
                break    
            #
            print raw
            s['istrrch'] = int(raw[0])
            s['istrnum'] = int(raw[1])
            s['istrconn'] = int(raw[2])
            s['istrtype'] = int(raw[3])
            
            #--
            if s['istrtype'] == 1:
                a_com.extend(raw[4:])    
                while True:
                    line = f.readline()
                    raw = line.strip().split()
                    if not raw[0].startswith('#') and line[0] != '#':
                        break
                    else:
                        a_com.extend(raw)                    
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
                        a_com.extend(raw[6:])                                                                                   
                    else:
                         a_com.extend(raw[5:])                            
                except IndexError:
                    pass                                
            
            #--uncontrolled
            #elif s['istrtype'] == 2:
                
            
            #--pump
            elif s['istrtype'] == 3:
                #print raw
                s['strval'] = float(raw[4])
                a_com.extend(raw[5:])                   
                while True:
                    line = f.readline() 
                    raw = line.strip().split()
                    if not raw[0].startswith('#') and line[0] != '#':
                        break
                    else:                         
                         a_com.extend(raw)
                                                   
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
                        a_com.extend(raw[8:])                                               
                    else:
                        a_com.extend(raw[7:])
                except IndexError:
                    pass                 
            
            #--stage-discharge
            elif s['istrtype'] == 4:
                s['nstrpts'] = int(raw[4])
                a_com.extend(raw[5:])
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
                        a_com.extend(raw[13:])
                    except IndexError:
                        pass
                #--circular
                else:
                    s['strlen'] = float(raw[9])
                    s['strman'] = float(raw[10])
                    s['istrdir'] = int(raw[11])
                    try:
                        a_com.extend(raw[12:])
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
                    a_com.extend(raw[10:])
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
                    a_com.extend(raw[11:])
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
                    a_com.extend(raw[10:])
                except IndexError:
                    pass
                while True:
                    line = f.readline() 
                    raw = line.strip().split()
                    if not raw[0].startswith('#') and line[0] != '#':
                        break
                    else:
                        a_com.extend(raw)                    
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
                        a_com.extend(raw[8:])
                    else:
                        a_com.extend(raw[7:])
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
                    a_com.extend(raw[11:])
                except IndexError:
                    pass
                                       
                while True:
                    line = f.readline()   
                    raw = line.strip().split()
                    if not raw[0].startswith('#') and line[0] != '#':
                        break
                    else:
                        a_com.extend(raw)                        
                                      
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
                        a_com.extend(raw[8:])
                    else:
                        a_com.extend(raw[7:])
                except IndexError:
                    pass
            com = []
            for a in a_com:
                if a not in ds_13a_h and a not in ds_13b_h:
                    #a_new = a.replace('#',' ')                
                    if a != '#':
                        #com.append(a_new)
                        com.append(a)
                
            s['a_com'] = com                                    
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
                                    

