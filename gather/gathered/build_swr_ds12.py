


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
    if line == '':
        break
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

f.close()

#--write dataset 12
####DON"T USE - must build after ds13a is written
#f_11 = open('swr_ds12.dat','w')
#for r,c in zip(reaches,r_count):
#    f_11.write(' {0:10.0f} {1:10.0f}\n'.format(r,c))
#f_11.close()    

#--now rewrite istrnum and also write dataset 11
f = open(file,'r')
f_13 = open('swr_ds13.dat','w')

h1 = f.readline()
h2 = f.readline()
f_13.write(h1)
f_13.write(h2)

while True:
    line = f.readline()
    if line == '':
        break
    raw = line.strip().split()    
    istrrch = int(raw[0])
    istrtype = int(raw[3])
    idx = reaches.index(istrrch)
    istrnum_list = list('{0:10.0f}'.format(r_count[idx]))
    line_list = list(line)
    line_list[11:23] = istrnum_list
    line = str(line_list)
    f_13.write(''.join(line_list))
    r_count[idx] -= 1
    if r_count[idx] < 0:
        raise IndexError, 'something is wrong'+str(istrrch)

    if istrtype in cntstr_type:
        f_13.write(f.readline())
    

    