import numpy as np
from scipy import linalg
import pandas
import mat_handler as mhand
import pst_handler as phand

class param_unc_var():

    def __init__(self,case,par_uncfile=None,obs_uncfile=None,ref_var=1.0,verbose=False):
        self.case = case
        self.par_uncfile = par_uncfile
        self.obs_uncfile = obs_uncfile
        self.pst = self.load_pst()
        self.jco = self.load_jco()
        self.ref_var = ref_var
        self.verbose = bool(verbose)

        self.__par_scaled = False
        self.__obs_scaled = False
        self.__qhalf = None
        self.__fehalf = None
        self.__par_unc = None
        self.__obs_unc = None
        self.__v = None
        self.__s_vec = None
        self.__u = None

    def load_pst(self):
        return phand.pst(self.case+".pst")

    def clean_jco(self):
        #--remove zero-weight and regul obs
        drop_row_names = []
        nz_weights,nz_names = [],[]
        for name,weight in zip(self.pst.observation_data.obsnme,\
                               self.pst.observation_data.weight):
            if weight == 0.0:
                drop_row_names.append(name)
            else:
                nz_weights.append(weight)
                nz_names.append(name)
        self.jco.drop(drop_row_names)

    def load_jco(self):
        jco = mhand.matrix()
        jco.from_binary(self.case+".jco")
        return jco

    def scale_jco(self):
        self.apply_kl_inplace()
        self.apply_qhalf_inplace()        
                 
        self.__v = None
        self.__s_vec = None
        self.__u = None

    def apply_kl_inplace(self):       
        self.jco.x = np.dot(self.jco.x,self.fehalf)
        self.__par_unc.x = np.diag(np.ones((self.jco.shape[1])))
        self.__par_scaled = True
              
    def apply_qhalf_inplace(self):
        self.jco.x = np.dot(self.qhalf,self.jco.x)
        self.obs_unc.x = np.diag(np.ones((self.jco.x.shape[0])))
        self.__obs_scaled = True

    def var_first(self,nsing):
        if nsing > self.jco.shape[1]:
            return np.zeros((self.jco.shape[1]))
        v2v2t = np.dot(self.v[:,nsing:],self.v[:,nsing:].transpose())
        if self.__par_scaled:
            first = v2v2t
        else:
            first = np.dot(v2v2t,self.par_unc.x)
            first = np.dot(first,v2v2t.transpose())
        #first = np.dot(self.v[:,nsing:],self.v[:,nsing:].transpose())
        #first = np.dot(first,self.par_unc.x)
        #first = np.dot(first,self.v[:,nsing:])
        #first = np.dot(first,self.v[:,nsing:].transpose())


        return np.diag(first)

    def var_second(self,nsing):
        if nsing == 0:
            return np.zeros((self.jco.shape[1]))
        else:
            if nsing > self.s_vec.shape[0]:
                return np.zeros((self.jco.shape[1])) + 1.0E+35
            elif np.any(self.s_vec[:nsing] < 1.0e-20):
                return np.zeros((self.jco.shape[1])) + 1.0E+35
            
            else:    
                s_inv = 1.0/self.s_vec                                
                G = self.v[:,:nsing]
                for ising in range(nsing):
                    G[:,ising] *= s_inv[ising]
                G = np.dot(G,self.u[:,:nsing].transpose())
                if self.__obs_scaled:
                    second = np.dot(G,G.transpose())
                else:
                    second = np.dot(G,self.obs_unc.x)
                    second = np.dot(second,G.transpose())
                #return np.diag(np.dot(second,self.v[:,:nsing].transpose()))
                return self.ref_var * np.diag(second)

    def unc(self):
        if self.__obs_scaled:
            raise Exception("not qhalf scaling for unc() calculation")
        if self.__par_scaled:
            raise Exception("not KL transform for unc() calculation")
        #--form XtC-1(e)X
        obs_unc = self.obs_unc.x
        par_unc = self.par_unc.x
        obs_inv = linalg.inv(self.obs_unc.x)
        first = np.dot(self.jco.x.transpose(),obs_inv)
        first = np.dot(first,self.jco.x)
        second = linalg.inv(self.par_unc.x)
        return linalg.inv(first+second)                        

    @property
    def fehalf(self):
        if self.__fehalf != None:
            return self.__fehalf
        u,s,vt = linalg.svd(self.par_unc.x)      
        for i in range(u.shape[0]):
            u[:,i] *= s[i]**(0.5)
        self.__fehalf = u
        return self.__fehalf

    @property
    def u(self):
        if self.__u != None:
            return self.__u
        self.__set_jco_svd()
        return self.__u

    @property
    def s_vec(self):
        if self.__s_vec != None:
            return self.__s_vec
        self.__set_jco_svd()
        return self.__s_vec

    @property
    def v(self):
        if self.__v != None:
            return self.__v
        self.__set_jco_svd()
        return self.__v

    def __set_jco_svd(self):
        if self.__u != None:
            return
        try:
            u,s_vec,vt = linalg.svd(self.jco.x)
            v = vt.transpose()
        except Exception as e:
            print str(e)
            print 'svd failed, trying SVD on (q^(1/2)X)^T'
            try:
                v,s_vec,u = linalg.svd(self.jco.x.transpose())
            except Exception as e:
                print 'both attempts of SVD failed...shit out of luck'
                print str(e)
                raise
            u = u.transpose()
        self.__u = u
        self.__s_vec = s_vec
        self.__v = v

    @property
    def par_unc(self):
        if self.__par_unc != None:
            return self.__par_unc
        self.__par_unc = mhand.uncert(self.nes_names)
        if isinstance(self.par_uncfile,np.ndarray):
            self.__par_unc.x = self.par_uncfile
        elif self.par_uncfile is None:
            self.__par_unc.x = np.diag(np.ones((self.jco.shape[1])))
        elif self.par_uncfile.endswith("pst"):
            self.__par_unc.from_parbounds(self.par_uncfile)
        else:
            self.__par_unc.from_uncfile(self.par_uncfile)
        
        return self.__par_unc

    @property
    def obs_unc(self):
        if self.__obs_unc != None:
            return self.__obs_unc
        if self.obs_uncfile is not None:
            self.__obs_unc = mhand.uncert(self.nz_names)
            self.__obs_unc.from_uncfile(self.obs_uncfile)
        else:
            self.__obs_unc = mhand.uncert(self.nz_names)
            self.__obs_unc.from_obsweights(self.case+".pst")
        return self.__obs_unc

    @property
    def nes_names(self):
        return self.jco.col_names

    @property
    def nz_names(self):
        return self.jco.row_names

    @property
    def qhalf(self):
        if self.__qhalf != None:
            return self.__qhalf
        u,s,vt = linalg.svd(self.obs_unc.x)
        for i in range(u.shape[0]):
            u[:,i] *= s[i]**(-0.5)
        self.__qhalf = np.dot(u,vt)
        return self.__qhalf



