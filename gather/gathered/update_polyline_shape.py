import sys
import calendar
import shutil
import numpy as np
from numpy import ma
import pylab
import MFBinaryClass as mfb
import shapefile
import arrayUtil as au
import swr

def load_swr_ibnd(file):
    irch = []
    ibnd = []
    f = open(file,'r')
    for line in f:
        if line[0] != '#' and line != '':
            raw = line.strip().split()
            irch.append(int(raw[0]))
            ibnd.append(int(raw[1]))
    f.close()
    return np.array([irch,ibnd]).transpose()



shape_dir = 'shapes\\'
reach_shpfile = shape_dir+'polylines_active'
reach_shp = shapefile.Reader(reach_shpfile)
num_records = reach_shp.numRecords
polylines = reach_shp.shapes()
poly_recs = reach_shp.records()
polyline_header = reach_shp.dbfHeader()

col_idx = 10
row_idx = 11
rch_idx = 12
rchgrp_idx = 13
conn_idx = 14
nconn_idx = 15
len_idx = 16
grp_len_idx = 17
ibnd_idx = 18
iroute_idx = 25
rgpnum_idx = 26
init_idx = 27

wr = shapefile.Writer()
for i,item in enumerate(polyline_header):
    #print i,item
    wr.field(item[0],fieldType=item[1],size=item[2],decimal=item[3])
#wr.field('iroutetype',fieldType='N',size=10,decimal=0)

f = open('swr_full\\swr_ds4a.dat','r')
header = f.readline()
header += f.readline()
f.close()
ds4a = np.loadtxt('swr_full\\swr_ds4a.dat',skiprows=2)
ds4b = swr.load_ds4b('swr_full\\swr_ds4b.dat')
ds6 = np.loadtxt('swr_full\swr_ds6.dat',usecols=[0,1])  
ds14a = np.loadtxt('swr_full\\swr_ds14a.dat',usecols=[0,1])

shutil.copy('swr_full\\swr_ds6.dat','swr_full\\swr_ds6_bak.dat')
shutil.copy('swr_full\\swr_ds4a.dat','swr_full\\swr_ds4a_bak.dat')


#--build swr internal rgpnum
rgpnum = []
irgpnum = []
rgpnum_count = 1
for rg in ds4a[:,2]:
    if rg not in irgpnum:
        rgpnum.append(rgpnum_count)
        rgpnum_count += 1
        irgpnum.append(rg)

#--calc new group lengths
rg_names,rg_len = [],[]
for rg,leng in zip(ds4a[:,2],ds4a[:,-1]):
    if rg in rg_names:
        idx = rg_names.index(rg)
        rg_len[idx] += leng
    else:
        rg_names.append(rg)
        rg_len.append(leng)

reach_names,reach_rg_len = [],[]
for reach,rg in zip(ds4a[:,0],ds4a[:,2]):
    reach_names.append(reach)
    reach_rg_len.append(rg_len[rg_names.index(rg)])        
    
    

#--loop over each reach and update fields
ds4a_fmt = '%10d %10d %10d %10d %10d %10d %15.6e'
ds6_out = []
print 'processing reaches...'
for polyline,rec in zip(polylines,poly_recs):
    
    #this_rec = reach_shp.record(p)    
    this_reach = rec[rch_idx]   
    #print this_reach,
    this_ibnd = ds6[np.where(ds6[:,0]==this_reach),1][0][0]
    this_ds4a = ds4a[np.where(ds4a[:,0]==this_reach),:][0][0]
    this_ds4b = ds4b[this_reach]
    this_ds14a = ds14a[np.where(ds14a[:,0]==this_reach),1][0][0]
    this_conn = ''
    for c in this_ds4b:
        this_conn += str(c)+' '
    this_conn.strip()  
    this_rgpnum = rgpnum[irgpnum.index(this_ds4a[2])]  
    #print this_reach,this_ds14a
    #rec[rchgrp_idx] = this_ds4a[2]
    rec[rchgrp_idx] = this_rgpnum
    rec[conn_idx] = this_conn
    rec[nconn_idx] = len(this_ds4b)
    rec[len_idx] = this_ds4a[6]
    rec[col_idx] = this_ds4a[5]
    rec[row_idx] = this_ds4a[4]
    rec[ibnd_idx] = this_ibnd
    rec[iroute_idx] = this_ds4a[1]
    rec[rgpnum_idx] = this_rgpnum
    rec[grp_len_idx] = reach_rg_len[reach_names.index(this_reach)]
    rec[init_idx] = this_ds14a
    #f_out.write('{0:10.0f} {1:10.0f} # {2:10.0f}\n'.format(this_reach,this_ibnd,this_ds4a[2]))    
    #ds6_out.append('{0:10.0f} {1:10.0f} # {2:10.0f}\n'.format(this_reach,this_ibnd,this_ds4a[2]))
    ds6_out.append('{0:10.0f} {1:10.0f} # {2:10.0f}\n'.format(this_reach,this_ibnd,this_rgpnum))
    #this_ds4a[2] = this_rgpnum   
    ds4a[np.where(ds4a[:,0]==this_reach),2] = this_rgpnum
                    
    wr.poly([polyline.points],shapeType=3)
    wr.record(rec)
wr.save(shape_dir+'polylines_active')

f_out = open('swr_full\\swr_ds6.dat','w')
for line in ds6_out:
    f_out.write(line)
f_out.close()
f_out = open('swr_full\\swr_ds4a.dat','w')
f_out.write(header)
np.savetxt(f_out,ds4a,fmt=ds4a_fmt)
f_out.close()
