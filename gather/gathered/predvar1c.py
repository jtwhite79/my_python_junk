import numpy as np
import pylab
import pestUtil as pu


#--load q^0.5X
xx = np.loadtxt('qX.mat')
xx_s = np.loadtxt('qX_s.mat')

#--get structual parameter names
structpar_names = []
f = open('struct.dat','r')
for line in f:
    structpar_names.append(line.strip())
f.close()
#print astructpar

#--get predvector
y1,par_names,cn = pu.load_matrix('pd_3_one.vec')

#--get cp matrix
cp = np.loadtxt('cp.mat')

is_structpar = []
for p in par_names:
    if p in structpar_names:
        is_structpar.append(True)
    else:
        is_structpar.append(False)

#--form y and y_s from y1
#--assume y1 in same order as everything
y,y_s = [],[]
for val,is_struct in zip(y1,is_structpar):
    if is_struct:
        y_s.append(val)
    else:
        y.append(val)
        
y,y_s = np.array(y),np.array(y_s)      


nxrow1 = xx.shape[0]
nespar = len(par_names)
nstpar = len(structpar_names)

u,s,vt = np.linalg.linalg.svd(xx)
s *= s
sx = 1.0/s

singvals = np.loadtxt('singvals.dat',dtype=np.int)
#singvals = [20]
ytv2 = np.zeros((nespar-nstpar))
ytv1 = np.zeros((nespar-nstpar))
yy = np.zeros((nespar))
yyu1t = np.zeros(nxrow1)
yyy_s = np.zeros(nstpar)
refvar = 1.0

for sv in singvals:
    #--first term
    
    j=0
    for i in range(sv):
        
        rtemp = 0.0
        for k in range(nespar-nstpar):
            rtemp += y[k] * vt[i,k]
        ytv2[j] = rtemp
        j += 1 
    for i in range(nespar-nstpar):
        j = 0
        rtemp = 0.0           
        for k in range(sv):
            rtemp += ytv2[j] * vt[k,i]
            j += 1
        yy[i] = rtemp
    first = 0.0
    ii = 0
    
    for i in range(nespar):
        if is_structpar[i] is False:
            jj = 0
            for j in range(nespar):
                if is_structpar[j] is False:
                    
                    first += yy[ii] * cp[i,j] * yy[jj]
                    jj += 1
            ii += 1         
    
    #--second term
    if sv == 0:
        second = 0.0
    else:
        if sv > nespar-nstpar:
            sv = nespar-nstpar
        for i in range(sv):
            rtemp = 0.0
            for k in range(nespar-nstpar):
                rtemp += y[k] * vt[i,k]
            ytv1[i] = rtemp
        
        second = 0.0
        for i in range(sv):
            second += ytv1[i] * sx[i] * ytv1[i]
        second *= refvar
        

    #--structural term
    for i in range(sv):
        rtemp = 0.0
        for k in range(nespar-nstpar):
            rtemp += y[k] * vt[i,k]
        ytv1[i] = rtemp

    for i in range(sv):
        ytv1[i] *= sx[i]                
  
    for i in range(nxrow1):
        rtemp = 0.0
        for j in range(sv):
            rtemp += ytv1[j] * u[i,j]
        yyu1t[i] = rtemp
    
    for j in range(nstpar):
        rtemp = 0.0
        for i in range(nxrow1):
            rtemp += yyu1t[i] * xx_s[i,j]
            #print rtemp,yyu1t[i],xx_s[i,j]
        yyy_s[j] = rtemp

    for i in range(nstpar):
        yyy_s[i] -= y_s[i]    
    
    s_term = 0.0
    jj = 0
    for i in range(nespar):    
        if is_structpar[i] is True:           
            rtemp = 0.0
            for ii in range(nespar):
                if is_structpar[ii] is True:                              
                    rtemp += yyy_s[jj] * cp[i,ii] * yyy_s[jj]                                
            jj += 1
            s_term += rtemp            
    print first,second,s_term
    
           
#print pv1b[0,0]
#np.savetxt('ua.dat',u)
#np.savetxt('sa.dat',s)
#np.savetxt('vta.dat',vt)
#lhs = np.loadtxt('lhs.mat')
#diff = vt - lhs
#diff = np.ma.masked_where(np.abs(diff) < 1.0e-5,diff)
#fig = pylab.figure()
#ax = pylab.subplot(111)
#ax.pcolor(diff)
#pylab.show()
#print u.shape,s.shape,vt.shape
#print np.cumsum(diff)[-1]
#print diff.max(),diff.min()