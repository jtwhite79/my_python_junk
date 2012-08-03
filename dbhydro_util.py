import numpy as np
import pandas
from datetime import datetime


idx = {'DA':{'STATION':0,'DBKEY':1,'DATE':2,'DATA':3},
       'BK':{'STATION':2,'DBKEY':3,'DATE':0,'TIME':1,'DATA':4}
       }


def parse_fname(fname):
    raw = fname.split('\\')[-1].split('.')
    fdict = {} 
    fdict['DBKEY'] = raw[0]  
    fdict['STATION'] = raw[1]
    fdict['FREQUECNCY'] = raw[2]
    fdict['STAT'] = raw[3]
    fdict['strnum'] = int(raw[4])
    s = raw[5]    
    e = raw[6]
    fdict['START'] = datetime.strptime(s,'%Y%m%d')
    fdict['END'] = datetime.strptime(e,'%Y%m%d')
    return fdict

#def interp_precip_pandas(fname):
#    '''interpolate a break point precip record to daily sum values
#    DON'T USE - precip breakpoint data are accumulated to the day of reading 
#    (the breakpoint).  Too dangerous to spread precip back over previous days
#    '''
#    #--load the pandas series
#    series = load_series(fname,aspandas=True)
#    #--cast the first and last day to whole days
#    s_date = datetime(year=series.index[0].year,month=series.index[0].month,day=series.index[0].day)
#    e_date = datetime(year=series.index[-1].year,month=series.index[-1].month,day=series.index[-1].day)
#    #--create the date range 
#    dr1day = pandas.DateRange(s_date,e_date,offset=pandas.DateOffset())
#    #--use groupby to create daily grouping
#    grouped = series.groupby(dr1day.asof)
#    #--a new dataframe of summed daily values
#    sums = grouped.sum()    
#    #--since it is breakpoint, assume no entry means zero rain
#    sums_filled = sums.fillna(0.0)
#    #--form new file name - ugly
#    f_dict = parse_fname(fname)
#    f_dict['FREQUENCY'] = 'DA'
#    f_dict['STAT'] = 'SUM'
#    f_dict['START'] = f_dict['START'].strftime('%Y%m%d')
#    f_dict['END'] = f_dict['END'].strftime('%Y%m%d')
#    raw = fname.split('\\')
#    new_fname = '\\'.join(raw[:-1])+'\\'
#    new_fname += f_dict['STATION']+'.'+f_dict['FREQUENCY']+'.'+f_dict['STAT']+'.'+\
#                 str(f_dict['strnum'])+'.'+str(f_dict['START'])+'.'+str(f_dict['END'])+'..dat'        
#    print sums_filled[sums_filled.columns[0]]
#    #--save the new daily summed filled series
#    save_series(new_fname,sums_filled)



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
        
                           
def save_series(fname,df,write_col=None):
    '''save a pandas dataframe instance in an acceptable format
    expects the index to be a datetime
    default = writes the first entry returned by DataFrame.columns
    '''
    cols = df.columns
    if write_col is None:
        write_col = cols[0]
    f_out = open(fname,'w')
    #for dt,r in df.iteritems():
    for dt,val in zip(df.index,df[write_col]):
        f_out.write(dt.strftime('%Y%m%d')+',{0:15.7e}\n'.format(val))
    f_out.close()        
    return


def load_series(fname,aspandas=False):        
    f_dict = parse_fname(fname)                   
    h_dict = load_header(fname)    
    print 'loading dbkey: ',h_dict['DBKEY']
    print 'from file: ',fname    
    iidx = idx[h_dict['FQ']]   
    f = open(fname,'r')                
    #--read the first 3 lines (headers)
    h1,h2,h3 = f.readline(),f.readline(),f.readline()            
    rec,flg = [],[]
    #for line in f:
    while True:
        line = f.readline()
        if line == '':
            break
        dt,val,fflg = parse_line(line,iidx)
        if aspandas:
            rec.append([dt,val])
            flg.append(fflg)
        elif val is not np.NaN:
            rec.append([dt,val])
            flg.append(fflg)
        
    f.close()
    print '--- ',len(rec),' records'
    rec = np.array(rec)
    if aspandas:
        
        df = pandas.DataFrame({'datetime':rec[:,0],h_dict['DBKEY']:rec[:,1]})
        df.index = df['datetime']
        #df.pop('datetime')
        #s = pandas.Series(rec[:,1],index=rec[:,0],name=h_dict['DBKEY'])        
        return df
    else:
        return np.array(rec),flg

def load_header(f):
    f = open(f,'r')
    #--read the first 3 lines (headers)
    hkeys,hvalues = f.readline().strip().split(','),f.readline().strip().split(',')   
    h_dict = {}
    for hkey,hvalue in zip(hkeys,hvalues):
        h_dict[hkey] = hvalue    
    f.close()
    return h_dict

def parse_line(line,idx):
    raw = line.strip().split(',')
    if 'TIME' not in idx.keys():
        dt = datetime.strptime(raw[idx['DATE']],'%d-%b-%Y')
    else:
        dt =  datetime.strptime(raw[idx['DATE']]+' '+raw[idx['TIME']],'%d-%b-%Y %H:%M') 
    flg = None
    #if len(raw) > 6:
    if 'FLAG' in idx.keys():
        flg = raw[idx['FLAG']]
        #print flg
    try:
        val = float(raw[idx['DATA']])     
    except ValueError:
        v = raw[idx['DATA']].upper() 
        if v == 'M' or v == 'X' or v == 'N':
            val = np.NaN
        elif v == 'PROVISIONAL':
            val = np.NaN        
        else:
            print line
            raise ValueError, 'unrecognized non-float in value field: '+str(raw[idx['DATA']])
    return dt,val,flg