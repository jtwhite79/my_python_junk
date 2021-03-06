import numpy as np
from flopy2.mbase import Package
from flopy2.utils import util_2d,util_3d

class ModflowDis(Package):
    '''Discretization package class
    Input:
    model: modflow object to which package is added, created with Modflow( nlay, nrow, ncol, nper=1 )
    delr: column widths, scalar or array of length ncol
    delc: row widths, scalar or array of length nrow
    laycbd: flag that indicates if confining unit is present below layer, length nlay
    top: elevation of top of first layer, scalar or array of nrow,ncol
    botm: elevations of bottoms of layers, array of length nlay, or array of (nlay,nrow,ncol)
    steady=[True]: boolean indicating whether simulation of stress period is steady, scalar or array of length nper
    perlen=[1]: lengths of stress periods, scalar or array of length nper
    nstp=[1]: number of steps per stress period, scalar or array of length nper
    tsmult=[1]: time step multiplier, scalar or array of length nper
    itmuni: time units, default days (= 4)
    lenuni: length units, default meters (= 2)
    fname: filename between quotes
    '''
    def __init__(self, model, nlay=1, nrow=2, ncol=2, nper=1, delr=1.0, delc=1.0, laycbd=1, top=1, botm=0, perlen=1, nstp=1, tsmult=1, steady=True, itmuni=4, lenuni=2, extension='dis', unitnumber=11):
        Package.__init__(self, model, extension, 'DIS', unitnumber) # Call ancestor's init to set self.parent, extension, name and unit number
        self.url = 'dis.htm'
        self.nrow = nrow
        self.ncol = ncol
        self.nlay = nlay
        self.nper = nper
        
        # Set values of all parameters
        self.heading = '# Discretization file for MODFLOW, generated by Flopy.'
        #self.laycbd = self.assignarray((self.nlay,), np.int, laycbd, name='laycbd')
        self.laycbd = util_2d(model,(self.nlay,),np.int,laycbd,name='laycbd')
        self.laycbd[-1] = 0 # bottom layer must be zero
        self.delr = util_2d(model,(self.ncol,),np.float32,delr,name='delr',locat=self.unit_number[0])
        self.delc = util_2d(model,(self.nrow,),np.float32,delc,name='delc',locat=self.unit_number[0])  
        self.top = util_2d(model,(self.nrow,self.ncol),np.float32,top,name='model_top',locat=self.unit_number[0])
        self.botm = util_3d(model,(self.nlay+sum(self.laycbd),self.nrow,self.ncol),np.float32,botm,'botm',locat=self.unit_number[0])    
        #if (not self.checklayerthickness()):
        #    if self.parent.silent == 0: print 'Warning: Cells with zero-layer thickness encountered!'
        self.perlen = util_2d(model,(self.nper,),np.float32,perlen,name='perlen')
        self.nstp = util_2d(model,(self.nper,),np.int,nstp,name='nstp')
        self.tsmult = util_2d(model,(self.nper,),np.float32,tsmult,name='tsmult')
        self.steady = util_2d(model,(self.nper,),np.bool,steady,name='steady')
        self.itmuni = itmuni
        self.lenuni = lenuni
        self.parent.add_package(self)
    def checklayerthickness(self):
        return (self.thickness > 0).all()

    def get_cell_volumes(self):
        vol = np.empty((self.nlay, self.nrow, self.ncol))
        for l in range(self.nlay):
            vol[l,:, :] *= self.get_thickness()[l]
        for r in range(self.nrow):
            vol[:, r, :] *= self.delc[r]
        for c in range(self.ncol):
            vol[:, :, c] *= self.delr[c]
        return vol
    def get_node_coordinates(self):
        # In row direction
        y = np.empty((self.nrow))
        for r in range(self.nrow):
            if (r == 0):
                y[r] = self.delc[r] / 2.
            else:
                y[r] = y[r - 1] + self.delc[r]
        # In column direction
        x = np.empty((self.ncol))
        for c in range(self.ncol):
            if (c == 0):
                x[c] = self.delr[c] / 2.
            else:
                x[c] = x[c - 1] + self.delr[c]
        # In layer direction
        z = np.empty((self.nlay, self.nrow, self.ncol))
        for l in range(self.nlay):
            if (l == 0):
                z[l] = (self.top + self.botm[l]) / 2.
            else:
                z[l] = (self.botm[l - 1] + self.botm[l]) / 2.
        return y, x, z
    
    
    def read_from_cnf(self, cnf_file_name):
        try:
            f_cnf = open(cnf_file_name, 'r')

            # nlay, nrow, ncol
            line = f_cnf.readline()
            s = line.split()
            cnf_nlay = int(s[0])
            cnf_nrow = int(s[1])
            cnf_ncol = int(s[2])

            # ncol column widths delr[c]
            line = f_cnf.readline()
            cnf_delr = [float(s) for s in line.split()]

            # nrow row widths delc[r]
            line = f_cnf.readline()
            cnf_delc = [float(s) for s in line.split()]

            # nrow * ncol htop[r, c]
            line = f_cnf.readline()
            cnf_top = [float(s) for s in line.split()]
            cnf_top = np.reshape(cnf_top, (cnf_nrow, cnf_ncol))

            # nlay * nrow * ncol layer thickness dz[l, r, c]
            line = f_cnf.readline()
            cnf_dz = [float(s) for s in line.split()]
            cnf_dz = np.reshape(cnf_dz, (cnf_nlay, cnf_nrow, cnf_ncol))

            # cinact, cdry, not used here so commented
            '''line = f_cnf.readline()
            s = line.split()
            cinact = float(s[0])
            cdry = float(s[1])'''

            f_cnf.close()
        finally:
            self.nlay = cnf_nlay
            self.nrow = cnf_nrow
            self.ncol = cnf_ncol

            self.delr = np.empty( self.ncol )
            self.assignarray_old( self.delr, cnf_delr )

            self.delc = np.empty( self.nrow )
            self.assignarray_old( self.delc, cnf_delc )

            self.top = np.empty((self.nrow, self.ncol))
            self.assignarray_old( self.top, cnf_top)

            self.botm = np.empty((self.nrow, self.ncol, self.nlay + sum(self.laycbd) ))
            # First model layer
            self.botm[:, :, 0] = self.top - cnf_dz[0, :, :]
            # All other layers
            for l in range(1, self.nlay):
                self.botm[:, :, l] = self.botm[:, :, l - 1] - cnf_dz[l, :, :]
            self.update_thickness()
    @property
    def thickness(self):
        #self.__thickness = np.empty((self.botm.shape))
        # First model layer
        #self.__thickness[0] = self.top - self.botm[0]
        # All other layers
        #for l in range(1, self.nlay):
        #    self.__thickness[l] = self.botm[l-1] - self.botm[l]
        thk = []
        thk.append(self.top - self.botm[0])
        for k in range(1,self.nlay):
            thk.append(self.botm[k-1] - self.botm[k])
        self.__thickness = util_3d(self.parent,(self.nlay,self.nrow,self.ncol),np.float32,thk,name='thickness')
        return self.__thickness
    def write_file(self):
        # Open file for writing
        f_dis = open(self.fn_path, 'w')
        # Item 0: heading        
        f_dis.write('{0:s}\n'.format(self.heading))
        # Item 1: NLAY, NROW, NCOL, NPER, ITMUNI, LENUNI        
        f_dis.write('{0:10d}{1:10d}{2:10d}{3:10d}{4:10d}{5:10d}\n'\
            .format(self.nlay, self.nrow, self.ncol, self.nper, self.itmuni, self.lenuni))
        # Item 2: LAYCBD

        for l in range(0, self.nlay):            
            f_dis.write('{0:3d}'.format(self.laycbd[l]))
        f_dis.write('\n')
        # Item 3: DELR
        f_dis.write(self.delr.get_file_entry())
        # Item 4: DELC       
        f_dis.write(self.delc.get_file_entry())
        # Item 5: Top(NCOL, NROW)
        f_dis.write(self.top.get_file_entry())
        # Item 5: BOTM(NCOL, NROW)        
        f_dis.write(self.botm.get_file_entry())
        
        # Item 6: NPER, NSTP, TSMULT, Ss/tr
        for t in range(self.nper):           
            f_dis.write('{0:14f}{1:14d}{2:10f} '.format(self.perlen[t],self.nstp[t],self.tsmult[t]))
            if self.steady[t]:                
                f_dis.write(' {0:3s}\n'.format('SS'))
            else:                
                f_dis.write(' {0:3s}\n'.format('TR'))
        f_dis.close()


