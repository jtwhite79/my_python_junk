

f = open('swr_ds13a.dat','r')
f_out = open('swr_ds13a_w.dat','w')

for line in f:
    if 'STAGE' not in line:
        f_out.write(line)
f.close()
f_out.close()        