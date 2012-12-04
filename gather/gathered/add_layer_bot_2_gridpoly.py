import shapefile

ngvd2navd = -1.5
layers = ['H','Q5','Q4','Q3','Q2','Q1','T3','T2','T1']

#--load the grid polygon shape
shp = shapefile.Reader('shapes\\broward_grid_master')
header = shp.dbfHeader()
#records = shp.records()
#shapes = shp.shapes()


top_idx = None
layer_idxs = [None for i in layers]
for i,item in enumerate(header):        
    if item[0] == '29to88':
        ng2nv_idx = i
    elif item[0] == 'top_smooth':
        top_idx = i
    else:
        if item[0] in layers:
            layer_idxs[layers.index(item[0])] = i

if None in layer_idxs:
    raise IndexError,'layer attribute index not found'

#--set up the writer
wr = shapefile.Writer()
for item in header:
    wr.field(item[0],fieldType=item[1],size=item[2],decimal=item[3])
for lay in layers:
    wr.field(lay+'_bot',fieldType='N',size=20,decimal=6)


for irec in range(shp.numRecords):
    if irec % 100 == 0:
        print irec,shp.numRecords
    rec = shp.record(irec)
    shape = shp.shape(irec)
    top = rec[top_idx]
    prev = float(top)    
    for il,lay in zip(layer_idxs,layers):
        bot = prev - float(rec[il]) 
        if (prev-bot) < 1.0:
            print lay,bot
        rec.append(bot)
        prev = bot
    wr.poly([shape.points],shapeType=shapefile.POLYGON)
    wr.record(rec)

wr.save('scratch\\broward_grid_master')                    
    