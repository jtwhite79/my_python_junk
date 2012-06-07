import re
import os
import math
import sys
import copy
import shapefile


def get_points(file):
    #--load the points from a MIKE11 nwk file
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
    #--load the branch info from a MIKE11 nwk file
    br = re.compile('\[BRANCHES\]',re.IGNORECASE)
    br1 = re.compile('\[branch\]',re.IGNORECASE)
    br2 = re.compile('EndSect  // BRANCHES',re.IGNORECASE)
    stor = re.compile('storage',re.IGNORECASE)
    name_list,st_chain_list,end_chain_list,points_list = [],[],[],[]
    conn_name_list,conn_chain_list,topo_id_list = [],[],[]
    f = open(file,'r')
    while True:
        line = f.readline()
        if br2.search(line) != None:
           f.close()
           return name_list,topo_id_list,st_chain_list,end_chain_list,\
                  points_list,conn_name_list,conn_chain_list
        if br1.search(line) != None:
            definitions = f.readline()
            #--parse the definitions line into variables
            name,topo_id,st_chain,end_chain,dir = parse_def_line(definitions)
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
                topo_id_list.append(topo_id)


def get_xsec(file):
    #--read the xsection information from a xsection export TXT file from MIKE11
    f = open(file,'r')    
    xsec_list = []
    
    this_id = f.readline().strip().split()[0]
    this_name = f.readline().strip().split()[0]    
    this_chain = float(f.readline().strip())
    this_entries = int(read_to(f,'PROFILE').strip().split()[-1])
    this_xz = []
    for e in range(this_entries):
        raw = f.readline().strip().split()
        this_x = float(raw[0])
        this_z = float(raw[1])
        this_xz.append([this_x,this_z])
    #--calculate xsec area        
    #--first find the top and bottom        
    top = -1.0e+20
    bot = 1.0e+20
    for pt in this_xz:
        if pt[1] > top:
            top = pt[1]
        if pt[1] < bot:
            bot = pt[1]
    #--now calc the area
    area = 0.0
    for i in range(1,len(this_xz)):
       
        width = (this_xz[i][0] - this_xz[i-1][0])
        bot = (this_xz[i][1] + this_xz[i-1][1])/2.0
        height = top - bot
        if height < 0.0: height = 0.0
        area += (width * height)
                            
    this_list = [this_name,this_id,this_chain,this_xz,top,bot,area]
    xsec_list.append(this_list)
    
    while True:
        line = read_to(f,'\*\*\*')          
        try:
            this_id = f.readline().strip()
        except: 
            break 
        if this_id == '':
            break                        
        this_name = f.readline().strip()        
        line = f.readline().strip() 
        #print this_id,this_name,line        
        this_chain = float(line)
        #try:
        line = read_to(f,'PROFILE',pos=0).strip().split()
        #print this_name,this_id,this_chain,line
        try:
            this_entries = int(line[-1])
        except:
            this_entries = 0
       # print this_name,this_id,this_chain,this_entries,line    
        this_xz = []
        this_list = []
        
        for e in range(this_entries):
            raw = f.readline().strip().split()
            this_x = float(raw[0])
            this_z = float(raw[1])
            this_xz.append([this_x,this_z])
        
        #--calculate xsec area        
        #--first find the top and bottom        
        top = -1.0e+20
        bot = 1.0e+20
        for pt in this_xz:
            if pt[1] > top:
                top = pt[1]
            if pt[1] < bot:
                bot = pt[1]
       #--now calc the area
        area = 0.0
        for i in range(1,len(this_xz)):
           
            width = (this_xz[i][0] - this_xz[i-1][0])
            bot = (this_xz[i][1] + this_xz[i-1][1])/2.0
            height = top - bot
            if height < 0.0: height = 0.0
            area += (width * height)
                                
        this_list = [this_name,this_id,this_chain,this_xz,top,bot,area]
        #print this_list[0],this_list[1],this_list[2]
        xsec_list.append(this_list)
        
        #except:
        #    #print line
        #    pass
    
    f.close()
    return xsec_list
        
        
def read_to(file,tag,pos=None):
    #--generic function to read to a match in a text file
    #--kwarg pos used to specify a specific location on line
    reg = re.compile(tag,re.IGNORECASE)
    while True:
        line = file.readline()
        if line == '':  
            return False
        if pos != None:
            raw = line.strip().split()
            try:
                if reg.search(raw[pos]) != None:
                    return line
            except:
                pass
        
        
        elif reg.search(line) != None:
            return line
                 

