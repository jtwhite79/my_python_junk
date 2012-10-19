!------------------------------------------------------------------------
!------------------------------------------------------------------------
!------------------------------------------------------------------------
!------------------------------------------------------------------------
!------------------------------------------------------------------------
!------------------------------------------------------------------------
!------------------------------------------------------------------------
!------------------------------------------------------------------------
!------------------------------------------------------------------------
!------------------------------------------------------------------------
subroutine get_swr_series(ifail)

! -- Subroutine get_swr_flow_series reads a time series from an swr flow binary output file.
! -- Copied blatantly from get_ssf_series

       use tspvar
       use defn
       use inter
       implicit none

       integer, intent(out)   :: ifail

       integer dd1,mm1,yy1,hh1,nn1,ss1,dd2,mm2,yy2,hh2,nn2,ss2,ierr,k,ixcon, &
       icontext,nn,ss,i,iunit,begdays,begsecs,enddays,endsecs,iterm,jline,j,  &
       irchgrpnum, ifiletype, idataidx
       double precision dvalue
       character*10 asite,aname,bsite,afiletype,adatatype
       character*15 aline
       character*20 atemp
       character*25 aoption
       character*120 afile
       character*25 acontext(MAXCONTEXT)      

       ifail=0
       currentblock='GET_SERIES_SWR'

       write(*,10) trim(currentblock)
       write(recunit,10) trim(currentblock)
10     format(/,' Processing ',a,' block....')

       afile=' '
       asite=' '
       acontext(1)=' '
       aname=' '
       afiletype=' '
       icontext=0
       irchgrpnum=-1
       idataidx=-1
       yy1=-9999
       hh1=-9999
       yy2=-9999
       hh2=-9999
       ixcon=0
       iunit=0
       
       !set the file type 1 - flow binary file
       ifiletype=1
       

! -- The GET_SERIES_SWR_FLOW block is first parsed.

       do
         iline=iline+1
         read(inunit,'(a)',err=9000,end=9100) cline
         if(cline.eq.' ') cycle
         if(cline(1:1).eq.'#') cycle
         call linesplit(ierr,2)
         if(ierr.ne.0)then
           call num2char(iline,aline)
           call addquote(infile,astring)
           write(amessage,20) trim(aline),trim(astring)
20         format('there should be 2 entries on line ',a,' of file ',a)
           go to 9800
         end if
         aoption=cline(left_word(1):right_word(1))
         call casetrans(aoption,'hi')
         if(aoption.ne.'CONTEXT')then
           call test_context(ierr,icontext,acontext)
           if(ierr.eq.-1)then
             call find_end(ifail)
             if(ifail.eq.1) go to 9800
             return
           else if(ierr.eq.1) then
             go to 9800
           end if
           ixcon=1
         end if
         if(aoption.eq.'FILE')then
           call read_file_name(ierr,afile)
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'DATE_1')then
           call read_date(ierr,dd1,mm1,yy1,'DATE_1')
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'TIME_1')then
           call read_time(ierr,hh1,nn1,ss1,'TIME_1')
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'NEW_SERIES_NAME')then
           call read_new_series_name(ierr,aname)
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'DATA_TYPE')then
           call swr_read_data_type(ierr,idataidx,adatatype)
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'REACH_GROUP_NUMBER')then
           call swr_read_reach_group_number(ierr,irchgrpnum)
           if(ierr.ne.0) go to 9800
         !else if(aoption.eq.'FILE_TYPE')then
         !  call swr_read_file_type(ierr,afiletype,ifiletype)
         !  if(ierr.ne.0) go to 9800
         else if(aoption.eq.'CONTEXT')then
           if(ixcon.ne.0)then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,41) trim(aline),trim(astring)
41           format('CONTEXT keyword in incorrect location at line ',a,' of file ',a)
             go to 9800
           end if
           call read_context(ierr,icontext,acontext)
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'END')then
           go to 100
         else
           call num2char(iline,aline)
           call addquote(infile,astring)
           write(amessage,80) trim(aoption),trim(currentblock),trim(aline),trim(astring)
