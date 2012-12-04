import copy
import shapefile

def intersect(well_interval,layer_elevs):
    lay,frac = [],[]
    for i in range(len(layer_elevs[:-1])):
        layer_interval = [layer_elevs[i],layer_elevs[i+1]]
        olap = overlap(well_interval,layer_interval)
        #f = olap / (layer_interval[0] - layer_interval[1])
        f = olap / (well_interval[0] - well_interval[1])
        if f > 0.0:
            lay.append(i)
            frac.append(f)
        #print well_interval,layer_interval,olap
    return lay,frac        

def overlap(interval1,interval2):
    olap = min(interval1[0],interval2[0]) - max(interval1[1],interval2[1])
    if olap > 0.0 :
        return olap
    else:
        return 0.0



layer_names = ['H_bot','Q5_bot','Q4_bot','Q3_bot','Q2_bot','Q1_bot','T3_bot','T2_bot','T1_bot']

shapename = '..\\_gis\\scratch\\pws_grid_join'
shapes,records = shapefile.load_as_dict(shapename)
shp = shapefile.Reader(shapename)
rlist = shp.records()

wr = shapefile.writer_like(shapename)
wr.field('int_layer',fieldType='C',size=10)
wr.field('int_frac',fieldType='C',size=50)

for i,shape in enumerate(shapes):
    if '187' in records['PERM_NO'][i]:
        print records['PERM_NO'][i]
    try:
        top,bot = float(records['WELL_CAS'][i]),float(records['WELL_DEP'][i])
    except ValueError:
        top = 1.0e+10
        bot = 1.0e+10
    if top != bot:             
        ls = float(records['top_smooth'][i])
        interval = [ls-top,ls-bot]
        layer_elevs = [ls]
        for l in layer_names:
            layer_elevs.append(float(records[l][i]))
        lay,frac = intersect(interval,layer_elevs)
        rec = copy.deepcopy(rlist[i])
        lay_str,frac_str = '',''
        for l,f in zip(lay,frac):        
            
            x = shape.points[0][0]
            y = shape.points[0][1]           
            lname = layer_names[l].split('_')[0]            
            lay_str += ' '+lname
            frac_str += ' {0:3.2f}'.format(f)
        rec.append(lay_str)
        rec.append(frac_str)
        wr.poly([shape.points],shapeType=shape.shapeType)
        wr.record(rec)
    else:
        print 'well case depth == well total depth',records['DPEP_WEL'][i]

wr.save('..\\_gis\\scratch\\pws_layers')


