import numpy as np
import pylab
import pandas
from bro import seawat

potable = 0.014
near_zero = 1.0e-6



well_df_org,wfield_df_org = pandas.read_csv('well_conc.csv',index_col=0,parse_dates=True),pandas.read_csv('wellfield_conc.csv',index_col=0,parse_dates=True)

#--tile the record out of the entire runtime
wdict,wfdict = {},{}
for wname in well_df_org.keys():
    wdict[wname] = np.NaN
for wfield in wfield_df_org.keys():
    wfdict[wfield] = np.NaN

well_df = pandas.DataFrame(wdict,index=seawat.sp_end)
well_df = well_df.combine_first(well_df_org)
wfield_df = pandas.DataFrame(wfdict,index=seawat.sp_end)
wfield_df = wfield_df.combine_first(wfield_df_org)

       
figdir = 'png\\results\\well_conc\\'
for wname,rec in well_df.iteritems():
    if (rec.max() > near_zero):
        print wname,'\r',
        fig = pylab.figure(figsize=(8,4))
        ax = pylab.subplot(111)
        ax.plot(rec.index,rec.values,'k--')
        rec[rec < potable] = np.NaN
        ax.plot(rec.index,rec.values,'r-')
        ax.plot([rec.index[0],rec.index[-1]],[potable,potable],'b--')
        ax.grid()
        ax.set_title('well: '+str(wname))
        figname = figdir + str(wname)
        pylab.savefig(figname,fmt='png',dpi=300,bbox_inches='tight')