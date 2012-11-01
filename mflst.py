import os
import re
from datetime import datetime,timedelta
import numpy as np
import pandas


class lstbudget():
    def __init__(self,file_name):
        raise Exception('base class lstbudget does not have a constructor - must call a derived class')
        
    
    def to_pandas(self):
        '''creates flux and vol dataframes with a multiindex of entry order (in list file) and (in,out)
        '''
        tss,sps = [],[]
        for ts,sp,seekpoint in self.idx_map:
            tss.append(ts)
            sps.append(sp)

        df_flux,df_vol = None,None
        if self.flux:
            in_dict = {}
            out_dict = {}
            for entry,record in self.flux.iteritems():
                in_dict[entry] = record[0]
                out_dict[entry] = record[1]
            df_in = pandas.DataFrame(in_dict,index=[tss,sps])
            df_out = pandas.DataFrame(out_dict,index=[tss,sps])            
            df_flux = pandas.concat([df_in,df_out],axis=1,keys=('in','out'))
        if self.cumu:
            in_dict = {}
            out_dict = {}
            for entry,record in self.cumu.iteritems():
                in_dict[entry] = record[0]
                out_dict[entry] = record[1]
            df_in = pandas.DataFrame(in_dict,index=[tss,sps])
            df_out = pandas.DataFrame(out_dict,index=[tss,sps])            
            df_vol = pandas.concat([df_in,df_out],axis=1,keys=('in','out'))
                    
        return df_flux,df_vol

                

    def build_index(self,maxentries):
        print 'building index...'
        self.idx_map = self.get_index(maxentries)
        print '\ndone - found',len(self.idx_map),'entries'

    def get_index(self,maxentries):        
        #--parse throught the file looking for matches and parsing ts and sp
        idxs = []
        l_count = 1
        while True:
            seekpoint = self.f.tell()
            line = self.f.readline()
            if line == '':
                break                   
            if self.lstkey.match(line.strip()) != None:                
                for l in range(self.tssp_lines):
                    line = self.f.readline()
                try:
                    ts,sp = self.get_ts_sp(line)
                except:
                    print 'unable to cast ts,sp on line number',l_count,' line: ',line
                    break
                print 'info found for timestep stress period',ts,sp,'\r',
                idxs.append([ts,sp,seekpoint])                
                if maxentries and len(idxs) >= maxentries:
                    break
#------------------testing------------------                
                #if sp == 10:
                #    break
        return idxs

    def get_ts_sp(self,line):
        ts = int(line[self.ts_idxs[0]:self.ts_idxs[1]])
        sp = int(line[self.sp_idxs[0]:self.sp_idxs[1]])
        return ts,sp

    def set_entries(self):
        if self.entries:
            raise Exception('entries already set'+str(self.enties))                                                      
        if not self.idx_map:
           raise Exception('must call build_index before call set_entries')    
        try:
            influx,incu,outflux,outcu = self.get_sp(self.idx_map[0][0],self.idx_map[0][1],self.idx_map[0][2])   
        except:
            raise Exception('unable to read budget information from first entry in list file')
        self.entries = influx.keys()
        null_entries = {}
        for entry in influx.keys():
            self.flux[entry] = [[],[]]
            self.cumu[entry] = [[],[]]
            null_entries[entry] = np.NaN
        self.null_entries = [null_entries,null_entries,null_entries,null_entries]

    
    def load(self,maxentries=None):                
        self.build_index(maxentries)
        self.set_entries()
                
        for ts,sp,seekpoint in self.idx_map:
            #print 'loading stress period, timestep',sp,ts

            influx,incu,outflux,outcu = self.get_sp(ts,sp,seekpoint)  
            for entry in self.entries:
                self.flux[entry][0].append(influx[entry])
                self.flux[entry][1].append(outflux[entry])
                self.cumu[entry][0].append(incu[entry])      
                self.cumu[entry][1].append(outcu[entry])                                         
        return

    
    def get_sp(self,ts,sp,seekpoint):                
        self.f.seek(seekpoint)
        #--read to the start of the "in" budget information
        while True:
            line = self.f.readline()
            if line == '':
                #raise Exception('end of file found while seeking budget information') 
                print 'end of file found while seeking budget information for ts,sp',ts,sp
                return self.null_entries
                   
            #--if there are two '=' in this line, then it is a budget line
            if len(re.findall('=',line)) == 2:
                break
                    
        infx,incu = {},{}        
        while True:
            
            if line == '':
                #raise Exception('end of file found while seeking budget information')
                print 'end of file found while seeking budget information for ts,sp',ts,sp
                return self.null_entries
            if line == '\n' or len(re.findall('=',line)) != 2:
                break
            try:
                entry,flux,cumu = self.parse_budget_line(line)                  
            except e:
                print 'error parsing budget line in ts,sp',ts,sp
                return self.null_entries
            if flux is None:
                print 'error casting in flux for',entry,' to float in ts,sp',ts,sp
                return self.null_entries
            if cumu is None:
                print 'error casting in cumu for',entry,' to float in ts,sp',ts,sp
                return self.null_entries
            infx[entry] = flux
            incu[entry] = cumu
            line = self.f.readline()

        #--read to the start of the "OUT" budget information
        while True:
            line = self.f.readline()
            if line == '':
                #raise Exception('end of file found while seeking budget information')
                print 'end of file found while seeking budget information'
                return self.null_entries
            if len(re.findall('=',line)) == 2 and 'TOTAL' not in line.upper():
                break                
        outfx,outcu = {},{}
        while True:
            
            if line == '':
                #raise Exception('end of file found while seeking budget information')
                print 'end of file found while seeking budget information'
                return self.null_entries
            if line == '\n' or len(re.findall('=',line)) != 2:
                break
            try:
                entry,flux,cumu = self.parse_budget_line(line)                  
            except e:
                print 'error parsing budget line in ts,sp',ts,sp
                return self.null_entries
            if flux is None:
                print 'error casting out flux for',entry,' to float in ts,sp',ts,sp
                return self.null_entries
            if cumu is None:
                print 'error casting out cumu for',entry,' to float in ts,sp',ts,sp
                return self.null_entries                    
            outfx[entry] = flux
            outcu[entry] = cumu  
            line = self.f.readline()                  
                
        return infx,incu,outfx,outcu
 
    
    def parse_budget_line(self,line):
        raw = line.strip().split()
        entry = line.strip().split('=')[0].strip()            
        cu_str = line[self.cumu_idxs[0]:self.cumu_idxs[1]]
        fx_str = line[self.flux_idxs[0]:self.flux_idxs[1]]
        flux,cumu = None,None
        try:
            cumu = float(cu_str)
        except:
            if 'NAN' in cu_str.strip().upper():
                cumu = np.NaN               
        try:
            flux = float(fx_str)
        except:
            if 'NAN' in fx_str.strip().upper():
                flux = np.NaN         
        return entry,flux,cumu            
           
                  

