import sys
import numpy as np
from numpy import ma
import pylab
import MFBinaryClass as mfb

import shapefile
import arrayUtil as au

def load_reaches(nreach,file,skiprows=0,usecols=[0]):
    f = open(file,'r')
    for r in range(skiprows):
        f.readline()
    data = np.zeros(len(usecols))
    
    for line in f:
        this_line = line.strip().split()
        this_entry = []
        #print this_line
        for c in range(len(usecols)):
            this_entry.append(float(this_line[usecols[c]]))
        data = np.vstack((data,np.array(this_entry)))
        if data.shape[0] > nreach: break
    return np.delete(data,0,axis=0)

def load_next_wel_sp(f):
    itmp = int(f.readline().strip().split()[0])
    well_list = []
    for i in range(itmp):
        line = f.readline()
        well_list.append(line)
    return well_list
    
    
  
nrow,ncol,nlay = 411,501,1
delr,delc = 500,500
offset = [728600.0,577350.0,0.0]
results = 'results\\'
nreach = 2400

#--open the existing well file and read the header junk
f_wel = open('wel\\avg_ann.wel','r')
f_wel.readline()
mxact = int(f_wel.readline().strip().split()[0])




reach_key = load_reaches(nreach,'dis\\dataset.txt',skiprows=2,usecols=[0,2,4,5])

f_out_riv = open('test.riv','w')
f_out_riv.write('#swr river equivalent\n')
f_out_riv.write('{0:10.0f} {1:10.0f}\n'.format(0,0))
f_out_riv.write('{0:10.0f} {1:10.0f}\n'.format(nreach,0))

f_out_wel = open('test.wel','w')
f_out_wel.write('#swr wel package equivalent\n')
f_out_wel.write('{0:10.0f} {1:10.0f}\n'.format(0,0))
f_out_wel.write('{0:10.0f} {1:10.0f}\n'.format(nreach+mxact,0))

#--get aq_ex info
swr_obj = mfb.SWR_Record(1,results+'bro_7lay.aqx')
swr_items = swr_obj.get_item_list()      
header_items = swr_obj.get_header_items()
st_idx = swr_items.index('stage')
cond_idx = swr_items.index('cond')
lay_idx = swr_items.index('ilay')
rch_idx = swr_items.index('irch')
aqflow_idx = swr_items.index('aq-rchflow')
bot_idx = swr_items.index('bottom')

#--setup unique,row and col arrays
totim,dt,kper,kstp,swrstp,success,r = swr_obj.next()
rch_unique = np.unique(r[:,rch_idx])
row = np.zeros_like(rch_unique) - 999
col = np.zeros_like(rch_unique) - 999

for idx in range(rch_unique.shape[0]):
    reaches = r[np.where(r[:,rch_idx]==rch_unique[idx])]          
    row[idx] = reach_key[np.where(reach_key[:,0]==rch_unique[idx]),2][0]
    col[idx] = reach_key[np.where(reach_key[:,0]==rch_unique[idx]),3][0]      

#--re-instance the object to reset
swr_obj = mfb.SWR_Record(1,results+'bro_7lay.aqx')

#--for each entry in the file
while True:
    #--get this record
    totim,dt,kper,kstp,swrstp,success,r = swr_obj.next()
    if success == False:
        break
    
    existing_wells = load_next_wel_sp(f_wel)    
    
    
    cond = np.zeros_like(rch_unique) - 1.0e+20
    stage = np.zeros_like(rch_unique) - 1.0e+20
    flow =  np.zeros_like(rch_unique) - 1.0e+20
    bot =  np.zeros_like(rch_unique) + 999   
    #--for each unique reach, sum the conductances for each intersected layer    
    for idx in range(rch_unique.shape[0]):
        reaches = r[np.where(r[:,rch_idx]==rch_unique[idx])]   
        cond[idx] = np.cumsum(reaches[:,cond_idx])[-1]
        stage[idx] = np.mean(reaches[:,st_idx])    
        bot[idx] = np.min(reaches[:,bot_idx])
        flow[idx] = np.cumsum(reaches[:,aqflow_idx])[-1]           
    #--flip the sign on the flow
    flow *= -1.0
   
       
    #--for each unique reach, write out the equivalent riv entry
    f_out_riv.write('{0:10.0f} {1:10.0f} # totim,kper,kstp {2:10.3e}{3:6.0f}{4:6.0f}  \n'\
         .format(nreach,0,totim,kper,kstp))
    for idx in range(rch_unique.shape[0]):
        f_out_riv.write('{0:10.0f} {1:10.0f} {2:10.0f} {3:10.3e}  {4:10.3e}  {5:10.3e}  # reach number {6:6.0f}\n'\
            .format(1,row[idx],col[idx],stage[idx],cond[idx],bot[idx],rch_unique[idx]))
    
    
    
    #--for each unique reach, write out the equivalent wel entry
    f_out_wel.write('{0:10.0f} {1:10.0f} # totim,kper,kstp {2:10.3e}{3:6.0f}{4:6.0f}  # reach number {5:6.0f}\n'\
         .format(nreach+mxact,0,totim,kper,kstp,rch_unique[idx]))
    
    #--write the existing wells to the new file
    for w in existing_wells:
       f_out_wel.write(w)
             
    for idx in range(rch_unique.shape[0]):
        f_out_wel.write('{0:10.0f} {1:10.0f} {2:10.0f} {3:10.3e} #   reach number {4:6.0f}\n'\
            .format(1,row[idx],col[idx],flow[idx],rch_unique[idx]))
        
    print totim,kper,kstp,np.cumsum(flow)[-1]
    #break  
    

f_out_riv.close
f_out_wel.close            