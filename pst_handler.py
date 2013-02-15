import numpy as np
import pandas
'''tries to do all lower case for strings
'''

S = str
I = np.int
F = np.float
FMT = {I:'{0:10.0f} ',S:'{0:20s} ',F:'{0:15.7G} '}

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







class entry():
    def __init__(self,value=None,dtype=None,required=True,name=None):                
        self.__value = value
        if dtype == None:
            dtype = type(value)
        self.dtype = dtype
        self.name = name
        self.required = required
        
    @property
    def value(self):
        return self.__value

    @property
    def string(self):
        return FMT[self.dtype].format(self.__value)

    def __eq__(self,other):   
        if self.dtype == S:
            if self.__value.lower() == other.lower():
                return True
            else:
                return False     
        elif self.__value == other:
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
                if self.required:
                    raise Exception('unable to cast '+str(value)+' to type '+str(self.dtype)+' for entry '+str(self.name))
                else:
                    print 'Warning - unable to cast '+str(value)+' to type '+str(self.dtype)+' for non-required entry '+str(self.name)
        elif self.dtype == F:
            try:
                self.__value = np.float(value)
            except:
                if self.required:
                    raise Exception('unable to cast '+str(value)+' to type '+str(self.dtype)+' for entry '+str(self.name))
                else:
                    print 'Warning - unable to cast '+str(value)+' to type '+str(self.dtype)+' for non-required entry '+str(self.name)
        elif self.dtype == S:
            try:                
                self.__value = str(value).lower()
            except:
                if self.required:
                    raise Exception('unable to cast '+str(value)+' to type '+str(self.dtype)+' for entry '+str(self.name))
                else:
                    print 'Warning - unable to cast '+str(value)+' to type '+str(self.dtype)+' for non-required entry '+str(self.name)
        else:
            raise Exception('unsupported dtype: '+str(self.dtype))

                                              

