import numpy as np
import pylab
import pandas
import mflst
import bro
'''compare the wel+swr flux to the wel flux
'''
maxentries=749
swr_lst = mflst.mfbudget('bro.list')
wel_lst = mflst.mfbudget('bro_seawat.list')

ltime = mflst.lsttime('bro.list',start=bro.start)
ltime.load(maxentries=maxentries) 
swr_time = ltime.to_pandas()

swr_lst.load(maxentries=maxentries)
swr_flux,swr_cumu = swr_lst.to_pandas()
swr_flux.index = swr_time['datetime']

wel_lst.load(maxentries=maxentries)
wel_flux,swr_cumu = wel_lst.to_pandas()
wel_flux.index = swr_time['datetime']

tot_swr_flux = -1.0 * np.loadtxt('tot_vol_record.dat',usecols=[1])

fig = pylab.figure()
ax1 = pylab.subplot(311)
ax2 = pylab.subplot(312)
ax3 = pylab.subplot(313)

swr_flux.select(lambda x:x[1]=='SWR LEAKAGE',axis=1).to_csv('swr_flux.csv')
wel_flux.select(lambda x:x[1]=='WELLS',axis=1).to_csv('wel_flux.csv')
swr_flux['tot_vol'] = tot_swr_flux



aq_swr = swr_flux['out','SWR LEAKAGE'] - swr_flux['in','SWR LEAKAGE']
aq_wel = wel_flux['out','WELLS'] - wel_flux['in','WELLS'] - swr_flux['out','WELLS']

df_compare = pandas.DataFrame({'swr':aq_swr,'wel':aq_wel,'tv':swr_flux['tot_vol']})
df_compare.to_csv('flux_compare.csv')

aq_swr.plot(ax=ax1)
swr_flux['tot_vol'].plot(ax=ax1)
aq_wel.plot(ax=ax1)
ax1.lines[0].set_color('k')
ax1.lines[0].set_color('g')
(aq_swr-aq_wel).plot(ax=ax2)
(aq_swr - swr_flux['tot_vol']).plot(ax=ax3)
pylab.show()

