import os
import sys
import re
import math
import numpy as np
import shapefile

def write_swr_geo_entry(f_obj,reach,num_profile_pts,profile_name):
    igeotype = 3 #irregular
    igcndop = 1 #leakance
    glk = 10.0 # k/l  ft/day/1.0 ft
    gmann = 0.03
    #print num_profile_pts
    f_obj.write('{0:10.0f}{1:10.0f}{2:10.0f}{3:10.3f}{4:10.0f}'\
                .format(reach,igeotype,igcndop,gmann,num_profile_pts))   
    f_obj.write('{0:70.3f}\n'.format(glk))
    f_obj.write('     OPEN/CLOSE '+profile_name+'\n')
    return

def distance(point1,point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
    

poly_file = 'polylines_active'
poly_shp = shapefile.Reader(shapefile=poly_file)
num_poly_lines = poly_shp.numRecords
poly_lines = poly_shp.shapes()
poly_header = poly_shp.dbfHeader()

r_idx_poly = 12
up_name_idx = 4
dw_name_idx = 5
min_elev_idx = 24
area_idx = 23
prof_idx = 22

#--first build the xsec names,num_pts and location lists
xsec_dir = '..\\MIKE_SHE_Baseline\\xsec\\'
xsec_list = os.listdir(xsec_dir)
xsec_name = []
xsec_pts = []
xsec_loc = []
xsec_area = []
xsec_min = []
for x in xsec_list:
    #name = xsec_name
    raw = x.split('.')[0].split('_')
    #--build the name
    name = x    
    num_pts = 0
    f = open(xsec_dir+x,'r')
    header = f.readline()
    raw = header.strip().split()    
    num_pts = int(raw[3])
    f.close()
    xsec = np.loadtxt(xsec_dir+x,skiprows=1)
    #print f,xsec[:,1].min()
    xsec_min.append(xsec[:,1].min())  
    
    x_pt = float(raw[4])
    y_pt = float(raw[5])
    area = float(raw[6])
     
    xsec_name.append(name)
    #xsec_chainage.append([chainage])                   
    xsec_pts.append(num_pts)
    xsec_loc.append([x_pt,y_pt])    
    xsec_area.append(area)
      



f = open('swr_ds11a.dat','w')
f.write('#  IGEONUM  IGEOTYPE   IGCNDOP  GMANNING   NGEOPTS    GWIDTH    GBELEV')
f.write('   GSSLOPE      GCND       GLK    GCNDLN   GETEXTD\n')   

f2 = open('swr_ds10.dat','w')  

#--setup a writer instance
wr = shapefile.Writer()
for item in poly_header:
    wr.field(item[0],fieldType=item[1],size=item[2],decimal=item[3])
    
#wr.field('profile',fieldType='C',size=50)
#wr.field('area',fieldType='N',size=50,decimal=5)
#wr.field('min',fieldType='N',size=50,decimal=5)

ngeonum = 1
written_xsec = []
igeo_num = [] 
igeo_list = []
igeo_reach = []

for l_idx in range(num_poly_lines): 
    #--get polyline attributes of interest
    rec = poly_shp.record(l_idx) 
   
    reach = rec[r_idx_poly]          
    up_name =  rec[up_name_idx]
    dw_name =  rec[dw_name_idx]
    #print up_name
    up_idx = xsec_name.index(up_name)
    dw_idx = xsec_name.index(dw_name)
    
    up_pt = xsec_loc[up_idx]
    dw_pt = xsec_loc[dw_idx]
    
    up_area = xsec_area[up_idx]
    dw_area = xsec_area[dw_idx]
    
    #--find the xsec closest to this reach- either start or end
    min_dist = 1.0e+20
    min_idx = None
        
    r_points = poly_lines[l_idx].points    
    for rpt in r_points:
        
        up_dist = distance(r_points[0],up_pt)
        dw_dist = distance(r_points[0],dw_pt)
        if up_dist < min_dist:
            min_dist = up_dist
            min_idx = up_idx
        if dw_dist < min_dist:
            min_dist = dw_dist
            min_idx = dw_idx                               
    
    this_num_pts = xsec_pts[min_idx]
    this_p_name = xsec_name[min_idx]
    this_p_area = xsec_area[min_idx]
    this_min_elev = xsec_min[min_idx]
    assert this_p_name in xsec_list
    rec[prof_idx] = this_p_name
    rec[area_idx] = this_p_area
    rec[min_elev_idx] = this_min_elev
    #rec.append(this_p_name)
    #rec.append(this_p_area)
    #rec.append(this_min_elev)
    wr.poly([poly_lines[l_idx].points],shapeType=3)
    wr.record(rec)
    #--write this igeo profile entry
    if this_p_name not in written_xsec:
        write_swr_geo_entry(f,ngeonum,this_num_pts,'swr_full\\xsec_navd\\'+this_p_name)    
        igeo_num.append(ngeonum)
        written_xsec.append(this_p_name)
        #igeo_reach.append(ngeonum)
        ngeonum += 1
    
    
    #--write the reach-igeonum list
    idx = written_xsec.index(this_p_name)
    f2.write('{0:10.0f}{1:10.0f}       0.0\n'.format(reach,igeo_num[idx]))            
    
f.close() 
f2.close()
wr.save('polylines_active')
