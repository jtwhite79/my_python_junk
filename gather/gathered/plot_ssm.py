import arrayUtil as au
import ssmClass
reload(au)
reload(ssmClass)
nrow,ncol = 301,501

ibnd_l1 = au.loadArrayFromFile(nrow,ncol,'ibound_l1.ref')

idx = np.argwhere(ibnd_l1 == -1)
print np.shape(idx)


#f = open('simple.ssm','w')
cells1 = []


map1 = au.mapBndCellsArray(nrow,ncol,cells1,parm='concen')
map2 = au.mapBndCellsArray(nrow,ncol,cells2,parm='concen')

au.plotArray(map1,500,500,output=None)
au.plotArray(map2,500,500,output=None)
#f.close()