def parse_conn_line(line):
    #--parse the connection line of a MIKE11 nwk file
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
    #--parse the definition line of the MIKE11 nwk file
    raw = def_line.strip().split(',')
    name = raw[0].split('=')[-1].strip()[1:-1]
    topo_id = raw[1].strip()[1:-1]
    st_chain = float(raw[2])   
    end_chain = float(raw[3])   
    dir = False
    if int(raw[4]) == 0: dir = True
    return name,topo_id,st_chain,end_chain,dir


def parse_points(points,dir):
    #--parse the points section of the MIKE11 nwk file
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
    #--get the attributes of a point based in it's number
    for pt in point_attri:        
        if pt[0] == p: return pt[1],pt[2],pt[4]
    print 'bpoint not found in point_attri list: ',p
    raise IndexError


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



def get_structures(file):
    #--load the structure information from the MIKE11 nwk file
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
    print len(loc_line)
    return loc_line

def list_2_string(l,delimiter=' '):
    st = ''
    for i in l:  
        st = st + ' ' + str(i)
    return st


def point_compare(point1,point2):
    if point1[0] == point2[0] and point1[1] == point2[1]:
        return True
    else: return False

            
def interp_conn_point(frac_dist,point1,point2):
    #--find a connection point based in the fractional distance between the two points
    dist = distance(point1,point2)    
    delta_x = frac_dist * (point2[0] - point1[0])
    delta_y = frac_dist * (point2[1] - point1[1])
    #print 'delta_x,delta_y',delta_x,delta_y
    #print 'dist, frac_dist',dist,frac_dist
    return [point1[0] + delta_x,point1[1] + delta_y]    
    
                           
