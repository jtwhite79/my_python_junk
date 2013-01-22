import math
import numpy as np
import pylab

class prism():    
    def __init__(self):
        return
        
    def set(self,key,val):
        if key in self.p_dict:
            self.p_dict[key] = val
        else:
            print 'key '+key+' not in p_dict'
            raise KeyError
        return
    
    def add_key(self,key,val=None):
        if key not in self.p_dict:
            self.p_dict[key] = val
        else:
            print 'key '+key+' already exists'
            raise KeyError
        return
    
    def rm_key(self,key):
        if key in self.p_dict:
            self.p_dict.pop(key)
        else:
            print 'key '+key+' not in p_dict'
            raise KeyError
        return
        
    def get_p_dict(self):
        return self.p_dict       

    def e(self):
        term2 = (self.p_dict['Q']**2) / \
                (2.0 * self.p_dict['g'] * self.area()**2)
        return self.p_dict['y'] + term2

    def r(self):
        r = self.area() / self.p()
        return r           
    
    def f(self):
        try:
            return self.p_dict['v'] / (self.p_dict['g'] * self.dh())**0.5
        except:
            try:
                v = self.p_dict['q'] / self.p_dict['y']        
                return v / (self.p_dict['g'] * self.dh())**0.5
            except:
                v = self.p_dict['Q'] / self.area()
                return v / (self.p_dict['g'] * self.dh())**0.5         

    def dh(self):
        area = self.area()
        width = self.width()
        dh = area / width
        return dh

    def yc(self):    
        r = 1.0e+20
        correct_yc = -999
        self.add_key('y')
        for y in self.p_dict['Y']:
            self.set('y',y)
            this_f = self.f()            
            this_r = abs(this_f - 1.0)
            if this_r < r:
                r = this_r
                correct_yc = y
        if correct_yc == self.p_dict['Y'][0] or \
           correct_yc == self.p_dict['Y'][-1]:
            print 'Y does not bracket yc'
            raise IndexError                           
        self.rm_key('y')
        return correct_yc 
 
    def y0(self):
        rhs = (self.p_dict['n'] * self.p_dict['Q']) / \
              (self.p_dict['kn'] * (self.p_dict['s']**0.5))          
        r = 1.0e+20
        correct_y0 = -999    
        self.add_key('y')
        for y in self.p_dict['Y']:
            self.set('y',y)
            lhs = (self.area()**(5.0/3.0)) /  (self.p()**(2.0/3.0))
            this_r = abs(lhs-rhs)
            if this_r < r:
                r = this_r
                correct_y0 = y
        #print correct_y0
        if correct_y0 == self.p_dict['Y'][-1] or \
           correct_y0 == self.p_dict['Y'][0]:
            print 'Y does not bracket y0'
            raise IndexError            
        self.rm_key('y')
        return correct_y0               


    def mann_Q(self):
        Q = (self.p_dict['kn']/self.p_dict['n']) * \
            self.area() * self.r()**(2.0/3.0) * self.p_dict['s']**0.5
        return Q
    
    def v(self):
        return self.p_dict['Q'] / self.area()
    
    def se(self):
        return (self.p_dict['n']**2 * self.v()**2) / self.r()**(4.0/3.0)
    
    
    def direct_step(self,Y,length=None):        
        X = np.zeros_like(Y)
        V = np.zeros_like(Y)
        Se = np.zeros_like(Y)
        SeBar = np.zeros_like(Y)
        E = np.zeros_like(Y)
        DeltaE = np.zeros_like(Y)
        DeltaX = np.zeros_like(Y)
        M = np.zeros_like(Y)
        self.add_key('y')
        if length != None:
            X[0] = length
        
        for idx in range(len(Y)):
            self.set('y',Y[idx])
            this_e = self.e()
            this_se = self.se()
            this_v = self.v()
            this_m = self.m()
            V[idx] = this_v
            E[idx] = this_e
            Se[idx] = this_se                        
            M[idx] = this_m
            
            if idx != 0:                
                this_sebar = (Se[idx-1] + this_se)/2.0
                this_delta_e = (E[idx] - E[idx-1])
                this_delta_x =  this_delta_e / (self.p_dict['s'] - this_sebar)
                Se[idx] = this_se
                SeBar[idx] = this_sebar
                E[idx] = this_e
                DeltaE = this_delta_e
                DeltaX = this_delta_x
                X[idx] =  X[idx-1] + this_delta_x       
        self.rm_key('y')
        return [X,V,Se,E,DeltaE,DeltaX,M]
                
    def sc(self):
        numer = self.p_dict['n']**2 * self.p_dict['Q']**2
        demon = self.p_dict['kn']**2 * self.area()**2 * self.r()**(4.0/3.0)
        so_crit = numer/demon           
        return so_crit

    def find_depths(self,target,function):
        
        #--calculate the residuals
        rs = np.zeros_like(self.p_dict['Y'])
        mins = []
        self.add_key('y')
        for idx in range(self.p_dict['Y'].shape[0]):
            #--calc this_e
            self.set('y',self.p_dict['Y'][idx])
            this_val = function()
            #--calc this residual
            this_r = abs(this_val - target)
            rs[idx] = this_r
            
        #--loop over the residuals looking for minimums
        mins = []
        for idx in range(1,rs.shape[0]-1):
            if rs[idx] < rs[idx-1] and rs[idx] < rs[idx+1]:
                mins.append(idx)
        self.rm_key('y')
        return self.p_dict['Y'][mins]                
        
    
class rect(prism):
    def __init__(self,p_dict):
        self.p_dict = p_dict
    
    def area(self):
        return self.p_dict['y'] * self.p_dict['b']
    
    def width(self):
        return self.p_dict['b']
    
    def p(self):
        p = self.p_dict['b'] + (2.0 * self.p_dict['y'])
        return p
    def m(self):
        term1 = (self.p_dict['b'] * self.p_dict['y']**2) / 2.0
        term2 = self.p_dict['Q']**2/(self.p_dict['g'] * \
                self.p_dict['b'] * self.p_dict['y'])
        m = term1 + term2   
        return m
    def e(self):
        try:
            term2 = (self.p_dict['Q']**2) / \
                    (2.0 * self.p_dict['g'] * self.area()**2)
            return self.p_dict['y'] + term2
        except:
            term2 = self.p_dict['q']**2 / \
                    (2.0 * self.p_dict['g'] * self.p_dict['y']**2)
            return self.p_dict['y'] + term2
    def dh(self):
        try:
            return self.p_dict['y']
        except:
            area = self.area()
            width = self.width()
            dh = area / width
            return dh
            

class trap(prism):
    def __init__(self,p_dict):
        self.p_dict = p_dict
    def area(self):
        return self.p_dict['y'] * (self.p_dict['b'] + \
               (self.p_dict['m'] * self.p_dict['y']))

    def width(self):
        return self.p_dict['b'] + \
               (2.0 * self.p_dict['m'] * self.p_dict['y'])
    
    def p(self):
        p = self.p_dict['b'] + (2.0 * self.p_dict['y'] * \
           (1.0 + self.p_dict['m']**2)**0.5)
        return p
    
    def m(self):
        term1 = (self.p_dict['b'] * self.p_dict['y']**2)/2.0
        term2 = (self.p_dict['m'] * self.p_dict['y']**3)/3.0
        term3 = self.p_dict['Q']**2 / (self.p_dict['g']*self.p_dict['y'] * \
                (self.p_dict['b']+(self.p_dict['m']*self.p_dict['y'])))
        m = term1 + term2 + term3
        return m    
    
                        