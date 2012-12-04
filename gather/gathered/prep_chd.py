#--must manually input MXBND after file is written - too lazy


import numpy as np
import MFPackageReader_explicit as mf
import arrayUtil as au


def write_file_header(header,outfile):
	try:
		for line in range(0,len(header)):
			outfile.write(header[line])
	except:
		print 'error writing header...'
		raise IOError
	return

nrow,ncol = 301,501
sp = 100

	
fileNew = 'bro.chd'
f_out = open(fileNew,'w')
offset = [728600.,577350.]

newMXBND = -1e+30
orgMXBND = -1e+30

#write_file_header()

cont = True
count = 0

ibnd_l1 = au.loadArrayFromFile(nrow,ncol,'ref\\ibound_l1.ref')
ibnd = au.loadArrayFromFile(nrow,ncol,'ref\\ibound.ref')

l1_idx = (np.argwhere(ibnd_l1==-1))+1
idx = (np.argwhere(ibnd==-1))+1

print np.shape(l1_idx),np.shape(idx)

chd_stage = 0.0
newCells = []
for cell in range(0,np.shape(l1_idx)[0]):
    #print l1_idx[cell,0],l1_idx[cell,1]
    newCells.append(mf.MODFLOW_HDF('HDF',1,l1_idx[cell,0],l1_idx[cell,1],[chd_stage,chd_stage]))

for ilay in range(2,9):

    for cell in range(0,np.shape(idx)[0]):
        #print idx[cell,0],idx[cell,1]
        newCells.append(mf.MODFLOW_HDF('HDF',ilay,idx[cell,0],idx[cell,1],[chd_stage,chd_stage]))   
         
print len(newCells)         
mf.write_sp(1,len(newCells),f_out,newCells)
f_out.close()


#while cont:
#	kper,nbnd,orgCells,cont = thisBnd.next()
#	if nbnd > orgMXBND:
#		orgMXBND = nbnd
#	if cont is False: break
#	newCells = []
#	if nbnd >= 0:
#		for cell in range(0,len(orgCells)):
#			thisCell = orgCells[cell]
#			count += 1
#			newrows = (np.argwhere(rowmapArray == thisCell.row-1))+1
#			newcols = (np.argwhere(colmapArray == thisCell.column-1))+1 
#			newrowcount = np.shape(newrows)[0]
#			newcolcount = np.shape(newcols)[0]
##			newcond = thisCell.cond/2.0
#			newcond = thisCell.cond
#			for col in range(0,newcolcount):
#				for row in range(0,newrowcount):
#					newCells.append(mf.MODFLOW_HDF(thisCell.layer,newrows[row,1],newcols[col,1],[thisCell.stage,newcond,]))#thisCell.rbot]))
##		if len(orgCells) > 0:	
##			au.plotArray(au.map_bndcells_array(nrowOrg,ncolOrg,orgCells),150.0,150.0,max=5.0,gridFlag=True,offset=offset)		
##			au.plotArray(au.map_bndcells_array(nrowNew,ncolNew,newCells),150.0,'colDimNew.dat',max=5.0,gridFlag=True,offest=offset) 
#		print len(newCells)
#		mf.write_sp(kper,len(newCells),f_out,newCells)
#		if len(newCells) > newMXBND:
#				newMXBND = len(newCells)
#	else:
#		mf.write_sp(kper,nbnd,f_out,newCells)
#print newMXBND,orgMXBND
#f_out.close()