import numpy as np


# set a few constants
UNINIT_STRING = 'unititialized'
UNINIT_REAL   = '-9.9999e25'
UNINIT_INT    = '-99999'

# ############################################################################### #
# Function to write out a KW block line to the PST file for pest++ variables only #
# ############################################################################### #

def write_KW_line_ppp(ofp,cdict,cblock,mandatoryvals,mandatorytypes,optionalvals=False,optionaltypes=False,**kwargs):
    
    try:
        writenewline = kwargs['writenewline']        
    except KeyError:
        writenewline = True
    
    # check that all mandatory keys are present
    for ckey in mandatoryvals:
        if ckey not in cdict.keys():
            raise(DefaultValueError(ckey,cblock))
    for i,cmand in enumerate(mandatoryvals):
        write_val_ppp(ofp,cdict[cmand],mandatorytypes[i],cmand,cblock)
    if optionalvals != False:    
        for i,copt in enumerate(optionalvals):
            try:
                write_val(ofp,cdict[copt],optionaltypes[i],copt,cblock,optflag=True)
            except KeyError:
                pass
    if writenewline:
        ofp.write('\n')
# ########################################################################################################## #
# Function to write out a KW block line to the PST file: can include mix of mandatory and optional variables #
# ########################################################################################################## #

def write_KW_line(ofp,cdict,cblock,mandatoryvals,mandatorytypes,optionalvals=False,optionaltypes=False,**kwargs):
    
    try:
        writenewline = kwargs['writenewline']        
    except KeyError:
        writenewline = True
    
    # check that all mandatory keys are present
    for ckey in mandatoryvals:
        if ckey not in cdict.keys():
            raise(DefaultValueError(ckey,cblock))
    for i,cmand in enumerate(mandatoryvals):
        write_val(ofp,cdict[cmand],mandatorytypes[i],cmand,cblock)
    if optionalvals != False:    
        for i,copt in enumerate(optionalvals):
            try:
                write_val(ofp,cdict[copt],optionaltypes[i],copt,cblock,optflag=True)
            except KeyError:
                pass
    if writenewline:
        ofp.write('\n')

# ########################################################################################################## #
# Function to write out a TABLE block line to the PST file: can include mix of mandatory and optional variables #
# ########################################################################################################## #

def write_TAB_line(ofp,cdict,cblock,mandatoryvals,mandatorytypes,optionalvals=False,optionaltypes=False,**kwargs):
    try:
        writenewline = kwargs['writenewline']        
    except KeyError:
        writenewline = True
        
    # check that all mandatorykeys are present
    for ckey in mandatoryvals:
        if ckey not in cdict.keys():
            raise(DefaultValueError(mandatoryvals[0],cblock))
    for cr in xrange(len(cdict[mandatoryvals[0]])):
        for i,cmand in enumerate(mandatoryvals):
            write_val(ofp,cdict[cmand][cr],mandatorytypes[i],cmand,cblock)
        if optionalvals != False:     
            for i,copt in enumerate(optionalvals):
                try:
                    write_val(ofp,cdict[copt][cr],optionaltypes[i],copt,cblock)
                except KeyError:
                    pass
        if writenewline:
            ofp.write('\n')

# ############################################################################### #
# Function to write out a single value to the PST file with type-checking: pest++ # 
# ############################################################################### #
def write_val_ppp(ofp,cval,cvaltype,parnme,blockname,optflag=False):
    if cvaltype == 'int':
        if cval == UNINIT_INT:
            if optflag:
                return
            else:
                raise(DefaultValueError(parnme,blockname))        
        try:
            cv = int(cval)
            ofp.write(' %s ' %(parnme + '(' + str(cval) + ')'))
        except:
            raise(TypeFailError(cval,parnme,cvaltype))
    elif cvaltype == 'real':
        if cval == UNINIT_REAL:
            if optflag:
                return
            else:
                raise(DefaultValueError(parnme,blockname))        
        try:
            cv = float(cval)
            ofp.write(' %s ' %(parnme + '(' + str(cval) + ')'))
        except:
            raise(TypeFailError(cval,parnme,cvaltype))
    elif cvaltype == 'string':
        if cval == UNINIT_STRING:
            if optflag:
                return
            else:
                raise(DefaultValueError(parnme,blockname))        
        try: # is it an int?
            cv = int(cval)
        except:
            try: # is it a float?
                cv = float(cval)
            except: # neither a float nor an int
                ofp.write(' %s ' %(parnme + '(' + str(cval) + ')'))


# ####################################################################### #
# Function to write out a single value to the PST file with type-checking # 
# ####################################################################### #
def write_val(ofp,cval,cvaltype,parnme,blockname,optflag=False):
    if cvaltype == 'int':
        if cval == UNINIT_INT:
            if optflag:
                return
            else:
                raise(DefaultValueError(parnme,blockname))        
        try:
            cv = int(cval)
            ofp.write('%8d' %(cv))
        except:
            raise(TypeFailError(cval,parnme,cvaltype))
    elif cvaltype == 'real':
        if cval == UNINIT_REAL:
            if optflag:
                return
            else:
                raise(DefaultValueError(parnme,blockname))        
        try:
            cv = float(cval)
            ofp.write('%16.8e' %(cv))
        except:
            raise(TypeFailError(cval,parnme,cvaltype))
    elif cvaltype == 'string':
        if cval == UNINIT_STRING:
            if optflag:
                return
            else:
                raise(DefaultValueError(parnme,blockname))        
        try: # is it an int?
            cv = int(cval)
        except:
            try: # is it a float?
                cv = float(cval)
            except: # neither a float nor an int
                ofp.write(' %s ' %(cval))


# ############################ #
# Class to hold keyword blocks # 
# ############################ #
class kw:

    def __init__(self, blockname,kwdict,blockstart=0,blockend=0):
        self.blockname = blockname   # name of the block
        self.kwdict = kwdict         # provided at initialization ---
                        # dict with keys -> parname, vals -> values                                   
        self.blockstart = blockstart # starting line for block
        self.blockend = 0            # ending line for block

# ########################## #
# Class to hold table blocks # 
# ########################## #
class tb:

    def __init__(self,blockname,colnames,nrow=0,ncol=0,blockstart=0,blockend=0):
        self.blockname = blockname   # name of the block
        self.nrow = nrow             # number of rows to read
        self.ncol = ncol             # number of columns to read
        self.colnames = colnames     # read in the column names
        self.extfile = UNINIT_STRING # external file in case of external
        self.blockstart = blockstart # starting line for block
        self.blockend = 0            # ending line for block


# ########################### #
# Function to find duplicates # 
# ########################### #
def dedupe(allv,uniqueval):
    dupes = []
    for u in uniqueval:
        k = 0
        for v in allv:
            if v == u:
                k+=1
        if k>1:
            dupes.append(u)
    return dupes

