import numpy as np
import pandas
from datetime import datetime

def parse_fname(fname):
    raw = fname.split('.')
    fdict = {}
    fdict['site'] = raw[0]
    fdict['dtype'] = raw[1]
    fdict['freq'] = raw[2]
    fdict['strnum'] = int(raw[3])
    s = raw[4]    
    e = raw[5]
    fdict['sdate'] = datetime.strptime(s,'%Y%m%d')
    fdict['edate'] = datetime.strptime(e,'%Y%m%d')
    return fdict


def interp_breakpoint(series,flag,threshold=0.0):
    '''interpolate the series from breakpoint to daily    
    threshold = minimum significant opening
    '''    
    #--cast series datetimes to ordinals
    series_ord = []
    for i,dt in enumerate(series[:,0]):
        series_ord.append(dt.toordinal())      
    
    #--apply threshold
    series[np.where(series[:,1] < threshold),1] = threshold
    
    series_ord = np.array(series_ord)    
    last_entry = series[0,1]
    rec = []    
    for day in range(series_ord[0],series_ord[-1]):              
        series_day = series[np.where(series_ord == day),:][0]
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
    return np.array(rec)              


def calc_time_avg(last_entry,series):
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


def create_full_record(p_series_list):
    '''tiles records together
    creates a daily record over the minimum to maximum dates in the 
    series list
    '''
    
    #--find the min and max dates
    min_date,max_date = datetime(year=3012,month=1,day=1),datetime(year=1512,month=1,day=1)
    for p in p_series_list:
       
        if p.index.min() < min_date:
            min_date = p.index[0]
        if p.index.max() > max_date:
            max_date = p.index[-1]
    #print min_date,max_date 
    
    #--create new pandas date range inclusive of the whole record
    d_range = pandas.DateRange(start=min_date,end=max_date,offset=pandas.core.datetools.day)
    full_series = pandas.TimeSeries(np.ones(len(d_range))*np.nan,d_range)
    #print d_range   
    
    #--since I can't get all of the pandas functionality to run...
    for dt,val in full_series.iteritems():
        #--try to find an entry in one of the series for this day
        v = np.nan
        for p in p_series_list:
            #print p.head()
            try:
                if p[dt] != np.nan:
                    v = p[dt]
            except:
                pass
            if v != np.nan:
                full_series[dt] = v
                #break
                                                                                    
        
    return full_series        
        
                           
def save_series(fname,p_series):
    f_out = open(fname,'w')
    for dt,r in p_series.iteritems():
        f_out.write(dt.strftime('%Y%m%d')+',{0:15.7e}\n'.format(r))
    f_out.close()        


def load_series(fname):
    
    #--parse the filename 
    print 'loading file: ',fname
    
    f = open(fname,'r')
    #--read the first 3 lines (headers)
    h1,h2,h3 = f.readline(),f.readline(),f.readline()
    rec,flg = [],[]
    for line in f:
        dt,val,fflg = parse_line(line)
        rec.append([dt,val])
        flg.append(fflg)
        
    f.close()
    print '--- ',len(rec),' records'
    return np.array(rec),flg


def parse_line(line):
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