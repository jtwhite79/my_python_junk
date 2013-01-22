
import os
import numpy as np
from pst_handler import pst





#--uncorrelated uncertainty by group
'''
param = std
etsx = 0.25m
petm = 0.25
pseg = 0.0 (all fixed)
nex = 0.1
cond = 100
'''
std_dict = {'etsx':0.25,'petm':0.25,'nex':0.1,'cond':100,'pseg':1.0e-10}
p = pst(filename='..\\umd02.pst')
f_unc_sc = open('umd02_scaled.unc','w',0)
f_unc_sc.write('START STANDARD_DEVIATION\n')
for pname in p.parameter_data.parnme:
    f_unc_sc.write('  {0:20s} {1:15.7G}\n'.format(pname,1.0))    
f_unc_sc.write('END STANDARD_DEVIATION\n\n')
f_unc_sc.close()

f_unc = open('umd02.unc','w',0)
for pargp in p.parameter_groups.pargpnme:
    
    if pargp in std_dict.keys():
        f_unc.write('START STANDARD_DEVIATION\n')
        params = p.parameter_data[p.parameter_data.pargp==pargp]        
        for i in params.index:
            par = params.ix[i]            
            std = std_dict[pargp]
            if par['partrans'] == 'log':                
                if std > par['parval1']:
                    std = (np.log10(par['parval1'] + std) - np.log10(par['parval1']))
                else:
                    std = (np.log10(par['parval1'] + std) - np.log10(par['parval1'] - std)) / 2.0
            f_unc.write('  {0:20s} {1:15.7G}\n'.format(par['parnme'],std))
        f_unc.write('END STANDARD_DEVIATION\n\n')


#--build cov matrices for pilot points
struct_file = '..\\setup_files\\struct3.dat'
base_pp_file = '..\\setup_files\\pp_locs.dat'
pp_prefixes = ['l1k_','l2k_','l3k_']
pp_dir = 'pp_locs\\'
cov_dir = 'mat\\'
exe = 'ppcov.exe'
cov_names = []
for prefix in pp_prefixes:
    f_in = open(base_pp_file,'r')
    pp_name = pp_dir+prefix+'locs.dat'
    f_out = open(pp_name,'w',0)
    for line in f_in:
        f_out.write(prefix+line[2:])
    f_in.close()
    f_out.close()
    cov_name = cov_dir+prefix+'cov.mat'
    cov_names.append(cov_names)
    f_unc.write('START COVARIANCE_MATRIX\n  variance_multiplier 1.0\n  file '+cov_name+'\nEND COVARIANCE_MATRIX\n\n')    
    ppcov_in = [pp_name,'0.0',struct_file,'interpolat',cov_name,'','']
    f = open('ppcov.in','w',0)
    f.write('\n'.join(ppcov_in))
    f.close()
    os.system(exe+' < ppcov.in')









