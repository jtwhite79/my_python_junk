import numpy as np
import pandas

from simple import grid



#--load ds 4a
ds4a = np.loadtxt('swr_ds4a.dat')
pass

#--build geometry entries
channel_depth = 7.0
geo_num = 1
condop = 1
mann = 0.03
width = 3.0
igeotype = 2
slope = 2.0
leakance = 1.0
dwn_stage = 95.0
#str_reach = 182
#str_inv = 94.5
f_ds10,f_ds11 = open('swr_ds10.dat','w',0),open('swr_ds11.dat','w',0)
f_ds14 = open('swr_ds14.dat','w',0)
for i,(r,c) in enumerate(zip(ds4a[:,4],ds4a[:,5])):
    top = grid.top[r-1,c-1]
    geo_entry = '{0:6d} {1:6d} {2:6d} {3:6.5f} {4:6.2f} {5:6.2f} {6:6.3f} {7:6.3f}  #{8:6.3f}\n'.\
        format(geo_num,igeotype,condop,mann,width,top-channel_depth,slope,leakance,top)
    f_ds11.write(geo_entry)
    f_ds10.write('{0:6d} {0:6d}  0.0\n'.format(geo_num))
    #if i >= str_reach:
    #    f_ds14.write('{0:6d} {1:15.6f}\n'.format(geo_num,dwn_stage))
    #else:
    #    f_ds14.write('{0:6d} {1:15.6f}\n'.format(geo_num,str_inv))
    f_ds14.write('{0:6d} {1:15.6f}\n'.format(geo_num,dwn_stage))
    geo_num += 1
    pass
f_ds11.close()
f_ds10.close()
f_ds14.close()
f_ds6 = open('swr_ds6.dat','w',0)
f_cnst = open('..\\base\\swr_constant.dat','w',0)
for i in range(ds4a.shape[0]-1):
    f_ds6.write('{0:6d} {1:6d}\n'.format(i+1,1))
    f_cnst.write('{0:6d} {1:6d}\n'.format(i+1,-1))
f_ds6.write('{0:6d} {1:6d}\n'.format(i+2,-1))
f_cnst.write('{0:6d} {1:6d}\n'.format(i+2,-1))
f_cnst.close()
f_ds6.close()
shutil.copy('swr_ds6.dat','..\\base\\swr_ds6_dynamic.dat')





#--reduced row col
#--load ds 4a
ds4a = np.loadtxt('swr_ds4a_rc.dat')
pass

#--build geometry entries
channel_depth = 7.0
geo_num = 1
condop = 1
mann = 0.03
width = 3.0
igeotype = 2
slope = 2.0
leakance = 1.0
dwn_stage = 95.0
#str_reach = 182
#str_inv = 94.5
f_ds10,f_ds11 = open('swr_ds10_rc.dat','w',0),open('swr_ds11_rc.dat','w',0)
f_ds14 = open('swr_ds14_rc.dat','w',0)
reduced_top = np.loadtxt('ref_rc\\top.ref')
for i,(r,c) in enumerate(zip(ds4a[:,4],ds4a[:,5])):
    top = reduced_top[r-1,c-1]
    geo_entry = '{0:6d} {1:6d} {2:6d} {3:6.5f} {4:6.2f} {5:6.2f} {6:6.3f} {7:6.3f}  #{8:6.3f}\n'.\
        format(geo_num,igeotype,condop,mann,width,top-channel_depth,slope,leakance,top)
    f_ds11.write(geo_entry)
    f_ds10.write('{0:6d} {0:6d}  0.0\n'.format(geo_num))
    #if i >= str_reach:
    #    f_ds14.write('{0:6d} {1:15.6f}\n'.format(geo_num,dwn_stage))
    #else:
    #    f_ds14.write('{0:6d} {1:15.6f}\n'.format(geo_num,str_inv))
    f_ds14.write('{0:6d} {1:15.6f}\n'.format(geo_num,dwn_stage))
    geo_num += 1
    pass
f_ds11.close()
f_ds10.close()
f_ds14.close()
f_ds6 = open('swr_ds6_rc.dat','w',0)
for i in range(ds4a.shape[0]-1):
    f_ds6.write('{0:6d} {1:6d}\n'.format(i+1,1))
f_ds6.write('{0:6d} {1:6d}\n'.format(i+2,-1))






            