# ################################################ #
# Class to hold information about the in/out files #
# ################################################ #
class file_control():
    # ############## #
    # INITIALIZATION #
    # ############## #
    def __init__(self,infilename,outfilename):
        self.infile = infilename
        self.outfile = outfilename
        #self.kwblocksall = kws
        self.kwblocksall = kwblocks.keys
        self.kwblocks = dict()
        #self.tabblocksall = tabs
        self.tabblocksall = tabblocks.keys()
        self.tabblocks = dict()
        #self.tabblockdict = tabblockdicts
        self.tabblockdict =  tabblockdicts

    # ################################################### #
    # Learn block names, bomb on duplicates or bad syntax #
    # ################################################### #
    def check_block_integrity(self):
        self.indat = open(self.infile,'r').readlines()
        cline = -1
        # first find all block names and types
        allbegins = list()
        allends = list()
        for line in self.indat:
            cline += 1
            tmp = line.lower().strip().split()
            if 'begin' in tmp:
                if len(tmp) > 3:
                    raise(BlockSyntaxError(cline))
                if 'keywords' in tmp:
                    allbegins.append([cline,tmp[1],'kw'])
                elif 'table' in tmp:
                    allbegins.append([cline,tmp[1],'tab'])
                elif 'file' in tmp:
                    allbegins.append([cline,tmp[1],'tab'])
                else:
                    raise(BlockSyntaxError(cline))
            elif 'end' in tmp:
                if len(tmp) > 2:
                    raise(BlockSyntaxError(cline))
                else:
                    allends.append([cline,tmp[1]])
        allbegins = np.array(allbegins)
        allends = np.array(allends)

        # now check that there are no duplicates
        kwbegins = allbegins[np.nonzero(allbegins[:,2]=='kw')[0]]
        eunichkwbegins = np.unique(kwbegins[:,1])
        tabbegins = allbegins[np.nonzero(allbegins[:,2]=='tab')[0]]
        eunichtabbegins = np.unique(tabbegins[:,1])

        # run dedupe function to identify dupes
        kwbegin_dupes = dedupe(kwbegins[:,1],eunichkwbegins) 
        tabbegin_dupes = dedupe(tabbegins[:,1],eunichtabbegins) 
        end_dupes = dedupe(allends[:,1],np.unique(allends[:,1]))
        dupes = []
        if len(kwbegin_dupes) > 0:
            dupes.extend(kwbegin_dupes)
        if len(tabbegin_dupes) > 0:
            dupes.extend(tabbegin_dupes)
        if len(end_dupes) > 0 :
            dupes.extend(end_dupes)
        dupes = np.unique(np.array(dupes))
        if len(dupes) > 0:
            raise(BlockDuplicate(dupes))


    # ################################################################## #
    # Set starting and ending row numbers, bomb on wrongly nested blocks #
    # ################################################################## #
    def initialize_blocks(self):        
        cline = -1
        # read through and create the block classes, just finding BEGINs of blocks
        for line in self.indat:    
            cline += 1
            tmp = line.lower().strip().split()
            if 'begin' in tmp:
                if len(tmp) > 3:
                    raise(BlockSyntaxError(cline))
                if 'keywords' in tmp:
                    if tmp[1] in self.kwblocksall:
                        self.kwblocks[tmp[1]]=kw(tmp[1],
                                                 kwblocks[tmp[1]],
                                                 blockstart=cline)
                    else:
                        raise(BlockNameError(cline,tmp[1]))
                elif 'table' in tmp:
                    if tmp[1] in self.tabblocksall:
                        self.tabblocks[tmp[1]] = tb(tmp[1],
                                                    tabblocks[tmp[1]],
                                                    blockstart=cline)
                    else:
                        raise(BlockNameError(cline,tmp[1]))
                elif 'file' in tmp:
                    if tmp[1] in self.tabblocksall:
                        self.tabblocks[tmp[1]] = tb(tmp[1],
                                                    tabblocks[tmp[1]],
                                                    blockstart=cline)
                    else:
                        raise(BlockNameError(cline,tmp[1]))
        allkeynames = self.kwblocks.keys()
        alltabnames = self.tabblocks.keys()

        # read through and add END line numbers
        cline = -1
        for line in self.indat:    
            cline += 1
            tmp = line.lower().strip().split()
            if 'end' in tmp:
                if len(tmp) > 2:
                    raise(BlockSyntaxError(cline))
                if tmp[1] in allkeynames:
                    self.kwblocks[tmp[1]].blockend = cline
                elif tmp[1] in alltabnames:
                    self.tabblocks[tmp[1]].blockend = cline
                else:
                    raise(BlockMismatchNoBEGIN(tmp[1]))

        # check for blocks that start without end 
        for cb in self.kwblocks:
            if self.kwblocks[cb].blockend == 0:
                raise(BlockMismatchNoBEGIN(cb))
            elif self.kwblocks[cb].blockend <= self.kwblocks[cb].blockstart:
                raise(BlockReversed(cb))

        for cb in self.tabblocks:
            if self.tabblocks[cb].blockend == 0:
                raise(BlockMismatchNoBEGIN(cb))
            elif self.tabblocks[cb].blockend <= self.tabblocks[cb].blockstart:
                raise(BlockReversed(cb))        
        # check or blocks that end before they start

        # finally, make sure there are no blocks inside other blocks
        dumbcheck = []
        dumbchecknames = []
        # get an array of starting and ending line numbers 
        for i,v in enumerate(self.kwblocks):
            dumbchecknames.append([v])
            dumbcheck.append([self.kwblocks[v].blockstart,
                              self.kwblocks[v].blockend,
                              i])
        for i,v in enumerate(self.tabblocks):
            dumbchecknames.append([v])
            dumbcheck.append([self.tabblocks[v].blockstart,
                              self.tabblocks[v].blockend,
                              i])
        dumbcheck = np.array(dumbcheck)
        dumbcheck = dumbcheck[dumbcheck[:,0].argsort()]
        # easy check first
        dc = dumbcheck[:,[0,1]].reshape(dumbcheck.shape[0]*2,1)
        dds = np.diff(np.squeeze(dc))
        if np.min(dds > 0):
            return # all good
        else:
            # now got to figure out where the dumbness occurs
            for i in np.arange(1,len(dumbcheck)):
                if dumbcheck[i,0] <= dumbcheck[i-1,1]:
                    insidenm = dumbchecknames[dumbcheck[i,2]][0]
                    outsidenm = dumbchecknames[dumbcheck[i-1,2]][0]
                    raise(BlockIllegalNesting(insidenm,outsidenm))
        print i
    # ################################################# #
    # read each keyword block and populate the keywords #
    # ################################################# #
    def read_keyword_blocks(self):
        for i in self.kwblocks:
            # cblock is shorthand for the current block
            cblock = self.kwblocks[i]
            # set the list of legal keys
            legal_keywords = cblock.kwdict.keys()
            #read between the boundaries of the block
            cbdata = self.indat[cblock.blockstart+1:cblock.blockend]
            # make an extended list alternating between KEY and VAL
            allpairs = list()
            for line in cbdata:
                tmp = line.split()
                if len(tmp)>0:
                    if tmp[0] != '#':
                        tmp = line.strip().split('=')
                        for j in tmp:
                            allpairs.extend(j.split())
            if len(allpairs) == 0:
                raise(KeywordBlockEmpty(i,cblock.blockstart+1))
            # split temporarily into two lists
            ckeys = allpairs[::2]
            cvals = allpairs[1::2]
            # check that they are the same length
            if len(ckeys) != len(cvals):
                raise(KeywordBlockError(i))
            # make a dictionary of keywords with values
            allpairs = dict(zip(ckeys,cvals))
            for ckey in allpairs:
                if ckey.upper() in legal_keywords:
                    cblock.kwdict[ckey.upper()] = allpairs[ckey]
                # case especiale for the pesky pareto reporting keywords
                elif i == 'pareto':
                    if 'OBS_REPORT_' in ckey.upper():
                        cblock.kwdict[ckey.upper()] = allpairs[ckey]    

    # ########################################### #
    # read each table block and populate the data #
    # ########################################### #
    def read_table_blocks(self):
        for i in self.tabblocks:
            # cblock is shorthand for the current block
            cblock = self.tabblocks[i]
            # set the list of legal keys
            legal_columns = cblock.colnames
            # ## handle external files ability
            if 'file' in self.indat[cblock.blockstart].lower():
                tmp1 = []
                tmp = self.indat[cblock.blockstart+1:cblock.blockend]
                for line in tmp:
                    tval = line.strip().split()
                    if len(tval) > 0:
                        if '#' not in tval[0]:
                            tmp1.append(line)
                if len(tmp1) > 1:
                    raise(ExternalFileError(tmp1,i))
                else:
                    try:
                        cbdata = open(tmp1[0].strip(),'r').readlines()
                    except:
                        raise(ExternalFileOpenError(tmp1[0],i))
            else:
                #read between the boundaries of the block
                cbdata = self.indat[cblock.blockstart+1:cblock.blockend]
            # pull out the header information and parse nrow and ncol
            cheader = cbdata.pop(0)
            header_data = cheader.strip().split('=')
            hd = []
            for j in header_data:
                hd.extend(j.split())
            # check that the header information is correctly formatted
            if len(hd) == 0:
                raise(TableBlockEmpty(i,cblock.blockstart+2))
            try:
                if ((hd[0].lower() == 'nrow') and
                    (hd[2].lower() == 'ncol') and
                    (hd[4].lower() == 'columnlabels')):
                    try:
                        cblock.nrow = int(hd[1])
                    except:
                        raise(TableBlockHeaderError(cblock.blockstart+2))
                    try:
                        cblock.ncol = int(hd[3])
                    except:
                        raise(TableBlockHeaderError(cblock.blockstart+2))
            except:
                raise(TableBlockHeaderError(cblock.blockstart+2))


            # pull off the column labels
            clabels = cbdata.pop(0).strip().split()

            # check each row for the correct number of columns
            cline = cblock.blockstart + 3
            if len(clabels) != cblock.ncol:
                raise(TableBlockColError(i,cline,cblock.ncol,len(clabels)))
            for line in cbdata:
                cline += 1
                if '#' in line:
                    raise(TableCommentError(cline,cblock.blockname))
                else:
                    tmp = line.strip().split()
                    if i != 'prior_information':
                        if len(tmp) != cblock.ncol:
                            raise(TableBlockColError(i,cline,cblock.ncol,len(tmp)))
                    elif len(tmp) < 1: 
                        raise(TableBlockColError(i,cline,cblock.ncol,len(tmp)))
            # now check the number of rows
            if len(cbdata) != cblock.nrow:
                raise(TableBlockRowError(i,cblock.nrow,len(cbdata)))   

            # parse the data into a dictionary for later output
            data_array = list()
            for line in cbdata:
                if '#' not in line:
                    if i != 'prior_information':
                        data_array.append(line.strip().split())
                    else:
                        data_array.append(line.strip())
            data_array = np.atleast_2d(np.squeeze(np.array(data_array)))
            for jj,keyy in enumerate(clabels):
                if keyy in legal_columns:
                    if cblock.ncol == 1:
                        self.tabblockdict[i][keyy] = data_array[0]
                    else:
                        self.tabblockdict[i][keyy] = data_array[:,jj]
                else:
                    raise(BlockIllegalColumn(i,keyy))
    # ###################### #
    # Write out the PST file #
    # ###################### #
    def write_pst_file(self):
        # open an output file
        ofp = open(self.outfile,'w')
        # ###
        # Write out mandatory control data block
        # ###
        cblock = 'control_data'
        try:
            cdict = self.kwblocks[cblock].kwdict
        except KeyError:
            raise(MissingBlockError(cblock))
        # write out the mandatory control data block
        ofp.write('pcf\n'+
                  '* control data\n')
        write_val(ofp,cdict['RSTFLE'],'string','RSTFLE',cblock)
        write_val(ofp,cdict['PESTMODE'],'string','PESTMODE',cblock)
        ofp.write('\n')
        # write a line
        mandatoryvals = ['NPAR', 'NOBS', 'NPARGP', 'NPRIOR', 'NOBSGP']
        mandatorytypes = ['int','int','int','int','int']
        optionalvals = ['MAXCOMPDIM']
        optionaltypes = ['int']
        write_KW_line(ofp,cdict,cblock,mandatoryvals,mandatorytypes,optionalvals,optionaltypes)
        # write a line
        mandatoryvals = ['NTPLFLE', 'NINSFLE', 'PRECIS', 'DPOINT']
        mandatorytypes = ['int','int','string','string']
        optionalvals = ['NUMCOM', 'JACFILE', 'MESSFILE']
        optionaltypes = ['int','int','int']
        write_KW_line(ofp,cdict,cblock,mandatoryvals,mandatorytypes,optionalvals,optionaltypes)
        # write a line
        mandatoryvals = ['RLAMBDA1', 'RLAMFAC', 'PHIRATSUF', 'PHIREDLAM', 'NUMLAM']
        mandatorytypes = ['real','real','real','real','int']
        optionalvals = ['JACUPDATE', 'LAMFORGIVE', 'MESSFILE']
        optionaltypes = ['int','string','int']
        write_KW_line(ofp,cdict,cblock,mandatoryvals,mandatorytypes,optionalvals,optionaltypes)
        # write a line
        mandatoryvals = ['RELPARMAX', 'FACPARMAX', 'FACORIG']
        mandatorytypes = ['real','real','real']
        optionalvals = ['IBOUNDSTICK', 'UPVECBEND']
        optionaltypes = ['int','int']
        write_KW_line(ofp,cdict,cblock,mandatoryvals,mandatorytypes,optionalvals,optionaltypes)
        # write a line
        mandatoryvals = ['PHIREDSWH']
        mandatorytypes = ['real']
        optionalvals = ['NOPTSWITCH', 'SPLITSWH','DOAUI','DOSENREUSE']
        optionaltypes = ['int','real','string','string']
        write_KW_line(ofp,cdict,cblock,mandatoryvals,mandatorytypes,optionalvals,optionaltypes)
        # write a line
        mandatoryvals = ['NOPTMAX', 'PHIREDSTP', 'NPHISTP', 'NPHINORED', 'RELPARSTP', 'NRELPAR']
        mandatorytypes = ['int','real','int','int','real','int']
        write_KW_line(ofp,cdict,cblock,mandatoryvals,mandatorytypes,writenewline=False)
        # strange special case here
        if cdict['PHISTOPTHRESH'] != UNINIT_REAL:
            write_val(ofp,cdict['PHISTOPTHRESH'],'real','PHISTOPTHRESH',cblock) 
        if cdict['LASTRUN'] != UNINIT_INT:
            write_val(ofp,cdict['LASTRUN'],'int','LASTRUN',cblock)  
        if cdict['PHIABANDON'] != UNINIT_INT:
            if cdict['PHIABANDON'] != UNINIT_STRING:
                try:
                    int(cdict['PHIABANDON'])
                    write_val(ofp,cdict['PHIABANDON'],'int','PHIABANDON',cblock)
                except:
                    write_val(ofp,cdict['PHIABANDON'],'string','PHIABANDON',cblock)
        ofp.write('\n')
        # write a line
        mandatoryvals = ['ICOV', 'ICOR', 'IEIG']
        mandatorytypes = ['int','int','int']
        optionalvals = ['IRES','JCOSAVE', 'VERBOSEREC','JCOSAVEITN', 'REISAVEITN','PARSAVEITN']
        optionaltypes = ['int','string','string','string','string','string']
        write_KW_line(ofp,cdict,cblock,mandatoryvals,mandatorytypes,optionalvals,optionaltypes)

        # ###
        # Write out optional automatic user intervention block if requested by DOAUI
        # ###
        cblock = 'automatic_user_intervention'
        try:
            if self.kwblocks[cblock].kwdict['DOAUI'].lower() == 'aui':
                try:
                    cdict = self.kwblocks[cblock].kwdict
                except KeyError:
                    raise(MissingBlockError(cblock))
            ofp.write('* automatic user intervention\n')
            # write a line
            mandatoryvals = ['MAXAUI', 'AUISTARTOPT', 'NOAUIPHIRAT', 'AUIRESTITN']
            mandatorytypes = ['int','int','real','int']
            write_KW_line(ofp,cdict,cblock,mandatoryvals,mandatorytypes)
            # write a line
            mandatoryvals = ['AUISENSRAT', 'AUIHOLDMAXCHG', 'AUINUMFREE']
            mandatorytypes = ['real','int','int']
            write_KW_line(ofp,cdict,cblock,mandatoryvals,mandatorytypes)
            # write a line
            mandatoryvals = ['AUIPHIRATSUF', 'AUIPHIRATACCEPT', 'NAUINOACCEPT']
            mandatorytypes = ['real','real','int']
            write_KW_line(ofp,cdict,cblock,mandatoryvals,mandatorytypes)
        except KeyError:
            pass
        # ###
        # Write out optional singular value decomposition block
        # ###
        cblock = 'singular_value_decomposition'
        try:
            cdict = self.kwblocks[cblock].kwdict
            ofp.write('* singular value decomposition\n')
            # write a line
            mandatoryvals = ['SVDMODE']
            mandatorytypes = ['int']
            write_KW_line(ofp,cdict,cblock,mandatoryvals,mandatorytypes)
            # Set MAXSING to a default value if not specified
            if cdict['MAXSING'] == UNINIT_REAL:
                cdict['MAXSING'] = self.kwblocks['control_data'].kwdict['NPAR']
            # write a line
            mandatoryvals = ['MAXSING', 'EIGTHRESH']
            mandatorytypes = ['int','real']
            write_KW_line(ofp,cdict,cblock,mandatoryvals,mandatorytypes)
            # write a line
            mandatoryvals = ['EIGWRITE']
            mandatorytypes = ['int']
            write_KW_line(ofp,cdict,cblock,mandatoryvals,mandatorytypes)
        except KeyError:
            pass
        # ###
        # Write out optional lsqr block
        # ###
        cblock = 'lsqr'
        try:
            cdict = self.kwblocks[cblock].kwdict
            ofp.write('* lsqr\n')
            # write a line
            mandatoryvals = ['LSQRMODE']
            mandatorytypes = ['int']
            write_KW_line(ofp,cdict,cblock,mandatoryvals,mandatorytypes)
            # write a line
            mandatoryvals = ['LSQR_ATOL', 'LSQR_BTOL', 'LSQR_CONLIM', 'LSQR_ITNLIM']
            mandatorytypes = ['real','real','real','int']
            write_KW_line(ofp,cdict,cblock,mandatoryvals,mandatorytypes)
            # write a line
            mandatoryvals = ['LSQRWRITE']
            mandatorytypes = ['int']
            write_KW_line(ofp,cdict,cblock,mandatoryvals,mandatorytypes)
        except KeyError:
            pass         
        # ###
        # Write out optional SVDA block
        # ###
        cblock = 'svd_assist'
        try:
            cdict = self.kwblocks[cblock].kwdict
            ofp.write('* svd assist\n')
            #write a line
            write_val(ofp,cdict['BASEPESTFILE'],'string','BASEPESTFILE',cblock)
            ofp.write('\n')
            #write a line
            write_val(ofp,cdict['BASEJACFILE'],'string','BASEJACFILE',cblock)
            ofp.write('\n')
            #write a line
            mandatoryvals = ['SVDA_MULBPA', 'SVDA_SCALADJ', 'SVDA_EXTSUPER', 'SVDA_SUPDERCALC', 'SVDA_PAR_EXCL']
            mandatorytypes = ['int','int','int','int']
            write_KW_line(ofp,cdict,cblock,mandatoryvals,mandatorytypes)
        except KeyError:
            pass        
        # ###
        # Write out optional sensitivity reuse block
        # ###
        cblock = 'sensitivity_reuse'
        try:
            cdict = self.kwblocks[cblock].kwdict
            ofp.write('* sensitivity reuse\n')
            # write a line
            mandatoryvals = ['SENRELTHRESH', 'SENMAXREUSE']
            mandatorytypes = ['real','int']
            write_KW_line(ofp,cdict,cblock,mandatoryvals,mandatorytypes)
            # write a line
            mandatoryvals = ['SENALLCALCINT', 'SENPREDWEIGHT', 'SENPIEXCLUDE']
            mandatorytypes = ['int','real','string']
            write_KW_line(ofp,cdict,cblock,mandatoryvals,mandatorytypes)
        except KeyError:
            pass        
        # ###
        # Write out mandatory parameter groups block
        # ###        
        cblock = 'parameter_groups'
        cdict = self.tabblockdict[cblock]
        if len(cdict) == 0:
            raise(MissingBlockError(cblock))
        else:
            ofp.write('* parameter groups\n')
            #write out the table rows
            mandatoryvals = ['PARGPNME', 'INCTYP', 'DERINC', 'DERINCLB', 'FORCEN', 'DERINCMUL', 'DERMTHD']
            mandatorytypes = ['string','string','real','real','string','real','string']
            optionalvals = ['SPLITTHRESH', 'SPLITRELDIFF', 'SPLITACTION']
            optionaltypes = ['real','real','string']
            write_TAB_line(ofp,cdict,cblock,mandatoryvals,mandatorytypes,optionalvals,optionaltypes)
            
        # ###
        # Write out mandatory parameter data block
        # ###        
        cblock = 'parameter_data'
        cdict = self.tabblockdict[cblock]
        if len(cdict) == 0:
            raise(MissingBlockError(cblock))
        else:
            ofp.write('* parameter data\n')
            mandatoryvals = ['PARNME', 'PARTRANS', 'PARCHGLIM', 'PARVAL1', 'PARLBND', 'PARUBND', 'PARGP', 'SCALE', 'OFFSET', 'DERCOM']
            mandatorytypes = ['string','string','string','real','real','real','string','real','real','int','string']
            write_TAB_line(ofp,cdict,cblock,mandatoryvals,mandatorytypes)

        # ###
        # Write out optional parameter tied data block
        # ###        
        cblock = 'parameter_tied_data'
        cdict = self.tabblockdict[cblock]
        if len(cdict) == 0:
            pass
        else:
            mandatoryvals = ['PARNME', 'PARTIED']
            mandatorytypes = ['string','string']
            write_TAB_line(ofp,cdict,cblock,mandatoryvals,mandatorytypes)
        # ###
        # Write out mandatory observation groups block
        # ###        
        cblock = 'observation_groups'
        cdict = self.tabblockdict[cblock]
        if len(cdict) == 0:
            raise(MissingBlockError(cblock))
        else:
            ofp.write('* observation groups\n')
            mandatoryvals = ['OBGNME']
            mandatorytypes = ['string']
            optionalvals = ['GTARG', 'COVFLE']
            optionaltypes = ['real','string']
            write_TAB_line(ofp,cdict,cblock,mandatoryvals,mandatorytypes,optionalvals,optionaltypes)

        # ###
        # Write out mandatory observation data block
        # ###        
        cblock = 'observation_data'
        cdict = self.tabblockdict[cblock]
        if len(cdict) == 0:
            raise(MissingBlockError(cblock))
        else:
            ofp.write('* observation data\n')
            mandatoryvals = ['OBSNME', 'OBSVAL', 'WEIGHT', 'OBGNME']
            mandatorytypes = ['string','real','real','string']
            write_TAB_line(ofp,cdict,cblock,mandatoryvals,mandatorytypes)
            
        # ###
        # Write out optional derivatives command line block
        # ###
        cblock = 'derivatives_command_line'
        try:
            cdict = self.kwblocks[cblock].kwdict
            ofp.write('* derivatives command line\n')
            write_val(ofp,cdict['DERCOMLINE'],'string','DERCOMLINE',cblock)
            ofp.write('\n')
            write_val(ofp,cdict['EXTDERFLE'],'string','EXTDERFLE',cblock)
            ofp.write('\n')
        except KeyError:
            pass 

        # ###
        # Write out mandatory model command line block
        # ###        
        cblock = 'model_command_line'
        cdict = self.tabblockdict[cblock]
        if len(cdict) == 0:
            raise(MissingBlockError(cblock))
        else:
            ofp.write('* model command line\n')
            mandatoryvals = ['COMLINE']
            mandatorytypes = ['string']
            write_TAB_line(ofp,cdict,cblock,mandatoryvals,mandatorytypes)
            
        # ###
        # Write out mandatory model input/output block
        # ###        
        ofp.write('* model input/output\n')
        cblock = 'model_input'
        cdict = self.tabblockdict[cblock]
        if len(cdict) == 0:
            raise(MissingBlockError(cblock))
        else:
            mandatoryvals = ['TEMPFLE', 'INFLE']
            mandatorytypes = ['string','string']
            write_TAB_line(ofp,cdict,cblock,mandatoryvals,mandatorytypes)
        cblock = 'model_output'
        cdict = self.tabblockdict[cblock]
        if len(cdict) == 0:
            raise(MissingBlockError(cblock))
        else:
            mandatoryvals = ['INSFLE', 'OUTFLE']
            mandatorytypes = ['string','string']
            write_TAB_line(ofp,cdict,cblock,mandatoryvals,mandatorytypes)        

        # ###
        # Write out optional prior information block
        # ###        
        cblock = 'prior_information'
        cdict = self.tabblockdict[cblock]
        if len(cdict) == 0:
            pass
        else:
            ofp.write('* prior information\n')
            mandatoryvals = ['PILINES']
            mandatorytypes = ['string']
            write_TAB_line(ofp,cdict,cblock,mandatoryvals,mandatorytypes)
        
        # ###
        # Write out optional predictive analysis block
        # ###
        cblock = 'predictive_analysis'
        try:
            cdict = self.kwblocks[cblock].kwdict
            # write a line
            mandatoryvals = ['NPREDMAXMIN']
            mandatorytypes = ['int']
            optionalvals = ['PREDNOISE']
            optionaltypes = ['int']
            write_KW_line(ofp,cdict,cblock,mandatoryvals,mandatorytypes,optionalvals,optionaltypes)
            # write a line
            mandatoryvals = ['PD0', 'PD1', 'PD2']
            mandatorytypes = ['real','real','real']
            write_KW_line(ofp,cdict,cblock,mandatoryvals,mandatorytypes)
            # write a line
            mandatoryvals = ['ABSPREDLAM', 'RELPREDLAM', 'INITSCHFAC', 'MULSCHFAC', 'NSEARCH']
            mandatorytypes = ['real','real','real','real','int']
            write_KW_line(ofp,cdict,cblock,mandatoryvals,mandatorytypes)
            # write a line
            mandatoryvals = ['ABSPREDSWH', 'RELPREDSWH']
            mandatorytypes = ['real','real']
            write_KW_line(ofp,cdict,cblock,mandatoryvals,mandatorytypes)
            # write a line
            mandatoryvals = ['NPREDNORED', 'ABSPREDSTP', 'RELPREDSTP', 'NPREDSTP']
            mandatorytypes = ['int','real','real','int']
            write_KW_line(ofp,cdict,cblock,mandatoryvals,mandatorytypes)
        except KeyError:
            pass  
        # ###
        # Write out optional predictive analysis block
        # ###
        # here comes a bit of a kludge to handle multiple spellings of regularization/regularisation

        if (('regularization' in self.kwblocks.keys()) and ('regularisation' in self.kwblocks.keys())):
            raise(RegularizationDouleDipping('reg'))
        elif ('regularization' in self.kwblocks.keys()):
            cblock = 'regularization'
        elif ('regularisation' in self.kwblocks.keys()):
            cblock = 'regularisation'
        else:
            cblock = 0
        if cblock:
            cdict = self.kwblocks[cblock].kwdict
            ofp.write('* regularisation\n')
            # handle default values for PHIMLIM and PHIMACCEPT
            if cdict['PHIMLIM'] == UNINIT_REAL:
                cdict['PHIMLIM'] = self.kwblocks['control_data'].kwdict['NOBS']
            if cdict['PHIMACCEPT'] == UNINIT_REAL:
                cdict['PHIMACCEPT'] = float(cdict['PHIMLIM']) * 1.05                
            mandatoryvals = ['PHIMLIM', 'PHIMACCEPT']
            mandatorytypes = ['real','real']
            optionalvals = ['FRACPHIM', 'MEMSAVE']
            optionaltypes = ['real','string']
            # write a line         
            mandatoryvals = ['WFINIT', 'WFMIN', 'WFMAX']
            mandatorytypes = ['real','real', 'real']
            optionalvals = ['LINREG', 'REGCONTINUE']
            optionaltypes = ['string','string']
            write_KW_line(ofp,cdict,cblock,mandatoryvals,mandatorytypes,optionalvals,optionaltypes)
            # write a line
            mandatoryvals = ['WFFAC', 'WFTOL', 'IREGADJ']
            mandatorytypes = ['real','real', 'int']
            optionalvals = ['NOPTREGADJ', 'REGWEIGHTRAT', 'REGSINGTHRESH']
            optionaltypes = ['int','real','real']
            write_KW_line(ofp,cdict,cblock,mandatoryvals,mandatorytypes,optionalvals,optionaltypes)
        # ###
        # Write out optional pareto block
        # ###
        cblock = 'pareto'
        try:
            cdict = self.kwblocks[cblock].kwdict
            ofp.write('* pareto\n')
            # write a line
            mandatoryvals = ['PARETO_OBSGROUP']
            mandatorytypes = ['string']
            write_KW_line(ofp,cdict,cblock,mandatoryvals,mandatorytypes)
            # write a line
            mandatoryvals = ['PARETO_WTFAC_START', 'PARETO_WTFAC_FIN', 'NUM_WTFAC_INC']
            mandatorytypes = ['real','real','int']
            write_KW_line(ofp,cdict,cblock,mandatoryvals,mandatorytypes)
            # write a line
            mandatoryvals = ['NUM_ITER_START', 'NUM_ITER_GEN', 'NUM_ITER_FIN']
            mandatorytypes = ['int','int','int']
            write_KW_line(ofp,cdict,cblock,mandatoryvals,mandatorytypes)
            # write a line
            mandatoryvals = ['ALT_TERM']
            mandatorytypes = ['int']
            write_KW_line(ofp,cdict,cblock,mandatoryvals,mandatorytypes)
            try:
                cval = int(cdict['ALT_TERM'])
            except:
                raise(TypeFailError(cval,'ALT_TERM','int'))
            if cval != 0:
                # write a line
                mandatoryvals = ['OBS_TERM', 'ABOVE_OR_BELOW', 'OBS_THRESH', 'NUM_ITER_THRESH']
                mandatorytypes = ['string','string','real','int']
                write_KW_line(ofp,cdict,cblock,mandatoryvals,mandatorytypes)
            # write a line
            mandatoryvals = ['NOBS_REPORT']
            mandatorytypes = ['int']
            write_KW_line(ofp,cdict,cblock,mandatoryvals,mandatorytypes)
            try:
                cval = int(cdict['NOBS_REPORT'])
            except:
                raise(TypeFailError(cval,'NOBS_REPORT','int'))
            if cval > 0:
                mandatoryvals = []
                mandatorytypes = []
                for crep in xrange(cval):
                    mandatoryvals.append('OBS_REPORT_%d' %(crep+1))
                    mandatorytypes.append('string')
                write_KW_line(ofp,cdict,cblock,mandatoryvals,mandatorytypes)
        except KeyError:
            pass            
            
        # ###
        # Write out optional pest++ block
        # ###
        cblock = 'pest++'
        try:
            cdict = self.kwblocks[cblock].kwdict
            ofp.write('++# PEST++ section generated by keyPEST\n')            
        except KeyError:
            pass  
        if cdict['HOST'] == UNINIT_STRING:
            raise(DefaultValueError('HOST',cblock))
        else:
            chost = cdict['HOST']
        if cdict['PORT'] == UNINIT_INT:
            raise(DefaultValueError('PORT',cblock))
        else:
            try:
                cport = int(cdict['PORT'])
            except:
                raise(TypeFailError(cdict['PORT'],'PORT','int'))
        cdict['GMAN_SOCKET'] = str(chost) + ":" + str(cport)
        # write a line
        mandatoryvals = ['GMAN_SOCKET']
        mandatorytypes = ['string']
        ofp.write('++ ')
        write_KW_line_ppp(ofp,cdict,cblock,mandatoryvals,mandatorytypes)
        # write a line
        mandatoryvals = ['SUPER_NMAX','SUPER_EIGTHRES']
        mandatorytypes = ['int','real']
        ofp.write('++ ')
        write_KW_line_ppp(ofp,cdict,cblock,mandatoryvals,mandatorytypes)
        # write a line
        mandatoryvals = ['N_ITER_BASE','N_ITER_SUPER']
        mandatorytypes = ['int','int']
        ofp.write('++ ')
        write_KW_line_ppp(ofp,cdict,cblock,mandatoryvals,mandatorytypes)
                 
        # ######
        # CLOSE THE PST FILE
        # ######
        ofp.close()
        
