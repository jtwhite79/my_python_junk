import os
import re
import itertools
from datetime import datetime
import calendar
import numpy as np
import pylab
import pandas

dstart_reg = re.compile('Station Year Mo')

d_start,d_end = 55,68

data_dir = 'raw_data\\'
data_files = os.listdir(data_dir)
dfs = []
line_styles = {}
line_weight = {}
line_color = {}
line_color_list = ['r','g','b']
for i,dfile in enumerate(data_files):
    f = open(data_dir+dfile,'r')
    dts,vals = [],[]
    while True:
        line = f.readline()
        if line == '':
            break
        if dstart_reg.search(line) != None:
            while True:
                line = f.readline()
                if line == '':
                    break
                raw = line.strip().split()               
                yr = int(raw[1])
                mn = int(raw[2])
                station = (raw[0])
                dy = calendar.monthrange(yr,mn)[1]
                dt = datetime(year=yr,month=mn,day=dy)
                val = float(line[d_start:d_end].replace('[','').replace(']',''))
                dts.append(dt)
                vals.append(val)
    
    f.close()
    site_name = station + '('+dfile.split('.')[0]+')'
    line_styles[site_name] = '--'
    line_weight[site_name] = 0.1
    line_color[site_name] = line_color_list[i]
    df = pandas.DataFrame({site_name:vals},index=dts)
    df = df.dropna()    
    dfs.append(df)


df = pandas.concat(dfs,axis=1)



window = 1
for site in df.keys():
    df[site] = pandas.rolling_mean(df[site],window)


df['merged'] = np.NaN
for site in df.keys():
    df['merged'] = df['merged'].combine_first(df[site])
window = 100
df['merged'] = df['merged'].interpolate()
df[str(window)+'-day rolling mean'] = pandas.rolling_mean(df['merged'],window)
df.pop('merged')
fig = pylab.figure(figsize=(8,8))
ax = pylab.subplot(111)
df.plot(ax=ax,legend=False)
colors = ['#0099FF','#B82E00','#33FF99']
for i,l in enumerate(ax.lines[:-1]):
    l.set_ls('-')
    l.set_color(colors[i])
    l.set_alpha(1.0)
ax.lines[-1].set_ls('-')
ax.lines[-1].set_color('k')
ax.lines[-1].set_alpha(1.0)
ax.lines[-1].set_lw(3.0)
ax.grid()
ax.set_ylabel('Sea Level ($feet NAVD$)')
ax.legend(loc=2)
pylab.savefig('noaa.png',dpi=300,fmt='png',bbox_inches='tight')