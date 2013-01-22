import numpy as np
from shapely.geometry import Polygon,Point
import shapefile

#--load the nexrad pixels
shapename_nex = '..\\shapes\\cwm_pixels_NEXRAD'
shp_nex = shapefile.Reader(shapename_nex)
nexrad_records = shp_nex.records()
nexrad_shapes = shp_nex.shapes()
[xmin,ymin,xmax,ymax] = shp_nex.bbox
deltax,deltay = xmax-xmin,ymax-ymin
pt_deltax,pt_deltay = (deltax / 5.0)/2.0,(deltay / 10.0)/2.0
nexrad_polygons = []
for shape in nexrad_shapes:   
    poly = Polygon(shape.points)
    nexrad_polygons.append(poly)


#--load the grid shape
ibnd_idx = 5
pix_idx = 7
shapename_grid = '..\\shapes\\cwm_grid_with_nexrad_pixels'
shp_grid = shapefile.Reader(shapename_grid)
grid_shapes,grid_records = shp_grid.shapes(),shp_grid.records()
grid_polygons = []
for s in grid_shapes:
    grid_polygons.append(Polygon(s.points))

xpts = np.linspace(xmin+pt_deltax,xmax-pt_deltax,5)
ypts = np.linspace(ymin+pt_deltay,ymax-pt_deltay,10)

#--find valid points - those that intersect a model cell with an appropriate ibound
valid_points = []
valid_Points = []
for x in xpts:
    for y in ypts:
        pt = [x,y]
        point = Point(pt)
        #--make sure this point is in an active model cell
        for poly,rec in zip(grid_polygons,grid_records):
            ibnd = rec[ibnd_idx]
            if ibnd != 0 and ibnd != 2 and point.intersects(poly):
                valid_points.append([x,y])
                valid_Points.append(point)
        pass




#--write a valid points shapefile
wr = shapefile.Writer()
wr.field('x',fieldType='N',size=20,decimal=3)
wr.field('y',fieldType='N',size=20,decimal=3)
for [x,y] in valid_points:
    wr.poly([[[x,y]]],shapeType=shapefile.POINT)
    wr.record([x,y])
wr.save('shapes\\nexrad_points')    


#--write a nearest-neighbor nexrad shapefile
wr = shapefile.writer_like(shapename_nex)
wr.field('group',fieldType='N',size=2,decimal=0)
pmap = {}
for shape,poly,record in zip(nexrad_shapes,nexrad_polygons,nexrad_records):
    imin,dist = None,1.0e+30
    for i,v in enumerate(valid_Points):
        d = poly.distance(v)
        if d < dist:
            dist = d
            imin = i
    if imin in pmap.keys():
        pmap[imin].append(record[0])
    else:
        pmap[imin] = [record[0]]            
    wr.poly([shape.points],shapeType=shape.shapeType)
    record.append(imin)
    wr.record(record)
wr.save('shapes\\nexrad_groups')

#--add the grouping to the grid shapefile
wr = shapefile.writer_like(shapename_grid)
wr.field('nex_group',fieldType='N',size=3,decimal=0)

for shape,record in zip(grid_shapes,grid_records):
    pix = int(record[pix_idx].split()[0])
    group = None
    for grp,pixels in pmap.iteritems():
        if pix in pixels:
            group = grp
            break
    if group is None:
        print
    wr.poly([shape.points],shapeType=shape.shapeType)
    record.append(group+1)
    wr.record(record)
wr.save('shapes\\cwm_grid_groups')    
            
