import sys
import os
import datetime as dt
import subprocess
import pylab
from pylab import *
import numpy as np
from scikits import delaunay as dlny
import MFArrayUtil as au
import MFInterpolators as mfintrp
import shapefile as sf

#import scipy
#from scipy.io import netcdf as nc
import MFArrayUtil as au

from Scientific.IO.NetCDF import NetCDFFile

#-Figure defaults
import matplotlib as mpl
from matplotlib.font_manager import FontProperties
mpl.rcParams['font.sans-serif']          = 'Univers 57 Condensed'
mpl.rcParams['font.serif']               = 'Times'
mpl.rcParams['font.cursive']             = 'Zapf Chancery'
mpl.rcParams['font.fantasy']             = 'Comic Sans MS'
mpl.rcParams['font.monospace']           = 'Courier New'
mpl.rcParams['pdf.compression']          = 0
mpl.rcParams['pdf.fonttype']             = 42
ticksize = 6
mpl.rcParams['font.size']        = 8
mpl.rcParams['legend.fontsize']  = 6
mpl.rcParams['axes.labelsize']   = 8
mpl.rcParams['axes.titlesize']   = 8
mpl.rcParams['xtick.labelsize']  = ticksize
mpl.rcParams['ytick.labelsize']  = ticksize
mpl.rcParams['contour.negative_linestyle'] = 'solid'


def eqfwh( rho, h, z ):
    zt = z
    if h < z:
        zt = h
    hf = ( rho / 1000. ) * h - ( ( rho - 1000. ) / 1000. ) * zt
    return hf

def SetBoundary(nrow,ncol,ib,top,mf_stage):
    mf_bnd = np.zeros( (nrow,ncol), np.int )
    ntghb = 0
    ntdrn = 0
    for irow in range(0,nrow):
        for icol in range(0,ncol):
            icode = ib[irow,icol]
            if icode < 2:
                continue
            te = top[irow,icol]
            tib = icode
            if mf_stage[irow,icol] == te:
                ntdrn += 1
                #tib = -icode
                tib = -1
            else:
                ntghb += 1
                tib = 1
                if icode == 3:
                    tib = 2
                elif icode == 4:
                    tib = 3
            mf_bnd[irow,icol] = tib
    return ntghb,ntdrn,mf_bnd

def WriteData(tdf,tgf,nghb,ighbl,mf_bnd,top,mf_stage,r_coast,r_tp_ret,r_tp_dis):
    for ibnd in range(0,nghb):
        ilay  = 1
        icol  = int( ighbl[ibnd,0] )
        irow  = int( ighbl[ibnd,1] )
        icode = mf_bnd[irow,icol]
        acode = abs( icode )
        te    = top[irow,icol]
        rraw  = mf_stage[irow,icol]
        r     = rraw
        ctag  = ''
        if acode == 2 or acode == 6:
            #--equivalent freshwater head at the top of the aquifer
            r    = eqfwh( 1025., r_coast, te )
            ctag = 'S123_T'
        elif acode== 3:
            #--equivalent freshwater head at the top of the aquifer
            r    = eqfwh( 1025., r_tp_ret, te )
            ctag = 'S123_T_TP_RETURN'
        elif acode == 4:
            #--equivalent freshwater head at the top of the aquifer
            r    = eqfwh( 1025., r_tp_dis, te )
            ctag = 'S123_T_TP_DISCHARGE'
        elif acode == 5:
            ctag = 'EDEN'
        #--write data
        if icode > 0:
            cval = '% 9i %9i %9i %9.5f %9.3g  #--%s\n' % ( ilay, irow+1, icol+1, r, cond, ctag ) 
            tgf.write( cval )
        else:
            cval = '% 9i %9i %9i %9.5f %9.3g  %s\n' % ( ilay, irow+1, icol+1, te, cond, ctag) 
            tdf.write( cval )
    return True


