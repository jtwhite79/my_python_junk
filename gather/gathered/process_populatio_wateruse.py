from datetime import datetime
import re
import xlrd
import pandas
import numpy as np
import matplotlib.pyplot as plt
import pylab
from fuzzywuzzy import fuzz,process

import shapefile
import pws_class as pws


#-----------------------------------------------------------
#--load the shapefile with the wfield names added

shp = shapefile.Reader('..\\_gis\\shapes\\pws_combine')
records = shp.records()
header = shp.dbfHeader()

#--find the indexs of important attributes
idxs = {}
idxs['wname'] = None
idxs['perm_no'] = None
idxs['wfield'] = None
idxs['utility'] = None
idxs['status'] = None
idxs['aban_year'] = None
idxs['dril_year'] = None
idxs['well_dia'] = None
idxs['well_dep'] = None
idxs['well_cas'] = None
idxs['dpep_name'] = None

for i,h in enumerate(header):
    for k,v in idxs.iteritems():
        if k.upper() == h[0].upper():           
            idxs[k] = i
            break
for k,v in idxs.iteritems():
    if v == None:
        raise IndexError,'couldnt find index for '+k

#--create well objects
wells = []
w_util = []
shp_plist = []
for i,r in enumerate(records):    
    p,wn,wf = r[idxs['perm_no']],r[idxs['wname']],r[idxs['wfield']]    
    u,s,a_yr = r[idxs['utility']],r[idxs['status']],r[idxs['aban_year']]    
    d_yr,dia,dep = r[idxs['dril_year']],r[idxs['well_dia']],r[idxs['well_dep']]
    cas = r[idxs['well_cas']]
    depname = r[idxs['dpep_name']]
    #--try to use dril and aban fields, otherwise...
    try:
        d_dt = datetime(year=int(d_yr),month=1,day=1)
    except:
        d_dt = datetime(year=1900,month=1,day=1)        
    try:
        a_dt = datetime(year=int(a_yr),month=1,day=1)
    except:
        a_dt = datetime(year=2012,month=5,day=31)        
             
    #--if the wfield attribute is blank...           
    if len(wf) == 0:        
        wf = 'all'        
    #--a list of keys to make
    wflist = wf.strip().split(',')
    if 'all' not in wflist:
        wflist.append('all')
    for i,wf in enumerate(wflist):
        wflist[i] = wf.upper()
    #--create a pws object
    w = pws.pws(p,wn,depname,u,dia,dep,cas,wfield=wflist,dril=d_dt,aban=a_dt)
    wells.append(w) 
    if u not in w_util:
        w_util.append(u)
      
    if p not in shp_plist:
        shp_plist.append(p)

print len(wells)

#--group wells by util name in a dict
well_dict = {}
for w in wells:
    if w.util in well_dict.keys():
        well_dict[w.util].append(w)
    else:
        well_dict[w.util] = [w]



fname = 'source_spreadsheets\\Comp_Broward_Cens&Wtruse.xls'
wb = xlrd.open_workbook(fname)

#--load the per captia water use data (Marella) - for pre-1965
#--gal/person/day
percaptia_sheet = wb.sheet_by_name('Marellafig6')
percaptia_data = [[],[]]
cap_header = percaptia_sheet.row_values(0)
for i in range(1,percaptia_sheet.nrows):
    row = percaptia_sheet.row_values(i)
    dt = datetime(year=int(row[0]),month=1,day=1)   
    #--convert value from gal to ft^3
    val = float(row[1]) / 7.481
    percaptia_data[0].append(dt)
    percaptia_data[1].append(val)
#--create PANDAS series
pc = pandas.Series(percaptia_data[1],index=percaptia_data[0],name='percaptia')
#--create an NAN daily series for the percaptia range
d_range = pandas.DateRange(percaptia_data[0][0],percaptia_data[0][-1],offset=pandas.DateOffset())
pc_daily = pandas.Series(np.nan,index=d_range)
#--insert the percaptia data into the daily series
pc_daily = pc_daily.combine_first(pc)
#--interpolate to daily
#pc_daily = pc_daily.interpolate()
#-create a PANDAS dataframe
df = pandas.DataFrame({'percapita':pc})


#--load the city population data
pop_sheet = wb.sheet_by_name('Mapcitypop')
pop_header = pop_sheet.row_values(0)
pop_data = {}
min_dt,max_dt = datetime(2100,1,1),datetime(1800,1,1)
for i in range(1,pop_sheet.nrows):
    row = pop_sheet.row_values(i) 
    loc = row[1]
    dt = datetime(year=int(row[0]),month=1,day=1)   
    if dt > max_dt:
        max_dt = dt
    if dt < min_dt:
        min_dt = dt
    val = float(row[2])
    if loc in pop_data.keys():       
        pop_data[loc][0].append(dt)
        pop_data[loc][1].append(val)
    else:        
        pop_data[loc] = [[dt],[val]]
                 
