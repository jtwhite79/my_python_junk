from datetime import datetime
import numpy as np


def load_ascii_list(filename,dtype):    

    arr = np.genfromtxt(filename,dtype=dtype,comments='|')           
    return arr

def load_bin_list(filename,dtype):    
    arr = np.fromfile(filename,dtype=dtype)       
    return arr        




class point_property():
    def __init__(self,lay,row,col,names,data_dict,index):
        '''data should be a dict of keyed on data type and valued with ndarrays
        '''
        self.lay = int(lay)
        self.row = int(row)
        self.col = int(col)
        self.ifmt = '{0:10d}'
        self.ffmt = '{0:10.2G}'
        self.sfmt = '{0:<20s}'
        self.names = names
        self.data_dict = data_dict        
        self.index = index        
        
    def __getattr__(self,name):
        try:
            return getattr(self,name)
        except:
            try:
                return self.data_dict[name]
            except:
                raise AttributeError('point_property instance does not have attribute '+str(name))

    
    def string(self,k):
        s = ''
        s += self.ifmt.format(self.lay)        
        s += self.ifmt.format(self.row)
        s += self.ifmt.format(self.col)
        s += self.ifmt.format(self.lay)
        i = self.index.index(k)
        for key in self.names:
            s += self.ffmt.format(self.data_dict[key][i])
    
        


class ghb_list():
    def __init__(self):
        self.points = []
        self.dtype = np.dtype([('layer','i4'),('row','i4'),('column','i4'),\
            ('stage','f4'),('conductance','f4'),('aux','a20')])

    def string_list(self,k):
        s = ''
        for p in points:


                        




        



