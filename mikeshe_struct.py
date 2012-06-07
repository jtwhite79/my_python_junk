import sys
import re

type_dict = {0:'Overflow',1:'Underflow',2:'Discharge',\
             3:'Radial_Gate',4:'Sluice_Formula'}

weir_dict = {0:'Broad_crested',1:'Special',2:'Formula_1',3:'Formula_2',4:'Formula_3'}
    
target_dict = {0:'h',1:'dh',2:'Q',3:'dQ',4:'abs(Q)',5:'Q_Structure',\
               6:'Sum_Q',7:'V',8:'Gate_level',9:'Concentration'}    
calc_mode_dict = {0:'Tabulated',1:'PID_operation',2:'Momentum_eqs',\
                  3:'Iterative_solution',4:'Fully_open',5:'Close',\
                  6:'Unchanged',7:'Change_with',8:'Set_equal_to'}  

control_dict = {0:'h',1:'dh',2:'Q',3:'dQ',4:'abs(Q)',5:'Q_Structure',6:'Sum_Q',\
                7:'V',8:'Gate_level',9:'Acc_vol',10:'Time',11:'Min_of_hour',\
                12:'Hr_of_day',13:'Day_of_week',14:'Day_of_month',15:'Mon_of_yr',\
                16:'Year',17:'Time_after_start',19:'Hups',20:'Hdws',33:'thisGate_dh',\
                35:'thisGate_level'}
                                  
target_dict =  {0:'h',1:'dh',2:'Q',3:'dQ',4:'abs(Q)',5:'Q_Structure',6:'Sum_Q',\
                7:'V',8:'Gate_level',10:'Hups',11:'Hdws'}   
                    
lo_type_dict = {0:'h',1:'dh',2:'Q',3:'dQ',5:'Q_structure',8:'Gate_level',\
                11:'Hour_of_day',15:'TSLGLC',17:'TS_Scalar',21:'Hups',\
                22:'Hdws',35:'thisGate_dh',38:'thisGate_TSLGLC'}                    

#lo_sign_dict = {0:'<',1:'<=',2:'>',3:'>=',4:'=',5:'<>'}  
#--simplified for SWR  
lo_sign_dict = {0:'LT',1:'LT',2:'GE',3:'GE',4:'='}

culvert_dict = {0:'Rectangular',1:'Circular',2:'Irregular',3:'Irregular',4:'Xsection_DB'}

def write_swr_dataset13_header(file_obj):
    file_obj.write('#   ISTRRCH    ISTRNUM   ISTRCONN   ISTRTYPE    NSTRPTS')
    file_obj.write('     STRWCD    STRWCD2     STRCD3     STRINV    STRINV2')
    file_obj.write('     STRWID    STRWID2     STRLEN     STRMAN     STRVAL')
    file_obj.write('    ISTRDIR\n')
    file_obj.write('#      CSTROTYP   ISTRORCH  ISTROQCON     CSTRLO   CSTRCRIT')
    file_obj.write('   STRCRITC     STRRT      STRMAX    CSTRVAL\n')
    return
                               

def load_culverts(file):
    cul_start = re.compile('\[culvert_data\]',re.IGNORECASE) 
    f = open(file,'r')

    culvert_list = []
    while True:
        line = f.readline()
        if line == '':
            f.close
            return culvert_list
        if cul_start.search(line) != None:
            this_culvert = culvert(f)
            culvert_list.append(this_culvert)

def load_weirs(file):
    str_start = re.compile('\[weir_data\]',re.IGNORECASE) 
    f = open(file,'r')

    weir_list = []
    while True:
        line = f.readline()
        #print line
        if line == '':
            f.close
            return weir_list
        if str_start.search(line) != None:
            this_weir = weir(f)
            weir_list.append(this_weir)
            
            
def load_structure(file):
    str_start = re.compile('\[control_str_data\]',re.IGNORECASE) 
    f = open(file,'r')

    str_list = [] 
    l_count = 0 
    
    while True:
        line = f.readline()
        l_count += 1
        if line == '':
            #print l_count
            f.close
            return str_list
        
        if str_start.search(line) != None:
            #print l_count
            this_str = structure(f)
            str_list.append(this_str) 
            #if str_list[-1].branch == 'Horsefarm':
            #    return str_list
            #break           


    
