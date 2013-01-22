import numpy as np
import pylab


def func(x):
    return 0.5*x**3 + 10*x

def secant(x0,y0,x1,y1,func,tol=0.0001):
    xs,ys = [],[]
    for it in range(10):
        xi = x1 - y1*((x1-x0)/(y1-y0))
        yi = func(xi)
        xs.append([x0,x1,xi])
        ys.append([y0,y1,yi])
        x0 = x1
        y0 = y1
        y1 = yi
        x1 = xi              
        if yi < tol:
            break
    return xs,ys


x0 = 70.0
y0 = func(x0)

x1 = x0 - 10.0
y1 = func(x1)

xs,ys = secant(x0,y0,x1,y1,func)

x = np.linspace(-10,75,100)
vfunc = np.vectorize(func)

y = vfunc(x)
fig_num = 1
for xss,yss in zip(xs,ys):
    fig = pylab.figure(figsize=(3,3))
    ax = pylab.subplot(111)
    #ax.grid()
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    ax.plot(x,y,'b-',lw=0.5)
    ax.plot(xss[0],yss[0],'k.',ms=3.0)
    ax.plot(xss[1],yss[1],'k.',ms=3.0)
    pylab.savefig('figures\\sec_'+str(fig_num)+'.png',dpi=300,format='png',bbox_inches='tight')
    fig_num += 1
    ax.plot([xss[0],xss[2]],[yss[0],0],'r-',lw=.5)
    pylab.savefig('figures\\sec_'+str(fig_num)+'.png',dpi=300,format='png',bbox_inches='tight')
    fig_num += 1
    ax.plot(xss[2],0,'k.',ms=3.0)
    pylab.savefig('figures\\sec_'+str(fig_num)+'.png',dpi=300,format='png',bbox_inches='tight')
    fig_num += 1
    ax.plot([xss[2],xss[2]],[0,yss[2]],'k--',lw=.5)
    pylab.savefig('figures\\sec_'+str(fig_num)+'.png',dpi=300,format='png',bbox_inches='tight')
    fig_num += 1
    
    #pylab.show()
    #pass