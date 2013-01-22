import sys
import numpy as np  
import pestUtil


#----------------------------------------------------------------
#--load the BLU csv and write white-space equivalent and TPL file
#--output formats - tied to the tpl format 
txt_fmt = ' {0:>35}'
real_fmt = ' {0:35.8E}'
int_fmt = ' {0:35.0f}'
fname = 'setup_files\\UMD_SFWMM_ETParameters.csv'
f = open(fname,'r')
header = f.readline().strip().split(',')
#lines = [txt_fmt.format('name')+txt_fmt.format('x')+txt_fmt.format('y')]
lines = [txt_fmt.format('BLU_CODE')]
tpl_lines = ['ptf ~',txt_fmt.format('BLU_CODE')]
blu_codes,blu_idx = [],0
#tpl_lines.append(txt_fmt.format('name')+txt_fmt.format('x')+txt_fmt.format('y'))

par_cols = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
par_names = ['ETSX','PSEG01','PSEG02','PETM01','PETM02','PETM03','PETM04','PETM05','PETM06','PETM07','PETM08','PETM09','PETM10','PETM11','PETM12']
par_count = []
for p in par_cols:
    par_count.append(1)
    #par_names.append(header[p]+'_')
for i,h in enumerate(header):
    if i in par_cols:
        lines[-1] += txt_fmt.format(h)
        tpl_lines[-1] += txt_fmt.format(h)

#lines.append(txt_fmt.format('none')+txt_fmt.format('none')+txt_fmt.format('none'))
#tpl_lines.append(txt_fmt.format('none')+txt_fmt.format('none')+txt_fmt.format('none'))
lines.append(txt_fmt.format('none'))
tpl_lines.append(txt_fmt.format('none'))
for i,h in enumerate(header):
    if i in par_cols:
        p = par_names[par_cols.index(i)]
        lines[-1] += txt_fmt.format('UMD.01\\ref\\UMD_ETS_'+p+'.ref')
        tpl_lines[-1] += txt_fmt.format('UMD.01\\ref\\UMD_ETS_'+p+'.ref')
    #else:
    #    lines[-1] += txt_fmt.format('none')
    #    tpl_lines[-1] += txt_fmt.format('none')
pst_names = {}
for line in f:
    raw = line.strip().split(',')
    blu_codes.append(int(raw[blu_idx]))
    #lines.append(txt_fmt.format(str(l))+real_fmt.format(0.0)+real_fmt.format(0.0))
    #tpl_lines.append(txt_fmt.format('blu'+str(l))+real_fmt.format(0.0)+real_fmt.format(0.0))  
    lines.append('')
    tpl_lines.append('')    
    for i,r in enumerate(raw):
        
        #--if this is a parameter col, then write a tpl entry
        if i in par_cols:
            val = float(r)
            lines[-1] += real_fmt.format(val)
            pidx = par_cols.index(i)
            #par_name = par_names[pidx]+'{0:02.0f}'.format(par_count[pidx])
            par_name = par_names[pidx]+'{0:02.0f}'.format(blu_codes[-1])
            par_name = par_name.replace('_','')
            pst_names[par_name] = val
            if len(par_name) > 10:
                par_name = par_name[len(par_name)-10:]               
            elif len(par_name) < 10:
                while len(par_name) < 10:
                    par_name = ' '+par_name            
            tpl_entry = ' ~         '+par_name+'              ~'
            tpl_lines[-1] += tpl_entry
            print len(par_name),len(tpl_entry)
            par_count[pidx] += 1
        #--otherwise, just cast and write
        elif i == 0:
            val = int(r)
            lines[-1] += int_fmt.format(val)
            tpl_lines[-1] += int_fmt.format(val)
        
f.close()
f = open('par\\blu_parameters.dat','w')
for line in lines:
    f.write(line+'\n')
f.close()

f = open('tpl\\blu_parameters.tpl','w')
for line in tpl_lines:       
    f.write(line+'\n')
f.close()    


pnames = pst_names.keys()
pnames.sort()
f = open('pst_components\\blu_params.dat','w')
for p in pnames:
    val = pst_names[p]
    f.write(p.ljust(20)+'   log  factor  {0:20.8E}'.format(val)+'  1.0E-10   1.0E+10\n')    
f.close()


sys.exit()


#-------------------------------------------------------------------
#--NOT USED...


#----------------------------------------------------------------------
#--write a fake factors file for the BLU array

#--load the grid info
ginfo = pestUtil.load_grid_spec('misc\\grid.spc')

#--load the blu array
grp_arr = np.loadtxt('setup_files\\UMD_BLU.ref')

#--write a mapped blu array sinec the blu codes aren't ordered or continous - needed since the factors file is in the order of occurence
grp_arr_mapped = np.zeros_like(grp_arr) - 999
for i,code in enumerate(blu_codes):
    grp_arr_mapped[np.where(grp_arr==code)] = i + 1
np.savetxt('ref\\UMD_BLU_mapped.ref',grp_arr_mapped,fmt=' %2.0f')

    
num_grps = np.unique(grp_arr).shape[0]
f = open('fac\\blu_fac.dat','w')
f.write('cl_blu\n')
f.write('cl_mf_grid\n')
f.write('{0:10.0f}{1:10.0f}\n'.format(1,num_grps))
f.write('{0:10.0f}{1:10.0f}\n'.format(1,ginfo['nrow']*ginfo['ncol']))
f.write('{0:10.0f}{1:10.0f}\n'.format(num_grps,ginfo['nrow']*ginfo['ncol']))
f.write('{0:10.0f}\n'.format(1))

cell_num = 1         
for i in range(ginfo['nrow']):
    for j in range(ginfo['ncol']):
        #print i,j,grp_arr[i,j]
        f.write('{0:6.0f} {1:5.0f} {2:10.4E} {3:10.0f} {4:10.4E}\n'.format(cell_num,1,0.0,grp_arr_mapped[i,j],1.0))
        cell_num += 1
f.close()



#--write a portion of the plproc input file
f = open('setup_files\\plproc_blu_part.in','w')
f.write('\n\n\n#-----------------------------------------------------\n')
f.write('#--BLU processing\n')
f.write('#-----------------------------------------------------\n')
line1 = 'cl_blu = read_list_file(dimensions=2,id_type="character",skiplines=1,file="par\\blu_parameters.dat",&\n'
f.write(line1)
for pname,pcol in zip(par_names,par_cols):
    
    f.write(' '.ljust(30)+'plist=\"pl_'+pname+'";column='+str(pcol+4)+',&\n')
f.write(' '.ljust(30)+')\n\n')
#pl_grid = pl_nxpts_jan.krige_using_file(file='nex_fac.dat',transform='none', &         
#                                      lower_limit=1.0e-10,upper_limit=1.0e+10)         
#write_model_input_file(template_file='pp_ref.tpl',model_input_file='ref\\nx_jan.ref')  
f.write('\n\n#--assign values to grid using fake factors\n\n')

for pname in par_names:
    
    f.write('pl_grid = pl_'+pname+'.krige_using_file(file="fac\\blu_fac.dat",transform="none", &\n'+' '.ljust(40)+'lower_limit=-1.0e+10,upper_limit=1.0e+10)\n')
    f.write('write_model_input_file(template_file="tpl\\pp_ref.tpl",model_input_file="ref\\UMD_ETS_'+pname+'.ref")\n\n')  
f.close()

       

