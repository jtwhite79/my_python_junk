import os
import shutil


source = 'D:\\Users\\jwhite\\Projects\\Broward\\_prediction\\_pyprojects\\'
dest = 'bro.03.pred\\python\\'

if not os.path.exists(dest):
    os.mkdir(dest)


shutil.copy('bro_pred.py',dest+'bro_pred.py')
shutil.copy('D:\\Users\\jwhite\\git_repo\\my_python_junk\\MFBinaryClass.py',dest+'MFBinaryClass.py')
shutil.copy('D:\\Users\\jwhite\\git_repo\\my_python_junk\\pestUtil.py',dest+'pestUtil.py')
shutil.copy('D:\\Users\\jwhite\\git_repo\\my_python_junk\\shapefile.py',dest+'shapefile.py')

for path,dirs,files in os.walk(source):
    for f in files:
        if f.endswith('.py'):
            shutil.copy(path+'\\'+f,dest+f)

