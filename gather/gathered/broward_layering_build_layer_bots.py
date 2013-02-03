import numpy as np
from scipy import ndimage
import pylab
import shapefile
'''hangs layers off of a heaily smoothed top
combines H and Q5
generates a lightly smoothed top for the model input
'''





#--top max and mins
tmax,tmin = 20,-2.0

#-- minimum thick of layer 1
l1_min = 5.0

ref_dir = 'ref\\bro_'
out_dir = 'ref_new\\'
top = np.loadtxt(ref_dir+'top.ref')

#ibound = np.loadtxt(ref_dir+'ibound_CS.ref')

model_layers = ['H.ref','Q5.ref','Q4.ref','Q3.ref','Q2.ref','Q1.ref','T3.ref','T2.ref','T1.ref']
top[np.where(top>tmax)] = tmax
top[np.where(top<tmin)] = tmin
#top = np.ma.masked_where(ibound==0,top)

mask = np.zeros_like(top)
mask[np.where(np.logical_or(top>tmax,top<tmin))] = 1

#-- a lightly smoothed top for model top
#sigma = 1
#top_sml = ndimage.gaussian_filter(top,sigma=sigma)
#top_sml = np.ma.masked_where(ibound==0,top_sml)
#top_sml[np.where(top_sml>tmax)] = tmax
#top_sml[np.where(top_sml<tmin)] = tmin
#np.savetxt(out_dir+'top_sml.ref',top_sml,fmt=' %15.6G')

#p = pylab.imshow(top_sml)
#pylab.colorbar(p)
#pylab.show()

#--smooth the top heavily and hang layers off of it
sigma = 15
top_sm = ndimage.gaussian_filter(top,sigma=sigma)
#top_sm = np.ma.masked_where(ibound==0,top_sm)
top_sm[np.where(top_sm>tmax)] = tmax
top_sm[np.where(top_sm<tmin)] = tmin
np.savetxt(out_dir+'top_layering.ref',top_sm,fmt=' %15.6G')

#--combine H and Q5 and Q4
l1_thk = np.loadtxt(ref_dir+model_layers[0]) + np.loadtxt(ref_dir+model_layers[1]) + np.loadtxt(ref_dir+model_layers[2])
l1_bot = top_sm - l1_thk
#--raw thickness using unfiltered top
l1_thk_raw = top - l1_bot
#l1_thk[np.where(l1_thk_raw<l1_min)] += (l1_min - l1_thk_raw[np.where(l1_thk_raw<l1_min)])
#--where the raw thickness is less than l1_min, raise the top to meet l1_min
top[np.where(l1_thk_raw<l1_min)] += (l1_min - l1_thk_raw[np.where(l1_thk_raw<l1_min)])

l1_bot = top_sm - l1_thk

np.savetxt(out_dir+'Q4_bot.ref',l1_bot,fmt=' %15.6E')
np.savetxt(out_dir+'top_mod.ref',top,fmt=' %15.6E')
#--plot layer 1 thk against top
l1_thk_sml = top - l1_bot
#print l1_thk_sml.min()
#p = pylab.imshow(l1_thk_sml)
#p = pylab.imshow(l1_bot)
#pylab.colorbar(p)
#pylab.show()

#--split production layers (Q2 and Q1) into more layers each
split = 4
ibound = np.loadtxt('..\\_model\\bro.03\\flowref\\ibound_CS.ref')
q2 = np.loadtxt(ref_dir+model_layers[4])
q2_frac = q2 / float(split)
q1 = np.loadtxt(ref_dir+model_layers[5])
q1_frac = q1 / float(split)
#q1_frac = np.ma.masked_where(ibound==0,q2_frac)
print q2.min(),q2_frac.min()
print q1.min(),q1_frac.min()
#p = pylab.imshow(q2_frac)
#p = pylab.imshow(q2_4)
#pylab.colorbar(p)
#pylab.show()




prev_bot = l1_bot
for ml in model_layers[3:]:
    if 'q1' in ml.lower():
        for s in range(split):
            lay_bot = prev_bot - q1_frac
            np.savetxt(out_dir+'Q1_'+str(s+1)+'_bot.ref',lay_bot,fmt=' %15.6E')
            prev_bot = lay_bot
    elif 'q2' in ml.lower():
        for s in range(split):
            lay_bot = prev_bot - q2_frac
            np.savetxt(out_dir+'Q2_'+str(s+1)+'_bot.ref',lay_bot,fmt=' %15.6E')
            prev_bot = lay_bot
    else:
        lay_thk = np.loadtxt(ref_dir+ml)
        lay_bot = prev_bot - lay_thk
        np.savetxt(out_dir+ml.split('.')[0]+'_bot.ref',lay_bot,fmt=' %15.6E')
        prev_bot = lay_bot






#vmax,vmin = top.max(),top.min()
#ax = pylab.subplot(211)
#ax2 = pylab.subplot(212)
#p = ax.imshow(top)
#ax2.imshow(top_sm,vmax=vmax,vmin=vmin)
#pylab.colorbar(p)
#pylab.show()

