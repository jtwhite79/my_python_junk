import numpy as np
import pandas






class entry():
    def __init__(self,value=None,dtype=None,required=True,name=None):                
        self.__value = value
        if dtype == None:
            dtype = type(value)
        self.dtype = dtype
        self.name = name
        self.required = required
        #self.acceptable_dtype = [np.int,np.float32,str]
        #if dtype not in self.acceptable_dtypes:
        #    raise Exception('unacceptable dtype: '+str(dtype)+' for entry: '+str(name))
       
    @property
    def value(self):
        return self.__value

    @property
    def string(self):
        #if self.dtype == I:
        #    return I.format(self.__value)
        #elif self.dtype == F:
        #    return F_FMT.format(self.__value)
        #else:
        #    return S_FMT.format(self.__value)        
        return FMT[self.dtype].format(self.__value)

    def __eq__(self,other):        
        if self.__value == other:
            return True
        else:
            return False
    def __repr__(self):
        return str(self.name) + ': '+self.string    
 
    def set_value(self,value):
        if self.dtype == I:
            try:
                self.__value = np.int(value)
            except:
                raise Exception('unable to cast '+str(value)+' to type '+str(self.dtype)+' for entry '+str(self.name))
        elif self.dtype == F:
            try:
                self.__value = np.float(value)
            except:
                raise Exception('unable to cast '+str(value)+' to type '+str(self.dtype)+' for entry '+str(self.name))
        elif self.dtype == S:
            try:
                self.__value = str(value)
            except:
                raise Exception('unable to cast '+str(value)+' to type '+str(self.dtype)+' for entry '+str(self.name))
        else:
            raise Exception('unsupported dtype: '+str(self.dtype))
                                              

class pst():
    def __init__(self):
        self.build_pst_structure()

