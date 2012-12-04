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

in_shapename = '..\\_gis\\shapes\\sw_reaches'
out_shapename = '..\\_gis\\scratch\\sw_reaches_conn'
shp = shapefile.Reader(in_shapename)
lines = shp.shapes()
records = shp.records()
#--tolerance distance for making a connection
tol_dist = 0.0
warn_dist = 50.0

conn_list = []
nconn_list = []
id_list = []

#--set the writer instance
wr = shapefile.writer_like(in_shapename)
wr.field('nconn',fieldType='N',size=20)
wr.field('conn',fieldType='C',size=50)

name_idx,reach_idx = 0,2

f_warn = open('build_check_connectivity.warn','w')

for i,[l,r] in enumerate(zip(lines,records)):        
    if len(l.points) == 0:
        print 'null geometry found, skipping',rr
    else:
        i_name = r[name_idx]
        i_reach = r[reach_idx]    
        nconn = 0
        conn = []
        conn_names = []
        conn_dist = []
        
        for ii,[ll,rr] in enumerate(zip(lines,records)):                               
            if i != ii:            
                ii_name = rr[name_idx]
                ii_reach = rr[reach_idx]            
                if len(ll.points) == 0:
                    #print 'null geometry found, skipping',rr
                    pass
                else:
                    #--starting conn of l
                    #--the first point of ll                
                    d = dist(l.points[0],ll.points[0]) 
                    if d <= warn_dist and d > tol_dist:
                        f_warn.write(str(i_reach)+',start,'+str(ii_reach)+',start,'+str(d)+'\n')
                    elif d <= tol_dist:
                        nconn += 1
                        conn_names.append(ii_name)
                        conn.append(ii_reach)
            
                    #--the last point of ll    
                    d = dist(l.points[0],ll.points[-1])
                    if d <= warn_dist and d > tol_dist:
                        f_warn.write(str(i_reach)+',start,'+str(ii_reach)+',start,'+str(d)+'\n')
                    elif d <= tol_dist:            
                        nconn += 1
                        conn_names.append(ii_name)
                        conn.append(ii_reach)
       
                    #--ending conn of l    
                    d = dist(l.points[-1],ll.points[0])
                    if d <= warn_dist and d > tol_dist:
                        f_warn.write(str(i_reach)+',start,'+str(ii_reach)+',start,'+str(d)+'\n')
                    elif d <= tol_dist:                        
                        nconn += 1
                        conn_names.append(ii_name)
                        conn.append(ii_reach)
            
                    #--the last point of ll    
                    d = dist(l.points[-1],ll.points[-1])
                    if d <= warn_dist and d > tol_dist:
                        f_warn.write(str(i_reach)+',start,'+str(ii_reach)+',start,'+str(d)+'\n')
                    elif d <= tol_dist:                            
                        nconn += 1
                        conn_names.append(ii_name)
                        conn.append(ii_reach)
    
    
        
    
        print 'name: ',i_name,'reach: ',i_reach,' nconn: ',nconn,' conn:',conn_2_string(conn)
        print '   conn_names: ',conn_2_string(conn_names)
        #if nconn == 0:
        #    break
        r.append(nconn)
        r.append(conn_2_string(conn))
        wr.poly(parts=[l.points], shapeType=l.shapeType)
        wr.record(r)       
 
wr.save(target=out_shapename)
    