def read_2_key(key,file,stop=None):
    #print key
    k = re.compile(key,re.IGNORECASE)
    if stop != None:
     st = re.compile(stop,re.IGNORECASE)
    else:
     st = re.compile('BoLoGnA SaNdWiTcH')
    while True:
        line = file.readline()
        if st.search(line) != None:
            return None
        if k.search(line) != None:
            return line


def parse_line(line):
    raw = line.strip().split('=')[-1].split(',')
    return raw


def get_flow_dir(valve_reg):
        if valve_reg == 0:
            return 'both'
        elif valve_reg == 1:
            return 'neg'
        elif valve_reg == 2:
            return 'pos'
        elif valve_reg == 3:
            return None
        else:
            raise TypeError('unrecognized valve type: '+str(valve_reg))   


class structure():
    def __init__(self,file_obj):
        line = file_obj.readline()
        self.location_line = parse_line(line)
        self.branch = self.location_line[0].strip()[1:-1]
        self.chainage = float(self.location_line[1])
        self.id = self.location_line[2].strip()[1:-1]
        self.topo_id = self.location_line[3].strip()[1:-1]
        try:
            self.tag = self.location_line[3][1:-1]
        except:
            self.tag = ''
        self.set_attributes(file_obj)
        self.set_control_def(file_obj)
                   
    def set_control_def(self,file_obj):
        priority = []
        calc_mode = []
        cnt_type = []
        values = []
        cnt_pts = []
        cnt_strat = []
        targ_type = []
        lo = []
        line = read_2_key('\[logical_statement\]',file_obj,\
                          stop='EndSect  // control_str_data')
        stop_cnt_strat = re.compile('EndSect  // control_strategy',re.IGNORECASE)                 
        while True:
            #--set logical parameters
            line = parse_line(file_obj.readline())            
            priority.append(int(line[0]))
            calc_mode.append(calc_mode_dict[int(line[1])])
            cnt_type.append(control_dict[int(line[2])])
            targ_type.append(target_dict[int(line[3])])
            #print self.branch,self.type,line
            values.append(float(line[-1]))
            #--just read the first logical operand
            lo.extend(self.get_logical_operands(file_obj))
                        
            #--set control point location data
            line = read_2_key('controlpoint',file_obj)
            #if line == None: break
            line = parse_line(line)
            cnt_pts.append([line[0][1:-1],float(line[1])])
                       
            #--set control strategy
            this_cnt_strat = []
            line = read_2_key('\[control_strategy\]',file_obj)
            while True:
                line = file_obj.readline()
                if stop_cnt_strat.search(line) != None: break
                line = parse_line(line)
                this_cnt_strat.append([float(line[0]),float(line[1])])
            cnt_strat.append(this_cnt_strat)
            
            #-- try to read another
            line = read_2_key('\[logical_statement\]',file_obj,\
                          stop='EndSect  // control_str_data')
            if line == None: break
        
        self.control_priority = priority
        self.control_values = values
        self.control_points = cnt_pts
        self.control_strategy = cnt_strat
        self.control_type = cnt_type
        self.target_type = targ_type
        self.logical_operand = lo
        return
    
    def get_logical_operands(self,file_obj):        
        lo = []
        line = read_2_key('\[logical_operands\]',file_obj,\
                          stop='EndSect  // logical_operands')
        stop_lo = re.compile('EndSect  // logical_operands',re.IGNORECASE)
        while True:
            line = read_2_key('logicaloperand',file_obj,\
                          stop='EndSect  // logical_operands')
            
            if line == None:
                #print lo
                return lo
            line = parse_line(line)
            #print self.branch,line
            if len(line) > 1:
                lo_type = lo_type_dict[int(line[0])]
                lo_sign = lo_sign_dict[int(line[7])]
                if int(line[8]) == 1:
                    lo_ts = True
                else:
                    lo_ts = False
                                  
                lo_value = float(line[9])
                lo.append([lo_type,lo_sign,lo_value,lo_ts])
            else:
                lo.append([None,None,None,None])
            
          
    
    def get_max_target(self,strategy):
       max_target = -1.0e+20
       for s in strategy:
           if abs(s[1]) > max_target: max_target = s[1]
            
       
    def set_attributes(self,file_obj):
        line = read_2_key('Attributes',file_obj)        
        self.attribute_line = parse_line(line) 
        self.itype = int(self.attribute_line[0])       
        self.type = self.get_str_type(self.itype)
        self.num = int(self.attribute_line[1])
        self.coeff = float(self.attribute_line[2])
        self.width = float(self.attribute_line[3])
        self.sill = float(self.attribute_line[4])
        self.speed = float(self.attribute_line[5])       
        if self.attribute_line[6].strip().upper() == 'TRUE':            
            self.init = float(self.attribute_line[7])
        else:
            if self.itype == 2:
                self.init = 0.0
            else:    
                print 'warning - gate instance with no specified initial value',self.id
                self.init = 0.0 
        if self.attribute_line[8].strip().upper() == 'TRUE':            
            self.max = float(self.attribute_line[7])
        else:
            self.max = None        
        return
    
    def get_str_type(self,str_type):        
        return type_dict[str_type]             

    def m_2_ft(self):
        print 'Too Lazy - do it on the backend...'
        raise SystemError
                
        
    def set_istrrch_istrconn(self,istrrch,istrconn):
        self.istrrch = istrrch
        self.istrconn = istrconn
    def set_istrorch(self,istrorch,istroqcon=None):
        self.istrorch = istrorch
        if istroqcon != None:
            self.istroqcon = istroqcon
        

    def write_swr_entry(self,file_obj,istrnum,istrrch=None,\
                        istrconn=None,istrorch=None,istroqcon=None,\
                        strwcd=0.61,strwcd2=0.5,strwcd3=0.5,\
                        m2ft=False):
     
        if istrrch == None:
            istrrch = self.istrrch
        if istrconn == None:
            istrconn = self.istrconn
        if istrorch == None:
            istrorch = self.istrorch
        
        
        strcritc_flow = 100.0
        strcritc_stage = 0.25
        strmax_pump = 1000000.0
        strmax_gate = 100.0
        
        place = '           '
        
        #--list of supported logical operands
        supported_log_ops = ['Hups','h','Hdws','Q_structure','Q',]
        
                
        #--check that this instance is supported
        #if self.logical_operand[0][0] not in supported_log_ops:         
        #    print 'control structure not supported',self.id,self.logical_operand[0][0]
        #    return
        
        #--find the highest-priority LO that can be used
        this_lo = None
        print self.id,len(self.logical_operand)
        for lo in self.logical_operand:
            print lo
            if lo[0] in supported_log_ops:
                this_lo = lo
                break        
        #--if no usable LO was found, just use the first one for place holding
        if this_lo == None:
            try:
                this_lo = self.logical_operand[0]
            except:
                this_lo = ['!JUNK!','!JUNK!',-999,'!JUNK!']
        
        #--make sure istroqcon passed if needed
        if this_lo[0] == 'Q' or \
           this_lo[0] == 'Q_structure' and \
                            istroqcon == None:
            try:
                istroqcon = self.istroqcon
            except:
                print 'ISTROQCON must be passed if control is Q or Q_structure',self.id
                raise ValueError
                
        
        #--determine what type of constrol structure
        if self.itype == 0:
            istrtype = 8 #overflow gate
        elif self.itype == 1:
            istrtype = 9 #underflow gate        
        elif self.itype == 2:
            istrtype = 3 #pump
        elif self.itype == 3:
            print 'radial underflow gate not supported',self.id
            raise ValueError
        elif self.itype == 4:  
            print 'Sluice, formula not supported',self.id
            raise ValueError
                                
        if m2ft:
            self.m_2_ft()
        
        #--istrcch,istrnum,istrconn,istrtype
        file_obj.write(' {0:10.0f} {1:10.0f} {2:10.0f} {3:10.0f}'\
                       .format(istrrch,istrnum,istrconn,istrtype))
        #--nstrpts
        file_obj.write(place)
        
        #--strwcd
        if istrtype != 3:
            file_obj.write(' {0:10.3e}'.format(strwcd))
        else:
            file_obj.write(place)
        
        #--strwcd2
        if istrtype == 9:
            file_obj.write(' {0:10.3e}'.format(strwcd2))
        else:
            file_obj.write(place)
        
        #--strwcd3
        if istrtype != 3:
            file_obj.write(' {0:10.3e}'.format(strwcd3))
        else:
            file_obj.write(place)
        
        #--strinv
        if istrtype != 3:           
            file_obj.write(' {0:10.3e}'.format(self.sill))
        else:
            file_obj.write(place)
        
        #--strinv2
        file_obj.write(place)
        
        #--strwid - assumes all gates operator together and are identical in geometry
        if istrtype != 3:
            file_obj.write(' {0:10.3e}'.format(self.width*self.num))
        else:
            file_obj.write(place)
            
        #--strwid2,strlen,strman
        file_obj.write(place+place+place)
        
        #--strval
        print self.id, self.init
        file_obj.write(' {0:10.3e}'.format(self.init))
        
        #--istrdir
        if istrtype != 3:
            file_obj.write(' {0:10.0f}'.format(0)) 
        else:
            file_obj.write(place)
        
        #--write some info
        file_obj.write(' #'+self.branch+' '+str(self.chainage)+' '+self.id+'\n')
               
        
        
        #--------------------------
        #--now write item 13b
        #--------------------------
        
        #--some spaces to offset 13b from 13a
        file_obj.write('    ')
                
        #--cstrotyp
       
        #this_lo = self.logical_operand[0]
        print self.id,this_lo
        if this_lo[0] == 'Hups' or \
           this_lo[0] == 'h' or \
           this_lo[0] == 'Hdws':
            cstrotyp = 'STAGE'
        elif this_lo[0] == 'Q' or \
             this_lo[0] == 'Q_structure':
            cstrotyp = 'FLOW'
        else:
            print 'Unsupported logical operand control type',this_lo[0],self.id
            cstrotyp = '!JUNK!'
            #raise ValueError
        
        #--istrorch
        file_obj.write(cstrotyp.rjust(11)+' {0:10.0f}'.format(istrorch))
        
        #--istroqcon
        if cstrotyp == 'FLOW':
            file_obj.write(' {0:10.0f}'.format(istroqcon))
        else:
            file_obj.write(place)
        
        #--cstrolo
        if cstrotyp != '!JUNK!':
            file_obj.write(this_lo[1].rjust(11))
        else:
            file_obj.write('!JUNK!'.rjust(11))
        
        #--strcrit
        if cstrotyp != '!JUNK!':
            file_obj.write(' {0:10.3e}'.format(this_lo[2]))
        else:
            file_obj.write('!JUNK!'.rjust(11))
        
        #--strcritc
        if cstrotyp == 'FLOW':
            file_obj.write(' {0:10.3e}'.format(strcritc_flow))
        elif cstrotyp == 'STAGE':
            file_obj.write(' {0:10.3e}'.format(strcritc_stage))
        else:
            file_obj.write('!JUNK!'.rjust(11))
        #--strrt
        file_obj.write(' {0:10.3e}'.format(self.speed))
        
        #--strmax
        try:
            file_obj.write(' {0:10.3e}'.format(self.max))
        except:
            if istrtype == 3:
                file_obj.write(' {0:10.3e}'.format(strmax_pump))
            else:
                file_obj.write(' {0:10.3e}'.format(strmax_gate))
        
        #--write some more info...
        file_obj.write('  #'+this_lo[0].rjust(10)+this_lo[1].rjust(5))
        file_obj.write('{0:10.3e}'.format(this_lo[2]))        
        file_obj.write('\n')
         

