import os

new_dir = 'xsec\\'
old_dir = 'xsec_bak\\'

new_files = os.listdir(new_dir)
old_files = os.listdir(old_dir)

for of in old_files:
    if of not in new_files:
        print 'org xsec not in new dir:',of
        raise IndexError
    #--compare the two xsec
    old_xsec = [[],[]]
    new_xsec = [[],[]]
    fo = open(old_dir+of,'r')
    fn = open(new_dir+of,'r')
    fo.readline()
    fn.readline()
    for line in fo:
        raw = line.strip().split()
        old_xsec[0].append(float(raw[0]))
        old_xsec[1].append(float(raw[1]))
    for line in fn:
        raw = line.strip().split()      
        new_xsec[0].append(float(raw[0]))
        new_xsec[1].append(float(raw[1]))
    fo.close()
    fn.close()
    same = True
    if len(old_xsec[0]) != len(new_xsec[0]):
        same = False
    else:
        for xo,xn in zip(old_xsec[0],new_xsec[0]):
            if xo != xn:
                same = False
                break
        for zo,zn in zip(old_xsec[1],new_xsec[1]):   
            if zo != zn:                               
                same = False                      
                break                           
    if same == False:
        print 'difference:',of                 