import sys
import os
import math
import shapefile
import numpy as np
import swr

#--the fields to put in the shapefile
ds_13a_in = [8,10]
ds_13b_in = [0,4,5,6,7]

#--load the swr structure records
ds_13a = swr.ds_13a('..\\500_grid_setup\\swr_full\\swr_ds13a_working_strval.dat')
ds_13a.load_structures()
#for s in ds_13a.structures:
#    print s['a_com']

#sys.exit()
#--load the structure shapefile
file = 'she_structures_culverts_1.shp'
shp = shapefile.Reader(shapefile=file)
nrec = shp.numRecords
records = shp.records()
shapes = shp.shapes()
dbf_header = shp.dbfHeader()

#--the dbf attribute index of the reach identifier
bname_idx = 0
sname_idx = 1
stype_idx = 2
chain_idx = 3

#--set the writer instance
wr = shapefile.Writer()
wr_fnames = []
for item in dbf_header:
    wr.field(item[0],fieldType=item[1],size=item[2],decimal=item[3])
    wr_fnames.append(item[0])
#for name in swr.ds_13a_english:
for idx in ds_13a_in:
    wr.field(swr.ds_13a_english[idx],fieldType='C',size=20)
    wr_fnames.append(swr.ds_13a_h[idx])
#for name in swr.ds_13b_english:
for idx in ds_13b_in:
    wr.field(swr.ds_13b_english[idx],fieldType='C',size=20)    
    wr_fnames.append(swr.ds_13b_h[idx])

found = []
for shape,rec in zip(shapes,records):
    bname = rec[bname_idx]
    sname = rec[sname_idx]
    stype = rec[stype_idx]
    chain = rec[chain_idx]
    #print stype
    if 'culvert' not in stype:
        #print bname,sname,stype,chain
        
        #--find this structure is the swr records    
        s_idx = None    
        for i,s in enumerate(ds_13a.structures):
            a_com = s['a_com']                       
            if bname in a_com[0] and sname in a_com[2]:                              
                s_idx = i            
                found.append(i)            
                break       
        #--now try to find ones with spaces on the names            
        if s_idx is None:        
            for i,s in enumerate(ds_13a.structures):
                if i not in found:
                    a_str = ' '.join(s['a_com'])
                    if bname in a_str and sname in a_str:
                        #print bname,sname,chain,a_str
                        s_idx = i
        #--if still not found...            
        if s_idx is None:
            print 'WARNING - structures not found',bname,sname,stype                    
        
        #--add the attributes to the record
        else:
            s = ds_13a.structures[s_idx]                        
            for i in ds_13a_in:
                fname = swr.ds_13a_h[i]                            
                if fname.lower() in s.keys():
                    print fname
                    rec.append(str(s[fname.lower()]))
                else:
                    rec.append('na')                                                
            for i in ds_13b_in:
                fname = swr.ds_13b_h[i]                            
                if fname.lower() in s.keys():
                    print fname
                    rec.append(str(s[fname.lower()]))
                else:
                    rec.append('na')                    
   
            wr.poly([shape.points],shapeType=1)
            wr.record(rec)
    
wr.save('model_structures')    