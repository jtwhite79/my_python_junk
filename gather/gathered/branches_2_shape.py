import re
import os
import math
import sys
import copy
import shapefile
import mikeshe_util as msu

    
############################################
#--Main
############################################

    
#--get the points from the nwk11 file
file = 'Broward_Base_05.nwk11'
point_attri = msu.get_points(file)

#--get branches
names,topo_id,st_chain,end_chain,bpoints,conn_name,conn_chain = msu.get_branches(file)

#--get branch point x and y
branch_points,branch_lengths = msu.get_branch_points(point_attri,bpoints)

#--get bounding box of the points
#branch_bbox = get_bbox(branch_points)
#print branch_bbox

#--initialize a list to track breakpoints
chain_breaks = []
for n in names: chain_breaks.append([])

#--get structures,culverts and weirs
#str_cul_attri = get_str_culvert(file)
str_cul_attri = msu.get_structures(file)

#--get xsections
xsec_file = 'raw_xsec.txt'
xsec_attri = msu.get_xsec(xsec_file)


#--set break points at connections                                                           
branch_points,branch_lengths,chain_breaks= msu.set_conn_breaks(names,conn_name,\
                        conn_chain,branch_points,branch_lengths,chain_breaks)

#--set break points at structures and culverts
branch_points,branch_lengths,chain_breaks = msu.set_str_breaks(names,str_cul_attri,\
                                      branch_points,branch_lengths,chain_breaks)

#--set break points at xsections
#branch_points,branch_lengths,chain_breaks = set_xsec_breaks(names,xsec_attri,\
#                                      branch_points,branch_lengths,chain_breaks)

#--set break points at xsections - only use unique xsections
branch_points,branch_lengths,chain_breaks = msu.set_xsec_breaks_dissolve(names,topo_id,\
                                      xsec_attri,branch_points,branch_lengths,\
                                      chain_breaks)


#--set connection points
branch_points,branch_lengths = msu.set_conn_points(names,st_chain,end_chain,bpoints,conn_name,\
                                     conn_chain,branch_points,branch_lengths)

#--branch_points from meters to feet
branch_points = msu.m_2_ft(branch_points)


#--set the writer instance
wr = shapefile.Writer()
wr.field('name',fieldType='C',size=50)
wr.field('topo_id',fieldType='C',size=50)
wr.field('reach',fieldType='N',size=50)
#start and end branch xsec profile attributes
wr.field('pf_name_up',fieldType='C',size=100)   
wr.field('pf_name_dw',fieldType='C',size=100)
wr.field('pf_area_up',fieldType='N',size=100,decimal=5)
wr.field('pf_area_dw',fieldType='N',size=100,decimal=5)
wr.field('pf_bot_up',fieldType='N',size=100,decimal=5)
wr.field('pf_bot_dw',fieldType='N',size=100,decimal=5)

#--tolerance for length of reaches and chainage length
tol = 1.0

#--some info for writing the xsections
xsec_dir = 'xsec\\'


#--loop over each branch
reach = 1
for i in range(len(branch_points)):
    #--get the indexes of breaks
    break_idx = msu.get_break_idx(branch_lengths[i],chain_breaks[i],tol=tol)                  
    
    #--get the start and ending profiles closest to each broken branch segment
    up_profiles,up_names = msu.get_profiles(names[i],topo_id[i],break_idx,\
                                        branch_lengths[i],xsec_attri,'start')
    dw_profiles,dw_names = msu.get_profiles(names[i],topo_id[i],break_idx,\
                                        branch_lengths[i],xsec_attri,'end')
    #--save the profiles in the format for SWR
    msu.write_profiles(xsec_dir,up_profiles,up_names)         
    msu.write_profiles(xsec_dir,dw_profiles,dw_names)
    #print names[i],len(break_idx),len(up_names),len(dw_names)
    #--loop over each broken branch segment 
    for j in range(1,len(break_idx)):
            
        start_idx = break_idx[j-1]
        end_idx = break_idx[j]        
        #--make sure the segment is of minimum length tol
        dist = msu.distance(branch_points[i][start_idx],branch_points[i][end_idx])        
        if dist >= tol:
            num_pts = end_idx - start_idx + 1 
            wr.poly(parts=[branch_points[i][start_idx:end_idx+1]], shapeType=3)
            wr.record([names[i],topo_id[i],reach,up_names[j-1],dw_names[j-1],\
            up_profiles[j-1][6],dw_profiles[j-1][6],up_profiles[j-1][5],\
            dw_profiles[j-1][5]])
            reach += 1   
        else:
            print names[i],start_idx,end_idx,len(branch_points[i])            
    #if i > 2 :
    #    break       
    
wr.save(target='..\\shapes\\she_branches_xsec1')
    