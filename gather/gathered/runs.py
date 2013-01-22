#Simple runstest
#Jeremy White - TSA - Fall 2010

import math
import numpy as np

def runstest(vec,**kwargs):
    #--define
    n1,n2,runs = 0,0,1
    splits = 0
    
    
    #-- try to get kwarg for split value
    try:
        splt = kwargs['splt']
    except:
        splt = None
        
    
    length = np.shape(vec)[0]
    #--if a split value was found, use above/below
    if splt != None:
    
        
        
        #--check first position
        if vec[0] > splt: n1 += 1
        elif vec[0] < splt: n2 += 1
        
        for i in range(1,length):
            if vec[i] > splt: 
                #print 'n1'
                n1 += 1
            elif vec[i] < splt:
                #print 'n2'
                n2 += 1
            elif vec[i] == splt: 
                splits += 1
                #print 'split value'
            if vec[i] != vec[i-1]:
                runs += 1
                #print 'new run'
    
    #--if no split value use binary 
    else:
        
        #get unique vals
        vals = np.unique(vec)
        assert np.shape(vals)[0] == 2
        
        #--check first position
        if vec[0] == vals[0]: n1 += 1
        elif vec[0] == vals[1]: n2 += 1
        
        for i in range(1,length):
            print i
            if vec[i] == vals[0]: n1 += 1
            elif vec[i] == vals[1]: n2 += 1
            if vec[i] != vec[i-1]: runs += 1
    
    
    print 'Totals:n1,n2,runs,splits:',n1,n2,runs,splits
    runs_exp = float(1.0 + ((2*n1*n2)/(n1+n2)))
    #runs_exp = float(((2*n1*n2)/(n1+n2+1.0)))
    nterm1 = float(2*n1*n2)
    nterm2 = float(nterm1-n1-n2)
    dterm1 = float((n1+n2)*(n1+n2))
    dterm2 = float(n1+n2-1) 
    print nterm1,nterm2,dterm1,dterm2
    exp_var = (nterm1*nterm2)/(dterm1*dterm2)
    Z_score = (float(runs)-runs_exp)/math.sqrt(exp_var)
    print 'E(runs), Var(E(runs)):',runs_exp,exp_var
    
    return(Z_score)
    
   
            
        
        
        
        