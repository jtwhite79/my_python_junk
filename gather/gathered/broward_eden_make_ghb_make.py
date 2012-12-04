from shapely.geometry import Polygon
import shapefile


eden_shapename = '..\\_gis\\shapes\\EDEN_grid_poly_Jan_10_sp'
grid_shapename = '..\\_gis\\shapes\\broward_grid_master'




print 'loading EDEN polygons...'
eshape = shapefile.Reader(eden_shapename)
eshapes,erecords = eshape.shapes(),eshape.records()
fieldnames = shapefile.get_fieldnames(eden_shapename)
cell_idx = fieldnames.index('MASTERID')
ecells,epolys = [],[]
for es,er in zip(eshapes,erecords):
    poly = Polygon(es.points)
    if not poly.is_valid:
        raise TypeError('invalid eden poly geo'+str(i))
    epolys.append(poly)
    ecells.append(er[cell_idx])
print 'done'

print 'loading WCA ghb cells and intersecting against EDEN polys'
wr = shapefile.writer_like(grid_shapename)
wr.field('eden_fracs',fieldType='C',size=50)
wr.field('eden_cells',fieldType='C',size=50)

ieden = [31,32,33,34]
gshape = shapefile.Reader(grid_shapename)
fieldnames = shapefile.get_fieldnames(grid_shapename)
ibnd_idx = fieldnames.index('ibound')
cell_idx = fieldnames.index('cellnum')
for i in range(gshape.numRecords):
    rec,shape = gshape.record(i),gshape.shape(i)
    if rec[ibnd_idx] in ieden:       
        gpoly = Polygon(shape.points)
        if not gpoly.is_valid:
            raise TypeError('invalid grid poly geo'+str(i))
        interx_frac,interx_cell = '',''
        for epoly,ecell in zip(epolys,ecells):
            if epoly.intersects(gpoly):
                ipoly = gpoly.intersection(epoly)
                frac = ipoly.area/gpoly.area
                interx_frac += ' {0:0.5f}'.format(frac)
                interx_cell += ' {0:5.0f}'.format(ecell)
        rec.append(interx_frac)
        rec.append(interx_cell)
        wr.poly([shape.points],shapeType=shape.shapeType)
        wr.record(rec)
wr.save('..\\_gis\\scratch\\broward_grid_eden')