#--main script
cpath2mod = '..\\..\\UMD.01\\'
KeepAllPng  = False
MakeImages  = False
MakeMFFiles = False
maxdays = 0

shape_name = 'D:\\Data\\Users\\jdhughes\\GIS\\Project Data\\2080DBF00\\Spatial\\FigureData\\BaseMap'
hydrography = sf.load_shape_list(shape_name)

figuresize = [4.4,6]

#--get command line arguments
narg = len(sys.argv)
iarg = 0
if narg > 1:
    while iarg < narg-1:
        iarg += 1
        basearg = sys.argv[iarg].lower()
        if basearg == '-maxdays':
            try:
                iarg += 1
                maxdays = int( sys.argv[iarg] )
                print 'command line arg: maxdays = ', maxdays
            except:
                print 'cannot parse command line arg: maxdays'
        elif basearg == '-keepallpng':
            KeepAllPng = True
        elif basearg == '-makeimages':
            MakeImages = True
        elif basearg == '-makemffiles':
            MakeMFFiles = True
        elif basearg == '-all':
            MakeImages = True
            MakeMFFiles = True

if MakeImages == False:
    KeepAllPng = True

if MakeImages == False and MakeMFFiles == False:
    print 'Error: nothing to do - MakeImages and MakeMFFiles are false.'
    sys.exit()

print 'MakeMFFiles {0}'.format( MakeMFFiles )
print 'MakeImages  {0}'.format( MakeImages  )
print 'KeepAllPng  {0}'.format( KeepAllPng  )


#--UMD dimensions
nrow   = 189
ncol   = 101
dx     = 500.
scale  = 1.0 / 3.28081
cond   = 5. * scale * dx * dx / 1.

#--simulation start time
start_date = dt.datetime(year=1996,month=1,day=1,hour=12)

#--initialize average data value
r_avgcoast = 0.0
r_avgtp_ret   = 0.0
r_avgtp_dis   = 0.0
#--calculate grid dimensions
dx = dy = 500.
offset  = np.array( [539750., 2785750.] )
xlen    = float( ncol ) * dx
ylen    = float( nrow ) * dx
delr    = np.zeros((ncol),'float')
delc    = np.zeros((nrow),'float')
xcell   = np.zeros((ncol),'float')
ycell   = np.zeros((nrow),'float')
#--cell dimensions
for i in range(0,ncol):
    delr[i] = dx
for i in range(0,nrow):
    delc[i] = dy
#--node coordinates
xcell[0] = offset[0] + delr[0] / 2.0
for i in range(1,ncol):
    xcell[i] = xcell[i-1] + ( delr[i-1] + delr[i] ) / 2.0
ycell[0] = offset[1] + delc[0] / 2.0
for i in range(1,nrow):
    ycell[i] = ycell[i-1] + ( delc[i-1] + delc[i] ) / 2.0
ycell = ycell[::-1]
#--setup mesh grid for interpolation
X,Y = np.meshgrid(xcell,ycell)
#extent
im_extent = [xcell.min(), xcell.max(), ycell.min(), ycell.max() ]

#--ibound
ib_ref   = cpath2mod + 'REF\\UMD_IBOUND.ref'
ib = au.loadArrayFromFile(nrow,ncol,ib_ref)
#--topography
top_ref = cpath2mod + '\REF\\UMD_URBAN_EDEN_TOPO.ref'
top = au.loadArrayFromFile(nrow,ncol,top_ref)
#--array for storing calculated mf boundary type and stage data
mf_bnd      = np.zeros( (nrow,ncol), np.float )
mf_stage    = np.zeros( (nrow,ncol), np.float )
mf_avgstage = np.zeros( (nrow,ncol), np.float )

