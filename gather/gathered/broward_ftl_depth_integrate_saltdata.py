import os
import numpy as np
import pandas
import pylab
import shapefile
import pestUtil as pu
from bro import seawat

def group_intervals(intervals,geom):
    groups = {}
    midpoints = {}
    for i in range(len(geom[:-1])):
        t,b = geom[i],geom[i+1]
        mid = (t + b) / 2.0
        for intrv in intervals:
            if float(intrv) < t and float(intrv) >= b:
                if i in groups.keys():
                    groups[i].append(intrv)
                else:
                    groups[i] = [intrv]
                    midpoints[i] = mid
    return midpoints,groups


#--build the geo array
geom = np.zeros((seawat.nlay+1,seawat.nrow,seawat.ncol))
geom[0,:,:] = np.loadtxt(seawat.top_name)
for i,lay in enumerate(seawat.layer_botm_names):
    arr = np.loadtxt(seawat.ref_dir+lay+'_bot.ref')
    geom[i+1,:,:] = arr

#--load ftl salt grid shapefile
shapename = '..\\..\\_gis\\scratch\\ftl_salt_grid'
shapes,records = shapefile.load_as_dict(shapename)
wellnums,rows,cols = records['Id'],records['row'],records['column_']
xs,ys = [],[]
for s in shapes:
    x,y = s.points[0]
    xs.append(x)
    ys.append(y)


#--load the relconc dataframes
df_dir = '..\\..\\_ftl_salt\\dataframes\\'
files = os.listdir(df_dir)
dfs = {}
for f in files:
    if 'relconc' in f:
        print f
        wellnum = int(f.split('_')[0].split('-')[1]) 
        df = pandas.read_csv(df_dir+f,index_col=0,parse_dates=True)
        #df = df.fillna(method='bfill')
        dfs[wellnum] = df


mod_dfs = []
bore_coords_lines = []
for wnum,row,col,x,y in zip(wellnums,rows,cols,xs,ys):
    df = dfs[wnum]
    gm = geom[:,int(float(row))-1,int(float(col))-1]
    midpts,groups = group_intervals(df.keys(),gm)
    mod_dicts = {}   
    for ilay,group in groups.iteritems():
        sname = 'ftl'+str(wnum)+'_'+str(ilay+1)+'L'
        print sname
        line = sname+' {0:20.8G}  {1:20.8G} {2:d}\n'.format(x,y,ilay+1)
        bore_coords_lines.append(line)

        #print seawat.layer_botm_names[ilay]

        mod_dicts[sname] = df[group].mean(axis=1).dropna()  
    df = pandas.DataFrame(mod_dicts)
    df.to_csv(df_dir+str(wnum)+'_mod.csv',index_label='datetime')              
    mod_dfs.append(df)
df = pandas.concat(mod_dfs,axis=1)
smp = pu.smp(None,load=False,pandas=True)
smp.records = df
smp_dir = '..\\..\\_ftl_salt\\'
smp.save(smp_dir+'ftl_mod.smp',dropna=True)

f = open(smp_dir+'ftl_borecoords.dat','w',0)
for line in bore_coords_lines:
    f.write(line)


for wnum,df in zip(wellnums,mod_dfs):
    fig = pylab.figure()
    ax = pylab.subplot(111)
    for site,record in df.iteritems():
        print site
        ax.plot(record.index,record.values,'.',label=site)
    ax.grid()
    ax.legend()                        
    pylab.savefig(smp_dir+'png\\'+str(wnum)+'.png',fmt='png')

