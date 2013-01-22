import math
import numpy as np
from shapely.geometry import Polygon

def rotate(box,angle):
    new_box = []
    sin_phi = math.sin(angle*math.pi/180.0)
    cos_phi = math.cos(angle*math.pi/180.0)
    #print sin_phi,cos_phi
    for point in box:
        new_x = (point[0] * cos_phi) - (point[1] * sin_phi)
        new_y = (point[0] * sin_phi) + (point[1] * cos_phi)
        new_box.append([new_x,new_y])
    return new_box    

class node():
    def __init__(self,dx,dy,xyverts,top,bot):
        self.dx = float(dx)
        self.dy = float(dy)
        self.dz = float(np.abs(top-bot))               
        self.xy = Polygon(xyverts)
        self.top = float(top)
        self.bot = float(bot)

    def intersects(self,other):
        #--if other node instance intersects in xy plane and is in the range of [top,bot]
        if self.xy.intersects(other.xy) and self.zrange(other):
            return True
        return False
    def zrange(self,other):
        if other.top <= self.top and other.top >= self.bot:
            return True
        elif other.bot <= self.top and other.bot >= self.bot:
            return True
        else:
            return False

    def z_overlap(self,other):
        zo = min(self.top,other.top) - max(self.bot,other.bot) 
        return zo 

    def intersection(self,other):
        #--calc the fractional volumne of over lap between the self and other node instance
        xy = self.xy.intersection(other.xy)        
        dx = np.abs(xy.bounds[0] - xy.bounds[2])
        dy = np.abs(xy.bounds[1] - xy.bounds[3])                
        dz = self.z_overlap(other)        
        return (xy.area * dz) / self.volume

    @property
    def volume(self):
        return self.xy.area * self.dz
        

class grid():
    def __init__(self,origin,dis_file,rotation=None):
        self.x = float(origin[0])
        self.y = float(origin[1])

        self.dis_file = dis_file
        self.rotation = rotation
        self.load_dis()
    
    def load_dis(self):
        print 'loading dis file...',self.dis_file
        f = open(self.dis_file,'r')
        while True:
            line = f.readline()
            if not line.startswith('#'):
                break
        #--DS 1
        raw = line.strip().split()
        self.nlay = int(raw[0])
        self.nrow = int(raw[1])
        self.ncol = int(raw[2])
        #--DS 2
        line = f.readline()
        #--DS 3 - DELR
        delr = self.u2drel(f,1,self.ncol)
        #--DS 4 - DELC
        delc = self.u2drel(f,self.nrow,1)
        #--DS 5 - TOP
        top = self.u2drel(f,self.nrow,self.ncol)
        self.top = top
        #--DS 6 BOTM
        botm = []
        for k in range(self.nlay):
            this_botm = self.u2drel(f,self.nrow,self.ncol)
            botm.append(this_botm)
        botm = np.array(botm)
        self.botm = botm

        print botm.shape
        #--close the dis file - that is all we need
        f.close()
        print 'done' 

        print 'building node objects...'
        #--now build the cell objects
        #xs = self.x + np.cumsum(delr)
        #ys = self.y + np.cumsum(delc)
        xs = np.cumsum(delr)
        ys = np.cumsum(delc)
        #xs = np.insert(xs,0,[self.x])
        #ys = np.insert(ys,0,[self.y])
        xs = np.insert(xs,0,[0])
        ys = np.insert(ys,0,[0])
        ys = np.flipud(ys)

        nodes = []
        inodes = {}
        inode = 0
        for j,x in enumerate(xs[:-1]):
            for i,y in enumerate(ys[:-1]):               
                zs = botm[:,i,j]
                zs = np.insert(zs,0,top[i,j])
                for k,z in enumerate(zs[:-1]):
                    x1,x2 = xs[j:j+2]                    
                    y1,y2 = ys[i:i+2]
                    z1,z2 = zs[k:k+2]
                    dx = np.abs(x2-x1)
                    dy = np.abs(y2-y1)
                    dz = np.abs(z2-z1)
                    xyverts = [[x1,y1],[x1,y2],[x2,y2],[x2,y1],[x1,y1]]                    
                    if self.rotation != None:                                               
                        xyverts = rotate(xyverts,self.rotation)
                    #--add in the offset
                    arr = np.array(xyverts)
                    arr[:,0] += self.x
                    arr[:,1] += self.y

                    n = node(dx,dy,list(arr),z1,z2)
                    nodes.append(n) 
                    inodes[inode] = (i,j,k) 
                    inode += 1   
        self.nodes = nodes
        self.inodes = inodes
        print 'done'
        return                        

    
    def u2drel(self,f,nrow,ncol):
        line = f.readline()
        raw = line.strip().split()
        #--check for internal external
        if 'external' in raw[0].lower() or 'internal' in raw[0].lower():
            raise NotImplementedError('"internal" or "external" not supported')

        #--check for open/close
        if 'open' in raw[0].lower():
            fname = raw[1]
            cnstnt = float(raw[2])
            fmtin = raw[3]
            iprn = raw[4]
            if 'free' not in  fmtin.lower():
                print 'Warning - parsing record using whitespace, but format is listed as ',fmtin
            data = np.loadtxt(fname,dtype=np.float64)
            #print data.shape
            if data.shape != (nrow,ncol):
                if nrow == 1:
                    data = np.atleast_2d(data)
                elif ncol == 1:
                    data = np.atleast_2d(data).transpose()
                else:
                    raise IndexError('data array not the right shape')

            #assert data.shape == (nrow,ncol)
            data *= cnstnt                        
            #print data.shape
            return data
        
        else:
            locat = int(raw[0])
            if locat == 0:
                cnstnt = float(raw[1])
                data = np.zeros((nrow,ncol)) + cnstnt
                return data
            if locat > 0:
                cnstnt = float(raw[1])
                fmtin = raw[3]
                iprn = raw[4]
                if 'free' not in fmtin.lower():
                    print 'Warning - parsing record using whitespace, but format is listed as ',fmtin
                data = []
                while True:                    
                    raw = f.readline().split()
                    data.extend(raw)
                    if len(data) >= (nrow * ncol):
                        break
                data = np.array(data,dtype=np.float64)
                data = np.resize(data,(nrow,ncol))
                return data

    def build_map(self,other): 
        '''creates a mapping between to grid instances
        ''' 
        if self.rotation != other.rotation:
            raise NotImplementedError('cannot map two grids with different rotations - too lazy')
        
        grid_map = {}        
        #--for each node in this instance
        for i,nd in enumerate(self.nodes):
            ix_nodes = {}
            #--for each node in other instance
            for ii,nnd in enumerate(other.nodes):
                #--if node nd of this instance intersects node nnd of other instance
                if nd.intersects(nnd):
                    #--calc the fraction of the volume of nd that is covered by nnd
                    ivol = nd.intersection(nnd)
                    #--this filters out 0.0 ivols - happens if grids are aligned
                    if ivol:
                        #--store the fractional volume overlap by the (i,j,k) tuple key
                        ix_nodes[other.inodes[ii]] = ivol
                        #print ivol,self.inodes[ind],other.inodes[iind]
            grid_map[self.inodes[i]] = ix_nodes                                                    
        return grid_map
    
