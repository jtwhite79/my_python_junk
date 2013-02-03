import numpy as np  

class ulist():
    def __init__(self,ncol,lrc,value,aux_strings=None,name=None):        
        self.ncol = ncol
        self.lrc = self.parse_lrc(lrc)                               
        self.__value = self.parse_value(value)
        if aux_strings:
            self.aux_strings = self.parse_aux_strings(aux_strings)
        else:
            self.aux_strings = None
        print
        

    def __getitem__(self,kper):                
        #--lrc 
        if len(self.lrc) < kper or self.lrc[kper] is None:
            #--find the last entry
            for lrcs in self.lrc[::-1]:
                if lrcs is not None:
                    break
        else:
            lrcs = self.lrc[kper]
        #--values 
        vals = []
        for idata,data in enumerate(self.__value):
            if len(data) < kper or data[kper] is None:
                for d in data[::-1]:
                    if d is not None:
                        break
            else:
                d = data[kper]
            vals.append(d)
        #--aux_strings
        if self.aux_strings is not None:
            if len(self.aux_strings) < kper or self.aux_strings[kper] is None:
                for aux in self.aux_strings[::-1]:
                    if aux is not None:
                        break
            else:
                aux = self.aux_strings[kper]
        else:
            aux = ''
        #--tile out single values or check there are the right number of entries        
        for i,val in enumerate(vals):  
            if np.isscalar(val):
                vals[i] = [val] * len(lrcs)
            else:                                                                          
                assert len(val) == len(lrcs)
        if isinstance(aux,str):
            aux = [aux] * len(lrcs)
        else:
            assert len(aux) == len(lrcs)
    
        #--write lines
        lines = []
        for lrc,val,aux_string in zip(lrcs,zip(*vals),aux):
            line = ' {0:9d} {1:9d} {2:9d}'.format(*lrc)
            for v in val:
                line += ' {0:15.7G}'.format(v)
            line += ' '+aux_string
            lines.append(line)

        return '\n'.join(lines)        

    def build_fmt(self):
        fmt = ' {0:9d} {1:9d} {2:9d}'
        for i,dt in enumerate(self.dtype):
            f = ' {'+str(i+3)+':'+FMT_DICT[dt]+'}'
            fmt += f
        return fmt
        
    def parse_dtype(self,dtype):
        if not isinstance(dtype,list) and not isinstance(dtype,tuple):
            dtype = [dtype]
        for dt in dtype:
            assert dt in self.acceptable_types,'util_list: unsupported type in dtype: '+str(dt)
        return dtype


    def parse_aux_strings(self,aux_strings):
        #--if a string or scalar, then all nper, all kij get the same aux
        if isinstance(aux_strings,str) or np.isscalar(aux_strings):
            aux_strings = [str(aux_strings)]
        else:
            for iper,kper_entry in enumerate(aux_strings):            
                if kper_entry is None:
                        aux_strings[iper] = None
                else:
                    if isinstance(kper_entry,str) or np.isscalar(kper_entry):
                        aux_strings[iper] = str(kper_entry)
                    else:
                        for i,entry in enumerate(kper_entry):                                
                            aux_strings[iper][i] = str(entry)                
        return aux_strings
    
    def parse_lrc(self,lrc):     
        for iper,kper_entry in enumerate(lrc):            
            if kper_entry is None:
                    lrc[iper] = None
            else:
                for i,entry in enumerate(kper_entry):                                
                    assert len(entry) == 3
                    l,r,c = np.int(entry[0]),np.int(entry[1]),np.int(entry[2])
                    lrc[iper][i] = (l,r,c)
                lrc[iper] = np.array(lrc[iper])
        return lrc
    
    def parse_value(self,value):
        #--a little trickery
        if self.ncol == 1 and len(value) != 1:
            value = [value]        
        assert len(value) == self.ncol
        for idata,data_entry in enumerate(value):  
            #--if a scalar or string here, then all kper, all kij gets the same value
            if isinstance(data_entry,str) or np.isscalar(data_entry):
                
                value[idata] = [np.float32(data_entry)]
            else:    
                for iper,kper_entry in enumerate(data_entry):
                    if kper_entry is None:
                        entry = None
                    if isinstance(kper_entry,str) or np.isscalar(kper_entry):                    
                        entry = np.float32(kper_entry)
                    elif isinstance(kper_entry,list):
                        entry = np.array(kper_entry,dtype=np.float32)
                    elif isinstance(kper_entry,np.ndarray):
                        entry = kper_entry.astype(np.float32)   
                    value[idata][iper] = entry                             
        return value
                    


        