80         format('unexpected keyword - "',a,'" in ',a,' block at line ',a, &
           ' of file ',a)
           go to 9800
         end if
       end do
       
       !parsing was good, so check errors
       
       100    continue
       if(afile.eq.' ')then
         call addquote(infile,astring)
         write(amessage,110) trim(currentblock),trim(astring)
110      format('no FILE keyword provided in ',a,' block in file ',a)
         go to 9800
       end if
       if(icontext.eq.0)then
         call addquote(infile,astring)
         write(amessage,122) trim(currentblock),trim(astring)
122      format('no CONTEXT keyword provided in ',a,' block in file ',a)
         go to 9800
       end if
!       if(afiletype.eq.' ')then
!         call addquote(infile,astring)
!         write(amessage,125) trim(currentblock),trim(astring)
!125      format('no FILE_TYPE keyword provided in ',a,' block in file ',a)
!         go to 9800
!       end if
       if(irchgrpnum.eq.-1)then
         call addquote(infile,astring)
         write(amessage,126) trim(currentblock),trim(astring)
126      format('no REACH_GROUP_NUMBER keyword provided in ',a,' block in file ',a)
         go to 9800
       end if
       if(idataidx.eq.-1)then
         call addquote(infile,astring)
         write(amessage,127) trim(currentblock),trim(astring)
127      format('no DATA_TYPE keyword provided in ',a,' block in file ',a)
         go to 9800  
       end if
       if(aname.eq.' ')then
         call addquote(infile,astring)
         write(amessage,128) trim(currentblock),trim(astring)
128      format('no NEW_SERIES_NAME keyword provided in ',a,' block in file ',a)
         go to 9800
      end if
        
      call date_check(ierr,yy1,mm1,dd1,hh1,nn1,ss1,yy2,mm2,dd2,hh2,nn2,ss2,  &
      begdays,begsecs,enddays,endsecs)
      if(ierr.ne.0) go to 9800
       
      !entries look good, so let's read... 
      call read_swr_binary(ierr,irchgrpnum,ifiletype,idataidx,afile,aname,yy1,mm1,dd1,hh1,nn1,ss1,begdays,begsecs)
      if(ierr.ne.0) go to 9800
      return
       
       
              
9000   call num2char(iline,aline)
       call addquote(infile,astring)
       write(amessage,9010) trim(aline), trim(astring)
9010   format('cannot read line ',a,' of TSPROC input file ',a)
       go to 9800
9100   continue
       call addquote(infile,astring)
       write(amessage,9110) trim(astring),trim(currentblock)
9110   format('unexpected end encountered to TSPROC input file ',a,' while ', &
       ' reading ',a,' block.')
       go to 9800

9200   call num2char(jline,aline)
       call addquote(afile,astring)
       write(amessage,9210) trim(aline),trim(astring)
9210   format('unable to read line ',a,' of file ',a)
       go to 9800

9800   call write_message(leadspace='yes',error='yes')
       call write_message(iunit=recunit,leadspace='yes')
       ifail=1
       
end subroutine get_swr_series







subroutine get_mul_swr_series(ifail)

! -- Subroutine get_swr_flow_series reads a time series from an swr flow binary output file.
! -- Copied blatantly from get_ssf_series

       use tspvar
       use defn
       use inter
       implicit none

       integer, intent(out)   :: ifail

       integer dd1,mm1,yy1,hh1,nn1,ss1,dd2,mm2,yy2,hh2,nn2,ss2,ierr,k,ixcon, &
       icontext,nn,ss,i,iunit,begdays,begsecs,enddays,endsecs,iterm,jline,j,  &
       ifiletype, idataidx,jseries,kseries,isite,iseriesname
       integer, dimension(:) ,allocatable :: jjseries,irchgrpnum
       double precision dvalue
       character*10 asite,bsite,afiletype,adatatype
       character*15 aline
       character*20 atemp
       character*25 aoption
       character*120 afile
       character*25, dimension(:),allocatable :: acontext
       character*10, dimension(:),allocatable :: aname


       allocate(jjseries(MAXSERIES),irchgrpnum(MAXSERIES))
       allocate(acontext(MAXCONTEXT),aname(MAXSERIES))
       
       ifail=0
       currentblock='GET_MUL_SERIES_SWR'

       write(*,10) trim(currentblock)
       write(recunit,10) trim(currentblock)
