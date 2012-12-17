import os
import shutil
from datetime import datetime
import zipfile
import numpy as np
import pandas

dirs =  ['NEXRAD','PET','RET']
uzd = '_unzipped\\' 
for d in dirs:
    print 'processing ',d

    if os.path.exists(d+uzd):
        shutil.rmtree(d+uzd)
    files = os.listdir(d)   
    os.mkdir(d+uzd)
    print 'unzipping..'
    for f in files:
        #--unzip 
        z = zipfile.ZipFile(d+'\\'+f)
        z.extractall(path=d+uzd)
    print 'done'
    print 'loading datafiles into dataframes...'
    #--get a list of unzipped files
    data_files = os.listdir(d+uzd)
    
    dfs = []
    for dfile in data_files:  
        print dfile              
        f = open(d+uzd+dfile,'r')
        pix_vals,pix_dts = {},{}

        for line in f:
            raw = line.strip().split()
            dt = datetime.strptime(raw[1],'%m/%d/%Y')            
            val = float(raw[2])
            pix = int(raw[0])
            if pix not in pix_vals.keys():
                pix_vals[pix] = [val]
                pix_dts[pix] = [dt]
            else:
                pix_vals[pix].append(val)
                pix_dts[pix].append(dt)                
        f.close()
        failed = []
        for p1 in pix_dts.keys():
            for p2 in pix_dts.keys():
                if len(pix_dts[p1]) != len(pix_dts[p2]):
                    failed.append(str(p1)+','+str(p2))
        if len(failed) > 0:
            print 'missing data',str(failed)
        df = pandas.DataFrame(pix_vals,index=pix_dts[p1])
        dfs.append(df)
    df = pandas.concat(dfs,axis=0)
    df.to_csv(d+'.csv')

    
