import numpy as np
import pandas
import pylab
import MFBinaryClass as mfb

from bro import seawat as cal
from bro_pred import seawat as pred

def apply():

    #--calibration
    keyfile = 'misc\\bro.03_calibration_seawatlist.key'
    key_well,key_wfield = {},{}
    wconc,wfconc,wfflux,wfmass = {},{},{},{}
    f = open(keyfile,'r')
    for line in f:
        if 'wel' in line:
            raw = line.strip().split()
            kij = (int(raw[1])-1,int(raw[2])-1,int(raw[3])-1)
            if raw[0] in key_wfield.keys() :
                if kij not in key_wfield[raw[0]]:
                    key_wfield[raw[0]].append(kij)
            else:
                key_wfield[raw[0]] = [kij]
                wfconc[raw[0]] = []
                wfflux[raw[0]] = []
                wfmass[raw[0]] = []
            
            if raw[4] in key_well.keys():
                key_well[raw[4]].append(kij)
            else:
                key_well[raw[4]] = [kij]                    
                wconc[raw[4]] = []                 
                                                                
    path = 'bro.03\\calibration\\'    
    cbc_file = path+cal.root+'_wel.cbc'
    cbc_obj = mfb.MODFLOW_CBB(cal.nlay,cal.nrow,cal.ncol,cbc_file)
    flux_type = '           WELLS'
    conc_file = path+'MT3D001.UCN'
    conc_obj = mfb.MT3D_Concentration(cal.nlay,cal.nrow,cal.ncol,conc_file)
    dts = []
    for itime,end in enumerate(cal.sp_end):
        print end,'\r',
        ctotim,conc,kstp,kper,csuccess = conc_obj.next()
        flux,ftotim,fsuccess = cbc_obj.read_next_fluxtype(flux_type)   
        
        if not csuccess:
            #raise Exception('Error reading binary file: '+str(conc_file))
            break
        if not fsuccess:
            #raise Exception('Error reading binary file: '+str(cbc_file))
            break
        if kper != itime+1:
            #raise Exception('cbc kper not the same as loop kper')
            break
        if ctotim != ftotim:
            #raise Exception('cbc totim not the same as conc totim')
            break
        dts.append(end)
        #--individual wells - max concetration at any node for active wells
        for wname,kijs in key_well.iteritems():
            max_conc,max_flux = 0.0,0.0
            for (k,i,j) in kijs:            
                cn = conc[k,i,j]
                fx = np.abs(flux[k,i,j])
                if fx > 0.0 and cn > max_conc:
                    max_conc = cn
                    max_flux = fx
            if max_flux != 0.0:                            
                wconc[wname].append(max_conc) 
            else:
                wconc[wname].append(np.NaN)                                   
        
        #-- well fields
        for wname,kijs in key_wfield.iteritems():
            tot_mass,tot_fx = 0.0,0.0
            for (k,i,j) in kijs:            
                cn = conc[k,i,j]                    
                fx = np.abs(flux[k,i,j])
                tot_mass += (cn * fx)
                tot_fx += fx
            if tot_fx > 0.0:
                avg_conc = tot_mass / tot_fx
                
            else:
                avg_conc = np.NaN
                tot_mass = np.NaN                

            wfconc[wname].append(avg_conc)
            wfflux[wname].append(tot_fx)
            wfmass[wname].append(tot_mass)

    df_wconc = pandas.DataFrame(wconc,index=dts)
    df_wconc.to_csv('calibration_wconc.csv')
    
    df_wfconc = pandas.DataFrame(wfconc,index=dts)
    df_wfconc.to_csv('calibration_wfconc.csv')
    df_wfmass = pandas.DataFrame(wfmass,index=dts)
    df_wfmass.to_csv('calibration_wfmass.csv')

        
def setup():
    pass

def plot():
    
    
    potable = 0.014
    near_zero = 1.0e-20

    #--calibration

    #--well field mass and average concentration
    wfield_mass_org = pandas.read_csv('calibration_wfmass.csv',index_col=0,parse_dates=True)
    wfield_conc_org = pandas.read_csv('calibration_wfconc.csv',index_col=0,parse_dates=True)
    wfdict = {}
    for wfield in wfield_mass_org.keys():
        wfdict[wfield] = np.NaN
    wfield_mass = pandas.DataFrame(wfdict,index=cal.sp_end)
    wfield_mass = wfield_mass.combine_first(wfield_mass_org)

    wfield_conc = pandas.DataFrame(wfdict,index=cal.sp_end)
    wfield_conc = wfield_conc.combine_first(wfield_conc_org)
       
    figdir = 'png\\well_conc\\wfield\\'
    for wname in wfield_mass.keys():
        mass_rec = wfield_mass[wname]
        conc_rec = wfield_conc[wname]
        if (mass_rec.max() > near_zero):
            print wname,'\r',
            fig = pylab.figure(figsize=(8,4))
            ax = pylab.subplot(111)
            axt = pylab.twinx()
            ax.plot(mass_rec.index,mass_rec.values,'k-')                    
            axt.plot(conc_rec.index,conc_rec.values,'g-')                    
            ax.grid()
            ax.set_title('well field: '+str(wname))
            figname = figdir + str(wname) + '_mass.png'
            pylab.savefig(figname,fmt='png',dpi=300,bbox_inches='tight')

    return


    #--inidividutal well concs
    well_df_org = pandas.read_csv('calibration_wconc.csv',index_col=0,parse_dates=True)

    #--tile the record out of the entire runtime
    wdict = {}
    for wname in well_df_org.keys():
        wdict[wname] = np.NaN
    

    well_df = pandas.DataFrame(wdict,index=cal.sp_end)
    well_df = well_df.combine_first(well_df_org)
         
    figdir = 'png\\well_conc\\individual\\'
    for wname,rec in well_df.iteritems():
        if (rec.max() > near_zero):
            print wname,'\r',
            fig = pylab.figure(figsize=(8,4))
            ax = pylab.subplot(111)
            ax.plot(rec.index,rec.values,'k--')
            rec[rec < potable] = np.NaN
            ax.plot(rec.index,rec.values,'r-')
            ax.plot([rec.index[0],rec.index[-1]],[potable,potable],'b--')
            ax.grid()
            ax.set_title('well: '+str(wname))
            figname = figdir + str(wname)
            pylab.savefig(figname,fmt='png',dpi=300,bbox_inches='tight')

   




if __name__ == '__main__':
    #setup()
    #apply()
    plot()