#----------------------------------------------------------
#--IO stuff
#----------------------------------------------------------   
    def build_pst_structure(self):       
        '''load the text pst structure
        into nested lists for output structure
        Also builds the required list by looking
        for '[' and ']' and builds the repeatable entry list
        by keying on the '(' and ')'

        special treatment of the tied parameter mess

        '''        
        #--nested list of parameter names
        pst_list = []
        #--nested list of bools for required pars
        req_list = []                       
        #--list of bools for repeatable entries (pars,obs,etc)
        #--one entry for each section    
        rep = False
        section_dict = {}
        section_entries = {}
        section_order = []
        #--parse and build
        lines = PST_BASE.split('\n')
        l_count = 0
        last = 'pcf'
        entries = {}
        for line in lines:        
            line = line.strip()
            #--if this is a control marker, then set req as False
            if line.startswith('*'):                           
                section_dict[last] = {'parameters':pst_list,'required':req_list,'repeatable':rep}
                section_entries[last] = entries
                section_order.append(line)
                last = line 
                pst_list = []
                req_list = []
                entries = {}
                rep = False
            #--otherwise
            else:
                
                if '(' not in line:
                    pst_list.append([])
                    req_list.append([])
                    rep = False
                    raw = line.strip().split()              
                    rq = True
                    for i,r in enumerate(raw):
                        if r.startswith('['):
                            rq = False                                    
                        req_list[-1].append(rq)
                        if r.endswith(']'):
                            rq = True                    
                        r = r.replace('[','')
                        r = r.replace(']','')
                        if r in DTYPES.keys():
                            e = entry(None,dtype=DTYPES[r],name=r.lower())
                            entries[r] = e
                        else:
                            print 'warning',r,'not found in DTYPES'
                        pst_list[-1].append(r)                    
                else:
                    rep = True                                                                        
            l_count += 1 
            
        
        section_dict[last] = {'parameters':pst_list,'required':req_list,'repeatable':rep}
        section_entries[last] = entries                         
        #--set a needed flag for each section
        section_needed = {}
        for key in section_dict.keys():
            section_needed[key] = False
        self.structure = section_dict
        self.needed = section_needed
        self.sections = section_entries
        self.section_order = section_order
        return

    def parse_line(self,line,section_marker):
        if 'PRIOR' in section_marker.upper():
            raw = line.strip().split()
            new_line = [raw[0],' '.join(raw[1:-2]),raw[-2],raw[-1]]
            return new_line
        else:
            return line.strip().split()

    def read_pst_section(self,f,section_marker):
        '''read a non-repeatable section - set the entry instance values
        '''
        l_count = 0
        params = self.structure[section_marker]['parameters']
        while True:
            line_start_pointer = f.tell()
            line = f.readline().strip()
            if line == '':
                break
            elif line.startswith('*'):
                f.seek(line_start_pointer)
                return       
            raw = self.parse_line(line,section_marker)
            for r,p in zip(raw,params[l_count]):                                  
               self.sections[section_marker][p].set_value(r)              
            l_count += 1                                                
                             
    def read_pst_repeatable_section(self,f,section_marker):
        '''read a repeatable section - build pandas dataframes
        '''
        #--create a dict structure to store the entries
        params = self.structure[section_marker]['parameters'][0]        
        records = {}
        for key in params:
            records[key] = []
        while True:
            line_start_pointer = f.tell()
            line = f.readline().strip()
            if line == '':
                break
            elif line.startswith('*'):
                f.seek(line_start_pointer)
                break  
            raw = self.parse_line(line,section_marker)
            for p,r in zip(params,raw):
                records[p].append(r)

        #--set the missing entries as NaNs 
        mx = 0
        for key,rec in records.iteritems():
            if len(rec) == 0:
                records[key] = np.NaN                
            if mx < len(rec):
                mx = len(rec)
        if mx == 0 :
            raise Exception('zero-length repeatable section: '+str(section_marker))
        elif mx == 1:
            index = [0]
            df = pandas.DataFrame(records,index=index)
        else:
            df = pandas.DataFrame(records) 
                      
        #--set the numeric dataframe column types
        for key in df.keys():
            if key in DTYPES and DTYPES[key] in [I,F]:
                df[key] = df[key].astype(DTYPES[key])        
        for key,series in df.iteritems():
            if len(series.dropna()) == 0:
                df.pop(key)
        self.sections[section_marker] = df
        return
                
    def read_pst(self,filename):
        '''read an existing PST file
        '''
        f = open(filename,'r')
        #--read the pcf line
        f.readline()
         #--counters for position in the file and in the pst_list,rep_list
        l_count,p_count = 1,1
        while True:
            line = f.readline().strip()
            if line == '':
                break
            #--if this is the start of a section     
            elif '*' in line:            
                self.needed[line] = True
                p_count += 1
                #p_list = self.section_structure[line]['parameters']
                #rq_list = self.section_structure[line]['required']
                rep = self.structure[line]['repeatable']
                if not rep:
                    self.read_pst_section(f,line)
                else:
                    df = self.read_pst_repeatable_section(f,line)                                                                                                                  
        self.__to_attrs()
        f.close()

    def __to_attrs(self):
        for key,record in self.sections.iteritems():
            #attr_base = self.control_2_attr(key)
            #print attr_base
            #setattr(self,attr_base,record)
            for ename,entry in record.iteritems():                               
                #attr = attr_base+'.'+ename.lower()
                attr = ename.lower()
                print attr
                setattr(self,attr,entry)
        self.sections = None




    def write_pst(self,filename):
        f = open(filename,'w',0)
        f.write('pcf\n')
        for sname in self.section_order:
            if self.needed[sname]:
                f.write(sname+'\n')
                structure = self.structure[sname]
                section = getattr(self,self.control_2_attr(sname))
                #--iterate over each line
                rep = structure['repeatable']
                if not rep:
                    for plist,rqlist in zip(structure['parameters'],structure['required']):
                        for p in plist:
                            if section[p].value != None:
                                f.write(section[p].string)  
                        f.write('\n')    
                else:
                    keys = section.keys()
                    dtypes,fmts = {},{}
                    for k in keys:
                        dtypes[k] = DTYPES[k]
                        fmts[k] = FMT[DTYPES[k]]
                    for idx,rec in section.iterrows():
                        for plist,rqlist in zip(structure['parameters'],structure['required']):
                            for p in plist:
                                if p in keys:
                                    #print rec[p],fmts[p].format(rec[p])
                                    #pass
                                    f.write(fmts[p].format(rec[p]))
                        f.write('\n')
        f.close()

    def control_2_attr(self,cstring):
        return cstring.replace('*','').strip().replace(' ','_')
    def attr_2_control(self,astring):
        return '* '+astring.replace('_',' ')

