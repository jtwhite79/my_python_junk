import numpy as np

def write_line(raw,file):
    for r in raw:
        file.write(r.ljust(10))
    file.write('\n')
    return



f_in = open('swr_stage.dat','r')
f_out = open('swr_stage_mod.dat','w')

for line in f_in:
    raw = line.strip().split()
    this_stage = float(raw[1])
    if this_stage < 1.5:
        this_stage = -0.5
        raw[1] = '-0.5'
    write_line(raw,f_out)
    