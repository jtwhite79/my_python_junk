import numpy as np
import pylab

data = np.loadtxt('lt_pars.dat',delimiter=' ') 
rows,cols =  np.shape(data)
x = np.arange(1,cols)
for col in range(1,cols):
    fig = pylab.figure(figsize=(11,8.5))
    ax = pylab.subplot(111)
    print data[:,col]
    #ax.bar(x,data[col,:])
    #pylab.show()