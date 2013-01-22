import numpy as np
from flopy2.mbase import Package
from flopy2.utils import util_3d

class ModflowBas(Package):
    'Basic package class\n'
    def __init__(self, model, ibound=1, strt=1.0, ixsec=False, ichflg=False, hnoflo=-999.99, extension='bas', unitnumber=13):
        Package.__init__(self, model, extension, 'BAS6', unitnumber) # Call ancestor's init to set self.parent, extension, name and unit number
        self.url = 'bas6.htm'
        nrow, ncol, nlay, nper = self.parent.nrow_ncol_nlay_nper
        # First create arrays so that they have the correct size
        self.__ibound = np.empty((nrow, ncol, nlay), dtype='int32') # IBOUND array
        self.strt = np.empty((nrow, ncol, nlay)) # Starting heads
        # Set values of all parameters
        
        #self.__ibound = self.assignarray((nlay,nrow,ncol), np.int, ibound, name='ibound', load=True)
        self.__ibound = util_3d(model,(nlay,nrow,ncol),np.int,ibound,name='ibound',locat=self.unit_number[0])
        #self.strt = self.assignarray((nlay,nrow,ncol), np.float, strt, name='strt', load=model.load)
        self.strt = util_3d(model,(nlay,nrow,ncol),np.float32,strt,name='strt',locat=self.unit_number[0])
        self.heading = '# Basic package file for MODFLOW, generated by Flopy.'
        self.options = '' # Can be either or a combination of XSECTION, CHTOCH or FREE
        self.ixsec = ixsec # Flag for use of cross-section option
        self.ichflg = ichflg # Flag for calculation of flow between constant head cells
        self.ifrefm = True # Free format specifier is set to True, as other packages depend on that
        self.hnoflo = hnoflo # Head in no-flow cells
        self.parent.add_package(self)
    def getibound(self):
        return self.__ibound
    def setibound(self, value):
         self.__ibound = util_3d(model,(nlay,nrow,ncol),np.int,ibound,name='ibound',locat=self.unit_number[0])
    ibound = property(getibound, setibound)
    def write_file(self):
        # Open file for writing
        f_bas = open(self.fn_path, 'w')
        # First line: heading
        #f_bas.write('%s\n' % self.heading)
        f_bas.write('{0:s}\n'.format(self.heading))
        # Second line: format specifier
        self.options = ''
        if (self.ixsec):
            self.options = self.options + 'XSECTION'
        if (self.ichflg):
            self.options = self.options + ' CHTOCH'
        if (self.ifrefm):
            self.options = self.options + ' FREE'
        #f_bas.write('%s\n' % self.options)
        f_bas.write('{0:s}\n'.format(self.options))
        # IBOUND array
        #self.parent.write_array(f_bas, self.ibound, self.unit_number[0], True, 4, -5, 'IBOUND Array for Layer',ext_base='ibound')
        f_bas.write(self.__ibound.get_file_entry())
        # Head in inactive cells
        #f_bas.write('%f\n' % self.hnoflo)
        f_bas.write('{0:15.6G}\n'.format(self.hnoflo))
        # Starting heads array
        #self.parent.write_array(f_bas, self.strt, self.unit_number[0], True, 13, 5, 'Starting Heads in Layer',ext_base='strt')
        f_bas.write(self.strt.get_file_entry())
        # Close file
        f_bas.close()

