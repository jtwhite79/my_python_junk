import re
import math
import sys
import shapefile


def get_points(file):
    
    pt1 = re.compile('\[POINTS\]',re.IGNORECASE)
    pt2 = re.compile('point')
    pt3 = re.compile('EndSect  // POINTS',re.IGNORECASE)
    
    point_x,point_y,point_attri = [],[],[]
    
    f = open(file,'r')
    while True:
        line = f.readline()
        if pt1.search(line) != None:
            while True:
                line = f.readline()
                if pt3.search(line) != None:
                    f.close()
                    return point_attri
                raw = line.strip().split(',')
                this_name = float(raw[0].split('=')[-1].strip()) 
                this_list = [this_name] 
                for r in raw[1:]: 
                    this_list.append(float(r))
                point_attri.append(this_list)
                

def get_branches(file):
    br = re.compile('\[BRANCHES\]',re.IGNORECASE)
    br1 = re.compile('\[branch\]',re.IGNORECASE)
    br2 = re.compile('EndSect  // BRANCHES',re.IGNORECASE)
    stor = re.compile('storage',re.IGNORECASE)
    name_list,st_chain_list,end_chain_list,points_list = [],[],[],[]
    conn_name_list,conn_chain_list = [],[]
    
    f = open(file,'r')
    while True:
        line = f.readline()
        if br2.search(line) != None:
           f.close()
           return name_list,st_chain_list,end_chain_list,\
                  points_list,conn_name_list,conn_chain_list
        if br1.search(line) != None:
            definitions = f.readline()
            #--parse the definitions line into variables
            name,st_chain,end_chain,dir = parse_def_line(definitions)
            connections = f.readline()
            #--parse the connections line
            conn_name,conn_chain = parse_conn_line(connections)
            points = f.readline()
            #--parse the points line
            points = parse_points(points,dir)
            if stor.search(name) == None:
                name_list.append(name)
                st_chain_list.append(st_chain)
                end_chain_list.append(end_chain)
                points_list.append(points) 
                conn_name_list.append(conn_name)
                conn_chain_list.append(conn_chain)
       

def parse_conn_line(line):
    raw = line.strip().split('=')[-1].split(',') 
    st_name = raw[0].strip()[1:-1]
    end_name = raw[2].strip()[1:-1]
    st_ch = float(raw[1])
    end_ch = float(raw[3])
    if st_name == '' and end_name == '':
        return [],[]
    elif st_name == '':
        return [end_name],[end_ch]        
    elif end_name == '':
        return [st_name],[st_ch]        
    else:
        return [st_name,end_name],[st_ch,end_ch]

                  
def parse_def_line(def_line):
    raw = def_line.strip().split(',')
    name = raw[0].split('=')[-1].strip()[1:-1] 
    #print name
    st_chain = float(raw[2])   
    end_chain = float(raw[3])   
    dir = False
    if int(raw[4]) == 0: dir = True
    return name,st_chain,end_chain,dir


def parse_points(points,dir):
    raw = points.strip().split(',')
    point_list = [int(raw[0].split('=')[-1])]
    for r in raw[1:]: point_list.append(int(r))
    
    if dir == False: 
        point_list.reverse()
    return point_list


def get_branch_points(point_attri,bpoints):
    #--get the points and chainage lengths associated with each branch
    branch_points = []
    branch_lengths = []
    for bp in bpoints:
        this_branch_points = []
        this_branch_lengths = []
        for p in bp:
            #--get the x, y, and chainage length of 
            this_x,this_y,this_len = get_point_xy_len(p,point_attri)
            #print p,this_x,this_y
            this_branch_points.append([this_x,this_y])
            this_branch_lengths.append(this_len)
        branch_points.append(this_branch_points)
        branch_lengths.append(this_branch_lengths)
    return branch_points,branch_lengths


def get_point_xy_len(p,point_attri):
    for pt in point_attri:        
        if pt[0] == p: return pt[1],pt[2],pt[4]
    print 'bpoint not found in point_attri list: ',p
    sys.exit()


def m_2_ft(points):
    for bp in points:
        try:
            for p in bp:
                p[0] *= 3.281
                p[1] *= 3.281
        except:
            bp[0] *= 3.281
            bp[1] *= 3.281
    return points


def get_all_structures(file):
    weir = re.compile('\[weir_data\]',re.IGNORECASE)
    culvert = re.compile('\[culvert_data\]',re.IGNORECASE)
    struct = re.compile('\[control_str_data\]',re.IGNORECASE)
    f = open(file,'r')
    loc_line = []
    cul_count,weir_count,str_count = 0,0,0
     
    while True:
        line = f.readline()
        if line == '':
            break
        str_type = None
        
        if weir.search(line) != None:
            str_type = 'weir'
        elif culvert.search(line) != None:
            str_type = 'culvert'
        elif struct.search(line) != None:
            str_type = 'control_structure'
        if str_type != None:            
            this_loc_line = f.readline()
            raw = this_loc_line.strip().split(',')
            this_loc_line = [raw[0].split('=')[-1].strip()[1:-1]]
            this_loc_line.append(float(raw[1]))
            this_loc_line.append(raw[2].strip()[1:-1])
            this_loc_line.append(str_type)
            this_loc_line.extend(raw[3:])
            loc_line.append(this_loc_line)
        #if str.search(line) != None: str_count += 1
        #if culvert    
    f.close()
    #print len(loc_line)
    return loc_line


