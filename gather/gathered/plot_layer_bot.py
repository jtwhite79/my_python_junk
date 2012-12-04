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

nrow,ncol = 459,615
delr,delc = 500,500
offset = [668350.,580985.]

max_elev - 15.0
top = au.loadArrayFromFile(nrow,ncol,'model_top.ref')
top[np.where(top>max_elev)] = max_elev
au.plotArray(top,delr,delc,gpts=harddata[:,0:2],offset=offset)
#
#l1_bot = top - au.loadArrayFromFile(nrow,ncol,'H_resample_500_500.ref')
#l2_bot = l1_bot - au.loadArrayFromFile(nrow,ncol,'Q5_resample_500_500.ref')
#l3_bot = l2_bot - au.loadArrayFromFile(nrow,ncol,'Q4_resample_500_500.ref')
#l4_bot = l3_bot - au.loadArrayFromFile(nrow,ncol,'Q3_resample_500_500.ref')
#l5_bot = l4_bot - au.loadArrayFromFile(nrow,ncol,'Q2_resample_500_500.ref')
#l6_bot = l5_bot - au.loadArrayFromFile(nrow,ncol,'Q1_resample_500_500.ref')
#l7_bot = l6_bot - au.loadArrayFromFile(nrow,ncol,'T3_resample_500_500.ref')
#l8_bot = l7_bot - au.loadArrayFromFile(nrow,ncol,'T2_resample_500_500.ref')
#l9_bot = l8_bot - au.loadArrayFromFile(nrow,ncol,'T1_resample_500_500.ref')
#au.writeArrayToFile(top,'model_top_25ft.ref')
#au.writeArrayToFile(l1_bot,'l1_bot.ref')
#au.writeArrayToFile(l2_bot,'l2_bot.ref')
#au.writeArrayToFile(l3_bot,'l3_bot.ref')
#au.writeArrayToFile(l4_bot,'l4_bot.ref')
#au.writeArrayToFile(l5_bot,'l5_bot.ref')
#au.writeArrayToFile(l6_bot,'l6_bot.ref')
#au.writeArrayToFile(l7_bot,'l7_bot.ref')
#au.writeArrayToFile(l8_bot,'l8_bot.ref')
#au.writeArrayToFile(l9_bot,'l9_bot.ref')

#au.plotArray(au.loadArrayFromFile(nrow,ncol,'model_top_25ft.ref'),500,500,offset=offset,gtps=harddata[:,0:2])
#au.plotArray(au.loadArrayFromFile(nrow,ncol,'l1_bot.ref'),500,500,offset=offset,gtps=harddata[:,0:2])
#au.plotArray(au.loadArrayFromFile(nrow,ncol,'l2_bot.ref'),500,500,offset=offset,gtps=harddata[:,0:2])
#au.plotArray(au.loadArrayFromFile(nrow,ncol,'l3_bot.ref'),500,500,offset=offset,gtps=harddata[:,0:2])
#au.plotArray(au.loadArrayFromFile(nrow,ncol,'l4_bot.ref'),500,500,offset=offset,gtps=harddata[:,0:2])
#au.plotArray(au.loadArrayFromFile(nrow,ncol,'l5_bot.ref'),500,500,offset=offset,gtps=harddata[:,0:2])
#au.plotArray(au.loadArrayFromFile(nrow,ncol,'l6_bot.ref'),500,500,offset=offset,gtps=harddata[:,0:2])
#au.plotArray(au.loadArrayFromFile(nrow,ncol,'l7_bot.ref'),500,500,offset=offset,gtps=harddata[:,0:2])
#au.plotArray(au.loadArrayFromFile(nrow,ncol,'l8_bot.ref'),500,500,offset=offset,gtps=harddata[:,0:2])
#au.plotArray(au.loadArrayFromFile(nrow,ncol,'l9_bot.ref'),500,500,offset=offset,gtps=harddata[:,0:2])



#path = ''
#files = os.listdir(path) 
#print files
#for file in files:
#    if file.split('.')[-1] == 'ref':
#        print file
#        this_array = au.loadArrayFromFile(nrow,ncol,path+file)
#        print np.mean(this_array)
#        au.plotArray(this_array,delr,delc,gpts=harddata[:,0:2],offset=offset)
#           
#pylab.show()
    




