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
#for s in str_cul_attri:
#    if s[2].upper() == 'CS-37_CULVERT':
#        print s
        
#--get the structure and culvert points
str_cul_idx,str_cul_points = msu.get_str_cul_points(str_cul_attri,names,branch_points,branch_lengths)

#for s in structs:
#    print s.id,s.branch,s.type
#    #-- find the 
#    
#    #if s.control_values[0] != 0.0:
#    #    print s.control_values[0]
#    if s.control_values[0] == s.init:
#        print '  ',s.control_values[0]
#    if s.logical_operand[0][0] == 'Hups' or \
#         s.logical_operand[0][0] == 'h' or \
#         s.logical_operand[0][0] == 'Hdws' or \
#         s.logical_operand[0][0] == 'Q_structure':
#        print '--  ',s.logical_operand[0][0],s.logical_operand[0][1],s.logical_operand[0][2],s.target_type[0]
#    else:
#        print 'No easy solution!',s.control_type[0],s.target_type[0],s.logical_operand[0]
#        for cs in s.control_strategy[0]:
#            print cs
#    #print '  ',s.control_values[0],s.logical_operand[0]
#print len(structs)    





#--str_cul_points from meters to feet
msu.m_2_ft(str_cul_points)

#--set the writer instance
wr = shapefile.Writer()
wr.field('branch_name',fieldType='C',size=50)
wr.field('str_cul_name',fieldType='C',size=50)
wr.field('str_type',fieldType='C',size=50)
wr.field('chainage',fieldType='N',size=50,decimal=10)
#print names
print len(str_cul_attri),len(str_cul_idx)
for i in range(len(str_cul_idx)):    
    this_str = str_cul_attri[str_cul_idx[i]]
    #--find the matching structure instance
    this_str_obj = None
    for s in structs:
        if s.branch == this_str[0] and \
           s.chainage == this_str[1] and \
           s.id == this_str[2]:
            this_str_obj = s
            break
    if this_str_obj == None:
        print 'Error - matching structure instance not found'
        
    
    #print str_cul_attri[str_cul_idx[i]]
    wr.poly(parts=[[str_cul_points[i]]], shapeType=1)
    wr.record([str_cul_attri[str_cul_idx[i]][0],str_cul_attri[str_cul_idx[i]][2],\
              str_cul_attri[str_cul_idx[i]][3],str_cul_attri[str_cul_idx[i]][1]])
     #if str_cul_attri[str_cul_idx[i]][2].upper() == 'CS-37_CULVERT':
     #    print 'found'
    
wr.save(target='..\\shapes\\she_structures_culverts_1')
    