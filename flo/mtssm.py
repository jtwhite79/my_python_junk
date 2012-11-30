import sys
import copy
import numpy as np
from mbase import package

class mtssm(package):
    'Sink & Source Mixing package class\n'
    def __init__(self, model, criv=0.0, cghb = 0.0,cibd = 0.0, cchd=0.0,\
                 crch=0.0, cpbc=1.0, cwel = 0.0, cevt = 0.0, itype_dict = None,extension='ssm'):
        # Call ancestor's init to set self.parent, extension, name and unit number
        package.__init__(self, model, extension, 'SSM', 34) 
        nrow, ncol, nlay, nper = self.parent.mf.nrow_ncol_nlay_nper
        mfchd = self.parent.mf.get_package('CHD')
        mfrch = self.parent.mf.get_package('RCH')
        mfevt = self.parent.mf.get_package('EVT')
        mfpbc = self.parent.mf.get_package('PBC')
        mfwel = self.parent.mf.get_package('WEL')
        mfghb = self.parent.mf.get_package('GHB')
        mfriv = self.parent.mf.get_package('RIV')
        # Check if the IBOUND array has any fixed heads
        mfbas = self.parent.mf.get_package('BAS6')
        self.ssmibound = np.empty((0, 3), dtype='int32')
        for r in range(nrow):
            for c in range(ncol):
                for l in range(nlay):
                    if (mfbas.ibound[r, c, l] < 0):
                        self.ssmibound = np.vstack((self.ssmibound, \
                                         np.array([l + 1, r + 1, c + 1])))
        if (self.ssmibound.shape[0] > 0):
            self.cibd = []
            if (not isinstance(cibd, list)):
                cibd = [cibd]
            for a in cibd:
                a = np.atleast_2d(a)
                b = np.empty((self.ssmibound.shape[0], a.shape[1]))
                for c in range(b.shape[0]):
                    if c < a.shape[0]:
                        b[c, :] = a[c, :]
                    else:
                        b[c, :] = a[-1, :]
                self.cibd = self.cibd + [b]
        # The assignments below do not yet check if the dimensions 
        #     of crch, cpbc, ..., etc. are
        # compatible with their corresponding MODFLOW structures! Better to fix...
        if (mfchd != None):
            self.cchd = []
            if (not isinstance(cchd, list)):
                cchd = [cchd]
            for a in cchd:
                b = np.empty((mfchd.layer_row_column_shead_ehead[0].shape[0]))
                self.assignarray(b , a )
                self.cchd = self.cchd + [b]
        if (mfghb != None):
            self.cghb = []
            if (not isinstance(cghb, list)):
                cghb = [cghb]
            for a in cghb:
                b = np.empty((mfghb.layer_row_column_head_cond[0].shape[0]))
                self.assignarray(b , a )
                self.cghb = self.cghb + [b]

        if (mfriv != None):
            self.criv = []
            if (not isinstance(criv, list)):
                criv = [criv]
            for a in criv:
                b = np.empty((mfriv.layer_row_column_Q[0].shape[0]))                
                self.assignarray(b , a )                
                self.criv = self.criv + [b]                        
               
        if (mfrch != None):
            self.crch = []
            if (not isinstance(crch, list)):
                crch = [crch]
            for a in crch:
                crch_t = []
                if (not isinstance(a, list)):
                    a = [a]
                for b in a:
                    c = np.empty((nrow, ncol))
                    self.assignarray(c , b )
                    crch_t.append(c)
                self.crch.append(crch_t)

        if (mfevt != None):
            self.cevt = []
            if (not isinstance(cevt, list)):
                cevt = [cevt]
            for a in cevt:
                cevt_t = []
                if (not isinstance(a, list)):
                    a = [a]
                for b in a:
                    c = np.empty((nrow, ncol))
                    self.assignarray(c , b )
                    cevt_t.append(c)
                self.cevt.append(cevt_t)
                           
        if (mfpbc != None):
            self.cpbc = []
            if (not isinstance(cpbc, list)):
                cpbc = [cpbc]
            for a in cpbc:
                b = np.empty((mfpbc.layer_row_column_shead_ehead[0].shape[0]))
                self.assignarray(b , a )
                self.cpbc = self.cpbc + [b]
           

        if (mfwel != None):
            self.cwel = []
            if (not isinstance(cwel, list)): cwel = [cwel]
            for a in cwel:
                a = np.atleast_2d(a)
                b = np.empty((mfwel.layer_row_column_Q[0].shape[0], a.shape[1]))  # allows for multiple species
                for c in range(b.shape[0]):
                    if c < a.shape[0]:
                        b[c, :] = a[c, :]
                    else:
                        b[c, :] = a[-1, :]
                self.cwel = self.cwel + [b]
        if itype_dict is not None:
            self.itype_max = 0
            for itype,data in itype_dict.items():
                if (not isinstance(data,list)):
                    data = [data]
                itype_max = 0
                for i,a in enumerate(data):
                    if a.shape[0] > itype_max:
                        itype_max = a.shape[0]
                    for aa in a:
                        assert len(aa) == 4
                    itype_dict[itype][i] = np.array(itype_dict[itype][i])                    
                self.itype_max += itype_max
            self.itype_dict = itype_dict                                                                                                           
        else:
            self.itype_dict = None
            self.itype_max = 0
        self.parent.add_package(self)
        
    def write_file(self):
        nrow, ncol, nlay, nper = self.parent.mf.nrow_ncol_nlay_nper
        mfchd = self.parent.mf.get_package('CHD')
        mfdrn = self.parent.mf.get_package('DRN')
        mfevt = self.parent.mf.get_package('EVT')
        mfghb = self.parent.mf.get_package('GHB')
        mfrch = self.parent.mf.get_package('RCH')
        mfpbc = self.parent.mf.get_package('PBC')
        mfriv = self.parent.mf.get_package('RIV')
        mfwel = self.parent.mf.get_package('WEL')  
        # Open file for writing
        f_ssm = open(self.file_name[0], 'w')
        maxssm = 0
        if (mfwel == None):
            f_ssm.write('%2s' % ('F'))
        else:
            f_ssm.write('%2s' % ('T'))
            maxssm = maxssm + mfwel.ncells()
        if (mfdrn == None):
            f_ssm.write('%2s' % ('F'))
        else:
            f_ssm.write('%2s' % ('T'))
            maxssm = maxssm + mfdrn.ncells()           
        if (mfrch == None):
            f_ssm.write('%2s' % ('F'))
        else:
            f_ssm.write('%2s' % ('T'))
            maxssm = maxssm + mfrch.ncells()
        if (mfevt == None):
            f_ssm.write('%2s' % ('F'))
        else:
            f_ssm.write('%2s' % ('T'))
            maxssm = maxssm + mfevt.ncells()
        if (mfriv == None):
            f_ssm.write('%2s' % ('F'))
        else:
            f_ssm.write('%2s' % ('T'))
            maxssm = maxssm + mfriv.ncells()
        if (mfghb == None):
            f_ssm.write('%2s' % ('F'))
        else:
            f_ssm.write('%2s' % ('T'))            
            maxssm = maxssm + mfghb.ncells()            
        # Fixed heads in IBOUND
        if (self.ssmibound.shape[0] > 0):
            maxssm = maxssm + self.ssmibound.shape[0]
        # CHD package
        if (mfchd != None):
            maxssm = maxssm + mfchd.ncells()
        # PBC package
        if (mfpbc != None):
            maxssm = maxssm + mfpbc.ncells()
        
        maxssm += self.itype_max             
        f_ssm.write('%2s%2s%2s%2s\n' % ('F', 'F', 'F', 'F'))
        f_ssm.write('%10d\n' % (maxssm))
        for n in range(nper):
            # Recharge
            if (mfrch != None):
                if (n < len(self.crch)):
                    incrch = 1
                else:
                    incrch = -1
                f_ssm.write('%10i\n' % (incrch))
                if (n < len(self.crch)):
                    for s in range(len(self.crch[n])):                        
                        comment = 'Recharge concentration array of species '+\
                                  '%d for stress period %d' % (s + 1, n + 1)
                        self.parent.write_array( f_ssm, self.crch[n][s], \
                             self.unit_number[0], True, 13, ncol, comment )
            # Evapotranspiration
            if (mfevt != None):
                if (n < len(self.cevt)):
                    incevt = 1
                else:
                    incevt = -1
                f_ssm.write('%10i\n' % (incevt))
                if (n < len(self.cevt)):
                    for s in range(len(self.cevt[n])):
                        #print 'calling ssm EVT'
                        comment = 'EVT concentration array of species' +\
                                  '%d for stress period %d' % (s + 1, n + 1)
                        self.parent.write_array( f_ssm, self.cevt[n][s], \
                             self.unit_number[0], True, 13, ncol, comment )
            # WEL, DRN, RIV, GHB, PBC
            nss = 0
            need_nss = False
            if (self.ssmibound.shape[0] > 0):
                need_nss = True
                nss = nss + self.ssmibound.shape[0]
            if (mfchd != None):
                if (n < len(mfchd.layer_row_column_shead_ehead)):
                    ssmchd = mfchd.layer_row_column_shead_ehead[n]
                    need_nss = True
                else:
                    ssmchd = mfchd.layer_row_column_shead_ehead[-1]
                nss = nss + ssmchd.shape[0]
            if (mfpbc != None):
                if (n < len(mfpbc.layer_row_column_shead_ehead)):
                    ssmpbc = mfpbc.layer_row_column_shead_ehead[n]
                    need_nss = True
                else:
                    ssmpbc = mfpbc.layer_row_column_shead_ehead[-1]
                nss = nss + ssmpbc.shape[0]
            if (mfdrn != None):
                if (n < len(mfdrn.layer_row_column_elevation_cond)):
                    ssmdrn = mfdrn.layer_row_column_elevation_cond[n]
                    need_nss = True
                else:
                    ssmdrn = mfdrn.layer_row_column_elevation_cond[-1]
                nss = nss + ssmdrn.shape[0]    
                
            if (mfwel != None):
                if (n < len(mfwel.layer_row_column_Q)):
                    ssmwel = mfwel.layer_row_column_Q[n]
                    need_nss = True
                else:
                    ssmwel = mfwel.layer_row_column_Q[-1]
                nss = nss + ssmwel.shape[0]
            if (mfghb != None):
                if (n < len(mfghb.layer_row_column_head_cond)):
                    ssmghb = mfghb.layer_row_column_head_cond[n]
                    need_nss = True
                else:
                    ssmghb = mfghb.layer_row_column_head_cond[-1]
                nss = nss + ssmghb.shape[0]
            if (mfriv != None):
                if (n < len(mfriv.layer_row_column_Q)):
                    ssmriv = mfriv.layer_row_column_Q[n]
                    need_nss = True
                else:
                    ssmriv = mfriv.layer_row_column_Q[-1]
                nss = nss + ssmriv.shape[0]
            #--generic - itypes 15 and -1
            if self.itype_dict is not None:
                itype_data = []
                for itype,data in self.itype_dict.items():
                    if (n < len(data)):
                        itype_data.append(data[n])           
                        need_nss = True
                        nss += data[n].shape[0]
                    else:
                        itype_data.append(data[-1])
                        nss += data[-1].shape[0]                                                       
           
            if (need_nss == True):
                f_ssm.write('%10i\n' % (nss))
                if (self.ssmibound.shape[0] > 0):
                    if (n < len(self.cibd)):
                        c = self.cibd[n]
                    else:
                        c = self.cibd[-1]
                    i = 0
                    for b in self.ssmibound:
                        f_ssm.write('%10i%10i%10i%10f%10i' % \
                                   (b[0], b[1], b[2], c[i, 0], 1) )
                        for j in range(c.shape[1]):
                            f_ssm.write('%10f' % c[i, j])
                        f_ssm.write('\n')
                        i = i + 1
                if (mfchd != None):
                    if (n < len(self.cchd)):
                        c = self.cchd[n]
                    else:
                        c = self.cchd[-1]
                    i = 0
                    for b in ssmchd:
                        f_ssm.write('%10i%10i%10i%10f%10i\n' % \
                                   (b[0], b[1], b[2], c[i], 1) )
                        i = i + 1
                if (mfghb != None):
                    if (n < len(self.cghb)):
                        c = self.cghb[n]
                    else:
                        c = self.cghb[-1]
                    i = 0
                    for b in ssmghb:
                        f_ssm.write('%10i%10i%10i%10f%10i\n' % \
                                   (b[0], b[1], b[2], c[i], 5) )
                        i = i + 1
                
                if (mfriv != None):
                    if (n < len(self.criv)):
                        c = self.criv[n]
                    else:
                        c = self.criv[-1]                   
                    for b,c in zip(ssmriv,c):
                        f_ssm.write('%10i%10i%10i%10f%10i\n' % \
                                   (b[0], b[1], b[2], c, 4) )
                
                if (mfdrn != None):                                      
                    for b in ssmdrn:
                        #print b
                        f_ssm.write('%10i%10i%10i%10f%10i\n' % \
                                   (b[0], b[1], b[2], 0.0, 3) )
                
                
                                
                if (mfpbc != None):
                    if (n < len(self.cpbc)):
                        c = self.cpbc[n]
                    else:
                        c = self.cpbc[-1]
                    i = 0
                    for b in ssmpbc:
                        f_ssm.write('%10i%10i%10i%10f%10i\n' % \
                                   (b[0], b[1], b[2], c[i], 51) )
                        i = i + 1
                if (mfwel != None):
                    if (n < len(self.cwel)):
                        c = self.cwel[n]
                    else:
                        c = self.cwel[-1]
                    i = 0                                        
                    for b in ssmwel:
                        f_ssm.write('%10i%10i%10i%10f%10i' % \
                                   (b[0], b[1], b[2], c[i, 0], 2) )
                        for j in range(c.shape[1]):
                            f_ssm.write('%10f' % c[i, j])
                        f_ssm.write('\n')
                        i = i + 1
                if (self.itype_dict is not None):
                    for itype,data in self.itype_dict.items():
                        if (n<len(data)):
                            cells = data[n]
                        else:
                            cells = data[-1]                        
                        for c in cells:
                            #print c
                            f_ssm.write('{0:10.0f}{1:10.0f}{2:10.0f}{3:10.3e}{4:10.0f}\n'\
                                    .format(c[0],c[1],c[2],c[3],itype))                                
                                               
            else:
               f_ssm.write('%10i\n' % (-1))
        f_ssm.close()
        


