import re
import sys
import math
import shapefile
import mikeshe_struct as mss


def dist(point1,point2):
    xx = (point1[0] - point2[0])**2
    yy = (point1[1] - point2[1])**2
    return math.sqrt(xx+yy)


def find_istrrch_istrconn(str_point,grouped,group_idxs,ply_shp):
    
    dist_list = [] 
    reach_list = []
    for gidx in range(len(grouped)):
        this_start_idx = group_idxs[gidx][0]     
        this_end_idx = group_idxs[gidx][-1]  
        this_start_rec = ply_shp.record(this_start_idx)               
        this_start_reach = this_start_rec[ply_reach_idx]              
        this_end_rec = ply_shp.record(this_end_idx)               
        this_end_reach = this_end_rec[ply_reach_idx]              
        #--the first point of the first reach of this rchgrp
        this_start_first_point = grouped[gidx][0].points[0] 
        #--the last point of the first reach of this rchgrp
        this_start_last_point = grouped[gidx][0].points[-1] 
        #--the first point of the last reach of this rchgrp
        this_end_first_point = grouped[gidx][-1].points[0]  
        #--the last point of the last reach of this rchgrp
        this_end_last_point = grouped[gidx][-1].points[-1]
               
        sf_dist = dist(str_point,this_start_first_point)
        sl_dist = dist(str_point,this_start_last_point)
        ef_dist = dist(str_point,this_end_first_point)
        el_dist = dist(str_point,this_end_last_point) 
        
        if sf_dist < sl_dist : s_dist = sf_dist
        else: s_dist = sl_dist
            
        if ef_dist < el_dist : e_dist = ef_dist
        else: e_dist = el_dist                 
        
        if s_dist < e_dist:  
            dist_list.append(s_dist)
            reach_list.append(this_start_reach)    
        else:                                
            dist_list.append(e_dist)  
            reach_list.append(this_end_reach)    
        
    
    #--find the closest two reaches in dist_list
    min_1 = min(dist_list)
    min_1_idx = dist_list.index(min_1)
    reach_1 = reach_list[min_1_idx]
    dist_list.remove(min_1)
    reach_list.remove(reach_1)
    min_2 = min(dist_list)
    min_2_idx = dist_list.index(min_2)
    reach_2 = reach_list[min_2_idx]
    
    #print str_name.ljust(20)+' {0:5.0f} {1:5.0f}'.format(reach_1,reach_2)#,min_1,min_2                   
    return reach_1,reach_2
    #break     
    

def centroid(points):
    total = [0.0,0.0]
    c = 0
    for p in points:
        total[0] += p[0]
        total[1] += p[1]
        c += 1
    return [float(total[0]/c),float(total[1]/c)]
    






#--load the structure information from the MIKE11 nwk file
file = '..\\MIKE_SHE_Baseline\\Broward_Base_05.nwk11'
structs = mss.load_structure(file)
weirs = mss.load_weirs(file)
culverts = mss.load_culverts(file)

#--load the structure points
file = 'she_structures_culverts_1'
str_shp = shapefile.Reader(shapefile=file)

str_points = str_shp.shapes()
str_header = str_shp.dbfHeader()

#--the dbf attribute index of the str name
str_name_idx = 1
str_br_idx = 0
str_ch_idx = 3

#--load the swrpre polylines
file = 'polylines_active'
ply_shp = shapefile.Reader(shapefile=file)
ply_lines = ply_shp.shapes()
ply_header = ply_shp.dbfHeader()
ply_recs = ply_shp.records()

ply_rchgrp_idx = 17
ply_reach_idx = 16

ply_centroids = []
for idx in range(ply_shp.numRecords):
    ply_centroids.append(centroid(ply_lines[idx].points))

#print ply_header
#print ply_header[ply_rchgrp_idx]
#print ply_header[ply_reach_idx]


#--load the control points shapefile
file = 'she_controlpoints_1'
ctl_shp = shapefile.Reader(shapefile=file)
ctl_pts = ctl_shp.shapes()
ctl_header = ctl_shp.dbfHeader()
ctl_recs = ctl_shp.records()
ctl_name_idx = 0
ctl_br_idx = 1
ctl_ch_idx = 2



#--group the polylines by reachgroup
grouped = []
group_names = []
group_idxs = []
for idx in range(len(ply_lines)):
    this_rec = ply_shp.record(idx)
    this_rchgrp = this_rec[ply_rchgrp_idx]
    if this_rchgrp in group_names:
        i = group_names.index(this_rchgrp)
        grouped[i].append(ply_lines[idx])
        group_idxs[i].append(idx)
    else:
        group_names.append(this_rchgrp)
        grouped.append([ply_lines[idx]])
        group_idxs.append([idx])

#print group_names
#print group_names[0]
#print len(grouped[0])

#--loop over each structure and find the closest two reachgroups,
#--and find the closest reaches within each

#--first the easy ones - weirs, culverts
missing = []
complete = []
#-skip weirs for storage or bridges
keywords = ['storage','stoareg','bridge']
re_list = []
for k in keywords:
    re_list.append(re.compile(k,re.IGNORECASE))
    
#stor = re.compile('storage',re.IGNORECASE)
#stor2 = re.compile('stoareg',re.IGNORECASE)
#brig = re.compile('bridge',re.IGNORECASE)       
#re_list = [stor,stor2,brig]