10     format(/,' Processing ',a,' block....')

       afile=' '
       asite=' '
       acontext(1)=' '
       aname=' '
       afiletype=' '
       icontext=0
       irchgrpnum=-1
       idataidx=-1
       yy1=-9999
       hh1=-9999
       yy2=-9999
       hh2=-9999
       ixcon=0
       iunit=0
       jseries=0
       kseries=0
       isite=1
       iseriesname=0
       
       !set the file type 1 - flow binary file
       ifiletype=1
       

! -- The GET_SERIES_SWR_FLOW block is first parsed.

       do
         iline=iline+1
         read(inunit,'(a)',err=9000,end=9100) cline
         if(cline.eq.' ') cycle
         if(cline(1:1).eq.'#') cycle
         call linesplit(ierr,2)
         if(ierr.ne.0)then
           call num2char(iline,aline)
           call addquote(infile,astring)
           write(amessage,20) trim(aline),trim(astring)
20         format('there should be 2 entries on line ',a,' of file ',a)
           go to 9800
         end if
         aoption=cline(left_word(1):right_word(1))
         call casetrans(aoption,'hi')
         if(aoption.ne.'CONTEXT')then
           call test_context(ierr,icontext,acontext)
           if(ierr.eq.-1)then
             call find_end(ifail)
             if(ifail.eq.1) go to 9800
             return
           else if(ierr.eq.1) then
             go to 9800
           end if
           ixcon=1
         end if
         if(aoption.eq.'FILE')then
           call read_file_name(ierr,afile)
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'DATE_1')then
           call read_date(ierr,dd1,mm1,yy1,'DATE_1')
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'TIME_1')then
           call read_time(ierr,hh1,nn1,ss1,'TIME_1')
           if(ierr.ne.0) go to 9800
         
         else if(aoption.eq.'DATA_TYPE')then
           call swr_read_data_type(ierr,idataidx,adatatype)
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'REACH_GROUP_NUMBER')then
           if(isite.eq.0)then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,42) trim(currentblock),trim(aline),trim(astring)
42           format('SITE keyword in wrong position in ',a,' block at line ',a, &
             ' of file ',a)
             go to 9800
           end if 
           
           jseries=jseries+1
45         kseries=kseries+1
           if(kseries.gt.MAXSERIES)then
             write(amessage,44) trim(currentblock)
44           format('too many new series cited in ',a,' block. Increase MAXSERIES ', &
             'and re-compile program.')
             go to 9800
           end if
           if(series(kseries)%active) go to 45
           jjseries(jseries)=kseries
           call swr_read_reach_group_number(ierr,irchgrpnum(jseries))
           if(ierr.ne.0)then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,57) trim(aline),trim(astring)
57           format('cannot read REACH_GROUP_NUMBER name from line ',a,' of file ',a)
             go to 9800
           end if
           isite=0
           iseriesname=1
         else if(aoption.eq.'NEW_SERIES_NAME')then
           if(iseriesname.eq.0)then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,43) trim(currentblock),trim(aline),trim(astring)
43           format('NEW_SERIES_NAME keyword can only follow a SITE ',  &
             'keyword in ',a,' block at line ',a,' of file ',a)
             go to 9800
           end if
           call read_new_series_name(ierr,aname(jseries))
           if(ierr.ne.0) go to 9800           
           if(jseries.gt.1)then
             do j=1,jseries-1
               if(aname(jseries).eq.aname(j))then
                 write(amessage,146) trim(aname(jseries)),trim(currentblock)
146               format('SERIES_NAME "',a,'" used more than once in ',a,' block.')
                 go to 9800
               end if
             end do
           end if
           iseriesname=0
           isite=1
           
         !else if(aoption.eq.'FILE_TYPE')then
         !  call swr_read_file_type(ierr,afiletype,ifiletype)
         !  if(ierr.ne.0) go to 9800
         else if(aoption.eq.'CONTEXT')then
           if(ixcon.ne.0)then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,41) trim(aline),trim(astring)