# ###################################################### #
# DICTIONARY OF KEWYWORD BLOCK NAMES, PARS, AND DEFAULTS #
# ###################################################### #
kwblocks = {'control_data' : # ######################
            {'RSTFLE' : 'restart', 
             'PESTMODE' : 'estimation',
             'NPAR' : UNINIT_INT,
             'NOBS' : UNINIT_INT,
             'NPARGP' : UNINIT_INT,
             'NPRIOR' : UNINIT_INT, 
             'NOBSGP' : UNINIT_INT,
             'MAXCOMPDIM' : UNINIT_INT,
             'NTPLFLE' : UNINIT_INT,
             'NINSFLE' : UNINIT_INT,
             'PRECIS' : 'single',
             'DPOINT' : 'point',
             'NUMCOM' : UNINIT_INT,
             'JACFILE' : UNINIT_INT,
             'MESSFILE' : UNINIT_INT,
             'RLAMBDA1' : 20,
             'RLAMFAC' : -3,
             'PHIRATSUF' : 0.3,
             'PHIREDLAM' : 0.03,
             'NUMLAM' : 10,
             'JACUPDATE' : 999,
             'LAMFORGIVE' : 'lamforgive',
             'RELPARMAX' : UNINIT_REAL,
             'FACPARMAX' : UNINIT_REAL,
             'FACORIG' : UNINIT_REAL,
             'IBOUNDSTICK' : UNINIT_INT,
             'UPVECBEND' : UNINIT_INT,
             'PHIREDSWH' : UNINIT_REAL,
             'NOPTSWITCH' : UNINIT_INT,
             'SPLITSWH' : UNINIT_REAL,
             'DOAUI' : 'noaui',
             'DOSENREUSE' : 'senreuse',
             'NOPTMAX' : 25,
             'PHIREDSTP' : 0.005,
             'NPHISTP' : 4,
             'NPHINORED' : 4,
             'RELPARSTP' : 0.005,
             'NRELPAR' : 4,
             'PHISTOPTHRESH' : UNINIT_REAL,
             'LASTRUN' : 1,
             'PHIABANDON' : UNINIT_REAL,
             'ICOV' : 1,
             'ICOR' : 1,
             'IEIG' : 1,
             'IRES' : 1,
             'JCOSAVE' : 'jcosave',
             'VERBOSEREC' : 'verboserec',
             'JCOSAVEITN' : 'nojcosaveitn',
             'REISAVEITN' : 'reisaveitn',
             'PARSAVEITN' : 'parsaveitn'},
            'automatic_user_intervention' : # ######################
            {'MAXAUI' : UNINIT_INT,
             'AUISTARTOPT' : UNINIT_INT,
             'NOAUIPHIRAT' : UNINIT_REAL,
             'AUIRESTITN' : UNINIT_INT,
             'AUISENSRAT' : UNINIT_REAL,
             'AUIHOLDMAXCHG' : UNINIT_INT,
             'AUINUMFREE' : UNINIT_INT,
             'AUIPHIRATSUF' : UNINIT_REAL,
             'AUIPHIRATACCEPT' : UNINIT_REAL,
             'NAUINOACCEPT' : UNINIT_INT},
            'singular_value_decomposition' : # ######################
            {'SVDMODE': 1,
             'MAXSING' : UNINIT_INT, #SET DEFAULT AS NPAR
             'EIGTHRESH': 5.0e-7,
             'EIGWRITE' : 0},
            'lsqr' :
            {'LSQRMODE' : UNINIT_INT,
             'LSQR_ATOL' : UNINIT_REAL,
             'LSQR_BTOL' : UNINIT_REAL,
             'LSQR_CONLIM' : UNINIT_REAL,
             'LSQR_ITNLIM' : UNINIT_INT,
             'LSQRWRITE' : UNINIT_INT},
            'svd_assist' : # ######################
            {'BASEPESTFILE' : UNINIT_STRING,
             'BASEJACFILE' : UNINIT_STRING,
             'SVDA_MULBPA' : 1,
             'SVDA_SCALADJ' : UNINIT_INT,
             'SVDA_EXTSUPER' : UNINIT_INT,
             'SVDA_SUPDERCALC' : 1,
             'SVDA_PAR_EXCL' : UNINIT_INT},
            'sensitivity_reuse': # ######################
            {'SENRELTHRESH' : UNINIT_REAL,
             'SENMAXREUSE' : UNINIT_INT,
             'SENALLCALCINT' : UNINIT_INT,
             'SENPREDWEIGHT' : UNINIT_REAL,
             'SENPIEXCLUDE' : UNINIT_STRING},
            'derivatives_command_line': # ######################
            {'DERCOMLINE' : UNINIT_STRING,
             'EXTDERFLE' : UNINIT_STRING},
            'model_command_line' : # ######################
            {'NPREDMAXMIN' : UNINIT_INT,
             'PREDNOISE' : UNINIT_INT,
             'PD0' : UNINIT_REAL, 
             'PD1' : UNINIT_REAL, 
             'PD2' : UNINIT_REAL,
             'ABSPREDLAM' : UNINIT_REAL,
             'RELPREDLAM' : UNINIT_REAL,
             'INITSCHFAC' : UNINIT_REAL,
             'MULSCHFAC' : UNINIT_REAL,
             'NSEARCH' : UNINIT_INT,
             'ABSPREDSWH' : UNINIT_REAL,
             'RELPREDSWH' : UNINIT_REAL,
             'NPREDNORED' : UNINIT_INT,
             'ABSPREDSTP' : UNINIT_REAL,
             'RELPREDSTP' : UNINIT_REAL,
             'NPREDSTP' : UNINIT_INT},
            'regularisation' : # ######################
            # -- kludge here. Must ensure that 'regularization' data matches ' regularisation'
            {'PHIMLIM' : UNINIT_REAL, # SET DEFAULT AS NOBS
             'PHIMACCEPT' : UNINIT_REAL, # SET DEFAULT AS NOBS*1.05
             'FRACPHIM' : UNINIT_REAL, 
             'MEMSAVE' : 'nomemsave',
             'WFINIT' : 1.0, 
             'WFMIN' : 1.0e-10, 
             'WFMAX' : 1.0e+10, 
             'LINREG' : UNINIT_STRING, 
             'REGCONTINUE' : 'nocontinue',
             'WFFAC' : 1.3, 
             'WFTOL' : 1.0e-02, 
             'IREGADJ' : 1, 
             'NOPTREGADJ' : UNINIT_INT, 
             'REGWEIGHTRAT' : UNINIT_REAL, 
             'REGSINGTHRESH' : UNINIT_REAL},
            'regularization' : # ######################
            {'PHIMLIM' : UNINIT_REAL, # SET DEFAULT AS NOBS
             'PHIMACCEPT' : UNINIT_REAL, # SET DEFAULT AS NOBS*1.05
             'FRACPHIM' : UNINIT_REAL, 
             'MEMSAVE' : 'nomemsave',
             'WFINIT' : 1.0, 
             'WFMIN' : 1.0e-10, 
             'WFMAX' : 1.0e+10,
             'LINREG' : UNINIT_STRING, 
             'REGCONTINUE' : 'nocontinue',
             'WFFAC' : 1.3, 
             'WFTOL' : 1.0e-02, 
             'IREGADJ' : 1, 
             'NOPTREGADJ' : UNINIT_INT, 
             'REGWEIGHTRAT' : UNINIT_REAL, 
             'REGSINGTHRESH' : UNINIT_REAL},
            'predictive_analysis': # ################
            {'NPREDMAXMIN' : UNINIT_INT,
             'PREDNOISE' : UNINIT_INT,
             'PD0' : UNINIT_REAL,
             'PD1' : UNINIT_REAL,
             'PD2' : UNINIT_REAL,
             'ABSPREDLAM' : UNINIT_REAL,
             'RELPREDLAM' : UNINIT_REAL,
             'INITSCHFAC' : UNINIT_REAL,
             'MULSCHFAC' : UNINIT_REAL,
             'NSEARCH' : UNINIT_INT,
             'ABSPREDSWH' : UNINIT_REAL,
             'RELPREDSWH' : UNINIT_REAL,
             'NPREDNORED' : UNINIT_INT,
             'ABSPREDSTP' : UNINIT_REAL,
             'RELPREDSTP' : UNINIT_REAL,
             'NPREDSTP' : UNINIT_INT},
            'pareto' : # ######################
            {'PARETO_OBSGROUP' : UNINIT_STRING,
             'PARETO_WTFAC_START' : UNINIT_REAL, 
             'PARETO_WTFAC_FIN' : UNINIT_REAL, 
             'NUM_WTFAC_INC' : UNINIT_INT,
             'NUM_ITER_START' : UNINIT_INT, 
             'NUM_ITER_GEN' : UNINIT_INT, 
             'NUM_ITER_FIN' : UNINIT_INT,
             'ALT_TERM' : 0,
             'OBS_TERM' : UNINIT_REAL, 
             'ABOVE_OR_BELOW' : UNINIT_STRING, 
             'OBS_THRESH' : UNINIT_REAL, 
             'NUM_ITER_THRESH' : UNINIT_INT, 
             'NOBS_REPORT' : UNINIT_STRING},
            'pest++' : # ##################
            {'GMAN_SOCKET' : UNINIT_STRING,
             'HOST' : UNINIT_STRING,
             'PORT' : UNINIT_INT,
             'N_ITER_BASE' : UNINIT_INT,
             'N_ITER_SUPER' : UNINIT_INT,
             'SUPER_EIGTHRES' : 5.0E-07,
             'SUPER_NMAX' : UNINIT_INT
             }}


