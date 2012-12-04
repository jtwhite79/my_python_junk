import re
import mikeshe_struct as mss

file = 'Broward_Base_05.nwk11'

structs = mss.load_structure(file)
weirs = mss.load_weirs(file)
culverts = mss.load_culverts(file)

f = open('swr_struct_test.dat','w')
mss.write_swr_dataset13_header(f)
istrrch = 1
istrnum = 1
istrconn =2
istrorch = 3
istroqcon = 4


for s in structs:
    #print s.id,s.branch,s.type       
    s.write_swr_entry(f,istrnum,istrrch,istrconn,istrorch,istroqcon=istroqcon)
    #if s.logical_operand[0][0] == 'Hups' or \
    #     s.logical_operand[0][0] == 'h' or \
    #     s.logical_operand[0][0] == 'Hdws' or \
    #     s.logical_operand[0][0] == 'Q_structure':
    #    print '--  ',s.logical_operand[0][0],s.logical_operand[0][1],s.logical_operand[0][2],s.target_type[0]
    #    if s.itype != 2:
    #        print '-+- ',s.sill,s.width
    #else:
    #    print 'No easy solution!',s.control_type[0],s.target_type[0],s.logical_operand[0]
    #    for cs in s.control_strategy[0]:
    #        print cs
    ##print '  ',s.control_values[0],s.logical_operand[0]
print len(structs)    

#f = open('swr_struct_test.dat','w')
#mss.write_swr_dataset13a_header(f)
#istrrch = 1
#istrnum = 1
#istrconn =2
#
#stor = re.compile('storage',re.IGNORECASE)
#brig = re.compile('bridge',re.IGNORECASE)
#
#for weir in weirs:
#    if stor.search(weir.id) == None and \
#       brig.search(weir.id) == None :
#        weir.write_swr_entry(f,istrnum,istrrch,istrconn)
#
#for culvert in culverts:
#    culvert.write_swr_entry(f,istrnum,istrrch,istrconn,m2ft=True)
#
#