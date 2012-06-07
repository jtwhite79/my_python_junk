#--2d real array utilities 
#--for reading, writing and plotting
#--ASCII 2-D MODFLOW real arrays

#--libraries
import numpy as np
import os
import sys
import pylab
from pylab import *                      
from matplotlib import colors, cm
import time

import blnUtil
reload(blnUtil)


def mapCellsArray(nrow,ncol,row_col_val):
    array = np.zeros((nrow,ncol)) - 999.
    try: 
        vals = np.shape(row_col_val)[0]
        for val in range(0,vals):
            array[row_col_val[val,0]-1,row_col_val[val,1]-1] = row_col_val[val,2]
    except:
        vals = len(row_col_val)
        for val in range(0,vals):
            array[row_col_val[val][0]-1,row_col_val[val][1]-1] = row_col_val[val][2]             
    return array
        

def mapBndCellsArray(nrow,ncol,bndcells,**kwargs):	
	try:
		parm = kwargs['parm']
	except:
		parm = ''
	array = np.zeros((nrow,ncol),dtype='double')-1.0e+30
	for cells in range(0,len(bndcells)): 
		if cmp(parm,'stage') == 0:
			array[(bndcells[cells].row)-1,(bndcells[cells].column)-1] = bndcells[cells].stage
		elif cmp(parm,'rate') == 0:
			array[(bndcells[cells].row)-1,(bndcells[cells].column)-1] = bndcells[cells].rate
		elif cmp(parm,'concen') == 0:
			array[(bndcells[cells].row)-1,(bndcells[cells].column)-1] = bndcells[cells].concen
		elif cmp(parm,'cond') == 0:
			array[(bndcells[cells].row)-1,(bndcells[cells].column)-1] = bndcells[cells].cond
		elif cmp(parm,'int') == 0:
			array[(bndcells[cells].row)-1,(bndcells[cells].column)-1] = 1
		else:		 
			try:
				array[(bndcells[cells].row)-1,(bndcells[cells].column)-1] = bndcells[cells].stage
			except:
				try:
					array[(bndcells[cells].row)-1,(bndcells[cells].column)-1] = bndcells[cells].rate
				except:
					try:
						array[(bndcells[cells].row)-1,(bndcells[cells].col)-1] = bndcells[cells].concen
					except:
						raise TypeError 
	return array




def loadArrayFromFile(nrow,ncol,file):
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



def ref2grd(file,ref,nrow,ncol,offset,delt,nodata=-999):
    f = open(file,'w')
    f.write('ncols '+str(ncol)+'\n')
    f.write('nrows '+str(nrow)+'\n')
    f.write('xllcorner '+str(offset[0])+'\n')
    f.write('yllcorner '+str(offset[1])+'\n')
    f.write('cellsize '+str(delt)+'\n')
    f.write('nodata_value -9999\n')
    writeArrayToFile(ref,f,nWriteCol=ncol) 
    f.close()
    return


def loadgrdfromfile(file,dtype='float'):
    f = open(file,'r')
    ncol = int(f.readline().strip().split()[-1])
    nrow = int(f.readline().strip().split()[-1])
    offset = [float(f.readline().strip().split()[-1])]
    offset.append(float(f.readline().strip().split()[-1]))
    gridDim = float(f.readline().strip().split()[-1])
    noData = float(f.readline().strip().split()[-1])
    f.close()
    array = np.loadtxt(file,dtype=dtype,skiprows=6)
    assert array.shape[0] == nrow
    assert array.shape[1] == ncol
    return nrow,ncol,offset,gridDim,noData,array


def writeArrayToFile(array,file,**kwargs):
	'''
	write 2-d array to file
	nWriteCol(int) = number of columns in output file array
	oFormat(str) = output format ex: {0:12.4E}
	file(str) = path and filename
	'''
	
	#--get keyword arguments
	try:
		nWriteCol = kwargs['nWriteCol']
	except:
		nWriteCol = 10
	
	try:
		oFormat = kwargs['oFormat']
		if len(oFormat) == 1:
			if cmp(oFormat,'i') == 0 or cmp(oFormat,'I') == 0:
				oFormat = '{0:3.0f}'
	except:
		oFormat = '{0:14.6E}'
	
	
	assert len(np.shape(array)) == 2
	nrow,ncol = np.shape(array)
	#--check for line return flag at end each column
	if ncol%nWriteCol == 0:
		lineReturnFlag = False
	else:
		lineReturnFlag = True	
		
	#--try to open file, if fail, file is an open fileobj		
	try:
		file_out = open(file,'w')
		openFlag = True
	except:
		file_out = file
		openFlag = False
			
	#--write the array						
	for a in range(0,nrow):
		for b in range(0,ncol):
			try:
				file_out.write(oFormat.format(float(array[a][b])))
			except:
				print 'NAN at row,col: ',a,b,array[a][b]
				sys.exit()
			if (b+1)%nWriteCol == 0.0 and b != 0:
				file_out.write('\n')
		if lineReturnFlag == True:
			file_out.write('\n')
	if openFlag == True:		
		file_out.close()
	return True




