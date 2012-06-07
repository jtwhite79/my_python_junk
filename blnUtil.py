#--BLN utilities



import numpy as np
import sys
import os


def loadBlnFile(file):
	
	data = np.array([0,0,0])
	dataIdx = np.array([0])
	f_in = open(file,'r')
	while True:
		try:
			points = int(f_in.readline().strip('\n').split(',')[0])
		except:
			break				
		for a in range(0,points):
			point = f_in.readline().strip('\n').split(',')
			data = np.vstack((data,[float(point[0]),float(point[1]),float(point[2])]))
		dataIdx = np.append(dataIdx,dataIdx[-1]+points)
	data = np.delete(data,0,axis=0)
	return(data,dataIdx) 
	

			
		
		
		