import os
import shutil

root_dirs = ['D:\\Users\\jwhite\\']
skip_dirs = ['git_repo']

extensions = ['py']

gather_path = 'gathered\\'
copied = []
count = []
f_log = open('gathered.log','w',0)
for root in root_dirs:
    for path,dirs,files in os.walk(root):
        for sd in skip_dirs:
            if sd in dirs:
                dirs.remove(sd) 
        for f in files:
            for ext in extensions:
                if f.endswith(ext):
                    if f in copied:
                        c = '_'+str(count[copied.index(f)])
                        count[copied.index(f)] += 1
                    else:
                        c = ''
                        count.append(1)
                        copied.append(f)
                    ff = f + c
                    f_log.write(ff+','+path+'\\'+f+'\n')
                    shutil.copy2(path+'\\'+f,gather_path+ff)
f_log.close()                    

