f = open('test.dat','r')
c1 = 0
c2 = 0
for line in f:
    raw = line.strip().split()
    if raw[3].upper() == 'M':
        c1 += 1
    elif raw[3].upper() == 'N':
        c2 += 1        
print c1,c2,c1+c2        