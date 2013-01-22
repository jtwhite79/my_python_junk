import re

def parse_line(line):
   
   raw = line.strip().split()
   obs_group = raw[-1]
   obs_name = raw[0]
   return obs_group,obs_name 

pst_file = 'pest_actual.pst'
f = open(pst_file,'r')
f_out = open('obs.typ','w')

re_obs = re.compile('\* observation data')
re_mod = re.compile('\* model command line')
while True:
    line = f.readline()
    if line == '':
        break
    if re_obs.search(line) != None:
        line2 = f.readline()
        og,on = parse_line(line2)
        f_out.write('* observation type '+og+'\n')
        f_out.write(on+'\n')
        this_og = og
        while True:
            line2 = f.readline()
            if re_mod.search(line2) != None:
                break
            og,on = parse_line(line2)
            if og != this_og:
                f_out.write('* observation type '+og+'\n')
                this_og = og
            f_out.write(on+'\n')
f.close()
f_out.close()
            
                
            
            
        
        