# ################################################# #
# DICTIONARY OF TABLE BLOCK NAMES WITH COLUMN NAMES #
# ################################################# #
tabblocks = {'parameter_groups' : # ######################
             ['PARGPNME', 'INCTYP', 'DERINC', 'DERINCLB', 'FORCEN', 
              'DERINCMUL', 'DERMTHD', 'SPLITTHRESH', 'SPLITRELDIFF', 'SPLITACTION'],
             'parameter_data' : # ######################
             ['PARNME', 'PARTRANS', 'PARCHGLIM', 'PARVAL1', 'PARLBND', 
              'PARUBND', 'PARGP', 'SCALE', 'OFFSET', 'DERCOM'],
             'parameter_tied_data' : # ######################
             ['PARNME', 'PARTIED'],
             'observation_groups' : # ######################
             ['OBGNME', 'GTARG', 'COVFLE'],
             'observation_data' : # ######################
             ['OBSNME', 'OBSVAL', 'WEIGHT', 'OBGNME'],
             'model_command_line' : # ######################
             ['COMLINE'],
             'model_input' : # ######################
             ['TEMPFLE', 'INFLE'],
             'model_output' : # ######################
             ['INSFLE', 'OUTFLE'],
             'prior_information' : # ######################
             ['PILINES']}
