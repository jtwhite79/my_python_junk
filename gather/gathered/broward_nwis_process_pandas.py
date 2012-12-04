import pandas

#--load the raw nwis file
master = pandas.read_csv('nwis_raw.csv',sep='|',header=0)
master.index = [master['site_no'],master['parm_nm']]
grouped = master.groupby(level=1)
print grouped
print junk
