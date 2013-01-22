import os
import numpy as np
import pylab
import arrayUtil as au

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


#--run fieldgen with an input file
os.system('fieldgen.exe <fieldgen.in')

#--get and plot the realizations
files = os.listdir('reals')
nlay,ncol = 50,151
for i,f in enumerate(files):    
    array = au.loadArrayFromFile(nlay,ncol,'reals\\'+f)    
    fig = pylab.figure(figsize=(15,5))
    ax = pylab.axes((0.05,0.05,0.85,0.85))
    cax = pylab.axes((0.9,0.05,0.025,0.85))
    p = ax.pcolor(np.log10(np.flipud(array)))
    #p = ax.pcolor(np.flipud(array/array.max()))    
    #p = ax.pcolor((np.flipud(poro)))
    ax.set_xlim(0,ncol)
    ax.set_ylim(0,nlay)
    ax.set_xlabel('col')
    ax.set_ylabel('row')
    pylab.colorbar(p,cax=cax)
    ax.set_title('log10 hydraulic conductivity realization '+str(i+1))
    np.savetxt('reals\\'+f,array,fmt='%15.3e')   
    #break    
pylab.show()