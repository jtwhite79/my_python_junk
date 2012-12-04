import copy
import shapefile

shape_name = 'scratch\\broward_grid_pixelmap'
shp = shapefile.Reader(shape_name)
attrib_idx = shapefile.load_attrib_idx(shape_name)
wr = shapefile.writer_like(shape_name)

for i in range(shp.numRecords):
    shape = shp.shape(i)
    rec = shp.record(i)
    wr.poly([shape.points],shapeType=shape.shapeType)
    pixels = rec[attrib_idx['pixels']]
    raw = pixels.split()
    for i,r in enumerate(raw):
        if r.startswith('['):
            raw[i] = copy.deepcopy(r[1:-1])
            #print i,raw[i],raw 
    rec[attrib_idx['pixels']] = ' '.join(raw)                                  
    wr.record(rec)
wr.save('scratch\\borward_grid_pixelmap_fix')                        
                