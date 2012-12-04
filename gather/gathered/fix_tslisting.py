from datetime import datetime

#--load new ts listing
f = open('ts_listing.csv','r')
dbkeys,sdates,edates = [],[],[]
header = f.readline()
for line in f:
    raw = line.strip().split(',')
    try:
        sdt = datetime.strptime(raw[8],'%d-%b-%Y')
        edt = datetime.strptime(raw[9],'%d-%b-%Y')
        dbkeys.append(raw[0])
        sdates.append(sdt)
        edates.append(edt)
    except:
        pass
f.close()

#--repair the dates
f = open('ts_listing_brokendate.csv','r')
f_out = open('temp.dat','w')
h = f.readline()
for line in f:
    raw = line.strip().split(',')
    if raw[0] in dbkeys:
        idx = dbkeys.index(raw[0])
        try:
            sdt = datetime.strptime(raw[8],'%Y-%m-%d')
            edt = datetime.strptime(raw[9],'%Y-%m-%d')
            sdt_new = datetime(year=sdates[idx].year,month=sdt.month,day=sdt.day)
            edt_new = datetime(year=edates[idx].year,month=edt.month,day=edt.day)        
            raw[8] = sdt_new.strftime('%d-%b-%Y')
            raw[9] = edt_new.strftime('%d-%b-%Y') 
            f_out.write(','.join(raw)+'\n')
        except:
            print 'could not cast dt for record ',raw[0]
    else:
        print 'record not found',raw[0]
f.close()
f_out.close()
        
