import os
import numpy as np
import pandas
from datetime import datetime

class dbhydro_record():
    
    
    def __init__(self,fname):
        assert os.path.exists(fname)
        self.fname = fname
        self.parse_fname()       

    def parse_fname(self):
        if '\\' in self.fname:
            fname = self.fname.split('\\')[-1]
        else:
            fname = self.fname            
        raw = fname.split('.')         
        self.site = raw[0]
        self.dtype = raw[1]
        self.freq = raw[2]
        self.strnum = int(raw[3])
        s = raw[4]    
        e = raw[5]
        self.sdate = datetime.strptime(s,'%Y%m%d')
        self.edate = datetime.strptime(e,'%Y%m%d')        
        return


    def sample_breakpoint(self):
        '''interpolate the series from breakpoint to daily
        with time-weighted averaging
         '''
              
        #--cast series datetimes to ordinals
        series_ord = []
        for i,dt in enumerate(self.series[:,0]):
            series_ord.append(dt.toordinal())      
        series_ord = np.array(series_ord)
        
        last_entry = series[0,1]
        rec = []    
        for day in series_ord:              
            series_day = self.series[np.where(series_ord == day),:][0]
            #print day,datetime.fromordinal(day),series_day
            #print series_day.shape
            if series_day.shape[0] > 0:
                #--calc time weighted avg
                v_day = calc_time_avg(last_entry,series_day)
                #v_day = np.mean(series_day[:,1])
                #print series_day[-1,1]
                last_entry = series_day[-1,1]
                
            else:            
                v_day = last_entry
            rec.append([datetime.fromordinal(day),v_day])
            #break
            #if v_day != 0.0:
            #    print rec[-1]
            #break  
        self.record = rec
        return              
    
    
    def calc_time_avg(self,last_entry,series):
        ''' series is augmented with the previous value at
        the start of the day
        '''
        
        #--if only one entry
        if series.shape[0] == 0:
            return last_entry
                    
        else:
            #--a dt object, 00:00:00
            s_day,s_mon,s_yr = series[0,0].day,series[0,0].month,series[0,0].year
            day_start = datetime(year=s_yr,month=s_mon,day=s_day)
            
            #--midnight to the first entry
            wght = (float((series[0,0] - day_start).seconds)/86400.0)
            val = wght * last_entry
            
            for i,s in enumerate(series[1:]):
                wght = (float((series[i,0] - series[i-1,0]).seconds)/86400.0)
                val += series[i-1,1] * wght                        
        return val
    
    
    def load_series(self):
        
        #--parse the filename 
        print 'loading file: ',self.fname
        
        f = open(self.fname,'r')
        #--read the first 3 lines (headers)
        h1,h2,h3 = f.readline(),f.readline(),f.readline()
        rec,flg = [],[]
        for line in f:
            dt,val,fflg = parse_line(line)
            rec.append([dt,val])
            flg.append(fflg)
            
        f.close()
        print '--- ',len(rec),' records'        
        self.record = np.array(rec)
        self.flag = flg
        return #np.array(rec),flg
    
    
    def parse_line(self,line):
        raw = line.strip().split(',')
        dt =  datetime.strptime(raw[0]+' '+raw[1],'%d-%b-%Y %H:%M') 
        flg = None
        if len(raw) > 6:
            flg = raw[5]
            #print flg
        try:
            val = float(raw[4])     
        except ValueError:
            if raw[4].upper() == 'M':
                val = np.NaN
            elif raw[4].upper() == 'PROVISIONAL':
                val = np.NaN
            else:
                print line
                raise ValueError, 'unrecognized non-float in value field: '+str(raw[4])
        return dt,val,flg