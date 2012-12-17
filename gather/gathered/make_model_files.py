import re
import sys
import math
import numpy as np
import shapefile

from mf import *
from mfreadbinaries import *
from mt import *
from mswt import *
from numpy import *
from mfaddoutsidefile import mfaddoutsidefile



def free_u1drel(length,file):
    line = file.readline().strip().split()
    data = []
    if line[0].upper() == 'CONSTANT':
        for l in range(length): data.append(float(line[1]))
        
    elif line[0].upper() == 'INTERNAL': 
        cnst = float(line[1])       
        for l in range(length):
            dline = f.readline().strip()
            data.append(float(dline) * cnst)
    
    elif line[0].upper() == 'EXTERNAL':
        raise NameError('External not supported')
    
    elif line[0].upper() == 'OPEN/CLOSE':
        cnst = float(line[2])
        f2 = open(line[1])
        for l in range(length):
            dline = f2.readline()
            #print dline,length
            data.append(float(dline.strip()) * cnst)
        f2.close
    else:
        raise TypeError('unrecognized keyword: '+line[0].upper())
    
    return data

def load_dis_file(file): 
    f = open(file,'r')
    off = re.compile('offset',re.IGNORECASE)
    
    #--read comment lines
    #--try to get the offset
    while True:
        line = f.readline()
        if line[0] != '#': break
        if off.search(line) != None:
            try:
                raw = line.strip().split('=')[-1].split(',')
                xoff = float(raw[0])
                yoff = float(raw[1])
                rotation = float(raw[2])
                offset = [xoff,yoff,rotation]
            except:
                print 'offset not found in dis file header...continuing'
                offset = [-999,-999]
    
    #--parse the first line
    raw = line.split()
    nlay = int(raw[0])
    nrow = int(raw[1])
    ncol = int(raw[2])
    nper = int(raw[3])
    itmuni = int(raw[4])
    lenunit = int(raw[5])   
    
    #--parse the laycbd line
    line = f.readline()
    raw = line.strip().split()
    if len(raw) != nlay:
        raise IndexError('need '+str(nlay)+' entries for dataset 2')
    laycbd = []
    for r in raw : laycbd.append(float(r))
    
    
    delr = free_u1drel(ncol,f) 
    delc = free_u1drel(nrow,f)
                            
    return offset,nlay,nrow,ncol,np.array(delr),np.array(delc)
                                           

def rotate(box,angle):
    new_box = []
    sin_phi = math.sin(angle*math.pi/180.0)
    cos_phi = math.cos(angle*math.pi/180.0)
    #print sin_phi,cos_phi
    for point in box:
        new_x = (point[0] * cos_phi) - (point[1] * sin_phi)
        new_y = (point[0] * sin_phi) + (point[1] * cos_phi)
        new_box.append([new_x,new_y])
    return new_box                                   


def add_offset(box,offset):
    for point in box:
        point[0] += offset[0]
        point[1] += offset[1]
    return box
f = open('gridin6.TXT','r')
raw = f.readline().strip().split()
nrow,ncol = int(raw[0]),int(raw[1])
rot = float(f.readline().strip())
org_offset = f.readline()

delc = []
while True:
    line = f.readline() 
    if 'END' in line: break
    raw = line.strip().split(',')
    for r in raw:
        if '*' in r:
           r2 = r.split('*')
           num = int(r2[0])
           space = float(r2[1])
           for n in range(num):
               #print space
               delc.append(space)
        elif r != '':
            #print r
            delc.append(float(r))

delr = []
while True:
    line = f.readline() 
    if 'END' in line: break
    raw = line.strip().split(',')
    for r in raw:
        if '*' in r:
           r2 = r.split('*')
           num = int(r2[0])
           space = float(r2[1])
           for n in range(num):
               #print space
               delr.append(space)
        elif r != '':
            #print r
            delr.append(float(r))

print 'nrow,ncol',nrow,ncol    
print 'delc,delr',len(delc),len(delr)

np.savetxt('delc.dat',delc,fmt='%15.6g')
np.savetxt('delr.dat',delr,fmt='%15.6g')

offset = [462593.111,1335200.686,15]

nrow = len(delc)
ncol = len(delr)
nlay = 3

top = 'ref_shp\\elevation_array.ref'
top_array = np.loadtxt(top)
print top_array.min()
botm = [top_array.min()-1.0,-20.,-300.]

nper = 1
perlen = [10000000.0]
nstp = [1]
#--flip the delc since we moved the orgin to lower left
delr = (np.array(delr))
delc = np.flipud(np.array(delc))

modelname = 'tsala'

mf = modflow(modelname,external_path='ref\\',load=True)
dis = mfdis(mf, nrow, ncol, nlay, nper =nper, delr = delr, delc = delc, laycbd = 0,\
            top = top, botm = botm, perlen = perlen, nstp = nstp,steady=False)



#--ibound
#--31=north,32=east,33=south,34=west
ibound = np.loadtxt('ref_shp\\ibound_array.ref',dtype=np.int32)
init_heads = ['ref\\init_heads_1.ref','ref\\init_heads_2.ref','ref\\init_heads_3.ref']

bas = mfbas(mf,ibound,init_heads)

#--set ghbs along the coast
ghb_list = []
ghb_stage = 0.0
ghb_cond = 10000000000.0
for i in range(nrow):
    for j in range(ncol):
        if ibound[i,j] == 34:
            for k in range(nlay):
                ghb_list.append([k+1,i+1,j+1,ghb_stage,ghb_cond])       

lpf = mflpf(mf,hk=[10.0,0.1,500.],vka=[10.0,0.1,500.],laytyp=1)
gmg = mfgmg(mf,mxiter=1000,hclose=1e-2,rclose=1e-2)
oc = mfoc(mf,words=['head','budget'],save_head_every=1)
ghb = mfghb(mf,layer_row_column_head_cond=[ghb_list])

rch = mfrch(mf,rech=0.000114,external=False)    

swr = mfaddoutsidefile(mf,'SWR','swr',25)
mf.add_external('tsala.fls',101,binflag=True)
mf.add_external('tsala.stg',102,binflag=True)
mf.add_external('tsala.aqx',103,binflag=True)
mf.add_external('tsala.pqm',104,binflag=True)
mf.add_external('tsala.str',105)
mf.add_external('tsala.riv',106)

mf.write_input()

os.system('MF2005-SWR_x64.exe tsala.nam')
