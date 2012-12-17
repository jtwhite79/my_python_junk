from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta
import numpy as np
import pandas
'''just a container for model details
'''


class bro:
    dir = 'bro.02\\'
    rch_mult = 0.083 #inches to feet
    ets_mult = 0.003281 #mm to feet

    rch_unit,ets_unit = 54,55
    well_unit,ghb_unit = 56,57

    start = datetime(year=2012,month=6,day=1)
    end = datetime(year=2112,month=5,day=31)
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
    slr_scenario = 'med_rise'    
   

class flow(bro):    
    root = 'flow'    
    name = bro.dir+root
    ref_dir = root + 'ref\\'
    list_dir = root + 'list\\'
    top_name,ibound_name = ref_dir+'top_mod.ref',ref_dir+'ibound_CS.ref'    
    try:
        top = np.loadtxt(top_name)
        ibound = np.loadtxt(ibound_name)
    except:
        pass
    nrow,ncol = 411,501
    #--layer specific stuff
    
    #layer_botm_names = ['Q5','Q4','Q3','Q2','Q1','T3','T1']
    #layer_botm_names = ['Q3','Q1','T1']
    layer_botm_names = ['T1']
    nlay = len(layer_botm_names)
    
    ghb_layers = [1]
    
    delr,delc = 500.0,500.0
    #offset = [728600.0,782850.0]
    offset = [728600.0,577350.0]

    #--plotting stuff
    x = np.arange(0,ncol*delr,delr) + offset[0]
    y = np.arange(0,nrow*delc,delc) + offset[1]
    X,Y = np.meshgrid(x,y)
    plt_x = [825000.0,x.max()]
    plt_y = [offset[1],712000.0]

class seawat(bro):
    root = 'seawat'
    name = bro.dir+root
    ref_dir = root + 'ref\\'
    list_dir = root + 'list\\'
    


    top_name,ibound_name = ref_dir+'top_mod.ref',ref_dir+'ibound_CS.ref'
    try:
        ibound = np.loadtxt(ibound_name)
        top = np.loadtxt(top_name)
    except:
        pass
    nrow,ncol = 411,501
    #--layer specific stuff
    layer_botm_names = ['Q4','Q3','Q2','Q1','T3','T1']
    #layer_botm_names = ['Q3','Q1','T1']
    #layer_botm_names = ['T1']
    nlay = len(layer_botm_names)
    ghb_layers = [1,2,3,4,5,6]
    
    delr,delc = 500.0,500.0
    #offset = [728600.0,782850.0]
    offset = [728600.0,577350.0]

    #--plotting stuff
    x = np.arange(0,ncol*delr,delr) + offset[0]
    y = np.arange(0,nrow*delc,delc) + offset[1]
    X,Y = np.meshgrid(x,y)
    plt_x = [825000.0,x.max()]
    plt_y = [offset[1],712000.0]

    sea_conc = 1.0
    brackish_conc = 0.5
    fresh_conc = 0.0


  
    