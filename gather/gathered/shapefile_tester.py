import shapefile
#--writer testing
#shp = shapefile.Reader('grid')
#shapes1 = shp.shapes()
#header1 = shp.dbfHeader()
#shp2 = shapefile.Reader('gridtestgrid')
#header2 = shp2.dbfHeader()
#shapes2 = shp2.shapes()
#records2 = shp2.records()
#wr = shapefile.Writer()
##wr.field('test','N',size=20,decimal=3)
#for item in header2:
#    wr.field(item[0],fieldType=item[1],size=item[2],decimal=item[3])
#print shapes1[0].points
#print shapes2[0].points
#print records2
#for r,s in zip(records2,shapes2):
#    wr.poly([s.points])
#    wr.record(r)
#wr.save('grid_python')
#print

#-- reader testing
shp = shapefile.Reader('test')
shapes1 = shp.shapes()
header1 = shp.dbfHeader()
records1 = shp.records()
print
