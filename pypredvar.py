import numpy as np
import scipy 
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
    def __init__(self,jco,pred_vectors,singular_values,ref_var=1.0,\
             verbose=False,jco_struct=None,pred_vectors_struct=None,\
             struct_cov=None,par_cov=None,obs_cov=None,qhalf=None):
        self.jco = jco        
        self.pred_vectors = pred_vectors
        self.singular_values = singular_values
        self.ref_var = ref_var
        self.verbose = bool(verbose)
        self.jco_struct = jco_struct
        self.pred_vectors_struct = pred_vectors_struct
        self.struct_cov = struct_cov
        self.par_cov = par_cov
        self.obs_cov = obs_cov
        self.qhalf = qhalf
 
    def calc(self):        
        print 'SVD on scaled q^(1/2)X'
        try:
            u,s_vec,vt = np.linalg.svd(self.jco)
            v = vt.transpose()
        except Exception as e:
            print str(e)
            print 'svd failed, trying SVD on (q^(1/2)X)^T'            
            try:
                v,s_vec,u = scipy.linalg.svd(self.jco.transpose())
            except Exception as e:
                print 'both attempts of SVD failed...shit out of luck'
                print str(e)
            u = u.transpose()

        
        #s_vec = s_vec **2

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
            f.write('{0:10s} {1:15s} {2:15s}'.format('sing_val','first_term','second_term'))           
            f.write(' {0:15s}'.format('third_term'))
            f.write(' {0:15s} {1:15s}\n'.format('total_var','st_dev'))
            
            for sv in self.singular_values:            
                print name,sv,'\r',
                        
                if sv > self.jco.shape[1]:
                    first = 0.0                
                elif self.par_cov is None:
                    first = np.dot(p.transpose(),v[:,sv:])                    
                    first = np.dot(first,v[:,sv:].transpose())                    
                    first = np.dot(first,p)                   
                else:
                    temp = np.dot(p.transpose(),v[:,sv:])                                         
                    temp = np.dot(temp,v[:,sv:].transpose())                                
                    first = np.dot(temp,self.par_cov)                                      
                    first = np.dot(first,temp.transpose())
                                                         

                if sv == 0.0:
                    second = 0.0                
                else:                    
                    if sv > s_vec.shape[0]:
                        second = 1.0e+35                    
                    else:
                       
                        temp = np.dot(p.transpose(),v[:,:sv])
                        second = 0.0
                        for i in range(sv):
                            second += temp[0,i] * s_inv[i] * s_inv[i] * temp[0,i]
                        
                        #if self.obs_cov is None:
                        #    second = 0.0
                        #    for i in range(sv):
                        #        second += temp[0,i] * s_inv[i] * s_inv[i] * temp[0,i]
                        #else:
                        #    for i in range(sv):
                        #        temp[0,i] *= s_inv[i]
                        #    temp  = np.dot(temp,u[:,:sv].transpose())
                        #    second = np.dot(temp,self.obs_cov)                            
                        #    second = np.dot(second,temp.transpose())
                        #temp = np.dot(p.transpose(),v[:,:sv])
                        #for i in range(sv):
                        #    temp[0,i] *= s_inv[i]
                        #temp = np.dot(temp,u[:,:sv].transpose())
                        #temp = np.dot(temp,self.qhalf)
                      
                        #if self.obs_cov is None:
                        #    second = np.dot(temp,temp.transpose())
                        #else:
                        #    second = np.dot(temp,self.obs_cov)
                        #    second = np.dot(second,temp.transpose())
                             
                if self.jco_struct is not None:
                    if sv > s_vec.shape[0]:
                        third = 1.0e+35 
                    else:    
                        ps = self.pred_vectors_struct[name]
                        temp = np.dot(p.transpose(),v[:,:sv])                    
                        for i in range(sv):
                            temp[0,i] *= s_inv[i]
                        temp = np.dot(temp,u[:,:sv].transpose())
                        #temp = np.dot(temp,self.qhalf)
                        temp = np.dot(temp,self.jco_struct).transpose()
                        temp -= ps  
                        if self.struct_cov is None:                  
                            third = np.dot(temp.transpose(),temp)                                           
                        else:
                            third = np.dot(temp.transpose(),self.struct_cov)
                            #print third.shape,temp.shape,self.struct_cov.shape 
                            third = np.dot(third,temp)
                else:
                    third = 0.0
                tot_var = first + second + third
                stdev = np.sqrt(tot_var)
                line = '{0:10d} {1:15.6E} {2:15.6E} {3:15.6E} {4:15.6E} {5:15.6E}\n'\
                    .format(sv,float(first),float(second),float(third),float(tot_var),float(stdev))
                f.write(line)
                if second >= 1.0e+35:
                    break
            f.close()
