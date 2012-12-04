import numpy as np
import pylab
import shapefile
import MFBinaryClass as mfb
from bro import seawat,flow


def in_layers(z_elev,botm):
    in_lay = np.zeros_like(botm)
    l_idx = 0
    for t,b in zip(botm[:-1],botm[1:]):
        if z_elev >= t:
            in_lay[l_idx] = 1.0
        elif z_elev <= b:
            in_lay[l_idx] = 0.0
        else:
            in_lay[l_idx] = 0.5
        l_idx += 1
    return in_lay


#--read the zeta file
extract_sp = 48
zeta_file = flow.root+'.zta'
zetaObj = mfb.MODFLOW_CBB(flow.nlay,flow.nrow,flow.ncol,zeta_file)
zta_text = '    ZETAPLANE  1'
z1times = zetaObj.get_time_list(zta_text)
zta_seekpoint =  long(z1times[extract_sp,3]) 
z,totim,success = zetaObj.get_array(zta_seekpoint)               
z1 = z[0,:,:]  


#--build 3-d vertical geometry array
botm = np.zeros((seawat.nlay+1,seawat.nrow,seawat.ncol))
botm[0,:,:] = seawat.top
for i,l in enumerate(seawat.layer_botm_names):
    b = np.loadtxt(seawat.ref_dir+l+'_bot.ref')
    botm[i+1,:,:] = b


#--load the ibound to limit calcs
ibound = np.loadtxt(flow.ref_dir+'ibound_CS.ref')

#--load the icbund
icbund = np.loadtxt(seawat.ref_dir+'icbnd.ref')


init_conc = np.zeros_like(botm)
#--process each active cell
for i in range(flow.nrow):
    for j in range(flow.ncol):
        if ibound[i,j] != 0:    
            b = botm[:,i,j]
            z_elev = z1[i,j]
            ic = in_layers(z_elev,b)
            init_conc[:,i,j] = ic

for k,lname in enumerate(seawat.layer_botm_names):
    aname = seawat.ref_dir+lname+'_srconc.ref'
    np.savetxt(aname,init_conc[k,:,:],fmt='%13.5E')


#--plot 
imshow_extent = [flow.x[0],flow.x[-1],flow.y[0],flow.y[-1]]
line_shapename = '..\\..\\_gis\shapes\sw_reaches'
lines = shapefile.load_shape_list(line_shapename)
for k in range(seawat.nlay):
    fig = pylab.figure()
    ax = pylab.subplot(111)
    init_lay = init_conc[k,:,:]
    init_lay = np.ma.masked_where(init_lay==0,init_lay)
    ax.imshow(init_lay,extent=imshow_extent)
    for line in lines:                        
        ax.plot(line[0,:],line[1,:],'k-',lw=0.25)
    l_name = seawat.layer_botm_names[k]
    ax.set_title(l_name)
    fig_name = 'png\\input\\init_conc_'+l_name+'.png'
    pylab.savefig(fig_name,format='png',dpi=500)
    