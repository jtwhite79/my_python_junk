import shapefile

f = open('unit_thickness.csv','r')
f_out = open('unit_thickness.dat','w')

header = f.readline().strip().split('|')

f_out.write('tsala\n5\n')
for item in header:
    f_out.write(item+'\n')

records = []
for line in f:
    rec = line.strip().split('|')
    f_out.write(' '.join(rec)+'\n')
    records.append(rec)
    
    
f.close()
f_out.close()    
        
wr = shapefile.Writer()
wr.field('X',fieldType='N',size=20,decimal=5)
wr.field('Y',fieldType='N',size=20,decimal=5)
wr.field('Sand',fieldType='N',size=20,decimal=5)
wr.field('Clay',fieldType='N',size=20,decimal=5)
wr.field('Lmstn',fieldType='N',size=20,decimal=5)

for r in records:
    pt = [float(r[0]),float(r[1])]
    wr.poly([[pt]],shapeType=shapefile.POINT)
    wr.record(r)
wr.save('lith_control_points')    