#--set up interpolation factors for coastal area
#--filter out elevations exceeding max_elev and interpolate 
#  in filtered locations using closes data point
ipos = 0
for irow in range(0,nrow):
    for icol in range(0,ncol):
        if ib[irow,icol] != 6:
            if ipos == 0:
                Xpts = np.zeros( (1), np.float )
                Ypts = np.zeros( (1), np.float )
                Xpts[0] = X[irow,icol]
                Ypts[0] = Y[irow,icol]
            else:
                Xpts = np.append(Xpts,X[irow,icol])
                Ypts = np.append(Ypts,Y[irow,icol])
        ipos += 1
#--set up factors triangulate data
tri = dlny.Triangulation(Xpts,Ypts)

#--create structure for ghbs
nghb = 0
ighbl = []
ib_ghb = np.arange(2,7,1)
for i in ib_ghb:
    for irow in range(0,nrow):
        for icol in range(0,ncol):
            if ib[irow,icol] == i:
                t = np.zeros( (3), np.float )
                t[0] = icol
                t[1] = irow
                t[2] = i
                ighbl.append( t )
                nghb += 1
ighbl = np.array( ighbl )

#--read data for coastal areas
cghb_dat = 'S123_T.csv'
ighbt = np.genfromtxt( cghb_dat, skip_header=1, delimiter=',' )
nghbt = ighbt.shape[0]
#--adjust NVGD29 to NAVD88 and scale from ft to m
for iday in range(0,nghbt):
    #coast
    ighbt[iday,1] = ( ighbt[iday,1]  - 1.53 ) * scale

#--check length of maxdays
if maxdays == 0:
    maxdays = nghbt
if maxdays > nghbt:
    maxdays = nghbt

#--get base eden data
#--netcdf file base information for stages
syear = 1996
sqtr  = 1
cdir = 'D:\\Data\\Users\\jdhughes\\GIS\\Original Data\\EDEN\\surface_netcdf\\'
cfile = '{0}_q{1}.nc'.format( syear, sqtr )
#--get dimensions and coordinates of the netcdf files
f = NetCDFFile(cdir+cfile, 'r')
#variableNames = f.variables.keys() 
#print variableNames
d = f.variables['x']
eden_ncol = d.shape[0]
eden_x = np.copy( d )
print 'X units: ', d.units, 'X size: ', eden_ncol
#print eden_x
d = f.variables['y']
eden_nrow = d.shape[0]
eden_y = np.copy( d )
eden_y = eden_y[::-1]
print 'Y units: ', d.units, 'Y size: ', eden_nrow
#print eden_y
eden_dx = eden_dy = 400. #m
stage = f.variables['stage']
s = np.copy( stage[0,:,:] )
s = np.flipud( s )
s = np.ma.masked_invalid( s )
eden_mask = np.ma.getmask( s )
#print eden_mask
f.close()
#--load eden topo data
eden_topo_ref   = '..\\Topography\\ref\\eden_topo.ref'
eden_topo = au.loadArrayFromFile(eden_nrow,eden_ncol,eden_topo_ref)
eden_topo = np.ma.masked_where(eden_topo==-9999.,eden_topo)

#--find the netcdf cell nw of modflow cells
eden2mf_col = np.zeros( (ncol), np.int )
eden2mf_row = np.zeros( (nrow), np.int )
for icol in range(0,ncol):
    x = xcell[icol]
    ix = 0
    for xe in eden_x:
        if xe > x:
            break
        ix += 1
    eden2mf_col[icol] = ix - 1
for irow in range(0,nrow):
    y = ycell[irow]
    iy = 0
    for ye in eden_y:
        if ye < y:
            break
        iy += 1
    eden2mf_row[irow] = iy - 1

#--read transient netcdf data and create dataset for ghb and drains
#maxdays = 10
#maxdays = 365 * 2

