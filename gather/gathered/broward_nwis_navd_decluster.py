import os
import numpy as np
#from dateutil.relativedelta import relativedelta
from datetime import timedelta
import pandas
from shapely.geometry import Point
import shapefile
import pestUtil as pu
from bro import flow

'''spatailly declusters relconc data and thin out site that are not in the active domain

'''

df = pandas.read_csv('dataframes\\navd_modeltime.csv',index_col=0,parse_dates=True)

#--get the nwis site no and locations
nwis_shapename = '..\\_gis\\scratch\\broward_nwis_gw_navd'
shapes,records = shapefile.load_as_dict(nwis_shapename)
nwis_sitenos = records['site_no']
nwis_ibnd = records['ibound_CS']

nwis_pts = []
for shape in shapes:
    pt = Point(shape.points[0])
    nwis_pts.append(pt)

print len(df.keys())
#--remove columns that are in the inactive domain

#for sn,ib in zip(nwis_sitenos,nwis_ibnd):
#    if ib < 1 and sn in df.keys():
#        df.pop(sn)
#print len(df.keys())
for sn in df.keys():
    if sn not in nwis_sitenos or nwis_ibnd[nwis_sitenos.index(sn)] < 1:
        df.pop(sn)
print len(df.keys())

#--find clusters
clus_distance = 500 #ft - one coarse model cell
clusters = {}
for i1,[pt1,site1,ib1] in enumerate(zip(nwis_pts,nwis_sitenos,nwis_ibnd)):
    if ib1 > 0:
        print 'searching point ',i1
 
        for i2,[pt2,site2,ib2] in enumerate(zip(nwis_pts[i1+1:],nwis_sitenos[i1+1:],nwis_ibnd[i1+1:])):
            if ib2 > 0 and pt1.distance(pt2) < clus_distance:
                if site1 in clusters.keys():
                    clusters[site1].append(site2)
                else:
                    clusters[site1] = [site2]

#--make sure this structure is correct
for site,clus in clusters.iteritems():
    for site2 in clus:
        if site2 in clusters.keys() and site in clusters[site2]:
            raise Execption('symmetric cluster found')


#--thin the data is data points are within minimum timedelta
min_days = 32
for site,sites in clusters.iteritems():
    sites.append(site)
    for i,site1 in enumerate(sites):
        if site1 not in df.keys():
            print 'missing site1',site1
        else:
            for site2 in sites[i+1:]:
                if site2 not in df.keys():
                    print 'missing site2',site2
                else:
                    #print site1,site2                    
                    #--find data points from site1,site2 that are too close in time
                    dt_idx1,dt_idx2 = [],[]
                    for dt1 in df[site1].dropna().index:
                        for dt2 in df[site2].dropna().index:
                            if np.abs((dt1 - dt2).days) < min_days:
                                df[site2][dt2] = np.NaN                                
                        pass
        pass

smp = pu.smp(None,load=False,pandas=True)
smp.records = df
smp.save('navd_declustered.smp',dropna=True)



