import re
import sys
import math
import numpy as np
import shapefile    


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

#print 'nrow,ncol',nrow,ncol    
#print 'delc,delr',len(delc),len(delr)
#sys.exit()

offset = [462593.111,1335200.686,15]

#--flip the delr since we moved the orgin to lower left
delr = np.flipud(np.array(delr))
delc = (np.array(delc))

#--sum the lengths along the vectors
delr_cum = np.cumsum(delr)
delc_cum = np.cumsum(delc)

#print delr_cum.shape,delc_cum.shape
#sys.exit()

#--insert '0' in the first position 
xoff = np.hstack((0,delc_cum))
yoff = np.hstack((0,delr_cum))

wr = shapefile.Writer()
wr.field('row',fieldType='N',size=20)
wr.field('column',fieldType='N',size=20)
wr.field('delx',fieldType='N',size=20)
wr.field('dely',fieldType='N',size=20)
wr.field('cellnum',fieldType='N',size=20)

cell_count = 0


for c in range(0,ncol):
    print 'column ',c+1,' of ',ncol
    for r in range(0,nrow):
        
        #--calc the box points relative to the grid
        #print nrow,ncol,r,c,yoff.shape
        lowleft = [xoff[c],yoff[r]]     
        lowright = [xoff[c+1],yoff[r]]  
        upright = [xoff[c+1],yoff[r+1]] 
        upleft = [xoff[c],yoff[r+1]]            
        
        this_box = [lowleft,lowright,upright,upleft]
        
        #--if rotation is non-zero
        if offset[2] != 0.0:
            this_box = rotate(this_box,offset[2])
        
        #--add the offset in after the rotation
        this_box = add_offset(this_box,offset)
        
        #print nrow-r,c+1

        wr.poly(parts=[this_box], shapeType=5)
        wr.record([nrow-r,c+1,delr[r],delc[c],cell_count])
        cell_count += 1
        #break
    #break
        
wr.save(target='model')
    