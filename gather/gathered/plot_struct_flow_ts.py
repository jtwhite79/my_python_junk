import sys
import re
import numpy as np
import pylab
import swr
import MFBinaryClass as mfb  
import bro_info as bi

filename = 'results\\bro_6lay.str'
idx_reach = 5
idx_strnum = 6

crit = None
try:
    crit = sys.argv[1]
except:
    pass

if crit:
    reg = re.compile(crit,re.IGNORECASE)    

header = open(filename,'r').readline().strip().split(',')
uc = []
for i,h in enumerate(header):
    if h != '':
        uc.append(i)
sdata = np.loadtxt(filename,delimiter=',',skiprows=1,usecols=uc)
cfd_2_cfs = 1.0/86400.0
#--scale str flow to cfs
sdata[:,11] *= cfd_2_cfs * 1.0
#--over write invert with up/dw diff
sdata[:,9] = sdata[:,7] - sdata[:,8]
header[9] = 'DIFF'
header.append('')

#--get a list of unique structure reaches
us = np.unique(sdata[:,idx_reach])
#print us

#--load structure info
ds_13a = swr.ds_13a('swr_full\\swr_ds13a_working_strval.dat')
ds_13a.load_structures()
#sys.exit()

#--load the entire active reach stage record
#--better to do it once than over and over
reach_key = np.loadtxt('swr_full\\swr_ds4a.dat',skiprows=2,usecols=[0,2,4,5])
swr_obj = mfb.SWR_Record(0,'results\\bro_6lay.stg')
totim,dt,kper,kstp,swrstp,success,r = swr_obj.next()
stage = r.copy()
stage_totim = [totim]
while True:
    totim,dt,kper,kstp,swrstp,success,r = swr_obj.next()
    if success is False:
        break
    stage = np.hstack((stage,r))
    stage_totim.append(totim)
    
#print stage.shape,stage_totim[0],stage_totim[-1]    
#sys.exit()

#--iswrbnd
iswrbnd = np.loadtxt('swr_full\\swr_ds6.dat')



op_str =  [1,3,8,9]

for u in us:
    ibnd = iswrbnd[np.where(iswrbnd[:,0] == u),1]
    if ibnd != 0:
        
        
        
        #print com                
        #--get unique structure numbers for this reach
        
        this_struct = sdata[np.where(sdata[:,idx_reach]==u)]
        un = np.unique(this_struct[:,idx_strnum])
        for uu in un:
            plot_cols = [7,8,9,10,11]
            this_struct_num = this_struct[np.where(this_struct[:,6]==uu)]
            this_s = None
            for s in ds_13a.structures:
               if s['istrrch'] == u and s['istrnum'] == uu:
                   this_s = s
            
            #--if this is an operable struct, then load the stage ts at the istrorch
            this_stage = None
            if this_s['istrtype'] in op_str:
                istrorch = this_s['istrorch']                                                
                this_stage = stage[np.where(reach_key[:,0]==istrorch),:][0]                                        
                this_struct_num = np.hstack((this_struct_num,this_stage.transpose()))
                plot_cols.append(12)
            
            make = False    
            if crit is not None and reg.search(' '.join(this_s['a_com'])) is not None:
                make = True
            elif crit is None:
                make = True
            if make:                
                fig = pylab.figure()   
                axes = []
                for i,p in enumerate(plot_cols):
                    
                    ax = pylab.subplot(len(plot_cols),1,i+1)
                    ax.plot(this_struct_num[:,0],this_struct_num[:,p],'b-')                
                    ax.text(0.05,0.7,header[p],transform=ax.transAxes)
                    axes.append(ax)
                
                a_com = ' '.join(this_s['a_com'])
                #axes[0].set_title(str(int(uu))+' istrrch:'+str(this_s['istrrch'])+\
                #                     ' ' +str(this_s['istrconn'])+' '+a_com[:35])
                axes[0].set_title(str(this_s['istrtype'])+' '+a_com[:50])                     
                
                #--set the max and min up/dw
                umn,umx = axes[0].get_ylim()
                dmn,dmx = axes[1].get_ylim()
                mx = max(umx,dmx)
                mn = min(umn,dmn)
                #print umx,umn,dmx,dmn,mx,mn
                #axes[0].set_ylim(mn,mx)            
                #axes[1].set_ylim(mn,mx)
                axes[0].set_ylim(-0.5,15)
                axes[1].set_ylim(-0.5,15)
                #--plot the zero line on the opening plot
                #try:
                #    axes[3].set_ylim(0,this_s['strmax'])
                #except:
                #    pass
                
                #--add some reference lines
                if this_s['istrtype'] in op_str:
                    axes[-1].plot([stage_totim[0],stage_totim[-1]],[this_s['cstrcrit'],this_s['cstrcrit']],'k--',lw=2.5)                            
                    axes[-1].text(0.05,0.7,str(this_s['istrorch'])+' istrroch stage '+this_s['cstrolo'],transform=ax.transAxes)
                elif this_s['istrtype'] == 6:
                    #print 'weir invert:',this_s['strinv'],a_com[:35]
                    axes[0].plot([stage_totim[0],stage_totim[-1]],[this_s['strinv'],this_s['strinv']],'k--',lw=2.5) 
                    axes[1].plot([stage_totim[0],stage_totim[-1]],[this_s['strinv'],this_s['strinv']],'k--',lw=2.5) 
pylab.show()        
        
    

