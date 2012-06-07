import datetime
import re,sys
import numpy as np
import pylab
from matplotlib.dates import *
import matplotlib.ticker as tk


def load_uzf_budget(file,key='UNSATURATED ZONE PACKAGE VOLUMETRIC BUDGET'):
    try:
        f = open(file,'r')
    except:
        print 'Unable to open file: ',file
        return []  
    
    reg = re.compile(key,re.IGNORECASE)
    
    in_flux = np.zeros(1)
    out_flux = np.zeros(2)
    stor_flux = np.zeros(1)
    in_vol = np.zeros(1)
    out_vol = np.zeros(2)
    stor_vol = np.zeros(1)
    
    sp_ts = np.zeros(2)
    
    while True:
        line = f.readline()
       
        if reg.search(line) != None:
            
            this_sp = int(line[76:].strip())
            this_ts = int(line[58:63].strip())
            sp_ts = np.vstack((sp_ts,(this_sp,this_ts)))
            this_in_flux,this_out_flux,this_stor_flux = [],[],[]
            this_in_vol,this_out_vol,this_stor_vol = [],[],[]
           
            for a in range(0,9): f.readline()
       
            line2 = f.readline() 
            this_in_vol.append(float(line2[22:40].strip()))
            this_in_flux.append(float(line2[64:80].strip()))
            #print this_in_vol,in_vol    
            in_vol = np.vstack((in_vol,this_in_vol))
            in_flux = np.vstack((in_flux,this_in_flux))

            for a in range(0,3): f.readline()
            for a in range(0,2):
                line3 = f.readline() 
                this_out_vol.append(float(line3[22:40].strip()))
                this_out_flux.append(float(line3[64:80].strip()))
           #print this_out_vol,out_vol
            out_vol = np.vstack((out_vol,this_out_vol))
            out_flux = np.vstack((out_flux,this_out_flux))
            
            for a in range(0,5): f.readline()
            line4 = f.readline()
            this_stor_vol.append(float(line3[22:40].strip()))
            this_stor_flux.append(float(line3[64:80].strip()))
            stor_vol = np.vstack((stor_vol,this_stor_vol))
            stor_flux = np.vstack((stor_flux,this_stor_flux))
            
        elif len(line) == 0: break
    sp_ts = np.delete(sp_ts,0,axis=0)
    in_flux = np.delete(in_flux,0,axis=0)
    out_flux = np.delete(out_flux,0,axis=0)
    in_vol = np.delete(in_vol,0,axis=0)
    out_vol = np.delete(out_vol,0,axis=0)
    stor_flux = np.delete(stor_flux,0,axis=0)
    stor_vol = np.delete(stor_vol,0,axis=0)
    return [sp_ts,in_flux,out_flux,stor_flux,in_vol,out_vol,stor_vol]




def get_mf_items(file,key='VOLUMETRIC BUDGET FOR ENTIRE MODEL'):
    try:
        f = open(file,'r')
    except:
        print 'Unable to open file: ',file
        return []
    reg = re.compile(key,re.IGNORECASE)
    reg_in  = re.compile('STORAGE',re.IGNORECASE)
    
    items = []        
    while True:
    
        line = f.readline()
        
        if line == '': 
            f.close()
            return []
        if reg.search(line) != None:
            while True:
                line2 = f.readline()
                if reg_in.search(line2) != None:
                    items.append(line2.strip().split('=')[0])
                    line3 = f.readline()
                    while line3.strip().split('=')[0] != '':
                        items.append(line3.strip().split('=')[0])
                        line3 = f.readline()
                    f.close()    
                    return items
                
def load_mf_budget(file,items,key='VOLUMETRIC BUDGET FOR ENTIRE MODEL'):
    try:
        f = open(file,'r')
    except:
        print 'Unable to open file: ',file
        return []  
    
    reg = re.compile(key,re.IGNORECASE)
    
    in_flux = np.zeros(len(items))
    out_flux = np.zeros_like(in_flux)
    in_vol = np.zeros_like(in_flux)
    out_vol = np.zeros_like(in_flux)
    
    sp_ts = np.zeros(2)
    
    while True:
        line = f.readline()
       
        if reg.search(line) != None:
            
            this_sp = int(line[76:].strip())
            this_ts = int(line[56:60].strip())
            sp_ts = np.vstack((sp_ts,(this_sp,this_ts)))
            this_in_flux,this_out_flux = [],[]
            this_in_vol,this_out_vol = [],[]
           
            for a in range(0,7): f.readline()
            for a in range(0,len(items)):
                line2 = f.readline() 
                this_in_vol.append(float(line2[22:40].strip()))
                this_in_flux.append(float(line2[64:80].strip()))
            #print this_in_vol,in_vol    
            in_vol = np.vstack((in_vol,this_in_vol))
            in_flux = np.vstack((in_flux,this_in_flux))

            for a in range(0,5): f.readline()
            for a in range(0,len(items)):
                line3 = f.readline() 
                this_out_vol.append(float(line3[22:40].strip()))
                this_out_flux.append(float(line3[64:80].strip()))
           #print this_out_vol,out_vol
            out_vol = np.vstack((out_vol,this_out_vol))
            out_flux = np.vstack((out_flux,this_out_flux))
        elif len(line) == 0: break
    sp_ts = np.delete(sp_ts,0,axis=0)
    in_flux = np.delete(in_flux,0,axis=0)
    out_flux = np.delete(out_flux,0,axis=0)
    in_vol = np.delete(in_vol,0,axis=0)
    out_vol = np.delete(out_vol,0,axis=0)
    return [sp_ts,in_flux,out_flux,in_vol,out_vol]


