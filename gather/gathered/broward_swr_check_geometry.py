import os
import numpy as np

import shapefile
import swr


def perimeter(xsec):
    p = 0.0
    for [x0,z0],[x1,z1] in zip(xsec[:-1],xsec[1:]):
        len = np.sqrt((x0-x1)**2 + (z0-z1)**2)
        p += len
    return p

def between(v,v1,v2):
    if v >= v1 and v <= v2:
        return 1
    if v <= v1 and v >= v2:
        return -1
    return 0

def clip_xsec(zval,xsec):
    
       
    if xsec[0,1] < zval:
        xc = [xsec[0,0]]
        zc = [zval]
        x1,x2 = xsec[0,0],xsec[1,0]
        z1,z2 = xsec[0,1],xsec[1,1]
        if z1 == z2:
            xval = x1
        else:
            dxdz = (x1-x2)/(z1-z2)
            dz = z1 - zval 
            dx = dz * dxdz
            xval = x1 - dx    
            xc.append(xval)
            zc.append(zval)
        
    else:
        xc,zc = [],[]
    for i in range(1,xsec.shape[0]):
        sign = between(zval,xsec[i-1,1],xsec[i,1])
        if sign != 0:    
            x1,x2 = xsec[i-1,0],xsec[i,0]
            z1,z2 = xsec[i-1,1],xsec[i,1]
            if z1 == z2:
                xval = x1
            else:
                dxdz = (x1-x2)/(z1-z2)
                dz = z1 - zval 
                dx = dz * dxdz
                xval = x1 - dx    
            xc.append(xval)
            zc.append(zval)
        elif xsec[i,1] < zval:
            xc.append(xsec[i,0])
            zc.append(xsec[i,1])                               
    
    if zc and zc[-1] < zval:
        x1,x2 = xc[-2],xc[-1]
        z1,z2 = zc[-2],zc[-1]
        if z1 == z2:
            xval = x1
        else:
            dxdz = (x1-x2)/(z1-z2)
            dz = z1 - zval 
            dx = dz * dxdz
            xval = x1 - dx    
            xc.append(xval)
            zc.append(zval)                     
    xsec_c = np.array((xc,zc)).transpose()    
    return xsec_c
            
    #if not idxs:
    #    return xsec

    #xc,zc = [],[]         
    #
    #for x,z in xsec:                            
    #    if z < zval:
    #        xc.append(x)
    #        zc.append(z)
    #if len(idxs) > 2:
    #    
    #for i in idxs:
    #    x1,x2 = xsec[i[0],0],xsec[i[1],0]
    #    z1,z2 = xsec[i[0],1],xsec[i[1],1]
    #    if x1 == x2:
    #        xval = x1
    #    else:
    #        dxdz = (x1-x2)/(z1-z2)
    #        dz = z1 - zval 
    #        dx = dz * dxdz
    #        xval = x1 - dx
    #    if xval < xc[0]:
    #        xc.insert(0,xval)
    #        zc.insert(0,zval)
    #    else:
    #        xc.append(xval)
    #        zc.append(zval)


    #xsec_c = np.array((xc,zc)).transpose()    
    #return xsec_c

            



top = np.loadtxt('..\\_model\\bro.01\\ref\\top_mod.ref')

xsec_dir = 'xsec_navd\\'
xsec_files = os.listdir(xsec_dir)
xsecs = {}
for xname in xsec_files:    
    header,xsec = swr.load_xsec(xsec_dir+xname)
    xsecs[xname] = xsec
    
shapename = '..\\_gis\\scratch\\sw_reaches_conn_SWRpolylines'
shapes,records = shapefile.load_as_dict(shapename)
wr = shapefile.Writer()
wr.field('reach',fieldType='N',size=10,decimal=0)
wr.field('top',fieldType='N',size=20,decimal=10)
wr.field('xsec_min',fieldType='N',size=20,decimal=10)
wr.field('xsec_max',fieldType='N',size=20,decimal=10)
wr.field('xsec_depth',fieldType='N',size=20,decimal=10)
wr.field('mod_depth',fieldType='N',size=20,decimal=10)
wr.field('depth_diff',fieldType='N',size=20,decimal=10)
wr.field('xsec_perm',fieldType='N',size=20,decimal=10)
wr.field('mod_perm',fieldType='N',size=20,decimal=10)
wr.field('perm_diff',fieldType='N',size=20,decimal=10)
#print shapefile.get_fieldnames(shapename)
reaches = records['REACH']
rows = records['ROW']
cols = records['COLUMN']
xsec_names = records['SRC_pf_name']
nreaches = reaches.shape[0]
for shape,reach,row,col,xname in zip(shapes,reaches,rows,cols,xsec_names):
    print 'processing ',reach,xname
    if reach == 7005:
        pass
    xsec = xsecs[xname]    
    t = top[row-1,col-1]
    xsec_clp = clip_xsec(t,xsec)    
    xsec_perm = perimeter(xsec)
    mod_perm = perimeter(xsec_clp)
    xsec_depth = xsec[:,1].max() - xsec[:,1].min()
    mod_depth = t - xsec[:,1].min()
    depth_diff = (xsec_depth - mod_depth)/xsec_depth
    perm_diff = (xsec_perm - mod_perm)/xsec_perm
    wr.poly([shape.points],shapeType=shape.shapeType)
    rec = [reach,t,xsec[:,1].min(),xsec[:,1].max(),xsec_depth,mod_depth,depth_diff,xsec_perm,mod_perm,perm_diff]
    wr.record(rec)
    #if depth_diff > 0.6:
    #    print 'depth',reach,xsec_depth,mod_depth
    #if p_diff > 0.2:
    #    print 'perimeter',reach,p,p_mod
wr.save('..\\_gis\\scratch\\swr_reaches_compare')            

    