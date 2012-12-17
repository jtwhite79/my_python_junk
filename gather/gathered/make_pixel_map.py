import os
import re
import numpy as np
from shapely.geometry import Polygon
import shapefile

def distance(pt1,pt2):
    return np.sqrt((pt1[0]-pt2[0])**2 + (pt1[1]-pt2[1])**2)

'''the joined pixel-grid shapefile needs to have an attribute
for the area of each polygon.
genereate using pixel_grid_union.py
'''

#--name of unioned pixel-grid shapefile
pixelgrid_shapename = '..\\..\\_gis\\scratch\\broward_pixel_grid'
#--name of pixels shape
pixel_shapename = '..\\..\\_gis\\shapes\\NEXRAD_pixels_broward'
#--name of grid shapefile
grid_shapename = '..\\..\\_gis\\shapes\\broward_grid_master'
#--name of new grid shapefile with pixel info attached
new_grid_shapename = '..\\..\\_gis\\scratch\\broward_grid_pixelmap'

#--load the pixel shapes into shapely - need to use centroid attribute later
print 'loading pixel shapefile...'
pixel_shapes,pixel_records = shapefile.load_as_dict(pixel_shapename)
pixel_polys = []
for p_shape in pixel_shapes:
    pixel_polys.append(Polygon(p_shape.points))
print 'done'

print 'loading pixel grid shapefile...'
pg_shapes,pg_records = shapefile.load_as_dict(pixelgrid_shapename,attrib_name_list=['pixel','cellnum','area'])
print pg_records.keys()
#pg_row,pg_col = np.array(pg_records['row']),np.array(pg_records['column'])
pg_pixel,pg_area = np.array(pg_records['pixel']),np.array(pg_records['area'])
pg_cellnum = np.array(pg_records['cellnum'])
#pg_delx,pg_dely = np.array(pg_records['delx']),np.array(pg_records['dely'])
print 'done'



#--writer instance
wr = shapefile.writer_like(grid_shapename)
wr.field('pixels',fieldType='C',size=50)
wr.field('fractions',fieldType='C',size=50)

#--load the grid...
print 'loading grid shapefile'
#grid_shapes,grid_records = shapefile.load_as_dict(grid_shapename)
grid_shp = shapefile.Reader(grid_shapename)
attrib_idx = shapefile.load_attrib_idx(grid_shapename)
for i in range(grid_shp.numRecords):    
    if i % 50 == 0:
        print 'cell ',i+1,' of ',grid_shp.numRecords
    #--get this shape and record    
    shp,rec = grid_shp.shape(i),grid_shp.record(i)
    cn = rec[attrib_idx['cellnum']]
    #--get the indices of cells that have this cell number
    idxs = np.argwhere(pg_cellnum==cn)
    
    #--if atleast one pixel intersected this cell
    if idxs.shape[0] > 0:                         
        tot_area = 0.0
        pixs = []
        areas = []
        for idx in idxs:                            
            tot_area += pg_area[idx]
            pixs.append(pg_pixel[idx])
            areas.append(pg_area[idx])                              
        #-- calc fractions
        p_str,f_str = '',''    
        for p,a in zip(pixs,areas):            
            f_str += '{0:4.3f} '.format((a/tot_area)[0])
            p_str += str(p[0])+' '
        
                                    
    #--for cells with no pixel intersection, IDW interpolation...crappy and slow
    else:        
        #--cast this model cell to shapely
        g_poly = Polygon(shp.points)        
        #--find the nearest 4 pixel centroids  
        #--slow      
        dist = []
        for i,p_poly in enumerate(pixel_polys):            
            dist.append([distance(g_poly.centroid.coords[0],p_poly.centroid.coords[0]),i])
        dist = np.array(dist)
        #--an index that sorts by distance
        srt_idx = np.argsort(dist[:,0])
        #--sort
        dist = dist[srt_idx]
        #--take the nearest 4 points
        dist_4 = dist[:4,0]     
        #--use them as an index since we included the index as the last column
        idx_4 = dist[:4,1].astype(int)
        #--calc IDW weighting factors
        dist_4tot = np.cumsum(dist_4)[-1]
        wght_4 = dist_4tot/dist_4
        wght_4tot = np.cumsum(wght_4)[-1]
        #--build the pixel number string and the factors string
        p_str,f_str = '',''
        for w,i in zip(wght_4,idx_4):
            #pnum = centroid_records[i][cent_pix_idx]
            pnum = pixel_records['Pixel'][i]
            f_str += '{0:4.3f} '.format(w/wght_4tot)
            p_str += str(pnum)+' '
    #--add to the shapefile
    wr.poly([shp.points],shapeType=shp.shapeType)
    rec.append(p_str)
    rec.append(f_str)
    wr.record(rec)
    #break 
wr.save(new_grid_shapename)                                         