class weir():
    def __init__(self,file_obj):
        line = file_obj.readline()
        self.location_line = parse_line(line)
        self.branch = self.location_line[0].strip()[1:-1]
        self.chainage = float(self.location_line[1])
        self.id = self.location_line[2].strip()[1:-1]
        self.num = 1
        try:
            self.tag = self.location_line[3][1:-1]
        except:
            self.tag = ''
        self.set_attributes(file_obj) 
        self.set_weir_parameters(file_obj)
        self.levelwidth = self.get_levelwidth(file_obj)   
        if self.itype == 0 or self.type == 1:
            self.set_invert_from_Qh(file_obj)
            self.set_width_from_levelwidth()
        return
    
    def set_width_from_levelwidth(self):
        #--set width from level Width data using max width value
        max = -1.0e+20
        for lw in self.levelwidth:
            if lw[1] > max: max = lw[1]
        self.width = max
        return
        
    
    
    def set_invert_from_Qh(self,file_obj):
        line = read_2_key('\[QH_Relations\]',file_obj,\
                          stop='EndSect  // weir_data')
        qh = []
        qh_stop = re.compile('EndSect  // QH_Relations',re.IGNORECASE)
        while True:
            line = file_obj.readline()
            if qh_stop.search(line) != None: break
            line = parse_line(line)
            qh.append([float(line[0]),float(line[1])])
        self.invert = self.find_last_zero_q(qh)
        return
    
    def find_last_zero_q(self,qh):
        if qh[0][0] != 0.0:
            raise ValueError('first q in qh list != 0.0')
        h = qh[0][1]
        for i in qh:
            if i[0] == 0.0: h = i[1]
        return h       
    
    def get_levelwidth(self,file_obj):
        line = read_2_key('Level_Width',file_obj)
        levelwidth = []
        while True:
            line = parse_line(file_obj.readline())
            try:
                levelwidth.append([float(line[0]),float(line[1])])
            except:
                return levelwidth
                
    
           
    def set_attributes(self,file_obj):
        line = read_2_key('Attributes',file_obj)        
        self.attribute_line = parse_line(line)        
        self.itype = int(self.attribute_line[0])
        self.type = self.get_weir_type(self.itype)
        
        self.dir = get_flow_dir(int(self.attribute_line[0]))
        #print self.id,self.dir
        return
    
    
    def set_weir_parameters(self,file_obj):
        line = parse_line(read_2_key('WeirFormulaParam',file_obj))
        #self.weirparameters1 = self.list_2_float_list(line)
        self.width = float(line[0])
        self.height = float(line[1])
        self.coeff = float(line[2])
        self.exp = float(line[3])
        self.invert = float(line[4])
        line = parse_line(file_obj.readline())
        self.weirparameters2 = self.list_2_float_list(line)
        line = parse_line(file_obj.readline())
        self.weirparameters3 = self.list_2_float_list(line)
        return 
    
    
    def list_2_float_list(self,line):
       f_list = []
       for l in line:
           f_list.append(float(l))
       return f_list
         
    def get_weir_type(self,type):
        return weir_dict[type]
        
    def write_swr_entry(self,file_obj,istrnum,istrrch=None,\
                        istrconn=None,strwcd=0.61,strwcd3=0.5,\
                        m2ft=False):
        place = '           '
        istrtype = 6
        
        if istrrch == None:
            istrrch = self.istrrch
        if istrconn == None:
            istrconn = self.istrconn
        
        
        if m2ft:
            self.m_2_ft()
        
        #--istrcch,istrnum,istrconn,istrtype
        file_obj.write(' {0:10.0f} {1:10.0f} {2:10.0f} {3:10.0f}'\
                       .format(istrrch,istrnum,istrconn,istrtype))
        #--nstrpts
        file_obj.write(place)
        #--strwcd
        file_obj.write(' {0:10.3e}'.format(strwcd))
        #--strwcd2,strwcd3
        #file_obj.write(place+' {0:10.3e}'.format(strwcd3))
        file_obj.write(place+'{0:10.3e}'.format(0.5))
        #--strinv
        file_obj.write(' {0:10.3e}'.format(self.invert))
        #--strinv2,strwid
        file_obj.write(place+' {0:10.3e}'.format(self.width))
        #--strwid2,strlen,strman
        file_obj.write(place+place+place)
        #--strval
        file_obj.write(' {0:10.3e}'.format(self.invert))
        #--istrdir
        file_obj.write(' {0:10.0f}'.format(0)) 
        #--write some info
        file_obj.write(' #'+self.branch+' '+str(self.chainage)+' '+self.id+'\n')               

    def m_2_ft(self):
        self.invert *= 3.281
        self.height *= 3.281
        self.width *= 3.281
    
    def set_istrrch_istrconn(self,istrrch,istrconn):
        self.istrrch = istrrch
        self.istrconn = istrconn
        return          

