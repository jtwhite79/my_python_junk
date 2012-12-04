import sys
import numpy as np
import xlrd
import shapefile


#--get a unique list of wl and qw site numbers
#--wl
fname = 'broward_wl_result_data.csv'
f = open(fname,'r')
header_wl = f.readline().strip().split(',')
for i,h in enumerate(header_wl):
    if 'site_no' in h:
        siteno_idx = i
siteno_all = []
for line in f:
    siteno_all.append(line.strip().split(',')[siteno_idx])
f.close()
    
wl_siteno = []
for siteno in siteno_all:
    if float(siteno) not in wl_siteno:
        wl_siteno.append(float(siteno))

#--qw
fname = 'broward_qw_result_data.csv'
f = open(fname,'r')
header_qw = f.readline().strip().split(',')
for i,h in enumerate(header_qw):
    if 'site_no' in h:
        siteno_idx = i
siteno_all = []
for line in f:
    siteno_all.append(line.strip().split(',')[siteno_idx])
f.close()    
qw_siteno = []
for siteno in siteno_all:
    if float(siteno) not in qw_siteno:
        qw_siteno.append(float(siteno))

print len(wl_siteno),'unique wl site numbers'
print len(qw_siteno),'unique qw site numbers'
                   
fname = 'broward_sites_master.csv'
f = open(fname,'r')
header = f.readline().strip().split(',')
#print header


#--create a shapefile writer instance, one for nad27 and one for nad83
wr83 = shapefile.Writer()
wr27 = shapefile.Writer()
for h in header:
    typ = 'C'
    wr83.field(str(h),fieldType='C',size=50)
    wr27.field(str(h),fieldType='C',size=50)
#-- additional field for qw or wl
wr83.field('data_type',fieldType='C',size=2)
wr27.field('data_type',fieldType='C',size=2)

x_idx = 4
y_idx = 3
datum_idx = 5
siteno_idx = 1

for line in f:
    raw = line.strip().split(',')
    idx_offset = len(raw) - len(header)
    #if len(raw) != len(header):
    #    print line
    #    raise IndexError,'extra damn commas again'    
    siteno = int(raw[siteno_idx])
    if siteno in wl_siteno:
        raw.append('wl')
    elif siteno in qw_siteno:
        raw.append('qw')
    else:
        raise IndexError,'site number not found as wl or qw site:'+str(siteno)                
    x,y = float(raw[x_idx+idx_offset]),float(raw[y_idx+idx_offset])
    datum = raw[datum_idx+idx_offset]
    if 'NAD83' in datum:
        wr83.poly([[[x,y]]],shapeType=1)
        wr83.record(raw)
        #print '83'
    elif 'NAD27' in datum:        
        wr27.poly([[[x,y]]],shapeType=1)
        wr27.record(raw)                
        #print '27'
    else:
        raise TypeError,'unrecognized datum'        
    
    #wr.record(raw)
    #break
wr83.save('broward_nwis_sites_83')    
wr27.save('broward_nwis_sites_27')    
    

