import pandas
from shapely.geometry import Polygon
import shapefile

nex_shapename = '..\\shapes\\NEXRAD_pixels_tsala'
grid_shapename = '..\\shapes\\join_all2'

df = pandas.read_csv('NEXRAD.csv',nrows=1)
df_keys = list(df.keys())

#--build nexrad polygons - just duplicate multipart polys
print 'loading grid shapefile'
nex_shapes,nex_recs = shapefile.load_as_dict(nex_shapename)
nex_polys,nex_pixelnums = [],[]
print 'building nexrad polygons'
for shape,pnum in zip(nex_shapes,nex_recs['Pixel']):
    if str(pnum) in df_keys:
        if len(shape.parts) > 1:
            points = shape.points
            for i1,i2 in zip(shape.parts[:-1],shape.parts[1:]):
                poly = Polygon(shape.points[i1:i2])
                if not poly.is_valid:
                    raise Exception('invalid nexrad geometry'+str(pnum))   
                nex_polys.append(poly)
                nex_pixelnums.append(pnum)        
            #raise Exception('multipart nexrad shape'+str(rec))
        else:
            poly = Polygon(shape.points)
            if not poly.is_valid:
                raise Exception('invalid nexrad geometry'+str(pnum))
            nex_polys.append(poly)
            nex_pixelnums.append(pnum)        
    #else:
    #    print 'skipping pixel:',pnum
print 'built polygons for',len(nex_polys),' nexrad pixels'
#--build grid polygons
print 'loading grid shapefile'
grid_shp = shapefile.Reader(grid_shapename)
grid_shapes = grid_shp.shapes()
grid_recs = grid_shp.records()
grid_polys = []
print 'building grid polygons'
for i,(shape,rec) in enumerate(zip(grid_shapes,grid_recs)):
    if i % 500 == 0:
        print 'record',i,'\r',
    poly = Polygon(shape.points)
    if not poly.is_valid:
        raise Exception('invalid nexrad geometry'+str(rec))
    grid_polys.append(poly)

print '\nintersecting grid and nexrad polygons'
wr = shapefile.writer_like(grid_shapename)
wr.field('nex_pix',fieldType='C',size=50)
wr.field('nex_frac',fieldType='C',size=50)
for i,(gshape,grec,gpoly) in enumerate(zip(grid_shapes,grid_recs,grid_polys)):
    
    print 'record',i,'\r',
    #--search for intersections
    #--sum up the total intersected area - for grid cells not completely covered
    pixs,areas = [],[]
    tot_area = 0.0    
    for npoly,pix in zip(nex_polys,nex_pixelnums):
        if gpoly.intersects(npoly):
            ipoly = gpoly.intersection(npoly)
            area = ipoly.area
            tot_area += area
            #--incase this is a multipart nexrad shape and multiple parts intersect the same grid cell
            if pix in pixs:
                areas[pixs.index(pix)] += area
            else:
                areas.append(area)
                pixs.append(pix)    
    if len(pixs) > 0:
        pstr,fstr = '',''
        for p,a in zip(pixs,areas):
            pstr += '{0:6.0f},'.format(p)
            fstr += '{0:6.5f},'.format(a / tot_area)
        pstr = pstr[:-1]
        fstr = fstr[:-1]
        grec.append(pstr)
        grec.append(fstr)           
    else:
        grec.append('')
        grec.append('')
    wr.poly([gshape.points])
    wr.record(grec)        
  
wr.save('..\\shapes\\tsala_grid_nexrad')

