f = open('ts_listing.csv','r')
f_out = open('temp.dat','w')
for line in f:
    f_out.write(line.replace('"',''))
f.close()
f_out.close()    