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
    def __init__(self,perm_no,well_no,depname,util,dia,dep,case,\
                 wfield=['all'],dril=M_START,\
                 aban=M_END):
        self.perm_no = perm_no
        self.well_no = well_no
        self.depname = depname     
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
    
    def add_record(self,rtype,dt,val,accum_dt=False,sort=False):
        '''accum_dt determines if entries for the same datetime are summed or not
        '''
        if rtype not in self.records.keys():
            #self.records[rtype] = [[dt],[val]]
            self.records[rtype] = np.atleast_2d(np.array([dt,val]))
        else:
            if accum_dt and dt in self.records[rtype][:,0]:
                self.records[rtype][np.where(self.records[rtype][:,0]==dt),1] += val                
            else:    
                self.records[rtype] = np.vstack((self.records[rtype],np.array([dt,val])))
                if sort:
                    idx = np.argsort(self.records[rtype][:,0])
                    self.records[rtype] = self.records[rtype][idx]
                pass

    def write_records(self,odir='.\\'):
        #--converts monthly mgals to daily ft3
        for k,rec in self.records.iteritems():
            sidx = np.argsort(rec[:,0])
            rec = rec[sidx]
            fname = self.depname+'.'+k+'.smp'
            f_out = open(odir+fname,'w')
            for dt,val in rec:
                days_month = calendar.monthrange(dt.year,dt.month)[1]
                val_ft3 = val * 1.0e6 / 7.481
                val_daily = val_ft3 / float(days_month)
                for day in range(1,days_month+1):
                    ddt = datetime(year=dt.year,month=dt.month,day=day)
                    ddt_str = ddt.strftime('%d/%m/%Y')
                    f_out.write(k.ljust(20)+'  '+ddt_str+'  00:00:00  {0:15.7e}\n'.format(val_daily))
                #break
                #dt_str = dt.strftime('%d/%m/%Y')                
                #f_out.write(k+'  '+dt_str+'  00:00:00  {0:15.7e}\n'.format(val_daily))
            f_out.close()                
                
    def write_raw_records(self,odir='.\\'):        
        for k,rec in self.records.iteritems():
            sidx = np.argsort(rec[:,0])
            rec = rec[sidx]
            fname = self.depname+'.'+k+'.smp'
            f_out = open(odir+fname,'w')
            for dt,val in rec:
                dt_str = dt.strftime('%d/%m/%Y')
                f_out.write(k.ljust(20)+'  '+dt_str+'  00:00:00  {0:15.7e}\n'.format(val))   
            f_out.close()                
                                   
           
            
            