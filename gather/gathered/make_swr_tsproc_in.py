#START GET_SERIES_SWR_FLOW      
#  CONTEXT all                  
#  FILE md.fls                  
#  REACH_GROUP_NUMBER 1         
#  DATA_TYPE qeflow               
#  DATE_1 01/01/1996            
#  TIME_1 00:00:00              
#  NEW_SERIES_NAME test         
#END GET_SERIES_SWR_FLOW  






numRchGrp = 126

f_out = open('swr_tsproc.dat','w')

for r in range(numRchGrp):
    f_out.write('\nSTART GET_SERIES_SWR_FLOW\n')
    f_out.write(' CONTEXT all\n')
    f_out.write(' FILE md.fls\n')
    f_out.write(' REACH_GROUP_NUMBER '+str(r+1)+'\n')
    f_out.write(' DATA_TYPE qeflow\n')
    f_out.write(' DATE_1 01/01/1996\n')
    f_out.write(' TIME_1 00:00:00\n')
    f_out.write(' NEW_SERIES_NAME rg'+str(r+1)+'\n')
    f_out.write('END GET_SERIES_SWR_FLOW\n')

f_out.close()
    
    