import numpy
import struct
from pylab import ma, flipud
import string
import math

#generic functions
def kij_from_icrl(icrl,nlay,nrow,ncol):
    'Convert the modflow node number to row, column, and layer.'
    nrc = nrow * ncol
    #k=int( icrl / nrow / ncol )+1
    #i=int( (icrl-(k-1)*nrow*ncol) / ncol )+1
    #j=icrl - (k-1)*nrow*ncol - (i-1)*ncol
    k  = int( icrl / nrc ) + 1
    ij = int( icrl - ( k - 1 ) * nrc )
    i = int( ij / ncol )
    if ( i * ncol ) < ij:
        i += 1
    j = ij - ( i - 1 ) * ncol
    return k,i,j

def icrl_from_kij(k,i,j,nlay,nrow,ncol):
    'Convert layer, row, and column to the modflow node number.'
    nrc = nrow * ncol
    icrl=int( ( ( k - 1 ) * nrc ) + ( ( i - 1 ) * ncol ) + j  )
    return icrl



def MFarray_to_plotarray(mfarray,maskvalue,orientation,rcl):
    '''Create a 2d plotting array from a 3d modflow array.
    mfarray: a 3d modflow array
    maskvalue: the value to mask (e.g. hdry)
    orientation: 'layer' 'row' or 'column'
    rcl: the layer row or column
    '''
    rcl=rcl-1
    nlay,nrow,ncol=shape(mfarray)
    if(orientation=='layer'):
        Z=flipud(mfarray[rcl,:,:]).copy()
    elif(orientation=='row'):
        Z=flipud(mfarray[:,rcl,:]).copy()
    elif(orientation=='column'):
        Z=flipud(mfarray[:,:,rcl]).copy()
    Z=ma.masked_where(Z == maskvalue,Z)
    return Z

class SWRReadBinaryStatements:
    integer = numpy.int32
    real = numpy.float64
    character = numpy.uint8
    integerbyte = 4
    realbyte = 8
    textbyte = 4
    def read_integer(self):
        intvalue=struct.unpack('i',self.file.read(1*SWRReadBinaryStatements.integerbyte))[0]
        return intvalue
    def read_real(self):
        realvalue=struct.unpack('d',self.file.read(1*SWRReadBinaryStatements.realbyte))[0]
        return realvalue
    def read_text(self):
        #textvalue=struct.unpack('cccccccccccccccc',self.file.read(16*self.textbyte))
        textvalue=numpy.fromfile(file = self.file, dtype=SWRReadBinaryStatements.character, count=16).tostring()
        return textvalue
    def read_record(self):
        x = numpy.fromfile(file=self.file,dtype=SWRReadBinaryStatements.real,count=self.nrecord*self.items)
        x.resize(self.nrecord,self.items)
        return x
    def read_items(self):
        x = numpy.fromfile(file=self.file,dtype=SWRReadBinaryStatements.real,count=self.items)
        return x


class MFReadBinaryStatements:
    'Class of methods for reading MODFLOW binary files'
    #--byte definition
    integer=numpy.int32
    real=numpy.float32
    character=numpy.uint8
    integerbyte=4
    realbyte=4
    textbyte=1
    def read_integer(self):
        intvalue=struct.unpack('i',self.file.read(1*MFReadBinaryStatements.integerbyte))[0]
        return intvalue
    def read_real(self):
        realvalue=struct.unpack('f',self.file.read(1*MFReadBinaryStatements.realbyte))[0]
        return realvalue
    def read_text(self):
        #textvalue=struct.unpack('cccccccccccccccc',self.file.read(16*self.textbyte))
        textvalue=numpy.fromfile(file = self.file, dtype=MFReadBinaryStatements.character, count=16).tostring()
        return textvalue
    def read_3drealarray(self):
        x=numpy.fromfile(file = self.file, dtype=MFReadBinaryStatements.real, count=self.nlay*self.nrow*self.ncol)
        x.shape=(self.nlay,self.nrow,self.ncol)
        return x
    def read_2drealarray(self):
        x=numpy.fromfile(file = self.file, dtype=MFReadBinaryStatements.real, count=self.nrow*self.ncol)
        x.shape=(self.nrow,self.ncol)
        return x
    def read_2dintegerarray(self):
        i=numpy.fromfile(file = self.file, dtype=MFReadBinaryStatements.integer, count=self.nrow*self.ncol)
        i.shape=(self.nrow,self.ncol)
        return i
    def read_1drealarray(self,i):
        x=numpy.fromfile(file = self.file, dtype=MFReadBinaryStatements.real, count=i)
        return x