class mfbudget(lstbudget):
    def __init__(self,file_name,key_string='VOLUMETRIC BUDGET FOR ENTIRE MODEL'):
        assert os.path.exists(file_name)
        self.file_name = file_name
        self.f = open(file_name,'r')
        self.lstkey = re.compile(key_string)                        
        self.idx_map = []
        self.entries = []
        self.null_entries = []
        self.flux = {}
        self.cumu = {} 
        self.cumu_idxs = [22,40]
        self.flux_idxs = [63,80]   
        self.ts_idxs = [56,60]
        self.sp_idxs = [76,80] 
        self.tssp_lines = 0   

class swrbudget(lstbudget):
    def __init__(self,file_name,key_string='VOLUMETRIC SURFACE WATER BUDGET FOR ENTIRE MODEL'):
        assert os.path.exists(file_name)
        self.file_name = file_name
        self.f = open(file_name,'r')
        self.lstkey = re.compile(key_string)                        
        self.idx_map = []
        self.entries = []
        self.null_entries = []
        self.flux = {}
        self.cumu = {} 
        self.cumu_idxs = [25,43]
        self.flux_idxs = [66,84]   
        self.ts_idxs = [39,46]
        self.sp_idxs = [62,68] 
        self.tssp_lines = 1  


class lsttime(lstbudget):
    '''class to extract time information from lst file
    passing a start datetime results in casting the totim to dts from start
    '''

    def __init__(self,file_name,timeunit='days',key_str='TIME SUMMARY AT END',start=None):
       
        assert os.path.exists(file_name)
        self.file_name = file_name
        self.f = open(file_name,'r')
        self.idx_map = []
        self.tslen = []
        self.sptim = []
        self.totim = []
        self.lstkey = re.compile(key_str)
        self.tssp_lines = 0
        self.ts_idxs = [42,47]
        self.sp_idxs = [63,69]
        self.time_line_idx = 20
        if timeunit.upper() =='DAYS':
            self.timeunit = 'D'
            self.time_idx = 3
        else:
            raise Exception('need to reset time_idxs attribute to use units other than days and check usage of timedelta')
        self.null_entries = [np.NaN,np.NaN,np.NaN]
        self.start = start
        if start:
            self.dt = []


    def to_pandas(self):
        tss,sps = [],[]
        for ts,sp,seekpoint in self.idx_map:
            tss.append(ts)
            sps.append(sp)

        if self.start is None:
            df = pandas.DataFrame({'tslen':self.tslen,'sptim':self.sptim,'totim':self.totim},index=[tss,sps])
        else:
            df = pandas.DataFrame({'tslen':self.tslen,'sptim':self.sptim,'totim':self.totim,'datetime':self.dt},index=[tss,sps])
        return df
    def load(self,maxentries=None):
        self.build_index(maxentries)

        for i,[ts,sp,seekpoint] in enumerate(self.idx_map):
            #print 'loading stress period, timestep',sp,ts,

            tslen,sptim,totim = self.get_sp(ts,sp,seekpoint)  
            self.tslen.append(tslen)
            self.sptim.append(sptim)
            self.totim.append(totim)               
        if self.start is not None:
            self.dt = self.cast_totim()
            
        return

    def cast_totim(self):
        if self.timeunit == 'D':
            totim = []
            for to in self.totim:
                t = timedelta(days=to)
                totim.append(self.start + t)
        return totim

    def get_sp(self,ts,sp,seekpoint):
        self.f.seek(seekpoint)
        #--read two lines
        for i in range(3):
            line = self.f.readline()
            if line == '':
                #raise Exception('end of file found while seeking budget information') 
                print 'end of file found while seeking time information for ts,sp',ts,sp
                return self.null_entries
        tslen = self.parse_time_line(self.f.readline())
        if tslen == None:
            print 'error parsing tslen for ts,sp',ts,sp
            return self.null_entries
        
        sptim = self.parse_time_line(self.f.readline())
        if sptim == None:
            print 'error parsing sptim for ts,sp',ts,sp
            return self.null_entries

        totim = self.parse_time_line(self.f.readline())
        if totim == None:
            print 'error parsing totim for ts,sp',ts,sp
            return self.null_entries
        return tslen,sptim,totim

    def parse_time_line(self,line):
        if line == '':
            print 'end of file found while parsing time information'
            return None
        try:
            time_str = line[self.time_line_idx:]
            raw = time_str.split()        
            tval = float(raw[self.time_idx])            
        except:
            print 'error parsing tslen information',time_str
            return None        
        return tval
        

        
    