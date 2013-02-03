from datetime import datetime
'''
set up decadal wet and dry season multipliers
'''

dry_months = [12,1,2,3,4,5]

rch_file = '..\\_prediction\\bro.03.pred\\flow.rch'
ets_file = '..\\_prediction\\bro.03.pred\\flow.ets'

par_dict = {'rch_pred':[],'ets_pred':[]}

f_in = open(rch_file,'r')
f_out = open('tpl\\rech_pred.tpl','w',0)
f_out.write('ptf ~\n')
f_out.write(f_in.readline())
f_out.write(f_in.readline())
decade = 2010
while True:
    crec = f_in.readline()
    f_out.write(crec)
    if crec == '':
        break
    raw = crec.split('#')[1].split()[3]
    dt = datetime.strptime(raw,'%Y-%m-%d')
    if dt.year %10 == 0:
        decade = dt.year

    u2drel = f_in.readline()
    raw = u2drel.split()
    pval = float(raw[2])
    if dt.month in dry_months:
        season = 'dr'
    else:
        season = 'wt'
    pname = 'rch'+season+'_'+str(decade)
    par_dict['rch_pred'].append(pname)
    tpl_entry = '~{0:15s}~'.format(pname)
    raw[2] = tpl_entry
    f_out.write(' '.join(raw)+'\n')
f_in.close()
f_out.close()

f_in = open(ets_file,'r')
f_out = open('tpl\\ets_pred.tpl','w',0)
f_out.write('ptf ~\n')
f_out.write(f_in.readline())
f_out.write(f_in.readline())
decade = 2010
while True:
    line = f_in.readline()
    if line == '':
        break
    if 'stress period' in line:
        raw = line.split('#')[1].split()[3]
        dt = datetime.strptime(raw,'%Y-%m-%d')
        if dt.year %10 == 0:
            decade = dt.year        
    elif 'ETSR' in line:
        u2drel = f_in.readline()
        raw = u2drel.split()
        pval = float(raw[2])
        if dt.month in dry_months:
            season = 'dr'
        else:
            season = 'wt'
        pname = 'ets'+season+'_'+str(decade)
        par_dict['ets_pred'].append(pname)
        tpl_entry = '~{0:15s}~'.format(pname)
        raw[2] = tpl_entry        
        line = '   '.join(raw)+'\n'
    f_out.write(line)
f_in.close()
f_out.close()

f_par = open('pst_components\\rchets_pars.dat','w',0)
f_grp = open('pst_components\\rchets_grps.dat','w',0)

par_grps = par_dict.keys()
par_grps.sort()

for prop in par_grps:            
    f_grp.write('{0:20s}       relative     1.0000E-02   0.000      switch      2.000      parabolic\n'.format(prop))
    par_names = par_dict[prop]
    for par_name in par_names:            
        f_par.write('{0:20s}  log   factor  1.0  1.0e-10  1.0e+10  {1:20s}   1.0   0.0   1\n'.format(par_name,prop))


f_par.close()
f_grp.close()            




