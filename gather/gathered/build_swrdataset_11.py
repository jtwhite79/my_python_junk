


cntstr_type = [3,8,9]

reaches = []
r_count = []

#--first build a list of the istrrch's and the number of reaches at each one
file = 'swr_structure_all.dat'
f = open(file,'r')
h1 = f.readline()
h2 = f.readline()
while True:
    line = f.readline()
    raw = line.strip().split()
    istrrch = int(raw[0])
    istrtype = int(raw[3])
    
    if istrrch in reaches:
        idx = reaches.index(istrrch)
        r_count[idx] += 1
    else:
        reaches.append(istrrch)
        r_count.append(1)
        
    if istrtype in cntstr_type:
        f.readline()
    