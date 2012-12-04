import shapefile





f = open('tbl29_pro.dat','r')
txt = f.readline()
num_attri = int(f.readline())
attribute_names = []
for a in range(num_attri):
    attribute_names.append(f.readline().strip())

wr = shapefile.Writer()
for a in attribute_names:
    wr.field(a,fieldType='N',size=20,decimal=3)

x_idx = 0
y_idx = 1

for line in f:
    raw = line.strip().split()
    for r_idx in range(len(raw)):
        raw[r_idx] = int(raw[r_idx])
    this_x = float(raw[x_idx])
    this_y = float(raw[y_idx])
    wr.poly([[[this_x,this_y]]],shapeType=1)
    wr.record(raw)
wr.save('table_29')




