import time
import copy
import numpy as np
import pandas

class matrix():
    def __init__(self,x=None,row_names=None,col_names=None):
        self.col_names,self.row_names = col_names,row_names
        self.x = x
        if x is not None:
            if row_names is not None:
                assert len(row_names) == x.shape[0],\
                    'shape[0] != len(row_names) '+str(x.shape)+' '+str(len(row_names))
            if col_names is not None:
                assert len(col_names) == x.shape[1],\
                    'shape[1] != len(col_names) '+str(x.shape)+' '+str(len(col_names))
        self.integer = np.int32
        self.double = np.float64
        self.char = np.uint8

    

    @property
    def shape(self):
        if self.x is None:
            return None
        else:
            return self.x.shape


    def svd(self):
        if self.x is None:
            raise Exception('self.x not set')
        #--build some name lists
        left_names,right_names,sing_names = [],[],[]
        for i in range(self.shape[0]):
            right_names.append('right_singvec_'+str(i+1))
        for j in range(self.shape[1]):
            left_names.append('left_singvec_'+str(j+1))
        for k in range(min(self.shape)):
            sing_names.append('sing_val_'+str(k+1))
        u,s,vt = np.linalg.svd(self.x)
        u = matrix(u,self.row_names,right_names)
        s = matrix(np.atleast_2d(s).transpose(),sing_names,['none'])
        vt = matrix(vt,left_names,self.col_names)
        return u,s,vt


            
    
    def vector(self,k):
        k = k.lower()
        self.col_names = list(self.col_names)
        self.row_names = list(self.row_names)
        if k in self.col_names:
            mat = matrix()
            mat.x = np.atleast_2d(self.x[:,self.col_names.index(k)].copy()).transpose()
            mat.row_names = copy.deepcopy(self.row_names)
            mat.col_names= [k]
            return mat
        elif k in self.row_names:
            mat = matrix()
            mat.x = np.atleast_2d(self.x[self.row_names.index(k),:].copy()).transpose()
            mat.row_names = copy.deepcopy(self.col_names)
            mat.col_names= [k]
            return mat
        else:
            raise Exception(str(k)+' not in col or row names')
    
    def to_binary(self,out_filename=None):
        if out_filename is None:
            out_filename = self.filename
        f = open(out_filename,'wb')
        f.close()

    def from_binary(self,filename):        
        f = open(filename,'rb')
        #--the header datatype
        header_dt = np.dtype([('itemp1',self.integer),('itemp2',self.integer),('icount',self.integer)])
        itemp1,itemp2,icount = np.fromfile(f,header_dt,1)[0]
        if itemp1 >= 0:
            raise TypeError, 'Jco produced by deprecated version of PEST,'+\
                             'Use JCOTRANS to convert to new format'
        if self.shape is not None:
            if abs(itemp1) != self.ncol:
                raise ValueError,'ncol value not equal to matrix dimensions'\
                                 +str(ncol)+' '+str(abs(itemp1))
        if self.shape is not None:
            if abs(itemp2) != self.nrow:
                raise ValueError,'nrow value not equal to matrix dimensions'\
                                 +str(nrow)+' '+str(abs(itemp2))
        ncol,nrow = abs(itemp1),abs(itemp2)    
        self.shape = (nrow,ncol)                              
        self.x = np.zeros((nrow,ncol))    
        start = time.clock()
        #--the record datatype
        rec_dt = np.dtype([('j',self.integer),('dtemp',self.double)])
    
        #--read all data records
        #--using this a real memory hog
        data = np.fromfile(f,rec_dt,icount) 
    
        #--uncompress the data into x    
        for i in data:
        #for ii in range(icount):
            #i = np.fromfile(f,rec_dt,1)[0]
            j = i[0]
            dtemp = i[1]
            icol = ((j-1) / nrow) + 1
            irow = j - ((icol - 1) * nrow)
            #print i,ies,irow
        
            #--zero-based indexing translation
            self.x[irow-1,icol-1] = dtemp
        #print time.clock() - start
        #--read parameter names
        col_names = []
        for i in range(ncol):
            cn = np.fromfile(f,self.char, count=12).tostring().lower()
            col_names.append(cn)
            #print 'par:',pn
    
        #--read obs names
        row_names = []
        for i in range(nrow):
            rn = np.fromfile(f,self.char, count=20).tostring().lower()
            row_names.append(rn)
            #print 'obs:',on
                
        self.col_names = col_names
        self.row_names = row_names
        
        
    def to_ascii(self,out_filename,icode=2):                
        #start = time.clock()
        nrow,ncol = self.shape
        f_out = open(out_filename,'w')
        f_out.write(' {0:7.0f} {1:7.0f} {2:7.0f}\n'.format(nrow,ncol,icode))
        #for i in range(nrow):            
        #    for j in range(ncol):
        #        f_out.write(' {0:15.7e} '.format(self.x[i,j]))                      
        #        if (j+1) % 7 == 0:
        #            f_out.write('\n')
        #    f_out.write('\n')    
        np.savetxt(f_out,self.x,fmt='%15.7E')
        if icode == 1:
            f_out.write('* row and column names\n')
            for r in self.row_names:
                f_out.write(r+'\n')

        else:

            f_out.write('* row names\n')
            for r in self.row_names:
                f_out.write(r+'\n')
    
            f_out.write('* column names\n')
            for c in self.col_names:
                f_out.write(c+'\n')
            f_out.close()
            #print time.clock() - start

    def from_ascii(self,filename):
        f = open(filename,'r')
        raw = f.readline().strip().split()
        nrow,ncol,icode = int(raw[0]),int(raw[1]),int(raw[2])
        x,icount = [],0
        while True:
            line = f.readline().strip().split()
            for l in line:
                x.append(float(l))
                icount += 1
            if icount == nrow * ncol:
                break
        line = f.readline().strip().lower()
        if not line.startswith('*'):
            raise Exception('error loading ascii file,line should start with '*', not '+line)
        if 'row' in line and 'column' in line:
            assert nrow == ncol
            names = []
            for i in range(nrow):
                line = f.readline().strip().lower()
                names.append(line)
            self.row_names = names
            self.col_names = names
        else:
            names = []
            for i in range(nrow):
                line = f.readline().strip().lower()
                names.append(line)
            self.row_names = names
            line = f.readline().strip().lower()
            names = []
            for j in range(ncol):
                line = f.readline().strip().lower()
                names.append(line)
            self.col_names = names
        f.close()
        x = np.array(x,dtype=self.double)
        x.resize(nrow,ncol)
        self.x = x                

                            
class uncert(matrix):
    def __init__(self,names):
        self.names = list(names)
        self.x = np.zeros((len(names),len(names)))
        self.row_names = names
        self.col_names = names


    
    def from_uncfile(self,filename):
        visited = [False] * len(self.names)
        f = open(filename,'r')
        while True:
            line = f.readline().strip().lower()
            if line == '':
                break
            if 'start' in line:
                if 'standard_deviation' in line:
                    while True:
                        line2 = f.readline().strip().lower()
                        if 'end' in line2:
                            break
                        raw = line2.strip().split()
                        name,val = raw[0],float(raw[1])
                        if name in self.names:
                            idx = self.names.index(name)
                            self.x[idx,idx] = val**2
                
                elif 'covariance_matrix' in line:
                    while True:
                        line2 = f.readline().strip().lower()
                        if 'end' in line2:
                            break
                        if line2.startswith('file'):
                            cov = matrix()
                            cov.from_ascii(line2.split()[1])
                            pass
                        elif line2.startswith('variance_multiplier'):
                            self.var = float(line2.split()[1])
                        else:
                            raise Exception('unrecognized keyword in std block: '+line2)
                

                    
        f.close()

