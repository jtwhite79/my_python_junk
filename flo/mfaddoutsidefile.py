from numpy import atleast_2d
from mbase import package

class mfaddoutsidefile(package):
    '''Add a file for which you have a MODFLOW input file'''
    def __init__(self, model, name, extension, unitnumber):
        package.__init__(self, model, extension, name, unitnumber) # Call ancestor's init to set self.parent, extension, name and unit number          
        self.parent.add_package(self)
    def __repr__( self ):
        return 'Outside package class'
    def write_file(self):
        pass
                
