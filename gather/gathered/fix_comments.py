import sys

fname = sys.argv[1]

f = open(fname,'r')
lines = []
lcount = 0
cont_chars = ['*','$']
for line in f:
    raw = line.strip().split()
    if raw:
        print lcount,raw[0]
    if line[0].upper() == 'C' or line[0] == '*':
        print line,
        line = '!' + line[1:]
        print line,            
    
    elif len(raw) > 0 and (raw[0].startswith('*') or raw[0].startswith('$')):
        lines[-1] = lines[-1][:-1] + ' &\n'
        line_new = ''
        for i,char in enumerate(line):
            if char in cont_chars:
                line_new += ' '
                break
            else:
                line_new += char                
        line_new += line[i+1:]
        line = line_new                                   
    lines.append(line)            
    lcount += 1
f.close()
f = open(fname,'w')
for line in lines:
    f.write(line)    
