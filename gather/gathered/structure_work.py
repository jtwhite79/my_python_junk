import re
import sys
import math
import shapefile
import mikeshe_struct as ms

def distance(point1,point2):                                                        
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)       

def find_index_2_nearest_reaches(s_point,reaches):
    
    up_idx,dw_idx = -1,-1
    #--find upstream reach - nearest last vertex
    up_idx = -1
    min = 1.0e+20
    for r in range(len(reaches)):
        last_point = reaches[r].points[-1]
        dist = distance(s_point,last_point)
        if dist < min:
            up_idx = r
            min = dist
    #--find downstream reach - nearest first vertex
    min = 1.0e+20
    dw_idx = -1
    for r in range(len(reaches)):
        first_point = reaches[r].points[0]
        dist = distance(s_point,first_point)
        if dist < min and r != up_idx:
            dw_idx = r
            min = dist

    return up_idx,dw_idx


def get_shape_index(name,chainage,num_shapes,shp_reader):
    chain_len = []
    chain_idx = []
    for n in range(num_shapes):
        this_rec = shp_reader.record(n)
        #print this_rec[0],name
        if this_rec[0].upper() == name.upper():
            #print name,float(this_rec[2]),chainage
            
            if float(this_rec[2]) == chainage:
                return True,0.0,n
            else:
                chain_len.append(float(this_rec[2]))
                chain_idx.append(n)
    
    #--if no exact match is found            
    min = 1.0e+20
    shortest = -1.0e+20
    for c in range(len(chain_len)):
        if abs(chain_len[c] - chainage) < min:
            shortest = chain_idx[c]
            min = abs(chain_len[c] - chainage)  
    return False,min,shortest
        
    
def get_swr_istrdir(flow_string):
    
    if flow_string == 'pos': istrdir = 1
    elif flow_string == 'neg': istrdir = -1
    elif flow_string == 'both': istrdir = 0
    else: istrdir =  None
    return istrdir
                    
                              

def build_swr_struct_string(swr_dict):
    ifmt = '{0:8.0f}'
    ffmt = '{0:8.3e}'
    
    str = ''
    
    try: str += ifmt.format(swr_dict['istrrch']).rjust(12)+' '
    except: str += '             '
    try: str += ifmt.format(swr_dict['istrnum']).rjust(12)+' '
    except: str += '             '
    try: str += ifmt.format(swr_dict['istrconn']).rjust(12)+' '
    except: str += '             '
    try: str += ifmt.format(swr_dict['istrtype']).rjust(12)+' '
    except: str += '             '
    try: str += ffmt.format(swr_dict['nstrpts']).rjust(12)+' '
    except: str += '             '
    try: str += ffmt.format(swr_dict['strwcd']).rjust(12)+' '
    except: str += '             '
    try: str += ffmt.format(swr_dict['strwcd2']).rjust(12)+' '
    except: str += '             '
    try: str += ffmt.format(swr_dict['strinv']).rjust(12)+' '
    except: str += '             '
    try: str += ffmt.format(swr_dict['strinv2']).rjust(12)+' '
    except: str += '             '
    try: str += ffmt.format(swr_dict['strwid']).rjust(12)+' '
    except: str += '             '
    try: str += ffmt.format(swr_dict['strwid2']).rjust(12)+' '
    except: str += '             '
    try: str += ffmt.format(swr_dict['strlen']).rjust(12)+' '
    except: str += '             '
    try: str += ffmt.format(swr_dict['strmann']).rjust(12)+' '
    except: str += '             '
    try: str += ifmt.format(swr_dict['istrdir']).rjust(12)+' '
    except: str += '             '
    try: str += ffmt.format(swr_dict['strqmax']).rjust(12)+' '
    except: str += '             '
    try: str += ffmt.format(swr_dict['strcrit']).rjust(12)+' '
    except: str += '             '
    try: str += ffmt.format(swr_dict['istropr']).rjust(12)+' '
    except: str += '             '
    try: str += ffmt.format(swr_dict['strgort']).rjust(12)+' '
    except: str += '             '
    try: str += ffmt.format(swr_dict['strmaxgo']).rjust(12)+' '
    except: str += '             '
    try: str += ffmt.format(swr_dict['strgo'].rjust(12))+' '
    except: str += '             '
    str += '\n'
    return str