#----------------------------------------------------------
#--some very basic logic
#----------------------------------------------------------
    def update(self):
        self.update_parameter_info()
        self.update_observation_info()
        self.update_prior_info()

    def update_parameter_info(self):
        npar = self.parameter_data.shape[0]
        unique_groups = self.parameter_data['pargrpnme'].unique()

        


#--global stuff

S = str
I = np.int
F = np.float
FMT = {I:'{0:10.0f} ',S:'{0:20s} ',F:'{0:15.7G} '}
#NULL = {I:np.NaN,S:None,F:np.NaN}


DTYPES = {'RSTFLE':S,'PESTMODE':S,'NPAR':I,'NOBS':I,'NPARGP':I,'NPRIOR':I,'NOBSGP':I,'MAXCOMPDIM':I,\
                    'NTPLFLE':I,'NINSFLE':I,'PRECIS':S,'DPOINT':S,'NUMCOM':I,'JACFILE':I,'MESSFILE':I,'OBSREREF':S,\
                    'RLAMBDA1':F,'RLAMFAC':F,'PHIRATSUF':F,'PHIREDLAM':F,'NUMLAM':I,'JACUPDATE':I,'LAMFORGIVE':S,\
                    'RELPARMAX':F,'FACPARMAX':F,'FACORIG':F,'IBOUNDSTICK':F,'UPVECBEND':F,'ABSPARMAX':F,\
                    'PHIREDSWH':F,'NOPTSWITCH':I,'SPLITSWH':F,'DOAUI':S,'DOSENREUSE':S,\
                    'NOPTMAX':I,'PHIREDSTP':F,'NPHISTP':I,'NPHINORED':I,'RELPARSTP':F,'NRELPAR':I,'PHISTOPTHRESH':F,\
                    'LASTRUN':I,'PHIABANDON':S,'ICOV':I,'ICOR':I,'IEIG':I,'IRES':I,'JCOSAVE':S,'VERBOSEREC':S,'JCOSAVEITN':S,\
                    'REISAVEITN':S,'PARSAVEITN':S,'PARSAVERUN':S,'SVDMODE':I,'MAXSING':I,'EIGTHRESH':F,'EIGWRITE':I,\
                    'PARGPNME':S,'INCTYP':S,'DERINC':F,'DERINCLB':F,'FORCEN':S,'DERINCMUL':F,'DERMTHD':S,\
                    'SPLITTHRESH':F,'SPLITRELDIFF':F,'SPLITACTION':S,'PARNME':S,'PARTRANS':S,'PARCHGLIM':S,'PARVAL1':F,\
                    'PARLBND':F,'PARUBND':F,'PARGP':S,'SCALE':F,'OFFSET':F,'DERCOM':I,'OBSNME':S,'OBSVAL':F,'WEIGHT':F,'OBGNME':S,\
                    'PILBL':S,'PI_EQUATION':S,'WEIGHT':F,'OBGNME':S,'PHIMLIM':F,'PHIMACCEPT':F,'FRACPHIM':F,'MEMSAVE':S,'WFINIT':F,'WFMIN':F,'WFMAX':F,'LINREG':S,'REGCONTINUE':S,\
                    'WFFAC':F,'WFTOL':F,'IREGADJ':I,'NOPTREGADJ':I,'REGWEIGHTRAT':F,'REGSINGTHRESH':F,'COMLINE':S,\
                    'MODEL_INTERFACE_FILE':S,'MODEL_FILE':S}


