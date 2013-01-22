import os
import numpy as np
import matplotlib.pyplot as mpl

from flopy2.modflow import *

#--this isn't needed except for the demo
from flopy2.utils import *

name = 'lake_example'

#--external dir
if not os.path.exists('ref\\'):
    os.mkdir('ref\\')

nlay = 10
n = 101
l = 400.0
h = 50.0
k = 1.0
nhalf = (n-1)/2.0

ibound = np.ones((nlay,n,n))
ibound[:,0,:] = -1
ibound[:,-1,:] = -1
ibound[:,:,0] = -1
ibound[:,:,-1] = -1
ibound[:,nhalf,nhalf] = 100.0

#--free format external example
#ml = Modflow(modelname=name,exe_name='mfnwt-SWR_x64.exe',external_path='ref\\')
#setattr(ml,'free_format',True)

#--fixed format external example
#ml = Modflow(modelname=name,exe_name='mfnwt-SWR_x64.exe',external_path='ref\\')


#--free format internal example
#ml = Modflow(modelname=name,exe_name='mfnwt-SWR_x64.exe')
#setattr(ml,'free_format',True)

#--fixed format internal example
ml = Modflow(modelname=name,exe_name='mfnwt-SWR_x64.exe')
#setattr(ml,'free_format',False)

#--just for demo
#--create an instance with a constant
u2d = util_2d(ml,(n,n),np.int,1,name='junk')
#--the type int
print u2d.vtype
#--by accessing the array by slice, an ndarray is created on the fly
u2d[0,:] = -4
#--now the dtype is ndarray
print u2d.vtype


hlay = h / nlay
#-create a bot list of mixed scalars and ndarrays
bot = []
for i in range(1,nlay):
    #--scalars
    bot.append(-float(i)/nlay*h)
    #--filenames
    #bot.append('ref\\botm_'+str(i)+'.ref')
    
bot.append(np.zeros((n,n))-h)
delr = delc = l/(n-1)
dis = ModflowDis(ml,nlay,n,n,delr=delr,delc=delc,top=0.0,botm=bot,laycbd=0)

strt = 100.0 * np.ones((n,n))
strt[nhalf,nhalf] = 90.0
bas = ModflowBas(ml,ibound=ibound,strt=strt)

lpf = ModflowLpf(ml,laytyp=0,hk=k,vka=k)
oc = ModflowOc(ml)
pcg = ModflowPcg(ml)

ml.write_input()
ml.run_model3()




