import os
import copy
import numpy as np
import scipy
import pylab
import pandas
import shutil
import pestUtil
'''converts chl mg/l to relative concentrations
   converts spec uS/m to relative concetrations by regressing against chl
'''

def get_trendline(xs,ys,params=False):
    m,b = scipy.polyfit(xs,ys,1)
    ys_trend = (m * xs) + b
    if params:
        return xs,ys_trend,m,b
    else:
        return xs,ys_trend

def parse_smp_filename(filename):
    raw = file.split('.')[:-1]
    parsed = {'agency':raw[0],'site_no':raw[1],'name':raw[2],'param':raw[3]}
    return parsed

def build_smp_filename(dict):
    fname = dict['agency']+'.'+dict['site_no']+'.'+dict['name']+'.'+dict['param']+'.smp'
    return fname

#--chloride concentration of seawater - to scale concentrations
chl_seawater = 19400.0 #mg/l


#--get a list of all the raw smp file
smp_in_dir = 'raw_smp\\'
smp_out_dir = 'smp_chl_mgl\\'
smp_files = os.listdir(smp_in_dir)

#--regressed spec 2 chl data output dir
smp_regress_dir = 'smp_chl_mgl_regressed\\'


#--parse the file names into dicts of attributes
parsed_smp_names = []
for file in smp_files:
    parsed = parse_smp_filename(file) 
    parsed_smp_names.append(parsed)


#--group files by site_no
grouped_idx = {}
for i,[file,attributes] in enumerate(zip(smp_files,parsed_smp_names)):
    if attributes['site_no'] not in grouped_idx.keys():
        grouped_idx[attributes['site_no']] = [i]
    else:
        grouped_idx[attributes['site_no']].append(i)


#--look for sites with salt data
spec_chl_idxs = {}
tds_chl_idxs = {}
salt_params = ['chloride','spec','dissovled']
for site_no,idxs in grouped_idx.iteritems():
    site_salt_params = []
    site_salt_idxs = []
    for idx in idxs:
        if parsed_smp_names[idx]['param'] in salt_params:
            site_salt_params.append(parsed_smp_names[idx]['param'])
            site_salt_idxs.append(idx)
    #--check for different types of salt data
    if len(site_salt_params) > 1:
        #--for spec and chlorida
        if 'spec' in site_salt_params and 'chloride' in site_salt_params:
            spec_chl_idxs[site_no] = [site_salt_idxs[site_salt_params.index('spec')],site_salt_idxs[site_salt_params.index('chloride')]]
        if 'dissolved' in site_salt_params and 'chloride' in site_salt_params:
            tds_chl_idxs[site_no] = [site_salt_idxs[site_salt_params.index('dissolved')],site_salt_idxs[site_salt_params.index('chloride')]]


#--load the paired salt files and look for data on the same day
spec_data,chl_data = [],[]
dfs = []
site_nos = []
for site_no,idxs in spec_chl_idxs.iteritems():
    print 'loading smp files:',smp_files[idxs[0]],smp_files[idxs[1]]
    spec_smp = pestUtil.smp(smp_in_dir+smp_files[idxs[0]],load=True,pandas=True)
    chl_smp = pestUtil.smp(smp_in_dir+smp_files[idxs[1]],load=True,pandas=True)
    #--filter obvious outliers
    for dt,val in spec_smp.records['site'].iteritems():
        if val > 50000:
           spec_smp.records['site'][dt] = np.NaN
    df = pandas.DataFrame({'spec':spec_smp.records['site'],'chl':chl_smp.records['site']})    
    df = df.dropna()
    if not df.empty:
        dfs.append(df)
        site_nos.append(site_no)
       
df = pandas.concat(dfs,keys=site_nos) 

#--calc a filtered global regression equation
x,y = df['spec'].values.astype(np.float64),df['chl'].values.astype(np.float64)
xt,yt,m,b = get_trendline(x,y,params=True)

#--errors
ye = y - yt
ye_mean = np.mean(ye)
ye_std = np.std(ye)

#--remove values that are greater than 2 stds from mean error and a spec value greater than 1000 uS/cm
x_filt,y_filt = [],[]
for i,(xx,yy,yye) in enumerate(zip(x,y,ye)):
    #if np.abs(yye - ye_mean) <= ye_std * 2 and xx > 1000.0:
    x_filt.append(xx)
    y_filt.append(yy)
