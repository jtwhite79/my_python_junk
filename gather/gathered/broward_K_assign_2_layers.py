import copy
import shapefile

def intersect(well_interval,layer_elevs):
    lay,frac = [],[]
    for i in range(len(layer_elevs[:-1])):
        layer_interval = [layer_elevs[i],layer_elevs[i+1]]
        olap = overlap(well_interval,layer_interval)
        f = olap / (layer_interval[0] - layer_interval[1])
        if f > 0.0:
            lay.append(i)
            frac.append(f)
        print well_interval,layer_interval,olap
    return lay,frac        

def overlap(interval1,interval2):
    olap = min(interval1[0],interval2[0]) - max(interval1[1],interval2[1])
    if olap > 0.0 :
        return olap
    else:
        return 0.0



layer_names = ['Q5_bot','Q4_bot','Q3_bot','Q2_bot','Q1_bot','T3_bot','T2_bot','T1_bot']

shapename = '..\\_gis\\scratch\\all_K_locations_grid_join'
shapes,records = shapefile.load_as_dict(shapename)
shp = shapefile.Reader(shapename)
rlist = shp.records()
#shp = shapefile.Reader(shapename)
#num_records = shp.numRecords
#header = shp.dbfHeader()
#top_idx,bot_idx,ls_idx = None,None,None
#for i,h in header:
#    if h[0] == 'top_smooth':
#        top_idx = i

#layer_idx = []
#for l in layer_names:
#    layer_idx.append(header.index(l))

wr = shapefile.writer_like(shapename)
wr.field('k_layer',fieldType='C',size=50)
wr.field('k_frac',fieldType='C',size=50)

f_out = open('k_locs_bylayer.dat','w')
f2_out = open('k_locs.dat','w')
layer_entries = {}
for i,shape in enumerate(shapes):
    x = shape.points[0][0]
    y = shape.points[0][1]
    k = float(records['K_ftday'][i])
    lname = 'k_'+str(i)
    f2_out.write(lname+'  {0:15.6e}  {1:15.6e} {2:02.0f}  {3:15.6e}\n'.format(x,y,1,k))
    top,bot = float(records['top'][i]),float(records['bot'][i])
    ls = float(records['top_layeri'][i])
    interval = [ls-top,ls-bot]
    layer_elevs = [ls]
    for l in layer_names:
        layer_elevs.append(float(records[l][i]))
    if max(layer_elevs) == 0 and min(layer_elevs) == 0:
        print 'well outside of grid'
    else:
        lay,frac = intersect(interval,layer_elevs)
        lay_str,frac_str = '',''
        for l,f in zip(lay,frac):
            if f > 0.25 or len(lay) == 1:
                            
                lname = layer_names[l].split('_')[0]
                line = lname+'_{0:03.0f}'.format(i+1)+'  {0:15.6e}  {1:15.6e} {2:02.0f}  {3:15.6e}\n'.format(x,y,1,k)
                if lname in layer_entries.keys():
                    layer_entries[lname].append(line)
                else:
                    layer_entries[lname] = [line]                
                f_out.write(line)
                lay_str = lname.split('_')[0]
                frac_str = '{0:1.2f}'.format(f)
                rec = copy.deepcopy(rlist[i])
                rec.append(lay_str)
                rec.append(frac_str)
                wr.poly([shape.points],shapeType=shape.shapeType)
                wr.record(rec)

f_out.close()    
f2_out.close()
wr.save('..\\_gis\\scratch\\all_K_locations_layers')
out_dir = 'k_locs\\'
for lname,lines in layer_entries.iteritems():
    f = open(out_dir+lname+'.dat','w')
    for line in lines:
        f.write(line)
    f.close()