def plotArray(array,rowDim,colDim,**kwargs):
	'''
	generic plot of 2d array with grid
	'''
	
	#--get keyword arguments
	
	
	
	try:
		title = kwargs['title']
	except:
		title = ''

	try:
		cBarLoc,cBarLabel = kwargs['cBarLoc'],kwargs['cBarLabel']
	except:
		cBarLoc,cBarLabel = [0.25,0.025,0.5,0.025],''
	try:
	    cbticks = kwargs['cbticks']
	except:
	    cbticks = None
	
	
	try:
		xOff,yOff = kwargs['offset'][0],kwargs['offset'][1]
	except:
		xOff,yOff = 0.0,0.0		
	try:
		max = kwargs['max']
	except:
		max = np.max(array)
	
	try:
		min = kwargs['min']
	except:
		min = np.min(array)
	#print 'min,max',min,max
	try:
		figuresize = kwargs['figuresize']
	except:
		if np.shape(array)[0] > np.shape(array)[1]:
			figuresize = (8.5,11)
		else:
			figuresize = (11,8.5)
	#print 'figsize',figuresize
	try:
		gridFlag = kwargs['gridFlag']
	except:
		gridFlag = False
		
	try:
		outputFlag = kwargs['outputFlag']
	except:
		try:
			outputFlag = kwargs['output']
		except:
			outputFlag = 'show'
	
	cmap='jet'
	
	#--get contour array
	try:
		con_array = kwargs['con_array']
	except:
		con_array = []
		
	#--get bln lines and index array
	try:
		blnlines = kwargs['bln']
		blnPoints,blnIdx = blnUtil.loadBlnFile(blnlines)
	except:
		blnPoints = []
		blnIdx = []
	
	#-- get generic points to plot
	try:
		genPoints = kwargs['gpts']
	except:
		genPoints = []
	
	try:
	    fig = kwargs['fig']
	except:
	    fig = pylab.figure(figsize=(figuresize))
	
	try:
	    ax = kwargs['ax']
	except:
	    ax = pylab.subplot(111)
	
	
	
						
	#--array params
	nrow,ncol = np.shape(array)
	#print xOff,yOff
	#print colDim,rowDim
	#--set x and y dimensions		
	try:	
		x = np.arange(xOff,xOff+(ncol*colDim)+colDim,colDim)
		#print x.shape
		xmin,xmax = xOff,xOff+(ncol*colDim)
	except:
		try:			
			f_in = open(colDim,'r')
			x = np.zeros((1),dtype='float')
			for line in f_in:
				raw = line.split()
				for a in range(0,len(raw)):
					x = np.append(x,float(raw[a]))
			x = np.delete(x,[0])
			xmin,xmax = np.min(x),np.max(x) 						
		except:
			print colDim.shape,ncol+1
			assert np.shape(colDim)[0] == ncol
			x = colDim
			xmin,xmax = np.min(x),np.max(x)
			
	try:
		y = np.arange(yOff,yOff+(nrow*rowDim),rowDim)
		#print y[0],y[-1]
		ymin,ymax = yOff,yOff+(nrow*rowDim)
	except:
		try:			
			f_in = open(rowDim,'r')
			y = np.zeros((1),dtype='float')
			for line in f_in:
				raw = line.split()
				for a in range(0,len(raw)):
					y = np.append(y,float(raw[a]))
			y = np.delete(y,[0])
			ymin,ymax = np.min(y),np.max(y) 						
		except:
			assert np.shape(rowDim)[0] == nrow
			y = rowDim
			ymin,ymax = np.min(y),np.max(y)
	
	
				
	array = np.flipud(array)
	#fig = figure(figsize=figuresize)
	#ax = subplot(1,1,1)
	ax.set_title(title)		
		
			
	#--define meshgrid
	X,Y = np.meshgrid(x,y)
	
	#--set up color map
	numColors = 128
	palette = cm.get_cmap(cmap,numColors)
	palette.set_over('w')
	palette.set_under('w')
	palette.set_bad('w')
	
	
	#--mask
#	array = ma.masked_where(array<min,array)
#	array = ma.masked_where(array>max,array)
	
	#-- plot array
	
	
	c = ax.pcolor(X,Y,array,vmin=min,vmax=max,cmap=palette,alpha=0.75,edgecolors='None')
	
	#-- plot grid if gridFlag
	if gridFlag:
		row = 0
		while row < nrow:
			plot([xmin,xmax],[y[row],y[row]],'k-',linewidth=0.1)
			row += 1	
		col = 0
		while col < ncol:
			plot([x[col],x[col]],[ymin,ymax],'k-',linewidth=0.1)
			col += 1
	#print xmin,xmax,ymin,ymax
	
	
	#--plot BLN lines
	if len(blnPoints) > 0:
		for a in range(1,np.shape(blnIdx)[0]):
			#print blnIdx[a-1]
			ax.plot(blnPoints[blnIdx[a-1]:blnIdx[a],0],blnPoints[blnIdx[a-1]:blnIdx[a],1],'k-',lw=2.0)
				
	#--plot generic points
	if len(genPoints) > 0:
	
		#try:
		ax.plot(genPoints[:,0],genPoints[:,1],'k+')
		#except:
		#	print 'error plotting generic points...'
	
	#--plot contours
	if len(con_array) > 0:
		cs = ax.contour(x[:-1],y[:-1],con_array,colors='k')
		ax.clabel(cs,inline=1,)
		
	#cax=axes(cBarLoc)
	#fig.colorbar(c,cax=cax,orientation='horizontal',ticks=cbticks)                                       
	cax = fig.colorbar(c,alpha=0.75) 
	#cax.ax.set_ylabel('log10(kh [m/d])')                                      
	
	
	ax.set_xlim(xmin,xmax)
	ax.set_ylim(ymin,ymax)

	if outputFlag == 'save':
		if title == '':
			title = str(time.time())
		plotname=title+'.png'
		savefig(plotname,orientation='portrait',format='png',dpi=150)
	elif outputFlag == 'show':
		show()
	elif outputFlag == None:
		#print 'no output produced...'
		return ax
	else:
		try:
			fmt = outputFlag.split('.')[-1]
  		
		except:
			print 'unable to parse outputFlag for output format type: ',outputFlag
		savefig(outputFlag,orientation='portrait',format=fmt,dpi=150)
	return
			