if MakeMFFiles == True:
    fdrn = cpath2mod + 'UMD.drn'
    fghb = cpath2mod + 'UMD.ghb'
    df = open(fdrn,'w')
    gf = open(fghb,'w')
    #--dataset 0
    cval = '#UMD DRN package from {0} - Created on {1}\n'.format( sys.argv[0], dt.datetime.today() )
    df.write(cval)
    cval = '#UMD GHB package from {0} - Created on {1}\n'.format( sys.argv[0], dt.datetime.today() )
    gf.write(cval)
    #--dataset 1
    cval = '%10i        50  NOPRINT\n' % (nghb)
    df.write(cval)
    gf.write(cval)


eden_iday = 0
for iday in range(0,maxdays):
    ondate = start_date + dt.timedelta(days=iday)
    ftitle = '{0}'.format( ondate )
    #--open netcdf file
    if eden_iday == 0:
        cfile = '{0}_q{1}.nc'.format( syear, sqtr )
        print 'reading...{0}'.format( cfile )
        f = NetCDFFile(cdir+cfile, 'r')
        d = f.variables['time']
        eden_idays = d.shape[0]
        d = f.variables['x']
        eden_tcol = d.shape[0]
        d = f.variables['y']
        eden_trow = d.shape[0]
        if eden_tcol != eden_ncol or eden_trow != eden_nrow:
            print 'dimensions of the netcdf files are not equal.'
            break
        stage = f.variables['stage']
    print 'Year {0:4d} Quarter {1:1d} Day {2:3d}/{3:3d} -- Total days {4:5d}/{5:5d}'.format( syear, sqtr, eden_iday+1, eden_idays, iday+1, maxdays )
    eden_s = np.copy( stage[eden_iday,:,:] ) / 100.
    eden_s = np.flipud( eden_s )
    eden_s[ eden_mask ] = -0.0

    #--plot raw eden stage data and calculated depth data
    if MakeImages == True:
        temp  = np.ma.masked_where(eden_mask==True,eden_s)
        fout = 'Figures_Eden\\EDEN_RAW_{0:05d}'.format( iday + 1 )
        print 'writing...{0}'.format( fout )
        au.plotimage( temp, vmin=-1, vmax=6, text=ftitle, fout=fout, addcolorbar='vertical', figuresize=figuresize )
        #au.plotgrid( eden_x, eden_y, temp, vmin=-1, vmax=6, text=ftitle, fout=fout, addcolorbar='vertical', figuresize=figuresize )
        temp  = np.ma.masked_where(eden_mask==True,eden_s-eden_topo)
        fout = 'Figures_Eden\\EDEN_DEPTH_{0:05d}'.format( iday + 1 )
        print 'writing...{0}'.format( fout )
        au.plotimage( temp, vmin=0, vmax=2, text=ftitle, fout=fout, addcolorbar='vertical', figuresize=figuresize )
        #au.plotgrid( eden_x, eden_y, temp, vmin=0, vmax=2, text=ftitle, fout=fout, addcolorbar='vertical', figuresize=figuresize )
    
    #--interpolate netcdf data to appropriate modflow cells
    for irow in range(0,nrow):
        for icol in range(0,ncol):
            if ib[irow,icol] != 5:
                continue
            x = xcell[icol]
            y = ycell[irow]
            eden_tcol = eden2mf_col[icol]
            eden_trow = eden2mf_row[irow]
            if (eden_tcol+1)==eden_ncol or (eden_trow+1)==eden_nrow:
                continue
            d = []
            for iy in range(eden_trow,eden_trow+2):
                for ix in range(eden_tcol,eden_tcol+2):
                    t = [ eden_x[ix], eden_y[iy], eden_s[iy,ix] ]
                    d.append( t )
            te = top[irow,icol]
            mf_stage[irow,icol] = max( mfintrp.bilinear_interpolation( x, y, d ), te )
    
    #--add time series data
    r_coast  = ighbt[iday,1]
    r_tp_ret = ighbt[iday,1] - 0.11
    r_tp_dis = ighbt[iday,1] + 0.19
    r_avgcoast  += r_avgcoast / float( maxdays )
    r_avgtp_ret += r_avgtp_ret / float( maxdays )
    r_avgtp_dis += r_avgtp_dis / float( maxdays )
    for irow in range(0,nrow):
        for icol in range(0,ncol):
            icode = ib[irow,icol]
            if icode < 2 or icode > 4:
                continue
            te = top[irow,icol]
            r = 0.0
            if icode == 2:
                r = max( r_coast, te )
            elif icode == 3:
                r = r_tp_ret
            elif icode == 4:
                r = r_tp_dis
            mf_stage[irow,icol] = r
   
    #--filter out stages in boundary area 6 and interpolate 
    #  in filtered locations using closest data points from
    #  eden and coastal data
    ipos = 0
    for irow in range(0,nrow):
        for icol in range(0,ncol):
            if ib[irow,icol] != 6:
                if ipos == 0:
                    temp = np.zeros( (1), np.float )
                    temp[0] = mf_stage[irow,icol]
                else:
                    temp = np.append(temp,mf_stage[irow,icol])
            ipos += 1
    #--interpolate data
    interp = tri.nn_interpolator(temp)
    mf_stage = interp(X, Y)
    #--make sure interpolated points are greater than the lse
    for irow in range(0,nrow):
        for icol in range(0,ncol):
            if ib[irow,icol] != 6:
                continue
            te = top[irow,icol]
            if mf_stage[irow,icol] < te:
                mf_stage[irow,icol] = te
    
    #--calculate average stage
    for irow in range(0,nrow):
        for icol in range(0,ncol):
            mf_avgstage[irow,icol] += mf_stage[irow,icol] / float( maxdays )

    #--set boundary type for current day
    ntghb,ntdrn,mf_bnd = SetBoundary(nrow,ncol,ib,top,mf_stage)
