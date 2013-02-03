import pandas
import matplotlib as mpl
mpl.rcParams['legend.fontsize']  = 6
import pylab
import mflst

import bro

cfd_2_mgd = 7.481 / 1.0e6

#--use maxentries to process the file if model is still running - otherwise a race condition between time and budget
maxentries = None

file_name = 'bro.list'
ltime = mflst.lsttime(file_name,start=bro.start)
ltime.load(maxentries=maxentries) 
df_time = ltime.to_pandas()
df_time.to_csv('list_time.csv',index_label=('ts','sp'))
mfb = mflst.mfbudget(file_name)    
mfb.load(maxentries=maxentries)
df_flux,df_cumu = mfb.to_pandas()

df_flux.to_csv('list_flux.csv',index_label=('ts','sp'))
df_cumu.to_csv('list_cumu.csv',index_label=('ts','sp'))

df_flux.index = df_time['datetime']
df_cumu.index = df_time['datetime']

#df_flux = df_flux.merge(df_time,left_index=True,right_index=True)
#df_cumu = df_cumu.merge(df_time,left_index=True,right_index=True)

#--sum all the outs and ins
df_fluxin = df_flux['in'].sum(axis=1)
df_fluxout = df_flux['out'].sum(axis=1)
df_cumuin = df_cumu['in'].sum(axis=1)
df_cumuout = df_cumu['out'].sum(axis=1)

#--get the differences
df_flux['diff'] = df_fluxin - df_fluxout
df_flux['discrep'] = 100.0 * df_flux['diff'] / df_fluxin
df_cumu['diff'] = df_cumuin - df_cumuout
df_cumu['discrep'] = 100.0 * df_cumu['diff'] / df_cumuin


fig = pylab.figure()
ax1 = pylab.subplot(411)
ax2 = pylab.subplot(412)
ax3 = pylab.subplot(413)
ax4 = pylab.subplot(414)

ax2.set_xticklabels([])
ax3.set_xticklabels([])
ax4.set_xticklabels([])

df_flux['discrep'].plot(ax=ax1,title='flux discrep')
df_cumu['discrep'].plot(ax=ax2,title='cumu discrep')

((df_flux['in'] - df_flux['out']) * cfd_2_mgd).plot(ax=ax3,title='flux')
#((df_cumu['in'] - df_cumu['out']) * cfd_2_mgd).plot(ax=ax4,title='cumu')
#df_flux['in','ets segements']df_flux['in','recharge']
(df_cumu['out','ET SEGMENTS'] / df_cumu['in','RECHARGE']).plot(ax=ax4,title='et fraction')
pylab.show()
