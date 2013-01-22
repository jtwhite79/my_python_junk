import shapefile

wr = shapefile.Writer()
wr.field('name',fieldType='C',size=30)
f = open('misc\\mod2obs_loc.dat','r')
for line in f:
    raw = line.strip().split()
    x = float(raw[1])
    y = float(raw[2])
    name = raw[0]
    wr.poly([[[x,y]]],shapeType=shapefile.POINT)
    wr.record([name])
wr.save('shapes\\obs_locs')