class FVSWSReadBinaryStatements:
    'Class of methods for reading FVSWS binary files'
    #--byte definition
    integer=numpy.int32
    real=numpy.float32
    double=numpy.float64
    character=numpy.uint8
    integerbyte=4
    realbyte=4
    doublebyte=8
    textbyte=1
    def read_integer(self):
        intvalue=struct.unpack('i',self.file.read(1*FVSWSReadBinaryStatements.integerbyte))[0]
        return intvalue
    def read_real(self):
        realvalue=struct.unpack('f',self.file.read(1*FVSWSReadBinaryStatements.realbyte))[0]
        return realvalue
    def read_double(self):
        doublevalue=struct.unpack('d',self.file.read(1*FVSWSReadBinaryStatements.doublebyte))[0]
        return doublevalue
    def read_text(self):
        #textvalue=struct.unpack('cccccccccccccccc',self.file.read(16*self.textbyte))
        textvalue=numpy.fromfile(file = self.file, dtype=FVSWSReadBinaryStatements.character, count=16).tostring()
        return textvalue
    def read_3drealarray(self):
        x=numpy.fromfile(file = self.file, dtype=FVSWSReadBinaryStatements.real, count=self.nlay*self.nrow*self.ncol)
        x.shape=(self.nlay,self.nrow,self.ncol)
        return x
    def read_2drealarray(self):
        x=numpy.fromfile(file = self.file, dtype=FVSWSReadBinaryStatements.real, count=self.nrow*self.ncol)
        x.shape=(self.nrow,self.ncol)
        return x
    def read_2ddoublearray(self):
        x=numpy.fromfile(file = self.file, dtype=FVSWSReadBinaryStatements.double, count=self.nrow*self.ncol)
        x.shape=(self.nrow,self.ncol)
        return x
    def read_2dintegerarray(self):
        i=numpy.fromfile(file = self.file, dtype=FVSWSReadBinaryStatements.integer, count=self.nrow*self.ncol)
        i.shape=(self.nrow,self.ncol)
        return i
    def read_1drealarray(self,i):
        x=numpy.fromfile(file = self.file, dtype=FVSWSReadBinaryStatements.real, count=i)
        return x
    def read_1ddoublearray(self,i):
        x=numpy.fromfile(file = self.file, dtype=FVSWSReadBinaryStatements.double, count=i)
        return x
    def read_record(self):
        x = numpy.fromfile(file=self.file,dtype=FVSWSReadBinaryStatements.double,count=self.nrecord*self.items)
        #print x
        x.resize(self.nrecord,self.items)
        return x


class MF_Discretization:
    def assign_rowcollay(self,nlay,nrow,ncol):
        #initialize grid information
        self.nrow=nrow
        self.ncol=ncol
        self.nlay=nlay
    #def read_PESTGridSpecificationFile(filename):
    #def read_MFDiscretizationFile(filename)



class SWR_Record(SWRReadBinaryStatements):
    def __init__(self,type,filename):
        #--type = 0 = stage record
        #--type = -1 = reach group record
        #--type = -2 = reach group connection velocity record
        #-- type > 0 = aq-reach exchange record type = nlay
        self.file = open(filename,'rb')
#        self.nrecord = self.read_integer()
        self.type = int(type)
