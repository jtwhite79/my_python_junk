import os
import pylab
import pandas
import pestUtil

def build_plotname(filename):
    raw = filename.split('.')
    raw[-1] = 'png'
    return '.'.join(raw)

#--plot directory
plt_dir_navd = 'png\\navd\\'
plt_dir_conc = 'png\\conc\\'

navd_dir = 'smp_waterlevel_navd\\'
navd_files = os.listdir(navd_dir)

chl_dir = 'smp_rel_conc_chl\\'
chl_files = os.listdir(chl_dir)

spec_dir = 'smp_rel_conc_regressed\\'
spec_files = os.listdir(spec_dir)

tds_dir = 'smp_rel_conc_tds\\'
tds_files = os.listdir(tds_dir)


#--build a unique list of concentration file names
unique_files = []
for file in chl_files:
    if file not in unique_files:
        unique_files.append(file)
for file in spec_files:
    if file not in unique_files:
        unique_files.append(file)
for file in tds_files:
    if file not in unique_files:
        unique_files.append(file)
                        


empty = []
fail = []
#--first plot water levels
#for file in navd_files:
#    smp = pestUtil.smp(navd_dir+file,load=True,pandas=True)
#    if not smp.records.empty:
#        try:
#            print file            
#            title = 'number of data points = ',str(d_points)
#            ax = smp.records.plot(legend=False,grid=True,marker='.',title=title)
#            ax.set_ylabel('ft navd')
#            ax.set_xlabel('datetime')        
#            plotname = build_plotname(smp_file)
#            pylab.savefig(plt_dir_navd+plotname,fmt='png',dpi=300) 
#            pylab.close('all') 
#        except:
#            fail.append(file)          
#    else:
#        print 'empty record',file
#        empty.append(file)

#--plot relative concentration records - combined plt of chl, spec, and tds
for file in unique_files:
    files = []
    types = []
    reclens = []
    if file in chl_files:
        files.append(chl_dir+file)
        types.append('chl')
    if file in spec_files:
        files.append(spec_dir+file)
        types.append('spec')
    if file in tds_files:
        files.append(tds_dir+file)
        types.append('tds')
    smp = pestUtil.smp(files[0],load=True,pandas=True)
    smp.records[types[0]] = smp.records['site']
    smp.records.pop('site')
    reclens.append(types[0]+' '+str(len(smp.records[types[0]])))
    #--if more than one file was found
    if len(files) > 1:                
        for file,dtype in zip(files[1:],types[1:]):
            other = pestUtil.smp(file,load=True,pandas=True)
            other.records[dtype] = other.records['site']
            other.records.pop('site')
            reclens.append(dtype+' '+str(len(other.records[dtype])))
            smp.records = pandas.merge(smp.records,other.records,left_index=True,right_index=True)
            print
    
    if not smp.records.empty:
        try:
            print file  
            title = ','.join(reclens)                                  
            ax = smp.records.plot(grid=True,marker='.',title=title)
            ax.set_ylabel('relative concentration')
            ax.set_xlabel('datetime')        
            plotname = build_plotname(file.split('\\')[-1])
            pylab.savefig(plt_dir_conc+plotname,fmt='png',dpi=300) 
            pylab.close('all') 
        except:
            fail.append(file)          
    else:
        print 'empty record',file
        empty.append(file)
f = open('empty_records.dat','w')
for e in empty:
    f.write(e+'\n')
f.close()

f = open('failed_2_plot.dat','w')
for fa in fail:
    f.write(fa+'\n')
f.close()

print junk