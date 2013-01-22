import shutil
import numpy as np

def flow_2_seawat(flow_rootname,seawat_rootname):
    '''for now, just a copy of riv,wel,ets and rch
       ghb gets written during parameterization
    '''
    exts = ['.riv','.wel','.ets','.rch']
    for ext in exts:
        shutil.copy(flow_rootname+ext,seawat_rootname+ext)
    
    