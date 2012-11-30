from numpy import empty
from mbase import package

class mtdsp(package):
    'Dispersion package class\n'
    def __init__(self, model, al=0.01, trpt=0.1, trpv=0.01, dmcoef=1e-9, extension='dsp',multiDiff=False):
        '''
        if dmcoef is passed as a list of (nrow,ncol,nlay) arrays,
        then the multicomponent diffusion is activated
        '''
        package.__init__(self, model, extension, 'DSP', 33) # Call ancestor's init to set self.parent, extension, name and unit number
        nrow, ncol, nlay, nper = self.parent.mf.nrow_ncol_nlay_nper
        ncomp = self.parent.get_ncomp()        
        if multiDiff:
            assert isinstance(dmcoef,list),'using multicomponent diffusion requires dmcoef is list of length ncomp'
            if len(dmcoef) != ncomp:
                raise TypeError,'using multicomponent diffusion requires dmcoef is list of length ncomp'
        self.multiDiff = multiDiff                                    
        # First create arrays so that they have the correct size
        self.al = empty((nrow, ncol, nlay))
        self.trpt = empty((nlay))
        self.trpv = empty((nlay))
        if self.multiDiff:
            self.dmcoef = []
            for c in range(ncomp):
                self.dmcoef.append(empty((nrow,ncol,nlay)))
        else:
            self.dmcoef = empty((nlay))
        # Set values of all parameters
        self.al = self.assignarray( self.al, al,load=model.load )  
        self.trpt = self.assignarray( self.trpt, trpt,load=model.load )
        self.trpv = self.assignarray( self.trpv, trpv,load=model.load )
        if self.multiDiff:
            for c in range(ncomp):
                self.dmcoef[c] = self.assignarray( self.dmcoef[c], dmcoef[c],load=model.load )    
        else:
            self.dmcoef = self.assignarray( self.dmcoef, dmcoef,load=model.load )
        self.parent.add_package(self)
    def write_file(self):
        nrow, ncol, nlay, nper = self.parent.mf.nrow_ncol_nlay_nper
        # Open file for writing
        f_dsp = open(self.fn_path, 'w')
        if self.multiDiff:
            f_dsp.write('$ MultiDiffusion\n')
        self.parent.write_array( f_dsp, self.al, self.unit_number[0], True, 13, ncol, 'Longitudinal dispersivity for Layer',ext_base='al')
        self.parent.write_array( f_dsp, self.trpt, self.unit_number[0], True, 13, nlay, 'TRPT=(horizontal transverse dispersivity) / (Longitudinal dispersivity)')
        self.parent.write_array( f_dsp, self.trpv, self.unit_number[0], True, 13, nlay, 'TRPV=(vertical transverse dispersivity) / (Longitudinal dispersivity)')
        if self.multiDiff:
            for i,c in enumerate(self.dmcoef):
                #print c.shape
                self.parent.write_array( f_dsp,c, self.unit_number[0], True, 13, ncol, 'Effective dmcoef for comp '+str(i+1),ext_base='dmcoef')
        else:
            self.parent.write_array( f_dsp, self.dmcoef, self.unit_number[0], True, 13, nlay, 'Effective molecular diffusion coefficient')
        f_dsp.close()

