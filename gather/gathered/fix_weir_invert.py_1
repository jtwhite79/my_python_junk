import swr

ds_13a = swr.ds_13a('swr_ds13a_working_strval.dat')
ds_13a.load_structures()
for s in ds_13a.structures:
    if s['istrtype'] == 6 and s['strinv'] < -2.0:
        s['strinv'] = -1.5
        print s['strinv'],s['a_com']
        
        
ds_13a.write_structures('swr_ds13a_working_strval_1.dat',byreach=True)
ds_13a.write_ds12('swr_ds12.dat')         