def list_2_string(l,delimiter=' '):
    st = ''
    for i in l:  
        st = st + ' ' + str(i)
    return st


def get_point(name,name_list,chainage,chainage_list,point_list):
    #--get the index of the connection branch
    branch_idx = get_branch_index_by_name(name,name_list) 
    if branch_idx != None:
        #print name,names[branch_idx]
        
        #--get the chainage index of the two nearest points in the connection branch
        ch_idx = get_nearest_2_point_indexes(chainage,chainage_list[branch_idx])
        if ch_idx[0] == None:
            print 'unable to find chainage points for point: ',name
            raise IndexError  
        #print ch_idx,len(branch_points[branch_idx]),len(branch_lengths[branch_idx])
        
        #--calc the fraction distance along the branch for the connection  
        numer = (chainage - chainage_list[branch_idx][ch_idx[0]])
        demon = (chainage_list[branch_idx][ch_idx[1]] - chainage_list[branch_idx][ch_idx[0]])
        #print branch_lengths[branch_idx][ch_idx[1]], branch_lengths[branch_idx][ch_idx[0]] 
        try:
            frac_dist = numer / demon
        except:
            frac_dist = 0.0
        
        #--get the new connection point using the chainage lengths and the two nearest points
        point = interp_conn_point(frac_dist,\
                         point_list[branch_idx][ch_idx[0]],\
                         point_list[branch_idx][ch_idx[1]])        
        #print 'frac_dist,ch_idx,point',frac_dist,ch_idx,point
        
        return point,branch_idx,ch_idx
    else: 
        print 'branch not found: ',name
        return None,None,None
                       

def get_str_cul_points(str_cul_attri,names,branch_points,branch_lengths):
    
    str_cul_points = []
    str_cul_idx = []
    for i in range(len(str_cul_attri)):
        
        str_point,branch_idx,ch_idx = get_point(str_cul_attri[i][0],names,str_cul_attri[i][1],branch_lengths,branch_points)
        
        if branch_idx != None:
            str_cul_points.append(str_point)            
            str_cul_idx.append(i)
        #if str_cul_attri[i][0] == '2_c1_e1_e2':sys.exit()
        else:
            print 'structure point not found:',str_cul_attri[i][0],str_cul_attri[i][1],str_cul_attri[i][3]    
    return str_cul_idx,str_cul_points


def get_branch_index_by_name(name,names):
    reg = re.compile(name)#,re.IGNORECASE)
    for n in range(len(names)):
        #print names[n],name
        #if reg.search(names[n]) != None:
        if names[n].upper() == name.upper():
            idx = n
            return idx 
    return None



            
def interp_conn_point(frac_dist,point1,point2):
    dist = distance(point1,point2)    
    delta_x = frac_dist * (point2[0] - point1[0])
    delta_y = frac_dist * (point2[1] - point1[1])
    #print 'delta_x,delta_y',delta_x,delta_y
    #print 'dist, frac_dist',dist,frac_dist
    return [point1[0] + delta_x,point1[1] + delta_y]    
    
                           
def distance(point1,point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

            
def get_nearest_2_point_indexes(chainage,branch_lengths):
    #print branch_lengths
    for i in range(1,len(branch_lengths)):
        if chainage >= branch_lengths[i-1] and chainage <= branch_lengths[i]:
            #print 'chainage points',chainage,branch_lengths[i-1],branch_lengths[i]
            return [i-1,i]
            ##--make sure the closest point is in position 0           
            #if abs(chainage - branch_lengths[i-1]) < abs(chainage - branch_lengths[i]):
            #    return [i-1,i]
            #else: 
            #    return [i,i-1]
                



    
############################################
#--Main
############################################

    
#--get the points from the nwk11 file
file = 'Broward_Base_05.nwk11'
point_attri = get_points(file)

#--get branches
names,st_chain,end_chain,bpoints,conn_name,conn_chain = get_branches(file)

#--get branch point x and y
branch_points,branch_lengths = get_branch_points(point_attri,bpoints)


#--get structures and culverts
str_cul_attri = get_all_structures(file)
#for s in str_cul_attri:
#    if s[2].upper() == 'CS-37_CULVERT':
#        print s
        
#--get the structure and culvert points
str_cul_idx,str_cul_points = get_str_cul_points(str_cul_attri,names,branch_points,branch_lengths)


#--str_cul_points from meters to feet
m_2_ft(str_cul_points)

#--set the writer instance
wr = shapefile.Writer()
wr.field('branch_name',fieldType='C',size=50)
wr.field('str_cul_name',fieldType='C',size=50)
wr.field('str_type',fieldType='C',size=50)
wr.field('chainage',fieldType='N',size=50,decimal=10)
#print names
print len(str_cul_attri),len(str_cul_idx)
for i in range(len(str_cul_idx)):
    
        #print str_cul_attri[str_cul_idx[i]][0]
        wr.poly(parts=[[str_cul_points[i]]], shapeType=1)
        wr.record([str_cul_attri[str_cul_idx[i]][0],str_cul_attri[str_cul_idx[i]][2],\
                  str_cul_attri[str_cul_idx[i]][3],str_cul_attri[str_cul_idx[i]][1]])
#        if str_cul_attri[str_cul_idx[i]][2].upper() == 'CS-37_CULVERT':
#            print 'found'
    
wr.save(target='..\\shapes\\she_structures_culverts_1')
    