import pandas
import shapefile

shape = shapefile.Reader('..\\shapes\\NEXRAD_pixels_florida_west')

df = pandas.read_csv('NEXRAD.csv',nrows=1)
df_keys = list(df.keys())

wr = shapefile.writer_like('..\\shapes\\NEXRAD_pixels_florida')
for i in range(shape.numRecords):
    pnum = shape.record(i)[0]
    if str(pnum) in df_keys:
        shp = shape.shape(i)
        wr.poly([shp.points],shapeType=shp.shapeType)
        wr.record([pnum])
wr.save('..\\shapes\\df_pixels')


