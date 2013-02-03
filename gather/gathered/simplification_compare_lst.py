import numpy as np
import pylab
import pandas
import mflst

modelnames = ['_model\\simple','_model\\simple_l','_model\\simple_rc']
names = ['base','layer','rowcol']
colors = ['k','b','g']

dfs = []
for mname in modelnames:
    lst = mflst.mfbudget(mname+'.list')
    lst.load()
    df_flux,df_vol = lst.to_pandas()
    df_flux_diff = df_flux['in'] - df_flux['out']
    df_flux_diff.index = df_flux_diff.index.get_level_values(1)
    dfs.append(df_flux_diff)

for ftype in dfs[0].columns:
    print ftype
    fig = pylab.figure(figsize=(6,6))
    ax = pylab.subplot(111)
    for df,name,color in zip(dfs,names,colors):
        ax.plot(df[ftype].index,df[ftype].values,color=color)
    ax.set_title(ftype)
    ax.legend(names)
    pylab.savefig('png\\'+ftype+'.png',fmt='png',dpi=300,bbox_inches='tight')

