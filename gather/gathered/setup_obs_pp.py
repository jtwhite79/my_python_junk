import numpy as np
import pylab
import kl_config as kl

nrow,ncol = kl.nrow,kl.ncol
delr,delc = kl.delr,kl.delc

#--setup evenly spaced pp
num_pp = 100

stride = int(np.ceil(np.sqrt(num_pp)))
pp_names,pp_locs = [],[]
pp_count = 1
for i in range(int(stride/2.0),nrow,stride):
    for j in range(int(stride/2.0),ncol,stride):
        pp_name = 'pp_'+(str(pp_count)).zfill(3)
        pp_names.append(pp_name)
        pp_locs.append([delr*j,delc*i])
        pp_count += 1
f_out = open('pp_locs.dat','w')
for n,l in zip(pp_names,pp_locs):
    f_out.write(n.ljust(15)+' {0:6.3f} {1:6.3f} 1  1.0\n'.format(l[0],l[1]))
f_out.close()

#--setup observation locations - random
num_obs = stride

xmin,xmax = 0,delr*ncol
ymin,ymax = 0,delc*nrow

x_rand = xmin + np.random.random(num_obs) * (xmax-xmin)
y_rand = ymin + np.random.random(num_obs) * (ymax-ymin)
f_out = open('bore_coords_new.dat','w')
obs_count = 1
for x,y in zip(x_rand,y_rand):
    o_name = 'obs_'+str(obs_count).zfill(3)
    f_out.write(o_name+' {0:15.6e} {0:15.6e}  1\n'.format(x,y))
f_out.close()    
    

pp_locs = np.array(pp_locs)

fig = pylab.figure()
ax = pylab.subplot(111)
ax.plot(x_rand,y_rand,'bo')
ax.plot(pp_locs[:,0],pp_locs[:,1],'k.')
pylab.show()
    