41           format('CONTEXT keyword in incorrect location at line ',a,' of file ',a)
             go to 9800
           end if
           call read_context(ierr,icontext,acontext)
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'END')then
           go to 100
         else
           call num2char(iline,aline)
           call addquote(infile,astring)
           write(amessage,80) trim(aoption),trim(currentblock),trim(aline),trim(astring)
80         format('unexpected keyword - "',a,'" in ',a,' block at line ',a, &
           ' of file ',a)
           go to 9800
         end if
       end do
       
       !parsing was good, so check errors      
       100    continue
       if(afile.eq.' ')then
         call addquote(infile,astring)
         write(amessage,110) trim(currentblock),trim(astring)
110      format('no FILE keyword provided in ',a,' block in file ',a)
         go to 9800
       end if
       if(icontext.eq.0)then
         call addquote(infile,astring)
         write(amessage,122) trim(currentblock),trim(astring)
122      format('no CONTEXT keyword provided in ',a,' block in file ',a)
         go to 9800
       end if
!       if(afiletype.eq.' ')then
!         call addquote(infile,astring)
!         write(amessage,125) trim(currentblock),trim(astring)
!125      format('no FILE_TYPE keyword provided in ',a,' block in file ',a)
!         go to 9800
!       end if

       if(idataidx.eq.-1)then
         call addquote(infile,astring)
         write(amessage,127) trim(currentblock),trim(astring)
127      format('no DATA_TYPE keyword provided in ',a,' block in file ',a)
         go to 9800  
       end if
       
      call date_check(ierr,yy1,mm1,dd1,hh1,nn1,ss1,yy2,mm2,dd2,hh2,nn2,ss2,  &
      begdays,begsecs,enddays,endsecs)
      if(ierr.ne.0) go to 9800
      
      !entries look good, so let's read... 
      call read_swr_binary_mul(ierr,jseries,irchgrpnum,ifiletype,idataidx,jjseries,afile,aname,yy1,mm1,dd1,hh1,nn1,ss1,begdays,begsecs)
      
      deallocate(jjseries,irchgrpnum,acontext,aname)      
      if(ierr.ne.0) go to 9800                  
      return
       
       
              
9000   call num2char(iline,aline)
       call addquote(infile,astring)
       write(amessage,9010) trim(aline), trim(astring)
9010   format('cannot read line ',a,' of TSPROC input file ',a)
       go to 9800
9100   continue
       call addquote(infile,astring)
       write(amessage,9110) trim(astring),trim(currentblock)
9110   format('unexpected end encountered to TSPROC input file ',a,' while ', &
       ' reading ',a,' block.')
       go to 9800

9200   call num2char(jline,aline)
       call addquote(afile,astring)
       write(amessage,9210) trim(aline),trim(astring)
9210   format('unable to read line ',a,' of file ',a)
       go to 9800

9800   call write_message(leadspace='yes',error='yes')
       call write_message(iunit=recunit,leadspace='yes')
       ifail=1
       
end subroutine get_mul_swr_series



