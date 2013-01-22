import os
import copy

dir = 'pred_vectors\\'
files = os.listdir(dir)
pred_vecs,pred_names = [],[]

for f in files:
    if f.endswith('vec'):
        pred_vecs.append(f)
        pred_names.append(f.split('.')[0])


#--load the base in file
base_in_file = 'predunc5_base.in'
base = []
f = open(base_in_file,'r')
for line in f:
    base.append(line)
f.close()    

#--loop over each pred vector
count = 1
for pv,pn in zip(pred_vecs,pred_names):
    this_in = copy.deepcopy(base)
    this_in[3] = dir+pv+'\n'
    this_in[6] = pn+'.out\n'
    f = open(str(count)+'.in','w')
    for item in this_in:
        f.write(item)
    f.close()
    count += 1

