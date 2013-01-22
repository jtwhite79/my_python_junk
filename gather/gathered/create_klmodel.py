import os
import sys
import shutil
import numpy as np
from mf import *
from mt import *
from mswt import *
from mfaddoutsidefile import mfaddoutsidefile
import kl_config

def loadtxt(nrow,ncol,file):
	'''
	read 2darray from file
	file(str) = path and filename
	'''
	try:
		file_in = open(file,'r')
		openFlag = True
	except:
#		assert os.path.exists(file)
		file_in = file
		openFlag = False
	
	data = np.zeros((nrow*ncol),dtype='double')-1.0E+10
	d = 0
	while True:
		line = file_in.readline()
		if line is None or d == nrow*ncol:break
		raw = line.strip('\n').split()
		for a in raw:
			try:
				data[d] = float(a)
			except:
				print 'error casting to float on line: ',line
				sys.exit()
			if d == (nrow*ncol)-1:
				assert len(data) == (nrow*ncol)
				data.resize(nrow,ncol)
				return(data) 
			d += 1	
	file_in.close()
	data.resize(nrow,ncol)
	return(data)


modelname = 'kltest'
ref_dir = 'ref\\'
mf = modflow(modelname,external_path=ref_dir,load=False)

#nrow, ncol, nlay = 20,200,10
#delr,delc = 500.,500.
nrow,ncol,nlay = kl_config.nrow,kl_config.ncol,1
delr,delc = kl_config.delr,kl_config.delc                        
top = 10.0
botm = -100.0

nstp = 1
nper = 1
perlen = np.ones((nper))
steady = [True]

for n in range(nper-1):   
    steady.append(False)

dis = mfdis(mf,nrow,ncol,nlay,nper=nper,delr=delr,delc=delc,laycbd=0,\
            top=top,botm=botm,perlen=perlen,nstp=nstp,steady=steady)
ibound = np.ones((nrow,ncol),dtype=np.int32)

#--set ghbs is col 1
ghb_lrchc = []
for r in range(nrow):
    for l in range(nlay):
        ghb_lrchc.append(np.array([l+1,r+1,1,10.0,100.0]))       
#--set ghbs along the right side
for r in range(nrow):
    for l in range(nlay):
        ghb_lrchc.append(np.array([l+1,r+1,ncol,0.0,100.0]))
        

init_heads = np.zeros((nrow,ncol))
bas = mfbas(mf,ibound=ibound,strt=init_heads)
hk = 'real1.ref'
#--convert from stupid wrapped format to free
arr = (loadtxt(nrow,ncol,hk))

np.savetxt('hk.ref',arr,fmt=' %15.6e')

lpf = mflpf(mf,hk=arr,vka=arr,laytyp=1)
gmg = mfgmg(mf,mxiter=1000,hclose=1e-2,rclose=1e-2)
oc = mfoc(mf,words=['head','budget'],save_head_every=1)
ghb = mfghb(mf,layer_row_column_head_cond=[ghb_lrchc])

#--run modflow to generate swr-equivalent river package
mf.write_input()    
os.system('MF2005-SWR_x64.exe '+modelname)

