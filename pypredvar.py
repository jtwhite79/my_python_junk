import numpy as np
import pandas
import mat_handler as mhand
import pst_handler as phand
import pypredvar as pvar

class predvar():
    '''
    takes scaled q^(1/2)X so doesn't need param unc information
    X should be scaled and shouldn't contain any zero-weight obs or regul obs
    assumes pred vectors have been aligned with corrected X
    '''
    def __init__(self,jco,pred_vectors,singular_values,ref_var=1.0,verbose=False,jco_struct=None,pred_vectors_struct=None):
        self.jco = jco        
        self.pred_vectors = pred_vectors
        self.singular_values = singular_values
        self.ref_var = ref_var
        self.verbose = bool(verbose)
        self.jco_struct = jco_struct
        self.pred_vectors_struct = pred_vectors_struct

 
    def calc(self):        
        print 'SVD on scaled q^(1/2)X'
        u,s_vec,vt = np.linalg.svd(self.jco)
        
        v = vt.transpose()
        s_vec = s_vec **2

        #--for testing       
        #u = np.loadtxt('u_py.mat')        
        #s_vec = np.loadtxt('s_py.mat')        
        #v = np.loadtxt('vt_py.mat').transpose()
        
        
        if self.verbose:
            np.savetxt('u_py.mat',u,fmt='%25.10E')
            np.savetxt('s_py.mat',s_vec,fmt='%25.10E')
            np.savetxt('vt_py.mat',vt,fmt='%25.10E')
            
        s_inv = 1.0/s_vec                
        nrow,ncol = self.jco.shape
                

        for i,[name,p] in enumerate(self.pred_vectors.iteritems()):
            f = open(name,'w',0)
            f.write('{0:10s} {1:15s} {2:15s}\n'.format('sing_val','first_term','second_term'))
            for sv in self.singular_values:            
                print name,sv,'\r',
                        
                if sv > self.jco.shape[1]:
                    first = 0.0                
                else:
                    first = np.dot(p.transpose(),v[:,sv:])                    
                    first = np.dot(first,v[:,sv:].transpose())                    
                    first = np.dot(first,p)                   
                if sv == 0.0:
                    second = 0.0                
                else:                    
                    if sv > s_vec.shape[0]:
                        second = 1.0e+35                    
                    else:
                        
                        temp = np.dot(p.transpose(),v[:,:sv])
                        second = 0.0
                        for i in range(sv):
                            second += temp[0,i] * s_inv[i] * temp[0,i]
                    
                if self.jco_struct is not None:
                    if sv > s_vec.shape[0]:
                        third = 1.0e+35 
                    else:    
                        ps = self.pred_vectors_struct[name]
                        temp = np.dot(p.transpose(),v[:,:sv])                    
                        for i in range(sv):
                            temp[0,i] *= s_inv[i]
                        temp = np.dot(temp,u[:,:sv].transpose())
                        temp = np.dot(temp,self.jco_struct).transpose()
                        temp -= ps                    
                        third = np.dot(temp.transpose(),temp)                                           
                else:
                    third = 0.0
                line = '{0:10d} {1:15.6E} {2:15.6E} {3:15.6E}\n'.format(sv,float(first),float(second),float(third))
                f.write(line)
            f.close()