#def reduce_strategy_discharge(self,strategy):
#       max_target = -1.0e+20
#       min_control = 1.0e+20
#       #--find the max target value
#       for s in strategy:
#           if abs(s[1]) > max_target: max_target = s[1]
#       
#       #--find the control point by linear interpolation
#       if max < 0.0:
#           for s in range(1,len(strategy)):
#               if strategy[s][1] =< 0 and strategy[s-1][1] == :
#                   control = interp_strategy(strategy[s-1],strategy[s])
#                   break
#           
#           
#       if max >= 0.0:
#           for s in range(1,len(strategy)):
#               if strategy[s][1] > 0.0 and strategy[s-1][1] <= 0.0:
#                   control = interp_strategy(strategy[s-1],strategy[s])
#                   break
#       





file = '..\\MIKE_SHE_Baseline\\Broward_Base_05.nwk11'

culvert_list = ms.load_culverts(file)
weir_list = ms.load_weirs(file)
struct_list = ms.load_structure(file)

struct_file = 'she_structures_culverts_1'   
struct_shp = shapefile.Reader(shapefile=struct_file)
structs = struct_shp.shapes()

reach_file = 'polylines'
reach_shp = shapefile.Reader(shapefile=reach_file)
reaches = reach_shp.shapes()   


stor = re.compile('storage',re.IGNORECASE)

#--initialize a counter for tracking the 
#--number of structures at each reach
reach_str_count = []
reach_str_name = []
for s in range(len(reaches)):
    reach_str_count.append(0)
    reach_str_name.append([])


swr_dict = {'istrrch':'','istrnum':'','istrconn':'','istrtype':'',\
            'nstrpts':'','strwcd':'','strwcd2':'','strinv':'',\
            'strinv2':'','strwid':'','strwid2':'','strlen':'',\
            'strmann':'','istrdir':'','strqmax':'','strcrit':'',\
            'istropr':'','strgort':'','strmaxgo':'','strgo':''}


#--control structures
swr_struct = []
for s in range(len(struct_list)):
    #--filter out 'storage' related structures
    if stor.search(struct_list[s].name) == None and \
       stor.search(struct_list[s].id) == None:
               
        found,dist,shape_index = get_shape_index(struct_list[s].name,struct_list[s].chainage,\
                                      len(structs),struct_shp)  
        if dist != 0.0:
            print 'structure not found in shapefile records: '+struct_list[s].id
            print shape_index,len(structs)

            sys.exit()
                
        up_idx,dw_idx = find_index_2_nearest_reaches(structs[shape_index].points[0],reaches) 
        if struct_list[s].type == 'Discharge':
            print struct_list[s].id,struct_list[s].control_strategy
            istr_type = 3 #swr pump
            #if struct_list[s].num == 1: reach_str_name[up_idx].append(struct_list[s].id)   
            #else: reach_str_name[up_idx].append(stuct_list[s].id+'*'+str(struct_list[s].num))   
            #for n in range(struct_list[s].num): 
            #    this_dict = swr_dict.copy()
            #    reach_str_count[up_idx] += 1 
            #    this_dict['istrrch'] = reach_shp.record(up_idx)[3]
            #    this_dict['istrnum'] = reach_str_count[up_idx]
            #    this_dict['istrconn'] = reach_shp.record(dw_idx)[3]
            #    this_dict['istrtype'] = istr_type
            #    this_dict[strqmax']
            #    temp = build_swr_struct_string(this_dict)
            #    swr_weir.append(temp)
            
        #elif struct_list[s].type == 'Underflow':
        #elif struct_list[s].type == 'Overflow':
        
        
        


sys.exit()

#--weirs
swr_weir = []
istr_type = 6 #swr weir
coeff = 0.61
for w in range(len(weir_list)):    
    #--filter out 'storage' related structures
    if stor.search(weir_list[w].name) == None and \
       stor.search(weir_list[w].id) == None:
               
        found,dist,shape_index = get_shape_index(weir_list[w].name,weir_list[w].chainage,\
                                      len(structs),struct_shp)  
        if dist != 0.0:
            print 'structure not found in shapefile records: '+weir_list[w].id
            print shape_index,len(structs)
            print '  distance to nearest point: ',dist
            print '  structure chainage,nearest chainage: ',\
                  weir_list[w].chainage,struct_shp.record(shape_index)[-1]  
            raise ValueError
        
        up_idx,dw_idx = find_index_2_nearest_reaches(structs[shape_index].points[0],reaches) 
        
        this_dir = get_swr_istrdir(weir_list[w].dir)
        up_rch = reach_shp.record(up_idx)[3]
        dw_rch = reach_shp.record(dw_idx)[3]
        
        
        if this_dir == None:
            #print 'null structure found in weirs: ',weir_list[w].id
            swr_null.append([up_rch,dw_rch,weir_list[w].id])
        else: 
            
            if weir_list[w].num == 1: reach_str_name[up_idx].append(weir_list[w].id)   
            else: reach_str_name[up_idx].append(weir_list[w].id+'*'+str(weir_list[w].num))   
            for n in range(weir_list[w].num): 
                this_dict = swr_dict.copy()
                reach_str_count[up_idx] += 1 
                this_dict['istrrch'] = reach_shp.record(up_idx)[3]
                this_dict['istrnum'] = reach_str_count[up_idx]
                this_dict['istrconn'] = reach_shp.record(dw_idx)[3]
                this_dict['istrtype'] = istr_type
                this_dict['strwcd'] = coeff
                this_dict['strinv'] = weir_list[w].invert * 3.281 
                this_dict['strwid'] = weir_list[w].width * 3.281 
                this_dict['istrdir'] = this_dir
                temp = build_swr_struct_string(this_dict)
                swr_weir.append(temp)

        
