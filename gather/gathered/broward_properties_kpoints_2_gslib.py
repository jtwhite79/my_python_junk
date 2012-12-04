import shapefile

shapename = '..\\_gis\\scratch\\all_K_locations_layers'
shp = shapefile.Reader(shapename)
records,shapes = shp.records(),shp.shapes()
fnames = shapefile.get_fieldnames(shapename)
lay_idx = fnames.index('k_layer')
k_idx = fnames.index('K_ftday')
#--loop once to get layer groups
layer_groups = {}
for rec,shape in zip(records,shapes):
    lay = rec[lay_idx]
    k = float(rec[k_idx])
    point = shape.points[0]
    if lay in layer_groups.keys():
        layer_groups[lay][0].append(k)
        layer_groups[lay][1].append(point)
    else:
        layer_groups[lay] = [[k],[point]]

out_dir = 'gslib\\'
for layer,[ks,points] in layer_groups.iteritems():
    print layer    
    f = open(out_dir+layer+'.dat','w')
    f.write(layer+'\n')
    f.write('3\nX\nY\nK\n')
    for pt,k in zip(points,ks):
        f.write('{0:15.6F}  {1:15.6F}  {2:15.6F}\n'.format(pt[0],pt[1],k))
    f.close()

    
