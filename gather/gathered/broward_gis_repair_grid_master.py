import numpy as np
import shapefile

#--load the master grid file
grid_shapename = 'shapes\\broward_grid_master'
grid_shp = shapefile.Reader(grid_shapename)
grid_polygons = []

wr = shapefile.writer_like(grid_shapename)

wr_extent = shapefile.Writer()
wr_extent.field('somejunk',fieldType='C',size=10)

xmin,xmax = 1.0e+10,-1.0e+10
ymin,ymax = 1.0e+10,-1.0e+10
for i in range(grid_shp.numRecords):
    shape = grid_shp.shape(i)
    rec = grid_shp.record(i)
    points = shape.points
    arr = np.array(points)
    if arr[:,0].max() > xmax:
        xmax = arr[:,0].max()
    if arr[:,0].min() < xmin:
        xmin = arr[:,0].min()

    if arr[:,1].max() > ymax:
        ymax = arr[:,1].max()
    if arr[:,1].min() < ymin:
        ymin = arr[:,1].min()

    points_reorder = [points[0],points[3],points[2],points[1],points[0]]
    wr.poly([points_reorder],shapeType=shape.shapeType)
    wr.record(rec)
wr.save('scratch\\broward_grid_master')    

points = [[xmin,ymin],[xmin,ymax],[xmax,ymax],[xmax,ymin],[xmin,ymin]]

wr_extent.poly([points],shapeType=shapefile.POLYGON)
wr_extent.record(['junk'])
wr_extent.save('scratch\\broward_grid_extent')