#        self.list = self.get_item_list()
        self.nrgout = 0
        if self.type == -2:
            self.nrgout = self.read_integer()
        self.nrecord = self.read_integer()
        self.items = self.get_num_items()
        #print self.nrecord,self.items
        self.null_record = numpy.zeros((self.nrecord,self.items)) + 1.0E+32
        #read connectivity for velocity data if necessary
        if self.type == -2:
            self.connectivity = self.read_connectivity()
            #print self.connectivity
    
    def read_connectivity(self):
        conn = numpy.zeros( (self.nrecord,3), numpy.int )
        icount = 0
        for nrg in range(0,self.nrgout):
            nconn = self.read_integer()
            for ic in range(0,nconn):
                conn[icount,0] = nrg
                conn[icount,1] = self.read_integer()
                conn[icount,2] = self.read_integer()
                icount += 1
        return conn
        
    def get_num_items(self):
        if self.type == 0   : return  1 #stage
        elif self.type == -1: return 14 #rchgrp budget
        elif self.type == -2: return  2 #reach group velocity
        elif self.type > 0  : return  8 #aq_ex
        else: return -1
    
    def get_header_items(self):
        return ['totim','dt','kper','kstp','swrstp','success_flag'] 

    def get_item_list(self):
        if self.type == 0:
            list = ['stage']
        if self.type == -1:
            list = ['stage','qsflow','qlatflow','quzflow','rain','evap',\
                            'qbflow','qeflow','qexflow','qbcflow','qcrflow','dv','inf-out','volume']
        if self.type == -2:
            list = ['flow','velocity']
        if self.type > 0:
            list = ['irch','ilay','bottom','stage','depth','head',\
                            'wetper','cond','headdiff','aq-rchflow']
        return list
         
    def get_temporal_list(self):
        list = ['totim','dt','kper','kstp','swrstp','success']
        return list

    def get_item_number(self,value):
        l = self.get_item_list()
        ioff = 6
        try:
            i = l.index(value.lower())
            i += ioff
#            print value, ' = item: ', i
        except ValueError:
            l = self.get_temporal_list()
            try:
                i = l.index(value.lower())
            except ValueError:
                i = -1  #-no match
                print 'no match to: ', value.lower()
        return i

    def read_header(self):
        try: 
            totim = self.read_real()
            dt = self.read_real()
            kper = self.read_integer()
            kstp = self.read_integer()
            swrstp = self.read_integer()
            return totim,dt,kper,kstp,swrstp,True
        except:
            return 0.0,0.0,0,0,0,False
    
    def get_record(self,*args):
        #--pass a tuple of timestep,stress period
        try:
            kkspt = int(args[0])
            kkper = int(args[1])
            while True:
                totim,dt,kper,kstp,swrstp,success,r = self.next()                
                if success == True:
                    if kkspt == kstp and kkper == kper:
                        print totim,dt,kper,kstp,swrstp,True
                        return totim,dt,kper,kstp,swrstp,True,r
                else:
                    return 0.0,0.0,0,0,0,False,self.null_record
        except:
            #--pass a scalar of target totim - 
            #--returns either a match or the first
            #--record that exceeds target totim
            try:               
                ttotim = float(args[0])
                while True:
                    #totim,dt,kper,kstp,swrstp,r,success = self.next()
                    totim,dt,kper,kstp,swrstp,success,r = self.next()                    
                    if success == True:                        
                        if ttotim <= totim:                    
                            return totim,dt,kper,kstp,swrstp,True,r                                                        
                    else:
                        return 0.0,0.0,0,0,0,False,self.null_record    
            except:
                #--get the last successful record
                previous = self.next()
                while True:
                    this_record = self.next()
                    if this_record[-2] == False:
                        print 'previous'
                        return previous
                    else: previous = this_record
    
    def get_gage(self,rec_num=0,iconn=0):    
        if self.type > 0:
            gage_record = numpy.zeros((self.items+8))#items plus 6 header values, reach number, and layer value
        else:
            gage_record = numpy.zeros((self.items+6))#items plus 6 header values
        while True:
            totim,dt,kper,kstp,swrstp,success,r = self.next()
            if success == True:
                #print totim,numpy.shape(r[rec_num-1])
                this_entry = numpy.array([totim,dt,kper,kstp,swrstp,success])
                #this_entry = numpy.hstack((this_entry,r[rec_num-1]))
                irec = rec_num - 1
                #find correct entry for record and layer
                if self.type > 0:
                    ifound = 0
                    ilen = numpy.shape(r)[0]
                    for i in range(0,ilen):
                        ir = int(r[i,0])
                        il = int(r[i,1])
                        if ir == rec_num and il == self.type:
                            ifound = 1
                            irec = i
                            break
                    if ifound < 1:
                        r[irec,:] = 0.0
                elif self.type == -2:
                    ifound = 0
                    for i in range(0,self.nrecord):
                        inode = self.connectivity[i,1]
                        ic    = self.connectivity[i,2]
                        if rec_num == inode and ic == iconn:
                            ifound = 1
                            irec = i
                            break
                    if ifound < 1:
                        r[irec,:] = 0.0
                    
                this_entry = numpy.hstack((this_entry,r[irec]))
                gage_record = numpy.vstack((gage_record,this_entry))

            else: 
                gage_record = numpy.delete(gage_record,0,axis=0) #delete the first 'zeros' element
                return gage_record
                     
    def next(self):
        totim,dt,kper,kstp,swrstp,success = self.read_header()        
        if success == False: 