class culvert():
    def __init__(self,file_obj):
        line = file_obj.readline()
        self.location_line = parse_line(line)
        self.branch = self.location_line[0].strip()[1:-1]
        self.chainage = float(self.location_line[1])
        self.id = self.location_line[2].strip()[1:-1]
        #self.type = 'culvert'
        try:
            self.tag = self.location_line[3][1:-1]
        except:
            self.tag = ''
        self.set_attributes(file_obj) 
        self.set_geometry(file_obj)   
        return
    
    def set_attributes(self,file_obj):
        
        line = read_2_key('Attributes',file_obj)        
        self.attribute_line = parse_line(line)        
        self.upstr = float(self.attribute_line[0])
        self.dwstr = float(self.attribute_line[1])
        self.length = float(self.attribute_line[2])
        self.mannings = float(self.attribute_line[3])
        self.num = int(self.attribute_line[4])
        self.dir = get_flow_dir(int(self.attribute_line[5]))
        return
        
    def set_geometry(self,file_obj):
        #--irregular not supported
        line = read_2_key('Geometry',file_obj)
        self.itype = int(parse_line(file_obj.readline())[0])
        self.type = culvert_dict[self.itype]
        rect = parse_line(file_obj.readline())
        self.width = float(rect[0])
        self.height = float(rect[1])
        self.diameter =  float(parse_line(file_obj.readline())[0])         
        return 

    def m_2_ft(self):
        self.upstr *= 3.281
        self.dwstr *= 3.281
        self.height *= 3.281
        self.width *= 3.281
        self.diameter *= 3.281
        self.length *= 3.281

        
    def write_swr_entry(self,file_obj,istrnum,istrrch=None,\
                        istrconn=None,strwcd=0.61,strwcd2=0.5,\
                        m2ft=False):
        place = '           '
        istrtype = 5
        
        if istrrch == None:
            istrrch = self.istrrch
        if istrconn == None:
            istrconn = self.istrconn
        
        
        if m2ft:
            self.m_2_ft()
        
        #--istrrch,istrnum,istrconn,istrtype
        file_obj.write(' {0:10.0f} {1:10.0f} {2:10.0f} {3:10.0f}'\
                       .format(istrrch,istrnum,istrconn,istrtype))
        #--nstrpts
        file_obj.write(place)
        #--strwcd,strwcd2
        file_obj.write(' {0:10.3e} {1:10.3e}'.format(strwcd,strwcd2))
        #--strwcd3
        file_obj.write(place)
        #--strinv,strinv2        
        file_obj.write(' {0:10.3e} {1:10.3e}'.format(self.upstr,self.dwstr))
        #--strwid,strwid2
        if self.type == 'Rectangular':
            file_obj.write(' {0:10.3e} {1:10.3e}'.format(-1.0*self.width,self.height))
            
        elif self.type == 'Circular':
            file_obj.write(' {0:10.3e}'.format(self.diameter))
            file_obj.write(place)
        else:
            print 'Unsupported culvert geometry:',self.type
            raise ValueError
        #--strlen    
        file_obj.write(' {0:10.3e}'.format(self.length))
        #--strman
        file_obj.write(' {0:10.3e}'.format(self.mannings))
        #--strval
        file_obj.write(place)
        #--istrdir
        file_obj.write(' {0:10.0f}'.format(0))         
        #--write some info                                                       
        file_obj.write(' #'+self.branch+' '+str(self.chainage)+' '+self.id+'\n')


    def set_istrrch_istrconn(self,istrrch,istrconn):
        self.istrrch = istrrch
        self.istrconn = istrconn
        return             