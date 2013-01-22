import os
from copy import deepcopy
import numpy as np
import pandas
import pst_handler
from pst_handler import pst

p = pst()
p.read_pst('umd02.pst')
p.reconcile_prior_2_pars()
out_dir = 'tests\\'
test_count = 1
#--find paired processed/raw obs groups
processed,raw = [],[]
obs_grps = list(p.observation_groups['obgnme'].values)
for ogp in obs_grps:
    if ogp+'_r' in obs_grps:
        processed.append(ogp)
        raw.append(ogp+'_r')
#--seperate processed and raw
sel1,sel2 = [],[]
bf_obsname = []
pred_groups = []
for ogp in p.observation_groups['obgnme'].values:
    if ogp in processed:
        sel1.append(False)
        sel2.append(True)
    elif ogp in raw:
        sel1.append(True)
        sel2.append(False)
    else:
        if not ogp.endswith('p'):
            bf_obsname.append(ogp)
        else:
            pred_groups.append(ogp)
        sel1.append(True)
        sel2.append(True)

f = open('umd02_prednames.dat','w',0)
for pred_group in pred_groups:
    print pred_group
    #print p.observation_data.obgnme==pred_group
    parnames = p.observation_data.obsnme[p.observation_data.obgnme==pred_group]
    f.write(parnames.values[0]+'\n')
f.close()

#--reset the mode to estimation and lose the prior info and regularization section
p.pestmode.set_value('estimation')
p.prior_information = None
p.regularisation = None
for bf in bf_obsname:
    p.observation_data.weight[p.observation_data.obgnme==bf] = 1.0
p1 = deepcopy(p)
p2 = deepcopy(p)
p1.observation_groups = pandas.DataFrame(p.observation_groups[sel1])
p1.update(False)
p1.write_pst('umd02_raw_head_bf.pst')
p2.observation_groups = pandas.DataFrame(p.observation_groups[sel2])
p2.update(False)
p2.write_pst('umd02_processed_head_bf.pst')

for bf in bf_obsname:
    p.observation_data.weight[p.observation_data.obgnme==bf] = 0.0
p1 = deepcopy(p)
p2 = deepcopy(p)
p1.observation_groups = pandas.DataFrame(p.observation_groups[sel1])
p1.update(False)
p1.write_pst('umd02_raw_head.pst')
p2.observation_groups = pandas.DataFrame(p.observation_groups[sel2])
p2.update(False)
p2.write_pst('umd02_processed_head.pst')


