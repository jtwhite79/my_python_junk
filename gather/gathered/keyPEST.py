#keyPEST --- a JUPITER-like keyword to PST translator for PEST++
# a m!ke@usgs joint
# Mike Fienen --> mnfienen@usgs.gov
import sys
import numpy as np
import keyPESTdata as kp
reload(kp)

# get the input filename from the command line
#infile  = sys.argv[1]
  
# initialize the main control
main_control = kp.file_control()
# read the input file
#infile = 'testcase.key'
infile = 'testcase_xls.xml'
main_control.read(infile)            
# write the output file
outfile = infile[:-3]+'_out.xml'               
main_control.write(outfile)