def plot_ts(t,data,names,output='show',ax=None,color=None,lw=1.0):
    #print 'total date range: ',t[-1]-t[0]
    #--set up date formatters
    if t[-1]-t[0] < 90:
       majortick   = MonthLocator() 
       minortick   = DayLocator(15)                                               
       minFmt = DateFormatter('%d')                                     
       majFmt = DateFormatter('%b')       
    elif t[-1]-t[0] < 365:
        majortick   = MonthLocator() 
        minortick   = DayLocator()                                               
        minFmt = DateFormatter('')                                     
        majFmt = DateFormatter('%b')   
    elif t[-1]-t[0] < 5280:
        majortick   = YearLocator() 
        minortick   = MonthLocator((5,9))                                               
        minFmt = DateFormatter('%b')                                     
        majFmt = DateFormatter('%Y')           
    elif t[-1]-t[0] < 3650:
        majortick   = YearLocator(2) 
        minortick   = MonthLocator()                                               
        minFmt = DateFormatter('')                                     
        majFmt = DateFormatter('%Y')       
    else:
        majortick   = YearLocator(5) 
        minortick   = YearLocator()                                               
        minFmt = DateFormatter('')                                    
        majFmt = DateFormatter('%Y')       
   

    if ax == None:
        fig = pylab.figure()
        ax = pylab.subplot(111)
    #print data.shape
    try:
        for s in range(0,np.shape(data)[1]):
            if color != None:
                ax.plot(t,data[:,s],label=names[s],color=color[s],lw=lw)
            else:
                ax.plot(t,data[:,s],label=names[s],lw=lw)
    except:
        if color != None:
            ax.plot(t,data,label=names,color=color,lw=lw)
        else:
            ax.plot(t,data,label=names,lw=lw)
    
    if names != None:
        ax.legend()
        
    ax.xaxis.set_major_locator(majortick)
    ax.xaxis.set_minor_locator(minortick)
    ax.xaxis.set_major_formatter(majFmt)
    ax.xaxis.set_minor_formatter(minFmt)
    
    if output =='show' : 
        pylab.show()
        return
    elif output == None: return ax
    else:
         fmt = output.split('.')[-1]
         pylab.savefig(output,orientation='portrait',format=fmt,dpi=150)
         return 

def get_swr_items(file,key='VOLUMETRIC SURFACE WATER BUDGET'):
    try:
        f = open(file,'r')
    except:
        print 'Unable to open file: ',file
        return []
    reg = re.compile(key,re.IGNORECASE)
    reg_in  = re.compile('LATERAL FLOW',re.IGNORECASE)
    
    items = []
    dict_items = {}        
    while True:
    
        line = f.readline()
        
        if line == '': 
            f.close()
            return []
        if reg.search(line) != None:
            while True:
                line2 = f.readline()
                if reg_in.search(line2) != None:
                    items.append(line2.strip().split('=')[0])
                    line3 = f.readline()
                    while line3.strip().split('=')[0] != '':
                        items.append(line3.strip().split('=')[0])
                        line3 = f.readline()
                    f.close()    
                    return items

def load_swr_budget(file,items,key='VOLUMETRIC SURFACE WATER BUDGET'):
    try:
        f = open(file,'r')
    except:
        print 'Unable to open file: ',file
        return []  
    
    reg = re.compile(key,re.IGNORECASE)
    
    in_flux = np.zeros(len(items))
    out_flux = np.zeros_like(in_flux)
    in_vol = np.zeros_like(in_flux)
    out_vol = np.zeros_like(in_flux)
    
    sp_ts = np.zeros(2)
    
    while True:
        line = f.readline()
       
        if reg.search(line) != None:
            sp_line = f.readline()
            this_sp = int(sp_line[59:].strip())
            this_ts = int(sp_line[37:42].strip())
            sp_ts = np.vstack((sp_ts,(this_sp,this_ts)))
            this_in_flux,this_out_flux = [],[]
            this_in_vol,this_out_vol = [],[]
           
            for a in range(0,7): f.readline()
            for a in range(0,len(items)):
                line2 = f.readline() 
                this_in_vol.append(float(line2[22:40].strip()))
                this_in_flux.append(float(line2[64:80].strip()))
            #print this_in_vol,in_vol    
            in_vol = np.vstack((in_vol,this_in_vol))
            in_flux = np.vstack((in_flux,this_in_flux))

            for a in range(0,5): f.readline()
            for a in range(0,len(items)):
                line3 = f.readline() 
                this_out_vol.append(float(line3[22:40].strip()))
                this_out_flux.append(float(line3[64:80].strip()))
           #print this_out_vol,out_vol
            out_vol = np.vstack((out_vol,this_out_vol))
            out_flux = np.vstack((out_flux,this_out_flux))
        elif len(line) == 0: break
    sp_ts = np.delete(sp_ts,0,axis=0)
    in_flux = np.delete(in_flux,0,axis=0)
    out_flux = np.delete(out_flux,0,axis=0)
    in_vol = np.delete(in_vol,0,axis=0)
    out_vol = np.delete(out_vol,0,axis=0)
    return [sp_ts,in_flux,out_flux,in_vol,out_vol]



