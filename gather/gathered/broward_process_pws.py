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
shp_plist = []
for r in records:
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
          
    #if wn.endswith('A'):
    #   wn = wn[:-1]
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
    if p not in shp_plist:
        shp_plist.append(p)
        #shp_wflist.append({})
        #for wf in wflist:                
        #    shp_wflist[0][wf] = [wn]
        
    #else:
    #    idx = shp_plist.index(p)        
    #    for wf in wflist:       
    #        if wf in shp_wflist[idx]:         
    #            shp_wflist[idx][wf].append(wn)                                
    #        else:                
    #            shp_wflist[idx][wf] = [wn]     

#--error checking            
#for p,wf in zip(shp_plist,shp_wflist):    
#    for key,wnlist in wf.iteritems():
#        print p,key,' '.join(wnlist)

        
#---------------------------------------------------------------------
#--load the pumpage
data_file = 'source_spreadsheets\\BrowardPWSpumpage-allOct2012.xls'
#data_file = 'source_spreadsheets\\prosepct_test.xls'
plist,dlist = load_pws_data(data_file)

#---------------------------------------------------------------------
#--build a record for each unique well

#--expressions to identify record type - very trail and error
accum = re.compile('biscayne|permit|P.S.|aka',re.IGNORECASE)
part = re.compile('wellfield|Wf|plant|Wellield|City Wells|&|and',re.IGNORECASE)
prob = re.compile('wells',re.IGNORECASE)
indiv = re.compile('well\s',re.IGNORECASE)
skip = re.compile('ASR|floridan|fas',re.IGNORECASE)


#---------------------------------------------------------------------
#--build well records
wnlist = []
rqlist = []
prtlist = []
notfound = []
f_warn = open('process_pws.wrn','w')
#--data_list = [[name],[reqm],[datetime],[val]]
for p,nlist,rlist,dtlist,vlist in zip(plist,dlist[0],dlist[1],dlist[2],dlist[3]):
    if p not in shp_plist:
        print 'permit not found:',p
        notfound.append(p)
    else:    
        print 'processing permit,date:',p
        #--get all well objects for this permit
        p_wells = []
        for w in wells:
            if w.perm_no == p:
                p_wells.append(w)
                               
        wnlist.append([])
        rqlist.append([])
        for n,r,dt,v in zip(nlist,rlist,dtlist,vlist):        
            #print r
            
             #--record to skip
            if skip.search(n) != None:
                skp = 1   

            #--if this is an accumulated record for the permit
            elif accum.search(n) != None or p == r:                                                
                #--find the number of active wells for this date
                a_wells = []
                for w in p_wells:
                    if w.active(dt):
                        a_wells.append(w)
                if len(a_wells) == 0:
                    #raise IndexError,'no active wells found for accumulated '+\
                    #      'permit,date'+str(p)+' '+str(dt)
                    f_warn.write('WARNING - no active wells found for accumulated '+\
                          'permit,date'+str(p)+' '+str(dt)+'\n')
                else:
                    q_well = v / (float(len(a_wells)))
                    for w in a_wells:
                        w.add_record(pws.ACCUM,dt,q_well,accum_dt=True)                        
                
            #--if this is an individual record    
            elif indiv.search(n) != None:
                raw = n.strip().split()
                #--look for the key word 'well ' in the name
                for i,rr in enumerate(raw):
                    if indiv.search(rr+' ') != None:
                        wname = raw[i+1]
                        #--sunrise southwest inconsistency
                        if 'SW' in n.upper():                           
                            wnum = int(raw[-1])
                            wname = 'SBU-'+str(wnum)

                        #--south broward inconsistency
                        if 'SBU ' in n.upper():
                            #print n
                            wname = 'SBU-'+raw[i+2]
                        #--ftl inconsistency
                        elif 'PROSPECT' in wname.upper() or 'DIXIE' in wname.upper():
                            wname = wname.split('-')[0]
                        
                        #--some junk to cleanup well names
                        try:
                            if raw[i+2].upper() == 'WEST' or\
                               raw[i+2].upper() == 'EAST' or\
                               raw[i+2].upper() == 'NORTH' or\
                               raw[i+2].upper() == 'SOUTH' or\
                               raw[i+2].upper() == 'CENTRAL':
                                wname = wname + ' ' +raw[i+2]
                        except:
                            pass                                
                        #--davie inconsistency                      
                        if wname.upper().startswith('B1'):
                            wnum = int(wname.split('-')[-1])                            
                            wname = str(wnum) + ' NORTH' 
                        elif wname.upper().startswith('B3'):
                            wnum = int(wname.split('-')[-1])                            
                            wname = str(wnum) + ' SOUTH'
                        
                        #--pembroke inconsistency
                        if wname.upper().startswith('PP2'):
                            wname = '2 CENTRAL'
                        elif wname.upper().startswith('PP1'):
                            wname = '1 CENTRAL'
                        
                        #--find the well with this name
                        ww = None
                        wname = str(wname).upper()    
                        for w in p_wells:                            
                            #print w.well_no.upper(),wname
                            if w.well_no.upper() == wname:
                                ww = w
                                break
                        if ww == None:
                            #raise IndexError,'permit,well not found'+str(p)+' '+str(wname)                                 
                            f_warn.write('WARNING - permit,well,date not found '+\
                                   str(p)+' '+str(wname)+' '+str(dt)+'\n')                                 
                        else:
                            ww.add_record(pws.INDIV,dt,v)
                                                                               
                        if wname not in wnlist[-1]:
                            wnlist[-1].append(wname)
                            rqlist[-1].append(r)
            
            #--if this is a partially accumulated record
            elif part.search(n) != None or\
                 r == 100527 or r == 100526 or\
                 r == 137073 or r == 100649:
                #--find wells with this wfield and that are active for this dt
                a_wells = []
                for w in p_wells:
                    if w.perm_no == p:
                        if w.check_wfield(n) and w.active(dt):
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
                                                                           
                if [p,n] not in prtlist:
                    prtlist.append([p,n])            
            
            #--if this is a problem record
            elif prob.search(n) != None:             
                print 'prob:',p,n,dt,r
                            
            
            #--try to cast the first element in name to a well number
            else:
                wname = None
                try:
                    raw = n.strip().split()
                    wname = int(raw[0])
                    if str(wname).upper() not in wnlist[-1]:
                        wnlist[-1].append(str(wname).upper())
                        rqlist[-1].append(r)
                    #print wname
                except:                
                    pass
                
                #--find the well with this name
                if wname is None:
                     f_warn.write('WARNING - well not found '+n+'\n')
                else:                          
                    ww = None
                    wname = str(wname).upper()    
                    for w in p_wells:                            
                        #print w.well_no.upper(),wname
                        if w.well_no.upper() == wname:
                            ww = w
                            break
                    if ww == None:
                        #raise IndexError,'permit,well not found'+str(p)+' '+str(wname)                                 
                        f_warn.write('WARNING - permit,well,date not found '+\
                                       str(p)+' '+str(wname)+' '+str(dt)+'\n')                                  
                    else:
                        ww.add_record(pws.INDIV,dt,v)
                                                           

           

