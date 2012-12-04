import os
import shapefile
import pestUtil

'''add two numeric attributes to the nwis sites shape
 - length of water level record
 - length of concentration record
 add two text attributes to the nwis sites shape
 - path to navd ts plot
 - path to conc ts plot
 splits the nwis shapefile into groundwater and surfacewater sites

'''

def parse_smp_filename(filename):
    raw = filename.split('.')[:-1]
    parsed = {'agency':raw[0],'site_no':raw[1],'name':raw[2],'param':raw[3]}
    return parsed

def build_plotname(filename):
    raw = filename.split('.')
    raw[-1] = 'png'
    return '.'.join(raw)

#--processed smp directories
navd_dir = 'smp_waterlevel_navd\\'
conc_dir = 'smp_rel_conc\\'

navd_files = os.listdir(navd_dir)
conc_files = os.listdir(conc_dir)

navd_attribs = []
for file in navd_files:
    navd_attribs.append(parse_smp_filename(file))

conc_attribs = []
for file in conc_files:
    conc_attribs.append(parse_smp_filename(file))

#--build plot names
navd_plt_dir = 'png\\navd\\'
conc_plt_dir = 'png\\conc\\'
navd_pltnames = []
for file in navd_files:
    pname = build_plotname(file)
    if os.path.exists(navd_plt_dir+pname):
        navd_pltnames.append(navd_plt_dir+pname)
    else:
        navd_pltnames.append('')
conc_pltnames = []
for file in conc_files:
    pname = build_plotname(file)
    if os.path.exists(conc_plt_dir+pname):
        conc_pltnames.append(conc_plt_dir+pname)
    else:
        conc_pltnames.append('')

#--load the shapefile
shapename = '..\\_gis\\shapes\\broward_nwis_sites'
#shapes,records = shapefile.load_as_dict(shapename)
site_no_idx = 2
site_type_idx = 4
shp = shapefile.Reader(shapename)
shapes = shp.shapes()
records= shp.records()

#--new shape instance for gw sites
wr_gw = shapefile.writer_like(shapename)
wr_gw.field('navd_len',fieldType='N',size=10,decimal=0)
wr_gw.field('navd_pth',fieldType='C',size=100)
wr_gw.field('conc_len',fieldType='N',size=10,decimal=0)
wr_gw.field('conc_pth',fieldType='C',size=100)


#--new shape instance for gw sites
wr_sw = shapefile.writer_like(shapename)
wr_sw.field('navd_len',fieldType='N',size=10,decimal=0)
wr_sw.field('navd_pth',fieldType='C',size=100)
wr_sw.field('conc_len',fieldType='N',size=10,decimal=0)
wr_sw.field('conc_pth',fieldType='C',size=100)




#--for each shape, look for matching records
for record,shape in zip(records,shapes):
    #site_no = records['site_no'][i]
    site_no = record[site_no_idx]
    
    site_type = record[site_type_idx]

    #--look for a matching navd smp file
    record.append(-1)
    record.append('')
    for filename,attrib,pltname in zip(navd_files,navd_attribs,navd_pltnames):
        if attrib['site_no'] == site_no:
            smp = pestUtil.smp(navd_dir+filename,load=True,pandas=True)
            record[-2] = smp.records.shape[0]
            record[-1] = pltname
            break
    
    #--look for a matching conc smp file
    record.append(-1)
    record.append('')
    for filename,attrib,pltname in zip(conc_files,conc_attribs,conc_pltnames):
        if attrib['site_no'] == site_no:
            smp = pestUtil.smp(conc_dir+filename,load=True,pandas=True)
            record[-2] = smp.records.shape[0]
            record[-1] = pltname
            break
    if site_type.upper().startswith('GW'):
        wr_gw.poly([shape.points],shapeType=shape.shapeType)
        wr_gw.record(record)

    elif site_type.upper().startswith('ST'):
        wr_sw.poly([shape.points],shapeType=shape.shapeType)
        wr_sw.record(record)
    else:
        print 'Unrecognized site type:',site_type

wr_gw.save('..\\_gis\\scratch\\broward_nwis_sites_reclen_gw')
wr_sw.save('..\\_gis\\scratch\\broward_nwis_sites_reclen_sw')



