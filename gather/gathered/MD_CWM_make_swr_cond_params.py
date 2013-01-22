
ds11_file = 'UMD.03\\SWRREF\\SWR_Dataset11.ref'
tpl_lines = []
cnd_par_names = []
cnd_par_vals = []
man_par_names = []
man_par_vals = []
f = open(ds11_file,'r')
for line in f:
    if not line.strip().startswith('#') and not line.strip().startswith('O'):
        raw = line.strip().split()
        rnum = int(raw[0])
        parname = 'man{0:03.0f}'.format(rnum)
        man_par_names.append(parname)
        man_par_vals.append(float(raw[3]))
        raw[3] = '~   '+parname+'   ~'
        parname = 'cnd{0:03.0f}'.format(rnum)
        cnd_par_names.append(parname)
        cnd_par_vals.append(float(raw[5]))
        raw[5] = '~   '+parname+'  ~'
        l = ''
        for r in raw:
            l += ' '+r.rjust(9)
        l += '\n'
        tpl_lines.append(l)
        
    else:
        tpl_lines.append(line)

f.close()
f = open('SWR_Dataset11.tpl','w')
f.write('ptf ~\n')
for line in tpl_lines:
    f.write(line)
f.close()

f = open('pst_components\\swr_cond.dat','w')
for pn,pv in zip(cnd_par_names,cnd_par_vals):
    f.write(pn.rjust(10)+'  log   factor   {0:15f}    1.0e-10  1.0e+10   cond     1.000   0.000   1\n'.format(pv))
for pn,pv in zip(man_par_names,man_par_vals):
    f.write(pn.rjust(10)+'  log   factor   {0:15f}      0.020    0.090   mann     1.000   0.000   1\n'.format(pv))
f.close()
