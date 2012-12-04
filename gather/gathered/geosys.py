#--script to process geosys data file for Broward Co.

import re
import sys

alf = re.compile('[A-Z]')

#--define a dictionary of relavent formations
formations = {'090UDSC':'undiff','111LKFL':'lake flirt marl',
							'112FTMP':'fort thompson','112KLRG':'key largo',
							'112MIMI':'miami lmst','122HTRN':'hawthorne',
							'112ANSS':'anastasia','122TMIM':'tamiami',
							'112CLSCR':'caloosa','123SWNN':'suwanne',
							'124AVPK':'avon park','124OLDM':'oldsmar',
							'000NOSM':'no sample','000NOPK':'no pick',
							'121PCPC':'plio-pliest'}

noint = 0
lcount = 0

f_in = open('pinellas.dat','r')
f_out = open('FGS_Dade_Formations.csv','w')

tops,bottoms = [],[]

##--write header line to output
#f_out.write('number,x,y,')
#for fcode,fname in formations.iteritems():
#	f_out.write(fname+'-top,'+fname+'-bottom,')

#for f in range(0,len(formations)):
#	f_out.write('top,bottom,')
#	tops.append('')
#	bottoms.append('')	
#f_out.write('\n')

for line in f_in:  
	lcount += 1
	try:
		key = int(line[0])
	except:
		key = 0
	keys = formations.keys()
	#--look for header lines
	if key == 1:
		#for f in range(0,len(formations)):
			#f_out.write(tops[f]+','+bottoms[f]+',')
			#tops[f],bottoms[f] = '',''		
		thisNumber = line[1:6].strip(' ')
		thisLat = alf.sub('',line[22:29]).strip(' ')
		thisLong = line[29:35].strip(' ')	
		print thisNumber,thisLat,thisLong
		f_out.write(thisNumber+','+thisLat+','+thisLong+'\n')
#	#--convert from deg,min,sec to dec deg
#		try:
#				thisDecLat = float(thisLat[0:2])+(float(thisLat[2:4])/60.0)\
#					+(float(thisLat[4:6])/60.0/60.0)
#				thisDecLong = float(thisLong[0:2])+(float(thisLong[2:4])/60.0)\
#					+(float(thisLong[4:6])/60.0/60.0)
#				f_out.write('\n'+thisNumber+','+str(thisDecLat)+',-'+str(thisDecLong)+',') 
#				#print thisDecLat,thisDecLong  
#		except:
#				print thisNumber,thisLat,thisLong  
 				
#	#--look for formation picks - line starts with '4'
#	elif key == 4:
#		#--write number lat long
##		print thisNumber,thisDecLat,thisDecLong
#		
#		thisTop = line[6:12].strip(' ')
#		thisBottom = line[13:19].strip(' ')
#		thisFrm = line[19:30].strip(' ').strip('\n')			
#		for f in range(0,len(formations)):
#			if cmp(thisFrm,keys[f]) == 0:
#				tops[f] = thisTop
#				bottoms[f] = thisBottom
					
f_out.close()