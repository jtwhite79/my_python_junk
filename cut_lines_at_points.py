import numpy as np
import shapely
from shapely.geometry import LineString,Point
import shapefile

def cut(line, distance):
    # Cuts a line in two at a distance from its starting point
    if distance <= 0.0 or distance >= line.length:
        return [LineString(line)]
    coords = list(line.coords)
    for i, p in enumerate(coords):
        pd = line.project(Point(p))
        if pd == distance:
            return [
                LineString(coords[:i+1]),
                LineString(coords[i:])]
        if pd > distance:
            cp = line.interpolate(distance)
            return [
                LineString(coords[:i] + [(cp.x, cp.y)]),
                LineString([(cp.x, cp.y)] + coords[i:])]





#--load the polylines
lfile_name = 'reaches3'
shp_lines = shapefile.Reader(lfile_name)
line_objs = shp_lines.shapes()
line_recs = shp_lines.records()
lines = []
for lo in line_objs:
    lines.append(LineString(lo.points))
    #print lines[-1].length
    
#--load the structure points
pfile_name = 'points'
shp_points = shapefile.Reader(pfile_name)
point_objs = shp_points.shapes()
point_recs = shp_points.records()
points = []
for po in point_objs:
    points.append(Point(po.points[0]))

#--output point shapefile of projected points
wr_pt = shapefile.Writer()
for i,item in enumerate(shp_points.dbfHeader()):    
    wr_pt.field(item[0],fieldType=item[1],size=item[2],decimal=item[3])
wr_pt.field('X',fieldType='N',size=50,decimal=10)
wr_pt.field('Y',fieldType='N',size=50,decimal=10)
wr_pt.field('proj_dist',fieldType='N',size=50,decimal=10)

#--output line shapefile of cut lines
wr_ln = shapefile.Writer()
for i,item in enumerate(shp_lines.dbfHeader()):
    wr_ln.field(item[0],fieldType=item[1],size=item[2],decimal=item[3])


for j,p in enumerate(points):
    #--loop over each line instance, looking for the nearest
    d = 1.0e+10
    idx = None
    projpoint,projdist = None,None
    for i,l in enumerate(lines):
        pd = l.project(p)
        #print pd
        pp = l.interpolate(pd)
        dist = p.distance(pp)
        if dist < d:
            d = dist
            projpoint = pp
            projdist = pd
            idx = i                    
                      
    #--cut the line (if needed)
    new_lines = cut(lines[idx],projdist)
    #--remove the orginal line and record
    lines.pop(idx)
    rec = line_recs.pop(idx)
    #--add the new (cut) line instances    
    for i,nl in enumerate(new_lines):
        lines.insert(idx+i,nl)
        line_recs.insert(idx+i,rec)
               
    #--write projected point shapefile
    x = list(projpoint.coords)[0][0]
    y = list(projpoint.coords)[0][1]
    wr_pt.poly([[[x,y]]],shapeType=shapefile.POINT)
    ptrec = point_recs[j]
    ptrec.append(x)
    ptrec.append(y)    
    ptrec.append(p.distance(projpoint))
    wr_pt.record(ptrec)

#--write lines shapefile
for l,r in zip(lines,line_recs):    
    coords = list(l.coords)
    #print coords
    wr_ln.poly([coords],shapeType=shapefile.POLYLINE)
    wr_ln.record(r)
    
wr_pt.save(pfile_name+'_projected')        
wr_ln.save(lfile_name+'_split')        



