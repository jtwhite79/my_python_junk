import os
import shutil
import numpy as np
from bro import seawat


name_dict = {'hk':{'prefix':'hk_','suffix':'_1.ref'},'prsity':{'prefix':'prsity_','suffix':'.ref'}}
coarse_map = ['upr','upr','prd','prd','prd','prd','prd','prd','prd','prd','lwr','lwr']
fine_map = [None,None,'pd1','pd1','pd1','pd1','pd2','pd2','pd2','pd2',None,None]

model_dir = '..\\_model\\bro.03\\seawatref\\mod\\'
mult_dir = 'ref\\mult\\'
base_dir = 'ref\\base\\'
in_dir = 'bro.03\\calibration\\seawatref\\mod\\'    

def apply():           
    fine_zone = np.loadtxt('ref\\fine_zone.ref')   
    mult_files = os.listdir(mult_dir)
    mult_dict = {}
    for mfile in mult_files:
        arr = np.loadtxt(mult_dir+mfile)
        raw = mfile.split('.')[0].split('_')
        par_type = raw[0]
        pp_type = raw[1]
        mult_dict[(par_type,pp_type)] = arr
    for ptype,ndict in name_dict.iteritems():
        prefix,suffix = ndict['prefix'],ndict['suffix']
        for k,[cmap,fmap] in enumerate(zip(coarse_map,fine_map)):
            base_name = prefix+str(k+1)+suffix
            base_arr = np.loadtxt(base_dir+base_name)
            cmult_arr = mult_dict[(ptype,cmap)]
            if fmap != None:
                fmult_arr = mult_dict[(ptype,fmap)]
                fmult_arr[np.where(fine_zone!=1)] = 1.0
            else:
                fmult_arr = 1.0
            np.savetxt(in_dir+base_name,base_arr*cmult_arr*fmult_arr,fmt=' %15.5E')



def setup():
    #--copy in fresh base arrays from the model dir
    for ptype,ndict in name_dict.iteritems():
        prefix,suffix = ndict['prefix'],ndict['suffix']
        for k,[cmap,fmap] in enumerate(zip(coarse_map,fine_map)):
            base_name = prefix+str(k+1)+suffix
            shutil.copy(model_dir+base_name,base_dir+base_name)

    

    

               
        








if __name__ == '__main__':
    setup()
    apply()
