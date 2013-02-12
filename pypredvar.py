import numpy as np
import pandas
import mat_handler as mhand
import pst_handler as phand
import pypredvar as pvar

class predvar():
    '''
    doesnt support obs covariance matrices
    '''
    def __init__(self,jco,pcov,ocov,pred_vectors,singular_values,ref_var=1.0):
        self.jco = jco
        self.pcov = pcov
        self.ocov = ocov
        self.pred_vectors = pred_vectors
        self.singular_values = singular_values
        self.ref_var = ref_var
 

    #@property
    #def cov_obs(self):
    #    if self.__cov_obs is not None:
    #        return self.__cov_obs
    #    else:
    #        obs_var = (1.0/self.pst.observation_data.weight.values)**2
    #        obs_names = self.pst.observation_data.obsnme.values
    #        cov_obs = mhand.matrix(np.atleast_2d(np.array(obs_var)).transpose(),obs_names)
    #        self.__cov_obs = cov_obs
    #        return cov_obs
            
    def jco_2_qhalfx(self):
        for i in range(self.jco.shape[0]):
            self.jco[i,:] *= np.sqrt(self.ocov[i])

    def scale_jco(self):
        u,s,vt = np.linalg.svd(self.pcov)
        s = 1.0/(np.sqrt(s))
        self.jco = np.dot(self.jco,u)
        self.jco = np.dot(self.jco,s)
        return

    def calc(self):
        #self.align_vectors()
        print 'scaling JCO'
        #self.scale_jco()
        print 'forming q^(1/2)X'
        #self.jco_2_qhalfx()
        print 'SVD on q^(1/2)X'
        #u,s,vt = np.linalg.svd(self.jco,full_matrices=False)
        #np.savetxt('u.mat',u,fmt='%15.7E')
        #np.savetxt('s.mat',s,fmt='%15.7E')
        #np.savetxt('vt.mat',vt,fmt='%15.7E')
        u = np.loadtxt('u.mat')
        #s = np.diagflat(np.loadtxt('s.mat'))
        s = np.loadtxt('s.mat')
        s_inv = 1.0/s
        v = np.loadtxt('vt.mat').transpose()
        nrow,ncol = self.jco.shape
        if nrow > ncol:
            u = u[:ncol,:ncol]
        elif ncol > nrow:
            v = v[:nrow,:nrow]
        print 'starting singular value cycle'
        #--open file handles for each results file

        results = []
        for name,p in self.pred_vectors.iteritems(): 
            f = open(name,'w',0)
            f.write('{0:10s} {1:15s} {2:15s}\n'.format('sing_val','first_term','second_term'))
            results.append(f)
        for s in self.singular_values:
            print s,'\r',
            if s == 0:
                pass
            elif s > self.jco.shape[1]:
                pass
            else: 
                I_minus_R = np.dot(v[:,s:],v[:,s:].transpose())
                G = v[:,:s]
                for i in range(s):
                    G[:,i] *= s_inv[i]
                G = np.dot(G,u[:,:s].transpose())
                 
                for i,[name,p] in enumerate(self.pred_vectors.iteritems()):
                    first = np.dot(p.transpose(),I_minus_R)
                    first = np.dot(first,p)
                    second = np.dot(p.transpose(),G)
                    second = np.dot(second,p)
                    line = '{0:10d} {1:15.6E} {2:15.6E}\n'.format(s,float(first),float(second))
                    results[i].write(line)

        for r in results:
            r.close()
                    
                    
                    
                

        


    
        

            

    #def align_vectors(self):
    #    #--loop over each pred vector
    #    for i,pred_vector in enumerate(self.pred_vectors):
    #        #--align the pred vector
    #        pvec = [0.0] * self.jco.shape[1]
    #        visited = [False] * self.jco.shape[1]
    #        for pname,val in zip(pred_vector.row_names,pred_vector.x):
    #            if pname in self.jco.col_names:
    #                idx = self.jco.col_names.index(pname)
    #                pvec[idx] = val
    #                visited[idx] = True
    #        if False in visited:
    #            for i,v in enumerate(visited):
    #                if not v:
    #                    print self.jco.col_names[i],' not found in pred vector',pred_vector.col_names
    #            raise Exception
    #        pred_vector.row_names = self.jco.col_names
    #        pred_vector.x = np.atleast_2d(np.array(pvec)).transpose()
    #        self.pred_vectors[i] = pred_vector
    #        pass
                               
                 
    #def check(self):
    #    errors = []
    #    #--check that all jco obs are in the pst
    #    for oname in self.jco.row_names:
    #        if oname not in self.pst.observation_data.obsnme:
    #            errors.append('jco obs name missing from pst file '+oname )
    #    #--check pred vectors
    #    for pred_vector in pred_vectors:
    #        for pname in pred_vector.col_names:
    #            if pname not in jco.col_names:
    #                errors.append('pred vector par name not in jco: '+pname)
