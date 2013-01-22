import os
import re
import itertools
from datetime import datetime
import calendar
import numpy as np
from matplotlib import ticker
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
df['rolling mean'] = pandas.rolling_mean(df['merged'],window)
df.to_csv('noaa_tidal_daily.csv',index_label='datetime')
df.pop('merged')
df.pop('8723080(haulover)')
df.pop('8723170(miami_beach)')
df.pop('8723214(virgina_key)')
last = df['rolling mean'][-1]

df_slr = pandas.read_csv('noaa_slr.csv',index_col=0,parse_dates=True)
offset = df_slr['no_rise'][0] - last
df_slr['low_rise'] -= offset
df_slr['9in in 50yr'] = df_slr['low_rise']
df_slr.pop('low_rise')
df_slr['med_rise'] -= offset
df_slr['16.5in in 50yr'] = df_slr['med_rise']
df_slr.pop('med_rise')
df_slr['high_rise'] -= offset
df_slr['24in in 50yr'] = df_slr['high_rise']
df_slr.pop('high_rise')
df_slr.pop('no_rise')
df = pandas.concat([df,df_slr])


ticks,ticklabels = [],[]
for dt in df.index:
    if dt.year % 10 == 0:
        ticks.append(dt)
        ticklabels.append(str(dt.year))
ticks = np.array(ticks)


fig = pylab.figure(figsize=(8,8))
ax = pylab.subplot(111)
#for col,rec in df.iteritems():
#    ax.plot(rec.index,rec.values)
df.plot(ax=ax,legend=False,xticks=ticks)
colors = ['#0099FF','#B82E00','#33FF99','k']
for i,l in enumerate(ax.lines[:-1]):
    l.set_ls('-')
    l.set_color(colors[i])
    l.set_alpha(1.0)
ax.lines[-1].set_ls('-')
ax.lines[-1].set_color('k')
ax.lines[-1].set_alpha(1.0)
ax.lines[-1].set_lw(3.0)
ax.set_ylabel('Sea Level ($feet NAVD$)')
#ax.set_xticks(ticks)
#ax.set_xticklabels(ticklabels)
#ax.grid()
ax.legend(loc=2)
pylab.savefig('noaa.png',dpi=300,fmt='png',bbox_inches='tight')