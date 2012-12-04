import copy
import shapefile 

shp1 = shapefile.Reader('shapes\\pws_bro')
shapes1 = shp1.shapes()
records1 = shp1.records()
header1 = shp1.dbfHeader()
p_idx1 = None
w_idx1 = None
u_idx1 = None
for i,item in enumerate(header1):
    if item[0].upper() == 'PERM_NO':
        p_idx1 = i
    if item[0].upper() == 'WELL_NO':
        w_idx1 = i    
    if item[0].upper() == 'UTILITY':
        u_idx1 = i
    
       
plist1 = []
for r in records1:        
    p = r[p_idx1]
    if p not in plist1:
        plist1.append(p)


shp2 = shapefile.Reader('shapes\\pws_wname_mod')
shapes2 = shp2.shapes()
records2 = shp2.records()
header2 = shp2.dbfHeader()
p_idx2 = None
w_idx2 = None
u_idx2 = None
for i,item in enumerate(header2):
    if item[0].upper() == 'PERMIT__95':
        p_idx2 = i
    if item[0].upper() == 'WELL_NAME':
        w_idx2 = i    
    if item[0].upper() == 'UTILITY_WE':
        u_idx2 = i
print p_idx2

wr = shapefile.Writer()
for i,item in enumerate(header1):
    wr.field(item[0],fieldType=item[1],size=item[2],decimal=item[3])

for s,r in zip(shapes1,records1):
    wr.poly([s.points],shapeType=shapefile.POINT)
    wr.record(r)
    
r_empty = []
for i,r in enumerate(records1[0]):
    r_empty.append('')    
    
plist2 = []
for s,r in zip(shapes2,records2):
    p = r[p_idx2]
    if p.startswith('06') and p not in plist1:
        w = r[w_idx2]
        u = r[u_idx2]
        rr = copy.deepcopy(r_empty)
        rr[p_idx1] = p
        rr[w_idx1] = w
        rr[u_idx1] = u
        wr.poly([s.points],shapeType=shapefile.POINT)
        wr.record(rr)
        
wr.save('shapes\\pws_combine1')


