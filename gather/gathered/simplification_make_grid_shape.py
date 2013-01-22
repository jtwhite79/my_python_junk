import numpy as np
import shapefile
import simple

rows = list(np.flipud(simple.grid.rows))
cols = list(simple.grid.cols)


wr = shapefile.Writer()
wr.field('row','N',20,5)
wr.field('column','N',20,5)
wr.field('ibound','N',10)
box = [[min(cols),min(rows),],\
    [min(cols),max(rows)],\
    [max(cols),max(rows)],\
    [max(cols),min(rows)],\
    [min(cols),min(cols)]]

wr.poly([box])
wr.record([len(rows)-1,len(cols)-1,0])
wr.save('shapes\\bounding_box')

wr = shapefile.Writer()
wr.field('row','N',20,5)
wr.field('column','N',20,5)
wr.field('ibound','N',10)

ibound = np.loadtxt('ref\\ibound_20.ref')

for i,row in enumerate(rows[:-1]):
    for j,col in enumerate(cols[:-1]):
        rec = [i+1,j+1,ibound[i,j]]
        lowerleft = [cols[j],rows[i+1]]
        upperleft = [cols[j],rows[i]]
        upperright = [cols[j+1],rows[i]]
        lowerright = [cols[j+1],rows[i+1]]

        box = [lowerleft,upperleft,upperright,lowerright,lowerleft]
        wr.poly(parts=[box],shapeType=5)
        wr.record(rec)

wr.save('shapes\\simple_grid_1')
                
