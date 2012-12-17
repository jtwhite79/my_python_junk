import numpy as np
import pandas
import shapefile


print 'loading grid shapefile info'
grid_shapename = '..\\shapes\\tsala_grid_nexrad'
grid_shape = shapefile.Reader(grid_shapename)
fieldnames = shapefile.get_fieldnames(grid_shapename,ignorecase=True)
row_idx,col_idx = fieldnames.index('ROW'),fieldnames.index('COLUMN_')
pix_idx,frac_idx = fieldnames.index('NEX_PIX'),fieldnames.index('NEX_FRAC')
pixel_map = {}
pixel_numbers = []
nrow,ncol = -1.0E+10,-1.0E+10
for i in range(grid_shape.numRecords):
    if i % 500 == 0:
        print i,'of',grid_shape.numRecords,'\r',
    rec = grid_shape.record(i)
    pix,frac = rec[pix_idx],rec[frac_idx]
    r,c = rec[row_idx],rec[col_idx]
    if r > nrow: nrow = r
    if c > ncol: ncol = c
    idx_tup = (r-1,c-1)    
    pf_list = []
    if len(pix) > 0:
        pf_list = []
        
        for p,f in zip(pix.split(','),frac.split(',')):
            p = int(p)
            f = float(f)
            pf_list.append((p,f))            
    pixel_map[idx_tup] = pf_list
        



print '\nloading nexrad dataframe'
precip_df = pandas.read_csv('NEXRAD.csv',index_col=0,parse_dates=True)
df_keys = precip_df.keys()

#--check for missing pixels
missing = []
for idx_tup,pf_list in pixel_map.iteritems():
    for p,f in pf_list:
        if p in df_keys:
            print 'found',p
        elif p not in missing:
            missing.append(p)
if len(missing) > 0:
    print 'missing data for',len(missing),' pixels'
    print len(df_keys)
    for m in missing:
        print m
    raise Exception()


print 'processing dataframe rows'
aprefix = 'rch\\rch_'
for dt,pixel_values in precip_df.iterrows():
    aname = aprefix+dt.strftime('%Y%m%d')+'.ref'    
    arr = np.zeros((nrow,ncol),dtype=np.float32) - 999.9
    for i in range(nrow):
        for j in range(ncol):
            pf_list = pixel_map[(i,j)]
            for (p,f) in pf_list:               
                arr[i,j] += pixel_values[p] * f
                print arr[i,j]               

    arr.tofile(aname)
    break


