import sys
import math
import shapefile

def dist(point1,point2):
    xx = (point1[0] - point2[0])**2
    yy = (point1[1] - point2[1])**2
    return math.sqrt(xx+yy)


line_file = 'she_branches_xsec_mod_primary_geo_dissolve'
line_shp = shapefile.Reader(shapefile=line_file)
header = line_shp.dbfHeader()
lines = line_shp.shapes()

pt_file = 'she_struct_primary'
pt_shp = shapefile.Reader(shapefile=pt_file)
points = pt_shp.shapes()
#print len(points)
#--tolerance distance for making a break
tol = 0.0

#--set the writer instance
wr = shapefile.Writer()
for item in header:
    wr.field(item[0],fieldType=item[1],size=item[2],decimal=item[3])
wr.field('reach_num',fieldType='N',size=10,decimal=0)


#--lists to track lines to split
split_l_idx_list = []
split_v_idx_list = []


#--loop over each point
for pt_idx in range(len(points)):
    
    #--find the nearest vertex in the lines
    
    min_l_idx = False
    min_v_idx = False
    min_dist = 1.0e+20
    for l_idx in range(len(lines)):
        this_vertices = lines[l_idx].points
        for v_idx in range(len(this_vertices)): 
            #print pt.points
            this_dist = dist(points[pt_idx].points[0],this_vertices[v_idx])
            if this_dist < min_dist:
                min_l_idx = l_idx
                min_v_idx = v_idx                
                min_dist = this_dist
    #print min_dist,pt_shp.record(pt_idx)
    if min_l_idx != False: 
        split_l_idx_list.append(min_l_idx)
        split_v_idx_list.append(min_v_idx)
    


#--loop over each line and check for splits
reach = 1
for l_idx in range(len(lines)):
    this_split_l_list = []
    
    #--start the vertex list with '0' for the first position
    this_split_v_list = [0]
    for s_idx in range(len(split_l_idx_list)):
        if split_l_idx_list[s_idx] == l_idx:
            this_split_l_list.append(split_l_idx_list[s_idx])
            this_split_v_list.append(split_v_idx_list[s_idx])
    
            
    
    this_line_verts = lines[l_idx].points        
    #--add the last position index to the split list
    this_split_v_list.append(len(this_line_verts))
    
    #--remove duplicates
    this_split_v_list = list(set(this_split_v_list))
    #--sort the vertex index list
    this_split_v_list.sort()
    
    for vert in range(1,len(this_split_v_list)):
        this_rec = line_shp.record(l_idx)
        start = this_split_v_list[vert-1]
        end = this_split_v_list[vert]
        
        #if (end - start) == 1:   
            #print start,end,this_line_verts[start:end+1]         
            #wr.poly(parts=[this_line_verts[start:end+1]], shapeType=3)                                                   
            #wr.record([reach])                   
        #    reach += 1                                  
        #else:
        #print start,end,this_line_verts[start:end+1]         
        wr.poly(parts=[this_line_verts[start:end+1]], shapeType=3)
        this_rec.append(reach)                                                   
        wr.record(this_rec)                                                                                                                
        reach += 1
wr.save(target='she_primary_split') 


#    wr.poly(parts=[l.points], shapeType=3)   
#    wr.record([name,reach,nconn,conn_2_string(conn),conn_2_string(conn_names)])   
#    l_idx += 1
# 
# 
#
#wr.save(target='she_primary_xsec_conn')
    