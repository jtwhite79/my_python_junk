#--the time series listing CSV from dbhydro
fname = 'ts_listing.csv'
f = open(fname,'r')
header = f.readline().strip().split(',')
str = ''
for i,line in enumerate(f):
    raw = line.strip().split(',')
    str += raw[0]+'/'
    if (i+1) % 200 == 0:
        print str        
print str    