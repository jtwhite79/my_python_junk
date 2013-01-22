import pandas
import shapefile

shape = shapefile.Reader('..\\shapes\\NEXRAD_pixels_florida_west')

df_nex = pandas.read_csv('NEXRAD.csv',nrows=1)
df_keys_nex = list(df_nex.keys())

df_pet = pandas.read_csv('PET.csv',nrows=1)
df_keys_pet = list(df_pet.keys())


wr = shapefile.writer_like('..\\shapes\\NEXRAD_pixels_florida')
for i in range(shape.numRecords):
    pnum = shape.record(i)[0]
    if str(pnum) in df_keys_nex:
        shp = shape.shape(i)
        wr.poly([shp.points],shapeType=shp.shapeType)
        wr.record([pnum])
wr.save('..\\shapes\\df_pixels')

wr = shapefile.writer_like('..\\shapes\\NEXRAD_pixels_florida')
for i in range(shape.numRecords):
    pnum = shape.record(i)[0]
    if str(pnum) in df_keys_pet:
        shp = shape.shape(i)
        wr.poly([shp.points],shapeType=shp.shapeType)
        wr.record([pnum])
wr.save('..\\shapes\\df_pixels_pet')



