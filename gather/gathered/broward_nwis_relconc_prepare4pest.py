import numpy as np
import pandas
import shapefile
import pestUtil as pu
from bro import seawat
'''writes borecoords and also writes a new smp with station names instead of site nos
Dec 5 2012 - waiting on NWIS sample depth data so just faked it for now

'''

def get_layer_num(elev,geom):
    if elev > geom[0]:
        return None
    if elev < geom[-1]:
        return len(geom)-1
    for i in range(len(geom[:-1])):
        t = geom[i]
        b = geom[i+1]
        if elev < t and elev >= b:
            return i+1
    return None            


#--build the geo array
geom = np.zeros((seawat.nlay+1,seawat.nrow,seawat.ncol))
geom[0,:,:] = np.loadtxt(seawat.top_name)
for i,lay in enumerate(seawat.layer_botm_names):
    arr = np.loadtxt(seawat.ref_dir+lay+'_bot.ref')
    geom[i+1,:,:] = arr


#--load nwis shapefile
shapename = '..\\..\\_gis\\scratch\\broward_nwis_gw_conc_depth'
shapes,records = shapefile.load_as_dict(shapename)
shp = shapefile.Reader(shapename)
rec_list = shp.records()
sitenos = records['site_no']
names = records['station_nm']
hdepths = records['hole_depth']
wdepths = records['well_depth']
rows = records['row']
cols = records['column_']
xs,ys = [],[]
for shape in shapes:
    x,y = shape.points[0]
    xs.append(x)
    ys.append(y)

#--correct the names
gen_prefix = 'conc_'
gen_count = 1
fixed = []
for n in names:
    n = n.replace(' ','')
    n = n.replace(',','')
    if n == '' or len(n) > 8:
        n = gen_prefix + str(gen_count)
        gen_count += 1
    if n in fixed:
        raise Exception('Duplicate names: '+n)
    fixed.append(n)

#--build sample elevation list
elevs = []
for r,c,hd,wd in zip(rows,cols,hdepths,wdepths):
    t = geom[0,int(float(r))-1,int(float(c))-1]
    try:
        d = float(hd)
    except:
        d = float(wd)
    e = t - d
    elevs.append(e)

#--load the decluster dataframe
smp = pu.smp('..\\..\\_nwis\\relconc_declustered.smp',load=True,pandas=True)
df = smp.records

f = open('..\\..\\_nwis\\nwis_conc_bore_coords.dat','w',0)
wr = shapefile.writer_like(shapename)
wr.field('fixed_name',fieldType='C',size=50)
for siteno in df.keys():
    if siteno in sitenos:
        idx = sitenos.index(siteno)
        name = fixed[idx]
        r = rows[idx]
        c = cols[idx]
        g = geom[:,int(float(r))-1,int(float(c))-1]
        x = xs[idx]
        y = ys[idx]
        e = elevs[idx]
        lnum = get_layer_num(e,g)   
        if lnum == None:
            raise Exception('sample elevation not within grid: '+str(siteno))
        df[name] = df[siteno]
        df.pop(siteno)
        wr.poly([shapes[idx].points],shapeType=shape.shapeType)
        rec = rec_list[idx]
        rec.append(name)
        wr.record(rec)
        f.write('{0:25s}  {1:20.8G}  {2:20.8G}  {3:d}\n'.format(name,x,y,lnum))
    else:
        print 'missing siteno: ',siteno
        df.pop(siteno)
f.close()
smp.records = df
smp.save('..\\..\\_nwis\\relconc_cali.smp',dropna=True)
wr.save('..\\..\\_gis\\scratch\\broward_nwis_conc_cali')
                     




