import numpy as np
import pylab
from matplotlib import transforms
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

import MFBinaryClass as mfb

def get_cell_corners(delta_x,array,offset=[0.0]):
    xs = []
    zs = []
    nlay,ncol = array.shape 
    #print ncol,nlay   
    for l in range(1,nlay):
        for c in range(1,ncol):
            #this_xs = [c*delta_x,(c*delta_x)+delta_x,(c*delta_x)+delta_x,c*delta_x,None]
            this_xs = [offset[0]+(c*delta_x),offset[0]+(c*delta_x)+delta_x,\
                       offset[0]+(c*delta_x)+delta_x,offset[0]+(c*delta_x),None]
            #this_ys = [array[c-1,l-1],array[c-1,l],array[c,l-1],array[c,l],None]
            this_zs = [array[l-1,c-1],array[l-1,c-1],array[l,c],array[l,c],None]            
            xs.extend(this_xs)
            zs.extend(this_zs)   
            #print this_zs
            #break
        #break                                          
    return xs,zs
 
def get_cell_rects(delta_x,array,offset=[0,0]):
    rects = []
    nlay,ncol = array.shape 
    #print ncol,nlay   
    for l in range(1,nlay):
        for c in range(1,ncol):
            this_xs = [offset[0]+(c*delta_x),offset[0]+(c*delta_x)+delta_x,\
                       offset[0]+(c*delta_x)+delta_x,offset[0]+(c*delta_x)]
            this_zs = [array[l-1,c-1],array[l-1,c-1],array[l,c],array[l,c]]
            this_rect = np.array(zip(this_xs,this_zs))            
            rects.append(Polygon(this_rect,True))
            #print len(rects)
            #rects.append(zip(this_xs,this_zs))
            #break
        #break                   
    return rects 
 
    
   
nrow,ncol,nlay = 411,501,6
delr,delc = 500,500
offset = [728600.0,577350.0,0.0] 
master = np.zeros((nlay+1,nrow,ncol)) - 1.0e+20

#--load top
top = np.loadtxt('ref\\top_filter_20_edge.ref')

master[0] = top

#--load layer bottoms
dir = 'ref\\'
layer_refs = ['bot_q4.ref','bot_q3.ref','bot_q2.ref',\
              'bot_q1.ref','bot_t1.ref','bot_t2.ref']
l = 1
for r in layer_refs:
    this_lay = np.loadtxt(dir+r)
    master[l] = this_lay
    l += 1
    
   
xsec_row = 185  #pompano
#xsec_row = 277   #dixie
#xsec_row = 380   #C-9
start_col,end_col = 250,460



#conc_handle = mfb.MT3D_Concentration(nlay,nrow,ncol,'MT3D001.UCN')
#totim_c,kstp_c,kper_c,c,success = conc_handle.get_record()

#--thickness
#thk_array = np.zeros((nlay,nrow,ncol))
#for l in range(1,nlay+1):
#    thk_array[l-1,:,:] = master[l-1,:,:] - master[l,:,:]
#print thk_array.max()
#thk_array /= thk_array.max()
#print thk_array.max()
#
thk_array = np.zeros((nlay,nrow,ncol))                  
for l in range(1,nlay+1):                               
    thk_array[l-1,:,:] = l

plot_array = master[:,xsec_row,start_col:end_col]
color_array = thk_array[:,xsec_row,start_col:end_col]

#--build normalized color array
#max_c = color_array.max()
#min_c = color_array.min()
#num_val = color_array.shape[1]
#normed_color = np.linspace(min_c,max_c,num_val)
#print color_array.shape,normed_color.shape
#print min_c,max_c
#print color_array.max()
#color_array /= color_array.min()
#print color_array.max()
fig = pylab.figure()

#xs,zs = get_cell_corners(delc,plot_array,offset)
#ax = pylab.subplot(211)
#p = ax.fill(xs,zs,edgecolor='none')



ax2 = pylab.subplot(111)

for l in range(1,nlay+1):
    #print 'layer',l,l-2
    rects = get_cell_rects(delc,plot_array[l-1:l+1])
    col = PatchCollection(rects,edgecolor='none')
    col.set_array(color_array[l-1])
    #col.set_array(normed_color)
    #print col
    
    ax2.add_collection(col) 
    ax2.autoscale_view()
    #break
#ax2.set_xlim(xmin,xmax)
#ax.set_xlim(xmin,xmax)
ax2.set_ylabel('Elevation (feet NAVD)')
pylab.show()

    