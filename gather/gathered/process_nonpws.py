import re
import sys
import math
import calendar
from string import printable
from datetime import datetime
import numpy as np
import xlrd
import shapefile

import pws_class as pws


def unique_list(lst):
    seen = {}
    result = []
    for item in lst:
        if marker in seen:
            seen[marker] = 1
            result.append(item)
    return result
    

def load_pws_data(dfile):            
    permit_idx = 0
    name_idx = 2
    date_idx = 3
    data_idx = 4
    reqm_idx = 5    
    
    
    fail_count = 0
    wb = xlrd.open_workbook(dfile)
    sh = wb.sheet_by_index(0)
    header = sh.row_values(0)
            
 
    
    permit_list = []
    #--name,reqm,datetime,val
    data_list = [[],[],[],[]]
    
    for i in range(1,sh.nrows):
        raw = sh.row_values(i)    
        #print raw       
        
        if raw[data_idx] != '':                       
        
            this_permit = raw[permit_idx]
            try:
                this_reqm = int(raw[reqm_idx])
            except:
                this_reqm = raw[reqm_idx] 
            #print this_reqm                                               
            this_name = raw[name_idx].strip()
            this_date_str = raw[date_idx]
            this_val = raw[data_idx]
            try:
                this_dt = xlrd.xldate_as_tuple(this_date_str,wb.datemode)                            
                #print this_date_str,this_dt[0]
                this_date = datetime(year=this_dt[0],month=this_dt[1],day=this_dt[2])
                #this_year,this_month = this_dt[0],this_dt[1]
                if this_permit in permit_list:
                    idx = permit_list.index(this_permit)
                    data_list[0][idx].append(this_name)
                    data_list[1][idx].append(this_reqm)
                    data_list[2][idx].append(this_date)
                    data_list[3][idx].append(this_val)
                else:
                    permit_list.append(this_permit)
                    data_list[0].append([this_name])                
                    data_list[1].append([this_reqm])
                    data_list[2].append([this_date])
                    data_list[3].append([this_val])
            except:
                fail_count += 1    
        
    return permit_list,data_list







#-----------------------------------------------------------
#--main
#-----------------------------------------------------------




#-----------------------------------------------------------
#--load the shapefile with the wfield names added
print 'loading shapefile...'
shapename = '..\\_gis\\scratch\\nonpws_web_points_reduce'
shp = shapefile.Reader(shapename)

header = shp.dbfHeader()

#--find the indexs of important attributes
idxs = {}
idxs['permit_no'] = None
idxs['project_na'] = None
idxs['start_date'] = None
idxs['end_date'] = None
idxs['web_src'] = None

for i,h in enumerate(header):
    for k,v in idxs.iteritems():
        if k.upper() == h[0].upper():           
            idxs[k] = i
            break

for k,v in idxs.iteritems():
    if v == None:
        raise IndexError,'couldnt find index for '+k

#--this takes awhile...
records = shp.records()
shapes = shp.shapes()
print len(records),' records loaded from shapefile'

#--create well objects
print 'creating well objects from shape info...'
wells = []
shp_plist = []
shp_plist_full = []
for r in records:
    p = r[idxs['permit_no']]
    u,s = r[idxs['project_na']],'Existing'
    dia,dep = -999,-999
    cas = -999        
    s_text = r[idxs['start_date']]
    e_text = r[idxs['end_date']]
    try:
        s_dt = datetime.strptime(s_text,'%d-%b-%Y')        
    except:
        s_dt = datetime(year=1900,month=1,day=1)            
    try:
        e_dt = datetime.strptime(e_text,'%d-%b-%Y')        
    except:
        e_dt = datetime(year=2012,month=5,day=1)        
    
    #--set dt to the first day of the month
    e_dt = datetime(e_dt.year,e_dt.month,1)
    s_dt = datetime(s_dt.year,s_dt.month,1)
    wflist = ['ALL']              
    wn = 1    
    
    #--create a pws object   
    w = pws.pws(p,wn,u,dia,dep,cas,wfield=wflist,dril=s_dt,aban=e_dt)
    wells.append(w) 
    shp_plist_full.append(p)  
    if p not in shp_plist:
        shp_plist.append(p)
        #shp_wflist.append({})
        #for wf in wflist:                
        #    shp_wflist[0][wf] = [wn]
        
