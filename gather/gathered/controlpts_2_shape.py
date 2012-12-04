import re
import math
import sys
import shapefile
import mikeshe_struct as mss
import mikeshe_util as msu
reload(msu)


    
############################################
#--Main
############################################


#--get the control structures
file = 'Broward_Base_05.nwk11'
structs = mss.load_structure(file)
    
#--get the points from the nwk11 file
file = 'Broward_Base_05.nwk11'
point_attri = msu.get_points(file)

#--get branches
names,topo_id,st_chain,end_chain,bpoints,conn_name,conn_chain = msu.get_branches(file)

#--get branch point x and y
branch_points,branch_lengths = msu.get_branch_points(point_attri,bpoints)


#--get structures and culverts
str_cul_attri = msu.get_structures(file)

#--build a list of control points
cntl_pts = []
struct_map = []
for idx in range(len(structs)):
    #print s.id
    s = structs[idx]
    for cp in s.control_points:
        print cp[0],cp[1]
        #--strip off the leading single quote
        cntl_pts.append([cp[0][1:],cp[1],'junk',s.id])
        struct_map.append(idx)
        


#--get the structure control points
cntl_idx,cntl_points = msu.get_str_cul_points(cntl_pts,names,branch_points,branch_lengths)
     
#--str_cul_points from meters to feet
msu.m_2_ft(cntl_points)

#--set the writer instance
wr = shapefile.Writer()
wr.field('struct_name',fieldType='C',size=50)
wr.field('cp_name',fieldType='C',size=50)
wr.field('cp_chainage',fieldType='N',size=50,decimal=3)

#print names

for i in range(len(cntl_idx)):    
    this_str = structs[struct_map[cntl_idx[i]]]         
    this_cntl_pts = cntl_pts[cntl_idx[i]]    
    #print str_cul_attri[str_cul_idx[i]]
    wr.poly(parts=[[cntl_points[i]]], shapeType=1)
    wr.record([this_str.id,this_cntl_pts[0],this_cntl_pts[1]])
    
wr.save(target='..\\shapes\\she_controlpoints_1')
    