PST_BASE = '''pcf
* control data
RSTFLE PESTMODE
NPAR NOBS NPARGP NPRIOR NOBSGP [MAXCOMPDIM]
NTPLFLE NINSFLE PRECIS DPOINT [NUMCOM JACFILE MESSFILE] [OBSREREF]
RLAMBDA1 RLAMFAC PHIRATSUF PHIREDLAM NUMLAM [JACUPDATE] [LAMFORGIVE]
RELPARMAX FACPARMAX FACORIG [IBOUNDSTICK UPVECBEND] [ABSPARMAX]
PHIREDSWH [NOPTSWITCH] [SPLITSWH] [DOAUI] [DOSENREUSE]
NOPTMAX PHIREDSTP NPHISTP NPHINORED RELPARSTP NRELPAR [PHISTOPTHRESH] [LASTRUN] [PHIABANDON]
ICOV ICOR IEIG [IRES] [JCOSAVE] [VERBOSEREC] [JCOSAVEITN] [REISAVEITN] [PARSAVEITN] [PARSAVERUN]
* automatic user intervention
MAXAUI AUISTARTOPT NOAUIPHIRAT AUIRESTITN
AUISENSRAT AUIHOLDMAXCHG AUINUMFREE
AUIPHIRATSUF AUIPHIRATACCEPT NAUINOACCEPT
* singular value decomposition
SVDMODE
MAXSING EIGTHRESH
EIGWRITE
* lsqr
LSQRMODE
LSQR_ATOL LSQR_BTOL LSQR_CONLIM LSQR_ITNLIM
LSQRWRITE
* svd assist
BASEPESTFILE
BASEJACFILE
SVDA_MULBPA SVDA_SCALADJ SVDA_EXTSUPER SVDA_SUPDERCALC SVDA_PAR_EXCL
* sensitivity reuse
SENRELTHRESH SENMAXREUSE
SENALLCALCINT SENPREDWEIGHT SENPIEXCLUDE
* parameter groups
PARGPNME INCTYP DERINC DERINCLB FORCEN DERINCMUL DERMTHD [SPLITTHRESH SPLITRELDIFF SPLITACTION]
(one such line for each of NPARGP parameter groups)
* parameter data
PARNME PARTRANS PARCHGLIM PARVAL1 PARLBND PARUBND PARGP SCALE OFFSET DERCOM
(one such line for each of NPAR parameters)
PARNME PARTIED
(one such line for each tied parameter)
* observation groups
OBGNME [GTARG] [COVFLE]
(one such line for each of NOBSGP observation group)
* observation data
OBSNME OBSVAL WEIGHT OBGNME
(one such line for each of NOBS observations)
* derivatives command line
DERCOMLINE
EXTDERFLE
* model command line
COMLINE
(one such line for each of NUMCOM command lines)
* model input/output
MODEL_INTERFACE_FILE MODEL_FILE
(one such line for each of NTPLFLE template files)
* prior information
PILBL PI_EQUATION WEIGHT OBGNME
(one such line for each of NPRIOR articles of prior information)
* predictive analysis
NPREDMAXMIN [PREDNOISE]
PD0 PD1 PD2
ABSPREDLAM RELPREDLAM INITSCHFAC MULSCHFAC NSEARCH
ABSPREDSWH RELPREDSWH
NPREDNORED ABSPREDSTP RELPREDSTP NPREDSTP
* regularisation
PHIMLIM PHIMACCEPT [FRACPHIM] [MEMSAVE]
WFINIT WFMIN WFMAX [LINREG] [REGCONTINUE]
WFFAC WFTOL IREGADJ [NOPTREGADJ REGWEIGHTRAT [REGSINGTHRESH]]
* pareto
PARETO_OBSGROUP
PARETO_WTFAC_START PARETO_WTFAC_FIN NUM_WTFAC_INC
NUM_ITER_START NUM_ITER_GEN NUM_ITER_FIN
ALT_TERM
OBS_TERM ABOVE_OR_BELOW OBS_THRESH NUM_ITER_THRESH (only if ALT_TERM is non-zero)
NOBS_REPORT
OBS_REPORT_1 OBS_REPORT_2 OBS_REPORT_3.. (NOBS_REPORT items)'''