#            print 'SWR_Stage.next() object reached end of file'
            return 0.0,0.0,0,0,0,False,self.null_record
        else:
            if self.type > 0:
                #r = numpy.zeros((self.items+1)) 
                r = numpy.zeros((self.items+2))                
                for rec in range(0,self.nrecord):
                    nlay = self.read_integer()                    
                    for lay in range(0,nlay):
                        this_lay = self.read_integer()
                        this_items = self.read_items()
                        this_r = numpy.insert(this_items,[0],this_lay)
                        this_r = numpy.insert(this_r,[0],rec+1)
                        #print totim,this_lay,numpy.shape(r),numpy.shape(this_r)
                        r = numpy.vstack((r,this_r))
                r = numpy.delete(r,0,axis=0)
                return totim,dt,kper,kstp,swrstp,True,r
            else:
                r = self.read_record()
#        print 'SWR data read for time step ',kstp,',stress period \
#                    ',kper,'and swr step ',swrstp
        return totim,dt,kper,kstp,swrstp,True,r

    
    
    
class MODFLOW_Head(MFReadBinaryStatements,MF_Discretization):
    'Reads binary head output from MODFLOW head file'
    def __init__(self,nlay,nrow,ncol,filename):
        #initialize grid information
        self.assign_rowcollay(nlay,nrow,ncol)
        self.h = numpy.zeros((self.nlay, self.nrow, self.ncol)) + 1.0E+32
        self.items = self.get_num_items()
        self.x0 = 0.0
        self.y0 = 0.0
        self.dx = 0.0
        self.dy = 0.0
        #open binary head file
        self.file=open(filename,'rb')

    def get_num_items(self):
        return 1 #heads

    def set_coordinates(self,x0,y0,dx,dy):
        self.x0 = x0
        self.y0 = y0
        self.dx = dx
        self.dy = dy
        #--set x and y coordinate for each row and column
        self.x = numpy.empty( (self.nrow+1,self.ncol+1) )
        self.y = numpy.empty( (self.nrow+1,self.ncol+1) )
        xt = numpy.zeros( self.ncol+1 )
        yt = numpy.zeros( self.nrow+1 )
        xt[0] = self.x0
        for j in range(1,self.ncol+1):
                xt[j] = xt[j-1] + self.dx
        yt[self.nrow] = self.y0
        for i in range(self.nrow-1,-1,-1):
                yt[i] = yt[i+1] + self.dy
                #print i, yt[i]
        for i in range(0,self.nrow+1):
                y = yt[i]
                for j in range(0,self.ncol+1):
                        x = xt[j]
                        self.x[i,j] = x
                        self.y[i,j] = y
        return 1
        
    def get_ijfromcoordinates(self,x,y):
        i = 0
        j = 0
        iexit = 0
        jexit = 0
        for ii in range(0,self.nrow):
                y1 = self.y[ii,0]
                y2 = self.y[ii+1,0]
                if y < y1 and y >= y2:
                        i = ii + 1
                        iexit = 1
                        for jj in range(0,self.ncol):
                                x1 = self.x[ii,jj]
                                x2 = self.x[ii,jj+1]
                                if x >= x1 and x < x2:
                                        j = jj + 1
                                        exit
                if iexit > 0:
                        exit

        return i,j 

    def get_nodefromrcl(self,row,col,lay):
        inode = icrl_from_kij(lay,row,col,self.nlay,self.nrow,self.ncol)
        return inode

    def read_header(self):
        try:
            kstp=self.read_integer()
            kper=self.read_integer()
            pertim=self.read_real()
            totim=self.read_real()
            text=self.read_text()
            ncol=self.read_integer()
            nrow=self.read_integer()
            ilay=self.read_integer()
