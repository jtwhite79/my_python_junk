import re
import sys
import shapefile

def get_points(file):
    m_2_ft = 3.281
    pt1 = re.compile('\[POINTS\]',re.IGNORECASE)
    pt2 = re.compile('point')
    pt3 = re.compile('EndSect  // POINTS',re.IGNORECASE)
    point_x,point_y,point_attri = [],[],[]
    f = open(file,'r')
    while True:
        line = f.readline()
        if pt1.search(line) != None:
            while True:
                line = f.readline()
                if pt3.search(line) != None:
                    return point_x,point_y,point_attri
                raw = line.strip().split(',')
                point_x.append(float(raw[1])*m_2_ft)
                point_y.append(float(raw[2])*m_2_ft)
                this_name = float(raw[0].split('=')[-1].strip())
                this_list = [this_name]
                this_list.extend(raw[1:])
                point_attri.append(this_list)
                




#--get the points from the nwk11 file
file = 'Broward_Base_05.nwk11'
point_x,point_y,point_attri = get_points(file)
#print point_x[0],point_attri[0]


#--set the writer instance
wr = shapefile.Writer()
wr.field('field1',fieldType='N',size=50,decimal=10)
wr.field('field2',fieldType='N',size=50,decimal=10)
wr.field('field3',fieldType='N',size=50,decimal=10)
wr.field('field4',fieldType='N',size=50,decimal=10)
wr.field('field5',fieldType='N',size=50,decimal=10)
wr.field('field6',fieldType='N',size=50,decimal=10)



for i in range(len(point_x)):
    this_point = [point_x[i],point_y[i]]
    
    wr.poly(parts=[[this_point]], shapeType=1)
    wr.record(point_attri[i][0],point_attri[i][1],point_attri[i][2],point_attri[i][3],point_attri[i][4],point_attri[i][5])

wr.save(target='..\\shapes\\she_points')
    