#    ntghb = 0
#    ntdrn = 0
#    for irow in range(0,nrow):
#        for icol in range(0,ncol):
#            icode = ib[irow,icol]
#            if icode < 2:
#                continue
#            te = top[irow,icol]
#            tib = icode
#            if mf_stage[irow,icol] == te:
#                ntdrn += 1
#                #tib = -icode
#                tib = -1
#            else:
#                ntghb += 1
#                tib = 1
#                if icode == 3:
#                    tib = 2
#                elif icode == 4:
#                    tib = 3
#            mf_bnd[irow,icol] = tib
    
    #--write data to ghb and drn files
    if MakeMFFiles == True:
        #--write header for drn and ghb files   
        #--drn
        cval = '{0:10d}         0          #STRESS PERIOD {1:05d}\n'.format( ntdrn, iday+1 )
        df.write(cval)
        cdrnlstd = 'BNDLIST\\DRN\\UMD_DRN_{0:04d}{1:02d}{2:02d}.dat'.format( ondate.year, ondate.month, ondate.day )
        cdrnlstf = cpath2mod + cdrnlstd
        if ntdrn > 0:
            cval = 'OPEN/CLOSE {0}\n'.format( cdrnlstd )
            df.write(cval)
        tdf = open(cdrnlstf,'w')
        #--ghb
        cval = '{0:10d}         0          #STRESS PERIOD {1:05d}\n'.format( ntghb, iday+1 )
        gf.write(cval)
        cghblstd = 'BNDLIST\\GHB\UMD_GHB_{0:04d}{1:02d}{2:02d}.dat'.format( ondate.year, ondate.month, ondate.day )
        cghblstf = cpath2mod + cghblstd
        if ntghb > 0:
            cval = 'OPEN/CLOSE {0}\n'.format( cghblstd )
            gf.write(cval)
        tgf = open(cghblstf,'w')
        #--write data for drains and ghbs
        success = WriteData(tdf,tgf,nghb,ighbl,mf_bnd,top,mf_stage,r_coast,r_tp_ret,r_tp_dis)
