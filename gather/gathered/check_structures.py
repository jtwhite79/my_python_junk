import sys
import math
import shapefile

def dist(point1,point2):
    xx = (point1[0] - point2[0])**2
    yy = (point1[1] - point2[1])**2
    return math.sqrt(xx+yy)

line_shapename = '..\\_gis\\shapes\\sw_reaches'
#shp_lines = shapefile.Reader(line_shapename)
#lines = shp_lines.shapes()
#l_records = shp_lines.records()
#l_name_idx,reach_idx = 0,2
lines,l_records = shapefile.load_as_dict(line_shapename)


#--tolerance distance
warn_dist = 50.0
tol_dist = 0.0

#--set the writer instance
in_shapename = '..\\_gis\\shapes\\sw_structures'
out_shapename = '..\\_gis\\scratch\\sw_structures_reaches'
shp_points = shapefile.Reader(in_shapename)
points = shp_points.shapes()
p_records = shp_points.records()
p_name_idx,dwnstr_idx = 4,6

wr = shapefile.writer_like(in_shapename)
wr.field('upstream',fieldType='N',size=10)


f_warn = open('check_structures.warn','w')
for p,r in zip(points,p_records):            
    s_name = r[p_name_idx]
    s_dwn_reach = r[dwnstr_idx]

    #--find the index of the downstream reach
    dw_idx = None
    for i,reach in enumerate(l_records['reach']):
        if reach == s_dwn_reach:
            dw_idx = i
            break
    if dw_idx == None:
        raise IndexError('downstream reach for structure '+s_name+' not found in reaches')
    
    #--check that the downstream reach is within the tolerance distance
    dwnstr_line = lines[dw_idx]                            
    
    d_start = dist(p.points[0],dwnstr_line.points[0]) 
    d_end = dist(p.points[0],dwnstr_line.points[-1]) 
    if d_start > tol_dist and d_end > tol_dist:
        f_warn.write(str(s_name)+','+str(s_dwn_reach)+',start,'+str(d_start)+',end,'+str(d_end)+'\n')            
    
    #--find the upstream reach
    up_dist = 1.0e+10
    up_reach = None
    for ii,[line,reach] in enumerate(zip(lines,l_records['reach'])):
        if ii != dw_idx:
            d_start = dist(p.points[0],line.points[0]) 
            d_end = dist(p.points[0],line.points[-1]) 
            if d_start < up_dist:
                up_reach = reach
                up_dist = d_start
            if d_end < up_dist:
                up_reach = reach
                up_dist = d_end
    if up_dist > tol_dist:                    
        f_warn.write(str(s_name)+','+str(up_reach)+',upstream,'+str(up_dist)+'\n')                               
                    
    r.append(up_reach)    
    wr.poly(parts=[p.points], shapeType=p.shapeType)
    wr.record(r)       
 
wr.save(target=out_shapename)
    