for w in weirs:
    accept = True
    for r in re_list:
        #print w.id, w.branch
        #print r.search(w.id),r.search(w.branch)
        if r.search(w.id) != None or \
           r.search(w.branch) != None:           
            accept = False#    
    if accept != False:
        #--find the index of the structure point        
        found = 'f'
        for idx in range(len(str_points)):
            rec = str_shp.record(idx)
            #print w.branch,rec[str_br_idx],idx
            if w.branch.strip() == rec[str_br_idx].strip() and \
               w.id.strip() == rec[str_name_idx].strip():               
                found = idx
                break
        #print found        
        if found == 'f':
            print 'not found',w.id
            missing.append(w)
            sys.exit()
        else:
            str_point = str_points[idx].points[0]
            istrrch,istrconn = find_istrrch_istrconn(str_point,grouped,\
                                                     group_idxs,ply_shp)
            w.set_istrrch_istrconn(istrrch,istrconn)
            print w.id,istrrch,istrconn
            complete.append(w)
                   
for c in culverts:    
    accept = True
    for r in re_list:        
        if r.search(w.id) != None or \
           r.search(w.branch) != None:           
            accept = False
    
    if accept == True:
        #--find the index of the structure point    
        found = 'f'
        for idx in range(len(str_points)):
            rec = str_shp.record(idx)
            #print w.branch,rec[str_br_idx]
            if c.branch.strip() == rec[str_br_idx].strip() and \
               c.id.strip() == rec[str_name_idx].strip():                  
                found = idx
                break
        if found == 'f':
            print 'not found',c.id
            missing.append(c)        
        else:
            str_point = str_points[idx].points[0]
            istrrch,istrconn = find_istrrch_istrconn(str_point,grouped,\
                                                     group_idxs,ply_shp)
            c.set_istrrch_istrconn(istrrch,istrconn)
            print c.id,istrrch,istrconn
            complete.append(c)


#for s in structs:    
#    #--find the index of the structure point    
#    found = 'f'
#    for idx in range(len(str_points)):
#        rec = str_shp.record(idx)
#        #print s.branch,s.id,rec[str_br_idx],rec[str_name_idx]
#        if s.branch.strip() == rec[str_br_idx].strip() and \
#           s.id.strip() == rec[str_name_idx].strip():                  
#            found = idx
#            break
#    if found == 'f':
#        print 'not found',s.id
#        missing.append(s)
#        sys.exit()        
#    else:
#        str_point = str_points[idx].points[0]
#        istrrch,istrconn = find_istrrch_istrconn(str_point,grouped,\
#                                                 group_idxs,ply_shp)
#        #--find istrorch
#        
#        ctl_reaches = []
#        ctl_tol = 0.01
#        for c in s.control_points:
#            #--find the xy point for this control point
#            ctl_xy = None
#            for idx in range(ctl_shp.numRecords):
#                ch_diff = abs(ctl_recs[idx][ctl_ch_idx] - c[1])
#                name = ctl_recs[idx][ctl_br_idx].strip()
#                #print name,ch_diff
#                #--strip off the leading single quote in c[0]
#                if name == c[0][1:].strip() and \
#                   ch_diff < ctl_tol:
#                    ctl_xy = ctl_pts[idx].points[0]
#                        
#            min_dist = 1.0e+20
#            min_idx = None            
#            for idx in range(ply_shp.numRecords):
#                this_centroid = ply_centroids[idx]                
#                try:
#                    d = dist(this_centroid,ctl_xy)
#                except:
#                    d = 1.0e+20
#                if d < min_dist:
#                    min_dist = d
#                    min_idx = idx
#            if min_idx != None:
#                ctl_reaches.append(ply_recs[min_idx][ply_reach_idx])                    
#        #print min_dist,ply_recs[min_idx][ply_reach_idx]
#        #sys.exit() 
#                          
#        #print '  ',len(ctl_reaches)
#        
#        #--if no control points were found
#        #if len(ctl_reaches) == 0:            
#        #    this_lo = s.logical_operand[0]
#        #    if this_lo[0] == 'Hups' or \
#        #       this_lo[0] == 'Hdws':
#        
#        if len(ctl_reaches) > 0:
#            istrorch = ctl_reaches[0]
#        else:
#            istrorch = -999                                       
#        s.set_istrrch_istrconn(istrrch,istrconn)                      
#        s.set_istrorch(istrorch,istroqcon=-999)
#        print s.id,istrrch,istrconn
#        complete.append(s)
#        #if len(ctl_reaches) == 0:
#        #    sys.exit()         
#        #if s.id == 'CS-1_pump':
#        #    break


#--build the nstruct list 
nstruct = []
for idx in range(len(ply_lines)):
    nstruct.append(0)

for c in complete:
    idx = c.istrrch-1
    nstruct[idx] += 1



#--now write swr structure dataset...finally
f = open('swr_structures.dat','w')
mss.write_swr_dataset13_header(f)
for c in complete:
    idx = c.istrrch-1
    c.write_swr_entry(f,nstruct[idx])
    nstruct[idx] -= 1
    if nstruct[idx] < 0:
        print 'something is wrong...'

    
print 'missing...'    
for m in missing:
    print m.branch,m.chainage,m.id
      