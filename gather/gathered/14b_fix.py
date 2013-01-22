f = open('14b.dat','r')
f_out = open('14b_scale.dat','w')

for line in f:
    raw = line.strip().split()
    raw[3]  = str(float(raw[3]) * 2.0)
    for r in raw: f_out.write(r.ljust(10))
    f_out.write('\n')