def distance(point1,point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

            
def get_nearest_2_point_indexes(chainage,branch_lengths):
    #--find the indexes of the two existing points bracketing the chainage value
    
    #print branch_lengths    
    #--try for an exact equality
    for i in range(1,len(branch_lengths)):        
        if chainage >= branch_lengths[i-1] and chainage <= branch_lengths[i]:
            #print 'chainage points',chainage,branch_lengths[i-1],branch_lengths[i]
            return [i-1,i]
    #--try with rounding error
    tol_dist = 0.1 #meters
    for i in range(1,len(branch_lengths)):        
        #print 'chainage points',chainage,branch_lengths[i-1],branch_lengths[i]
        if chainage >= branch_lengths[i-1]-tol_dist and chainage <= branch_lengths[i]+tol_dist:
            #print 'chainage points',chainage,branch_lengths[i-1],branch_lengths[i]
            return [i-1,i]
        
    return [None]
                

def get_branch_index_by_name(name,names):    
    #--find a branch by name
    
    for n in range(len(names)):
        #print names[n],name
        if names[n].upper() == name.upper():
            idx = n
            return idx 
    return None


def get_point(name,name_list,chainage,chainage_list,point_list):
    #--interpolates along a line segment to find the location of a new point
    #--based on chainage distance
    
    #--get the index of the connection branch
    branch_idx = get_branch_index_by_name(name,name_list) 
    if branch_idx != None:
        #print names[i],conn_chain[i][c],names[branch_idx]
        
        #--get the chainage index of the two nearest points in the connection branch
        #print chainage
        ch_idx = get_nearest_2_point_indexes(chainage,chainage_list[branch_idx])
        #print ch_idx
        if ch_idx[0] == None:
            print 'unable to find chainage points for point: ',name,chainage
            #raise IndexError 
            return None,None,None 
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
    else: return None,None,None
                       

def set_conn_points(names,st_chain,end_chain,bpoints,conn_name,conn_chain,branch_points,branch_lengths):
    #--set the connection points of the branches
    branch_points_conn = [] 
    branch_lengths_conn = []
    conn_point_list = []
    conn_name_list = []
    ch_idx_list = []
    #--for each branch
    for i in range(len(names)):
        branch_points_conn.append(copy.deepcopy(branch_points[i]))       
        branch_lengths_conn.append(copy.deepcopy(branch_lengths[i]))       
        #-- for each connection
        for c in range(len(conn_name[i])):            
            
            conn_point,branch_idx,ch_idx = get_point(conn_name[i][c],names,conn_chain[i][c],\
                                                     branch_lengths,branch_points)                                 
            if conn_point != None:
                start_dist = distance(conn_point,branch_points[i][0])
                end_dist = distance(conn_point,branch_points[i][-1])
                
                if start_dist < end_dist:
                    branch_points_conn[i].insert(0,conn_point)
                    branch_lengths_conn[i].insert(0,branch_lengths[i][0]-start_dist)
                else:
                    branch_points_conn[i].append(conn_point)
                    branch_lengths_conn[i].append(branch_lengths[i][-1]+end_dist)                
        #if names[i] == 'SBDD_SB8-7':break                                     
    return branch_points_conn,branch_lengths_conn


def set_conn_breaks(names,conn_name,conn_chain,branch_points,branch_lengths,chain_breaks):
    #--breaks the branches at the connection points
    
    branch_points_break = []
    branch_lengths_break = []
    for i in range(len(names)):
        branch_points_break.append(copy.deepcopy(branch_points[i]))
        branch_lengths_break.append(copy.deepcopy(branch_lengths[i]))
        
    for i in range(len(names)):
    
        #-- for each connection
        for c in range(len(conn_name[i])):
            
            conn_point,branch_idx,ch_idx = get_point(conn_name[i][c],names,conn_chain[i][c],\
                                                     branch_lengths_break,branch_points_break)            
            if branch_idx != None:                
                branch_points_break[branch_idx].insert(ch_idx[1],conn_point)
                branch_lengths_break[branch_idx].insert(ch_idx[1],conn_chain[i][c])
                chain_breaks[branch_idx].append(conn_chain[i][c])
        #        print names[i],conn_name[i],branch_lengths_break[branch_idx][ch_idx[1]],chain_breaks[branch_idx]
        #if names[i].upper() ==  '2_WCD2_C3MID':
        #    sys.exit() 
    return branch_points_break,branch_lengths_break,chain_breaks  
                

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
            print 'structure point not found:',str_cul_attri[i]   
    return str_cul_idx,str_cul_points




def set_str_breaks(names,str_cul_attri,branch_points,branch_lengths,chain_breaks):
    #--breaks the branches at structure locations
    
    branch_points_break = []
    branch_lengths_break = []
    
    for i in range(len(names)):
        branch_points_break.append(copy.deepcopy(branch_points[i]))
        branch_lengths_break.append(copy.deepcopy(branch_lengths[i]))
                        
    for i in range(len(str_cul_attri)):
        
        str_point,branch_idx,ch_idx = get_point(str_cul_attri[i][0],names,str_cul_attri[i][1],\
                                                branch_lengths_break,branch_points_break)        
        if branch_idx != None:
            #print 'new_point,branch_points',str_point,branch_points_break[branch_idx][ch_idx[0]],branch_points_break[branch_idx][ch_idx[1]]
            branch_points_break[branch_idx].insert(ch_idx[1],str_point)
            branch_lengths_break[branch_idx].insert(ch_idx[1],str_cul_attri[i][1])
            chain_breaks[branch_idx].append(str_cul_attri[i][1])
            #print branch_points_break[branch_idx][ch_idx[0]],branch_points_break[branch_idx][ch_idx[1]]
        
        #if str_cul_attri[i][2] == 'S-38A': break  
    return branch_points_break,branch_lengths_break,chain_breaks  



def set_xsec_breaks(names,xsec_attri,branch_points,branch_lengths,chain_breaks):
    #--break the branches at xsection locations
    
    
    branch_points_break = []
    branch_lengths_break = []
    #xsec_points = []
    for i in range(len(names)):
        branch_points_break.append(copy.deepcopy(branch_points[i]))
        branch_lengths_break.append(copy.deepcopy(branch_lengths[i]))
    
    for i in range(len(xsec_attri)):        
        #print xsec_attri[i]
        xsec_point,branch_idx,ch_idx = get_point(xsec_attri[i][0],names,xsec_attri[i][2],\
                                                branch_lengths_break,branch_points_break)      
                                                        
        #print xsec_attri[i][0],xsec_attri[i][1],xsec_attri[i][2],branch_idx
        #if xsec_attri[i][0] == '2_C1_SOUTH':
        #    sys.exit()
        if branch_idx != None:
            #print xsec_point
            #xsec_points.append(xsec_point)
            #print len(xsec_attri[i])
            xsec_attri[i].append(xsec_point)
            #print len(xsec_attri[i])
            
            branch_points_break[branch_idx].insert(ch_idx[1],xsec_point)
            branch_lengths_break[branch_idx].insert(ch_idx[1],xsec_attri[i][2])
            chain_breaks[branch_idx].append(xsec_attri[i][2])
    return branch_points_break,branch_lengths_break,chain_breaks


    
def set_xsec_breaks_dissolve(names,topo_id,xsec_attri,branch_points,branch_lengths,chain_breaks):
    #--break the branches at xsection locations                                 
    #--dissolves similar sections
    #---minimizes the number of xsection breaks
    
    #--first build a list of similar xsections
    #--all xsections start as unique
    unique_list = []
    for x in xsec_attri:
        unique_list.append(True)
    bot_idx = 5
    area_idx = 6
    area_tol,bot_tol = 2.5,0.25 #meters^2 and meters
    assert len(names) == len(topo_id)
    for n,t in zip(names,topo_id):
        #--get the indexes of all xsection attributes with this name
        xsec_idx = []        
        for i in range(len(xsec_attri)):
           if xsec_attri[i][0].upper() == n.upper() and \
              xsec_attri[i][1].upper() == t.upper():              
               xsec_idx.append(i)
        #--now compare all of the xsections associated with the branch
        for i in xsec_idx:
            for ii in xsec_idx:
                if i != ii:
                    #--calc bot elev diff and area diff
                    #print len(xsec_match[i] )
                    #print len(xsec_match[ii])
                    bot_diff = abs(xsec_attri[i][bot_idx] - xsec_attri[ii][bot_idx])
                    area_diff = abs(xsec_attri[i][area_idx] - xsec_attri[ii][area_idx])
                    if bot_diff < bot_tol and area_diff < area_tol:
                        #--some xsec names may get appended more than once - shouldn't matter                        
                        unique_list[ii] = False
                        
                        
    #--make a deep copy of the primary lists    
    branch_points_break = []
    branch_lengths_break = []
    
    for i in range(len(names)):
        branch_points_break.append(copy.deepcopy(branch_points[i]))
        branch_lengths_break.append(copy.deepcopy(branch_lengths[i]))
    
    for i in range(len(xsec_attri)):        
        #print xsec_attri[i]
        xsec_point,branch_idx,ch_idx = get_point(xsec_attri[i][0],names,xsec_attri[i][2],\
                                                branch_lengths_break,branch_points_break)      
                                                        
        #print xsec_attri[i][0],xsec_attri[i][1],xsec_attri[i][2],branch_idx
        #if xsec_attri[i][0] == '2_C1_SOUTH':
        #    sys.exit()
        if branch_idx != None:
            #print xsec_point
            #xsec_points.append(xsec_point)
            #print len(xsec_attri[i])
            xsec_attri[i].append(xsec_point)
            #print len(xsec_attri[i])
            #print unique_list[i],xsec_attri[i]
            
            if unique_list[i] == True:
                branch_points_break[branch_idx].insert(ch_idx[1],xsec_point)
                branch_lengths_break[branch_idx].insert(ch_idx[1],xsec_attri[i][2])
                chain_breaks[branch_idx].append(xsec_attri[i][2])
    return branch_points_break,branch_lengths_break,chain_breaks




def get_break_idx(branch_lengths,chain_breaks,tol=1.0):
    #--find the indexes of the branch segment to insert a new points and breaks
    
    idx = [0]
    chain_breaks.sort()
    for c in chain_breaks:
        #print c
        branch_length_idx = branch_lengths.index(c)
        if check_tolerance(c,branch_lengths,idx,tol):
            idx.append(branch_lengths.index(c))
    if check_tolerance(branch_lengths[-1],branch_lengths,idx,tol):
        idx.append(len(branch_lengths)-1)
    else: 
        idx.pop(-1)
        idx.append(len(branch_lengths)-1)
    idx.sort()
    return idx
        

def check_tolerance(chain,chainage,ch_idx,tolerance):
    #--check the closenss of chainage points
    #--looking for duplicates
    for cidx in ch_idx:
        if abs(chainage[cidx]-chain) < tolerance:
            return False
    return True    


#def get_bbox(branch_point):
#    xmin,ymin = 1.0e20,1.0e20
#    xmax,ymax = -1.0e20,-1.0e20
#    for bpoints in branch_points:
#        for p in bpoints:
#            print p[0]
#            if p[0] < xmin : xmin = p[0]
#            if p[0] > xmax : xmax = p[0]
#            if p[1] < ymin : ymin = p[1]
#            if p[1] > ymax : ymax = p[1]
#    return [xmin,ymin,xmax,ymax]


#def get_profile_by_name_topo_id(name,topo_id,chainage,xsec_attri):
#    #--find the matching profiles with the name, topo_id and chainage
#    for x in xsec_attri:
#        #if x[0] == '2_WCD2_IndBay':
#        #    print x[0],x[1]        
#        #    break
#        #print x[0],x[1],x[2],name,topo_id,chainage
#        dist = abs(abs(x[2]) - abs(chainage))
#        #print name,topo_id,x[0],x[1],dist
#        if x[0].upper() == name.upper() and \
#           x[1].upper() == topo_id.upper() and \
#           dist < 1.0:
#               return x[-1]
                      
    print 'profile not found for name/topo/chainage: ',name,topo_id,chainage
    #raise IndexError

def get_profiles(name,topo_id,break_idx,branch_lengths,xsec_attri,loc):
    #--find the profiles closest to each of the branch segements defined
    #--by the break_idx list
    #--loc used to define starting or ending closeness
    
    #--first find all of the xsections with the name and topo_id
    xsec_match = []
    for x in xsec_attri:
        if x[0].upper() == name.upper() and \
           x[1].upper() == topo_id.upper() and \
           len(x) == 8 :  #len == 8 means it has an X,Y location
            xsec_match.append(x)
    
    #--for each branch marked by break_idx, find the xsection closest either
    #-- the end or the beginning
    xsec = []
    xsec_names = []
    for b in range(1,len(break_idx)):
        if loc.upper() == 'START':
            idx = break_idx[b-1]
        elif loc.upper() == 'END':
            idx = break_idx[b]
        else:
            print 'unrecongnized location:',loc,' should be start and end'
            raise ValueError
        #cent_chain = (branch_lengths[start_idx] + branch_lengths[end_idx])/2.0
        #print branch_lengths[start_idx],branch_lengths[end_idx],cent_chain
        min_p,min_dist = None,1.0e+20
        for x in xsec_match:
            #print x[2]
            dist = abs(x[2] - branch_lengths[idx])
            if dist < min_dist:
                min_dist = dist
                min_p = x
        #print min_p[:2]
        xsec.append(min_p)
        xsec_names.append(build_profile_name(min_p[0],min_p[1],min_p[2]))
    
    return xsec,xsec_names
                     
def write_profiles(xsec_dir,profiles,names):
    #--write a group of profiles
    #--convert to ft and correct for navd
    for p,n in zip(profiles,names):
        files = os.listdir(xsec_dir)
        if n not in files:
            prof = p[3]            
            profile_m_2_ft(prof)
            profile_ngvd_2_navd(prof)
            write_swr_profile(xsec_dir+n,prof,p[7],p[6])
            
    



def write_swr_profile(profile_name,profile,xy,area):
    #--write the xsec profile to the SWR format - 
    #--add the num_pts,X,Y,and area to the header
    if len(profile) < 1:
        print 'Error = zero length xsection:',profile_name
        raise ValueError
    f = open(profile_name,'w')
    f.write('#       XB      ELEVB {0:10.0f} {1:15.6e} {2:15.6e} {3:15.6e}\n' \
            .format(len(profile),xy[0],xy[1],area*3.281*3.281))
    for entry in profile:
        f.write('{0:10.3f} {1:10.3f}\n'.format(entry[0],entry[1]))
    f.close()
    return

def profile_ngvd_2_navd(profile,ngvd2navd=-1.5):
    #--convert
    for p in range(len(profile)):
        profile[p][1] += ngvd2navd

def profile_min(profile):
    #--find the minimum elev
    min = 1.0e+20
    for p in profile:
        if p[1] < min:
            min = p[1]
    return min

def profile_m_2_ft(this_profile):
    #--convert
    for pt_idx in range(len(this_profile)):
        this_profile[pt_idx][0] *= 3.281
        this_profile[pt_idx][1] *= 3.281
    return this_profile



def build_profile_name(name,topo_id,chainage): 
    #--make the profile name compatible with MODFLOW   
    prof_name = re.sub('/','_',name+'_'+topo_id+'_'+str(int(chainage))) 
    prof_name = re.sub('\?','_',prof_name)    
    prof_name = re.sub('\s','_',prof_name)    
    prof_name = re.sub('\.','_',prof_name)  
    prof_name += '.dat'  
    return prof_name


    