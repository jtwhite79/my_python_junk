import urllib

source1="http://my.sfwmd.gov/dbhydroplsql/show_dbkey_info.show_keywordtab_info?v_dbkey="

filename="output.xy"
f=open(filename,'w')

dbkeyfile=open('dbkeys.txt')
print 'opened: dbkeys.txt'

for dbkey in dbkeyfile:
	
	line = dbkey[0:5]
	
	#get the data from the url
	print 'processing dbkey: ',dbkey
	source=source1+str(dbkey[0:5])
	data=urllib.urlopen(source).readlines()
	
	for i in range(0,len(data)):
		if data[i].find('X Coordinate:') > 0: 
			line=line + ' ' + data[i+1][0:9]
		if data[i].find('Y Coordinate:') > 0:
			line=line + ' ' + data[i+1][0:9] + '\n'
				
	f.write(line)
	print line
		
dbkeyfile.close()
f.close()