#        for ibnd in range(0,nghb):
#            ilay  = 1
#            icol  = int( ighbl[ibnd,0] )
#            irow  = int( ighbl[ibnd,1] )
#            icode = mf_bnd[irow,icol]
#            acode = abs( icode )
#            te    = top[irow,icol]
#            rraw  = mf_stage[irow,icol]
#            r     = rraw
#            ctag  = ''
#            if acode == 2 or acode == 6:
#                #--equivalent freshwater head at the top of the aquifer
#                r    = eqfwh( 1025., r_coast, te )
#                ctag = 'S123_T'
#            elif acode== 3:
#                #--equivalent freshwater head at the top of the aquifer
#                r    = eqfwh( 1050., r_tp_ret, te )
#                ctag = 'S123_T_TP_RETURN'
#            elif acode == 4:
#                #--equivalent freshwater head at the top of the aquifer
#                r    = eqfwh( 1050., r_tp_dis, te )
#                ctag = 'S123_T_TP_DISCHARGE'
#            elif acode == 5:
#                ctag = 'EDEN'
#            #--write data
#            if icode > 0:
#                #cval = '% 9i %9i %9i %9.5f %9.3g  #--%s  %9.3g   %9.3g\n' % ( ilay, irow+1, icol+1, r, cond, ctag, rraw, te ) 
#                cval = '% 9i %9i %9i %9.5f %9.3g  #--%s\n' % ( ilay, irow+1, icol+1, r, cond, ctag ) 
#                tgf.write( cval )
#            else:
#                cval = '% 9i %9i %9i %9.5f %9.3g  %s\n' % ( ilay, irow+1, icol+1, te, cond, ctag) 
#                tdf.write( cval )
        #--close temporary drn and ghb list files
        tdf.close()
        tgf.close()
    
    #--plot boundary type for UMD model grid
    if MakeImages == True:
        temp  = np.ma.masked_where(ib<2,mf_bnd)
        fout = 'Figures\\BND_TYPE_{0:05d}'.format( iday + 1 )
        print 'writing...{0}'.format( fout )
        au.plotimage( temp, vmin=-3, vmax=3, extent=im_extent, text=ftitle, fout=fout, addcolorbar='vertical', interpolation=None, polyline=hydrography, figuresize=figuresize )
        #au.plotgrid( xcell, ycell, temp, vmin=-3, vmax=3, text=ftitle, fout=fout, addcolorbar='vertical', polyline=hydrography, figuresize=figuresize )
        #--plot eden data interpolated to UMD model grid
        temp  = np.ma.masked_where(ib<2,mf_stage)
        fout = 'Figures\\BND_STAGE_{0:05d}'.format( iday + 1 )
        print 'writing...{0}'.format( fout )
        au.plotimage( temp, vmin=-1, vmax=5, extent=im_extent, text=ftitle, fout=fout, addcolorbar='vertical', interpolation=None, polyline=hydrography, figuresize=figuresize )
        #au.plotgrid( xcell, ycell, temp, vmin=-1, vmax=5, text=ftitle, fout=fout, addcolorbar='vertical', polyline=hydrography, figuresize=figuresize )
        #--plot water depth for UMD model grid
        temp  = np.ma.masked_where(ib<2,mf_stage-top)
        fout = 'Figures\\BND_DEPTH_{0:05d}'.format( iday + 1 )
        print 'writing...{0}'.format( fout )
        au.plotimage( temp, vmin=-2, vmax=2, extent=im_extent, text=ftitle, fout=fout, addcolorbar='vertical', interpolation=None, polyline=hydrography, figuresize=figuresize )
        #au.plotgrid( xcell, ycell, temp, vmin=-2, vmax=2, text=ftitle, fout=fout, addcolorbar='vertical', polyline=hydrography, figuresize=figuresize )
    
    eden_iday += 1
    if eden_iday == eden_idays:
        eden_iday = 0
        #--close the current netcdf file
        print 'closing...{0}'.format( cfile )
        f.close()
        sqtr += 1
        if sqtr > 4:
            sqtr = 1
            syear += 1

