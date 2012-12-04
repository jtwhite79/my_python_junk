import arrayUtil as au
import MFPackageReader_explicit as mf

nrow,ncol = 301,501

mfobj = mf.MODFLOW_HDFPackage('bro.chd')
kper,nbnd,cells,succes = mfobj.next()
print len(cells)
#au.plotArray(au.map_bndcells_array(nrow,ncol,cells),500,500)