subroutine read_swr_binary_mul(ifail,jseries,irchgrpnum,ifiletype,idataidx,jjseries,afile,aname,yy,mm,dd,hh,nn,ss, &
                           begdays,begsecs)
                           
       !copied from ReadSWRBinary  
                         
       use tspvar
       use defn
       use inter
       implicit none
       
           ! Variables
       integer, intent(out)               :: ifail
       integer, intent(in)                :: jseries
       integer, intent(in),dimension(jseries)  :: irchgrpnum
       integer, intent(in)                :: ifiletype
       integer, intent(in)                :: idataidx
       integer, intent(in)                :: yy,mm,dd,hh,nn,ss,begdays,begsecs       
       integer, intent(in),dimension(jseries)  :: jjseries
       
       character (len=120),intent(in)   :: afile
       character (len=10), intent(in), dimension(:) :: aname
       
       !number of items to read for each flow record
       integer, parameter               ::flow_items = 14
           
          
       character (len=128) :: fname
       character (len=6)   :: crch,timestring
       character (len=10)  :: aaname
       integer (kind=8) :: ios,iunit
       integer (kind=4) :: ncompele
       integer (kind=4) :: nreaches
       integer (kind=4) :: irch
       integer (kind=4) :: iterm
       integer (kind=4) :: kper, kstp, swrstp, outtimes, ierr
       integer (kind=4) :: idays,isecs,thisy,thism,thisd,thish,thisn,thiss
       integer (kind=4) :: offday,offsec       
       real (kind=8), dimension(:), allocatable :: stage
       real (kind=8), dimension(:), allocatable :: flow   
       real (kind=8) :: tottime, swrtime, dt, rdays,rsecs
       integer (kind=8) :: i, k, j
       real (kind=8) :: flowscale
       real (kind=4), dimension(:), allocatable :: dvalue
       
       !get the day and second offset of the series 
       offday=numdays(1,1,1970,dd,mm,yy)
       offsec=(((hh*24)+nn)*60)+ss
       
       iunit=nextunit() 
       open (unit=iunit,file=afile,status='old',form='binary',iostat=ios)
       if (ios /= 0) then
          write (amessage,*) 'could not open swr binary file: '//trim(adjustl(fname))
          goto 9999
        end if       
        select case (ifiletype)
            !computational element flow data
          case (1)
            !read the number of reachgroups from the first of the file            
            read (iunit) ncompele
            
            !--more error checking
            do j=1,jseries                
                write(*,*)'checking reachgroup: ',irchgrpnum(j)
                if (irchgrpnum(j).lt.1) then          
                  write (amessage,*) 'irchgrpnum number must be greater than zero'
                  goto 9999
                end if
                if (irchgrpnum(j).gt.ncompele) then
                  write (amessage,'(a,1x,i10)') 'irchgrpnum exceeds total number of reach groups ',ncompele
                  goto 9999
                end if
            end do
            
            !read the file once to determine length 
            iterm = 0
            allocate(flow(flow_items))
            do
              read (iunit,iostat=ios) tottime, dt, kper, kstp, swrstp
              if (ios /= 0) exit   
              iterm = iterm + 1                        
              do i = 1, ncompele
                read (iunit,iostat=ios) flow                                            
              end do
            end do    
            
            !--allocate series for each reachgroup
            do j=1,jseries              
              k=jjseries(j)               
              allocate(series(k)%days(iterm),series(k)%secs(iterm),stat=ierr)
              if(ierr.ne.0)then
                write(amessage,550)
550             format('cannot allocate memory for another time series.')
                go to 9999
              end if  
              allocate(series(k)%val(iterm),stat=ierr)
              if(ierr.ne.0)then
                write(amessage,550)
                go to 9999
              end if
              series(k)%active=.true.
              series(k)%name=aname(j)
              series(k)%type='ts'
              series(k)%nterm=iterm                
            end do
            
            allocate(dvalue(ncompele))           
            rewind(unit=iunit,iostat=ierr)            
            if(ierr.ne.0)then
              write(amessage,370) trim(astring)
370           format('cannot rewind swr binary file ',a)             
              go to 9999
            end if            
            read (iunit) ncompele  
            
            iterm = 0            
            do j=1,jseries
                do
                  read (iunit,iostat=ios) tottime, dt, kper, kstp, swrstp
                  if (ios /= 0) exit
                  call swr_tottime2daysec(tottime,idays,isecs)
                  idays = idays + offday
                  isecs = isecs + offsec
                                                      
                  do i = 1, ncompele
                    read (iunit,iostat=ios) flow            
                    dvalue(i) = flow(idataidx)
                  end do
                  iterm=iterm+1
                  do i=1,jseries
                    series(jjseries(i))%days(iterm) = idays  
                    series(jjseries(i))%secs(iterm) = isecs 
                    series(jjseries(i))%val(iterm) = dvalue(irchgrpnum(i))   
                  end do                                                    
                end do                 
             end do
             deallocate (flow,dvalue)
       end select
       
       do j=1,jseries
         aaname = series(jjseries(j))%name
         write(recunit,580) trim(aaname),trim(astring)
         write(*,580) trim(aaname),trim(astring)
580      format(t5,'Series "',a,'" successfully imported from file ',a)
       end do
       close(iunit)
       return 
           
9999   call write_message(leadspace='yes',error='yes')
       call write_message(iunit=recunit,leadspace='yes')
       if(iunit.ne.0)close(iunit)
       ifail=1           
end subroutine read_swr_binary_mul