def fail_count(file,key='CONVERGENCE FAILURE',skey='AT END OF TIME STEP'):
    try:
        f = open(file,'r')
    except:
        print 'Unable to open file: ',file
        return []  
    
    reg = re.compile(key,re.IGNORECASE)
    sreg = re.compile(skey,re.IGNORECASE)
    sp_ts = np.zeros((2))
    
    while True:
        line = f.readline()
        #print line
        if reg.search(line) != None:
            
            found = True
            while found == True:
                line2 = f.readline()
                
                if sreg.search(line2) != None:
                    this_sp = int(line2[59:].strip())
                    this_ts = int(line2[37:42].strip())
                    sp_ts = np.vstack((sp_ts,(this_sp,this_ts)))
                    found = False

        elif len(line) == 0: break
    sp_ts = np.delete(sp_ts,0,axis=0)
    return sp_ts.astype(int)

#init_ord = 728659
#file = 'Results\\syn_swr.lst'
#items_swr = get_swr_items(file)
#[st,sifx,sofx,siv,sov] = load_swr_budget(file,items_swr)
#st += init_ord
#items_mf = get_mf_items(file)
#[mt,mifx,mofx,miv,mov] = load_mf_budget(file,items_mf)
#mt += init_ord
#swr_aqex = sifx[:,4]-sofx[:,4]
#mf_aqex = mifx[:,5]-mofx[:,5] 
#fig = pylab.figure()
#ax = pylab.subplot(211)
#ax = plot_ts(st[:,0]+init_ord,np.array((swr_aqex,-mf_aqex)).transpose(),\
#             ['swr aq ex','mf aqex'],output=None,ax=ax,fig=fig)
#ax2 = pylab.subplot(212)
#plot_ts(st[:,0]+init_ord,(swr_aqex+mf_aqex)/mf_aqex*100,\
#        'aqex % diff',output=None,ax=ax2,fig=fig)
#
#fig = pylab.figure()
#ax = pylab.subplot(111)
#ax.plot(np.abs(swr_aqex),np.abs((swr_aqex+mf_aqex)/mf_aqex*100),'k+')

#for i in range(0,len(items_mf)):
#    print items_mf[i],np.shape(mifx[:,i])
#    plot_ts(mt[:,0]+init_ord,np.array((mifx[:,i],mofx[:,i])).transpose(),\
#            ['mifx-'+str(items_mf[i]),'mofx-'+str(items_mf[i])],output=None)
#    plot_ts(mt[:,0]+init_ord,mifx[:,i]-mofx[:,i],'mf diff-'+str(items_mf[i]),output=None)
#    
#    #plot_ts(t[:,0]+init_ord,np.array((iv[:,i],ov[:,i])).transpose(),['iv-'+str(items[i]),'ov-'+str(items[i])],output=None)
#    #plot_ts(t[:,0]+init_ord,iv[:,i]-ov[:,i],'diff-'+str(items[i]),output=None)
#    
#    
#for i in range(0,len(items_swr)):
#    print items_swr[i],np.shape(sifx[:,i])
#    plot_ts(st[:,0]+init_ord,np.array((sifx[:,i],sofx[:,i])).transpose(),\
#            ['sifx-'+str(items_swr[i]),'sofx-'+str(items_swr[i])],output=None)
#    plot_ts(st[:,0]+init_ord,sifx[:,i]-sofx[:,i],'swr diff-'+str(items_swr[i]),output=None)
#    
#    
#
#pylab.show()
#items = get_mf_items(file)
#[t,ifx,ofx,iv,ov] = load_mf_budget(file,items)
#x = np.linspace(1000,2000,num=t[-1,0]-t[0,0]+1).astype(int)
#plot_ts(t[:,0]*100+init_ord,np.array((ifx[:,2],ofx[:,2])).transpose(),['ifx-'+items[2],'ofx-'+items[2]])
#plot_ts(t[:,0]*100+init_ord,ifx[:,2]-ofx[:,2],'diff-'+items[2])







    