#--for each city population series...
series_dict = {}
for k,[dt_list,val_list] in pop_data.iteritems():
   
    #--make a unique list - sum up values
    udt_list,uval_list = [],[]
    for dt,val in zip(dt_list,val_list):
        if dt not in udt_list:
            udt_list.append(dt)
            uval_list.append(val)
        else:
            idx = udt_list.index(dt)
            uval_list[idx] += val
    #--create a date range object for this record
    d_range = pandas.DateRange(min(dt_list),pws.M_END,offset=pandas.DateOffset())
    #--create a PANDAS series
    ts = pandas.Series(uval_list,index=udt_list)  
    #--create an NAN series for the percaptia date range
    ts_daily = pandas.Series(np.nan,index=d_range)
    
    #df = pandas.DataFrame({'ts':ts})
    #df_daily = pandas.DataFrame({'ts':ts_daily})    
    #df_join = df_daily.join(df,on='ts',how='left')
    #df_merge = df_daily.merge(df,how='left',left_index=True,right_index=True) 
    #df_merge['ts_y_int'] = df_merge['ts_y'].interpolate()
    #print df_merge['ts_y_int'].dropna()
    #--insert the daily data
    
    ts_daily = ts_daily.combine_first(ts)           
    #--interpolate to daily
    ts_daily = ts_daily.interpolate()    
    #print ts_daily.dropna()
    #--create a total volume used series
    ts_daily = ts_daily * pc
    ts_daily = ts_daily.fillna().dropna()    
    if len(ts_daily) > 0:         
        print k,ts_daily.dropna()
        #--add it to the dataframe    
        series_dict[k] = ts_daily    
        #ts_daily.plot()
    else:
        print 'no valid merge points for ',k

df = pandas.DataFrame(series_dict)



#--match population titles with well util attributes
d_range = pandas.DateRange(pws.M_START,pws.M_END,offset=pandas.DateOffset())
missing = pandas.DataFrame({'temp':np.NaN},index=d_range)

for name,series in df.iteritems():
    print 'processing',name
    series = series.dropna()
    print 'length:',len(series)
    #--find probable matches    
    match = process.extract(name,w_util,limit=3)
    util_wells = []
    for m in match:
        if m[-1] > 80.0:             
            util_wells.extend(well_dict[m[0]])    
    if len(util_wells) > 0:
        series = series.dropna()
        missing_dt,missing_flux = [],[]
        
        for dt,val in series.iteritems():
            #print dt,val
            act_wells = []
            for w in util_wells:
                if w.active(dt):
                    act_wells.append(w)
            if len(act_wells) == 0:
                print 'warning - no active wells found for ',name,' on date ',dt
                if dt in missing_dt:
                    idx = missing_dt.index(dt)
                    missing_flux[idx] += val
                else:
                    missing_dt.append(dt)
                    missing_flux.append(val)
            else:
                val /= float(len(act_wells))
                for w in act_wells:
                    w.add_record(pws.POPEST,dt,val,sort=False)
        if len(missing_dt) > 0:
            df = pandas.DataFrame({name:missing_flux},index=missing_dt)
            missing = missing.merge(df,how='outer',left_index=True,right_index=True)           
            #break
        #break
    else:
        print 'no wells found for',name
        df = pandas.DataFrame({name:series})
        missing = missing.merge(df,how='outer',left_index=True,right_index=True)
    
for util,wlist in well_dict.iteritems():
    print 'writing utility',util
    for w in wlist:
        w.write_raw_records(odir='pws_smp_components\\')

missing.pop('temp')
#missing.pop('percapita')
missing *= 7.481
missing /= 1.0e+6
missing.to_csv('missing_popest.csv',index_label='datetime')
#missing.plot()
#pylab.show()
#missing_series = pandas.Series(missing_flux,index=missing_dt)
#missing_series *= 7.481
#missing_series /= 1.0e+6
#missing_series.to_csv('missing.csv')
#missing_series.plot()

    
    
#--now load the historic water use data - for 1965 to 1975 for PWS, 1965 to present for ag
#fname = 'Broward_County_water-use_1965-2000_mod.xls'
#wb = xlrd.open_workbook(fname)
#wuse_sheet = wb.sheet_by_index(0)
#h1,h2 = wuse_sheet.row_values(0),wuse_sheet.row_values(1)
#wuse_data = []
#for i in range(2,wuse_sheet.nrows):
#    r = tuple(wuse_sheet.row_values(i))
#    wuse_data.append(r)

#--some processing