tabblockdicts = {'parameter_groups' : # ######################
                 dict(),
                 'parameter_data' : # ######################
                 dict(),
                 'parameter_tied_data' : # ######################
                 dict(),
                 'observation_groups' : # ######################
                 dict(),
                 'observation_data' : # ######################
                 dict(),
                 'model_command_line' : # ######################
                 dict(),
                 'model_input' : # ######################
                 dict(),
                 'model_output' : # ######################
                 dict(),
                 'prior_information' : # ######################
                 dict()}
# ############# #
# Error classes # 
# ############# #

# -- illegal syntax on a block definition line
class BlockSyntaxError(Exception):
    def __init__(self,cline):
        self.value = cline
    def __str__(self):
        return('\n\nBlock input syntax ERROR: Illegal word on line: ' + str(self.value+1))

# -- illegal block name
class BlockNameError(Exception):
    def __init__(self,cline,cname):
        self.value = cline
        self.cname = cname
    def __str__(self):
        return('\n\nBlock name ERROR: Illegal blockname "' + self.cname + '" on line: ' + str(self.value+1))



# -- duplicate block names used
class BlockDuplicate(Exception):
    def __init__(self,dupes):
        self.dupes = dupes
    def __str__(self):
        print "\n\nBlockDuplicate ERROR: The following block names are used more than once:"
        for i in self.dupes:
            print i
        return

