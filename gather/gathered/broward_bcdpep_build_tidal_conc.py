import numpy as np
import shapefile

shapename = '..\\_gis\\scratch\\sw_reaches_coastal_conc'
records = shapefile.load_as_dict(shapename,loadShapes=False)
print records.keys()
conc_key = 'max_relcon'
reach_key = 'reach'
tidal_key = 'stage_rec'
f = open('BCDPEP_reach_conc.dat','w',0)
f.write('source_reach,rel_conc\n')
for conc,reach,tidal in zip(records[conc_key],records[reach_key],records[tidal_key]):
    if 'COASTAL' in tidal.upper():
        f.write(str(int(float(reach)))+','+str(conc)+'\n')
f.close()