class pst():
    def __init__(self,filename=None):
        self.DTYPES = DTYPES
        self.dtypes_2_lower()
        self.build_pst_structure()
        if filename:
            self.read_pst(filename)
    def dtypes_2_lower(self):
        dts = {}
        for key,value in self.DTYPES.iteritems():
            dts[key.lower()] = value
        self.DTYPES = dts


    #--override set so that direct assignment can be used for the entry attributes
    def __setattr__(self,name,value):
        try:
            attr = getattr(self,name)  
        except:
            self.__dict__[name] = value
            return          
        if isinstance(attr,entry):
            attr.set_value(value)
            self.__dict__[name] = attr
            pass
        else:
            self.__dict__[name] = value
               

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
        secrtion_required = {}
        section_order = []
        #--parse and build
        lines = PST_BASE.split('\n')
        l_count = 0
        last = 'pcf'
        entries = {}
        for line in lines:        
            line = line.strip().lower()
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
                        #if r.endswith(']'):
                        #    rq = True                    
                        r = r.replace('[','')
                        r = r.replace(']','')
                        #--this is the only place in the whole damn class that needs upper
                        if r in self.DTYPES.keys():
                            e = entry(None,dtype=self.DTYPES[r],name=r,required=rq)
                            entries[r] = e
                        else:
                            #  'warning',r,'not found in DTYPES'
                            pass
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
            line = f.readline().strip().lower()
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
            line = f.readline().strip().lower()
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
            if key in self.DTYPES and self.DTYPES[key] in [I,F]:
                df[key] = df[key].astype(self.DTYPES[key])        
        #--pop off null columns
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
        l_count,p_count = 1,1
        while True:
            line = f.readline().strip().lower()
            if line == '':
                break
            #--if this is the start of a section     
            elif '*' in line:            
                self.needed[line] = True
                p_count += 1
                rep = self.structure[line]['repeatable']
                if not rep:
                    self.read_pst_section(f,line)
                else:
                    df = self.read_pst_repeatable_section(f,line)                                                                                                                  
        self.__to_attrs()
        f.close()

    def __to_attrs(self):
        for key,record in self.sections.iteritems():
            attr_base = self.control_2_attr(key)
            setattr(self,attr_base,record)
            for ename,entry in record.iteritems():                               
                #attr = attr_base+'.'+ename.lower()
                attr = ename.lower()
                setattr(self,attr,entry)
        self.sections = None


    def write_pst(self,filename):
        f = open(filename,'w',0)
        f.write('pcf\n')
        for sname in self.section_order:
            if self.needed[sname] and getattr(self,self.control_2_attr(sname)) is not None:
                f.write(sname+'\n')
                structure = self.structure[sname]
                #section = getattr(self,self.control_2_attr(sname))
                #--iterate over each line
                rep = structure['repeatable']
                if not rep:
                    for plist,rqlist in zip(structure['parameters'],structure['required']):
                        for p in plist:
                            if hasattr(self,p):
                                attr = getattr(self,p)
                                if attr.value != None:
                                    f.write(attr.string)  
                        f.write('\n')    
                else:
                    attr = getattr(self,self.control_2_attr(sname))
                    keys = attr.keys()
                    dtypes,fmts = {},{}
                    for k in keys:
                        dtypes[k] = self.DTYPES[k]
                        fmts[k] = FMT[self.DTYPES[k]]
                    for idx,rec in attr.iterrows():
                        for plist,rqlist in zip(structure['parameters'],structure['required']):
                            for p in plist:
                                if p in keys:
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

    def remove_from_df_attr(self,attr_name,col_name,needed_list):
        attr = getattr(self,attr_name)        
        sel = []
        for value in attr[col_name].values:
            if value not in needed_list:
                sel.append(False)
            else:
                sel.append(True)
        attr = attr[sel]
        setattr(self,attr_name,attr)
        return

    def compare_list_elements(self,list1,list2):
        for e1 in list1:
            if e1 not in list2:
                return False
        for e2 in list2:
            if e2 not in list1:
                return False
        return True

    def update(self,bottomup=True):
        self.update_parameter_info(bottomup)
        self.update_observation_info(bottomup)
        self.update_prior_info(bottomup)
    

    def parse_pi_equation(self,p_str):
        '''parses the pi equation string into pifacs,parnmes,pival
        '''
        operators = ['+','-','*','/']
        lhs,rhs = p_str.split('=')
        pival = float(rhs)        
        lhs_tokens = lhs.split()
        #--take steps of 3
        parnames,pifacs = [],[]
        for pifac,operator,raw_parnme in zip(lhs_tokens[0::3],lhs_tokens[1::3],lhs_tokens[2::3]):
            parnme = raw_parnme.replace(')','').replace('log(','').lower()
            pifac = float(pifac)
            parnames.append(parnme)
            pifacs.append(pifac)
        return {'parnme':parnames,'pifac':pifacs,'pival':pival}
        

    def reconcile_prior_2_pars(self):
        '''checks for missing parameter names in pi equations
        '''
        par_names = list(self.parameter_data.parnme)
        pi_equation_strings = list(self.prior_information.pi_equation)
        sel = []
        for pi_eq in pi_equation_strings:
            pars = self.parse_pi_equation(pi_eq)['parnme']
            missing = False
            for p in pars:
                if p not in par_names or self.parameter_data.partrans[self.parameter_data.parnme==p] in ['fixed','tied']:
                    missing = True 
                    break 
            if missing:
                sel.append(False)
            else:
                sel.append(True)
        self.prior_information = self.prior_information[sel]
        return
        
        



    def update_prior_info(self,bottomup):
        if self.prior_information is not None:
            unique_groups = list(self.observation_data['obgnme'].unique())        
            unique_groups.extend(list(self.prior_information['obgnme'].unique()))
            existing_groups = self.observation_groups['obgnme'].values
            same = self.compare_list_elements(unique_groups,existing_groups)
            if not same:
                if not bottomup:
                    self.remove_from_df_attr('prior_information','obgnme',existing_groups)
                else:
                    self.remove_from_df_attr('observation_groups','obgnme',unique_groups)
            self.nprior.set_value(self.prior_information.shape[0])
        else:
            unique_groups = list(self.observation_data['obgnme'].unique())   
            self.remove_from_df_attr('observation_groups','obgnme',unique_groups)     
            self.nprior.set_value(0)
        nobsgp = self.observation_groups.shape[0]
        self.nobsgp.set_value(nobsgp)
        


    def update_observation_info(self,bottomup):
        unique_groups = list(self.observation_data['obgnme'].unique())
        #if self.prior_information is not None:
        try:
            unique_groups.extend(list(self.prior_information['obgnme'].unique()))
        except:
            pass
        existing_groups = self.observation_groups['obgnme'].values
        same = self.compare_list_elements(unique_groups,existing_groups)
        if not same:
            #--reconcile obs data groups against obs groups
            if not bottomup:
                self.remove_from_df_attr('observation_data','obgnme',existing_groups)  
            #--reconcile obs groups against observation data groups
            else:
                self.remove_from_df_attr('observation_groups','obgnme',unique_groups)
        #--if there are any observation data with an unknown group

        self.nobs.set_value(self.observation_data.shape[0])
        try:
            self.update_prior_info(bottomup)
        except:
            pass
        nobsgp = self.observation_groups.shape[0]
        self.nobsgp.set_value(nobsgp)

       
    def update_parameter_info(self,bottomup):
        unique_groups = self.parameter_data['pargp'].unique()
        existing_groups = self.parameter_groups['pargpnme'].values
        same = self.compare_list_elements(unique_groups,existing_groups)
        if not same:
            if not bottomup:
                self.remove_from_df_attr('parameter_data','pargp',existing_groups)    
            else:
                self.remove_from_df_attr('parameter_groups','pargpnme',unique_groups)
        self.npar.set_value(self.parameter_data.shape[0])
        self.npargp.set_value(self.parameter_groups.shape[0])
        self.maxsing.set_value(self.parameter_data.shape[0])
                    