# -- mismatched begin and end 1
class BlockMismatchNoEND(Exception):
    def __init__(self,blname):
        self.blname = blname
    def __str__(self):
        print '\n\nBlockMismatch ERROR: Block "' + self.blname + '" BEGINS without END'
        return
# -- mismatched begin and end 1
class BlockReversed(Exception):
    def __init__(self,blname):
        self.blname = blname
    def __str__(self):
        return( '\n\nBlockReversed ERROR: Block "' + self.blname + '" has BEGIN and END reversed')
# -- mismatched begin and end 2
class BlockMismatchNoBEGIN(Exception):
    def __init__(self,blname):
        self.blname = blname
    def __str__(self):
        print '\n\nBlockMismatch ERROR: Block "' + self.blname + '" ENDS without BEGIN'
        return
# -- nested blocks
class BlockIllegalNesting(Exception):
    def __init__(self,blockin,blockout):
        self.blockin = blockin
        self.blockout = blockout
    def __str__(self):
        return('\n\nBlockNesting ERROR: \nblock "' + 
               self.blockin + '" is inside block "' + self.blockout + '"')
# -- nested blocks
class KeywordBlockError(Exception):
    def __init__(self,blockname):
        self.blockname = blockname
    def __str__(self):
        return('\n\nKeyword Block ERROR: \nIn block "' + 
               self.blockname + '" Unbalanced keywords and values')
