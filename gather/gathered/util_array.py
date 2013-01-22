import os
import shutil
import copy
import numpy as np


def decode_fortran_descriptor(fd):    
    #--strip off '(' and ')'
    fd = fd.strip()[1:-1]
    if 'FREE' in fd.upper():
        return 'free',None,None,None
    elif 'BINARY' in fd.upper():
        return 'binary',None,None,None
    if '.' in fd:
        raw = fd.split('.')
        decimal = int(raw[1])
    else:
        raw = [fd]
        decimal=None
    fmts = ['I','G','E','F']
    raw = raw[0].upper()
    for fmt in fmts:
        if fmt in raw:
            raw = raw.split(fmt)
            npl = int(raw[0])
            width = int(raw[1])
            if fmt == 'G':
                fmt = 'E'
            return npl,fmt,width,decimal
    raise Exception('Unrecognized format type: '\
        +str(fd)+' looking for: '+str(fmts))
 
def build_fortran_desciptor(npl,fmt,width,decimal):
    fd = '('+str(npl)+fmt+str(width)
    if decimal != None:
        fd += '.'+str(decimal)+')'
    else:
        fd += ')'
    return fd   

def build_python_descriptor(npl,fmt,width,decimal):
    if fmt.upper() == 'I':
        fmt = 'd'
    pd = '{0:'+str(width)
    if decimal != None:
        pd += '.'+str(decimal)+fmt+'}'
    else:
        pd += fmt+'}'
    return pd



def array2string(a, fmt_tup):
        '''Converts a 1D or 2D array into a string
        Input:
            a: array
            fmt_tup = (npl,fmt_str)
            fmt_str: format string
            npl: number of numbers per line
        Output:
            s: string representation of the array'''

        aa = np.atleast_2d(a)
        nr, nc = np.shape(aa)[0:2]
        #print 'nr = %d, nc = %d\n' % (nr, nc)
        npl = fmt_tup[0]
        fmt_str = fmt_tup[1]
        s = ''
        for r in range(nr):
            for c in range(nc):
                #s = s + (fmt_str % aa[r, c])
                s = s + (fmt_str.format(aa[r, c]))
                if (((c + 1) % npl == 0) or (c == (nc - 1))):
                    s = s + '\n'
        return s

def u3d_like(model,other):
    u3d = copy.deepcopy(other)
    u3d.model = model
    for i,u2d in enumerate(u3d.util_2ds):
        u3d.util_2ds[i].model = model

    return u3d

def u2d_like(model,other):
    u2d = copy.deepcopy(other)
    u2d.model = model
    return u2d



class util_3d():
    def __init__(self,model,shape,dtype,value,name,\
        fmtin=None,cnstnt=1.0,iprn=-1,locat=None):
        '''3-D wrapper from util_2d - shape must be 3-D
        '''
        assert len(shape) == 3,'util_3d:shape attribute must be length 3'
        self.model = model
        self.shape = shape
        self.dtype = dtype
        self.__value = value
        self.name_base = name+' Layer '
        self.fmtin = fmtin
        self.cnstst = cnstnt
        self.iprn = iprn
        self.locat = locat
        if model.external_path != None:
            self.ext_filename_base = model.external_path+self.name_base.replace(' ','_')
        self.util_2ds = self.build_2d_instances()
   
    def __getitem__(self,k):
        if np.isscalar(k):
            return self.util_2ds[k]
        else:
            #--if a 3-d tuple was passed
            if len(k) == 3:
                #--if the util_2d instance for layer k[0] 
                #--is a scalar then return the value of the scalar
                if np.isscalar(self.util_2ds[k[0]].get_value()):
                    val = self.util_2ds[k[0]].get_value()
                    return val
                #--otherwise, get 3-d the array position value
                else:
                    val = self.util_2ds[k[0]].array[k[1:]]
                    return val
                    
    def get_file_entry(self):
        s = ''
        for u2d in self.util_2ds:
            s += u2d.get_file_entry()
        return s

    def get_value(self):
        value = []
        for u2d in self.util_2ds:
            value.append(u2d.get_value())
        return value

    @property
    def array(self):
        a = np.empty((self.shape))
        for i,u2d in self.uds:
            a[i] = u2d.array
        return a

    def build_2d_instances(self):
        u2ds = []
        #--if value is not enumerable, then make a list of something
        if not isinstance(self.__value,list) \
            and not isinstance(self.__value,np.ndarray):
            self.__value = [self.__value] * self.shape[0]


        #--if this is a list or 1-D array with constant values per layer
        if isinstance(self.__value,list) \
            or (isinstance(self.__value,np.ndarray) \
            and (self.__value.ndim == 1)):
            
            assert len(self.__value) == self.shape[0],\
                'length of 3d enumerable:'+str(len(self.__value))+\
                ' != to shape[0]:'+str(self.shape[0])
            
            for i,item in enumerate(self.__value):  
                name = self.name_base+str(i+1)
                ext_filename = None
                if self.model.external_path != None:
                    ext_filename = self.ext_filename_base+str(i+1)+'.ref'
                u2d = util_2d(self.model,self.shape[1:],self.dtype,item,\
                    fmtin=self.fmtin,name=name,ext_filename=ext_filename,\
                    locat=self.locat)
                u2ds.append(u2d)
                                      
        elif isinstance(self.__value,np.ndarray):
            #--if an array of shape nrow,ncol was passed, tile it out for each layer
            if self.__value.shape[0] != self.shape[0]:
                if self.__value.shape == (self.shape[1],self.shape[2]):
                    self.__value = [self.__value] * self.shape[0]
                else:
                    raise Exception('value shape[0] != to self.shape[0] and' +\
                        'value.shape[[1,2]] != self.shape[[1,2]]'+\
                        str(self.__value.shape)+' '+str(self.shape))
            for i,a in enumerate(self.__value):
                a = np.atleast_2d(a)                
                ext_filename = None
                name = self.name_base+str(i+1)
                if self.model.external_path != None:
                    ext_filename = self.ext_filename_base+str(i+1)+'.ref'
                u2d = util_2d(self.model,self.shape[1:],self.dtype,a,\
                    fmtin=self.fmtin,name=name,ext_filename=ext_filename,\
                    locat=self.locat)
                u2ds.append(u2d)
                
        else:
            raise Exception('util_array_3d: value attribute must be list '+\
               ' or ndarray, not'+str(type(self.__value)))
        return u2ds


