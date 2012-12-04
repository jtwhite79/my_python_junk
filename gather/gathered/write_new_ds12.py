import swr

ds_13a = swr.ds_13a('swr_ds13a_working_strval.dat')
ds_13a.load_structures()
ds_13a.write_ds12('swr_ds12.dat')