

pnames = ['surfwat','rowcol','layer']
pgrps = ['smpl_sw','smpl_rc','smpl_lay']
f_tpl = open('tpl\\simple.tpl','w',0)
f_in = open('par\\simple.dat','w',0)

f_tpl.write('ptf ~\n')
for pname in pnames:
    f_tpl.write(pname + '  ~{0:10s}~\n'.format(pname))
    f_in.write(pname+ '  1.0\n')
f_tpl.close()
f_in.close()

f_par,f_grp = open('pst_components\\simple_pars.dat','w',0),open('pst_components\\simple_grps.dat','w',0)

for pname,pgrp in zip(pnames,pgrps):
    f_par.write('{0:20s}  log   factor  1.0  1.0e-10  1.0e+10  {1:20s}   1.0   0.0   1\n'.format(pname,pgrp))
    f_grp.write('{0:20s}       absolute     1.0   0.000      always_2      2.000      parabolic\n'.format(pgrp))
                
f_par.close()
f_grp.close()