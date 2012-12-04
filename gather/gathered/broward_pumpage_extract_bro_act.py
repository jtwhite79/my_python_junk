import shapefile

shapename = '..\\_gis\\shapes\\pws_combine'
shp = shapefile.Reader(shapename)
fieldnames = shapefile.get_fieldnames(shapename)
dril_idx = fieldnames.index('DRIL_YEAR')
util_idx = fieldnames.index('UTILITY')
f = open('boward_active_1978.dat','w')
line = ','.join(fieldnames[:10])
f.write(line+'\n')
    
for i in range(shp.numRecords):
    rec = shp.record(i)
    if 'BROWARD' in rec[util_idx].upper() and int(rec[dril_idx]) < 1978:
        line = ','.join(rec[:10])
        f.write(line+'\n')
f.close()    