#            print kstp,kper,ilay,nrow,ncol,pertim,totim,True
            return kstp,kper,pertim,totim,ncol,nrow,ilay,True
        except:
            return 0,0,0.,0.,0,0,0,False 
        
    def read_layerheads(self):
        hl = self.read_2drealarray()
        hl.shape=(self.nrow,self.ncol)
        return hl

    def __iter__(self):
        return self

    def next(self):
        for k in range(self.nlay):
            kstp,kper,pertim,totim,ncol,nrow,ilay,success=self.read_header()
            if(success):
                assert ncol==self.ncol, 'NCOL not consistent with binary heads file.'
                assert nrow==self.nrow, 'NROW not consistent with binary heads file.'
                assert ilay==k+1, 'Layers in head file are not sequential'
                self.h[ilay - 1, :, :] = self.read_layerheads()
            else:
                #print 'MODFLOW_Head object.next() reached end of file.'
                return 0.,0,0, numpy.zeros((self.nlay, self.nrow, self.ncol),\
                dtype='float')+1.0E+32,False
        self.KSTP=kstp
        self.KPER=kper
        self.PERTIM=pertim
        self.TOTIM=totim
#        print 'Heads read for time step ',kstp,' and stress period ',kper
        return totim,kstp,kper,self.h,True
     
    def get_record(self,*args):
        try:
            kkspt = args[0]
            kkper = args[1]
            while True:
                totim,kstp,kper,h,success = self.next()
                if success == True:
                    if kstp == kkspt and kkper == kper:
                        print totim,kstp,kper,True
                        return totim,kstp,kper,h,True
                else:
                    return 0.0,0,0,numpy.zeros((self.nlay,self.nrow,self,ncol),dtype='float')+1.0E+32,False 
        except:
            try:        
                target_totim = float(args[0])
                while True:
                    totim,kstp,kper,h,success = self.next()
                    if success:
                        if target_totim <= totim:
                            return totim,kstp,kper,h,True
                    else:
                        return 0.0,0,0,numpy.zeros((self.nlay,self.nrow,self.ncol),dtype='float')+1.0E+32,False
                
            except:
                #--get the last successful record
                previous = self.next()
                while True:
                    this_record = self.next()
                    if this_record[-1] == False:
                        return previous
                    else: previous = this_record
                                                
    #rec_num is modflow node number
    def get_gage(self,rec_num):    
        k, i, j = kij_from_icrl(rec_num,self.nlay,self.nrow,self.ncol)
        print 'node=', rec_num, 'row=', i, ' col=', j, 'lay=', k
        gage_record = numpy.zeros((self.items+1))#items plus tottime
        while True:
            totim,kstp,kper,h,success = self.next()
            if success == True:
                #print totim,numpy.shape(h[rec_num-1])
                this_entry = numpy.array([totim])
                this_entry = numpy.hstack((this_entry,h[k-1,i-1,j-1]))
                gage_record = numpy.vstack((gage_record,this_entry))
            else: 
                gage_record = numpy.delete(gage_record,0,axis=0) #delete the first 'zeros' element
                return gage_record


