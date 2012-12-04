import sys
import os
import math
import shapefile
import numpy as np
import swr


#--load the swr structure records
ds_13a = swr.ds_13a('older\\swr_full\\swr_ds13a_working_strval.dat')
ds_13a.load_structures()

#--load the structure shapefile
file = '..\\_gis\\shapes\\sw_structures'
shp = shapefile.Reader(shapefile=file)
nrec = shp.numRecords
records = shp.records()
shapes = shp.shapes()
dbf_header = shp.dbfHeader()

#--the dbf attribute index of the reach identifier
bname_idx = 0
sname_idx = 1
chain_idx = 3

#--set the writer instance
wr = shapefile.Writer()

field_names = []
for item in dbf_header:
    wr.field(item[0],fieldType=item[1],size=item[2],decimal=item[3])    
    field_names.append(item[0])

null_13a = []
for entry,fmt in zip(swr.ds_13a_h,swr.ds_13a_fmt):
    if 'd' in fmt:
        wr.field(entry,fieldType='N',size=10,decimal=0)
    elif 'e' in fmt:
        wr.field(entry,fieldType='N',size=20,decimal=7)
    else:
        wr.field(entry,fieldType='C',size=20)

    field_names.append(entry)
    null_13a.append('none')
    
null_13b = []
for entry,fmt in zip(swr.ds_13b_h,swr.ds_13b_fmt):
    if 'd' in fmt:
        wr.field(entry,fieldType='N',size=10,decimal=0)
    elif 'e' in fmt:
        wr.field(entry,fieldType='N',size=20,decimal=7)
    else:
        wr.field(entry,fieldType='C',size=20)
    field_names.append(entry)    
    null_13b.append('none')

for shape,rec in zip(shapes,records):
    bname = rec[bname_idx]
    sname = rec[sname_idx]   
    chain = rec[chain_idx]
    rec.extend(null_13a)
    rec.extend(null_13b)
  
    #--find this structure is the swr records    
    s_idx = None   
    found = [] 
    for i,s in enumerate(ds_13a.structures):
        com = s['comments']                       
        if bname in com[0] and sname in com[2]:                              
            s_idx = i                                 
            found.append(i)
            break       
    #--now try to find ones with spaces on the names            
    if s_idx is None:        
        for i,s in enumerate(ds_13a.structures):
            if i not in found:
                a_str = ' '.join(s['comments'])
                if bname in a_str and sname in a_str:                    
                    s_idx = i

    #--if still not found...            
    if s_idx is None:
        print 'WARNING - structures not found',bname,sname                   
        
    #--add the attributes to the record
    else:
        s = ds_13a.structures[s_idx]
        s_attrs,s_vals = s.keys(),s.values()                        
        if s['istrtype'] == 9:
            print
        for entry in swr.ds_13a_h:            
            if entry.lower() in s_attrs:
                val = s_vals[s_attrs.index(entry.lower())]
                idx = field_names.index(entry)
                rec[idx] = val
    
        for entry in swr.ds_13b_h:            
            if entry.lower() in s_attrs:
                val = s_vals[s_attrs.index(entry.lower())]
                idx = field_names.index(entry)
                rec[idx] = val                   
    
    wr.poly([shape.points],shapeType=shape.shapeType)
    wr.record(rec)
    
wr.save('..\\_gis\\scratch\\sw_structures_merge')   
