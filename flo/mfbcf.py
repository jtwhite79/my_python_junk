import numpy as np
from mbase import package

class mfbcf(package):
    '''Block centered flow package class\n
    tran is used when laycon = 0 or 2, hy is otherwise'''
    def __init__(self, model, ibcfcb = 0, intercellt=0,laycon=3, trpy=1.0, hdry=-1E+30, iwdflg=0, wetfct=0.1, iwetit=1, ihdwet=0, \
                 tran=1.0, hy=1.0, vcont=1.0, sf1=1e-5, sf2=0.15, wetdry=-0.01, extension='bcf', unitnumber=15):
        package.__init__(self, model, extension, 'BCF6', unitnumber) # Call ancestor's init to set self.parent, extension, name and unit number
        self.url = 'bcf.htm'
        nrow, ncol, nlay, nper = self.parent.nrow_ncol_nlay_nper
        # First create arrays so that they have the correct size
        self.intercellt = np.empty(nlay, dtype='int32') # Specifies how to compute intercell conductance
        self.laycon = np.empty(nlay, dtype='int32') # Specifies the layer type (LAYCON) 
        self.trpy = np.ones(nlay) # Horizontal anisotropy factor for each layer
        # Set values of all parameters
        self.assignarray( self.intercellt, intercellt )
        self.assignarray( self.laycon, laycon )
        self.assignarray( self.trpy, trpy )
        self.ibcfcb = ibcfcb # Unit number for file with cell-by-cell flow terms
        self.hdry = hdry # Head in cells that are converted to dry during a simulation
        self.iwdflg = iwdflg # Flag that determines if the wetting capability is active
        self.wetfct = wetfct # Factor that is included in the calculation of the head when a cell is converted from dry to wet
        self.iwetit = iwetit # Iteration interval for attempting to wet cells
        self.ihdwet = ihdwet # Flag that determines which equation is used to define the initial head at cells that become wet
        self.tran = np.empty((nrow, ncol, nlay))
        self.hy = np.empty((nrow, ncol, nlay))
        self.vcont = np.empty((nrow, ncol, nlay - 1))
        self.sf1 = np.empty((nrow, ncol, nlay))
        self.sf2 = np.empty((nrow, ncol, nlay))
        self.wetdry = np.empty((nrow, ncol, nlay))
        self.tran = self.assignarray( self.tran, tran,load=True)
        self.hy = self.assignarray( self.hy, hy, load=True )
        self.vcont = self.assignarray( self.vcont, vcont,load=True )
        self.sf1 = self.assignarray( self.sf1, sf1, load=True )
        self.sf2 = self.assignarray( self.sf2, sf2,load=True )
        self.wetdry = self.assignarray( self.wetdry, wetdry,load=True )
        self.parent.add_package(self)
    def write_file(self):
        nrow, ncol, nlay, nper = self.parent.nrow_ncol_nlay_nper
        # Open file for writing
        f_bcf = open(self.fn_path, 'w')
        # Item 0: IBCFCB, HDRY, IWDFLG, WETFCT, IWETIT, IHDWET
        f_bcf.write('%10d%10.1e%10d%10f%10d%10d\n' % (self.ibcfcb, self.hdry, self.iwdflg, self.wetfct, self.iwetit, self.ihdwet))
        # LAYCON array
        for i in range(nlay):
            f_bcf.write('%1i%1i ' %(self.intercellt[i],self.laycon[i]))
        f_bcf.write('\n')
        #self.parent.write_array(f_bcf, self.laycon, self.unit_number[0], False, 2, -40)
        # TRPY array
        self.parent.write_array(f_bcf, self.trpy, self.unit_number[0], True, 13, -5, 'TRPY(): Anisotropy factor of layers')
        transient = not self.parent.get_package('DIS').steady.all()
        for i in range(nlay):
            if (transient == True):
                comment = 'Sf1() = Confined storage coefficient of layer ' + str(i + 1)
                self.parent.write_array( f_bcf, self.sf1[:,:,i], self.unit_number[0], True, 13, ncol, comment,ext_base='sf1' )
            if ((self.laycon[i] == 0) or (self.laycon[i] == 2)):
                comment = 'TRANS() = Transmissivity of layer ' + str(i + 1)
                self.parent.write_array( f_bcf, self.tran[:,:,i], self.unit_number[0], True, 13, ncol, comment,ext_base='tran' )
            else:
                comment = 'HY() = Hydr. Conductivity of layer ' + str(i + 1)
                self.parent.write_array( f_bcf, self.hy[:,:,i], self.unit_number[0], True, 13, ncol, comment,ext_base='hy')
            if i < nlay - 1:
                comment = 'VCONT() = Vert. leakance of layer ' + str(i + 1)
                self.parent.write_array( f_bcf, self.vcont[:,:,i], self.unit_number[0], True, 13, ncol, comment,ext_base='vcont' )
            if ((transient == True) and ((self.laycon[i] == 2) or (self.laycon[i] == 3))):
                comment = 'Sf2() = Specific yield of layer ' + str(i + 1)
                self.parent.write_array( f_bcf, self.sf2[:,:,i], self.unit_number[0], True, 13, ncol, comment,ext_base='sf2' )
            if ((self.iwdflg <> 0) and ((self.laycon[i] == 1) or (self.laycon[i] == 3))):
                comment = 'Wetdry() = Wetdry array of layer ' + str(i + 1)
                self.parent.write_array( f_bcf, self.wetdry[:,:,i], self.unit_number[0], True, 13, ncol, comment,ext_base='wetdry' )
        f_bcf.close()