#--clean up -- close netcdf file if not already closed
if eden_iday > 0:
    f.close()

#--close ghb and drn file
if MakeMFFiles == True:
    df.close()
    gf.close()

#--make average boundary array from average stage
ntghb,ntdrn,mf_bnd = SetBoundary(nrow,ncol,ib,top,mf_avgstage)
#--make average ghb and drn files
if MakeMFFiles == True:

    fdrn = cpath2mod + 'UMD_{0}-{1}.drn'.format( start_date.year, ondate.year )
    fghb = cpath2mod + 'UMD_{0}-{1}.ghb'.format( start_date.year, ondate.year )
    df = open(fdrn,'w')
    gf = open(fghb,'w')
    #--dataset 0
    cval = '#UMD Average DRN package from {0} - Created on {1}\n'.format( sys.argv[0], dt.datetime.today() )
    df.write(cval)
    cval = '#UMD Average GHB package from {0} - Created on {1}\n'.format( sys.argv[0], dt.datetime.today() )
    gf.write(cval)
    #--dataset 1
    cval = '%10i        50  NOPRINT\n' % (nghb)
    df.write(cval)
    gf.write(cval)

    #--write header for drn and ghb files   
    #--drn
    cval = '{0:10d}         0          #STRESS PERIOD {1:05d} {2}-{3}\n'.format( ntdrn, 1, start_date.year, ondate.year  )
    df.write(cval)
    cdrnlstd = 'BNDLIST\\DRN\\UMD_DRN_{0}-{1}.dat'.format( start_date.year, ondate.year )
    cdrnlstf = cpath2mod + cdrnlstd
    if ntdrn > 0:
        cval = 'OPEN/CLOSE {0}\n'.format( cdrnlstd )
        df.write(cval)
    tdf = open(cdrnlstf,'w')
    #--ghb
    cval = '{0:10d}         0          #STRESS PERIOD {1:05d} {2}-{3}\n'.format( ntghb, 1, start_date.year, ondate.year )
    gf.write(cval)
    cghblstd = 'BNDLIST\\GHB\UMD_GHB_{0}-{1}.dat'.format( start_date.year, ondate.year )
    cghblstf = cpath2mod + cghblstd
    if ntghb > 0:
        cval = 'OPEN/CLOSE {0}\n'.format( cghblstd )
        gf.write(cval)
    tgf = open(cghblstf,'w')
    #--write data for drains and ghbs
    success = WriteData(tdf,tgf,nghb,ighbl,mf_bnd,top,mf_avgstage,r_avgcoast,r_avgtp_ret,r_avgtp_dis)
    #--close temporary drn and ghb list files
    tdf.close()
    tgf.close()
#--close average ghb and drn files
    df.close()
    gf.close()

#--plot average boundary type for UMD model grid
if MakeImages == True:
    temp  = np.ma.masked_where(ib<2,mf_bnd)
    fout = 'Figures\\BND_TYPE_{0}-{1}'.format( start_date.year, ondate.year )
    print 'writing...{0}'.format( fout )
    au.plotimage( temp, vmin=-3, vmax=3, extent=im_extent, text=ftitle, fout=fout, addcolorbar='vertical', interpolation=None, polyline=hydrography, figuresize=figuresize )
    #au.plotgrid( xcell, ycell, temp, vmin=-3, vmax=3, text=ftitle, fout=fout, addcolorbar='vertical', polyline=hydrography, figuresize=figuresize )
    #--plot eden data interpolated to UMD model grid
    temp  = np.ma.masked_where(ib<2,mf_avgstage)
    fout = 'Figures\\BND_STAGE_{0}-{1}'.format( start_date.year, ondate.year )
    print 'writing...{0}'.format( fout )
    au.plotimage( temp, vmin=-1, vmax=5, extent=im_extent, text=ftitle, fout=fout, addcolorbar='vertical', interpolation=None, polyline=hydrography, figuresize=figuresize )
    #au.plotgrid( xcell, ycell, temp, vmin=-1, vmax=5, text=ftitle, fout=fout, addcolorbar='vertical', polyline=hydrography, figuresize=figuresize )
    #--plot water depth for UMD model grid
    temp  = np.ma.masked_where(ib<2,mf_avgstage-top)
    fout = 'Figures\\BND_DEPTH_{0}-{1}'.format( start_date.year, ondate.year )
    print 'writing...{0}'.format( fout )
    au.plotimage( temp, vmin=-2, vmax=2, extent=im_extent, text=ftitle, fout=fout, addcolorbar='vertical', interpolation=None, polyline=hydrography, figuresize=figuresize )
    #au.plotgrid( xcell, ycell, temp, vmin=-2, vmax=2, text=ftitle, fout=fout, addcolorbar='vertical', polyline=hydrography, figuresize=figuresize )