subroutine read_swr_binary(ifail,irchgrpnum,ifiletype,idataidx,afile,aname,yy,mm,dd,hh,nn,ss, &
                           begdays,begsecs)
                           
       !copied from ReadSWRBinary  
                         
       use tspvar
       use defn
       use inter
       implicit none
       
           ! Variables
       integer, intent(out)             :: ifail
       integer, intent(in)              :: irchgrpnum
       integer, intent(in)              :: ifiletype
       integer, intent(in)              :: idataidx
       integer, intent(in)              :: yy,mm,dd,hh,nn,ss,begdays,begsecs
       
       character (len=120),intent(in)   :: afile
       character (len=10), intent(in)   :: aname
       
       !number of items to read for each flow record
       integer, parameter               ::flow_items = 14
           
          
       character (len=128) :: fname
       character (len=6)   :: crch,timestring
       integer (kind=8) :: ios,iunit
       integer (kind=4) :: ncompele
       integer (kind=4) :: nreaches
       integer (kind=4) :: irch
       integer (kind=4) :: iterm
       integer (kind=4) :: kper, kstp, swrstp, outtimes, ierr
       integer (kind=4) :: idays,isecs,thisy,thism,thisd,thish,thisn,thiss
       integer (kind=4) :: offday,offsec
       real (kind=8), dimension(:), allocatable :: stage
       real (kind=8), dimension(:), allocatable :: flow   
       real (kind=8) :: tottime, swrtime, dt, rdays,rsecs
       integer (kind=8) :: i, k, j
       real (kind=8) :: flowscale
       real (kind=4) :: dvalue
       
       !get the day and second offset of the series 
       offday=numdays(1,1,1970,dd,mm,yy)
       offsec=(((hh*24)+nn)*60)+ss
       
       iunit=nextunit() 
       open (unit=iunit,file=afile,status='old',form='binary',iostat=ios)
       if (ios /= 0) then
          write (amessage,*) 'could not open swr binary file: '//trim(adjustl(fname))
          goto 9999
        end if

        select case (ifiletype)
            !computational element flow data
          case (1)
            !read the number of reachgroups from the first of the file
            read (iunit) ncompele                
            if (irchgrpnum.lt.1.and.irchgrpnum.ne.-999) then          
              write (amessage,*) 'irchgrpnum number must be greater than zero'
              goto 9999
            end if
            if (irchgrpnum.gt.ncompele) then
              write (amessage,'(a,1x,i10)') 'irchgrpnum exceeds total number of reach groups ',ncompele
              goto 9999
            end if
            
            !read the file once to determine length 
            iterm = 0
            allocate(flow(flow_items))
            do
              read (iunit,iostat=ios) tottime, dt, kper, kstp, swrstp
              iterm = iterm + 1
              if (ios /= 0) exit              
              do i = 1, ncompele
                read (iunit,iostat=ios) flow            
                !if (i == irchgrpnum) then                  
                !end if
                
              end do
            end do    
            
            !allocate a temporary series
            call alloc_tempseries(ierr,iterm)
            rewind(unit=iunit,iostat=ierr)
            !close(iin)
            !open (unit=iin,file=afile,status='old',form='binary',iostat=ios)
            if(ierr.ne.0)then
              write(amessage,370) trim(astring)
370           format('cannot rewind swr binary file ',a)
              deallocate (flow)
              go to 9999
            end if
            !re-read number of reachgroups
            read (iunit) ncompele  
            iterm = 0            
            do
              read (iunit,iostat=ios) tottime, dt, kper, kstp, swrstp
              if (ios /= 0) exit
              call swr_tottime2daysec(tottime,idays,isecs)
              idays = idays + offday
              isecs = isecs + offsec

              !call newdate(idays,dd,mm,yy,thisd,thism,thisy)
              !call swr_sectime(isecs,thiss,thisn,thish)
              
              dvalue = 0.0
              do i = 1, ncompele
                read (iunit,iostat=ios) flow            
                
                if (i == irchgrpnum.and.irchgrpnum.ne.-999) then
                  !write (*,'(2(e15.9,","),3(i10,","),12(e15.9,:","))') &
                  !  tottime, dt, kper, kstp, swrstp, flow
                  dvalue = flow(idataidx)
                  
                end if
                if (irchgrpnum.eq.-999) then
                  dvalue = dvalue + flow(idataidx)                                                      
                end if
              end do
              iterm=iterm+1
              tempseries%days(iterm)=idays
              tempseries%secs(iterm)=isecs
              tempseries%val(iterm)=dvalue
            end do 

            deallocate (flow)
       end select
       
       
       do i=1,MAXSERIES
         if(.not.series(i)%active) go to 515
       end do
       write(amessage,510)
