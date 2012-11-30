#!/usr/bin/env python
# To use:
#	   python setup.py build
#	   python setup.py install
#	   python setup.py install --prefix=...
#	   python setup.py bdist --format=wininst
#	   python setup.py bdist --format=rpm
#	   python setup.py sdist --formats=gztar,zip

# This setup script authored by Philippe Le Grand, June 13th 2005

import sys

if not hasattr(sys, 'version_info') or sys.version_info < (2,3,0,'alpha',0):
	raise SystemExit, "Python 2.6 or later required to build flopy"


from distutils.core import setup, Extension

setup (name = "flopy",
	   extra_path = 'flopy',
	   version = "0.0.2.py2x",
	   author="Mark Bakker and Vincent Post",
	   author_email="mark.bakker@tudelft.nl or vincent.post@flinders.edu.au",
	   py_modules = ["mbase"
,"mf"
,"mfbas"
,"mfbcf"
,"mfchd"
,"mfdis"
,"mfdrn"
,"mfevt"
,"mfghb"
,"mfoc"
,"mfpbc"
,"mfpcg"
,"mfrch"
,"mfreadbinaries"
,"mfriv"
,"mfswi"
,"mfwel"
,"mswt"
,"mswtvdf"
,"mt"
,"mtadv"
,"mtbtn"
,"mtdsp"
,"mtgcg"
,"mtrct"
,"mtreadbinaries"
,"mtssm"
,"mflpf"
,"mtphc"
,"mttob"
]
# This trick might be original; I haven't found it anywhere.
# The precompiled Fortran library is passed as a data file,
# so that dist does not try and recompile on the destination machine
#       data_files = [("Lib/site-packages/ttim",["bessel.pyd","invlap.pyd"])]
#	   ext_modules= [Extension("besselaes",["besselaes.f90","trianglemodule.c"])]
	   )
