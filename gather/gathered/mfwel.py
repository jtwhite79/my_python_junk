from numpy import atleast_2d
from flopy2.mbase import Package

class ModflowWel(Package):
    '''Well Package class
    No parameters implemented'''
    def __init__(self, model, iwelcb=0, layer_row_column_Q=None, extension ='wel', unitnumber=20):
        Package.__init__(self, model, extension, 'WEL', unitnumber) # Call ancestor's init to set self.parent, extension, name and unit number
        self.heading = '# Well file for MODFLOW, generated by Flopy.'
        self.url = 'wel.htm'
        self.iwelcb = iwelcb # no cell by cell terms are written
        self.mxactw = 0
        self.mxactw, self.layer_row_column_Q = self.assign_layer_row_column_data(layer_row_column_Q, 4)
        self.np = 0
        self.parent.add_package(self)
    def __repr__( self ):
        return 'Well package class'
    def ncells( self):
        # Returns the  maximum number of cells that have a well (developped for MT3DMS SSM package)
        return self.mxactw
    def write_file(self):
        f_wel = open(self.fn_path, 'w')
        f_wel.write('%s\n' % self.heading)
        f_wel.write('%10i%10i\n' % (self.mxactw, self.iwelcb))
        self.write_layer_row_column_data(f_wel, self.layer_row_column_Q)
        f_wel.close()

