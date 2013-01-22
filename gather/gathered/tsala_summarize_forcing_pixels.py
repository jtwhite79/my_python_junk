import calendar
import numpy as np

import pandas
import shapefile

days = calendar.mdays

print 'loading nexrad dataframe and computing yearly totals and monthly means'
nex_df = pandas.read_csv('NEXRAD.csv',index_col=0,parse_dates=True)
nex_df[nex_df < 0] = 0.0
nex_tots = nex_df.groupby(lambda x:x.year).sum()
nex_mnmeans = nex_df.groupby(lambda x:x.month).mean()
for mn,series in nex_mnmeans.iterrows():
    nex_mnmeans.ix[mn] *= days[mn]

print 'loading pet dataframe and computing yearly totals and monthly means'
pet_df = pandas.read_csv('PET.csv',index_col=0,parse_dates=True)
pet_df[pet_df < 0] = 0.0
pet_tots = pet_df.groupby(lambda x:x.year).sum()
pet_mnmeans = pet_df.groupby(lambda x:x.month).mean()
for mn,series in pet_mnmeans.iterrows():
    pet_mnmeans.ix[mn] *= days[mn]

#--convert from mm to inches
pet_tots /= 25.4
pet_mnmeans /= 25.4

print 'build shape attributes'
shapename = '..\\shapes\\df_pixels'
shp = shapefile.Reader(shapename)
wr = shapefile.Writer()
wr.field('Pixel',fieldType='N',size=10,decimal=0)
for yr in nex_tots.index:
    wr.field('nex_'+str(yr),fieldType='N',size=20,decimal=10)
for yr in pet_tots.index:
    wr.field('pet_'+str(yr),fieldType='N',size=20,decimal=10)
for mn in nex_mnmeans.index:
    wr.field('nex_'+str(mn),fieldType='N',size=20,decimal=10)    
for mn in pet_mnmeans.index:
    wr.field('pet_'+str(mn),fieldType='N',size=20,decimal=10)
  


for i in range(shp.numRecords):
    print i,'\r',
    shape = shp.shape(i)
    pnum = str(shp.record(i)[0])

    rec = [int(pnum)]
    for yr,pseries in nex_tots.iterrows():
        rec.append(pseries[pnum])
    for yr,pseries in pet_tots.iterrows():
        rec.append(pseries[pnum])
    for mn,pseries in nex_mnmeans.iterrows():
        rec.append(pseries[pnum])
    for mn,pseries in pet_mnmeans.iterrows():
        rec.append(pseries[pnum])
    wr.poly([shape.points],shapeType=shape.shapeType)
    wr.record(rec)   
wr.save('..\\shapes\\tsala_pixel_summaries')



