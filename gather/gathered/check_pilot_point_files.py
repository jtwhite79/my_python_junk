import os
from datetime import datetime
import numpy as np

files = os.listdir('pilot_point_files\\')

dt_list = []
for f in files:
    dt = datetime.strptime(f.split('_')[0],'%Y%m%d')
    dt_list.append(dt)
dt_arr = np.array(dt_list)
print dt_arr.shape,np.unique(dt_arr).shape    