#--create animation(s)
if MakeImages == True:
    #--eden stage data
    coutf = 'Figures_Eden\\EDEN_RAW.swf'
    cline = 'ffmpeg.exe -i Figures_Eden\\EDEN_RAW_%05d.png -r 24 {0} -y'.format( coutf )
    try:
        os.remove(coutf)
    except:
        print 'could not remove...{0}'.format( coutf )
    subprocess.call(cline, stdin=None, stdout=None, stderr=None, shell=False)
    #--eden water depth data
    coutf = 'Figures_Eden\\EDEN_DEPTH.swf'
    cline = 'ffmpeg.exe -i Figures_Eden\\EDEN_DEPTH_%05d.png -r 24 {0} -y'.format( coutf )
    try:
        os.remove(coutf)
    except:
        print 'could not remove...{0}'.format( coutf )
    subprocess.call(cline, stdin=None, stdout=None, stderr=None, shell=False)
    #--bnd types
    coutf = 'Figures\\BND_TYPE.swf'
    cline = 'ffmpeg.exe -i Figures\\BND_TYPE_%05d.png -r 24 {0} -y'.format( coutf )
    try:
        os.remove(coutf)
    except:
        print 'could not remove...{0}'.format( coutf )
    subprocess.call(cline, stdin=None, stdout=None, stderr=None, shell=False)
    #--bnd stages
    coutf = 'Figures\\BND_STAGE.swf'
    cline = 'ffmpeg.exe -i Figures\\BND_STAGE_%05d.png -r 24 {0} -y'.format( coutf )
    try:
        os.remove(coutf)
    except:
        print 'could not remove...{0}'.format( coutf )
    subprocess.call(cline, stdin=None, stdout=None, stderr=None, shell=False)
    #--bnd depths
    coutf = 'Figures\\BND_DEPTH.swf'
    cline = 'ffmpeg.exe -i Figures\\BND_DEPTH_%05d.png -r 24 {0} -y'.format( coutf )
    try:
        os.remove(coutf)
    except:
        print 'could not remove...{0}'.format( coutf )
    subprocess.call(cline, stdin=None, stdout=None, stderr=None, shell=False)


#--delete temporary files
if KeepAllPng == False:
    for iday in range(0,maxdays):
        fout = 'Figures_Eden\\EDEN_RAW_{0:05d}.png'.format( iday + 1 )
        os.remove(fout)
        fout = 'Figures_Eden\\EDEN_DEPTH_{0:05d}.png'.format( iday + 1 )
        os.remove(fout)
        fout = 'Figures\\BND_TYPE_{0:05d}.png'.format( iday + 1 )
        os.remove(fout)
        fout = 'Figures\\BND_STAGE_{0:05d}.png'.format( iday + 1 )
        os.remove(fout)
        fout = 'Figures\\BND_DEPTH_{0:05d}.png'.format( iday + 1 )
        os.remove(fout)
