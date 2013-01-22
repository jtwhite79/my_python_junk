import numpy as np
from flopy2.mbase import Package

class Mt3dDsp(Package):
    '''
    Dispersion package class\n
    '''
    def __init__(self, model, al=0.01, trpt=0.1, trpv=0.01, dmcoef=1e-9, 
                 extension='dsp', multiDiff=False):
        '''
        if dmcoef is passed as a list of (nlay, nrow, ncol) arrays,
        then the multicomponent diffusion is activated
        '''
        # Call ancestor's init to set self.parent, extension, name and 
        #unit number
        Package.__init__(self, model, extension, 'DSP', 33) 
        nrow, ncol, nlay, nper = self.parent.mf.nrow_ncol_nlay_nper
        ncomp = self.parent.get_ncomp()        
        if multiDiff:
            assert isinstance(dmcoef,list),('using multicomponent diffusion '
                                            'requires dmcoef is list of '
                                            'length ncomp')
            if len(dmcoef) != ncomp:
                raise TypeError,('using multicomponent diffusion requires '
                                 'dmcoef is list of length ncomp')
        self.multiDiff = multiDiff                                    
        self.al = self.assignarray((nlay, nrow, ncol), np.float, al, 
                                   name='al', load=model.load )
        self.trpt = self.assignarray((nlay,), np.float, trpt, name='trpt', 
                                     load=model.load)
        self.trpv = self.assignarray((nlay,), np.float, trpv, name='trpv', 
                                     load=model.load)
        if self.multiDiff:
            self.dmcoef = []
            for c in range(ncomp):
                self.dmcoef.append(self.assignarray( (nlay, nrow, ncol), 
                                   np.float, dmcoef[c], 
                                   name='dmcoef_sp_'+str(c), load=model.load))
        else:
            self.dmcoef = self.assignarray((nlay,), np.float, dmcoef,
                                           name='dmcoef', load=model.load)
        self.parent.add_package(self)
        return

    def write_file(self):
        nrow, ncol, nlay, nper = self.parent.mf.nrow_ncol_nlay_nper
        # Open file for writing
        f_dsp = open(self.fn_path, 'w')
        if self.multiDiff:
            f_dsp.write('$ MultiDiffusion\n')
        self.parent.write_array(f_dsp, self.al, self.unit_number[0], True, 13,
                                ncol, 'Longitudinal dispersivity for Layer',
                                ext_base='al')
        self.parent.write_vector(f_dsp, self.trpt, self.unit_number[0], True, 
                                 13, nlay, 
                                 ('TRPT=(horizontal transverse dispersivity) /'
                                 ' (Longitudinal dispersivity)'))
        self.parent.write_vector(f_dsp, self.trpv, self.unit_number[0], True, 
                                 13, nlay, 
                                 ('TRPV=(vertical transverse dispersivity) / '
                                 '(Longitudinal dispersivity)'))
        if self.multiDiff:
            for i,c in enumerate(self.dmcoef):
                self.parent.write_array(f_dsp, c, self.unit_number[0], True, 
                                        13, ncol, 'Effective dmcoef for comp '+
                                        str(i+1)+' and for Layer ', 
                                        ext_base='dmcoef')
        else:
            self.parent.write_vector(f_dsp, self.dmcoef, self.unit_number[0], 
                                     True, 13, nlay, ('Effective molecular '
                                     'diffusion coefficient'))
        f_dsp.close()
        return
