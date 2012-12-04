from datetime import datetime,timedelta
import numpy as np
import pandas

rch_mult = 0.083 #inches to feet
ets_mult = 0.003281 #mm to feet

modelname = 'bro'
seawatname = 'bro_seawat'
try:
    ibound = np.loadtxt('ref\\ibound_CS.ref')
    top = np.loadtxt('ref\\top_mod.ref')
except:
    pass

nrow,ncol = 411,501


#--layer specific stuff
nlay = 1
#layer_botm_names = ['Q5','Q4','Q3','Q2','Q1','T3','T1']
#layer_botm_names = ['Q3','Q1','T1']
layer_botm_names = ['T1']
ghb_layers = [1]

delr,delc = 500.0,500.0
#offset = [728600.0,782850.0]
offset = [728600.0,577350.0]
start = datetime(year=1950,month=1,day=1)
end = datetime(year=2012,month=5,day=31)
pandas_freq = '1M'
sp_end = pandas.date_range(start,end,freq=pandas_freq)
sp_start = [start]
sp_start.extend(list(pandas.date_range(start,end,freq=pandas_freq) + timedelta(days=1)))

sp_len = []
for i in range(1,len(sp_start)):
    sp_len.append(sp_start[i] - sp_start[i-1])
sp_start.pop(-1)
sp_start = pandas.DatetimeIndex(sp_start)
assert len(sp_start) == len(sp_end)
assert len(sp_len) == len(sp_end)
nper = len(sp_start)


 
#--plotting stuff
x = np.arange(0,ncol*delr,delr) + offset[0]
y = np.arange(0,nrow*delc,delc) + offset[1]
X,Y = np.meshgrid(x,y)
plt_x = [825000.0,x.max()]
plt_y = [offset[1],712000.0]
  
    