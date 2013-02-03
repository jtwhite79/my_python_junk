
import numpy as np
import pandas


class jco():
    def __init__(self,jco_filename,nespar=None,nobs=None):
        self.jco_filename = jco_filename
        self.nespar = nespar
        self.nobs = nobs
        self.parameters = None
        self.observations = None
        self.x = None

        self.integer = np.int32
        self.double = np.float64
        self.char = np.uint8


    def __getitem__(self,k):
        k = k.lower()
        if k in self.parameters:
            return self.x[:,self.parameters.index(k)]
        elif k in self.observations:
            return self.x[self.observations.index(k),:]
        else:
            raise Exception(str(k)+' not in parameters or observations')
    
    def to_binary(self,out_filename=None):
        if out_filename is None:
            out_filename = self.jco_filename
        f = open(out_filename,'wb')
        f.close()


    def from_binary(self):
        
        f = open(self.jco_filename,'rb')
        #--the header datatype
        header_dt = np.dtype([('itemp1',self.integer),('itemp2',self.integer),('icount',self.integer)])
        itemp1,itemp2,icount = np.fromfile(f,header_dt,1)[0]
    
        if itemp1 >= 0:
            raise TypeError, 'Jco produced by deprecated version of PEST,'+\
                             'Use JCOTRANS to convert to new format'
    
        if self.nespar is not None:
            if abs(itemp1) != nespar:
                raise ValueError,'nespar value not equal to jco dimensions'\
                                 +str(nespar)+' '+str(abs(itemp1))
        if self.nobs is not None:
            if abs(itemp2) != nobs:
                raise ValueError,'nobs value not equal to jco dimensions'\
                                 +str(nobs)+' '+str(abs(itemp2))
   
        nespar,nobs = abs(itemp1),abs(itemp2)                                  
        self.x = np.zeros((nobs,nespar))    
    
        #--the record datatype
        rec_dt = np.dtype([('j',self.integer),('dtemp',self.double)])
    
        #--read all data records
        #data = np.fromfile(f,rec_dt,icount) 
    
        #--uncompress the data into x    
        #for i in data:
        for ii in range(icount):
            i = np.fromfile(f,rec_dt,1)[0]
            j = i[0]
            dtemp = i[1]
            ies = ((j-1) / nobs) + 1
            irow = j - ((ies - 1) * nobs)
            #print i,ies,irow
        
            #--zero-based indexing translation
            self.x[irow-1,ies-1] = dtemp
        
        #--read parameter names
        par_names = []
        for i in range(nespar):
            pn = np.fromfile(f,self.char, count=12).tostring().lower()
            par_names.append(pn)
            #print 'par:',pn
    
        #--read obs names
        obs_names = []
        for i in range(nobs):
            on = np.fromfile(f,self.char, count=20).tostring().lower()
            obs_names.append(on)
            #print 'obs:',on
                
        self.parameters = par_names
        self.observations = obs_names
        
        
    def to_ascii(self,out_filename,icode=2):                
        nrow,ncol = len(self.observations),len(self.parameters)
        f_out = open(out_filename,'w')
        f_out.write(' {0:7.0f} {1:7.0f} {2:7.0f}\n'.format(nrow,ncol,icode))
        for i in range(nrow):            
            for j in range(ncol):
                f_out.write(' {0:15.7e} '.format(self.x[i,j]))                      
                if j % 7 == 0:
                    f_out.write('\n')
            f_out.write('\n')    
        f_out.write('* row names\n')
        for r in row_names:
            f_out.write(r+'\n')
    
        f_out.write('* column names\n')
        for c in col_names:
            f_out.write(c+'\n')
        f_out.close()