510    format('no more time series available for data storage - increase MAXSERIES and ', &
       'recompile program.')
       go to 9999

515    allocate(series(i)%days(iterm),series(i)%secs(iterm),  &
       series(i)%val(iterm),stat=ierr)
       if(ierr.ne.0)then
         write(amessage,550)
550      format('cannot allocate memory for another time series.')
         go to 9999
       end if
       series(i)%active=.true.
       series(i)%name=aname
       series(i)%nterm=iterm
       series(i)%type='ts'
       do j=1,iterm
         series(i)%days(j)=tempseries%days(j)
       end do
       do j=1,iterm
         series(i)%secs(j)=tempseries%secs(j)
       end do
       do j=1,iterm
         series(i)%val(j)=tempseries%val(j)
       end do
       call addquote(afile,astring)
       write(*,580) trim(aname),trim(astring)
       write(recunit,580) trim(aname),trim(astring)
580    format(t5,'Series "',a,'" successfully imported from file ',a)
       close(iunit)
       return 
           
9999   call write_message(leadspace='yes',error='yes')
       call write_message(iunit=recunit,leadspace='yes')
       if(iunit.ne.0)close(iunit)
       ifail=1
      
      
end subroutine read_swr_binary

subroutine swr_tottime2daysec(tottime,days,secs)

          real (kind=8), intent(in)         :: tottime
          integer, intent(out)        :: days,secs
          
          real (kind=8)               :: rdays,rsecs
          integer                     :: idays,isecs

          if(tottime.eq.0.0)then
            idays = 0
            isecs = 0                
          else if(tottime.lt.1.0)then
            idays = 0
            rsecs = tottime * 86400.0
            isecs = idint(rsecs)
          else 
            rdays = floor(tottime)
            idays = idnint(rdays)
            rsecs = modulo(tottime,rdays) * 86400.0
            isecs = idnint(rsecs)
          end if
          
          if(isecs.eq.86400)then
            idays = idays + 1
            isecs = 0  
          end if
          days = idays
          secs = isecs
          
          return
end subroutine swr_tottime2daysec


subroutine swr_read_reach_group_number(ifail,irchgrpnum)
       use tspvar
       use defn
       use inter
       implicit none

       integer, intent(out)         :: irchgrpnum
       integer, intent(out)         :: ifail
       integer ierr
       character*20 aline
       
       
       irchgrpnum = -1
       ierr = 0
       
       call a2i(ierr,cline(left_word(2):right_word(2)),irchgrpnum)
       if(ierr.ne.0)then
         call num2char(iline,aline)
         call addquote(infile,astring)
         write(amessage,78) trim(aline),trim(astring)
78       format('cannot read REACH_GROUP_NUMBER from line ',a,' of file ',a)
         go to 9800
       end if
       write(*,90) irchgrpnum
       write(recunit,90) irchgrpnum
90     format(t5,'REACH_GROUP_NUMBER ',i10)
       
       return
9800   ifail = 1
                    
end subroutine swr_read_reach_group_number

subroutine swr_read_data_type(ifail,idataidx,adatatype)
       
       
       use tspvar
       use defn
       use inter
       implicit none

       integer, intent(out)          :: idataidx
       integer, intent(out)          :: ifail
       character*10, intent(out)     :: adatatype
       
       integer ierr
       character*20 aline       
       
       call swr_gettype(ierr,cline,adatatype,left_word(2),right_word(2))
       select case(trim(adatatype))
         case('stage')
          idataidx = 1
         case('qsflow')
          idataidx = 2
         case('qlatflow')
          idataidx = 3
         case('quzflow')
          idataidx = 4
         case('rain')
          idataidx = 5
         case('evap')
          idataidx = 6
         case('qbflow')
          idataidx = 7
         case('qeflow')          
          idataidx = 8
         case('qexflow')
          idataidx = 9
         case('qbcflow')
          idataidx = 10
         case('qcrflow')
          idataidx = 11
         case('dv')
          idataidx = 12
         case('in-out')
          idataidx = 13
         case('volume')
          idataidx = 14
         case default
          call num2char(iline,aline)
          write(amessage,80) trim(adatatype),trim(aline)
