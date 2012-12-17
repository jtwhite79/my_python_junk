import numpy as np
import shapefile

data = np.loadtxt('Table3.dat')
data[:,1:] /= 35.0

shapename = '..\\_gis\\shapes\\bcdpep_locs'
shp = shapefile.Reader(shapename)
records = shp.records()
shapes = shp.shapes()

wr = shapefile.Writer()
wr.field('Location',fieldType='N',size=2,decimal=0)
wr.field('med_relconc',fieldType='N',size=20,decimal=10)
wr.field('max_relconc',fieldType='N',size=20,decimal=10)
wr.field('min_relconc',fieldType='N',size=20,decimal=10)

for shape,loc in zip(shapes,records):
    d = data[np.where(data[:,0]==loc[0])][0]
    rec = [int(d[0])]
    for dd in d[1:]:
        if dd > 1.0:dd = 1.0
        rec.append(dd)
    wr.poly([shape.points],shapeType=shape.shapeType)
    wr.record(rec)
wr.save('..\\_gis\\scratch\\bcdpep_locs')

