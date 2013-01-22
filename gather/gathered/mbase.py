import numpy as np
import sys
import os
import subprocess as sp
import webbrowser as wb

# Global variables
iconst = 1 # Multiplier for individual array elements in integer and real arrays read by MODFLOW's U2DREL, U1DREL and U2DINT.
iprn = -1 # Printout flag. If >= 0 then array values read are printed in listing file.

class BaseModel(object):
    'MODFLOW based models base class'
    def __init__(self, modelname = 'modflowtest', namefile_ext = 'nam', exe_name = 'mf2k.exe', model_ws = None):
        self.__name = modelname
        self.namefile_ext = namefile_ext
        self.namefile = self.__name + '.' + self.namefile_ext
        self.packagelist = []
        self.heading = ''
        self.exe_name = exe_name
        self.external_extension = 'ref'
        if model_ws is None: model_ws = os.getcwd()
        if not os.path.exists(model_ws):
            try:
                os.makedirs(model_ws)
            except:
                print '\n%s not valid, workspace-folder was changed to %s\n' % (model_ws, os.getcwd())
                model_ws = os.getcwd()
        self.model_ws= model_ws
        self.cl_params = ''
    
    def set_exename(self, exe_name):
        self.exe_name = exe_name
        return
        
    def add_package(self, p):                                    
        for pp in (self.packagelist):
            if isinstance(p, type(pp)):
                print '****Warning -- two packages of the same type: ',type(p),type(pp)                 
                #print 'replacing existing Package...'                
                #pp = p
                      
        self.packagelist.append( p )       
    
    def remove_package(self,pname):
        for i,pp in enumerate(self.packagelist):  
            if pname in pp.name:               
                print 'removing Package: ',pp.name
                self.packagelist.pop(i)
                return
        raise StopIteration , 'Package name '+pname+' not found in Package list'                
            
    def build_array_name(self,num,prefix):
       return self.external_path+prefix+'_'+str(num)+'.'+self.external_extension
       
    def assign_external(self,num,prefix):           
        fname = self.build_array_name(num,prefix)
        unit = (self.next_ext_unit())
        self.external_fnames.append(fname)
        self.external_units.append(unit)       
        self.external_binflag.append(False)        
        return fname,unit
    
    def add_external(self,fname,unit,binflag=False):
        '''
        supports SWR usage and non-loaded existing external arrays
        '''
        self.external_fnames.append(fname)
        self.external_units.append(unit)        
        self.external_binflag.append(binflag)
    
    def remove_external(self,fname=None,unit=None):                    
        if fname is not None:
            for i,e in enumerate(self.external_fnames):
                if fname in e:
                    self.external_fnames.pop(i)
                    self.external_units.pop(i)
                    self.external_binflag.pop(i)
        elif unit is not None:
            for i,u in enumerate(self.external_units):
                if u == unit:
                    self.external_fnames.pop(i)
                    self.external_units.pop(i)
                    self.external_binflag.pop(i)                    
                    
        else:
            raise Exception,' either fname or unit must be passed to remove_external()'
        return            
    
    
    
    
    def array2string(self, a, fmt_str, npl):
        '''Converts a 1D or 2D array into a string
        Input:
            a: array
            fmt_str: format string
            npl: number of numbers per line
        Output:
            s: string representation of the array'''

        aa = np.atleast_2d(a)
        nr, nc = np.shape(aa)[0:2]
        #print 'nr = %d, nc = %d\n' % (nr, nc)

        s = ''
        for r in range(nr):
            for c in range(nc):
                s = s + (fmt_str % aa[r, c])
                if (((c + 1) % npl == 0) or (c == (nc - 1))):
                    s = s + '\n'
        return s

    def get_name_file_entries(self):
        s = ''        
        for p in self.packagelist:
            for i in range(len(p.name)):
            	s = s + ('%s %3i %s %s\n' % (p.name[i], p.unit_number[i], p.file_name[i],p.extra[i]))            
        return s
                
    def get_package(self, name):
        for pp in (self.packagelist):
            if (pp.name[0] == name):
                return pp
        return None
   
    def run_model(self, pause = True, report = None):
        batch_file_name = os.path.join(self.model_ws, 'run.bat')
        error_message = ('Model executable %s not found!' % self.exe_name)
        assert os.path.exists(self.exe_name), error_message

        error_message = ('Name file %s not found!' % self.namefile)
        fn_path = os.path.join(self.model_ws, self.namefile)
        assert os.path.exists(fn_path), error_message

        # Create a batch file to call code so that window remains open in case of error messages
        f = open(batch_file_name, 'w')
        f.write('@ECHO Calling %s with %s\n' % (self.exe_name, self.namefile))
        f.write('%s %s %s\n' % (self.exe_name, self.namefile, self.cl_params))
        if (pause):
           f.write('@PAUSE\n')
        f.close()
        os.path.abspath = self.model_ws
        sp.call(batch_file_name, cwd=self.model_ws, stdout = report)
        os.remove(batch_file_name)
    
    def run_model2(self, pause = True, report = False):
        success = False
        buff = []
        proc = sp.Popen([self.exe_name,self.namefile],stdout=sp.PIPE)
        while True:
          line = proc.stdout.readline()
          if line != '':
            if 'normal termination of simulation' in line.lower():
                success = True
            c = line.split('\r')
            print c[0]
            if report == True:
                buff.append( c[0] )
          else:
            break
        if pause == True:
            raw_input('Press Enter to continue...')
        return ( [success,buff] )
        
    def run_model3(self):
        import subprocess
        a = subprocess.Popen([self.exe_name,self.namefile],stdout=subprocess.PIPE)
        b = a.communicate()
        c = b[0].split('\r')
        for cc in c:
            print cc
        

    def write_array(self, f, a, locat, write_fmtin, npi, npl, \
          description='', constant_str = '0 ',ext_base = None):
        '''Writes an array of reals/ints to a file.
        Input:
            f: handle to file
            a: array to be written, or optionally, a name(str) or list of names of an 
               existing external array
            locat: FORTRAN unit number
            write_fmtin: flag to indicate if format string must be written
            npi: number of characters per item
            npl: number of numbers per line
            description: string that is appended to the layer header
            ext_base: the external array filename base (ibound,hk,prsiy,etc)                      
                      
            Notes:
            npl < 0 indicates that this number of items per line must be enforced
            and no 'Constant' line will be written. This is needed for MT3DMS, which
            doesn't allow the 'Constant' option
            
            if ext_base is not passed, arrays are not written externally, regardless 
            whether the parent model has the external flag set.  
            
            constants are written externally as arrays if ext_base is passed                    
            
            if the array was not loaded, then the fmtin is set to (FREE)
            
            if the parent model is MODFLOW, then the open/close option is used
            '''
                        
        if isinstance(a,np.ndarray) or np.isscalar(a):            
                            
            if np.isscalar(a): a = np.array([a])
            nlay = a.shape[0]
                
            if (a.dtype == np.int):
                fmtin = '(%dI%d) ' % (abs(npl), npi) # FORTRAN format descriptor
                fmt_str = '%' + ('%d' % npi) + 'd'
            else:
                fmtin = '(%dG%d.0) ' % (abs(npl), npi) # FORTRAN format descriptor
                fmt_str = '%' + ('%d' % npi) + 'g' #' %13f'
    
            if (locat < 0):
                fmtin = '(BINARY)'
    
            for l in range(nlay):
                if (npl>0) and (a.ndim==1):  # One value for each layer
                    if (nlay > 1):
                        if a.dtype == np.int:
                            f.write('%10s%10d%20s%10d %s %d\n' % (constant_str, a[l], fmtin, iprn, description, l + 1))
                        else:
                            f.write('%10s%10.3e%20s%10d %s %d\n' % (constant_str, a[l], fmtin, iprn, description, l + 1))
                    else:
                        if a.dtype == np.int:
                            f.write('%10s%10d%20s%10d %s\n' % (constant_str, a[l], fmtin, iprn, description))
                        else:
                            f.write('%10s%10.3e%20s%10d %s\n' % (constant_str, a[l], fmtin, iprn, description))
                else:
                    if (write_fmtin):
                        if (nlay > 1):
                            f.write('%10d%10d%20s%10d %s %d\n' % (locat, iconst, fmtin, iprn, description, l + 1))
                        else:
                            f.write('%10d%10d%20s%10d %s\n' % (locat, iconst, fmtin, iprn, description))
    
                    f.write(self.array2string(a[l], fmt_str, abs(npl)))
                        
        else:  # Jeremy needs to clean this up
            #--hack...
            isMODFLOW = False
            if 'mf.modflow' in str(type(self)): isMODFLOW = True
            
            #--if 'a' is a string, then the array is a non-loaded existing external array         
            if isinstance(a,str):          
                fmtin = '(FREE)'            
                if isMODFLOW:                    
                    f.write('OPEN/CLOSE '+a.ljust(30)+' {0:2d} (FREE) {1:2d} '\
                           .format(iconst,iprn)+description+'\n')                
                else: 
                    locat = self.next_ext_unit()               
                    f.write('%10d%10d%20s%10d %s\n' % (locat, iconst, fmtin, iprn, description))  
                    self.add_external(a,locat)            
                return
                    
            #--if a is a list of strings
            elif isinstance(a,list):
                fmtin = '(FREE) '
                for i,aa in enumerate(a):                             
                    if isMODFLOW:
                        #locat = self.next_ext_unit()
                        #f.write('EXTERNAL {0:5d} {1:2d} (FREE) {2:2d} '\
                        #        .format(locat,iconst,iprn)+description+' '+str(i+1)+'\n')
                        f.write('OPEN/CLOSE '+aa.ljust(30)+' {0:2d} (FREE) {1:2d} '\
                           .format(iconst,iprn)+description+' '+str(i+1)+'\n')  
                    else:                
                        locat = self.next_ext_unit()   
                        f.write('%10d%10d%20s%10d %s\n' % (locat, iconst, fmtin, iprn, description))    
                        self.add_external(aa,locat)              
                return
            
                #--if an external base name was passed and the parent model object external flag is set
                if ext_base is not None and self.external:
                    for l in range(nl):
                        if isMODFLOW:
                            fname = self.build_array_name(l+1,ext_base)
                            f.write('OPEN/CLOSE '+fname.ljust(30)+' {0:2d} {1:20s} {2:2d} '\
                                    .format(iconst,fmtin,iprn)+description+'\n')                
                            write_this_fmtin = False                                     
                        else:                                                       
                            fname,locat = self.assign_external(l+1,ext_base)                                                                  
                        f_ext = open(fname,'w')
                        f_ext.write(self.array2string(aa[:, :, l], fmt_str, abs(npl)))                    
                        write_flag = False
                        f_ext.close()


    def write_array_old(self, f, a, locat, write_fmtin, npi, npl,\
          description='', constant_str = '0 ',ext_base = None):
        '''Writes an array of reals/ints to a file.
        Input:
            f: handle to file
            a: array to be written, or optionally, a name(str) or list of names of an 
               existing external array
            locat: FORTRAN unit number
            write_fmtin: flag to indicate if format string must be written
            npi: number of characters per item
            npl: number of numbers per line
            description: string that is appended to the layer header
            ext_base: the external array filename base (ibound,hk,prsiy,etc)                      
                      
            Notes:
            npl < 0 indicates that this number of items per line must be enforced
            and no 'Constant' line will be written
            
            if ext_base is not passed, arrays are not written externally, regardless 
            whether the parent model has the external flag set.  
            
            constants are written externally as arrays if ext_base is passed                    
            
            if the array was not loaded, then the fmtin is set to (FREE)
            
            if the parent model is MODFLOW, then the open/close option is used
            '''      
        #--hack...
        isMODFLOW = False
        if 'mf.modflow' in str(type(self)): isMODFLOW = True
        
        #--if 'a' is a string, then the array is a non-loaded existing external array 
        #--   and must use 'FREE' format         
        if isinstance(a,str):          
            fmtin = '(FREE)'            
            if isMODFLOW:
                #locat = self.next_ext_unit()
                #f.write('EXTERNAL {0:5d} {1:2d} (FREE) {2:2d} '\
                #       .format(locat,iconst,iprn)+description+'\n')
                f.write('OPEN/CLOSE '+a.ljust(30)+' {0:2d} (FREE) {1:2d} '\
                       .format(iconst,iprn)+description+'\n')                
            else: 
                locat = self.next_ext_unit()               
                f.write('%10d%10d%20s%10d %s\n' % (locat, iconst, fmtin, iprn, description))  
                self.add_external(a,locat)            
            return
                
        #--if a is a list of strings
        elif isinstance(a,list):
            fmtin = '(FREE) '
            for i,aa in enumerate(a):                             
                if isMODFLOW:
                    #locat = self.next_ext_unit()
                    #f.write('EXTERNAL {0:5d} {1:2d} (FREE) {2:2d} '\
                    #        .format(locat,iconst,iprn)+description+' '+str(i+1)+'\n')
                    f.write('OPEN/CLOSE '+aa.ljust(30)+' {0:2d} (FREE) {1:2d} '\
                       .format(iconst,iprn)+description+' '+str(i+1)+'\n')  
                else:                
                    locat = self.next_ext_unit()   
                    f.write('%10d%10d%20s%10d %s\n' % (locat, iconst, fmtin, iprn, description))    
                    self.add_external(aa,locat)              
            return     
            
        #--a is an numpy array object
        else:
               
            aa = np.atleast_3d(a)
            nr, nc, nl = np.shape(aa)[0:3]
            
            if (a.dtype == 'int32'):
                fmtin = '(%dI%d) ' % (abs(npl), npi) # FORTRAN format descriptor
                fmt_str = '%' + ('%d' % npi) + 'd'
            else:
                fmtin = '(%dG%d.0) ' % (abs(npl), npi) # FORTRAN format descriptor
                fmt_str = '%' + ('%d' % npi) + 'g' #' %13f'
    
            if (locat < 0):
                fmtin = '(BINARY)'
               
            for l in range(nl):            
                #--might need to reset fmtin if MODFLOW open/close format is used
                write_this_fmtin = write_fmtin
                
                #--if 'a' is a constant value and the ext_base was not passed                
                if ((npl > 0) and (aa[:, :, l].min() == aa[:, :, l].max()) \
                   and ext_base is None and write_fmtin is True):                
                    if (nl > 1):
                        if a.dtype == 'int32':
                            f.write('%10s%10d%20s%10d %s %d\n' % (constant_str, aa[0, 0, l], fmtin, iprn, description, l + 1))
                        else:
                            f.write('%10s%10.3e%20s%10d %s %d\n' % (constant_str, aa[0, 0, l], fmtin, iprn, description, l + 1))
                    else:
                        if a.dtype == 'int32':
                            f.write('%10s%10d%20s%10d %s\n' % (constant_str, aa[0, 0, l], fmtin, iprn, description))
                        else:
                            f.write('%10s%10.3e%20s%10d %s\n' % (constant_str, aa[0, 0, l], fmtin, iprn, description))
                else:                    
                    write_flag = True
                    
                    #--if an external base name was passed and the parent model object external flag is set
                    if ext_base is not None and self.external:                                            
                        if isMODFLOW:
                            fname = self.build_array_name(l+1,ext_base)
                            f.write('OPEN/CLOSE '+fname.ljust(30)+' {0:2d} {1:20s} {2:2d} '\
                                    .format(iconst,fmtin,iprn)+description+'\n')                
                            write_this_fmtin = False                                     
                        else:                                                       
                            fname,locat = self.assign_external(l+1,ext_base)                                                                  
                        f_ext = open(fname,'w')
                        f_ext.write(self.array2string(aa[:, :, l], fmt_str, abs(npl)))                    
                        write_flag = False
                        f_ext.close()                                              
                    if (write_this_fmtin):
                        if (nl > 1):
                            f.write('%10d%10d%20s%10d %s %d\n' % (locat, iconst, fmtin, iprn, description, l + 1))
                        else:
                            f.write('%10d%10d%20s%10d %s\n' % (locat, iconst, fmtin, iprn, description))                                        
                    if write_flag:                        
                        f.write(self.array2string(aa[:, :, l], fmt_str, abs(npl)))
                        
    def write_vector(self, f, a, locat, write_fmtin, npi, npl, \
          description='', constant_str = '0 '):
        '''Seperate function to write a vector (for example for delrow and delcol, and trpy in the bcf package)
        Input:
            f: handle to file
            a: array to be written
            locat: FORTRAN unit number
            write_fmtin: flag to indicate if format string must be written
            npi: number of characters per item
            npl: number of numbers per line
            description: string that is appended to the layer header
            ext_base: the external array filename base (ibound,hk,prsiy,etc)                      
                      
            Notes:
            npl < 0 indicates that this number of items per line must be enforced
            and no 'Constant' line will be written
            
            if ext_base is not passed, arrays are not written externally, regardless 
            whether the parent model has the external flag set.  
            
            constants are written externally as arrays if ext_base is passed                    
            
            if the array was not loaded, then the fmtin is set to (FREE)
            
            if the parent model is MODFLOW, then the open/close option is used
            '''
                
        assert a.ndim == 1, 'Error: dimension of vector needs to be 1 in write_vector'
                
        if (a.dtype == 'int32'):
            fmtin = '(%dI%d) ' % (abs(npl), npi) # FORTRAN format descriptor
            fmt_str = '%' + ('%d' % npi) + 'd'
        else:
            fmtin = '(%dG%d.0) ' % (abs(npl), npi) # FORTRAN format descriptor
            fmt_str = '%' + ('%d' % npi) + 'g' #' %13f'

        if (locat < 0):
            fmtin = '(BINARY)'

        if (len(a) == 1) or (a.min()==a.max()) and write_fmtin:
            if a.dtype == 'int32':
                f.write('%10s%10d%20s%10d %s\n' % (constant_str, a[0], fmtin, iprn, description))
            else:
                f.write('%10s%10.3e%20s%10d %s\n' % (constant_str, a[0], fmtin, iprn, description))
        else:
            if (write_fmtin):
                f.write('%10d%10d%20s%10d %s\n' % (locat, iconst, fmtin, iprn, description))
            f.write(self.array2string(a, fmt_str, abs(npl)))                    
                    
    def write_input(self,SelPackList=False):       
        if self.verbose:
            print self # Same as calling self.__repr__()
            print 'Writing packages:'
        if SelPackList == False:
            for p in self.packagelist:            
                p.write_file()
                if self.verbose:
                    print p.__repr__()        
        else:
#            for i,p in enumerate(self.packagelist):  
#                for pon in SelPackList:
            for pon in SelPackList:
                for i,p in enumerate(self.packagelist):  
                    if pon in p.name:               
                        print 'writing Package: ',p.name
                        p.write_file()
                        if self.verbose:
                            print p.__repr__()        
                        break
        #--write name file
        self.write_name_file()
    
    def write_name_file(self):
        '''Every Package needs its own writenamefile function'''
        raise Exception, 'IMPLEMENTATION ERROR: writenamefile must be overloaded'
    def get_name(self):
        return self.__name
    def set_name(self, value):
        self.__name = value
        self.namefile = self.__name + '.' + self.namefile_ext
        for p in self.packagelist:
            for i in range(len(p.extension)):
                p.file_name[i] = self.__name + '.' + p.extension[i]
    name = property(get_name, set_name)

class Package(object):
    'General Package class'
    def __init__(self, parent, extension='glo', name='GLOBAL', unit_number=1, extra=''):
        self.parent = parent # To be able to access the parent modflow object's attributes
        if (not isinstance(extension, list)):
            extension = [extension]
        self.extension = []
        self.file_name = []
        for e in extension:
            self.extension = self.extension + [e]
            self.file_name = self.file_name + [self.parent.name + '.' + e]
            self.fn_path = os.path.join(self.parent.model_ws,self.file_name[0])
        if (not isinstance(name, list)):
            name = [name]
        self.name = name
        if (not isinstance(unit_number, list)):
            unit_number = [unit_number]
        self.unit_number = unit_number
        if (not isinstance(extra, list)):
            self.extra = len(self.unit_number) * [extra]
        else:
            self.extra = extra
        self.url = 'index.html'
    def __repr__( self ):
        s = self.__doc__
        exclude_attributes = ['extension', 'heading', 'name', 'parent', 'url']
        for attr, value in sorted(self.__dict__.iteritems()):
            if not (attr in exclude_attributes):
                if (isinstance(value, list)):
                    if (len(value) == 1):
                        s = s + ' %s = %s (list)\n' % (attr, str(value[0]))
                    else:
                        s = s + ' %s (list, items = %d)\n' % (attr, len(value))
                elif (isinstance(value, np.ndarray)):
                    s = s + ' %s (array, shape = %s)\n' % (attr, value.shape.__str__()[1:-1] )
                else:
                    s = s + ' %s = %s (%s)\n' % (attr, str(value), str(type(value))[7:-2])
        return s
    def assignarray(self, shape, type, srcarray, name='', load=False):
        '''
        Input:
        shape: shape of array. needs to be a tuple, so if a 1d array something like (nrow,), 2d array (nrow,ncol), etc.
        type: np.int or np.float
        srcarray: input values, which can be:
            a scalar all layers get the same number
        load = flag whether to load data from a filename. This may be needed for
               ibound, icbund and others as they are used by other packages
        Returns:
        destarray: Array with shape (nlayers), (nrow,ncols), or (nlayers,nrows,ncols) 
        '''
        
        if (isinstance(srcarray,list)): 
            # try to convert to array. if that is not possible, it may be a list of filenames, which is dealt with later
            try:
                srcarray = np.array(srcarray, dtype=type)
            except:
                pass
                    
        if np.isscalar(srcarray):
            # If scalar, assign same value to all layers, or to entire 1D array
            destarray = srcarray * np.ones(shape[0],dtype=type)
        elif isinstance(srcarray,np.ndarray):
            if srcarray.dtype != type: print("Warning, srcarray "+name+" needs to be of type "+str(type)+" FloPy will convert it")
            # If dimension is 1, assign one value for each layer only
            if srcarray.ndim == 1:
                if np.shape(srcarray)[0] == 1:
                    destarray = srcarray * np.ones(shape[0],dtype=type)
                else:
                    assert np.shape(srcarray)[0] == shape[0], "Error: Shape of srcarray "+name+" needs to be "+str(shape[0])
                    destarray = srcarray
            # If dimension is 2, store grid for one layer
            elif srcarray.ndim == 2:            
                assert np.shape(srcarray) == shape[1:], "Error: Shape of srcarray "+name+" needs to be "+str(shape[1:])
                destarray = np.empty(shape,dtype=type)  # Returning 3D array as writearray needs either a 1d or 3d array
                for i in range(shape[0]): destarray[i] = srcarray
            # If dimension is 3, store entire grid
            elif srcarray.ndim == 3:
                assert np.shape(srcarray) == shape, "Error: Shape of srcarray "+name+" needs to be "+str(shape)
                destarray = srcarray
            # Otherwise, return an error
            else:
                assert False, "Error: Shape of srcarray "+name+" needs to be "+str(shape)
        elif (isinstance(srcarray, list)):
            # Must be list of filenames
            assert len(srcarray) == shape[0], "Error: Length of srcarray "+name+" with filenames needs to be "+str(shape[0])                
            for s in srcarray:
                assert os.path.exists(s), "Error: file "+s+" does not exists"
            if load:
                destarray = np.empty(shape,type)
                for i,s in enumerate(srcarray):                    
                    destarray[i] = np.loadtxt(s,dtype=type)
            else:
                destarray = srcarray
        return destarray
    def assignarray_old(self, destarray, srcarray,load=False):
        '''
        load = flag to load the existing array or simply check that it exists and return.
               Must return srcarray since destarray type becomes immutable when passed.
               Calling derived class must re-assign the return string to destarray.  This
               flag is needed since ibound, icbund and others must be loaded for use in other packages
        '''
        
        #--if source array is a string instance, then assume the array is external and already exists 
        
        if (isinstance(srcarray,str)):
            assert os.path.exists(srcarray),'external existing array could not be found:'+srcarray
            if load:
                destarray = np.loadtxt(srcarray,dtype=destarray.dtype)
                return destarray             
            else:
                return srcarray
                   
        elif (isinstance(srcarray, list)): 
            #-try to cast to array, otherwise must be a list of strings
            #--  of existing arrays for each layer 
            try:
                srcarray = np.array(srcarray, dtype = destarray.dtype)
            except:                
                assert len(srcarray) == destarray.shape[2],\
                   'if a list of existing propertyarrays is passed to '+\
                   'assignarray_old, then there must be as many list '+\
                   'elements as layers'                
                for s in srcarray:
                    assert os.path.exists(s),'external existing'+\
                        'array could not be found:'+s
                if load:
                    tempsrc = np.zeros_like(destarray) - 1.0e+30
                    for i,s in enumerate(srcarray):                    
                        temp = np.loadtxt(s,dtype=destarray.dtype)                    
                        tempsrc[:,:,i] = temp                        
                    srcarray = tempsrc
                    return srcarray                
                else:                                        
                    return srcarray
                
        if (np.isscalar(srcarray)):
            destarray[:] = srcarray
        else:
            assert destarray.dtype == srcarray.dtype, 'Error: Array types do not match'
            if srcarray.shape == destarray.shape:
                destarray[:] = srcarray
            elif ((srcarray.ndim == 1) and (destarray.ndim == 3) and (srcarray.size == destarray.shape[2])):
                # If srcarray is 1D and has a length equal to the number of layers
                # then assign the elements in srcarray as constant values to all
                # cells in the corresponding layers in destarray
                for l in range(srcarray.size):
                    destarray[ :, :, l ] = srcarray[l]
            elif ((srcarray.ndim == 2) and (destarray.ndim == 3) and (srcarray.shape == destarray[ :, :, 0].shape)):
                # If srcarray is 2D and the number of rows and columns matches
                # the number of rows and columns of destarray then assign the
                # values in srcarray to all the layers in destarray
                for l in range(destarray.shape[-1]):
                    destarray[ :, :, l ] = srcarray.copy()
            else:
                raise IndexError,'Cannot assign values to grid. Dimensions do not match.'
        return destarray
            
    def assign_layer_row_column_data(self, layer_row_column_data, ncols):
        if (layer_row_column_data != None):
            new_layer_row_column_data = []
            mxact = 0
            for a in layer_row_column_data:
                a = np.atleast_2d(a)                
                nr, nc = a.shape                
                assert nc == ncols, 'layer_row_column_Q must have {0:1d} columns'.format(ncols)+'\nentry: '+str(a.shape)                
                mxact = max(mxact, nr)
                new_layer_row_column_data.append(a)
            return mxact, new_layer_row_column_data
        return
    def webdoc(self):
        if self.parent.version == 'mf2k':
            wb.open('http://water.usgs.gov/nrp/gwsoftware/modflow2000/Guide/' + self.url)
        elif self.parent.version == 'mf2005':
            wb.open('http://water.usgs.gov/nrp/gwsoftware/modflow2005/Guide/' + self.url)
        elif self.parent.version == 'ModflowNwt':
            wb.open('http://water.usgs.gov/nrp/gwsoftware/modflow_nwt/Guide/' + self.url)
    def write_file(self):
        '''Every Package needs its own write_file function'''
        print 'IMPLEMENTATION ERROR: write_file must be overloaded'
    def write_layer_row_column_data(self, f, layer_row_column_data):
        for n in range(self.parent.get_package('DIS').nper):
            if (n < len(layer_row_column_data)):
                a = layer_row_column_data[n]
                itmp = a.shape[0]
                f.write('%10i%10i\n' % (itmp, self.np))
                for b in a:
                    f.write('%9i %9i %9i' % (b[0], b[1], b[2]) )
                    for c in b[3:]:
                        f.write(' %13.6e' % c)
                    f.write('\n')
            else:
                itmp = -1
                f.write('%10i%10i\n' % (itmp, self.np))
