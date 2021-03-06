import numpy as np
from flopy2.mbase import Package

class ModflowUpw(Package):
    'Upstream weighting package class\n'
    def __init__(self, model, laytyp=0, layavg=0, chani=1.0, layvka=0, laywet=0, iupwcb = 53, hdry=-1E+30, iphdry = 0,\
                 hk=1.0, hani=1.0, vka=1.0, ss=1e-5, sy=0.15, vkcb=0.0, wetdry=-0.01, storagecoefficient=False, constantcv=False,        \
                 extension='upw', unitnumber = 31):
        Package.__init__(self, model, extension, 'UPW', unitnumber) # Call ancestor's init to set self.parent, extension, name and unit number
        self.heading = '# UPW for MODFLOW-NWT, generated by Flopy.'
        self.url = 'upw_upstream_weighting_package.htm'
        nrow, ncol, nlay, nper = self.parent.nrow_ncol_nlay_nper
        # item 1
        self.iupwcb = iupwcb # Unit number for file with cell-by-cell flow terms
        self.hdry = hdry # Head in cells that are converted to dry during a simulation
        self.npupw = 0 # number of LPF parameters
        self.iphdry = iphdry
        # First create arrays so that they have the correct size
        self.laytyp = np.empty(nlay, dtype='int32') # Specifies both the layer type (LAYCON) and the method of computing interblock conductance
        self.layavg = np.ones(nlay, dtype='int32') # Interblock transmissivity flag for each layer
        self.chani = np.ones(nlay) # Horizontal anisotropy flag for each layer
        self.layvka = np.ones(nlay, dtype='int32') # vertical hydraulic conductivity flag for each layer
        self.laywet = np.ones(nlay, dtype='int32') # wet dry flag for each layer
        #self.laycbd = np.ones(nlay, dtype='int32') # confining bed flag for each layer
        # Set values of all parameters
        self.assignarray_old( self.laytyp, laytyp )
        self.assignarray_old( self.layavg, layavg )
        self.assignarray_old( self.chani, chani )
        self.assignarray_old( self.layvka, layvka )
        self.assignarray_old( self.laywet, laywet )
        self.hk = np.empty((nrow, ncol, nlay))
        self.hani = np.empty((nrow, ncol, nlay))
        self.vka = np.empty((nrow, ncol, nlay))
        self.ss = np.empty((nrow, ncol, nlay))
        self.sy = np.empty((nrow, ncol, nlay))
        self.vkcb = np.empty((nrow, ncol, nlay))
        self.assignarray_old( self.hk, hk )
        self.assignarray_old( self.hani, hani )
        self.assignarray_old( self.vka, vka )
        self.assignarray_old( self.ss, ss )
        self.assignarray_old( self.sy, sy )
        self.assignarray_old( self.vkcb, vkcb )
        self.parent.add_package(self)
    def write_file(self):
        nrow, ncol, nlay, nper = self.parent.nrow_ncol_nlay_nper
        # Open file for writing
        f_upw = open(self.fn_path, 'w')
        # Item 0: text
        f_upw.write('%s\n' % self.heading)
        # Item 1
        f_upw.write('%10d%10.1e%10d%10d\n' % (self.iupwcb, self.hdry, self.npupw, self.iphdry))
        # LAYTYP array
        self.parent.write_array_old(f_upw, self.laytyp, self.unit_number[0], False, 2, -40, 'LAYTYP(): Layer type of layers')
        # LAYAVG array
        self.parent.write_array_old(f_upw, self.layavg, self.unit_number[0], False, 2, -40, 'LAYAVG(): Layer average of layers')
        # CHANI array
        self.parent.write_array_old(f_upw, self.chani, self.unit_number[0], False, 2, -40, 'CHANI(): Horizontal anisotropy flag of layers')
        # LAYVKA array
        self.parent.write_array_old(f_upw, self.layvka, self.unit_number[0], False, 2, -40, 'LAYVKA(): Vertical hydraulic conductivity flag of layers')
        # LAYWET array
        self.parent.write_array_old(f_upw, self.laywet, self.unit_number[0], False, 2, -40, 'LAYWET(): Wet-Dry flag of layers')
        transient = not self.parent.get_package('DIS').steady.all()
        for i in range(nlay):
        	comment = 'HK() = Horizontal hydraulic conductivity of layer ' + str(i + 1)
        	self.parent.write_array_old( f_upw, self.hk[:,:,i], self.unit_number[0], True, 13, ncol, comment )
        	if self.chani[i] < 1:
	        	comment = 'HANI() = Ratio of horizontal hydraulic of columns to rows of layer ' + str(i + 1)
	        	self.parent.write_array_old( f_upw, self.hani[:,:,i], self.unit_number[0], True, 13, ncol, comment )
        	comment = 'VKA() = Vertical hydraulic conductivity of layer ' + str(i + 1)
        	self.parent.write_array_old( f_upw, self.vka[:,:,i], self.unit_number[0], True, 13, ncol, comment )
        	if transient == True:
        		comment = 'Ss() = Specific storage coefficient of layer ' + str(i + 1)
        		self.parent.write_array_old( f_upw, self.ss[:,:,i], self.unit_number[0], True, 13, ncol, comment )
        		if self.laytyp[i] !=0:
        			comment = 'Sy() = Specific yield of layer ' + str(i + 1)
        			self.parent.write_array_old( f_upw, self.sy[:,:,i], self.unit_number[0], True, 13, ncol, comment )
        	if self.parent.get_package('DIS').laycbd[i] > 0:
        		comment = 'VKCB() = Vertical hydraulic conductivity of quasi-three-dimensional confining bed of layer ' + str(i + 1)
        		self.parent.write_array_old( f_upw, self.vkcb[:,:,i], self.unit_number[0], True, 13, ncol, comment )
        f_upw.close()

