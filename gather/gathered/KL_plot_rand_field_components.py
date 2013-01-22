import sys
import os
import numpy as np
import pylab
import pestUtil as pu

def exp_vario(h,a=1.0,sill=1.0):
   return sill * (1.0 - (np.exp((-h/a))))

def dist(p1,p2):
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5

def loadtxt(nrow,ncol,file):
	'''
	read 2darray from file
	file(str) = path and filename
	'''
	try:
		file_in = open(file,'r')
		openFlag = True
	except:
#		assert os.path.exists(file)
		file_in = file
		openFlag = False
	
	data = np.zeros((nrow*ncol),dtype='double')-1.0E+10
	d = 0
	while True:
		line = file_in.readline()
		if line is None or d == nrow*ncol:break
		raw = line.strip('\n').split()
		for a in raw:
			try:
				data[d] = float(a)
			except:
				print 'error casting to float on line: ',line
				sys.exit()
			if d == (nrow*ncol)-1:
				assert len(data) == (nrow*ncol)
				data.resize(nrow,ncol)
				return(data) 
			d += 1	
	file_in.close()
	data.resize(nrow,ncol)
	return(data)

#--name of the structure file
sfile = 'structure.dat'
a = 10.0
sill = 1.0    
pu.write_structure('structure.dat','struct1',a=a,sill=sill,transform='log')

#--specify grid shape and create x,y locations vectors
offset = [0.0,0.0]
nrow,ncol = 25,25
delr,delc = 1.0,1.0
npar = nrow * ncol
itrunc = 500

x = np.zeros((ncol))
y = np.zeros((nrow))
for j in range(ncol):
    x[j] = offset[0] + (j*delr) + delr/2.0
for i in range(nrow):
    y[i] = offset[1] + (i*delc) + delc/2.0

#--save a grid spc file
f = open('grid.spc','w')
f.write(str(nrow)+' '+str(ncol)+'\n')
f.write('{0:15.6e} {1:15.6e} 0.0\n'.format(offset[0],offset[1]+y.max()+(delc/2.0)))
for j in range(ncol):
    f.write(str(delr)+' ')
f.write('\n')
for i in range(nrow):
    f.write(str(delc)+' ')
f.write('\n')
f.close()    

#--zone array
np.savetxt('zone.ref',np.ones((nrow,ncol)),fmt='%3.0f')

#--run fieldgen for a single realization
os.system('fieldgen.exe <fieldgen.in')

#--write out an equivalent pp_locs file for testing
f_out = open('pp_locs.dat','w')
c = 0 
ppoints = [] 
pval = []  
for xx in x:
    for yy in y:
        f_out.write('pp'+str(c)+'  {0:15.6e} {1:15.6e} 1  1.0\n'.format(xx,yy))
        ppoints.append([xx,yy])
        pval.append(xx*yy)
        c += 1
f_out.close()
pval = np.array(pval)

#--define and fill covariance matrix
cov = np.zeros((npar,npar))
#--fill in the diagonal
for p in range(npar):
    cov[p,p] = sill
#--fill in the upper tri along rows
for i in range(npar):
    for j in range(i+1,npar):
        d = dist(ppoints[j],ppoints[i])
        v = exp_vario(d,sill=sill,a=a)
        cov[i,j] =  sill -  v
#--replicate across the diagonal
for i in range(npar):
    for j in range(i+1,npar):
        cov[j,i] = cov[i,j]  

#--full SVD
u,s,vt = np.linalg.linalg.svd((cov))
#np.savetxt('u.mat',u,fmt=' %15.6e')
#np.savetxt('s.vec',s,fmt=' %15.6e')

#--load test array
arr = loadtxt(nrow,ncol,'real1.ref')
pval = []
for i in range(nrow):
    for j in range(ncol):
        pval.append(arr[i,j]) 
pval = np.log10(np.array(pval))
#np.savetxt('pval.dat',pval)
pval_mean = np.mean(pval)

#--plot singular spectrum
#fig = pylab.figure()
#ax = pylab.subplot(111)
#ax.plot(s)
#pylab.show()

#--plot the eigenvectors
for e in range(1,30):
    eig = u[:,e]
    unarr = np.zeros((nrow,ncol))-999        
    c = 0
    for i in range(nrow):
        for j in range(ncol):
            unarr[i,j] = 10**eig[c]            
            c += 1    
    X,Y = np.meshgrid(x,y)
    fig = pylab.figure(figsize=(2,2))
    ax = pylab.subplot(111,aspect='equal')
    p = ax.pcolor(X,Y,np.log10(unarr))
    ax.set_yticklabels([])  
    ax.set_xticklabels([])
    ax.set_title('eig '+str(e))
    pylab.savefig('png\\eig'+str(e)+'.png',dpi=300,fmt='png',bbox_inches='tight')                 
    

X,Y = np.meshgrid(x,y)
fig = pylab.figure(figsize=(2,2))
ax = pylab.subplot(111,aspect='equal')
p = ax.pcolor(X,Y,np.log10(arr))
ax.set_yticklabels([])  
ax.set_xticklabels([])
ax.set_title('base')
pylab.savefig('png\\base.png',dpi=300,fmt='png',bbox_inches='tight')   

vmin,vmax = np.log10(arr).min(),np.log10(arr).max()

fig_count = 1
for t in range(1,56,5):
    print t

    #--form and save FE^0.5 (unscale)
    #-- and (scale) E^-0.5F^T
    scale = u[:,:t].copy()
    unscale = u[:,:t].copy()
    for i in range(t):       
        scale[:,i] *= (1.0/np.sqrt(s[i]))        
        unscale[:,i] *= np.sqrt(s[i])             
    scale = scale.copy().transpose()       
    #print scale.shape,unscale.shape
    pscale = np.dot(scale,pval).copy()
    
    punscale = np.dot(unscale,pscale).copy()    
    unarr = np.zeros((nrow,ncol))-999    
    c = 0
    for i in range(nrow):
        for j in range(ncol):
            unarr[i,j] = 10**punscale[c]            
            c += 1       
    fig = pylab.figure(figsize=(2,2))
    ax = pylab.subplot(111,aspect='equal')               
    p = ax.pcolor(X,Y,np.log10(unarr),vmin=vmin,vmax=vmax)  
    ax.set_yticklabels([])  
    ax.set_xticklabels([])
    ax.set_title(str(t)+' components')
    pylab.savefig('png\\trunc_'+str(fig_count)+'.png',dpi=300,fmt='png',bbox_inches='tight')   
    fig_count += 1


