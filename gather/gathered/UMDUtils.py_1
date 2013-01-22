import os

def TestDirExist(ctest):
    #--Make sure output directories are created
    for f in ctest:
        print 'evaluating... "{0}"'.format( f )
        fa = os.path.abspath(f)
        d = os.path.dirname(fa)
        if not os.path.exists(d):
            print 'creating directory path...\n  "{0}"'.format( d )
            os.makedirs(d)
