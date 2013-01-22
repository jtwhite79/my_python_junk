import numpy as np
from mf import *

xmin,xmax = 0.0,1.0
ymin,ymax = 0.0,1.0
zmin,zmax = -1.0,0.0

c_nrow,c_ncol,c_nlay = 3,4,2
f_nrow,f_ncol,f_nlay = 4,7,3

c_delc = (ymax - ymin) / c_nrow
c_delr = (xmax - xmin) / c_ncol

f_delc = (ymax - ymin) / f_nrow
f_delr = (xmax - xmin) / f_ncol

c_botm = []
c_laythk = (zmax - zmin) / c_nlay
for k in range(c_nlay):
    c_botm.append(zmax - (c_laythk * (k + 1)))

f_botm = []
f_laythk = (zmax - zmin) / f_nlay
for k in range(f_nlay):
    f_botm.append(zmax - (f_laythk * (k + 1)))



#--coarse model
c_modelname = 'coarse'
c_mf = modflow(c_modelname,external_path='ref_coarse\\',load=False)
dis = mfdis(c_mf,c_nrow,c_ncol,c_nlay,nper=1,delr=c_delr,delc=c_delc,laycbd=0,\
            top=zmax,botm=c_botm)
c_mf.write_input()    

#--fine model
f_modelname = 'fine'
f_mf = modflow(f_modelname,external_path='ref_fine\\',load=False)
dis = mfdis(f_mf,f_nrow,f_ncol,f_nlay,nper=1,delr=f_delr,delc=f_delc,laycbd=0,\
            top=zmax,botm=f_botm)
f_mf.write_input()   