class MODFLOW_CBB(MFReadBinaryStatements,MF_Discretization):
    'Reads binary cell by cell output from MODFLOW cbb file'
    def __init__(self,nlay,nrow,ncol,filename):
        #initialize grid information
        self.assign_rowcollay(nlay,nrow,ncol)
        self.flux = numpy.empty((self.nlay, self.nrow, self.ncol))
        #open binary head file
        self.file=open(filename,'rb')
 
    def read_header(self):
        try:
            kstp=self.read_integer()
            kper=self.read_integer()
            text=self.read_text()
            ncol=self.read_integer()
            nrow=self.read_integer()
            nlay=self.read_integer()
            ubdsvtype=0;delt=0.;pertim=0.;totim=0.
            if (nlay < 0):
                nlay=-nlay
                ubdsvtype = self.read_integer()
                delt = self.read_real()
                pertim = self.read_real()
                totim = self.read_real()
           # print kstp,kper,text,nlay,nrow,ncol,ubdsvtype,delt,pertim,totim,True
            return kstp,kper,text,nlay,nrow,ncol,ubdsvtype,delt,pertim,totim,True
        except:
#            return kstp,kper,text,nlay,nrow,ncol,ubdsvtype,delt,pertim,totim,False
            return 0,0,'',0,0,0,0,0.0,0.0,0.0,False

    def read_cbbdata(self,nlay,nrow,ncol,ubdsvtype,text):
        temp=numpy.zeros((nlay,nrow,ncol))
        if(ubdsvtype < 2):
            temp[:,:,:]=self.read_3drealarray()
        if(ubdsvtype == 2):
            nlist = self.read_integer()
            for i in range(nlist):
                icrl=self.read_integer()
                Q=self.read_real()
                k,i,j=kij_from_icrl(icrl,nlay,nrow,ncol)
                temp[k-1,i-1,j-1] = temp[k-1,i-1,j-1] + Q
        if (ubdsvtype == 3):
            il = self.read_2dintegerarray()
            hl = self.read_2drealarray()
        if (ubdsvtype == 5):
            naux = 1 - self.read_integer()
            if (naux > 0):
                for i in range(naux):
                    dummy=self.read_text()
            nlist = self.read_integer()
            for i in range(nlist):
                icrl=self.read_integer()
                Q=self.read_real()
                k,i,j=kij_from_icrl(icrl,nlay,nrow,ncol)
                temp[k-1,i-1,j-1] = temp[k-1,i-1,j-1] + Q
                if (naux > 0):
                    for j in range(naux):
                        val[j]=self.read_real()
        self.flux=temp
        return

    def next(self):
        kstp,kper,text,nlay,nrow,ncol,ubdsvtype,delt,pertim,totim,success=self.read_header()
        if(success):
            self.read_cbbdata(nlay,nrow,ncol,ubdsvtype,text)
            return text,totim,kstp,kper,True
        else:
            #print 'MODFLOW_CBB object.read_next_cbb() reached end of file.'
            return '',0.0,0,0,False

    def read_next_fluxtype(self,fluxtype):
        while(True):
#            text,totim,kstp,kper,success=self.read_next_cbb()
            text,totim,kstp,kper,success=self.next()
            #print text,totim,kstp,kper
            if (success):
                if (string.strip(string.ljust(text,16)) == string.strip(string.ljust(fluxtype,16))):
#                               if (cmp(string.strip(string.ljust(text,16)),\
#                               string.strip(string.ljust(fluxtype,16)))) == 0:
                                        return kstp,kper,totim,self.flux,True
            else:
                return 0,0,0.0,numpy.empty((self.nlay,self.nrow,self.ncol)),False
                
    def get_record(self,fluxtype,kkstp,kkper):
                while(True):
