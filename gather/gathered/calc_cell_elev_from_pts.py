import sys
import math
import shapefile

def dist(point1,point2):
    xx = (point1[0] - point2[0])**2
    yy = (point1[1] - point2[1])**2
    return math.sqrt(xx+yy)


def get_cent_of_cell(points):
    xmin,xmax = 1.0e+20,-1.0e+20
    ymin,ymax = 1.0e+20,-1.0e+20
    for p in points:
        if p[0] < xmin:
            xmin = p[0]
        if p[0] > xmax:
            xmax = p[0]
        if p[1] < ymin:
            ymin = p[1]
        if p[1] > ymax:
            ymax = p[1]
    #print xmin,xmax,ymin,ymax
    x = (xmin+xmax) / 2.0
    y = (ymin+ymax) / 2.0
    return [x,y]
    



#--search radius 
tol = 350.0


#--index of elev value in elev points shapefile
idx_elev = 1


#--index of row and col values in the grid shapefile
idx_row = 0
idx_col = 1
idx_num = 3

#-- get elev points
print 'loading elev points...'
file = 'bor_srtm_pts'
shp_pts = shapefile.Reader(shapefile=file)
points = shp_pts.shapes()
print 'elev points loaded'
#print shp_pts.record(0)[idx_elev]


#--set the writer instance
wr = shapefile.Writer()
wr.field('row',fieldType='N',size=20)
wr.field('col',fieldType='N',size=20)
wr.field('cellnum',fieldType='N',size=20)
wr.field('elevation',fieldType='N',size=100,decimal=10)

#--get the grid polygons
print 'loading grid polygons...'
file = 'broward_grid'
shp_poly = shapefile.Reader(shapefile=file)
cells = shp_poly.shapes()
print 'grid loaded'

#print shp_poly.record(0)

#--loop over each cell, looking for elev points within the tol distance
for c in range(len(cells)):
    this_record = shp_poly.record(c)  
    print 'working on grid cell ',c+1,' of ',len(cells)
    this_cent = get_cent_of_cell(cells[c].points)     
    this_elev,this_wght = [],[]
    tot_wght = 0.0
    
    for p in range(len(points)): 
        this_dist = dist(points[p].points[0],this_cent)    
        if this_dist <= tol:
           this_elev.append(shp_pts.record(p)[idx_elev])
           try:
               this_wght.append(1.0/this_dist)
               tot_wght += 1.0/this_dist
           except:
               this_wght.append(100.0)
               tot_wght += 100.0
    if len(this_elev) > 0:
       idw_elev = 0
       for e in range(len(this_elev)):
           idw_elev += this_elev[e]*this_wght[e] 
       idw_elev /= tot_wght              
    else:
        #print 'Warning - no elev points within search radius for cell: '\
        #       ,shp_poly.record(c)[idx_row],shp_poly.record(c)[idx_col]
        idw_elev = -999.9
    print '  ',idw_elev,len(this_elev)
    wr.poly(parts=[cells[c].points], shapeType=5)   
    wr.record(this_record[idx_row],this_record[idx_col],this_record[idx_num],idw_elev)
    
    
wr.save(target='grid_elev_idw_test')           
