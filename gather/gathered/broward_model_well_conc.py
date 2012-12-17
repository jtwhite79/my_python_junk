import os
import numpy as np
import pandas
import MFBinaryClass as mfb
from bro import seawat

def parse_list_line(line):
    raw = line.strip().split()
    k = int(raw[0]) - 1
    i = int(raw[1]) - 1
    j = int(raw[2]) - 1
    flux = float(raw[3])
    wname = raw[4].replace('#','')
    return (k,i,j),flux,wname



#--load a list of well info
well_kij = {}
well_conc = {}
well_flux = {}
files = os.listdir(seawat.list_dir)
for file in files:
    if 'WEL_' in file.upper():
        kijs,wnames = [],[]
        f = open(seawat.list_dir+file,'r')
        for line in f:
            kij,flx,wname = parse_list_line(line)            
            kijs.append(kij)
            wnames.append(wname)
            if wname in well_kij.keys():
                well_kij[wname].append(kij)
            else:
                well_kij[wname] = [kij]
                well_conc[wname] = []
                well_flux[wname] = []
        f.close()
        break

cbc_file = seawat.root+'_wel.cbc'
cbc_obj = mfb.MODFLOW_CBB(seawat.nlay,seawat.nrow,seawat.ncol,cbc_file,aslist=True)
flux_type = '           WELLS'

conc_file = 'MT3D001.UCN'
conc_obj = mfb.MT3D_Concentration(seawat.nlay,seawat.nrow,seawat.ncol,conc_file)

f_smp = open('test.smp','w',0)
date_fmt = '%d/%m/%Y'
time = '12:00:00'
for itime,end in enumerate(seawat.sp_end):
    ctotim,conc,kstp,kper,csuccess = conc_obj.next()
    flux,ftotim,fsuccess = cbc_obj.read_next_fluxtype(flux_type)   
    #nnz_kijs = []
    #for i in range(seawat.nrow):
    #    for j in range(seawat.ncol):
    #        for k in range(seawat.nlay):
    #            if flux[k,i,j] != 0.0:
    #                print k,i,j, flux[k,i,j]
    #                nnz_kijs.append((k,i,j))
    if not csuccess or not fsuccess:
        break
    if kper != itime+1:
        raise Exception('cbc kper not the same as loop kper')
    if ctotim != ftotim:
        raise Exception('cbc totim not the same as conc totim')

    for wname,kijs in well_kij.iteritems():
        tot_mass,tot_fx = 0.0,0.0
        for k,i,j in kijs:            
            cn = conc[k,i,j]
            fx = flux[1][flux[0].index((k+1,i+1,j+1))]           
            tot_mass += (cn * fx)
            tot_fx += fx
        if tot_fx != 0.0:
            avg_conc = tot_mass / tot_fx
        else:
            avg_conc = 0.0
        f_smp.write(wname+'  '+end.strftime(date_fmt)+' '+time+' {0:20.8E}\n'.format(avg_conc))
        well_conc[wname].append(avg_conc)
        well_flux[wname].append(tot_fx)
f_smp.close()

df_conc = pandas.DataFrame(well_conc,index=seawat.sp_end)
df_conc.sort_index(axis=0,inplace=True)
df_conc.to_csv('well_conc.csv',index_label='datetime')


