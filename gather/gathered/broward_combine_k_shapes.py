import shapefile

#--shapenames
sc_shapename = '..\\_gis\\scratch\\pws_K_locations'
apt_shapename = '..\\_gis\\scratch\\apt_K_locations'

sc_shapes,sc_records = shapefile.load_as_dict(sc_shapename)
apt_shapes,apt_records = shapefile.load_as_dict(apt_shapename)

wr = shapefile.Writer()
wr.field('top',fieldType='N',size=10,decimal=1)
wr.field('bot',fieldType='N',size=10,decimal=1)
wr.field('K_ftday',fieldType='N',size=30,decimal=10)

for shape,top,bot,k in zip(sc_shapes,sc_records['top'],sc_records['bot'],sc_records['K']):
    wr.poly([shape.points],shapeType=shape.shapeType)
    wr.record([top,bot,k])

for shape,top,bot,k in zip(apt_shapes,apt_records['top'],apt_records['bot'],apt_records['K']):
    wr.poly([shape.points],shapeType=shape.shapeType)
    wr.record([top,bot,k])

wr.save('..\\_gis\\scratch\\all_K_locations')