80       format('invalid DATA_TYPE ',a,' on line ',a, &
                '. must be one of: stage qsflow qlatflow ' &
                'quzflow rain evap qbflow qeflow qexflow qbcflow ' & 
                'qcrflow dv in-out volume.  See SWR manual.')
         go to 9800
      end select
      
      write(*,81) adatatype
      write(recunit,81) adatatype
81    format(t5,'DATA_TYPE ',a)
      

      return
9800  ifail = 1
      
end subroutine swr_read_data_type

subroutine swr_read_file_type(ifail,afiletype,ifiletype)
       use tspvar
       use defn
       use inter
       implicit none
       integer, intent(out)          :: ifail
       integer, intent(out)          :: ifiletype

       integer ierr
       character*20 aline
       character*10, intent(out)     :: afiletype       
       
       afiletype = ' '
       ierr = 0

       call swr_gettype(ierr,cline,afiletype,left_word(2),right_word(2))
       if(ierr.ne.0)then
         call num2char(iline,aline)
         call addquote(infile,astring)
         write(amessage,78) trim(aline),trim(astring)
78       format('cannot read FILE_TYPE from line ',a,' of file ',a)
         go to 9800
       end if
       write(*,79) trim(afiletype)
       write(recunit,79) trim(afiletype)
79     format(t5,'FILE_TYPE ',a)
       call casetrans(afiletype,'lo')
      !if(trim(afiletype).eq.'stage')then
      !    ifiletype = 2
      if(trim(afiletype).eq.'flow')then
         ifiletype = 1
      else
         call num2char(iline,aline)
         call addquote(infile,astring)
         write(amessage,80) trim(aline),trim(astring)
80       format('invalid FILE_TYPE on line ',a,' of file ',a, &
                'must be "flow"')
         go to 9800
      end if

      return
9800  ifail = 1
end subroutine swr_read_file_type

subroutine swr_gettype(ifail,cline,filetype,ibeg,iend)

! Subroutine swr_gettype extracts a type from a string.

! -- Arguments are as follows:-
!       ifail: returned as zero if filename successfully read
!       cline: a character string containing the file name
!       filetype: the swr filetype read from the string
!       ibeg: character position at which to begin search for filetype
!       iend: on input  - character position at which to end search for filetype
!             on output - character postion at which filename ends

       
        integer, intent(out)               :: ifail
        integer, intent(in)                :: ibeg
        integer, intent(inout)             :: iend
        character (len=*), intent(in)      :: cline
        character (len=*), intent(out)     :: filetype

        integer                            :: i,j,k
        character (len=1)                  :: aa

        ifail=0
        do i=ibeg,iend
          aa=cline(i:i)
          if((aa.ne.' ').and.(aa.ne.',').and.(aa.ne.char(9)))go to 50
        end do
        ifail=1
        return

50      if((aa.eq.'"').or.(aa.eq.''''))then
!          do j=i+1,iend
          do j=i+1,len_trim(cline)              !note
            if(cline(j:j).eq.aa) go to 60
          end do
          ifail=1
          return
60        iend=j
          if(i+1.gt.j-1)then
            ifail=1
            return
          else
            filetype=cline(i+1:j-1)
          end if
        else
          do j=i+1,iend
            if((cline(j:j).eq.' ').or.(cline(j:j).eq.',').or.(cline(j:j).eq.char(9)))then
              k=j-1
              go to 100
            end if
          end do
          k=iend
100       filetype=cline(i:k)
          if(cline(k:k).eq.'"')then
            ifail=1
            return
          else if(cline(k:k).eq.'''')then
            ifail=1
            return
          end if

          iend=k
        end if
        filetype=adjustl(filetype)
        return

end subroutine swr_gettype

