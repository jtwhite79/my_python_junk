import sys
import numpy as np
from flopy2.modflow import *
from flopy2.utils import util_2d,util_3d,util_list



nlay,nrow,ncol = 3,20,40


#--gen up some fake data
nper = 4
lrc = [['1',1.0,1],[2,2,2],[3,3,3]]
#l = np.arange(1,100)
#r = np.arange(1,100)
#c = np.arange(1,100)
#lrc = zip(l,r,c)
#data3 = []
#for i in range(1,100):
#    data3.append('cell '+str(i))
aux_strings = 1.0
data1,data2 = '1.0',[[2.0] * len(lrc)] * nper
ul = util_list.ulist(1,[lrc],[1.0],[aux_strings])
#ul = util_list.ulist(nper,lrc,[data1],dtype=np.float32)
print ul[0]
print ul[-1]
sys.exit()

#--------------------------------------------------------------------
#--util_2d

#--no external path...
model_instance = Modflow(modelname='my_perfect_model',external_path=None)
#--I'm experimenting with this one, so it isn't committed yet, but so far, can really speed things up
#--if the arrays haven't changed since the last run
setattr(model_instance,'use_existing',False)
some_k_scalar = 50.0
k_layer1_2d = util_2d(model_instance,(nrow,ncol),np.float32,some_k_scalar,name='k_in_layer_1',locat=10)
#--this returns a constant control record
#print k_layer1_2d.get_file_entry()


#--using the slice operators forces the array to be created
k_layer1_2d[1:-1] = 25.0
#--now the file entry is the control record followed by the array string
#print k_layer1_2d.get_file_entry()

#--set external path to force external array writing
model_instance.external_path = '.\\'
some_k_scalar = 50.0
k_layer1_2d = util_2d(model_instance,(nrow,ncol),np.float32,some_k_scalar,name='k_in_layer_1',locat=10)
#--just the control record that points an external file
#print k_layer1_2d.get_file_entry()

#--now create an external file for testing
np.savetxt('my_perfect_k.dat',np.zeros((nrow,ncol))+50.0,fmt=' %15.5f')

#--without an external path, the array is loaded and written below the control record
model_instance.external_path = None
some_k_filename = 'my_perfect_k.dat'
k_layer1_2d = util_2d(model_instance,(nrow,ncol),np.float32,some_k_filename,name='k_in_layer_1',locat=10)
#--returns the control record followed by the string of the array
#print k_layer1_2d.get_file_entry()


#--now if the model doesn't support free format and the external path is passed...
model_instance.external_path = '.\\'
k_layer1_2d = util_2d(model_instance,(nrow,ncol),np.float32,some_k_filename,name='k_in_layer_1',locat=10)
#--returns the control record that points to an external filename which is a copy of 'my_perfect_k.dat'
#print k_layer1_2d.get_file_entry()


#--now if the model supports free format and the external path is passed...
model_instance.external_path = '.\\'
k_layer1_2d = util_2d(model_instance,(nrow,ncol),np.float32,some_k_filename,name='k_in_layer_1',locat=10)
#--returns the control record that points to "my_perfect_k.dat" without loading or copying (open/close)
#print k_layer1_2d.get_file_entry()

#--to access the array which in this case loads the array stored in 'my_perfect_k.dat'
#print k_layer1_2d.array

#--to access the string,  returns the string representation of the array that was just loaded
#print k_layer1_2d.string


#----------------------------------------------------------------------------------------------
#--util_3d - just a wrapper around util_2d

#--just a scalar assigns the same value to all layers
#--internal (constants)
model_instance.external_path = None
k_3d = util_3d(model_instance,(nlay,nrow,ncol),np.float32,some_k_scalar,name='k')
#print k_3d.get_file_entry()

#--external arrays
model_instance.external_path = '.\\'
k_3d = util_3d(model_instance,(nlay,nrow,ncol),np.float32,some_k_scalar,name='k')
#print k_3d.get_file_entry()

#--a mix of nlay items - internal
model_instance.external_path = None
some_k_list = [50.0,'my_perfect_k.dat',np.zeros((nrow,ncol))+50.0]
k_3d = util_3d(model_instance,(nlay,nrow,ncol),np.float32,some_k_list,name='k')
#print k_3d.get_file_entry()


#--a mix of nlay items - external
model_instance.external_path = '.\\'
some_k_list = [50.0,'my_perfect_k.dat',np.zeros((nrow,ncol))+50.0]
k_3d = util_3d(model_instance,(nlay,nrow,ncol),np.float32,some_k_list,name='k')
print k_3d.get_file_entry()

