import numpy as np
import pandas
from datetime import datetime,timedelta


idx = {'DA':{'STATION':0,'DBKEY':1,'DATE':2,'DATA':3},
       'BK':{'STATION':2,'DBKEY':3,'DATE':0,'TIME':1,'DATA':4},
       'FWM':{'STATION':0,'DBKEY':1,'DATE':2,'DATA':3},
       'DWR':{'STATION':0,'DBKEY':1,'DATE':2,'TIME':3,'DATA':4},
       'INST':{'STATION':2,'DBKEY':3,'DATE':0,'TIME':1,'DATA':4},
       'MEAN':{'STATION':0,'DBKEY':1,'DATE':2,'DATA':3}
       }


def build_fname(fdict):
    sdate = fdict['START'].strftime('%Y%m%d')
    edate = fdict['END'].strftime('%Y%m%d')
    fname = fdict['DBKEY']+'.'+fdict['STATION']+'.'+fdict['FREQUENCY']+'.'+fdict['STAT']+'.'+str(fdict['strnum'])+'.'+\
            sdate+'.'+edate+'.'+'.dat'   
    return fname


def parse_fname(fname):
    raw = fname.split('\\')[-1].split('.')
    fdict = {} 
    fdict['DBKEY'] = raw[0]  
    fdict['STATION'] = raw[1]
    fdict['FREQUENCY'] = raw[2]
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


def make_daily(df,interp=False):
    '''only one column per dataframe!
    '''
    #--get the data column name
    dbkey = df.columns.tolist()[0]
    
    #--average daily values - in case there are days with multiple entries
    grouped = df[dbkey].groupby(lambda x: x.toordinal())
    groups = grouped.groups
    series_mean = grouped.mean()
    df_mean = pandas.DataFrame({dbkey:series_mean},index=series_mean.index)
    df_mean['ord'] = df_mean.index
    df_mean['dt'] = df_mean['ord'].apply(lambda x:datetime.fromordinal(x) + timedelta(hours=12))
    df_mean.index = df_mean['dt']
    df_mean.pop('ord')
    df_mean.pop('dt')

    #--make a new df over the whole range of the data
    drange = pandas.date_range(df_mean.index[0],df_mean.index[-1])
    df_range = pandas.DataFrame({dbkey:np.NaN},index=drange)
    
    #--merge the data into the empty dataframe
    df_range = df_range.combine_first(df_mean)
    
    #--linearly interpolate missing days
    if interp:
        df_range[dbkey] = df_range[dbkey].interpolate()
         
    return df_range.dropna()
    
    
def make_daily_breakpoint(df,threshold=0.0,interp=False):
    '''interpolate the series from breakpoint to daily avg   
    threshold = minimum significant opening
    '''    
    
    #--apply threshold    
    dbkey = df.columns.tolist()[0]
    df[df[dbkey]<threshold] = threshold
    
    #--group by date   
    #grouped = df.groupby(lambda x: x.toordinal())
    #groups = grouped.groups
    #ord_days = groups.keys()

    dt = np.array(df.index.tolist())    
    data = np.array(df[dbkey].values.tolist())
    data = np.vstack((dt,data)).transpose()
    #--strip out the nans
    data = data[~np.isnan(data[:,1].astype(np.float64))]
    
    ord_days = []
    for d in data[:,0]:
        ord_days.append(d.toordinal())
    ord_days = np.array(ord_days)



    #--process each day
    #last_entry = df[dbkey][0]
    try:
        last_entry = data[-1,1]
    except:
        return pandas.DataFrame()
    rec = []
    for day in range(ord_days[0],ord_days[-1]):              
        #--if this day has some entries, calc the time-weighted average        
        if day in ord_days:
                                   
                entries = data[np.where(ord_days==day),:][0]                
                avg_day_value = calc_time_avg(last_entry,entries)            
                last_entry = entries[-1,1]  
            
        #--otherwise, use the last entry for the day
        else:            
            avg_day_value = last_entry
        rec.append([datetime.fromordinal(day)+timedelta(hours=12),avg_day_value])    
    #--create a new pandas dataframe of daily average values
    rec = np.array(rec)
    df = pandas.DataFrame({dbkey:rec[:,1].astype(np.float64)},index=rec[:,0])
    start = datetime.fromordinal(ord_days[0]) + timedelta(hours=12)
    end = datetime.fromordinal(ord_days[-1]) + timedelta(hours=12)
    df_range = pandas.DataFrame({dbkey:np.NaN},index=pandas.date_range(start,end))
    df_range = df_range.combine_first(df)
    if interp:
        df_range[dbkey] = df_range[dbkey].interpolate()

    return df_range.dropna()            
    

def calc_time_avg(last_entry,entries):
    ''' for averaging breakpoint data - series is augmented with the previous value at
    the start of the day
    '''    
    #--a dt object, 00:00:00
    s_day,s_mon,s_yr = entries[0,0].day,entries[0,0].month,entries[0,0].year
    day_start = datetime(year=s_yr,month=s_mon,day=s_day)
        
    #--midnight to the first entry
    wght = (float((entries[0,0] - day_start).seconds)/86400.0)        
    val = wght * last_entry
        
    #--from the first entry to the last
    for i in range(len(entries)-1):
        wght = (float((entries[i+1,0] - entries[i,0]).seconds)/86400.0)
        val += entries[i,1] * wght         
        #secs = (series.index[i+1] - series.index[i]).seconds        
        #wght = (float(secs))/86400.0
        #val += (series[i]) * wght
        
    #--last entry to midnight
    next_day = day_start + timedelta(days=1)
    wght = (float((next_day - entries[-1,0]).seconds)) / 86400.0
    val += wght * entries[-1,1]

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
        
#def save_smp(fname,df):
#    need to implement

                           
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
        dvals = rec[:,1].astype(np.float64)
        df = pandas.DataFrame({h_dict['DBKEY']:dvals},index=rec[:,0])        
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
    missing_vals = ['M','X','N','!','E']
    if 'TIME' not in idx.keys():
        dt = datetime.strptime(raw[idx['DATE']],'%d-%b-%Y')
        dt += timedelta(hours=12)
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
        if v in missing_vals:
            val = np.NaN
        elif v == 'PROVISIONAL':
            val = np.NaN        
        else:
            print line
            raise ValueError, 'unrecognized non-float in value field: '+str(raw[idx['DATA']])
    return dt,val,flg