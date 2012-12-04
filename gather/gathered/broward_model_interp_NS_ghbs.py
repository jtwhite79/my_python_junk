import numpy as np
import pandas
from shapely.geometry import Polygon,Point
import shapefile


nwis_shapename = '..\\..\\_gis\\scratch\\broward_nwis_sites_reclen_gw'
grid_shapename = '..\\..\\_gis\\shapes\\broward_grid_master'

print 'loading pandas dataframe to get site numbers'
df = pandas.read_csv('..\\..\\_nwis\\ghb_NS_stages_model.csv',index_col=0)
sites = df.keys()


print 'loading NWIS points...'
nshape = shapefile.Reader(nwis_shapename)
nshapes,nrecords = nshape.shapes(),nshape.records()
fieldnames = shapefile.get_fieldnames(nwis_shapename)
site_idx = fieldnames.index('site_no')
nsites,npoints = [],[]
for ns,nr in zip(nshapes,nrecords):
    if nr[site_idx] in sites:
        pt = Point(ns.points[0])        
        npoints.append(pt)
        nsites.append(nr[site_idx])
print 'done'

print 'loading north,south cells'

idx_north,idx_south = 40,35
rows,cols,polys = [],[],[]
gshape = shapefile.Reader(grid_shapename)
fieldnames = shapefile.get_fieldnames(grid_shapename)
ibnd_idx = fieldnames.index('ibound_CS')
row_idx,col_idx = fieldnames.index('row'),fieldnames.index('column')
for i in range(gshape.numRecords):
    rec,shape = gshape.record(i),gshape.shape(i)
    if rec[ibnd_idx] in [idx_north,idx_south]:       
        gpoly = Polygon(shape.points)
        if not gpoly.is_valid:
            raise TypeError('invalid grid poly geo'+str(i))
        rows.append(rec[row_idx])
        cols.append(rec[col_idx])
        polys.append(gpoly)
        #break

print 'done'

print 'calculating interpolation factors...'
num_pts = 4

f = open('..\\ghb_NS_factors.dat','w')
f.write('row,col,numpts')
for n in range(num_pts):
    f.write(',pt_'+str(n)+'_name,pt_'+str(n)+'_fac')
f.write('\n')

for r,c,poly in zip(rows,cols,polys):
    f.write(str(r)+','+str(c)+','+str(num_pts))
    #--find distance to every point
    dists = []
    for pt in npoints:
        dist = pt.distance(poly.centroid)
        dists.append(dist)
    dists = np.array(dists)
    sort_idx = (np.argsort(dists))
    #for si in sort_idx:
    #    print nsites[si],dists[si]
    #--calc total weight
    idists,isites = [],[]
    for i in sort_idx[:num_pts]:
        id = 1.0/dists[i]
        idists.append(id)
        isites.append(nsites[i])
    id_sum = sum(idists)
    for id,ist in zip(idists,isites):
        wght = id/id_sum        
        f.write(','+str(ist)+',{0:15.7e}'.format(wght))
    f.write('\n')
f.close()






       



