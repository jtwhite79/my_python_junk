import re
import calendar
from datetime import datetime
import numpy as np
import pandas

#--record types
ACCUM = 'accumulated'
PART = 'partial'
INDIV = 'individual'
POPEST = 'popestm'

#--global conceptual model start and end dates
M_START = datetime(1900,1,1)
M_END = datetime(2012,5,1)

class pws():
    def __init__(self,perm_no,well_no,util,dia,dep,case,\
                 wfield=['all'],dril=M_START,\
                 aban=M_END):
        self.perm_no = perm_no
        self.well_no = well_no     
        self.util = util        
        self.dril = dril
        self.aban = aban
        self.wfield = wfield
        self.dia = dia
        self.dep = dep
        self.case = case
        self.records = {}        
        #self.build_active_series()
    
    def build_active_series(self):
        d_range = pandas.DateRange(M_START,M_END,offset=pandas.DateOffset())
        ts_daily = pandas.Series(np.nan,index=d_range)
        ts_daily[self.dril:self.aban] = True
        self.active = ts_daily
    
    def active(self,dt):
        if dt >= self.dril and dt <= self.aban:
            return True
        else:
            return False                    
    def check_wfield(self,nstring):
        for wf in self.wfield:
            #print wf,nstring,re.search(wf,nstring,re.IGNORECASE)
            if re.search(wf.strip(),str(nstring),re.IGNORECASE) != None:
                return True
        return False 
    
    def add_record(self,rtype,dt,val,accum_dt=False):
        '''accum_dt determines if entries for the same datetime are summed or not
        '''
        if rtype not in self.records:
            self.records[rtype] = [[dt],[val]]
        else:
            if accum_dt and dt in self.records[rtype][0]:
                idx = self.records[rtype][0].index(dt)
                self.records[rtype][1][idx] += val
            else:    
                self.records[rtype][0].append(dt)                                   
                self.records[rtype][1].append(val)

    def write_records(self,odir='.\\'):
        #--converts monthly mgals to daily ft3
        for k,rec in self.records.iteritems():
            fname = self.perm_no+'_'+str(self.well_no).upper()+'_'+k+'.dat'
            f_out = open(odir+fname,'w')
            for dt,val in zip(rec[0],rec[1]):
                days_month = calendar.monthrange(dt.year,dt.month)[1]
                val_ft3 = val * 1.0e6 / 7.481
                val_daily = val_ft3 / float(days_month)
                for day in range(days_month):
                    ddt = datetime(year=dt.year,month=dt.month,day=day+1)
                    ddt_str = ddt.strftime('%Y%m%d')
                    f_out.write(ddt_str+' {0:15.7e}\n'.format(val_daily))
                
                #dt_str = dt.strftime('%Y%m%d')                
                #f_out.write(dt_str+' {0:15.7e}\n'.format(val))
            f_out.close()                
                
    def write_raw_records(self,odir='.\\'):        
        for k,rec in self.records.iteritems():
            fname = self.perm_no+'_'+str(self.well_no).upper()+'_'+k+'.dat'
            f_out = open(odir+fname,'w')
            for dt,val in zip(rec[0],rec[1]):
                dt_str = dt.strftime('%Y%m%d')
                f_out.write(dt_str+' {0:15.7e}\n'.format(val))                                
            f_out.close()                
                                   
           
            
            