if __name__ == "__main__":

    def exp_vario(h,a=1.0,sill=1.0):
        return sill * (1.0 - (np.exp((-h/a))))

    def dist(p1,p2):
        return ((p1 - p2)**2)**0.5

    import os
    os.chdir(r"D:\Users\jwhite\git_repo\pestpp\pest++\benchmarks\10par_xsec")
    #--define and fill covariance matrix
    #a = 300
    #sill = 1.0
    #delr = np.arange(10,110,10)

    #cov = np.zeros((10,10))
    ##--fill in the diagonal
    #for p in range(10):
    #    cov[p,p] = sill
    ##--fill in the upper tri along rows
    #for i in range(10):
    #    for j in range(i+1,10):
    #        d = dist(delr[j],delr[i])
    #        v = exp_vario(d,sill=sill,a=a)
    #        cov[i,j] =  sill -  v
    ##--replicate across the diagonal
    #for i in range(10):
    #    for j in range(i+1,10):
    #        cov[j,i] = cov[i,j]  
    


    case = "pest"
    pe = param_unc_var(case,par_uncfile=case+".pst")
    #for i in range(pe.obs_unc.shape[0]):
    #    if pe.obs_unc[i,i] == 0:
    #        pe.obs_unc[i.i] = 1.0e-30
    pe.par_unc.to_uncfile("10par.unc","10par.cov")
    pe.clean_jco()
    postunc = pe.unc()
    #pe.jco.x = np.zeros((10,10))
    #for i in range(10):
    #    pe.jco.x[i,i] = 1
    
    #for ising in range(4):
    #    print pe.var_first(ising)[0],pe.var_second(ising)[0]
    #pe.scale_jco()
    #print pe.jco.x
    #for ising in range(4):
    #    print pe.var_first(ising)[0],pe.var_second(ising)[0]
   
    #print pe.par_unc.x
    print np.diag(postunc)
    print
