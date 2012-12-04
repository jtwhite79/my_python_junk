import os
import sys
import numpy as np
import shapefile


#--index of row and col values in the grid shapefile
idx_case = 15
idx_td   = 16
idx_top  = 54

idx_bot_h  = 38
idx_bot_q5 = 43
idx_bot_q4 = 42
idx_bot_q3 = 41
idx_bot_q2 = 40
idx_bot_q1 = 39
idx_bot_t3 = 46
idx_bot_t2 = 45
idx_bot_t1 = 44

idx_bots = [idx_bot_q4,idx_bot_q3,idx_bot_q2,idx_bot_q1,idx_bot_t2,idx_bot_t1]
bot_portions_labels = ['botq4_por','botq3_por','botq2_por','botq1_por','bott2_por','bott1_por']

#--get the points
print 'loading PWS points...'
file = 'PWS_elevJoin'
shp_poly = shapefile.Reader(shapefile=file)
shp_header = shp_poly.dbfHeader()
print shp_header[idx_case],shp_header[idx_td]
print shp_header[idx_bot_h],shp_header[idx_bot_q1],shp_header[idx_top]
points = shp_poly.shapes()
print len(shp_header)

#--set the writer instance
wr = shapefile.Writer()
#--add all existing grid attributes
for item in shp_header:
    wr.field(item[0],fieldType=item[1],size=item[2],decimal=item[3])

for b in bot_portions_labels:
    wr.field(b,fieldType='N',size=20,decimal=4)

    
#--loop over each cell
for pt_idx in range(len(points)):
    
    print 'working on point ',pt_idx+1,' of ',len(points)
    
    this_rec = shp_poly.record(pt_idx)          
    this_top = this_rec[idx_top]
    this_case = this_rec[idx_case]
    this_td = this_rec[idx_td]
    
    this_int = this_case - this_td
    this_layer_depth = []
    for b in range(len(idx_bots)-1): 
        this_layer_depth.append(this_top - this_rec[idx_bots[b]])
    
    #--if the case and td data aren't missing
    if this_int != 0:
        this_portions = [0]    
        #print this_case,this_td,this_layer_depth        
        for b in range(len(idx_bots)-1):        
            this_top_depth = this_top - this_rec[idx_bots[b-1]]                                    
            this_bot_depth = this_top - this_rec[idx_bots[b]]
            #--bottom is shallower than casing depth
            if this_bot_depth < this_case:
                this_portions.append(0)
            #--         
            elif this_top_depth > this_td:
                this_portions.append(0)                                   
            else:
                #--check for partial penetration
                if this_bot_depth > this_td and this_top_depth < this_case:
                    this_length = this_case - this_td
                elif this_top_depth < this_case:
                    this_length = this_case - this_bot_depth
                elif this_bot_depth > this_td:
                    this_length = this_top_depth - this_td               
                else:
                    this_length = this_top_depth - this_bot_depth         
                this_portions.append(this_length / this_int)
            
        #print this_portions    
    #if pt_idx == 2:
    #    break       
    
    this_rec.extend(this_portions)    
    wr.poly([points[pt_idx].points], shapeType=1)     
    wr.record(this_rec)
    #break
   
wr.save(target='PWS_modelDomain_layerPortion')

      