f_warn.close()
#--save well records
for w in wells:
    w.write_records('pws_smp_components\\')
    #break

#--------------------------------------------------------------------
#--error checking                

#--missing permits
if len(notfound) > 0:
    f_out = open('missing_permits.dat','w')
    for nf in notfound:
        f_out.write(nf+'\n')
    f_out.close()            
                                        

#--rectify partial record names
prtlist_found = []
for p,prt in prtlist:
    found = False
    for w in wells:
        if w.perm_no == p:
            if w.check_wfield(prt):
                found = True                
                break
                           
    prtlist_found.append(found)            
    #break    
#--save partial record name output file
f = open('partial_names.dat','w')
for [p,prt],fd in zip(prtlist,prtlist_found):
    f.write(p.ljust(20)+' '+str(fd)+' '+str(prt).ljust(20)+'\n')
f.close()     

#--rectify well names between the spreadsheet and the shapefile
#--build a list to track shape wells that are found

wnlist_found = []
for p,wwnlist in zip(plist,wnlist):
    #--for those permits with individual records
    #if len(wwnlist) > 0:
    wnlist_found.append([])
    for wn in wwnlist:
        f = False
        for i,w in enumerate(wells):
            #print w.well_no,wn
            if w.perm_no == p and w.well_no.upper() == wn:
                f = True                
                break
        wnlist_found[-1].append(f)
        #break
    #break
#--save well name output file
f = open('well_names.dat','w')
for p,wwn,wwf,rrq in zip(plist,wnlist,wnlist_found,rqlist):
    #print p,wwnlist
    for wn,wf,rq in zip(wwn,wwf,rrq):
        f.write(p.ljust(20)+' '+str(wn).ljust(20)+' '+str(wf).ljust(10)+' '+str(rq).ljust(10)+'\n')
f.close() 


sys.exit()