class util_2d():   
    def __init__(self,model,shape,dtype,value,name=None,fmtin=None,\
        cnstnt=1.0,iprn=-1,ext_filename=None,locat=None,bin=False):
        '''1d or 2-d array support with minimum of mem footprint.  
        only creates arrays as needed, 
        otherwise functions with strings or constants
        shape = 1-d or 2-d tuple
        value =  an instance of string,list,np.int,np.float32,np.bool or np.ndarray
        vtype = str,np.int,np.float32,np.bool, or np.ndarray
        dtype = np.int, or np.float32
        if ext_filename is passed, scalars are written externally as arrays
        model instance bool attribute "free_format" used for generating control record
        model instance string attribute "external_path" 
        used to determine external array writing
        bin controls writing of binary external arrays
        '''

        self.model = model
        self.shape = shape
        self.dtype = dtype
        self.bin = bool(bin)
        self.name = name             
        self.locat = locat
        self.__value = self.parse_value(value)
        self.__value_built = None        
        self.cnstnt = float(cnstnt)
        self.iprn = iprn
        self.ext_filename = None
        
        #--set fmtin
        if fmtin != None:
            self.fmtin = fmtin
        else:
            if self.bin:
                self.fmtin = '(BINARY)'
            else:
                if len(shape) == 1:
                    npl = self.shape[0]
                else:
                    npl = self.shape[1]                        
                if self.dtype == np.int:
                    self.fmtin = '('+str(npl)+'I10) '
                    
                else:
                    self.fmtin = '('+str(npl)+'G15.6) '
                    
        #--get (npl,python_format_descriptor) from fmtin
        self.py_desc = self.fort_2_py(self.fmtin)  

        #--some defense
        if dtype not in [np.int,np.float32,np.bool]:
            raise Exception('util_2d:unsupported dtype: '+str(dtype))
        if self.model.external_path != None and name == None \
            and ext_filename == None:
            raise Exception('util_2d: use external arrays requires either '+\
               'name or ext_filename attribute')
        elif self.model.external_path != None and ext_filename == None:
            self.ext_filename = self.model.external_path+name+'.ref'
        else:
            self.ext_filename = ext_filename
             
        if self.bin and self.ext_filename is None:
            raise Exception('util_2d: binary flag requires ext_filename')


    def set_fmtin(self,fmtin):
        self.fmtin = fmtin
        self.py_desc = self.fort_2_py(self.fmtin)
        return

    def get_value(self):
        return self.__value
    
    #--overloads, tries to avoid creating arrays if possible
    def __add__(self,other):
        if self.vtype in [np.int,np.float32] and self.vtype == other.vtype:
            return self.__value + other.get_value()
        else:
            return self.array + other.array

    def __sub__(self,other):
        if self.vtype in [np.int,np.float32] and self.vtype == other.vtype:
            return self.__value - other.get_value()
        else:
            return self.array - other.array

    def __getitem__(self,k):
        return self.array[k]
    
    def __setitem__(self,k,value):
        '''this one is dangerous because it resets __value
        '''
        a = self.array
        a[k] = value
        a = a.astype(self.dtype)
        self.__value = a
        if self.__value_built is not None:
            self.__value_built = None
        
    def all(self):
        return self.array.all()
    
    def __len__(self):
        return self.shape[0]

    def sum(self):
        return self.array.sum()

    @property
    def vtype(self):
        return type(self.__value)
    
    def get_file_entry(self):
        '''this is the entry point for getting an 
        input file entry for this object
        '''
        #--call get_file_array first in case we need to
       #-- get a new external unit number and reset self.locat
        vstring = self.get_file_array()
        cr = self.get_control_record()
        return cr+vstring
    

    def get_file_array(self):
        '''increments locat and update model instance if needed.
        if the value is a constant, or a string, or external, 
        return an empty string
        '''       
        #--if the value is not a filename
        if self.vtype != str:
            
            #--if the ext_filename was passed, then we need 
            #-- to write an external array
            if self.ext_filename != None:
                #--if we need fixed format, reset self.locat and get a
               #--  new unit number                 
                if not self.model.free_format:
                    self.locat = self.model.next_ext_unit() 
                    if self.bin:
                        self.locat = -1 * np.abs(self.locat)
                        self.model.add_external(self.ext_filename,\
                            self.locat,binFlag=True)
                    else:
                        self.model.add_external(self.ext_filename,self.locat)
                #--write external formatted or unformatted array    
                if not self.model.use_existing:    
                    if not self.bin:
                        f = open(self.ext_filename,'w',0)
                        f.write(self.string)
                        f.close()
                    else:
                        a = self.array.tofile(self.ext_filename)                    
                return ''
                
            #--this internal array or constant
            else:
                if self.vtype is np.ndarray:
                    return self.string
                #--if this is a constant, return a null string
                else:
                    return ''
        else:         
            if os.path.exists(self.__value) and self.ext_filename != None:
                #--if this is a free format model, then we can use the same
                #-- ext file over and over - no need to copy
                #--also, loosen things up with FREE format
                if self.model.free_format:
                    self.ext_filename = self.__value
                    self.fmtin = '(FREE)'
                    self.py_desc =self.fort_2_py(self.fmtin)

                else:
                    if self.__value != self.ext_filename:
                        shutil.copy2(self.__value,self.ext_filename)
                    #--if fixed format, we need to get a new unit number 
                    #-- and reset locat
                    self.locat = self.model.next_ext_unit()
                    self.model.add_external(self.ext_filename,self.locat)
                    
                return '' 
            #--otherwise, we need to load the the value filename 
            #-- and return as a string
            else:
                return self.string

    @property
    def string(self):
        '''get the string reprenation of value attribute
        '''
        a = self.array
        #--convert array to sting with specified format
        a_string = array2string(a,self.py_desc)
        return a_string
                                    
    @property
    def array(self):
        '''get the array representation of value attribute
           if value is a string or a constant, the array is loaded/built only once
        '''
        if self.vtype == str:
            if self.__value_built is None:
                self.__value_built = self.load_txt().astype(self.dtype)
            return self.__value_built
        elif self.vtype != np.ndarray:
            if self.__value_built is None:
                self.__value_built = np.ones(self.shape,dtype=self.dtype) \
                    * self.__value
            return self.__value_built
        else:
            return self.__value
    
    def load_txt(self):
        '''load a (possibly wrapped format) array from a file 
        (self.__value) and casts to the proper type (self.dtype)
        '''
        file_in = open(self.__value,'r')
        nrow,ncol = self.shape
        data = np.zeros((nrow*ncol),dtype=self.dtype)-1.0E+10
        d = 0
        while True:
            line = file_in.readline()
            if line is None or d == nrow*ncol:
                break
            raw = line.strip('\n').split()
            for a in raw:
                try:
                    data[d] = self.dtype(a)
                except:
                    raise Exception ('util_2d:unable to cast value: '\
                        +str(a)+' to type:'+self.dtype)
                if d == (nrow*ncol)-1:
                    assert len(data) == (nrow*ncol)
                    data.resize(nrow,ncol)
                    return(data) 
                d += 1	
        file_in.close()
        data.resize(nrow,ncol)
        return data
   
    def get_control_record(self):  
        '''get the modflow control record
        '''      
        lay_space = '{0:>27s}'.format( '' )
        if self.model.free_format:
            if self.ext_filename is None:
                if self.vtype in [np.int]:
                    lay_space = '{0:>32s}'.format( '' )
                if self.vtype in [np.int,np.float32]:
                    cr = 'CONSTANT '+self.py_desc[1].format(self.__value)
                    cr = '{0:s}{1:s}#{2:<30s}\n'.format( cr,lay_space,self.name )
                else:
                    cr = 'INTERNAL {0:15.6G} {1:>10s} {2:2.0f} #{3:<30s}\n'\
                        .format(self.cnstnt,self.fmtin,self.iprn,self.name)
            else:
                #--need to check if ext_filename exists, if not, need to 
                #-- write constant as array to file or array to file               
                cr = 'OPEN/CLOSE  {0:>30s} {1:15.6G} {2:>10s} {3:2.0f}  #{4:<30s}\n'\
                    .format(self.ext_filename,self.cnstnt,\
                    self.fmtin.strip(),self.iprn,self.name)
        else:                       
            #--if value is a scalar and we don't want external array
            if self.vtype in [np.int,np.float32] and self.ext_filename is None:
                locat = 0
                cr = '{0:>10.0f}{1:>10.5G}{2:>20s}{3:10.0f} #{4}\n'\
                    .format(locat,self.__value,self.fmtin,self.iprn,self.name)
            else:
                if self.ext_filename is None:
                    assert self.locat != None,'util_2d:a non-constant value '+\
                       ' for an internal fixed-format requires LOCAT to be passed'                
                if self.dtype == np.int:
                    cr = '{0:>10.0f}{1:>10.0f}{2:>20s}{3:>10.0f} #{4}\n'\
                        .format(self.locat,self.cnstnt,self.fmtin,self.iprn,self.name)
                elif self.dtype == np.float32:
                    cr = '{0:>10.0f}{1:>10.5G}{2:>20s}{3:>10.0f} #{4}\n'\
                        .format(self.locat,self.cnstnt,self.fmtin,self.iprn,self.name)
                else:
                    raise Exception('util_2d: error generating fixed-format '+\
                       ' control record,dtype must be np.int or np.float32')
        return cr                                 

    def fort_2_py(self,fd):
        '''converts the fortran format descriptor 
        into a tuple of npl and a python format specifier

        '''
        npl,fmt,width,decimal = decode_fortran_descriptor(fd)
        if npl == 'free':
            if self.vtype == np.int:
                return (self.shape[1],'{0:10.0f} ')
            else:
                return (self.shape[1],'{0:15.6G} ')
        elif npl == 'binary':
            return('binary',None)
        else:
            pd = build_python_descriptor(npl,fmt,width,decimal)
            return (npl,pd)    


    def parse_value(self,value):
        '''parses and casts the raw value into an acceptable format for __value
        lot of defense here, so we can make assumptions later
        '''
        if isinstance(value,list):
            print 'util_2d: casting list to array'
            value = np.array(value)
        if isinstance(value,bool):
            if self.dtype == np.bool:
                try:
                    value = np.bool(value)
                    return value
                except:
                    raise Exception('util_2d:could not cast '+\
                        'boolean value to type "np.bool": '+str(value))
            else:
                raise Exeception('util_2d:value type is bool, '+\
                   ' but dtype not set as np.bool') 
        if isinstance(value,str):
            if self.dtype == np.int:
                try:
                    value = int(value)
                except:
                    assert os.path.exists(value),'could not find file: '+str(value)
                    return value
            else:
                try:
                    value = float(value)
                except:
                    return value
        if np.isscalar(value):
            if self.dtype == np.int:
                try:
                    value = np.int(value)
                    return value
                except:
                    raise Exception('util_2d:could not cast scalar '+\
                        'value to type "int": '+str(value))
            elif self.dtype == np.float32:
                try:
                    value = np.float32(value)
                    return value
                except:
                    raise Exception('util_2d:could not cast '+\
                        'scalar value to type "float": '+str(value))
            
        if isinstance(value,np.ndarray):
            if self.shape != value.shape:
                raise Exception('util_2d:self.shape: '+str(self.shape)+\
                    ' does not match value.shape: '+str(value.shape))
            if self.dtype != value.dtype:
                print 'util_2d:warning - casting array of type: '+\
                    str(value.dtype)+' to type: '+str(self.dtype)
            return value.astype(self.dtype)
        
        else:
            raise Exception('util_2d:unsupported type in util_array: '\
                +str(type(value))) 