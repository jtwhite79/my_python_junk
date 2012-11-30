from mbase import package

class mfgmg(package):
    '''Pcg package
    Only programmed to work with the default values; may need work for other options'''
    def __init__(self, model, mxiter=50, iiter=30, iadamp=0, \
                 hclose=1e-5, rclose=1e-5, relax=1.0, ioutgmg=0, \
                 ism=0, isc=0, damp=1.0,dup=0.75,dlow=0.01,\
                 chglimit=1.0,extension='gmg', unitnumber=27):
        package.__init__(self, model, extension, 'GMG', unitnumber) # Call ancestor's init to set self.parent, extension, name and unit number
        self.heading = '# GMG for MODFLOW, generated by Flopy.'
        self.url = 'gmg.htm'
        self.mxiter = mxiter
        self.iiter = iiter
        self.iadamp = iadamp
        self.hclose = hclose
        self.rclose = rclose
        self.relax = relax
        self.ism = ism
        self.isc = isc
        self.dup = dup
        self.dlow = dlow
        self.chglimit = chglimit
        self.damp = damp
        self.ioutgmg = ioutgmg
        self.iunitmhc = 0
        self.parent.add_package(self)
    def __repr__( self ):
        return 'Geometric multigrid package class'
    def write_file(self):
        # Open file for writing
        f_gmg = open(self.fn_path, 'w')
        f_gmg.write('%s\n' % self.heading)        
        #--ds0
        f_gmg.write('{0:9.3e} {1:9d} {2:9.3e} {3:9d}\n'\
             .format(self.rclose,self.iiter,self.hclose,self.mxiter))        
        #--ds1
        f_gmg.write('{0:9.3e} {1:9d} {2:9d} {3:9d}\n'\
             .format(self.damp,self.iadamp,self.ioutgmg,self.iunitmhc))
        #--ds2
        f_gmg.write('{0:9d} {1:9d} {2:9.3e} {3:9.3e} {4:9.3e}\n'\
             .format(self.ism,self.isc,self.dup,self.dlow,self.chglimit))
        #--ds3
        f_gmg.write('{0:10.3e}\n'.format(self.relax))
        f_gmg.close()

