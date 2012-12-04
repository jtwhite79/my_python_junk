import shapefile
import pestUtil

#--load the master sites spreadsheet to get x,y,datum info
fname = 'spreadsheet_data\\broward_sites_master.csv'
f = open(fname,'r')
header = f.readline().strip().split('|')
#--create a new shapefile instance
wr_27 = shapefile.Writer()
wr_83 = shapefile.Writer()
#--just make all field text
for h in header:
    wr_27.field(h,fieldType='C',size=50)
    wr_83.field(h,fieldType='C',size=50)
site_nos = []
for line in f:
    raw = line.strip().split('|')
    site_no = raw[1]
    lat = float(raw[5])
    long = float(raw[6])
    datum = raw[7]        
    if site_no not in site_nos: 
        if datum.upper() == 'NAD27':
            wr_27.poly([[[long,lat]]],shapeType=shapefile.POINT)
            wr_27.record(raw)
        elif datum.upper() == 'NAD83':
            wr_83.poly([[[long,lat]]],shapeType=shapefile.POINT)
            wr_83.record(raw)
        else:
            raise TypeError('unrecognized datum:'+str(datum))
        site_nos.append(site_no)
wr_27.save('..\\_gis\\scratch\\broward_nwis_27')    
wr_83.save('..\\_gis\\scratch\\broward_nwis_83')
        



