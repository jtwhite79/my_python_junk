import shapefile

#--first load the shapefile and attributes
shapename = '..\\_gis\\shapes\\pws_combine'
shapes,records = shapefile.load_as_dict(shapename)

wr = shapefile.Writer()
wr.field('well_name',fieldType='C',size=50)
wr.field('usgs_name',fieldType='C',size=50)
wr.field('top',fieldType='N',size=10,decimal=2)
wr.field('bot',fieldType='N',size=10,decimal=2)
wr.field('T',fieldType='N',size=20,decimal=2)
wr.field('K',fieldType='N',size=20,decimal=2)

#--load the specific capacity data - util_well_name usgs_supply_well_number depth_interval transmissivity
spec_file = 'fish1987\\specific_capacity_T_table2.txt'
f = open(spec_file,'r')
while True:
    line = f.readline()
    if line == '':
        break
    #--read the util name
    util_name = line.strip()
    #--read the wells
    wells = []
    while True:
        line = f.readline()
        if len(line.strip().split()) == 0:
            break
        raw = line.strip().split()
        top,bot = raw[2].split('-')
        top = float(top)
        bot = float(bot)
        t = float(raw[3].replace(',',''))
        k = t / (bot - top)
        well = [raw[0],raw[1],top,bot,t,k]
        #well = {'name':raw[0],'usgs':raw[1],'top':top,'bot':bot,'t':t,'k':k}
        #--try to find the record in the shape attributes
        for util,wname,shape in zip(records['UTILITY'],records['WELL_NO'],shapes):
            if util.lower() == util_name.lower() and wname.lower() == well[0].lower():
                wr.poly([shape.points],shapeType=shape.shapeType)
                wr.record(well)
wr.save('..\\_gis\\scratch\\pws_K_locations')    
f.close()

#--make a shapefile for the APT data from table 4 in fish 1987
wr = shapefile.Writer()
wr.field('usgs_name',fieldType='C',size=50)
wr.field('lat',fieldType='N',size=50,decimal=20)
wr.field('long',fieldType='N',size=50,decimal=20)
wr.field('top',fieldType='N',size=10,decimal=2)
wr.field('bot',fieldType='N',size=10,decimal=2)
wr.field('T',fieldType='N',size=20,decimal=2)
wr.field('K',fieldType='N',size=20,decimal=2)



#--load the specific capacity data - util_well_name usgs_supply_well_number depth_interval transmissivity
k_file = 'fish1987\\APT_table4.txt'
f = open(k_file,'r')
records = []
for line in f:
    raw = line.strip().split()
    #--dms to dd
    latd = float(raw[1][0:2])
    latm = float(raw[1][2:4])
    lats = float(raw[1][4:6])
    lat = latd + ((latm + (lats / 60.0)) / 60.0)

    longd = float(raw[2][0:3])
    longm = float(raw[2][3:5])
    longs = float(raw[2][5:7])
    long = longd + ((longm + (longs / 60.0)) / 60.0)
    
    top = float(raw[6].split('-')[0])
    bot = float(raw[6].split('-')[1])
    t = float(raw[10].replace(',',''))
    k = float(raw[11].replace(',',''))
    rec = [raw[0][:-1],lat,-1.0*long,top,bot,t,k]
    records.append(rec)
    wr.poly([[[rec[2],rec[1]]]],shapeType=shapefile.POINT)
    wr.record(rec)
wr.save('..\\_gis\\scratch\\apt_K_locations_decimalDegrees')   



                        




