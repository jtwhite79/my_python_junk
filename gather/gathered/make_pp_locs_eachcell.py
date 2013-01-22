import numpy as np

nrow,ncol = 10,60
delta = 0.2
offset = [0.0,0.0]
f_out = open('pp_locs.dat','w')
for i in range(nrow):
    for j in range(ncol):
        n = 'kr'+str(i+1).zfill(2)+'c'+str(j+1).zfill(2)              
        x = offset[0] + ((j+1)*delta) - (delta/2.0)
        y = offset[1] - ((i+1)*delta) + (delta/2.0)
        #print n,x,y
        #break
        f_out.write(n.ljust(10)+'  {0:10.3g}   {1:10.3g}   1    1.0\n'.format(x,y))
f_out.close()  
    