#--culverts 
swr_culvert = []
coeff = 0.61
coeff2 = 0.61
istr_type =  5 #swr culvert 
for c in range(len(culvert_list)):
    #--filter out 'storage' related structures
    if stor.search(culvert_list[c].name) == None and \
       stor.search(culvert_list[c].id) == None:
               
        found,dist,shape_index = get_shape_index(culvert_list[c].name,culvert_list[c].chainage,\
                                      len(structs),struct_shp)  
        if dist != 0.0:
            print 'structure not found in shapefile records: '+culvert_list[c].id
            print shape_index,len(structs)
            print '  distance to nearest point: ',dist
            print '  structure chainage,nearest chainage: ',\
                  culvert_list[c].chainage,struct_shp.record(shape_index)[-1]  
            raise ValueError
                
        up_idx,dw_idx = find_index_2_nearest_reaches(structs[shape_index].points[0],reaches) 
        
        #--determine circular or rectangular
        if culvert_list[c].type == 1:
            strwid = culvert_list[c].diameter * 3.281 
            strwid2 = ''
        elif culvert_list[c].type == 0:
            strwid = culvert_list[c].width * -1.0 * 3.281 
            strwid2 = culvert_list[c].height * 3.281 
        
        this_dir = get_swr_istrdir(culvert_list[c].dir)
        up_rch = reach_shp.record(up_idx)[3]
        dw_rch = reach_shp.record(dw_idx)[3]
         
        #print culvert_list[c].id,culvert_list[c].type,culvert_list[c].diameter,culvert_list[c].width, culvert_list[c].height       
    
        if culvert_list[c].num == 1: reach_str_name[up_idx].append(culvert_list[c].id)   
        else: reach_str_name[up_idx].append(culvert_list[c].id+'*'+str(culvert_list[c].num))   
        for n in range(culvert_list[c].num): 
            this_dict = swr_dict.copy()
            reach_str_count[up_idx] += 1
            this_dict['istrrch'] = reach_shp.record(up_idx)[3]
            this_dict['istrnum'] = reach_str_count[up_idx]
            this_dict['istrconn'] = reach_shp.record(dw_idx)[3]
            this_dict['istrtype'] = istr_type
            this_dict['strwcd'] = coeff 
            this_dict['strwcd2'] = coeff2
            this_dict['strinv'] = culvert_list[c].upstr * 3.281 
            this_dict['strinv2'] = culvert_list[c].dwstr * 3.281 
            this_dict['strwid'] = strwid
            this_dict['strwid2'] = strwid2
            this_dict['strlen'] = culvert_list[c].length * 3.281 
            this_dict['istrdir'] = this_dir
            this_dict['strmann'] = culvert_list[c].mannings
            temp = build_swr_struct_string(this_dict)
            swr_culvert.append(temp)


f = open('swr_struct_data.dat','w')                             
f.writre('#ISTRMOD NTRUCT\n')
for r in range(len(reach_str_count)):
    if reach_str_count[r] > 0:
        f.write(str(r+1).ljust(8)+' '+str(reach_str_count[r]).ljust(8)+' #')
        for rr in reach_str_name[r]:
            f.write(rr+' ')
        f.write('\n')


f.write('#    ISTRRCH      ISTRNUM     ISTRCONN     ISTRTYPE      NSTRPTS       STRWCD      STRWCD2       '+\
        'STRINV      STRINV2       STRWID      STRWID2       STRLEN      STRMANN      ISTRDIR      '+\
        'STRQMAX      STRCRIT      ISTROPR      STRGORT     STRMAXGO        STRGO')



#for weir in swr_weir:
#    f.write(weir)
#for culvert in swr_culvert:
#    f.write(culvert)

f.close()