x_filt = np.array(x_filt)
y_filt = np.array(y_filt)

#--bin the data
bins = np.linspace(x_filt.min(),x_filt.max(),50)
bin_idxs = np.digitize(x_filt,bins)
x_bin,y_bin = [],[]
for i in range(len(bins)):
    x_mean = x_filt[bin_idxs==i].mean()
    y_mean = y_filt[bin_idxs==i].mean()
    x_bin.append(x_mean)
    y_bin.append(y_mean)
x_bin = np.array(x_bin)
y_bin = np.array(y_bin)
x_bin[0] = 0.0
y_bin[0] = 0.0

#--rerun the regression
#xt_filt,yt_filt,m,b = get_trendline(x_filt,y_filt,params=True)
xt_bin,yt_bin,m,b = get_trendline(x_bin,y_bin,params=True)
f = open('spec_chl_regress_parameters.dat','w')
f.write('slope,offset\n{0:23.16E},{1:23.16E}\n'.format(m,b))
f.close()

#--write chloride equivalent smp files for specific conductance site
for i,[file,attributes] in enumerate(zip(smp_files,parsed_smp_names)):
    if attributes['param'] == 'spec':
        #--load the data and filter
        smp = pestUtil.smp(smp_in_dir+file,load=True)        
        smp.records['site'][:,1] = (m * smp.records['site'][:,1]) + float(b)
        print
               
        #--build a new smp file name
        new_attributes = copy.deepcopy(attributes)
        new_attributes['param'] = 'chloride'
        new_name = build_smp_filename(new_attributes)
        
        #--load the data and filter
        smp = pestUtil.smp(smp_in_dir+file,load=True)        
        #--regress spec to chl
        smp.records['site'][:,1] = (m * smp.records['site'][:,1]) + float(b)
        #--if predicted chl value is less than zero
        smp.records['site'][np.where(smp.records['site'][:,1]<0.0),1] = 0
        #--if predicted chl value is greater than seawater - no hyper salinity
        #smp.records['site'][np.where(smp.records['site'][:,1]>=chl_seawater),1] = chl_seawater
        
        #--if an smp file with this name already exists, left merge the existing chl data with the regression predicted chl data
        #if new_name in smp_files:           
        #    print
        #    #--load the existing chloride record
        #    smp_other = pestUtil.smp(smp_in_dir+new_name,load=True)            
        #    smp_other.merge(smp,how='left')
        #    smp_other.save(smp_out_dir+new_name)
        #    parsed_smp_names.pop(smp_files.index(new_name))
        #    smp_files.pop(smp_files.index(new_name))
        #                                                  
        #else:
        #    smp.save(smp_out_dir+new_name)
        smp.save(smp_regress_dir+new_name)

#--transfer all of the existing chl files that weren't merged into the out dir
for i,[file,attributes] in enumerate(zip(smp_files,parsed_smp_names)):
    if attributes['param'] == 'chloride':
        shutil.copy(smp_in_dir+file,smp_out_dir+file)

 
#fig = pylab.figure()
#ax = pylab.subplot(211)
##ax.plot(x,y,'bo')
#ax.plot(x_filt,y_filt,'b.')
#ax.plot(xt_filt,yt_filt,'b--')
#ax.plot(x_bin,y_bin,'r.')
#ax.plot(xt_bin,yt_bin,'r--')


#ax.set_xlabel('spec')
#ax.set_ylabel('chl')

#ax2 = pylab.subplot(212)
#ax2.hist(y_filt - yt_filt,bins=20)
#ymin,ymax = ax2.get_ylim()
#ax2.plot([ye_mean,ye_mean],[ymin,ymax],'k-')
#ax2.plot([ye_mean-ye_std,ye_mean-ye_std],[ymin,ymax],'k--')
#ax2.plot([ye_mean+ye_std,ye_mean+ye_std],[ymin,ymax],'k--')
#ax2.plot([ye_mean-(2*ye_std),ye_mean-(2*ye_std)],[ymin,ymax],'k--')
#ax2.plot([ye_mean+(2*ye_std),ye_mean+(2*ye_std)],[ymin,ymax],'k--')

#pylab.show()


