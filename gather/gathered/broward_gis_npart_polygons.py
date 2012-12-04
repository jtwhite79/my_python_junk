import copy
from shapely.geometry import Polygon
import shapefile

#shapename = 'shapes\\sfwmd_lulc_broward_1988'
shapename = 'scratch\\broward_landuse_1949_filled'
shp = shapefile.Reader(shapename)
#wr = shapefile.writer_like(shapename)
for i in range(shp.numRecords):
    shape = shp.shape(i)
    rec = shp.record(i)
    points = shape.points
    print len(points)
    parts = copy.deepcopy(shape.parts)
    if len(parts) > 1:

        parts.append(len(points))    
        shell = points[parts[0]:parts[1]]
        holes = []
        for pstart,pend in zip(parts[1:-1],parts[2:]):       
            holes.append(points[pstart:pend])
        poly = Polygon(shell,holes=holes)
        if not poly.is_valid:
            print
        #wr.poly([points[pstart:pend]],shapeType=shape.shapeType)
        #wr.record(rec)
    #break
#wr.save('scratch\\npart_test')    
