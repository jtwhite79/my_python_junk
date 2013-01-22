import pylab
import shapefile

shape_name = 'polylines_active'
lines = shapefile.load_shape_list(shape_name)

fig = pylab.figure()
ax = pylab.subplot(111)
for line in lines:
    ax.plot(line[0,:],line[1,:],'k--')
pylab.show()
    
