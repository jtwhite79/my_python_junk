import numpy as np
import matplotlib.pyplot as plt
import pylab



x1 = np.array([1,0])
x2 = np.array([0,1])

shear = np.linspace(0.0,2.0,20)
for i,s in enumerate(shear):
    A = np.array([[1,0],[s,1]]).transpose()
    b1 = np.dot(A,x1)
    b2 = np.dot(A,x2)


    fig = pylab.figure(figsize=(5,5))
    ax = pylab.subplot(111)

    ax.plot([0,b1[0]],[0,b1[1]],lw=3.0,color='b',ls='--')
    ax.plot([0,b2[0]],[0,b2[1]],lw=3.0,color='g',ls='--')
    ax.plot([0,x1[0]],[0,x1[1]],lw=3.0,color='b')
    ax.plot([0,x2[0]],[0,x2[1]],lw=3.0,color='g')


    ax.set_xlim(-1,3)
    ax.set_ylim(-1,3)
    ax.grid()
    pylab.savefig('figures\\shear_'+str(i)+'.png',dpi=300,format='png',bbox_inches='tight')
    #pylab.show()


x1 = np.array([0.25,1.1])
x2 = np.array([0.9,0.1])

scale = np.linspace(1.0,2.0,20)
for i,s in enumerate(shear):
    A = np.array([[s,0],[0,s]]).transpose()
    b1 = np.dot(A,x1)
    b2 = np.dot(A,x2)


    fig = pylab.figure(figsize=(5,5))
    ax = pylab.subplot(111)

    ax.plot([0,b1[0]],[0,b1[1]],lw=3.0,color='b',ls='--')
    ax.plot([0,b2[0]],[0,b2[1]],lw=3.0,color='g',ls='--')
    ax.plot([0,x1[0]],[0,x1[1]],lw=3.0,color='b')
    ax.plot([0,x2[0]],[0,x2[1]],lw=3.0,color='g')


    ax.set_xlim(-1,3)
    ax.set_ylim(-1,3)
    ax.grid()
    pylab.savefig('figures\\scale_'+str(i)+'.png',dpi=300,format='png',bbox_inches='tight')
    #pylab.show()