#            text,totim,kstp,kper,success=self.read_next_cbb()
                        text,totim,kstp,kper,success=self.next()
                        if (success):
#                               if (kstp == kkstp and kper == kkper and \
#                               cmp(string.strip(string.ljust(text,16)),\
#                               string.strip(string.ljust(fluxtype,16)))) == 0:
#                                       return self.flux,totim,True
                                if (cmp(string.strip(string.ljust(text,16)),\
                                string.strip(string.ljust(fluxtype,16)))) == 0:
                                        if (kstp == kkstp and kper == kkper):
                                                return self.flux,totim,True
                        else:
                                return numpy.zeros((self.nlay,self.nrow,self.ncol),dtype='float')+1.0E+32,0.,False

    def print_cbb_info(self):
        success=True
        while(success):
            text,totim,success=self.read_next_cbb()
            print text,'totim:',totim
        return


    
class MT3D_Concentration(MFReadBinaryStatements,MF_Discretization):
    'Reads binary concentration output from MT3D concentration file'
    def __init__(self,nlay,nrow,ncol,filename):
        #initialize grid information
        self.assign_rowcollay(nlay,nrow,ncol)
        self.h = numpy.zeros((self.nlay, self.nrow, self.ncol),dtype='float')+1.0E+32
        #open binary head file
        self.file=open(filename,'rb')

    def read_header(self):
        try:
            self.NTRANS=self.read_integer()
            self.KSTP=self.read_integer()
            self.KPER=self.read_integer()
            self.TOTIM=self.read_real()
            self.TEXT=self.read_text()
            self.NCOL=self.read_integer()
            self.NROW=self.read_integer()
            self.ILAY=self.read_integer()

            return True
        except:
            return False

    def read_layerconcens(self):
        cl = self.read_2drealarray()
        cl.shape=(self.nrow,self.ncol)
        return cl

    def __iter__(self):
        return self

    def next(self):
     for k in range(self.nlay):
         success=self.read_header()
         if(success):
             assert self.NCOL==self.ncol, 'NCOL not consistent with binary heads file.'
             assert self.NROW==self.nrow, 'NROW not consistent with binary heads file.'
             self.h[self.ILAY-1, :, :] = self.read_layerconcens()
         else:
             #print 'MT3DMS_Concentration object.read_next_heads() reached end of file.'
             return 0.,0,0, numpy.zeros((self.nlay, self.nrow, self.ncol),dtype='float')+1.0E+32,False
     #print 'MT3DMS concentration read (ntrans,kstp,kper,time): ',self.NTRANS,self.KSTP,self.KPER,self.TOTIM 
     return self.TOTIM,self.KSTP,self.KPER,self.h,True
     
    def get_record(self,*args):
        try:
                kkspt = args[0]
                kkper = args[1]
                while True:
                        totim,kstp,kper,concen,success = self.next()
                        if success:
                                if kstp == kkspt and kkper == kper:
                                        return totim,kstp,kper,concen,True
                        else:
                                return 0.0,0,0,numpy.zeros((self.nlay,self.nrow,self,ncol),dtype='float')+1.0E+32,False 
        except:
            try:
                target_totim = args[0]                
                while True:
                    totim,kstp,kper,concen,success = self.next()
                    if success:
                        if target_totim <= totim:
                            return totim,kstp,kper,concen,True
                    else:
                        return 0.0,0,0,numpy.zeros((self.nlay,self.nrow,self.ncol),dtype='float')+1.0E+32,False
            except:
                previous = self.next()
                while True:
                    this_record = self.next()
                    if this_record[-1] == False:
                        return previous
                    else: previous = this_record
                    
                        
                                
