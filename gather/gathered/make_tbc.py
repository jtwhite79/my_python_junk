###################################################
## - Example TBC file from SUTRAMS manual
#  ##                                          
#  ## DATASET TBC1                             
#  ## DNTIME - 1                               
#  18000.0                                     
#  ##                                          
#  ## DATASET TBC2                             
#  ## NTPBC,NTUBC,NTSOP,NTSOU                  
#  0 1 0 0                                     
#  ##                                          
#  ## DATASET TBC3A                            
#  ## SPECIFIED PRESSURES                      
#  ## ***NONE***                               
#  ##                                          
#  ## DATASET TBC3B                            
#  ## SPECIFIED CONCENTRATION                  
#  ##[NSN] [ITUBC] [UTBC]                      
#  2 6 10.0                                    
#  0                                           
#  ##                                          
#  ## DATASET TBC3C                            
#  ## SPECIFIED FLUID FLUXES                   
#  ## ***NONE***                               
#  ##                                          
#  ## DATASET TBC3D                            
#  ## SPECIFIED SOLUTE OR TEMPERATURE FLUXES   
#  ## ***NONE***                               
#  ##                                          
#  ## DATASET TBC1                             
#  ## DNTIME - 2                               
#  19000.0                                     
#  ## DATASET TBC2                             
#  ## NTPBC,NTUBC,NTSOP,NTSOU                  
#  0 2 0 0                                     
#  ##                                          
#  ## DATASET TBC3A                            
#  ## SPECIFIED PRESSURES                      
#  ## ***NONE***                               
#  ##                                          
#  ## DATASET TBC3B                            
#  ## SPECIFIED CONCENTRATION                  
#  ##[NSN] [ITUBC] [UTBC]                      
#  2 6 9.0                                     
#  1 100 1.0                                   
#  0                                           
#  ##                                          
#  ## DATASET TBC3C                            
#  ## SPECIFIED FLUID FLUXES                   
#  ## ***NONE***                               
#  ##                                          
#  ## DATASET TBC3D                            
#  ## SPECIFIED SOLUTE OR TEMPERATURE FLUXES   
#  ## ***NONE***                               
#  ##                                          
#  ## DATASET TBC4                             
#  ## DATA SET TERMINATION                     
#  'END'                                       
#  ##                                          

##########################################################



#--some functions to write the various datasets
def write_tbc1(f,sp,dntime):
    f.write('##\n## DATASET TBC1\n## DNTIME - '+str(sp)+'\n' )
    f.write(str(dntime)+'\n')
    return  

def write_tbc2(f,ntpbc,ntubc,ntsop,ntsou):
    f.write('##\n## DATASET TBC2\n## NTPBC,NTUBC,NTSOP,NTSOU\n')
    f.write(str(ntpbc)+' '+str(ntubc)+' '+str(ntsop)+' '+str(ntsou)+'\n')
    return
 
def write_tbc3a(f,nodes,pressure,noHeader=False):
    if noHeader==False:f.write('##\n## DATASET TBC3A\n## SPECIFIED PRESSURE\n')
    for n in nodes:
        f.write(str(n)+' '+str(pressure)+'\n')
    return
    
def write_tbc3b(f,nodes,temp,noHeader=False):
    if noHeader==False:f.write('##\n## DATASET TBC3A\n## SPECIFIED CONCENTRATION/TEMPERATURE\n')
    for n in nodes:
        f.write(str(n)+' '+str(temp)+'\n')
    return    
     
def write_tbc3c(f,nodes,fluid,noHeader=False):
    if noHeader==False:f.write('##\n## DATASET TBC3C\n## SPECIFIED FLUID SOURCES/SINKS\n')
    for n in nodes:
        f.write(str(n)+' '+str(fluid)+'\n')
    return

def write_tbc3d(f,nodes,mass,noHeader=False):
    if noHeader==False:f.write('##\n## DATASET TBC3D\n## SPECIFIED MASS/ENERGY SOURCES/SINKS\n')
    for n in nodes:
        f.write(str(n)+' '+str(mass)+'\n')
    return



#--get the top and bottom nodes from the file
def load_nodes_from_file(nodeFile):
    f = open(nodeFile,'r')
    topNodes = []
    botNodes = []
    for line in f:
        topNodes.append(line.strip().split()[0])
        botNodes.append(line.strip().split()[1])
    f.close()
    return topNodes,botNodes



#---------------------------------------------------------
#--main program
#---------------------------------------------------------



#--load top and bottom node lists
nodeFile = 'top_bot_nodes.dat'
topNodes,botNodes = load_nodes_from_file(nodeFile)


#--input file info
#--top of model temp column - count from zero!!!
#--for TBC3B
tempTopColNum = 3
#--bot of model temp column
tempBotColNum = 7

#--top and bot pressure columns
#--for TBC3A
presTopColNum = 9
presBotColNum = 8

#--top and bot fluid source
#--for TBC3C
fluidSourceTopColNum = 3
fluidSourceBotColNum = 7

#--top and bot mass/energy source
#--for TBC3D
massSourceTopColNum = 3
massSourceBotColNum = 7

fileName = 'Temperature time series SRS4_1.txt'

#--create file handles
inputFile = open(fileName,'r')
outputFile = open('test.tbc','w')

#--time stepping
thisTime = 0.0
step = 3600.0 #seconds per hour
stressPeriod = 1

#--control parameters


ntpbc = 82     #len(topNodes) + len(botNodes)
ntubc = 82     #len(topNodes) + len(botNodes)
ntsop = 0
ntsou = 0

#--read the first line of the file
header = inputFile.readline()

#--read each data line in the file
for line in inputFile:
    
    #--split this line by whitespaces
    raw = line.strip().split()
    
    #--write the control datasets for each entry in the file
    write_tbc1(outputFile,stressPeriod,thisTime)
    write_tbc2(outputFile,ntpbc,ntubc,ntsop,ntsou)
    
    if (ntpbc > 0):
        #--write the top nodes for this top pressure
        write_tbc3a(outputFile,topNodes,float(raw[presTopColNum]))
   
        #--write the bottom nodes for this bottom temperature
        write_tbc3a(outputFile,botNodes,float(raw[presBotColNum]),noHeader=True)
    
    if (ntubc > 0):
        #--write the top nodes for this top temperature
        write_tbc3b(outputFile,topNodes,float(raw[tempTopColNum]))
   
        #--write the bottom nodes for this bottom temperature
        write_tbc3b(outputFile,botNodes,float(raw[tempBotColNum]),noHeader=True)
    
    if (ntsop > 0):
        #--write the top nodes for this top fluid source
        write_tbc3c(outputFile,topNodes,float(raw[fluidSourceTopColNum]))
   
        #--write the bottom nodes for this bottom fluid source
        write_tbc3c(outputFile,botNodes,float(raw[fluidSourceBotColNum]),noHeader=True)
        
    if (ntsou > 0):
        #--write the top nodes for this top mass source
        write_tbc3d(outputFile,topNodes,float(raw[massSourceTopColNum]))
   
        #--write the bottom nodes for this bottom source
        write_tbc3d(outputFile,botNodes,float(raw[massSourceBotColNum]),noHeader=True)    
            
    
    #--increment counters
    thisTime += step
    stressPeriod += 1

#--write the CTERM 
outputFile.write('END\n')


#--close file handles
inputFile.close()
outputFile.close()    
    
    