# -- bad table header
class TableBlockHeaderError(Exception):
    def __init__(self,cline):
        self.value = cline
    def __str__(self):
        print('\n\nTable Block Header Error: \n' +
              'Table header row contains errors on line: ' + str(self.value))
        return 
# -- wrong number of rows
class TableBlockRowError(Exception):
    def __init__(self,blockname,nrow,nrowtrue):
        self.blockname = blockname
        self.nrow = nrow
        self.nrowtrue = nrowtrue
    def __str__(self):
        return('\n\nTable Block Rows Error: \n' +
               'Table header indicates ' + str(self.nrow) + ' rows expected.\n' + 
               str(self.nrowtrue) + ' rows found in block "' + self.blockname + '"')
# -- wrong number of columns
class TableBlockColError(Exception):
    def __init__(self,blockname,cline,ncol,ncoltrue):
        self.blockname = blockname
        self.cline = cline
        self.ncol = ncol
        self.ncoltrue = ncoltrue
    def __str__(self):
        return('\n\nTable Block Columns Error: \n' +
               'Table header indicates ' + str(self.ncol) + ' columns expected.\n' + 
               str(self.ncoltrue) + ' columns found on line ' + str(self.cline) + ' of block "' + self.blockname + '"')
# -- Table block is empty
class TableBlockEmpty(Exception):
    def __init__(self,blockname,cline):
        self.blockname = blockname
        self.cline = cline
    def __str__(self):
        return('\n\nTable Block Empty Error: \n' +
               'Table Block "' + self.blockname + '" is empty. See line: '+ str(self.cline))
