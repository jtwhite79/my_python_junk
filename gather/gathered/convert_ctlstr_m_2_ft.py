


#--conversion factors
m3ps_2_ft3pd = (3.281**3)*60.0*60.0*24.0
m3ps2_2_ft3pd2 = (3.281**3)*(60.0**2)*(60.0**2)*(24.0**2)
mps_2_ftpd = 3.281*60.0*60.0*24.0
m_2_ft = 3.281
#ngvd_2_navd = -1.5
ngvd_2_navd = 0.0

#--strcritc fraction of cstrcrit
sc_frac = 0.01  # 1%

place = '           '

file = 'swr_structures_checked_allstage.dat'
f = open(file,'r')
f_out = open('test.dat','w')
while True:
    line_13a = f.readline()
    if line_13a == '':
        break
    raw_13a = line_13a.strip().split()
    if raw_13a[0] != '#':
        try:
            istrtype = int((raw_13a[3]))
        except:
            istrtype == -999
        if istrtype != -999:
            #--if this a weir 
            if istrtype == 6:
                #print  'fixed',istrtype,raw_13a[-1]
                #--strinv
                raw_13a[6] = '{0:10.3e}'.format((float(raw_13a[6])*m_2_ft)+ngvd_2_navd)
                #--strwid
                raw_13a[7] = '{0:10.3e}'.format((float(raw_13a[7])*m_2_ft))
                #--strval
                raw_13a[8] = '{0:10.3e}'.format((float(raw_13a[8])*m_2_ft))
                
                #--istrrch,istrnum,istrconn,istrtype
                f_out.write(raw_13a[0].rjust(11))
                f_out.write(raw_13a[1].rjust(11))
                f_out.write(raw_13a[2].rjust(11))
                f_out.write(raw_13a[3].rjust(11))
                
                #--nstrpts
                f_out.write(place)
                
                #--strcd
                f_out.write(raw_13a[4].rjust(11))
                
                #--strcd2               
                #--a bust coming from get_structure_reaches.py
                #--so skip it 
                #f_out.write(raw_13a[5].rjust(11))
                f_out.write(place)
                
                #--strcd3
                f_out.write(place)
                
                #--strinv
                f_out.write(raw_13a[6].rjust(11))    
                
                #--strinv2
                f_out.write(place)
                
                #--strwid
                f_out.write(raw_13a[7].rjust(11))    
                
                #--strwid2,strlen,strman
                f_out.write(place+place+place)
                
                #--strval
                f_out.write(raw_13a[8].rjust(11))
                
                #--istrdir
                f_out.write(raw_13a[9].rjust(11))
                
                #--the rest
                for r in raw_13a[10:]:
                    f_out.write(' '+r)
                
                f_out.write('\n')
                                                              
            
            
            elif istrtype == 7:
               
                #print  'fixed',istrtype,raw_13a[-1]
                #--strinv
                raw_13a[6] = '{0:10.3e}'.format((float(raw_13a[6])*m_2_ft)+ngvd_2_navd)
                #--strwid
                raw_13a[7] = '{0:10.3e}'.format((float(raw_13a[7])*m_2_ft))
                #--strval
                raw_13a[8] = '{0:10.3e}'.format((float(raw_13a[8])*m_2_ft))
                
                #--istrrch,istrnum,istrconn,istrtype
                f_out.write(raw_13a[0].rjust(11))
                f_out.write(raw_13a[1].rjust(11))
                f_out.write(raw_13a[2].rjust(11))
                f_out.write(raw_13a[3].rjust(11))
                
                #--nstrpts
                f_out.write(place)
                
                #--strcd
                f_out.write(raw_13a[4].rjust(11))
                
                #--strcd2               
                f_out.write(raw_13a[5].rjust(11))
                
                #--strcd3
                f_out.write(place)
                
                #--strinv
                f_out.write(raw_13a[6].rjust(11))    
                
                #--strinv2
                f_out.write(place)
                
                #--strwid
                f_out.write(raw_13a[7].rjust(11))    
                
                #--strwid2,strlen,strman
                f_out.write(place+place+place)
                
                #--strval
                f_out.write(raw_13a[8].rjust(11))
                
                #--istrdir
                f_out.write(raw_13a[9].rjust(11))
                
                #--the rest
                for r in raw_13a[10:]:
                    f_out.write(' '+r)
                
                f_out.write('\n')
                                            
            #--if this is operable underflow/overflow
            elif istrtype == 8 or istrtype == 9:
                #print 'operable',istrtype,raw_13a[-1]
                line_13b = f.readline()
                raw_13b = line_13b.strip().split()
                #--CSTRCRIT   
                raw_13b[3] = '{0:10.3e}'.format((float(raw_13b[3])*m_2_ft)+ngvd_2_navd)
                #--STRCRITC
                #raw_13b[4] = '{0:10.3e}'.format(float(raw_13b[4])*m_2_ft)  
                raw_13b[4] = '{0:10.3e}'.format(float(raw_13b[3])*sc_frac)  
                #--     STRRT 
                raw_13b[5] = '{0:10.3e}'.format(float(raw_13b[5])*mps_2_ftpd)  
                #-- STRMAX
                raw_13b[6] = '{0:10.3e}'.format(float(raw_13b[6])*m_2_ft)
                
                #print  'fixed',istrtype,raw_13a[-1]
                #--strinv
                raw_13a[6] = '{0:10.3e}'.format((float(raw_13a[6])*m_2_ft)+ngvd_2_navd)
                #--strwid
                raw_13a[7] = '{0:10.3e}'.format(float(raw_13a[7])*m_2_ft)
                #--strval
                raw_13a[8] = '{0:10.3e}'.format(float(raw_13a[8])*m_2_ft)
                
                #--istrrch,istrnum,istrconn,istrtype
                f_out.write(raw_13a[0].rjust(11))
                f_out.write(raw_13a[1].rjust(11))
                f_out.write(raw_13a[2].rjust(11))
                f_out.write(raw_13a[3].rjust(11))
                
                #--nstrpts
                f_out.write(place)
                
                #--strcd
                f_out.write(raw_13a[4].rjust(11))
                
                #--strcd2               
                f_out.write(raw_13a[5].rjust(11))
                
                #--strcd3
                f_out.write(place)
                
                #--strinv
                f_out.write(raw_13a[6].rjust(11))    
                
                #--strinv2
                f_out.write(place)
                
                #--strwid
                f_out.write(raw_13a[7].rjust(11))    
                
                #--strwid2,strlen,strman
                f_out.write(place+place+place)
                
                #--strval
                f_out.write(raw_13a[8].rjust(11))
                
                #--istrdir
                f_out.write(raw_13a[9].rjust(11))
                
                #--the rest
                for r in raw_13a[10:]:
                    f_out.write(' '+r)
                
                f_out.write('\n    ')
                
                #--write 13b
                
                #--cstrotyp
                f_out.write(raw_13b[0].rjust(11))
                
                #--istrorch
                f_out.write(raw_13b[1].rjust(11))
                
                #--istroqcon
                f_out.write(place)
                
                #--cstrolo
                f_out.write(raw_13b[2].rjust(11))
                
                #--cstrcrit
                f_out.write(raw_13b[3].rjust(11))
                
                #--strcritc
                f_out.write(raw_13b[4].rjust(11))                                    
                
                #--strrt
                f_out.write(raw_13b[5].rjust(11))
                
                #--strmax
                f_out.write(raw_13b[6].rjust(11))
                
                for r in raw_13b[7:]:
                    f_out.write(' '+r)
                f_out.write('\n')
                            
                            
            #--this is a pump
            elif istrtype == 3:
                #print 'pump',istrtype,raw_13a[-1]
                #--strval
                raw_13a[4] = '{0:10.3e}'.format(float(raw_13a[4])*m3ps_2_ft3pd)
                line_13b = f.readline()
                raw_13b = line_13b.strip().split()
                #--CSTRCRIT   
                raw_13b[3] = '{0:10.3e}'.format((float(raw_13b[3])*m_2_ft)+ngvd_2_navd)
                #--STRCRITC
                #raw_13b[4] = '{0:10.3e}'.format(float(raw_13b[4])*m_2_ft)  
                raw_13b[4] = '{0:10.3e}'.format(float(raw_13b[3])*sc_frac)  
                #--     STRRT 
                raw_13b[5] = '{0:10.3e}'.format(float(raw_13b[5])*m3ps2_2_ft3pd2)  
                #-- STRMAX
                print raw_13b[6]
                raw_13b[6] = '{0:10.3e}'.format(float(raw_13b[6])*m3ps_2_ft3pd)
                  #--istrrch,istrnum,istrconn,istrtype
                f_out.write(raw_13a[0].rjust(11))
                f_out.write(raw_13a[1].rjust(11))
                f_out.write(raw_13a[2].rjust(11))
                f_out.write(raw_13a[3].rjust(11))
                
                #--nstrpts
                f_out.write(place)
                
                #--strcd
                f_out.write(place)
                
                #--strcd2               
                f_out.write(place)
                
                #--strcd3
                f_out.write(place)
                
                #--strinv
                f_out.write(place)
                
                #--strinv2
                f_out.write(place)
                
                #--strwid
                f_out.write(place)
                
                #--strwid2,strlen,strman
                f_out.write(place+place+place)
                
                #--strval
                f_out.write(raw_13a[4].rjust(11))
                
                #--istrdir
                f_out.write(place)
                
                #--the rest
                for r in raw_13a[5:]:
                    f_out.write(' '+r)
                
                f_out.write('\n    ')
                
                #--write 13b
                
                #--cstrotyp
                f_out.write(raw_13b[0].rjust(11))
                
                #--istrorch
                f_out.write(raw_13b[1].rjust(11))
                
                #--istroqcon
                f_out.write(place)
                
                #--cstrolo
                f_out.write(raw_13b[2].rjust(11))
                
                #--cstrcrit
                f_out.write(raw_13b[3].rjust(11))
                
                #--strcritc
                f_out.write(raw_13b[4].rjust(11))                                    
                
                #--strrt
                f_out.write(raw_13b[5].rjust(11))
                
                #--strmax
                f_out.write(raw_13b[6].rjust(11))
                
                for r in raw_13b[7:]:
                    f_out.write(' '+r)
                f_out.write('\n')
            
            else:
                raise TypeError,'control structure type not supported:'+raw[-1]
    else:
        f_out.write(line_13a)
    
                   
            
        
        
    