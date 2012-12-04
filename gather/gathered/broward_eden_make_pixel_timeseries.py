import os
from datetime import datetime,timedelta
import numpy as np
from scipy.io.netcdf import netcdf_file as ncdf
import pandas
import shapefile


#--get a list of the eden masterid numbers that are needed
recs = shapefile.load_as_dict('..\\_gis\\scratch\\broward_grid_eden',attrib_name_list=['eden_cells'],loadShapes=False)
masterids = []
for r in recs['eden_cells']:
    raw = r.split()
    for rr in raw:
        if int(rr) not in masterids:
            masterids.append(int(rr))
             
#--get the x,y of the masterids
recs = shapefile.load_as_dict('..\\_gis\\shapes\\EDEN_grid_poly_Jan_10_sp',loadShapes=False)
xs,ys = [],[]
for x,y,m in zip(recs['X_COORD'],recs['Y_COORD'],recs['MASTERID']):
    if int(m) in masterids:
        xs.append(float(x))
        ys.append(float(y))


cdf_dir = 'surface_netcdf\\'
cdf_files = os.listdir(cdf_dir)

#--group files by year
cdf_years = []
cdf_groups = []
for cfile in cdf_files:
    year = int(cfile.split('_')[0])
    if year in cdf_years:
        cdf_groups[cdf_years.index(year)].append(cfile)
    else:
        cdf_groups.append([cfile])
        cdf_years.append(year)

#--a simple structure to hold stage records
stages = []
for m in masterids:
    stages.append([])

#--an index map to extrac stage records
cdf = ncdf(cdf_dir+cdf_files[0],mode='r')
xarr = list(cdf.variables['x'])
yarr = list(cdf.variables['y'])
idx,jdx= [],[]
for x,y in zip(xs,ys):
    jdx.append(xarr.index(x))
    idx.append(yarr.index(y))



for year,group in zip(cdf_years,cdf_groups):
    print year    
    start = datetime(year=year,month=1,day=1)
    day = 0
    for cfile in group:            
        cdf = ncdf(cdf_dir+cfile,mode='r')
        print cdf.variables['time'].shape        
        for t in cdf.variables['time']:
            dt = start + timedelta(days=day)
            #print dt
            arr = cdf.variables['stage'][t]
            #np.savetxt('ref\\'+dt.strftime('%Y%m%d')+'.ref',arr,fmt=' %15.6e')
            for ii,[i,j] in enumerate(zip(idx,jdx)):
                val = arr[i,j]
                stages[ii].append([dt,val])                
            day += 1
        #break
    #break
            
#--build a pandas dataframe
sdict = {}
for m,s in zip(masterids,stages):
    s = np.array(s)
    s[:,1] /= 100.0
    s[:,1] *= 3.281
    sdict[m] = s[:,1]
df = pandas.DataFrame(sdict,index=s[:,0])
df.to_csv('eden_timeseries.csv',index_label='datetime')


#out_dir = 'stage_smp\\'
#for m,s in zip(masterids,stages):    
#    f = open(out_dir+str(m)+'.smp','w')
#    for dt,val in s:
#        f.write(str(m).ljust(20)+' '+dt.strftime('%d/%m/%Y')+' 00:00:00  {0:15.6E}\n'.format(val))
#    f.close()

