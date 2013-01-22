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
nrow,ncol = 100,100
delr,delc = 1.0,1.0
npar = nrow * ncol
itrunc = 100

f_out = open('kl_config.py','w')
f_out.write('nrow,ncol = '+str(nrow)+','+str(ncol)+'\n')
f_out.write('delr,delc = '+str(delr)+','+str(delc)+'\n')
f_out.close()

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

#--run ppcov.exe for testing
#os.system('ppcov.exe <ppcov.in')

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
#np.savetxt('cov1.mat',cov,fmt='%15.6e')        


#--full SVD
u,s,vt = np.linalg.linalg.svd((cov))
#np.savetxt('u.mat',u,fmt=' %15.6e')
np.savetxt('s.vec',s,fmt=' %15.6e')

#--plot singular spectrum
#fig = pylab.figure()
#ax = pylab.subplot(111)
#ax.plot(s)
#pylab.show()
#--form and save FE^0.5 (unscale)
#-- and (scale) E^-0.5F^T

scale = u[:,:itrunc].copy()
unscale = u[:,:itrunc].copy()

for i in range(itrunc):   
    
    scale[:,i] *= (1.0/np.sqrt(s[i]))        
    unscale[:,i] *= np.sqrt(s[i])             

scale = scale.copy().transpose()        
        
np.savetxt('scale.mat',scale,fmt=' %15.6e')
np.savetxt('unscale.mat',unscale,fmt=' %15.6e')



#--additional testing stuff...
ptest = np.zeros_like(pval) + np.log10(200)
pscale_test = np.dot(scale,ptest)
np.savetxt('pscale_test.dat',pscale_test)
punscale_test = np.dot(unscale,pscale_test).copy()
np.savetxt('punscale_test.dat',10**(punscale_test))
unarr_test = np.zeros((nrow,ncol))
c = 0
for i in range(nrow):
    for j in range(ncol):
        unarr_test[i,j] = 10**punscale_test[c]      
        c += 1
fig = pylab.figure()
ax = pylab.subplot(111,aspect='equal')
X,Y = np.meshgrid(x,y)
p = ax.pcolor(X,Y,(unarr_test))
pylab.colorbar(p)

#--load test array
arr = loadtxt(nrow,ncol,'real1.ref')
pval = []
for i in range(nrow):
    for j in range(ncol):
        pval.append(arr[i,j]) 

pval = np.log10(np.array(pval))
np.savetxt('pval.dat',pval)
pval_mean = np.mean(pval)
#pval -= pval_mean
pscale = np.dot(scale,pval).copy()
punscale = np.dot(unscale,pscale).copy()


np.savetxt('pscale.dat',pscale)
np.savetxt('punscale.dat',10**punscale)
pscale[0] *= 5.0
punscale2 = np.dot(unscale,pscale).copy()

#--plot the original and truncated field
unarr = np.zeros((nrow,ncol))-999
unarr2 = np.zeros((nrow,ncol))-999
c = 0
for i in range(nrow):
    for j in range(ncol):
        unarr[i,j] = 10**punscale[c]
        unarr2[i,j] = 10**punscale2[c]
        c += 1

np.savetxt('unarr.ref',unarr,fmt=' %15.6e')

#if nrow > 1:
X,Y = np.meshgrid(x,y)
fig = pylab.figure()
ax = pylab.subplot(311,aspect='equal')
ax2 = pylab.subplot(312,aspect='equal')
ax3 = pylab.subplot(313,aspect='equal')
p = ax.pcolor(X,Y,np.log10(arr))
vmin,vmax = np.log10(arr).min(),np.log10(arr).max()
#pylab.colorbar(p)
p = ax2.pcolor(X,Y,np.log10(unarr),vmin=vmin,vmax=vmax)
#p = ax2.pcolor(X,Y,(unarr),vmin=vmin,vmax=vmax)
p = ax3.pcolor(X,Y,np.log10(unarr2),vmin=vmin,vmax=vmax)
#p = ax3.pcolor(X,Y,(unarr2),vmin=vmin,vmax=vmax)
pylab.show()


sys.exit()


if nrow == 1:
    jj = 10
    fig = pylab.figure()
    p = np.linspace(1,npar,npar)
    for j in range(jj):            
        ax = pylab.subplot(jj,1,j+1) 
        print p.shape,u[:,j].shape
        ax.plot(p,u[:,j],'k-')
        if j == 0:
            xmin,xmax = ax.get_xlim()
        else:
            ax.set_xlim(xmin,xmax)
        ax.set_xticklabels([])
        ax.set_yticklabels([])                   

    
#--for 2-d
else:
    X,Y = np.meshgrid(x,y)
    jj = 10
    vmin,vmax = u[:,0].min(),u[:,0].max()            
    for jjj in range(jj):            
        #--shape column of v into 2-d grid
        p = np.zeros((nrow,ncol))
        c = 0
        for j in range(ncol):
            for i in range(nrow):
                p[i,j] = u[c,jjj]
                c += 1  
        #print jj,j    
        fig = pylab.figure()
        ax = pylab.subplot(111,aspect='equal')                    
        #ax.pcolor(X,Y,p,vmin=vmin,vmax=vmax)        
        ax.pcolor(X,Y,p)       
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.set_xlim(x.min(),x.max())
        ax.set_ylim(y.min(),y.max())                   

pylab.show()                


    




