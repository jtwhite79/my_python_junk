import sys
import math
import shapefile

def dist(point1,point2):
    xx = (point1[0] - point2[0])**2
    yy = (point1[1] - point2[1])**2
    return math.sqrt(xx+yy)

def conn_2_string(conn):
    conn_str = ''
    for c in conn:
        conn_str += str(c) + ' '
    return conn_str

file = 'she_branches_xsec1'
shp = shapefile.Reader(shapefile=file)

lines = shp.shapes()
dbf_header = shp.dbfHeader()
#--tolerance distance for making a connection
tol = 0.0

#--the dbf attribute index of the reach identifier
reach_idx = 2 
name_idx = 0

conn_list = []
nconn_list = []
id_list = []

#--set the writer instance
wr = shapefile.Writer()
for item in dbf_header:
    wr.field(item[0],fieldType=item[1],size=item[2],decimal=item[3])

wr.field('nconn',fieldType='N',size=20)
wr.field('conn',fieldType='C',size=50)

l_idx = 0
for l in lines:    
    this_rec = shp.record(l_idx)
    name = this_rec[name_idx]
    reach = this_rec[reach_idx]
    #--loop over each line and check the 
    #--first and last points against 
    #--the tolerance distance
    ll_idx = 0
    nconn = 0
    conn = []
    conn_names = []
        
    for ll in lines:
                       
        #if dist(l.points[0],ll.points[0]) < tol:
        #    print dist(l.points[0],ll.points[0])
        #        
        #if dist(l.points[0],ll.points[-1]) < tol:
        #    print dist(l.points[0],ll.points[-1])    
        
        #--starting conn of l
        #--the first point of ll
        if dist(l.points[0],ll.points[0]) <= tol and ll_idx != l_idx:
            nconn += 1
            conn.append(shp.record(ll_idx)[reach_idx])
            conn_names.append(shp.record(ll_idx)[name_idx])
            
        #--the last point of ll    
        elif dist(l.points[0],ll.points[-1]) <= tol and ll_idx != l_idx:
            nconn += 1
            conn.append(shp.record(ll_idx)[reach_idx])
            conn_names.append(shp.record(ll_idx)[name_idx])
       
        #--ending conn of l    
        if dist(l.points[-1],ll.points[0]) <= tol and ll_idx != l_idx:
            nconn += 1
            conn.append(shp.record(ll_idx)[reach_idx])            
            conn_names.append(shp.record(ll_idx)[name_idx])
            
        #--the last point of ll    
        elif dist(l.points[-1],ll.points[-1]) <= tol and ll_idx != l_idx:
            nconn += 1
            conn.append(shp.record(ll_idx)[reach_idx])        
            conn_names.append(shp.record(ll_idx)[name_idx])
            
        ll_idx += 1
    
    #--remove any duplicates?    
    if len(conn) > 1:
        conn.sort()
        last = conn[-1]
        for i in range(len(conn)-2, -1, -1):
            if last == conn[i]:
                del conn[i]
                nconn -= 1
            else:
                last = conn[i]
        
    
    print 'name: ',name,'reach: ',reach,' nconn: ',nconn,' conn:',conn_2_string(conn)
    print '   conn_names: ',conn_2_string(conn_names)
    #if nconn == 0:
    #    break
    this_rec.append(nconn)
    this_rec.append(conn_2_string(conn))
    wr.poly(parts=[l.points], shapeType=3)       
    wr.record(this_rec)   
    l_idx += 1
 
wr.save(target='she_branches_conn')
    