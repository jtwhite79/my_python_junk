import numpy as np
import calendar
import shapefile
import pestUtil

#--load the grid shapefile that has the nexrad groups
shapename = 'shapes\\cwm_grid_groups'
records = shapefile.load_as_dict(shapename,['row','column','nex_group'],loadShapes=False)

#--load the grid info
ginfo = pestUtil.load_grid_spec('misc\grid.spc')

#--fill in the groups array
grp_arr = np.zeros((ginfo['nrow'],ginfo['ncol']))

for r,c,g in zip(records['row'],records['column'],records['nex_group']):
    grp_arr[r-1,c-1] = g
np.savetxt('ref\UMD_nexrad.ref',grp_arr,fmt=' %2.0f')
num_grps = np.unique(grp_arr).shape[0]

f = open('fac\\nex_fac.dat','w')
f.write('cl_nexpts\n')
f.write('cl_mf_grid\n')
f.write('{0:10.0f}{1:10.0f}\n'.format(1,num_grps))
f.write('{0:10.0f}{1:10.0f}\n'.format(1,ginfo['nrow']*ginfo['ncol']))
f.write('{0:10.0f}{1:10.0f}\n'.format(num_grps,ginfo['nrow']*ginfo['ncol']))
f.write('{0:10.0f}\n'.format(1))

cell_num = 1         
for i in range(ginfo['nrow']):
    for j in range(ginfo['ncol']):
        #print i,j,grp_arr[i,j]
        f.write('{0:6.0f} {1:5.0f} {2:10.4E} {3:10.0f} {4:10.4E}\n'.format(cell_num,1,0.0,grp_arr[i,j],1.0))
        cell_num += 1
f.close()
       
#--write a generic points file for the group points and a tpl file
f = open('par\\nexrad_parameters.dat','w')
f_tpl = open('tpl\\nexrad_parameters.tpl','w')
f_tpl.write('ptf ~ \n')
#line1 = 'name'.rjust(10)+' '+'x'.rjust(10)+' '+'y'.rjust(10)
line1 = 'nxpt'.rjust(10)
months = calendar.month_abbr
txt_fmt = ' {0:>35}'
for m in months[1:]:
    line1 += txt_fmt.format(m)
f.write(line1+'\n')
f_tpl.write(line1+'\n')

line2 = 'none'.rjust(10)
i = 1
for m in months[1:]:
    ref_name = 'UMD.01\\ref\UMD_NEXRAD_MULT_'+str(i).zfill(2)+'.ref'
    line2 += txt_fmt.format(ref_name)
    i += 1
f.write(line2+'\n')
f_tpl.write(line2+'\n')

pst_params = []
for i in range(num_grps):
    #f.write('  nxpt{0:04.0f} {1:10.4E} {2:10.4E}'.format(i+1,0.0,0.0))
    f.write('{0:10.0f}'.format(i+1))
    #f_tpl.write('  nxpt{0:04.0f} {1:10.4E} {2:10.4E}'.format(i+1,0.0,0.0))
    f_tpl.write('{0:10.0f}'.format(i+1))
    for j,mon in enumerate(months[1:]):        
        print j,mon
        par_name = 'nx{0:02.0f}'.format(i+1)+'_'+mon
        pst_params.append(par_name)
        f.write(' {0:35.8E}'.format(j+1))
        f_tpl.write(' ~          '+par_name+'               ~')
    f.write('\n')
    f_tpl.write('\n')
f.close()
f_tpl.close()

pst_params.sort()
f = open('pst_components\\nexrad_params.dat','w')
for p in pst_params:
    f.write(p+'\n')
f.close()