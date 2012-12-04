import os
import zipfile

zip_dir = 'downloads\\'
zip_files = os.listdir(zip_dir)
out_dir = 'surface_netcdf\\'
for zfile in zip_files:
    z = zipfile.ZipFile(zip_dir+zfile,mode='r')
    z.extractall(out_dir)

