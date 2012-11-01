import numpy as np

EXP = 'exponential'
GAU = 'gaussian'

def exp_vario(h,a=1.0,sill=1.0):
   return sill * (1.0 - (np.exp((-h/a))))


def gauss_vario(h,a=1.0,sill=1.0):
    return sill * (1.0 - (np.exp((-h**2)/(a**2))))

def dist(p1,p2):
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5

class mfgrid():
    def __init__(self,xoff,yoff,nrow,ncol,delr,delc,rotation=0.0):
        self.xoff = float(xoff)
        self.yoff = float(yoff)                  
        self.nrow = int(nrow)
        self.ncol = int(ncol)                              
        if isinstance(delr,int):
                delr = float(delr)
        if isinstance(delr,float):
                delr = np.zeros(self.ncol) + delr
        assert len(delr) == self.ncol
        self.delr = delr
        if isinstance(delc,int):
                delc = float(delc)
        if isinstance(delc,float):
                delc = np.zeros(self.nrow) + delc
        assert len(delc) == self.nrow
        self.delc = delc

        
        self.rotation = float(rotation)
    
    def xnode_locations(self):
        cols = np.cumsum(self.delr) + self.xoff
        xs = []
        for j in range(self.ncol):
            x = self.xoff + cols[j] - (self.delr[j]/2.0)
            xs.append(x)
        return xs

    def ynode_locations(self):
        rows = np.cumsum(self.delc) + self.yoff
        ys = []
        for i in range(self.nrow):                
            y = self.yoff + rows[i] - (self.delc[i]/2.0)                
            ys.append(y)
        return ys

    def node_locations(self):
        points = []
        xs = self.xnode_locations()
        ys = self.ynode_locations()
        for x in xs:
            for y in ys:
                points.append([x,y])
        return np.array(points)                
        
    def write_grid(self,filename):
        f = open(filename,'w')
        f.write(' {0:10.0f} {1:10.0f}\n'.format(self,nrow,self.ncol))
        f.write(' {0:15.6e} {1:15.6e} {2:15.6e}\n'.format(self.xoff,self.yoff,self.rotation))
        for i in self.delc:
            f.write(' {0:15.6e}'.format(i))
        f.write('\n')
        for j in self.delr:
            f.write(' {0:15.6e}'.format(j))
        f.write('\n')
        f.close()
                                                                                        
class geostat():
    def __init__(self,a,sill,vtype,nodes,nugget=0.0):
        self.a = float(a)
        self.sill = float(sill)
        self.nugget = float(nugget)        
        self.eigvals = None
        self.eigvecs = None
        self.cov = None
        self.forward = None
        self.back = None
        self.nodes = nodes
        if 'EXP' in vtype.upper():
            self.vtype = EXP
            self.vario = exp_vario
        elif 'GAU' in vtype.upper():
            self.vtype = GAU                         
            self.vario = gauss_vario
        else:
            raise TypeError('only '+EXP+' or '+GUA+' variograms are supported')
    
    def build_covariance(self):
        nnodes = self.nodes.shape[0]
        cov = np.zeros((nnodes,nnodes)) - 1.0e+10
        for p in range(nnodes):
            cov[p,p] = self.sill + self.nugget
        #--fill in the upper tri along rows
        for i in range(nnodes):
            for j in range(i+1,nnodes):
                d = dist(self.nodes[j],self.nodes[i])
                v = self.vario(d,sill=self.sill,a=self.a)
                cov[i,j] =  (self.sill + self.nugget) -  v
        #--replicate across the diagonal
        for i in range(nnodes):
            for j in range(i+1,nnodes):
                cov[j,i] = cov[i,j] 
        self.cov = cov
        
    def eig(self):
        if self.cov == None:
            self.build_covariance()
        u,s,vt = np.linalg.linalg.svd((self.cov))
        self.eigvecs = u
        self.eigvals = s**2
         
    def build_forward_kl(self,itrunc):
        '''self.eigvals^-0.5 * self.eigvecs^T
        '''
        if self.eigvecs == None:
            self.eig()
        forward = self.eigvecs[:,:itrunc].copy()
        for i in range(itrunc):
            forward[:,i] *= 1.0/(np.sqrt(self.eigvals[i]))
        forward = forward.transpose()
        self.forward = forward
    
    def build_back_kl(self,itrunc): 
        if self.eigvecs == None:
            self.eig()    
        back = self.eigvecs[:,:itrunc].copy()
        for i in range(itrunc):
            back[:,i] *= np.sqrt(self.eigvals[i])        
        self.back = back                                                