#--for testing
if __name__ == '__main__':
    import shapefile
    coarse = grid([4588292.0,16933962.0],'SZ3_ss_CD.dis',rotation=35.0)
    #--write the shapefiles of each grid for testing        
    #--coarse
    wr = shapefile.Writer()
    wr.field('row',fieldType='N',size=10,decimal=0)
    wr.field('column',fieldType='N',size=10,decimal=0)
    wr.field('layer',fieldType='N',size=10,decimal=0)
    wr.field('cellnum',fieldType='N',size=10,decimal=0)    
    wr.field('top',fieldType='N',size=15,decimal=3)
    wr.field('l1_bot',fieldType='N',size=15,decimal=3)
    wr.field('l2_bot',fieldType='N',size=15,decimal=3)
    wr.field('l3_bot',fieldType='N',size=15,decimal=3)

    for i,nd in enumerate(coarse.nodes):
        inode = coarse.inodes[i] 
        i,j,k = inode[0],inode[1],inode[2] 
        top = coarse.top[i,j]
        l1 = coarse.botm[0,i,j]
        l2 = coarse.botm[1,i,j]
        l3 = coarse.botm[2,i,j]
              
        pts = list(nd.xy.exterior.coords)
        wr.poly([pts],shapeType=shapefile.POLYGON)
        wr.record([i+1,j+1,k+1,i+1,top,l1,l2,l3])
    wr.save('shapes\\'+coarse.dis_file.split('.')[0])


    print
    #coarse = grid([0.0,0.0],'coarse.dis',rotation=0.0)

    #fine = grid([0.30,0.30],'fine.dis',rotation=0.0)
    #grid_map = fine.build_map(coarse)
    #
    ##--write the shapefiles of each grid for testing        
    ##--coarse
    #wr = shapefile.Writer()
    #wr.field('row',fieldType='N',size=10,decimal=0)
    #wr.field('column',fieldType='N',size=10,decimal=0)
    #wr.field('layer',fieldType='N',size=10,decimal=0)
    #wr.field('cellnum',fieldType='N',size=10,decimal=0)    
    #wr.field('rcl_tup',fieldType='C',size=20,decimal=0)
    #for i,nd in enumerate(coarse.nodes):
    #    inode = coarse.inodes[i]        
    #    pts = list(nd.xy.exterior.coords)
    #    wr.poly([pts],shapeType=shapefile.POLYGON)
    #    wr.record([inode[0]+1,inode[1]+1,inode[2]+1,i+1,str(inode)])
    #wr.save('shapes\\coarse')

    #wr = shapefile.Writer()
    #wr.field('row',fieldType='N',size=10,decimal=0)
    #wr.field('column',fieldType='N',size=10,decimal=0)
    #wr.field('layer',fieldType='N',size=10,decimal=0)
    #wr.field('cellnum',fieldType='N',size=10,decimal=0)    
    #wr.field('rcl_tup',fieldType='C',size=50,decimal=0)
    #wr.field('ivol',fieldType='C',size=50,decimal=0)
    #for i,nd in enumerate(fine.nodes):
    #    inode = fine.inodes[i]
    #    gmap = grid_map[inode]
    #    rcl_str,ivol_str = '',''
    #    for rcl,ivol in gmap.iteritems():
    #        rcl_str += ' '+str(rcl)
    #        ivol_str += ' '+str(ivol)        
    #    pts = list(nd.xy.exterior.coords)
    #    wr.poly([pts],shapeType=shapefile.POLYGON)
    #    wr.record([inode[0]+1,inode[1]+1,inode[2]+1,i+1,rcl_str,ivol_str])
    #wr.save('shapes\\fine')

      



