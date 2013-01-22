import os
import sys
import subprocess as sp
import numpy as np

exe = 'i64parvar1.exe'
pst_pth = '..\\pst_jco\\pest_actual.pst'
jco_pth = '..\\pst_jco\\pest_actual.jco'
unc_pth = '..\\param_unc\\param.unc'
ref_var = 1.0




args = [pst_pth,ref_var,unc_pth,'']
for s in sing_vals:
    args.append(str(int(s)))
print args
sys.exit()    

#--get prediction and pred vector names
pred_dir = '..\\pred_vectors\\'
files = os.listdir(pred_dir)
pred_names,pred_vecs = [],[]
for f in files:
    if f.endswith('vec'):
        pred_names.append(f.split('.')[0])
        pred_vecs.append(f)
        

for idx in range(len(pred_names)):        
    
    
    p = sp.Popen(args,stdout=sp.PIPE,stderr=sp.PIPE)
    stdout,stderr = p.communicate()
    
    f_out = open(pred_names[idx]+'.out','w')
    f_err = open(pred_names[idx]+'.err','w')
    f_out.write(stdout)
    f_err.write(stderr)
    f_out.close()
    f_err.close()


