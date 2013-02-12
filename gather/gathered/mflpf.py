import numpy as np
from flopy2.mbase import Package
from flopy2.utils import util_2d,util_3d

class ModflowLpf(Package):
    'Layer-property flow package class\n'
    def __init__(self, model, laytyp=0, layavg=0, chani=1.0, layvka=0, laywet=0, ilpfcb = 53, hdry=-1E+30, iwdflg=0, wetfct=0.1, iwetit=1, ihdwet=0, \
                 hk=1.0, hani=1.0, vka=1.0, ss=1e-5, sy=0.15, vkcb=0.0, wetdry=-0.01, storagecoefficient=False, constantcv=False,        \
                 thickstrt=False, nocvcorrection=False, novfc=False, extension='lpf', unitnumber=15):
        Package.__init__(self, model, extension, 'LPF', unitnumber) # Call ancestor's init to set self.parent, extension, name and unit number
        self.heading = '# LPF for MODFLOW, generated by Flopy.'
        self.url = 'lpf.htm'
        nrow, ncol, nlay, nper = self.parent.nrow_ncol_nlay_nper
        # item 1
        self.ilpfcb = ilpfcb # Unit number for file with cell-by-cell flow terms
        self.hdry = hdry # Head in cells that are converted to dry during a simulation
        self.nplpf = 0 # number of LPF parameters
        self.laytyp = util_2d(model,(nlay,),np.int,laytyp,name='laytyp')
        self.layavg = util_2d(model,(nlay,),np.int,layavg,name='layavg')
        self.chani = util_2d(model,(nlay,),np.int,chani,name='chani')
        self.layvka = util_2d(model,(nlay,),np.int,layvka,name='vka')
        self.laywet = util_2d(model,(nlay,),np.int,laywet,name='laywet')
        self.wetfct = wetfct # Factor that is included in the calculation of the head when a cell is converted from dry to wet
        self.iwetit = iwetit # Iteration interval for attempting to wet cells
        self.ihdwet = ihdwet # Flag that determines which equation is used to define the initial head at cells that become wet
        self.options = ' '
        if storagecoefficient: self.options = self.options + 'STORAGECOEFFICIENT '
        if constantcv: self.options = self.options + 'CONSTANTCV '
        if thickstrt: self.options = self.options + 'THICKSTRT '
        if nocvcorrection: self.options = self.options + 'NOCVCORRECTION '
        if novfc: self.options = self.options + 'NOVFC '
        self.hk = util_3d(model,(nlay,nrow,ncol),np.float32,hk,name='hk',locat=self.unit_number[0])
        self.hani = util_3d(model,(nlay,nrow,ncol),np.float32,hk,name='hani',locat=self.unit_number[0])
        self.vka = util_3d(model,(nlay,nrow,ncol),np.float32,hk,name='vka',locat=self.unit_number[0])
        self.ss = util_3d(model,(nlay,nrow,ncol),np.float32,ss,name='ss',locat=self.unit_number[0])
        self.sy = util_3d(model,(nlay,nrow,ncol),np.float32,sy,name='sy',locat=self.unit_number[0])
        self.vkcb = util_3d(model,(nlay,nrow,ncol),np.float32,vkcb,name='vkcb',locat=self.unit_number[0])
        self.wetdry = util_3d(model,(nlay,nrow,ncol),np.float32,wetdry,name='wetdry',locat=self.unit_number[0])
        self.parent.add_package(self)
    def write_file(self):
        nrow, ncol, nlay, nper = self.parent.nrow_ncol_nlay_nper
        # Open file for writing
        f_lpf = open(self.fn_path, 'w')
        # Item 0: text
        f_lpf.write('%s\n' % self.heading)
        # Item 1: IBCFCB, HDRY, NPLPF        
        f_lpf.write('{0:10d}{1:10.3G}{2:10d},{3:s}\n'.format(self.ilpfcb,self.hdry,self.nplpf,self.options))
        # LAYTYP array
        f_lpf.write(self.laytyp.string);
        # LAYAVG array
        f_lpf.write(self.layavg.string);
        # CHANI array
        f_lpf.write(self.chani.string);
        # LAYVKA array
        f_lpf.write(self.layvka.string)
        # LAYWET array
        f_lpf.write(self.laywet.string);
        # Item 7: WETFCT, IWETIT, IHDWET
        iwetdry = self.laywet.sum()
        if iwetdry > 0:            
            f_lpf.write('{0:10f}{1:10d}{2:10d}\n'.format(self.wetfct,self.iwetit,self.ihdwet))
        transient = not self.parent.get_package('DIS').steady.all()
        for k in range(nlay):           
            f_lpf.write(self.hk[k].get_file_entry())
            if self.chani[k] < 1:                
                f_lpf.write(self.hani[k].get_file_entry())            
            f_lpf.write(self.vka[k].get_file_entry())
            if transient == True:                
                f_lpf.write(self.ss[k].get_file_entry())
                if self.laytyp[k] !=0:                                        
                    f_lpf.write(self.sy[k].get_file_entry())
            if self.parent.get_package('DIS').laycbd[k] > 0:                
                f_lpf.write(self.vkcb[k].get_file_entry())
            if (self.laywet[k] != 0 and self.laytyp[k] != 0):               
                f_lpf.write(self.laywet[k].get_file_entry())
        f_lpf.close()