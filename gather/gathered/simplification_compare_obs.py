import os
import shutil
import pandas
import pylab
import pestUtil as pu


mod2obs_ins = ['mod2obs.in','mod2obs_l.in','mod2obs_rc.in']
names = ['base','layer','rowcol']
colors = ['k','b','g']
dfs = []
exe = 'mod2obs.exe'
for m2o_in,name in zip(mod2obs_ins,names):
    cmd_line = exe + ' < ' + m2o_in
    print cmd_line
    os.system(cmd_line)
    shutil.copy('mheads.smp',name+'.smp')
    smp = pu.smp('mheads.smp',load=True,pandas=True)
    dfs.append(smp.records)

for site in dfs[0].columns:
    fig = pylab.figure(figsize=(6,6))
    ax = pylab.subplot(111)
    for df,name,color in zip(dfs,names,colors):
        ax.plot(df[site].index,df[site].values,color=color)
    ax.set_title(site)
    ax.legend(names)
    pylab.savefig('png\\'+site+'.png',fmt='png',dpi=300,bbox_inches='tight')

