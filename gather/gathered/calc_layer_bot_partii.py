import matplotlib
matplotlib.use('Agg')
import os,sys,pylab
import numpy as np
import gslibUtil as gu


import arrayUtil as au
import numpy as np
import pylab

#--load hard data
harddata_file = '..\\tbl29_pro.dat'
title,harddata_names,harddata = gu.loadGslibFile(harddata_file)
#print np.shape(harddata)

nrow,ncol = 301,501
delr,delc = 500,500
offset = [728600.,577350.]

top = au.loadArrayFromFile(nrow,ncol,'filter_28_edge.ref')
l1_thk  =  au.loadArrayFromFile(nrow,ncol,'Layer_thk\\H_resample_500_500.ref') 
l2_thk  =  au.loadArrayFromFile(nrow,ncol,'Layer_thk\\Q5_resample_500_500.ref')
l3_thk  =  au.loadArrayFromFile(nrow,ncol,'Layer_thk\\Q4_resample_500_500.ref')
l4_thk  =  au.loadArrayFromFile(nrow,ncol,'Layer_thk\\Q3_resample_500_500.ref')
l5_thk  =  au.loadArrayFromFile(nrow,ncol,'Layer_thk\\Q2_resample_500_500.ref')
l6_thk  =  au.loadArrayFromFile(nrow,ncol,'Layer_thk\\Q1_resample_500_500.ref')
l7_thk  =  au.loadArrayFromFile(nrow,ncol,'Layer_thk\\T3_resample_500_500.ref')
l8_thk  =  au.loadArrayFromFile(nrow,ncol,'Layer_thk\\T2_resample_500_500.ref')
l9_thk  =  au.loadArrayFromFile(nrow,ncol,'Layer_thk\\T1_resample_500_500.ref')

l1_bot =    top -  l1_thk 
l2_bot = l1_bot -  l2_thk 
l3_bot = l2_bot -  l3_thk 
l4_bot = l3_bot -  l4_thk 
l5_bot = l4_bot -  l5_thk 
l6_bot = l5_bot -  l6_thk 
l7_bot = l6_bot -  l7_thk 
l8_bot = l7_bot -  l8_thk 
l9_bot = l8_bot -  l9_thk 
print 'layer max/min:'
print np.max(l1_thk),np.min(l1_thk)
print np.max(l2_thk),np.min(l2_thk)
print np.max(l3_thk),np.min(l3_thk)
print np.max(l4_thk),np.min(l4_thk)
print np.max(l5_thk),np.min(l5_thk)
print np.max(l6_thk),np.min(l6_thk)
print np.max(l7_thk),np.min(l7_thk)
print np.max(l8_thk),np.min(l8_thk)
print np.max(l9_thk),np.min(l9_thk)

l1_row_diff = np.abs(l1_bot[0:-1,:]-l1_bot[1:,:])-l1_thk[0:-1,:]
l2_row_diff = np.abs(l2_bot[0:-1,:]-l2_bot[1:,:])-l2_thk[0:-1,:]
l3_row_diff = np.abs(l3_bot[0:-1,:]-l3_bot[1:,:])-l3_thk[0:-1,:]
l4_row_diff = np.abs(l4_bot[0:-1,:]-l4_bot[1:,:])-l4_thk[0:-1,:]
l5_row_diff = np.abs(l5_bot[0:-1,:]-l5_bot[1:,:])-l5_thk[0:-1,:]
l6_row_diff = np.abs(l6_bot[0:-1,:]-l6_bot[1:,:])-l6_thk[0:-1,:]
l7_row_diff = np.abs(l7_bot[0:-1,:]-l7_bot[1:,:])-l7_thk[0:-1,:]
l8_row_diff = np.abs(l8_bot[0:-1,:]-l8_bot[1:,:])-l8_thk[0:-1,:]
l9_row_diff = np.abs(l9_bot[0:-1,:]-l9_bot[1:,:])-l9_thk[0:-1,:]

l1_col_diff = np.abs(l1_bot[:,0:-1]-l1_bot[:,1:])-l1_thk[:,0:-1]
l2_col_diff = np.abs(l2_bot[:,0:-1]-l2_bot[:,1:])-l2_thk[:,0:-1]
l3_col_diff = np.abs(l3_bot[:,0:-1]-l3_bot[:,1:])-l3_thk[:,0:-1]
l4_col_diff = np.abs(l4_bot[:,0:-1]-l4_bot[:,1:])-l4_thk[:,0:-1]
l5_col_diff = np.abs(l5_bot[:,0:-1]-l5_bot[:,1:])-l5_thk[:,0:-1]
l6_col_diff = np.abs(l6_bot[:,0:-1]-l6_bot[:,1:])-l6_thk[:,0:-1]
l7_col_diff = np.abs(l7_bot[:,0:-1]-l7_bot[:,1:])-l7_thk[:,0:-1]
l8_col_diff = np.abs(l8_bot[:,0:-1]-l8_bot[:,1:])-l8_thk[:,0:-1]
l9_col_diff = np.abs(l9_bot[:,0:-1]-l9_bot[:,1:])-l9_thk[:,0:-1]