# -- Keyword block is empty
class KeywordBlockEmpty(Exception):
    def __init__(self,blockname,cline):
        self.blockname = blockname
        self.cline = cline
    def __str__(self):
        return('\n\nTable Block Empty Error: \n' +
               'Table Block "' + self.blockname + '" is empty. See line: '+ str(self.cline))
# -- type mismatch
class TypeFailError(Exception):
    def __init__(self,cval,parnme,cvaltype):
        self.cval = cval
        self.parnme = parnme
        self.cvaltype = cvaltype
    def __str__(self):
        return('\n\nVariable type mismatch: \n' +
               'Variable ' + self.parnme + ' should be of type: ' + self.cvaltype +
               '\nThe value provided is: "' + str(self.cval) + '"')
# -- no value provided
class DefaultValueError(Exception):
    def __init__(self,parnme,block):
        self.parnme = parnme
        self.block = block
    def __str__(self):
        return('\n\nNo Value was provided for variable: "' + self.parnme +
               '" in block: "' + self.block+ '"\n' +
               'This variable has no default value.')
# -- illegal column label in a table block
class BlockIllegalColumn(Exception):
    def __init__(self,block,col):
        self.blockname = block
        self.keyval = col
    def __str__(self):
        return('\n\nColumn Label "' + self.keyval + '" is not allowed in block "' + self.blockname)
# -- missing required block
class MissingBlockError(Exception):
    def __init__(self,block):
        self.blockname = block
    def __str__(self):
        return('\n\nRequired Block "' + self.block + '" is missing')    
# -- regularization double-dipping
class RegularizationDouleDipping(Exception):
    def __init__(self,block):
        self.blockname = block
    def __str__(self):
        return('\n\nBoth "regularization" and "regularisation" blocks found.\nChoose one spelling option only!') 
# -- multiple file names in a file block
class ExternalFileError(Exception):
    def __init__(self,fileblock,cblock):
        self.fileblock = fileblock
        self.blockname = cblock
    def __str__(self):
        blockstr = ''
        for i in self.fileblock:
            blockstr += i.strip() + '\n'
        return('\n\nToo many filenames in block: ' + self.blockname + '\n' + blockstr) 
# -- can't open external file
class ExternalFileOpenError(Exception):
    def __init__(self,filename,cblock):
        self.filename = filename.strip()
        self.blockname = cblock
    def __str__(self):
        return('\n\nCannot open external file: ' + self.filename + ' for block: ' + self.blockname + '\n' ) 
# -- no comments allowed in table blocks
class TableCommentError(Exception):
    def __init__(self,cline,cblock):
        self.cline = cline
        self.cblock = cblock
    def __str__(self):
        return('\n\nComments are not allowed in Table blocks.\nSee line ' + 
               str(self.cline) + ' in block: ' + self.cblock + '\n')

# -- no comments allowed in table blocks
class InvalidInputExtension(Exception):
    def __init__(self,filename):
        self.cfile = filename
    def __str__(self):
        return('\n\nInvalid input filename: ' + self.cfile + '\nFile should be of format <casename>.key\n')