class FVSWS_Record(FVSWSReadBinaryStatements):
    def __init__(self,filename):
        #--type = 0 = computation element record
        self.file = open(filename,'rb')
        self.nrow = self.read_integer()
        self.ncol = self.read_integer()
        self.nrecord = self.read_integer()
        self.ibound = self.read_2dintegerarray()
        self.delr = self.read_1drealarray(self.nrow)
        self.delc = self.read_1drealarray(self.ncol)
        self.botm = self.read_2drealarray()
        self.items = self.get_num_items()
        self.null_record = numpy.zeros((self.nrecord,self.items)) + 1.0E+32
        self.nodes = self.ncol * self.nrow
   
    def get_num_items(self):
        return 10 #volume
    
    def get_header_items(self):
        return ['totim','dt','kper','kstp','success_flag'] 

    def get_item_list(self):
        list = ['stage','qeast','qsouth','rain','evap',\
                        'latflow','qcrflow','dv','inf-out','volume']
        return list

    def get_bottom(self):
        return self.botm

    def get_row_col(self):
                rc = [self.nrow, self.ncol]
                return rc

    #--zero indexed row column location from one-based node number
    def get_row_col_loc(self, rec_num):
        if ( rec_num < 1 or rec_num > self.nodes ):
                rc = [0, 0]
        else:
                onrow = math.ceil( float(rec_num) / float(self.ncol) )
                oncol = float(rec_num) - ( (onrow - 1.0) * float(self.ncol) )
                rc = [int(onrow)-1, int(oncol)-1]
        return rc

    def read_header(self):
        try: 
            totim = self.read_double()
            dt = self.read_double()
            kper = self.read_integer()
            kstp = self.read_integer()
            return totim,dt,kper,kstp,True
        except:
            return 0.0,0.0,0,0,False
    
    def get_depth(self,h):
        r = numpy.zeros(len(h))
        for i in range(0,self.nrow):
                for j in range(0,self.ncol):
                        ib = self.ibound[i,j]
                        if ib > 0:
                                z = self.botm[i,j]
                                r[ib-1] = h[ib-1] - z
        return r 
                                

    def get_record(self,*args):
        #--pass a tuple of timestep,stress period
        try:
            kkspt = args[0]
            kkper = args[1]
            while True:
                totim,dt,kper,kstp,r,success = self.next()
                if success == True:
                    if kkspt == kstp and kkper == kper:
                        return totim,dt,kper,kstp,r,True
                else:
                    return 0.0,0.0,0,0,self.null_record,False
        except:
            #--pass a scalar of target totim - 
            #--returns either a match or the first
            #--record that exceeds target totim
            try:
                ttotim = float(args[0])
                while True:
                    totim,dt,kper,kstp,r,success = self.next()
                    if success == True:
                        if ttotim <= totim:
                            return totim,dt,kper,kstp,r,True
                    else:
                        return 0.0,0.0,0,0,self.null_record,False    
            except:
                #--get the last successful record
                previous = self.next()
                while True:
                    this_record = self.next()
                    if this_record[-1] == False:
                        return previous
                    else: previous = this_record
    
    def get_gage(self,rec_num):    
        gage_record = numpy.zeros((self.items+5))#items plus 4 header values
        while True:
            totim,dt,kper,kstp,r,success = self.next()
            if success == True:
                #print totim,numpy.shape(r[rec_num-1])
                this_entry = numpy.array([totim,dt,kper,kstp,success])
                this_entry = numpy.hstack((this_entry,r[rec_num-1]))
                gage_record = numpy.vstack((gage_record,this_entry))
            else: 
                gage_record = numpy.delete(gage_record,0,axis=0) #delete the first 'zeros' element
                return gage_record
                     
    def next(self):
        totim,dt,kper,kstp,success = self.read_header()
        #print totim,dt,kper,kstp,success     
        if success == False: 
#            print 'SWR_Stage.next() object reached end of file'
            return 0.0,0.0,0,0,self.null_record,False
        else:
                r = self.read_record()
#        print 'SWR data read for time step ',kstp,',stress period \
#                    ',kper,'and swr step ',swrstp
        return totim,dt,kper,kstp,r,True