print 'writing diff arrays'
au.writeArrayToFile(l1_bot,'l1_bot.ref')
au.writeArrayToFile(l2_bot,'l2_bot.ref')
au.writeArrayToFile(l3_bot,'l3_bot.ref')
au.writeArrayToFile(l4_bot,'l4_bot.ref')
au.writeArrayToFile(l5_bot,'l5_bot.ref')
au.writeArrayToFile(l6_bot,'l6_bot.ref')
au.writeArrayToFile(l7_bot,'l7_bot.ref')
au.writeArrayToFile(l8_bot,'l8_bot.ref')
au.writeArrayToFile(l9_bot,'l9_bot.ref')

#au.writeArrayToFile(l1_row_diff,'l1_row_thk_diff.ref') 
#au.writeArrayToFile(l2_row_diff,'l2_row_thk_diff.ref') 
#au.writeArrayToFile(l3_row_diff,'l3_row_thk_diff.ref') 
#au.writeArrayToFile(l4_row_diff,'l4_row_thk_diff.ref') 
#au.writeArrayToFile(l5_row_diff,'l5_row_thk_diff.ref') 
#au.writeArrayToFile(l6_row_diff,'l6_row_thk_diff.ref') 
#au.writeArrayToFile(l7_row_diff,'l7_row_thk_diff.ref') 
#au.writeArrayToFile(l8_row_diff,'l8_row_thk_diff.ref') 
#au.writeArrayToFile(l9_row_diff,'l9_row_thk_diff.ref') 
#
#au.writeArrayToFile(l1_col_diff,'l1_diff_thk_col.ref') 
#au.writeArrayToFile(l2_col_diff,'l2_diff_thk_col.ref') 
#au.writeArrayToFile(l3_col_diff,'l3_diff_thk_col.ref') 
#au.writeArrayToFile(l4_col_diff,'l4_diff_thk_col.ref') 
#au.writeArrayToFile(l5_col_diff,'l5_diff_thk_col.ref') 
#au.writeArrayToFile(l6_col_diff,'l6_diff_thk_col.ref') 
#au.writeArrayToFile(l7_col_diff,'l7_diff_thk_col.ref') 
#au.writeArrayToFile(l8_col_diff,'l8_diff_thk_col.ref') 
#au.writeArrayToFile(l9_col_diff,'l9_diff_thk_col.ref') 

print 'plotting diff arrays'
#au.plotArray(l1_row_diff,500,500,offset=offset,output='save',title='l1_row_diff_thk')
#au.plotArray(l2_row_diff,500,500,offset=offset,output='save',title='l2_row_diff_thk')
#au.plotArray(l3_row_diff,500,500,offset=offset,output='save',title='l3_row_diff_thk')
#au.plotArray(l4_row_diff,500,500,offset=offset,output='save',title='l4_row_diff_thk')
#au.plotArray(l5_row_diff,500,500,offset=offset,output='save',title='l5_row_diff_thk')
#au.plotArray(l6_row_diff,500,500,offset=offset,output='save',title='l6_row_diff_thk')
#au.plotArray(l7_row_diff,500,500,offset=offset,output='save',title='l7_row_diff_thk')
#au.plotArray(l8_row_diff,500,500,offset=offset,output='save',title='l8_row_diff_thk')
#au.plotArray(l9_row_diff,500,500,offset=offset,output='save',title='l9_row_diff_thk') 

#au.plotArray(l1_col_diff,500,500,offset=offset,output='save',title='l1_col_diff_thk')
#au.plotArray(l2_col_diff,500,500,offset=offset,output='save',title='l2_col_diff_thk')
#au.plotArray(l3_col_diff,500,500,offset=offset,output='save',title='l3_col_diff_thk')
#au.plotArray(l4_col_diff,500,500,offset=offset,output='save',title='l4_col_diff_thk')
#au.plotArray(l5_col_diff,500,500,offset=offset,output='save',title='l5_col_diff_thk')
au.plotArray(l6_col_diff,500,500,offset=offset,output='save',title='l6_col_diff_thk')
au.plotArray(l7_col_diff,500,500,offset=offset,output='save',title='l7_col_diff_thk')
au.plotArray(l8_col_diff,500,500,offset=offset,output='save',title='l8_col_diff_thk')
au.plotArray(l9_col_diff,500,500,offset=offset,output='save',title='l9_col_diff_thk')



au.plotArray(l1_bot,500,500,output='save',title='l1_bot',offset=offset,gtps=harddata[:,0:2])
au.plotArray(l2_bot,500,500,output='save',title='l2_bot',offset=offset,gtps=harddata[:,0:2])
au.plotArray(l3_bot,500,500,output='save',title='l3_bot',offset=offset,gtps=harddata[:,0:2])
au.plotArray(l4_bot,500,500,output='save',title='l4_bot',offset=offset,gtps=harddata[:,0:2])
au.plotArray(l5_bot,500,500,output='save',title='l5_bot',offset=offset,gtps=harddata[:,0:2])
au.plotArray(l6_bot,500,500,output='save',title='l6_bot',offset=offset,gtps=harddata[:,0:2])
au.plotArray(l7_bot,500,500,output='save',title='l7_bot',offset=offset,gtps=harddata[:,0:2])
au.plotArray(l8_bot,500,500,output='save',title='l8_bot',offset=offset,gtps=harddata[:,0:2])
au.plotArray(l9_bot,500,500,output='save',title='l9_bot',offset=offset,gtps=harddata[:,0:2])