print len(wells),' nonpws polygons converted to well objects'        

#---------------------------------------------------------------------
#--load the pumpage
print 'loading pumpage XLS...'
data_file = 'source_spreadsheets\\BrowardNon-PWSpumpage-all.xls'
plist,dlist = load_pws_data(data_file)
print len(plist),'records loaded from XLS'

#---------------------------------------------------------------------
#--build a record for each unique well
#--expressions to identify record type - very trail and error
accum = re.compile('permit',re.IGNORECASE)
part = re.compile('biscayne|surficial|lake|pond|canal',re.IGNORECASE)
indiv = re.compile('well|pump',re.IGNORECASE)

#---------------------------------------------------------------------
#--build well records
wnlist = []
rqlist = []
prtlist = []
notfound = []
f_warn = open('process_nonpws.wrn','w')
wr = shapefile.writer_like(shapename)

#--data_list = [[name],[reqm],[datetime],[val]]
for p,nlist,rlist,dtlist,vlist in zip(plist,dlist[0],dlist[1],dlist[2],dlist[3]):
    if p not in shp_plist:
        print 'permit not found:',p
        notfound.append(p)
    else:            
        print 'processing permit,date:',p
        idx = shp_plist_full.index(p)
        wr.poly([shapes[idx].points],shapeType=shapes[idx].shapeType)
        wr.record(records[idx])

        #--get the well objects for this permit
        p_wells = []
        for w in wells:
            if w.perm_no == p:
                p_wells.append(w)
                        
        wnlist.append([])
        rqlist.append([])
        for n,r,dt,v in zip(nlist,rlist,dtlist,vlist):        
            #print r
            
            #--if this is an accumulated record for the permit
            if accum.search(n) != None or p == r:                                                
                #--find the number of active wells for this date
                a_wells = []
                for w in p_wells:
                    if w.active(dt):
                        a_wells.append(w)
                if len(a_wells) == 0:
                    raise IndexError,'no active wells found for accumulated '+\
                          'permit,date'+str(p)+' '+str(dt)
                else:
                    q_well = v / (float(len(a_wells)))
                    for w in a_wells:
                        w.add_record(pws.ACCUM,dt,q_well)                        
                           

            #--if this is a partially accumulated or an individual record
            #--accumulate multiple entries for the same month
            #elif part.search(n) != None or indiv.search(n) != None:                 
            else:
                #--find wells that are active for this dt
                a_wells = []
                for w in p_wells:
                    if w.perm_no == p:
                        if w.active(dt):
                            a_wells.append(w)
                if len(a_wells) == 0:
                    #raise IndexError,'no active wells found for partial'+\
                    #      ' permit,date '+str(p)+' '+str(dt)+' '+n                            
                    f_warn.write('WARNING - no active wells found for partial'+\
                          ' permit,date '+str(p)+' '+str(dt)+' '+n+'\n')        
                
                else:
                    q_well = v / (float(len(a_wells)))
                    for w in a_wells:
                        w.add_record(pws.PART,dt,q_well,accum_dt=True)
                                                                                           
            
            #--problem record
            #else:                
            #    #raise IndexError,'permit,well not found'+str(p)+' '+str(wname)                                 
            #    f_warn.write('WARNING - permit,date,string not found '+\
            #                    str(p)+' '+str(dt)+str(n)+'\n')                                  
            #                                                          


wr.save('..\\_gis\\scratch\\nonpws_points_with_records')
f_warn.close()
#--save well records
for w in wells:
    w.write_records('nonpws_records\\')
    #break

#--------------------------------------------------------------------
#--error checking                

#--missing permits
if len(notfound) > 0:
    f_out = open('missing_permits.dat','w')
    for nf in notfound:
        f_out.write(nf+'\n')
    f_out.close()            
                                        