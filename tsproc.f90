!     Last change:  JD   26 Aug 2003    1:42 pm
MODULE DEFN

! -- File DEFN.F90 contains definitions for defined types and global variables.


!****************************************************************************
! defined types        
!****************************************************************************
	
	type modelgrid
	  integer                         :: nrow,ncol
	  double precision                :: east_corner,north_corner,rotation
	  real                            :: cosang,sinang
	  real, dimension(:), pointer     :: delr,delc
	  integer                         :: specunit,specline
	  character (len=80)              :: specfile
	end type modelgrid

!****************************************************************************
!global variables
!****************************************************************************

!variables for reading a file ------->

	integer, parameter              	:: NUM_WORD_DIM=1000
	integer, dimension(NUM_WORD_DIM)        :: left_word,right_word
	character (len=3000)             	:: cline


!variables for writing a message ------->
	
	integer                 :: imessage=0
	character (len=500)     :: amessage= ' '
	character (len=200)     :: initial_message=' '


!escape variables ------->

	integer                 :: escset=0
	character (len=5)       :: eschar = 'E ~e '


!variables in bore data manipulation ------->
	
	integer                         :: num_bore_coord, num_bore_list
	character (len=120)             :: bore_coord_file, bore_list_file
	integer, dimension(:), pointer			:: bore_coord_layer
	double precision, dimension(:), pointer         :: bore_coord_east, &
							   bore_coord_north
	character (len=10), dimension(:), pointer       :: bore_coord_id, &
                                                           bore_list_id

!variables recording data settings ------->

	integer				:: datespec


END MODULE DEFN
!     Last change:  JD   24 Aug 2001    2:49 pm
MODULE INTER

! -- Contains interface blocks for all subprograms.


!******************************************************************************
! generic subprograms
!******************************************************************************

interface char2num

	subroutine a2i(ifail,string,num)
	  integer, intent(out)          :: ifail
	  character (len=*), intent(in) :: string
	  integer, intent(out)          :: num
	end subroutine a2i
	subroutine a2r(ifail,string,num)
	  integer, intent(out)          :: ifail
	  character (len=*), intent(in) :: string
	  real, intent(out)             :: num
	end subroutine a2r
	subroutine a2d(ifail,string,num)
	  integer, intent(out)          :: ifail
	  character (len=*), intent(in) :: string
	  double precision, intent(out) :: num
	end subroutine a2d

end interface


interface num2char

	subroutine i2a(value,string,nchar)
	  integer, intent(in)           :: value
	  character (len=*), intent(out):: string
	  integer, intent(in), optional :: nchar
	end subroutine i2a
	subroutine r2a(value,string,nchar)
	  real, intent(in)              :: value
	  character (len=*), intent(out):: string
	  integer, intent(in), optional :: nchar
	end subroutine r2a
	subroutine d2a(value,string,nchar)
	  double precision, intent(in)  :: value
	  character (len=*), intent(out):: string
	  integer, intent(in), optional :: nchar
	end subroutine d2a

end interface


interface pos_test

	integer function pos_i_test(value,string)
	  integer, intent(in)           :: value
	  character (len=*), intent(in) :: string
	end function pos_i_test
	integer function pos_r_test(value,string)
	  real, intent(in)              :: value
	  character (len=*), intent(in) :: string
	end function pos_r_test
	integer function pos_d_test(value,string)
	  double precision, intent(in)  :: value
	  character (len=*), intent(in) :: string
	end function pos_d_test

end interface


interface nneg_test

	integer function nneg_i_test(value,string)
	  integer, intent(in)           :: value
	  character (len=*), intent(in) :: string
	end function nneg_i_test
	integer function nneg_r_test(value,string)
	  real, intent(in)              :: value
	  character (len=*), intent(in) :: string
	end function nneg_r_test
	integer function nneg_d_test(value,string)
	  double precision, intent(in)  :: value
	  character (len=*), intent(in) :: string
	end function nneg_d_test

end interface


interface key_read

	integer function int_key_read(value)
	  integer,intent(out)   :: value
	end function int_key_read
	integer function real_key_read(value)
	  real,intent(out)      :: value
	end function real_key_read
	integer function double_key_read(value)
	  double precision,intent(out)  :: value
	end function double_key_read

end interface


interface equals

       logical function equals_int(r1,r2)
          integer, intent(in)    :: r1
          integer, intent(in)    :: r2
       end function equals_int

       logical function equals_real(r1,r2)
          real, intent(in)      :: r1
          real, intent(in)      :: r2
       end function equals_real

       logical function equals_dbl(r1,r2)
          real (kind (1.0d0)), intent(in)      :: r1
          real (kind (1.0d0)), intent(in)      :: r2
       end function equals_dbl

end interface

interface swr
     subroutine read_swr_binary_mul(ifail,jseries,irchgrpnum,ifiletype,idataidx,  &
                                    jjseries,afile,aname,yy,mm,dd,hh,nn,ss,   &
                                    begdays,begsecs)
       integer, intent(out)               :: ifail
       integer, intent(in)                :: jseries
       integer, intent(in),dimension(jseries)  :: irchgrpnum
       integer, intent(in)                :: ifiletype
       integer, intent(in)                :: idataidx
       integer, intent(in)                :: yy,mm,dd,hh,nn,ss,begdays,begsecs       
       integer, intent(in),dimension(jseries)  :: jjseries
       
       character (len=120),intent(in)   :: afile
       character (len=10), intent(in), dimension(:) :: aname
     end subroutine read_swr_binary_mul
 end interface
      
        
        
        
        
        

!******************************************************************************
! other subprograms
!******************************************************************************

! utility subprograms ------->

interface

	subroutine casetrans(string,hi_or_lo)
	  character (len=*), intent(inout)        :: string
	  character (len=*), intent(in)           :: hi_or_lo
	end subroutine casetrans

	subroutine sub_error(subname)
	  character (len=*)               ::subname
	end subroutine sub_error

	integer function nextunit()
	end function nextunit

	subroutine close_files
	end subroutine close_files

	subroutine open_input_file(ifail,aprompt,infile,inunit,file_format)
          integer, intent(out)                    :: ifail
          character (len=*), intent(in)           :: aprompt
          character (len=*), intent(out)          :: infile
          integer, intent(out)                    :: inunit
          character (len=*), intent(in), optional :: file_format
	end subroutine open_input_file


        subroutine open_named_input_file(ifail,aprompt,infile,inunit)
          integer, intent(out)                    :: ifail
          character (len=*), intent(in)           :: aprompt
          character (len=*), intent(inout)        :: infile
          integer, intent(out)                    :: inunit
        end subroutine open_named_input_file


	subroutine open_output_file(ifail,aprompt,outfile,outunit)
	  integer, intent(out)          :: ifail
	  character (len=*)             :: aprompt,outfile
	  integer, intent(out)          :: outunit
	end subroutine open_output_file

	subroutine readfig(specfile,coordfile,sampfile,pumpfile,pilotfile)
	  character (len=*), intent(out)                :: specfile
	  character (len=*), intent(out), optional      :: coordfile,sampfile,&
							   pumpfile,pilotfile
	end subroutine readfig

	subroutine read_settings(ifail,idate)
	  integer, intent(out)	:: ifail,idate
	end subroutine read_settings

	subroutine char_add(astring,achar)
          character (len=*), intent(inout)        :: astring
          character (len=*), intent(in)           :: achar
	end subroutine char_add

	subroutine int2alph(inum,alph,nsig)
	  integer, intent(in)			:: inum
	  character (len=*), intent(out)	:: alph
	  integer, optional, intent(in)		:: nsig
	end subroutine int2alph

        logical function isspace(astring)
          character (len=*), intent(in)   :: astring
        end function isspace

        subroutine repchar(astring,substring,replacement)
          character (len=*), intent(inout)  :: astring
          character (len=*), intent(in)     :: substring
          character (len=*), intent(in)     :: replacement
        end subroutine

end interface


! reading-a-file subprograms ------->

interface

	subroutine linesplit(ifail,num)
	  integer, intent(out)            :: ifail
	  integer, intent(in)		  :: num
	end subroutine linesplit

	integer function char2int(ifail,num)
	  integer, intent(in)             :: num
	  integer, intent(out)            :: ifail
	end function char2int

	real function char2real(ifail,num)
	  integer, intent(in)             :: num
	  integer, intent(out)            :: ifail
	end function char2real

	double precision function char2double(ifail,num)
	  integer, intent(in)             :: num
	  integer, intent(out)            :: ifail
	end function char2double

        subroutine getfile(ifail,cline,filename,ibeg,iend)
          integer, intent(out)            :: ifail
          integer, intent(in)             :: ibeg
          integer, intent(inout)          :: iend
          character (len=*), intent(in)   :: cline
          character (len=*), intent(out)  :: filename
       end subroutine getfile

       subroutine addquote(afile,aqfile)
          character (len=*), intent(in)   :: afile
          character (len=*), intent(out)  :: aqfile
       end subroutine addquote

end interface


! message subprograms ------->

interface

	subroutine write_initial_message(leadspace,endspace)
	  character (len=*), intent(in), optional :: leadspace,endspace
	end subroutine write_initial_message

	subroutine write_message(increment,iunit,error,leadspace,endspace)
	  integer, intent(in), optional           ::increment,iunit
	  character (len=*), intent(in), optional ::error,leadspace,endspace
	end subroutine write_message

end interface


! site data manipulation subprograms ------->

interface

	subroutine read_rest_of_sample_line(ifail,cols,ndays,nsecs,value, &
	iline,sampfile)
          integer, intent(out)            :: ifail
          integer, intent(in)             :: cols
          integer, intent(out)            :: ndays,nsecs
          double precision, intent(out)   :: value
          integer, intent(in)             :: iline
          character (len=*), intent(in)   :: sampfile
	end subroutine read_rest_of_sample_line

	subroutine time_interp(ifail,nbore,ndays,nsecs,value,intday, &
	intsec,rnear,rconst,valinterp,extrap,direction,startindex)
          integer, intent(out)                    :: ifail
          integer, intent(in)                     :: nbore
          integer, intent(in), dimension(nbore)   :: ndays,nsecs
          double precision, intent(in), dimension(nbore)   :: value
          integer, intent(in)                     :: intday,intsec
	  real, intent(in)			  :: rnear,rconst
          double precision, intent(out)           :: valinterp
	  character (len=*), intent(in),optional  :: extrap
	  character (len=*), intent(in),optional  :: direction
          integer, intent(inout), optional        :: startindex
	end subroutine time_interp

	subroutine get_num_ids(ifail,iunit,afile,numid,maxsamp,ignore_x)
	  integer, intent(out)                    :: ifail
          integer, intent(in)                     :: iunit
          character (len=*), intent(in)           :: afile
          integer, intent(out)                    :: numid,maxsamp
	  character (len=*), intent(in), optional :: ignore_x
	end subroutine get_num_ids

	subroutine get_ids_and_interval(ifail,iunit,afile,nid,aid,ndays1, &
                                nsecs1,ndays2,nsecs2, ignore_x)
          integer, intent(out)                    :: ifail
          integer, intent(in)                     :: iunit
          character (len=*), intent(in)           :: afile
          integer, intent(in)                     :: nid
          character (len=*), intent(out)          :: aid(nid)
          integer, intent(out)                    :: ndays1(nid),nsecs1(nid), &
                                                     ndays2(nid),nsecs2(nid)
	  character (len=*), intent(in), optional :: ignore_x
	end subroutine get_ids_and_interval

        subroutine volume_interp(ifail,num,days,secs,flows,bdays,bsecs,  &
          fdays,fsecs,vol,fac)

          integer, intent(out)            :: ifail
          integer, intent(in)             :: num
          integer, intent(in)             :: days(num),secs(num)
          double precision, intent(in)    :: flows(num)
          integer, intent(in)             :: bdays,bsecs,fdays,fsecs
          double precision, intent(out)   :: vol
          double precision, intent(in)    :: fac
        end subroutine volume_interp


end interface


! date manipulation subprograms ------->

interface

	subroutine char2date(ifail,adate,dd,mm,yy)
          integer, intent(out)    	:: ifail
          character (len=*), intent(in) :: adate
          integer, intent(out) 		:: dd,mm,yy
	end subroutine char2date

	subroutine datestring(dd,mm,yy,hhh,mmm,sss,time,at,adate,atime)
	  integer, intent(in)             :: dd,mm,yy,hhh,mmm,sss
	  real, intent(in)                :: time
	  character (len=1), intent(in)   :: at
	  character (len=*), intent(out)  :: adate, atime
	end subroutine datestring

	logical function leap(year)
          integer, intent(in)     :: year
	end function leap

	integer function numdays(dr,mr,yr,d,m,y)
          integer, intent(in)     :: dr,mr,yr,d,m,y
	end function numdays

	integer function numsecs(h1,m1,s1,h2,m2,s2)
	  integer, intent(in)     :: h1,m1,s1,h2,m2,s2
	end function numsecs

	subroutine char2time(ifail,adate,hh,mm,ss,ignore_24)
          integer, intent(out)    	:: ifail
          character (len=*), intent(in) :: adate
          integer, intent(out) 		:: hh,mm,ss
          integer, optional,intent(in)  :: ignore_24
	end subroutine char2time

	subroutine time2char(ifail,hh,mm,ss,atime)
	  integer, intent(out)            :: ifail
	  integer, intent(in)             :: hh,mm,ss
	  character (len=*), intent(out)  :: atime
	end subroutine time2char

	subroutine elapsdate(eltime,dayfactor,day1,mon1,year1,hour1,min1,sec1,&
	  day2,mon2,year2,hour2,min2,sec2)
	  real, intent(in)		:: eltime,dayfactor
	  integer, intent(in)		:: day1,mon1,year1,hour1,min1,sec1
	  integer, intent(out)		:: day2,mon2,year2,hour2,min2,sec2
	end subroutine elapsdate

	subroutine newdate(ndays,day1,mon1,year1,day2,mon2,year2)
	  integer, intent(in)		:: ndays,day1,mon1,year1
	  integer, intent(out)		:: day2,mon2,year2
	end subroutine newdate

	subroutine sectime(nsecs,sec,min,hour)
	  integer, intent(in)   :: nsecs
	  integer, intent(out)  :: sec,min,hour
	end subroutine sectime

end interface


END MODULE INTER
!     Last change:  J     9 Sep 2004    5:38 pm
module tspvar

       integer, parameter    :: MAXSERIES=100000
       integer, parameter    :: MAXSERIESREAD=50
       integer, parameter    :: MAXSTABLE=300
       integer, parameter    :: MAXCTABLE=500
       integer, parameter    :: MAXCONTEXT=5
       integer, parameter    :: MAXVTABLE=500
       integer, parameter    :: MAXDTABLE=100
       integer, parameter    :: MAXTEMPDURFLOW=300
       integer, parameter    :: MAXTEMPFILE=200
       integer, parameter    :: MAXPAR=50000
       integer, parameter    :: MAXCONST=5000
!       character, parameter  :: OBSCHAR='#'
       character, parameter  :: OBSCHAR='_'

       type time_series
         logical active
         integer nterm
         character*2 type
         character*10 name
         integer, dimension(:), pointer :: days
         integer, dimension(:), pointer :: secs
         real,    dimension(:), pointer :: val
       end type time_series

       type s_table
         logical active
         character*10 name
         character*10 series_name
         real     maximum
         real     minimum
         real     range
         real     mean
         real     stddev
         real     total
         real     minmean
         real     maxmean
         real     rec_power
         integer  rec_icount
         integer  rec_itrans
         integer  rec_begdays
         integer  rec_begsecs
         integer  rec_enddays
         integer  rec_endsecs
         integer  avetime
       end type s_table

       
       type c_table
         logical active
         character*10 name
         character*10 series_name_obs
         character*10 series_name_sim
         real     bias
         real     se
         real     rbias
         real     rse
         real     ns
         real     ce
         real     ia
         integer  rec_icount
         integer  rec_begdays
         integer  rec_begsecs
         integer  rec_enddays
         integer  rec_endsecs
       end type c_table
       
              
       type v_table
         logical active
         character*10 name
         character*10 series_name
         integer nterm
         integer, dimension(:), pointer :: days1
         integer, dimension(:), pointer :: secs1
         integer, dimension(:), pointer :: days2
         integer, dimension(:), pointer :: secs2
         real, dimension(:), pointer    :: vol
       end type v_table


       type d_table
         logical active
         character*10 name
         character*10 series_name
         character*7 time_units
         integer under_over
         integer nterm
         real total_time
         real, dimension(:), pointer     :: flow
         real, dimension(:), pointer     :: tdelay
         real, dimension(:), pointer     :: time
       end type d_table
       
       type constants
         character*25 name
         logical active
         real value
       end type constants
                 
       type (time_series) tempseries
       type (time_series) series(MAXSERIES)
       type (s_table) stable(MAXSTABLE)
       type (c_table) ctable(MAXCTABLE)
       type (v_table) vtable(MAXVTABLE)
       type (d_table) tempdtable
       type (d_table) dtable(MAXDTABLE)
       type (constants) const(MAXCONST)
       
       integer inunit,recunit,outunit
       integer NumProcBlock,ILine,IProcSetting
       character*25 Context
       character*40 CurrentBlock
       character*120 infile,recfile,outfile,astring

! -- The following variables are global because they are used to exchange information
!    between the LIST_OUTPUT block and the WRITE_PEST_FILES block.

       integer imseries
       integer imstable
       integer imctable
       integer imvtable
       integer imdtable
       integer outseries(MAXSERIES),outstable(MAXSTABLE),outvtable(MAXVTABLE), &
               outdtable(MAXDTABLE),outctable(MAXCTABLE)
       character*10 series_format
       character*120 list_output_file

! -- Following are some parameter definitions related to equations.

! -- Maximum terms in any mathematical expression:-
       integer MAXTERM
       parameter(MAXTERM=200)
! -- Maximum number of function types:-
       integer NFUNCT
       parameter(NFUNCT=16)
! -- Maximum number of operators:-
       integer NOPER
       parameter(NOPER=7)
! -- Maximum number of series names in a series equation:-
       integer MAXEQNSER
       parameter (MAXEQNSER=25)

       integer iorder(MAXTERM)
       character*1   operat(7)
       character*6   funct(NFUNCT)
       character*28  aterm(MAXTERM),bterm(MAXTERM),cterm(MAXTERM)
       double precision rterm(MAXTERM), qterm(MAXTERM)

       data funct /'abs   ','acos  ','asin  ','atan  ','cos   ','cosh  ',  &
         'exp   ','log   ','log10 ','sin   ','sinh  ','sqrt  ','tan   ',   &
         'tanh  ','neg   ','pos   '/
       data operat /'^','/','*','-','+','(',')'/

! -- The following pertain to WDM files.

       integer MAXWDOPN
       parameter (MAXWDOPN=10)  ! Number of WDM files that can be open.
       integer iwdopn
       integer wdmun(MAXWDOPN)
       character*120 wdmfil(MAXWDOPN)

end module
 
!     Last change:  J     9 Sep 2004   10:05 pm


program tsproc

! -- Program TSPROC is a general time-series processor. It can also be used for
!    PEST input file preparation.

       use defn
       use inter
       use tspvar

       implicit none

       integer ifail,idate,ierr,nbb,iBlock,i,lastblock
       character*120 afile

       !open(unit=*,carriagecontrol='list')
       open(unit=11,carriagecontrol='list')

! -- Initialisation

       write(amessage,5)
5      format(' Program TSPROC is a general time-series processor. It can ', &
       'also be used for PEST input file preparation where time series data, ', &
       'or processed time series data, comprises at least part of the observation ',&
       'dataset.')
       call write_message(leadspace='yes',endspace='yes')

!       call read_settings(ifail,idate)
!       if(ifail.eq.1) then
!         write(amessage,7)
!7        format(' A settings file (settings.fig) was not found in the ', &
!         'current directory.')
!         go to 9890
!       else if(ifail.eq.2) then
!         write(amessage,8)
!8        format(' Error encountered while reading settings file settings.fig')
!          go to 9890
!       endif
!       if((idate.ne.0).or.(datespec.eq.0)) then
!         write(amessage,9)
!9        format(' Cannot read date format from settings file ', &
!         'settings.fig')
!         go to 9890
!       end if

! -- Some variables are initialised

       series%active=.false.        !series is an array
       stable%active=.false.        !stable is an array
       vtable%active=.false.        !vtable is an array
       dtable%active=.false.        !dtable is an array
       ctable%active=.false.        !ctable is an array
       tempseries%active=.false.
       const%active=.false.

       tempdtable%active=.true.
       allocate(tempdtable%flow(MAXTEMPDURFLOW),   &
                tempdtable%time(MAXTEMPDURFLOW),   &
                tempdtable%tdelay(MAXTEMPDURFLOW),stat=ierr)
       if(ierr.ne.0)then
         write(amessage,16)
16       format(' Cannot allocate sufficient memory to store temporary E_TABLE.')
         go to 9890
       end if

4      imessage=0
6      if(imessage.eq.5) go to 9900
11     write(6,15,advance='no')
15     format(' Enter name of TSPROC input file: ')
       read(5,'(a)') infile
       !infile = 'tsproc.dat'
       if(infile.eq.' ') go to 11
       infile=adjustl(infile)
       if(index(eschar,infile(1:2)).ne.0) go to 9900
       nbb=len_trim(infile)
       call getfile(ifail,infile,afile,1,nbb)
       if(ifail.ne.0) go to 11
       infile=afile
!       call casetrans(infile,'hi')
       inunit=nextunit()
       open(unit=inunit,file=infile,status='old',iostat=ierr)
       if(ierr.ne.0) then
         call addquote(infile,astring)
         write(amessage,20) trim(astring)
20       format(' Cannot open file ',a,'  - try again.')
         call write_message(increment=1)
         go to 6
       end if
       imessage=0

100    call open_output_file(ifail,   &
       ' Enter name for TSPROC run record file: ',recfile,recunit)
       if(ifail.ne.0) go to 9900
       if(escset.ne.0)then
         escset=0
         close(unit=inunit)
         write(*,*)
         go to 4
       end if

! -- More variables are initialised.

       imessage=0
       NumProcBlock=0
       ILine=0
       IProcSetting=0
       Context=' '
       tempseries%nterm=0
       call addquote(infile,astring)
       write(*,110) trim(astring)
       write(recunit,110) trim(astring)
110    format(/,' Processing information contained in TSPROC input file ',a,'....')

! -- The TSPROC input file is now read, looking for Blocks.

120    continue

       call GetNextBlock(ifail,iblock)
       if(ifail.ne.0) go to 9900

       if(iblock.eq.0) then              ! settings
         call process_settings(ifail)
       else if(iblock.eq.101)then        ! get series from WDM file
         call get_wdm_series(ifail)
       else if(iblock.eq.102)then        ! get series from site sample file
         call get_ssf_series(ifail)
       else if(iblock.eq.103)then        ! get series from PLOTGEN file
         call get_plt_series(ifail)
       else if(iblock.eq.104)then        ! get series from TETRAD output file
         call get_mul_series_tetrad(ifail)
       else if(iblock.eq.105)then        ! get multiple series from site sample file
         call get_mul_series_ssf(ifail)
       else if(iblock.eq.106)then        ! get series from UFORE-HYDRO file
         call get_ufore_series(ifail)
       else if(iblock.eq.107)then        ! get multiple series from a GSFLOW gage file
         call get_mul_series_gsflow_gage(ifail)
       else if(iblock.eq.108)then        ! get multiple series from a MMS/GSFLOW STATVAR file
         call get_mul_series_statvar(ifail)
       else if(iblock.eq.120)then        ! get series from SWR1 binary output
         call get_swr_series(ifail)
       else if (iblock.eq.121)then       ! get a list of constants from an external file
         call get_constants(ifail)
       else if (iblock.eq.122)then       ! get multiple series(reachgroups) from SWR1 binary file
         call get_mul_swr_series(ifail)                
       else if(iblock.eq.201)then        ! write list output file
         call write_list_output(ifail)
       else if(iblock.eq.301)then        ! erase entity from memory
         call erase_entity(ifail)
       else if(iblock.eq.302)then        ! reduce time_span of series
         call reduce_span(ifail)
       else if(iblock.eq.303)then        ! calculate series statistics
         call statistics(ifail)
       else if(iblock.eq.304)then        ! series comparison statistics
         call compare_series(ifail)
       else if(iblock.eq.305)then        ! change time_base
         call time_base(ifail)
       else if(iblock.eq.306)then        ! volume calculation
         call volume(ifail)
       else if(iblock.eq.308)then        ! exceedence time
         call time_duration(ifail)
       else if(iblock.eq.310)then        ! series equation
         call equation(ifail)
       else if(iblock.eq.311)then        ! series displace
         call displace(ifail)
       else if(iblock.eq.312)then        ! series clean
         call series_clean(ifail)
       else if(iblock.eq.313)then        ! digital filter
         call bfilter(ifail)
       else if(iblock.eq.314)then        ! series base level
         call series_base_level(ifail)
       else if(iblock.eq.315)then        ! volume to series
         call vol_to_series(ifail)
       else if(iblock.eq.316)then        ! moving minimum
         call moving_window(ifail)
       else if(iblock.eq.317)then        ! new uniform series
         call new_series_uniform(ifail)
       else if(iblock.eq.318)then        ! series difference
         call series_difference(ifail)
       else if(iblock.eq.319)then        ! series block drawdown
         call series_block_drawdown(ifail)         
       else if(iblock.eq.320)then        ! series time average
         call series_time_average(ifail)
       else if(iblock.eq.321)then
         call displace_constant(ifail)  
       else if(iblock.eq.401)then        ! write pest files
         call pest_files(ifail,lastblock)
       end if
       if(ifail.ne.0) go to 9900
       lastblock=iblock
       go to 120

9890   call write_message(leadspace='yes')
9900   call close_files
       do i=1,MAXSERIES
         if(series(i)%active)then
           deallocate(series(i)%days,series(i)%secs,series(i)%val,stat=ierr)
           if(associated(series(i)%days)) nullify(series(i)%days)
           if(associated(series(i)%secs)) nullify(series(i)%secs)
           if(associated(series(i)%val))  nullify(series(i)%val)
         end if
       end do
       if(tempseries%active)then
         deallocate(tempseries%days,tempseries%secs,tempseries%val,stat=ierr)
         if(associated(tempseries%days)) nullify(tempseries%days)
         if(associated(tempseries%secs)) nullify(tempseries%secs)
         if(associated(tempseries%val)) nullify(tempseries%val)
       end if
       do i=1,MAXVTABLE
         if(vtable(i)%active)then
           deallocate(vtable(i)%days1,vtable(i)%days2,vtable(i)%secs1,  &
           vtable(i)%secs2,vtable(i)%vol,stat=ierr)
           if(associated(vtable(i)%days1)) nullify(vtable(i)%days1)
           if(associated(vtable(i)%days2)) nullify(vtable(i)%days2)
           if(associated(vtable(i)%secs1)) nullify(vtable(i)%secs1)
           if(associated(vtable(i)%secs2)) nullify(vtable(i)%secs2)
           if(associated(vtable(i)%vol)) nullify(vtable(i)%vol)
         end if
       end do
       do i=1,MAXDTABLE
         if(dtable(i)%active)then
           deallocate(dtable(i)%time,dtable(i)%flow,  &
                      dtable(i)%tdelay,stat=ierr)
           if(associated(dtable(i)%time))   nullify(dtable(i)%time)
           if(associated(dtable(i)%flow))   nullify(dtable(i)%flow)
           if(associated(dtable(i)%tdelay)) nullify(dtable(i)%tdelay)
         end if
       end do
       deallocate(tempdtable%time,tempdtable%flow,tempdtable%tdelay,stat=ierr)
       nullify (tempdtable%time,tempdtable%flow,tempdtable%tdelay)


end program tsproc


subroutine GetNextBlock(ifail,iblock)

! -- Subroutine GetNextBlock obtains the header to the next section of
!    the TSPROC input file.

       use tspvar
       use defn
       use inter
       implicit none

       integer, intent(out) :: ifail,iblock

       integer ierr
       character*15 aline
       character*30 ablock

       ifail=0
       call addquote(infile,astring)
       do
         iline=iline+1
         read(inunit,'(a)',err=9000,end=500) cline
         if(cline.eq.' ') cycle
         if(cline(1:1).eq.'#')cycle
         cline=adjustl(cline)
         call linesplit(ierr,2)
         if(ierr.ne.0)then
           call num2char(iline,aline)
           write(amessage,5) trim(aline),trim(astring)
5          format('two entries expected on line ',a,' of file ',a)
           go to 9800
         end if
         ablock=cline(left_word(1):right_word(1))
         call casetrans(ablock,'hi')
         if(ablock.ne.'START')then
           call num2char(iline,aline)
           write(amessage,7) trim(aline),trim(astring)
7          format('first item on line ',a,' of file ',a,' expected to be START.')
           go to 9800
         end if
         ablock=cline(left_word(2):right_word(2))
         call casetrans(ablock,'hi')
         if(ablock.eq.'SETTINGS')then
           iBlock=0
         else if(ablock.eq.'GET_SERIES_WDM')then
           iBlock=101
         else if(ablock.eq.'GET_SERIES_SSF')then
           iBlock=102
         else if(ablock.eq.'GET_SERIES_PLOTGEN')then
           iBlock=103
         else if(ablock.eq.'GET_SERIES_TETRAD')then
           iBlock=104
         else if(ablock.eq.'GET_MUL_SERIES_SSF')then
           iBlock=105
         else if(ablock.eq.'GET_SERIES_UFORE_HYDRO')then
           iBlock=106
         else if(ablock.eq.'GET_MUL_SERIES_GSFLOW_GAGE')then
           iBlock=107
         else if(ablock.eq.'GET_MUL_SERIES_STATVAR')then
           iBlock=108
         else if(ablock.eq.'GET_SERIES_SWR')then
           iBlock=120
         else if(ablock.eq.'GET_MUL_SERIES_SWR')then
           iBlock=122  
         else if (ablock.eq.'GET_CONSTANTS')then
           iBlock=121  
         else if(ablock.eq.'LIST_OUTPUT')then
           iBlock=201
         else if(ablock.eq.'ERASE_ENTITY')then
           iblock=301
         else if(ablock.eq.'REDUCE_TIME_SPAN')then
           iblock=302
         else if(ablock.eq.'SERIES_STATISTICS')then
           iblock=303
         else if(ablock.eq.'SERIES_COMPARE')then
           iblock=304           
         else if(ablock.eq.'NEW_TIME_BASE')then
           iblock=305
         else if(ablock.eq.'VOLUME_CALCULATION')then
           iblock=306
         else if(ablock.eq.'EXCEEDENCE_TIME')then
           iblock=308
         else if(ablock.eq.'SERIES_EQUATION')then
           iblock=310
         else if(ablock.eq.'SERIES_DISPLACE')then
           iblock=311
         else if(ablock.eq.'SERIES_CLEAN')then
           iblock=312
         else if(ablock.eq.'DIGITAL_FILTER')then
           iblock=313
         else if(ablock.eq.'SERIES_BASE_LEVEL')then
           iblock=314
         else if(ablock.eq.'V_TABLE_TO_SERIES')then
           iblock=315
         else if(ablock.eq.'MOVING_MINIMUM')then
           iblock=316
         else if(ablock.eq.'NEW_SERIES_UNIFORM')then
           iblock=317
         else if(ablock.eq.'SERIES_DIFFERENCE')then
           iblock=318
         else if(ablock.eq.'SERIES_BLOCK_DRAWDOWN')then
           iblock=319
         else if(ablock.eq.'SERIES_TIME_AVERAGE')then
           iblock=320
         else if(ablock.eq.'SERIES_DISPLACE_CONSTANT')then
           iblock=321  
         else if(ablock.eq.'WRITE_PEST_FILES')then
           iblock=401
         else
           call num2char(iline,aline)
           write(amessage,10) trim(ablock),trim(aline),trim(astring)
10         format(' Unrecognised block title "',a,'" at line ',a, &
           ' of TSPROC input file ',a)
           call write_message(leadspace='yes')
           call write_message(iunit=recunit,leadspace='yes')
           ifail=1
           return
         end if
         go to 400
       end do

400    continue
       numprocBlock=numprocBlock+1
       if(iBlock.eq.0)then
         if(IProcSetting.ne.0)then
           write(amessage,525) trim(astring)
525        format('file ',a,' contains two SETTINGS blocks.')
           go to 9800
         else if(numprocBlock.ne.1)then
           write(amessage,520)
520        format('SETTINGS block must be the first block in a TSPROC input file.')
           go to 9800
         end if
       else
         if(iprocsetting.ne.1)then
           write(amessage,530) trim(astring)
530        format('a SETTINGS block must lead all other blocks in TSPROC ', &
           'input file ',a)
           go to 9800
         end if
       end if

       return

500    continue
       if(numprocblock.eq.0)then
         write(amessage,550) trim(astring)
550      format(' No blocks found in TSPROC input file ',a)
       else
         write(amessage,540) trim(astring)
540      format(' End of TSPROC input file ',a,' - no more blocks to process.')
       end if
       call write_message(leadspace='yes')
       call write_message(iunit=recunit,leadspace='yes')
       ifail=-1
       return

9000   call num2char(iline,aline)
       write(amessage,9010) trim(aline),trim(astring)
9010   format('unable to read line ',a,' of file ',a)
       go to 9800

9800   call write_message(leadspace='yes',error='yes')
       call write_message(iunit=recunit,leadspace='yes')
       ifail=1

       return
end subroutine GetNextBlock



subroutine Process_Settings(ifail)

! -- Subroutine ProcessSettings reads a SETTINGS segment from a TSPROC input file.

       use tspvar
       use defn
       use inter
       implicit none

       integer, intent(out) :: ifail

       integer ierr
       character*15 aline
       character*25 aoption,datestr

       ifail=0

       write(*,10)
       write(recunit,10)
10     format(/' Processing SETTINGS block....')

       datestr=' '
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
         if(aoption.eq.'CONTEXT')then
           if(context.ne.' ')then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,12) trim(aline), trim(astring)
12           format('only one CONTEXT keyword is allowed in a SETTINGS block. ', &
             'The second at line ',a,' of file ',a,' is illegal.')
             go to 9800
           end if
           call getfile(ierr,cline,context,left_word(2),right_word(2))
           if(ierr.ne.0)then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,23) trim(aline),trim(astring)
23           format('cannot read CONTEXT from line ',a,' of file ',a)
             go to 9800
           end if
           if(isspace(context))then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,21) trim(context),trim(aline),trim(astring)
21           format('space character in CONTEXT name "',a,'" at line ',a,' of file ',a)
             go to 9800
           end if
           call casetrans(context,'lo')
           write(*,25) trim(context)
           write(recunit,25) trim(context)
25         format(t5,'CONTEXT ',a)
         else if(aoption.eq.'DATE_FORMAT')then
           call getfile(ierr,cline,datestr,left_word(2),right_word(2))
           if(ierr.ne.0)then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,140) trim(aline),trim(astring)
140          format('cannot read date format string from line ',a,' of file ',a)
             go to 9800
           end if
           call casetrans(datestr,'lo')
           if((datestr(1:2).eq.'dd').and.(datestr(4:5).eq.'mm'))then
             datespec=1
           else if((datestr(1:2).eq.'mm').and.(datestr(4:5).eq.'dd'))then
             datespec=2
           else
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,140) trim(aline),trim(astring)
             go to 9800
           end if
           if(datespec.eq.1)then
             write(*,141)
             write(recunit,141)
141          format(t5,'DATE_FORMAT dd/mm/yyyy')
           else
             write(*,142)
             write(recunit,142)
142          format(t5,'DATE_FORMAT mm/dd/yyyy')
           end if
         else if(aoption.eq.'END')then
           go to 100
         else
           call num2char(iline,aline)
           call addquote(infile,astring)
           write(amessage,30) trim(aoption),trim(aline),trim(astring)
30         format('unexpected keyword - "',a,'" in SETTINGS block at line ',a, &
           ' of file ',a)
           go to 9800
         end if
       end do

100    continue

       if(context.eq.' ')then
         call addquote(infile,astring)
         write(amessage,19) trim(astring)
19       format('the SETTINGS block in file ',a,' does not contain ', &
         'a CONTEXT keyword.')
         go to 9800
       end if
       if(datestr.eq.' ')then
         call addquote(infile,astring)
         write(amessage,18) trim(astring)
18       format('the SETTINGS block in file ',a,' does not contain a ', &
         'DATE_FORMAT keyword.')
         go to 9800
       end if
       IProcSetting=1
       write(*,120)
120    format(t5,'Processing of SETTINGS block complete.')
       write(recunit,120)
       return


9000   continue
       call num2char(iline,aline)
       call addquote(infile,astring)
       write(amessage,9010) trim(aline),trim(astring)
9010   format('cannot read line ',a,' of TSPROC input file ',a)
       go to 9800
9100   continue
       call addquote(infile,astring)
       write(amessage,9110) trim(astring)
9110   format('unexpected end encountered to TSPROC input file ',a, &
       ' while reading SETTINGS block.')
       go to 9800

9800   call write_message(leadspace='yes',error='yes')
       call write_message(iunit=recunit,leadspace='yes')
       ifail=1
       return

end subroutine process_settings



subroutine get_ssf_series(ifail)

! -- Subroutine get_ssf_series reads a time series from a site sample file.

       use tspvar
       use defn
       use inter
       implicit none

       integer, intent(out)   :: ifail

       integer dd1,mm1,yy1,hh1,nn1,ss1,dd2,mm2,yy2,hh2,nn2,ss2,ierr,k,ixcon, &
       icontext,nn,ss,i,iunit,begdays,begsecs,enddays,endsecs,iterm,jline,j
       double precision dvalue
       character*10 asite,aname,bsite
       character*15 aline
       character*20 atemp
       character*25 aoption
       character*120 afile
       character*25 acontext(MAXCONTEXT)

       ifail=0
       currentblock='GET_SERIES_SSF'

       write(*,10) trim(currentblock)
       write(recunit,10) trim(currentblock)
10     format(/,' Processing ',a,' block....')

       afile=' '
       asite=' '
       acontext(1)=' '
       aname=' '
       icontext=0
       yy1=-9999
       hh1=-9999
       yy2=-9999
       hh2=-9999
       ixcon=0
       iunit=0

! -- The GET_SERIES_SSF block is first parsed.

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
         else if(aoption.eq.'SITE')then
           if(asite.ne.' ')then
             write(amessage,44)
44           format('only one site name can be provided in a ',  &
             'GET_SERIES_SSF block; use a GET_MUL_SERIES_SSF block ', &
             'to read multiple series using one block.')
             go to 9800
           end if
           call getfile(ierr,cline,atemp,left_word(2),right_word(2))
           if(ierr.ne.0)then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,45) trim(aline),trim(astring)
45           format('cannot read SITE name from line ',a,' of file ',a)
             go to 9800
           end if
           nn=len_trim(atemp)
           if(nn.gt.10)then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,50) trim(aline),trim(astring)
50           format('site identifier must be 10 characters or less at line ', &
             a,' of file ',a)
             go to 9800
           end if
           asite=atemp(1:10)
           if(isspace(asite))then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,51) trim(asite),trim(aline),trim(astring)
51           format('space character in SITE name "',a,'" at line ',a,' of file ',a)
             go to 9800
           end if
           call casetrans(asite,'lo')
           write(*,55) trim(asite)
           write(recunit,55) trim(asite)
55         format(t5,'SITE ',a)
         else if(aoption.eq.'DATE_1')then
           call read_date(ierr,dd1,mm1,yy1,'DATE_1')
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'DATE_2')then
           call read_date(ierr,dd2,mm2,yy2,'DATE_2')
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'TIME_1')then
           call read_time(ierr,hh1,nn1,ss1,'TIME_1')
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'TIME_2')then
           call read_time(ierr,hh2,nn2,ss2,'TIME_2')
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'NEW_SERIES_NAME')then
           call read_new_series_name(ierr,aname)
           if(ierr.ne.0) go to 9800
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

! -- If there are any absences in the GETSERIES block, this is now reported.

100    continue
       if(afile.eq.' ')then
         call addquote(infile,astring)
         write(amessage,110) trim(currentblock),trim(astring)
110      format('no FILE keyword provided in ',a,' block in file ',a)
         go to 9800
       end if
       if(asite.eq.' ')then
         call addquote(infile,astring)
         write(amessage,120) trim(currentblock),trim(astring)
120      format('no SITE keyword provided in ',a,' block in file ',a)
         go to 9800
       end if
       if(icontext.eq.0)then
         call addquote(infile,astring)
         write(amessage,122) trim(currentblock),trim(astring)
122      format('no CONTEXT keyword provided in ',a,' block in file ',a)
         go to 9800
       end if
       if(aname.eq.' ')then
         call addquote(infile,astring)
         write(amessage,125) trim(currentblock),trim(astring)
125      format('no NEW_SERIES_NAME keyword provided in ',a,' block in file ',a)
         go to 9800
       end if
       call date_check(ierr,yy1,mm1,dd1,hh1,nn1,ss1,yy2,mm2,dd2,hh2,nn2,ss2,  &
       begdays,begsecs,enddays,endsecs)
       if(ierr.ne.0) go to 9800

! -- There appear to be no errors in the block, so now it is processed.

       call addquote(afile,astring)
       write(*,179) trim(astring)
       write(recunit,179) trim(astring)
179    format(t5,'Reading site sample file ',a,'....')
       iunit=nextunit()
       open(unit=iunit,file=afile,status='old',iostat=ierr)
       if(ierr.ne.0)then
         write(amessage,180) trim(astring),trim(currentblock)
180      format('cannot open site sample file ',a,' cited in ',a,' block.')
         go to 9800
       end if

! -- The file is perused a first time to find out the storage requirements of the
!    time series (actually, the approximate storage requirements, because we don't
!    want to waste too much time processing this file on the first pass through it).

       iterm=0
       jline=0
       do
         jline=jline+1
         read(iunit,'(a)',err=9200,end=300) cline
         call linesplit(ierr,1)
         if(ierr.lt.0) cycle
         bsite=cline(left_word(1):right_word(1))
         call casetrans(bsite,'lo')
         if(bsite.eq.asite)then
           iterm=iterm+1
         else
           if(iterm.gt.0) go to 300
         end if
       end do

300    continue
       if(iterm.eq.0)then
         write(amessage,310) trim(asite),trim(astring)
310      format('site "',a,'" not found in site sample file ',a)
         go to 9800
       end if

! -- Samples pertaining to the site are now read into the temporary time series
!    structure. If the structure is not big enough, it is re-dimensioned appropriately.

       call alloc_tempseries(ierr,iterm)
       if(ierr.ne.0) go to 9800

! -- The site sample file is now re-read and only the necessary data read in.

       rewind(unit=iunit,iostat=ierr)
       if(ierr.ne.0)then
         write(amessage,370) trim(astring)
370      format('cannot re-wind site sample file ',a)
         go to 9800
       end if
       iterm=0
       jline=0
       do
         jline=jline+1
         read(iunit,'(a)',err=9200,end=500)cline
         call linesplit(ierr,4)
         if(ierr.lt.0) then
           cycle
         else if(ierr.gt.0)then
           call num2char(jline,aline)
           write(amessage,375) trim(aline),trim(astring)
375        format('four entries expected on line ',a,' of site sample file ',a)
           go to 9800
         end if
         bsite=cline(left_word(1):right_word(1))
         call casetrans(bsite,'lo')
         if(bsite.ne.asite)cycle
         if(cline(right_word(4):).ne.' ')then
           do k=right_word(4)+1,len_trim(cline)
             if(cline(k:k).ne.' ')then
               if(cline(k:k).eq.'x') go to 379
               go to 376
             end if
           end do
         end if
376      continue
         call read_rest_of_sample_line(ierr,4,nn,ss,dvalue,jline,afile)
         if(ierr.ne.0)then
           call write_message(iunit=recunit,leadspace='yes',error='yes')
           ifail=1
           return
         end if
         if(iterm.eq.0)then
           if((nn.lt.begdays).or.((nn.eq.begdays).and.(ss.lt.begsecs))) &
           cycle
         end if
         if((nn.gt.enddays).or.((nn.eq.enddays).and.(ss.gt.endsecs))) &
         go to 500
         iterm=iterm+1
         tempseries%days(iterm)=nn
         tempseries%secs(iterm)=ss
         tempseries%val(iterm)=dvalue
379      continue
       end do

500    continue
       if(iterm.eq.0)then
         write(amessage,505)
505      format('no terms of the series can be imported. Check the date settings.')
         go to 9800
       end if

! -- The time series is now copied to a real time series.

       do i=1,MAXSERIES
         if(.not.series(i)%active) go to 515
       end do
       write(amessage,510)
510    format('no more time series available for data storage - increase MAXSERIES and ', &
       'recompile program.')
       go to 9800

515    allocate(series(i)%days(iterm),series(i)%secs(iterm),  &
       series(i)%val(iterm),stat=ierr)
       if(ierr.ne.0)then
         write(amessage,550)
550      format('cannot allocate memory for another time series.')
         go to 9800
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
       go to 9900


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

9900   if(iunit.ne.0)close(unit=iunit,iostat=ierr)
       return

end subroutine get_ssf_series




subroutine write_list_output(ifail)

! -- Subroutine Write_List_Output writes TSPROC entities to an ASCII output file.

       use tspvar
       use defn
       use inter
       implicit none

       integer, intent(out) :: ifail

       integer icontext,ierr,i,dd,mm,yy,ss,hhh,mmm,sss,nn,iterm,j, &
       nnn,dds1,mms1,yys1,dds2,mms2,yys2,hhs1,nns1,sss1,ixcon, &
       hhs2,nns2,sss2,jstable,jvtable,jdtable,iseries,idtable,istable,ivtable, &
       ictable,jctable,iconst
       real totim
       character*3 aaa
       character*10 aname,sformat,atemp
       character*15 aline
       character*25 aoption
       character*25 acontext(MAXCONTEXT)

       ifail=0
       currentblock='LIST_OUTPUT'

       write(*,10)
       write(recunit,10)
10     format(/,' Processing LIST_OUTPUT block....')

       ixcon=0
       icontext=0
       outseries=0          !outseries is an array
       iseries=0
       istable=0
       ictable=0
       ivtable=0
       idtable=0
       iconst=0
       outfile=' '
       sformat=' '

! -- Options for the LIST_OUTPUT block are first read.

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
           call read_file_name(ierr,outfile)
           if(ierr.ne.0) go to 9800
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
         else if(aoption.eq.'SERIES_NAME')then
           iseries=iseries+1
           if(iseries.gt.MAXSERIES)then
             call num2char(MAXSERIES,aline)
             write(amessage,100) trim(aline)
100          format('a maximum of ',a,' series can be cited in a LIST_OUTPUT block.')
             go to 9800
           end if
           call read_series_name(ierr,outseries(iseries),'SERIES_NAME')
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'S_TABLE_NAME')then
           istable=istable+1
           if(istable.gt.MAXSTABLE)then
             call num2char(MAXSTABLE,aline)
             write(amessage,102) trim(aline)
102          format('a maximum of ',a,' s_tables can be cited in a LIST_OUTPUT block.')
             go to 9800
           end if
           call read_table_name(ierr,outstable(istable),1)
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'C_TABLE_NAME')then
           ictable=ictable+1
           if(ictable.gt.MAXCTABLE)then
             call num2char(MAXCTABLE,aline)
             write(amessage,109) trim(aline)
109          format('a maximum of ',a,' c_tables can be cited in a LIST_OUTPUT block.')
             go to 9800
           end if
           call read_table_name(ierr,outctable(ictable),4)
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'V_TABLE_NAME')then
           ivtable=ivtable+1
           if(ivtable.gt.MAXVTABLE)then
             call num2char(MAXVTABLE,aline)
             write(amessage,103) trim(aline)
103          format('a maximum of ',a,' v_tables can be cited in a LIST_OUTPUT block.')
             go to 9800
           end if
           call read_table_name(ierr,outvtable(ivtable),2)
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'E_TABLE_NAME')then
           idtable=idtable+1
           if(idtable.gt.MAXDTABLE)then
             call num2char(MAXDTABLE,aline)
             write(amessage,104) trim(aline)
104          format('a maximum of ',a,' E_TABLES can be cited in a LIST_OUTPUT block.')
             go to 9800
           end if
           call read_table_name(ierr,outdtable(idtable),3)
           if(ierr.ne.0) go to 9800
         
           
         else if(aoption.eq.'END')then
           go to 200
         else if(aoption.eq.'SERIES_FORMAT')then
           call getfile(ierr,cline,sformat,left_word(2),right_word(2))
           if(ierr.ne.0)then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,152) trim(aline),trim(astring)
152          format('cannot read SERIES_FORMAT from line ',a,' of file ',a)
             go to 9800
           end if
           call casetrans(sformat,'lo')
           if((sformat.ne.'short').and.(sformat.ne.'long'))then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,155) trim(aline),trim(astring)
155          format('series_format must be "long" or "short" at line ',a, &
             ' of TSPROC input file ',a)
             go to 9800
           end if
           write(*,157) trim(sformat)
           write(recunit,157) trim(sformat)
157        format(t5,'SERIES_FORMAT ',a)
         else
           call num2char(iline,aline)
           call addquote(infile,astring)
           write(amessage,180) trim(aoption),trim(aline),trim(astring)
180        format('unexpected keyword - "',a,'" in LIST_OUTPUT block at line ',a, &
           ' of file ',a)
           go to 9800
         end if
       end do

! -- The block has been read; now it is checked for correctness.

200    continue
       if((iseries.eq.0).and.(istable.eq.0).and.(ivtable.eq.0).and.   &
          (idtable.eq.0).and.(ictable.eq.0))then
         write(amessage,210)
210      format('no series or tables have been named for output in LIST_OUTPUT block.')
         go to 9800
       end if
       if((iseries.ne.0).and.(sformat.eq.' '))then
         write(amessage,215)
215      format('if a time series is specified for output then the SERIES_FORMAT ', &
         'specifier must also be set in a LIST_OUTPUT block.')
         go to 9800
       end if
       if(outfile.eq.' ')then
         write(amessage,230)
230      format('no FILE name provided in LIST_OUTPUT block.')
         go to 9800
       end if
       if(icontext.eq.0)then
         write(amessage,220)
220      format('no CONTEXT keyword(s) provided in LIST_OUTPUT block.')
         go to 9800
       end if

! -- All is well with the LIST_OUTPUT block so the output file is written.

       series_format=sformat
       list_output_file=outfile
       call addquote(outfile,astring)
       write(*,260) trim(astring)
       write(recunit,260) trim(astring)
260    format(t5,'Writing output file ',a,'....')
       outunit=nextunit()
       open(unit=outunit,file=outfile,iostat=ierr)
       if(ierr.ne.0)then
         write(amessage,270) trim(astring)
270      format('cannot open file ',a,' for output.')
         go to 9800
       end if

! -- All of the requested time series are first written.

       imseries=iseries
       imdtable=idtable
       imvtable=ivtable
       imstable=istable
       imctable=ictable

       if(iseries.eq.0) go to 500
       do i=1,iseries
         j=outseries(i)
         aname=series(j)%name
         write(outunit,271) trim(series(j)%name)
271      format(/,' TIME_SERIES "',a,'" ---->')
         if(series(j)%type.eq.'ts')then
           do iterm=1,series(j)%nterm
             if(sformat.eq.'long')then
               nn=series(j)%days(iterm)
               ss=series(j)%secs(iterm)
               call newdate(nn,1,1,1970,dd,mm,yy)
               hhh=ss/3600
               mmm=(ss-hhh*3600)/60
               sss=ss-hhh*3600-mmm*60
               if(datespec.eq.1) then
                 write(outunit,300) trim(aname),dd,mm,yy,hhh,mmm,sss,series(j)%val(iterm)
300              format(1x,a,t15,i2.2,'/',i2.2,'/',i4.4,3x,i2.2,':',i2.2,':',   &
                 i2.2,3x,1pg14.7)
               else
                 write(outunit,300) trim(aname),mm,dd,yy,hhh,mmm,sss,series(j)%val(iterm)
               endif
305            continue
             else
               write(outunit,301) series(j)%val(iterm)
301            format(4x,1pg14.7)
             end if
           end do
         end if
505      continue
       end do

! -- If any S_TABLEs were requested, they are now written.

500    if(istable.eq.0) go to 1200
       do i=1,istable
          jstable=outstable(i)
          write(outunit,510) trim(stable(jstable)%name)
510       format(/,' S_TABLE "',a,'" ---->')
          write(outunit,515) trim(stable(jstable)%series_name)
515       format(t5,'Series for which data calculated:',t55,'"',a,'"')
          nnn=stable(jstable)%rec_begdays
          sss=stable(jstable)%rec_begsecs
          call newdate(nnn,1,1,1970,dds1,mms1,yys1)
          hhs1=sss/3600
          nns1=(sss-hhs1*3600)/60
          sss1=sss-hhs1*3600-nns1*60
          nnn=stable(jstable)%rec_enddays
          sss=stable(jstable)%rec_endsecs
          call newdate(nnn,1,1,1970,dds2,mms2,yys2)
          hhs2=sss/3600
          nns2=(sss-hhs2*3600)/60
          sss2=sss-hhs2*3600-nns2*60
          if(datespec.eq.1)then
            write(outunit,520) dds1,mms1,yys1
          else
            write(outunit,520) mms1,dds1,yys1
          end if
520       format(t5,'Beginning date of data accumulation:',t55,i2.2,'/',i2.2,'/',i4)
          write(outunit,530) hhs1,nns1,sss1
530       format(t5,'Beginning time of data accumulation:',t55,i2.2,':',i2.2,':',i2.2)
          if(datespec.eq.1)then
            write(outunit,540) dds2,mms2,yys2
          else
            write(outunit,540) mms2,dds2,yys2
          end if
540       format(t5,'Finishing date of data accumulation:',t55,i2.2,'/',i2.2,'/',i4)
          write(outunit,550) hhs2,nns2,sss2
550       format(t5,'Finishing time of data accumulation:',t55,i2.2,':',i2.2,':',i2.2)
          call num2char(stable(jstable)%rec_icount,aline)
          write(outunit,555) trim(aline)
555       format(t5,'Number of series terms in this interval:',t55,a)
          if(stable(jstable)%rec_itrans.eq.0)then
            aaa='no'
          else
            aaa='yes'
          end if
          write(outunit,560) trim(aaa)
560       format(t5,'Logarithmic transformation of series?',t55,a)
!          if(stable(jstable)%rec_power.eq.0.0)then
!            aaa='no'
!          else
!            aaa='yes'
!          end if
!          write(outunit,570) trim(aaa)
!570       format(t5,'Power transformation of series?',t55,a)
          if(stable(jstable)%rec_power.eq.0.0)then
            aline='na'
          else
            call num2char(stable(jstable)%rec_power,aline)
          end if
          write(outunit,580) trim(aline)
580       format(t5,'Exponent in power transformation:',t55,a)
          if(stable(jstable)%maximum.gt.-1.0e35)then
            write(outunit,590) stable(jstable)%maximum
590         format(t5,'Maximum value:',t55,1pg14.7)
          end if
          if(stable(jstable)%minimum.gt.-1.0e35)then
            write(outunit,600) stable(jstable)%minimum
600         format(t5,'Minimum value:',t55,1pg14.7)
          end if
          if(stable(jstable)%range.gt.-1.0e35)then
            write(outunit,601) stable(jstable)%range
601         format(t5,'Range:',t55,1pg14.7)
          end if
          if(stable(jstable)%total.gt.-1.0e35)then
            write(outunit,605) stable(jstable)%total
605         format(t5,'Sum of values:',t55,1pg14.7)
          end if
          if(stable(jstable)%mean.gt.-1.0e35)then
            write(outunit,610) stable(jstable)%mean
610         format(t5,'Mean value:',t55,1pg14.7)
          end if
          if(stable(jstable)%stddev.gt.-1.0e35)then
            write(outunit,620) stable(jstable)%stddev
620         format(t5,'Standard deviation:',t55,1pg14.7)
          end if
          if(stable(jstable)%minmean.gt.-1.0e35)then
            call num2char(stable(jstable)%avetime,atemp)
            write(outunit,630) trim(atemp),stable(jstable)%minmean
630         format(t5,'Minimum ',a,'-sample mean',t55,1pg14.7)
          end if
          if(stable(jstable)%maxmean.gt.-1.0e35)then
            call num2char(stable(jstable)%avetime,atemp)
            write(outunit,640) trim(atemp),stable(jstable)%maxmean
640         format(t5,'Maximum ',a,'-sample mean',t55,1pg14.7)
          end if
       end do

! -- If any C_TABLEs were requested, they are now written.
       
1200   if(ictable.eq.0) go to 700
       do i=1,ictable
          jctable=outctable(i)
          write(outunit,1210) trim(ctable(jctable)%name)
1210      format(/,' C_TABLE "',a,'" ---->')
          write(outunit,1215) trim(ctable(jctable)%series_name_obs)
1215      format(t5,'Observation time series name:',t55,'"',a,'"')
          write(outunit,1216) trim(ctable(jctable)%series_name_sim)
1216      format(t5,'Simulation time series name:',t55,'"',a,'"')
          nnn=ctable(jctable)%rec_begdays
          sss=ctable(jctable)%rec_begsecs
          call newdate(nnn,1,1,1970,dds1,mms1,yys1)
          hhs1=sss/3600
          nns1=(sss-hhs1*3600)/60
          sss1=sss-hhs1*3600-nns1*60
          nnn=ctable(jctable)%rec_enddays
          sss=ctable(jctable)%rec_endsecs
          call newdate(nnn,1,1,1970,dds2,mms2,yys2)
          hhs2=sss/3600
          nns2=(sss-hhs2*3600)/60
          sss2=sss-hhs2*3600-nns2*60
          if(datespec.eq.1)then
            write(outunit,521) dds1,mms1,yys1
521         format(t5,'Beginning date of series comparison:',   &
            t55,i2.2,'/',i2.2,'/',i4)            
          else
            write(outunit,521) mms1,dds1,yys1
          end if
          write(outunit,531) hhs1,nns1,sss1
531       format(t5,'Beginning time of series comparison:',   &
          t55,i2.2,':',i2.2,':',i2.2)          
          if(datespec.eq.1)then
            write(outunit,541) dds2,mms2,yys2            
541         format(t5,'Finishing date of series comparison:',  &
            t55,i2.2,'/',i2.2,'/',i4)
          else
            write(outunit,541) mms2,dds2,yys2
          end if
          write(outunit,551) hhs2,nns2,sss2
551       format(t5,'Finishing time of series comparison:',  &
          t55,i2.2,':',i2.2,':',i2.2)          
          call num2char(ctable(jctable)%rec_icount,aline)
          write(outunit,555) trim(aline)
          if(ctable(jctable)%bias.gt.-1.0e35)then
            write(outunit,1290) ctable(jctable)%bias
1290        format(t5,'Bias:',t55,1pg14.7)
          end if
          if(ctable(jctable)%se.gt.-1.0e35)then
            write(outunit,1300) ctable(jctable)%se
1300        format(t5,'Standard error:',t55,1pg14.7)
          end if
          if(ctable(jctable)%rbias.gt.-1.0e35)then
            write(outunit,1305) ctable(jctable)%rbias
1305        format(t5,'Relative bias:',t55,1pg14.7)
          end if
          if(ctable(jctable)%rse.gt.-1.0e35)then
            write(outunit,1310) ctable(jctable)%rse
1310         format(t5,'Relative standard error:',t55,1pg14.7)
          end if
          if(ctable(jctable)%ns.gt.-1.0e35)then
            write(outunit,1320) ctable(jctable)%ns
1320         format(t5,'Nash-Sutcliffe coefficient:',t55,1pg14.7)
          end if
          if(ctable(jctable)%ce.gt.-1.0e35)then
            write(outunit,1330) ctable(jctable)%ce
1330        format(t5,'Coefficient of efficiency:',t55,1pg14.7)
          end if
          if(ctable(jctable)%ia.gt.-1.0e35)then
            write(outunit,1340) ctable(jctable)%ia
1340        format(t5,'Index of agreement:',t55,1pg14.7)
          end if          
       end do
                            
! -- If any V_TABLES were requested, they are now written.

700    if(ivtable.eq.0) go to 900
       do i=1,ivtable
          jvtable=outvtable(i)
          write(outunit,710) trim(vtable(jvtable)%name)
710       format(/,' V_TABLE "',a,'" ---->')
          write(outunit,715) trim(vtable(jvtable)%series_name)
715       format(t5,'Volumes calculated from series "',a,'" are as follows:-')
          do j=1,vtable(jvtable)%nterm
            call newdate(vtable(jvtable)%days1(j),1,1,1970,dds1,mms1,yys1)
            sss=vtable(jvtable)%secs1(j)
            hhs1=sss/3600
            nns1=(sss-hhs1*3600)/60
            sss1=sss-hhs1*3600-nns1*60
            call newdate(vtable(jvtable)%days2(j),1,1,1970,dds2,mms2,yys2)
            sss=vtable(jvtable)%secs2(j)
            hhs2=sss/3600
            nns2=(sss-hhs2*3600)/60
            sss2=sss-hhs2*3600-nns2*60
            if(datespec.eq.1)then
              write(outunit,720) dds1,mms1,yys1,hhs1,nns1,sss1,  &
                                 dds2,mms2,yys2,hhs2,nns2,sss2,vtable(jvtable)%vol(j)
            else
              write(outunit,720) mms1,dds1,yys1,hhs1,nns1,sss1,  &
                                 mms2,dds2,yys2,hhs2,nns2,sss2,vtable(jvtable)%vol(j)
            end if
720         format(t5,'From ',i2.2,'/',i2.2,'/',i4,' ',i2.2,':',i2.2,':',i2.2,  &
                      ' to ',i2.2,'/',i2.2,'/',i4,' ',i2.2,':',i2.2,':',i2.2,  &
                      '  volume = ',1pg14.7)
          end do
       end do

! -- If any E_TABLES were requested, they are now written.

900    continue
       if(idtable.eq.0) go to 1100
       do i=1,idtable
          jdtable=outdtable(i)
          totim=dtable(jdtable)%total_time
          write(outunit,910) trim(dtable(jdtable)%name)
910       format(/,' E_TABLE "',a,'" ---->')
          if(dtable(jdtable)%under_over.eq.1)then
            write(outunit,915) trim(dtable(jdtable)%time_units), &
            trim(dtable(jdtable)%time_units)
915         format(t4,'Flow',t19,'Time delay (',a,')',t40,'Time above (',a,')',  &
            t60,'Fraction of time above threshold')
          else
            write(outunit,916) trim(dtable(jdtable)%time_units), &
            trim(dtable(jdtable)%time_units)
916         format(t4,'Flow',t19,'Time delay (',a,')',t40,'Time under (',a,')',  &
            t60,'Fraction of time below threshold')
          end if
          do j=1,dtable(jdtable)%nterm
            write(outunit,920) dtable(jdtable)%flow(j),  &
            dtable(jdtable)%tdelay(j), dtable(jdtable)%time(j), &
            dtable(jdtable)%time(j)/totim
920         format(t2,1pg14.7,t20,1pg14.7,t40,1pg14.7,t63,1pg14.7)
          end do
       end do
1100   continue

       write(*,320) trim(astring)
       write(recunit,320) trim(astring)
320    format(t5,'File ',a,' written ok.')
       close(unit=outunit)

       return

9000   call num2char(iline,aline)
       call addquote(infile,astring)
       write(amessage,9010) trim(aline),trim(astring)
9010   format('cannot read line ',a,' of TSPROC input file ',a)
       go to 9800
9100   continue
       call addquote(infile,astring)
       write(amessage,9110) trim(astring)
9110   format('unexpected end encountered to TSPROC input file ',a,  &
       ' while reading LIST_OUTPUT block.')
       go to 9800
9800   call write_message(leadspace='yes',error='yes')
       call write_message(iunit=recunit,leadspace='yes')
       ifail=1

9900   close(unit=recunit,iostat=ierr)
       return


end subroutine write_list_output





subroutine get_plt_series(ifail)

! -- Subroutine get_plt_series reads one or a number of time series from a HSPF
!    PLTGEN file.

       use tspvar
       use defn
       use inter
       implicit none

       integer, intent(out)   :: ifail

       integer dd1,mm1,yy1,hh1,nn1,ss1,dd2,mm2,yy2,hh2,nn2,ss2,ierr, &
       icontext,i,iunit,begdays,begsecs,enddays,endsecs,jline,j, &
       ilabel,iname,jseries,nseries,ii,npltseries,ipyear,ipmonth,ipday,iphour, &
       ipmin,idata,iterm,jdatstart,ndays,nsecs,ixcon
       integer icurve(MAXSERIES),lw(MAXSERIES),rw(MAXSERIES),iiterm(MAXSERIES), &
       jjseries(MAXSERIES)
       real threshold,rtemp
       character*15 aline
       character*25 aoption
       character*120 afile
       character*25 acontext(MAXCONTEXT)
       character*10 aname(MAXSERIES)
       character*20 aalabel,alabel(MAXSERIES)

       ifail=0
       currentblock='GET_SERIES_PLOTGEN'

       write(*,10) trim(currentblock)
       write(recunit,10) trim(currentblock)
10     format(/,' Processing ',a,' block....')

       afile=' '
       icontext=0
       ixcon=0
       yy1=-9999
       hh1=-9999
       yy2=-9999
       hh2=-9999
       ilabel=1
       iname=0
       jseries=0
       nseries=0
       do i=1,MAXSERIES
         if(series(i)%active) nseries=nseries+1
       end do
       icurve=0         !icurve is an array
       iunit=0

! -- The GET_SERIES_PLOTGEN block is first parsed.

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
         else if(aoption.eq.'DATE_2')then
           call read_date(ierr,dd2,mm2,yy2,'DATE_2')
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'TIME_1')then
           call read_time(ierr,hh1,nn1,ss1,'TIME_1')
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'TIME_2')then
           call read_time(ierr,hh2,nn2,ss2,'TIME_2')
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'LABEL')then
           if(ilabel.eq.0)then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,42) trim(currentblock),trim(aline),trim(astring)
42           format('LABEL keyword in wrong position in ',a,' block at line ',a, &
             ' of file ',a)
             go to 9800
           end if
           jseries=jseries+1
           if(jseries.gt.MAXSERIES)then
             call num2char(MAXSERIES,aline)
             write(amessage,44)trim(aline)
44           format('maximum of ',a,' LABELs can be cited in SET_SERIES_PLOTGEN block.')
             go to 9800
           end if
           call getfile(ierr,cline,alabel(jseries),left_word(2),right_word(2))
           if(ierr.ne.0)then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,57) trim(aline),trim(astring)
57           format('cannot read LABEL from line ',a,' of file ',a)
             go to 9800
           end if
           call casetrans(alabel(jseries),'lo')
           call addquote(alabel(jseries),astring)
           write(*,46) trim(astring)
           write(recunit,46) trim(astring)
46         format(t5,'LABEL ',a)
           ilabel=0
           iname=1
           aname(jseries)=' '
         else if(aoption.eq.'NEW_SERIES_NAME')then
           if(iname.eq.0)then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,43) trim(currentblock),trim(aline),trim(astring)
43           format('"NEW_SERIES_NAME" keyword must follow a LABEL keyword in ',a, &
             ' block at line ',a,' of file ',a)
             go to 9800
           end if
           call read_new_series_name(ierr,aname(jseries))
           if(ierr.ne.0) go to 9800
           if(jseries.gt.1)then
             do j=1,jseries-1
               if(aname(jseries).eq.aname(j))then
                 write(amessage,146) trim(aname(jseries)),trim(currentblock)
146               format('NEW_SERIES_NAME "',a,'" used more than once in ',a,' block.')
                 go to 9800
               end if
             end do
           end if
           iname=0
           ilabel=1
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
           if(iname.eq.1)then
             write(amessage,48) trim(currentblock)
48           format(a,' block END encountered before finding ', &
             'expected NEW_SERIES_NAME.')
             go to 9800
           end if
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

! -- If there are any absences in the GETSERIES block, this is now reported.

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
       if(jseries.eq.0)then
         call addquote(infile,astring)
         write(amessage,125) trim(currentblock),trim(astring)
125      format('no LABEL keyword provided in ',a,' block in file ',a)
         go to 9800
       end if
       call date_check(ierr,yy1,mm1,dd1,hh1,nn1,ss1,yy2,mm2,dd2,hh2,nn2,ss2,  &
       begdays,begsecs,enddays,endsecs)
       if(ierr.ne.0) go to 9800
       if(nseries+jseries.gt.MAXSERIES)then
         call num2char(MAXSERIES,aline)
         write(amessage,132) trim(aline)
132      format('the time-series storage capabilities of TSPROC have been exceeded. ',&
         'You must increase MAXSERIES and recompile TSPROC.')
         go to 9800
       end if


! -- There appear to be no errors in the block, so now it is processed.

       call addquote(afile,astring)
       write(*,179) trim(astring)
       write(recunit,179) trim(astring)
179    format(t5,'Reading HSPF PLOTGEN file ',a,'....')
       iunit=nextunit()
       open(unit=iunit,file=afile,status='old',iostat=ierr)
       if(ierr.ne.0)then
         write(amessage,180) trim(astring),trim(currentblock)
180      format('cannot open file ',a,' cited in ',a,' block.')
         go to 9800
       end if

! -- The file is perused a first time to find out the storage requirements of the
!    time series.

       iterm=0
       jline=0
       do i=1,2
         jline=jline+1
         read(iunit,'(a)',err=9200,end=9300) cline
       end do
       jline=jline+1
       read(iunit,'(a)',err=9200,end=9300) cline
       call casetrans(cline,'lo')
       ii=index(cline,'total')
       if(ii.eq.0)then
         call num2char(jline,aline)
         write(amessage,210) trim(aline),trim(astring)
210      format('string "total" expected on line ',a,' of file ',a)
         go to 9800
       end if
       cline=cline(ii+5:)
       call linesplit(ierr,1)
       if(ierr.ne.0)then
         call num2char(jline,aline)
         write(amessage,220) trim(aline),trim(astring)
         go to 9800
       end if
       call char2num(ierr,cline(left_word(1):right_word(1)),npltseries)
       if(ierr.ne.0)then
         call num2char(jline,aline)
         write(amessage,220) trim(aline),trim(astring)
220      format('cannot read total curves from line ',a,' of file ',a)
         go to 9800
       end if
       do
         jline=jline+1
         read(iunit,'(a)',err=9200,end=9320) cline
         ii=index(cline,'reshold:')
         if(ii.ne.0) exit
       end do
       cline=cline(ii+8:)
       call linesplit(ierr,1)
       if(ierr.ne.0)then
         call num2char(jline,aline)
         write(amessage,225) trim(aline),trim(astring)
         go to 9800
       end if
       call char2num(ierr,cline(left_word(1):right_word(1)),threshold)
       if(ierr.ne.0)then
         call num2char(jline,aline)
         write(amessage,225) trim(aline),trim(astring)
225      format('cannot read threshold value from line ',a,' of file ',a)
         go to 9800
       end if
       do
         jline=jline+1
         read(iunit,'(a)',err=9200,end=9350) cline
         ii=index(cline,'for each curve')
         if(ii.ne.0) exit
       end do
       jline=jline+1
       read(iunit,'(a)',err=9200,end=9350) cline
       call casetrans(cline,'lo')
       if(index(cline,'abel').eq.0) go to 9350
       do i=1,npltseries
         jline=jline+1
         read(iunit,'(a)',err=9200,end=9400) cline
         aalabel=cline(6:25)
         aalabel=adjustl(aalabel)
         call casetrans(aalabel,'lo')
         do j=1,jseries
           if(alabel(j).eq.aalabel)then
             icurve(j)=i
             go to 230
           end if
         end do
230      continue
       end do
       do i=1,jseries
         if(icurve(i).eq.0)then
           write(amessage,240) trim(alabel(i)),trim(currentblock)
240        format('no curve in HSPF PLOTGEN file corresponding to label "',a,  &
           '" cited in ',a,' block.')
           go to 9800
         end if
         lw(i)=23+(icurve(i)-1)*14
         rw(i)=lw(i)+13
       end do
       do
         jline=jline+1
         read(iunit,'(a)',err=9200,end=9450) cline
         ii=index(cline,'ate/time')
         if(ii.ne.0) exit
       end do
       jline=jline+1
       read(iunit,'(a)',err=9200,end=9450) cline
       idata=0
       iterm=0
       jdatstart=jline
       do
         jline=jline+1
         read(iunit,'(a)',err=9200,end=450) cline
         call char2num(ierr,cline(7:10),ipyear)
         if(ierr.ne.0) go to 9500
         call char2num(ierr,cline(12:13),ipmonth)
         if(ierr.ne.0) go to 9500
         call char2num(ierr,cline(15:16),ipday)
         if(ierr.ne.0) go to 9500
         call char2num(ierr,cline(18:19),iphour)
         if(ierr.ne.0) go to 9500
         call char2num(ierr,cline(21:22),ipmin)
         if(ierr.ne.0) go to 9500
         ndays=numdays(1,1,1970,ipday,ipmonth,ipyear)
260      if(iphour.ge.24)then
           iphour=iphour-24
           ndays=ndays+1
           go to 260
         end if
         nsecs=numsecs(0,0,0,iphour,ipmin,0)
         if(idata.eq.0)then
           if(begdays.eq.-99999999)then
             begdays=ndays
             begsecs=nsecs
           end if
           idata=1
         end if
         if((ndays.lt.begdays).or.((ndays.eq.begdays).and.(nsecs.lt.begsecs))) go to 400
         if((ndays.gt.enddays).or.((ndays.eq.enddays).and.(nsecs.gt.endsecs))) go to 450
         iterm=iterm+1
400      continue
       end do

450    continue
       if(iterm.eq.0)then
         write(amessage,460) trim(astring),trim(currentblock)
460      format('no time series data can be imported from file ',a,'. Check contents ', &
         'of file, as well as DATE_1 and DATE_2 keywords in ',a,' block.')
         go to 9800
       end if

! -- Now that data storage requirements have been ascertained, space is allocated in the
!    time series.

       do j=1,jseries
         do i=1,MAXSERIES
           if(.not.series(i)%active) go to 515
         end do
         write(amessage,510)
510      format('no more time series available for data storage - increase MAXSERIES and ', &
         'recompile program.')
         go to 9800
515      allocate(series(i)%days(iterm),series(i)%secs(iterm),  &
         series(i)%val(iterm),stat=ierr)
         if(ierr.ne.0)then
           write(amessage,550)
550        format('cannot allocate memory for another time series.')
           go to 9800
         end if
         series(i)%active=.true.
         series(i)%name=aname(j)
         series(i)%type='ts'
         jjseries(j)=i
       end do

! -- The PLOTGEN file is now re-read and the time-series are imported.

       iiterm=0           ! iiterm is an array
       rewind(unit=iunit,iostat=ierr)
       if(ierr.ne.0)then
         write(amessage,560) trim(astring)
560      format('cannot rewind file ',a,' to import time series data.')
         go to 9800
       end if
       jline=0
       do i=1,jdatstart
         jline=jline+1
         read(iunit,'(a)',err=9200,end=9300) cline
       end do
       do
         jline=jline+1
         read(iunit,'(a)',err=9200,end=650) cline
         call char2num(ierr,cline(7:10),ipyear)
         call char2num(ierr,cline(12:13),ipmonth)
         call char2num(ierr,cline(15:16),ipday)
         call char2num(ierr,cline(18:19),iphour)
         call char2num(ierr,cline(21:22),ipmin)
         ndays=numdays(1,1,1970,ipday,ipmonth,ipyear)
570      if(iphour.ge.24)then
           iphour=iphour-24
           ndays=ndays+1
           go to 570
         end if
         nsecs=numsecs(0,0,0,iphour,ipmin,0)
         if((ndays.lt.begdays).or.((ndays.eq.begdays).and.(nsecs.lt.begsecs))) go to 640
         if((ndays.gt.enddays).or.((ndays.eq.enddays).and.(nsecs.gt.endsecs))) go to 650
         do j=1,jseries
           call char2num(ierr,cline(lw(j):rw(j)),rtemp)
           if(ierr.ne.0)then
             call num2char(jline,aline)
             write(amessage,580) trim(aline),trim(astring)
580          format('cannot read time series value from line ',a,' of HSPF ', &
             'PLOTGEN file ',a)
             go to 9800
           end if
           if(rtemp.gt.threshold+3*spacing(threshold))then
             iiterm(j)=iiterm(j)+1
             series(jjseries(j))%val(iiterm(j))=rtemp
             series(jjseries(j))%days(iiterm(j))=ndays
             series(jjseries(j))%secs(iiterm(j))=nsecs
           end if
         end do
640      continue
       end do
650    continue
       do j=1,jseries
         if(iiterm(j).eq.0)then
           write(amessage,630) trim(aname(j)),trim(astring)
630        format('no terms can be imported into series ',a, &
           ' from HSPF PLOTGEN file ',a)
           go to 9800
         end if
         series(jjseries(j))%nterm=iiterm(j)
         write(*,660) trim(aname(j)),trim(astring)
         write(recunit,660) trim(aname(j)),trim(astring)
660      format(t5,'Series "',a,'" successfully imported from file ',a)
       end do
       go to 9900

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
       write(amessage,9210) trim(aline),trim(astring)
9210   format('unable to read line ',a,' of file ',a)
       go to 9800
9300   continue
       write(amessage,9310) trim(astring)
9310   format('premature end encountered to HSPF PLOTGEN file ',a)
       go to 9800
9320   continue
       write(amessage,9330) trim(astring)
9330   format('cannot locate "Threshold" value in HSPF PLOTGEN file ',a)
       go to 9800
9350   continue
       write(amessage,9360) trim(astring)
9360   format('cannot locate label list in HSPF PLOTGEN file ',a)
       go to 9800
9400   continue
       write(amessage,9410) trim(astring)
9410   format('unexpected end encountered to HSPF PLOTGEN file ',a,' while reading ', &
       'list of curve labels.')
       go to 9800
9450   continue
       write(amessage,9460) trim(astring)
9460   format('unexpected end encountered to HSPF PLOTGEN file ',a,' while looking ', &
       'for curve data.')
       go to 9800
9500   call num2char(jline,aline)
       write(amessage,9510) trim(aline),trim(astring)
9510   format('cannot read date/time from line ',a,' of HSPF PLOTGEN file ',a)
       go to 9800

9800   call write_message(leadspace='yes',error='yes')
       call write_message(iunit=recunit,leadspace='yes')
       ifail=1

9900   if(iunit.ne.0)close(unit=iunit,iostat=ierr)
       return

end subroutine get_plt_series



subroutine erase_entity(ifail)

! -- Subroutine ERASE_ENTITY removes a TSPROC entity from memory.

       use tspvar
       use defn
       use inter
       implicit none

       integer, intent(out)   :: ifail

       integer iseries,icontext,ierr,istable,ivtable,idtable,j,is,ixcon, &
       ictable,ic
       integer eseries(MAXSERIES),evtable(MAXVTABLE),estable(MAXSTABLE), &
       edtable(MAXDTABLE),ectable(MAXCTABLE)
       character*20 aline
       character*25 aoption
       character*25 acontext(MAXCONTEXT)

       ifail=0
       icontext=0
       iseries=0
       istable=0
       ivtable=0
       idtable=0
       ictable=0
       currentblock='ERASE_ENTITY'
       ixcon=0

       write(*,10) trim(currentblock)
       write(recunit,10)trim(currentblock)
10     format(/,' Processing ',a,' block....')

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
         if(aoption.eq.'SERIES_NAME')then
           iseries=iseries+1
           if(iseries.gt.MAXSERIES)then
             call num2char(MAXSERIES,aline)
             write(amessage,100) trim(aline)
100          format('a maximum of ',a,' series can be cited in an ERASE_ENTITY block.')
             go to 9800
           end if
           call read_series_name(ierr,eseries(iseries),'SERIES_NAME')
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'S_TABLE_NAME')then
           istable=istable+1
           if(istable.gt.MAXSTABLE)then
             call num2char(MAXSTABLE,aline)
             write(amessage,102) trim(aline)
102          format('a maximum of ',a,' s_tables can be cited in an ERASE_ENTITY block.')
             go to 9800
           end if
           call read_table_name(ierr,estable(istable),1)
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'C_TABLE_NAME')then
           ictable=ictable+1
           if(ictable.gt.MAXCTABLE)then
             call num2char(MAXCTABLE,aline)
             write(amessage,110) trim(aline)
110          format('a maximum of ',a,' c_tables can be cited in an ERASE_ENTITY block.')
             go to 9800
           end if
           call read_table_name(ierr,ectable(ictable),4)
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'V_TABLE_NAME')then
           ivtable=ivtable+1
           if(ivtable.gt.MAXVTABLE)then
             call num2char(MAXVTABLE,aline)
             write(amessage,103) trim(aline)
103          format('a maximum of ',a,' v_tables can be cited in an ERASE_ENTITY block.')
             go to 9800
           end if
           call read_table_name(ierr,evtable(ivtable),2)
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'E_TABLE_NAME')then
           idtable=idtable+1
           if(idtable.gt.MAXDTABLE)then
             call num2char(MAXDTABLE,aline)
             write(amessage,104) trim(aline)
104          format('a maximum of ',a,' e_tables can be cited in an ERASE_ENTITY block.')
             go to 9800
           end if
           call read_table_name(ierr,edtable(idtable),3)
           if(ierr.ne.0) go to 9800
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
           go to 200
         else
           call num2char(iline,aline)
           call addquote(infile,astring)
           write(amessage,180) trim(aoption),trim(aline),trim(astring)
180        format('unexpected keyword - "',a,'" in ERASE_ENTITY block at line ',a, &
           ' of file ',a)
           go to 9800
         end if
       end do

! -- The block has been read; now it is checked for correctness.

200    continue
       if((iseries.eq.0).and.(istable.eq.0).and.(ivtable.eq.0).and.   &
          (idtable.eq.0).and.(ictable.eq.0))then
         write(amessage,210)
210      format('no series or tables have been named for deletion in ERASE_ENTITY block.')
         go to 9800
       end if
       if(icontext.eq.0)then
         write(amessage,220)
220      format('no CONTEXT keyword(s) provided in ERASE_ENTITY block.')
         go to 9800
       end if

       if(iseries.eq.0) go to 300
       do j=1,iseries
         is=eseries(j)
         deallocate(series(is)%days,series(is)%secs,series(is)%val,stat=ierr)
         if(ierr.ne.0)then
           write(amessage,230)
230        format('cannot de-allocate memory previously allocated to erased time series.')
           go to 9800
         end if
         nullify(series(is)%days,series(is)%secs,series(is)%val)
         series(is)%active=.false.
         series(is)%nterm=0
         series(is)%type=' '
         write(*,250) trim(series(is)%name)
         write(recunit,250) trim(series(is)%name)
250      format(t5,'Series "',a,'" erased.')
         series(is)%name=' '
       end do

300    continue
       if(istable.eq.0) go to 350
       do j=1,istable
         is=estable(j)
         stable(is)%active=.false.
         write(*,320) trim(stable(is)%name)
         write(recunit,320) trim(stable(is)%name)
320      format(t5,'s_table "',a,'" erased.')
         stable(is)%name=' '
       end do

350    continue
       if(ictable.eq.0) go to 400
       do j=1,ictable
         ic=ectable(j)
         ctable(ic)%active=.false.
         write(*,321) trim(ctable(ic)%name)
         write(recunit,321) trim(ctable(ic)%name)
321      format(t5,'c_table "',a,'" erased.')
         ctable(ic)%name=' '
       end do
       
400    continue
       if(ivtable.eq.0) go to 500
       do j=1,ivtable
         is=evtable(j)
         vtable(is)%active=.false.
         deallocate(vtable(is)%days1,vtable(is)%days2,vtable(is)%secs1,  &
                    vtable(is)%secs2,vtable(is)%vol,stat=ierr)
         if(ierr.ne.0)then
           write(amessage,420)
420        format('cannot de-allocate memory previously allocated to erased V_TABLE.')
           go to 9800
         end if
         nullify(vtable(is)%days1,vtable(is)%days2,vtable(is)%secs1,   &
                 vtable(is)%secs2,vtable(is)%vol)
         vtable(is)%nterm=0
         vtable(is)%series_name=' '
         write(*,430) trim(vtable(is)%name)
         write(recunit,430) trim(vtable(is)%name)
430      format(t5,'v_table "',a,'" erased.')
         vtable(is)%name=' '
       end do

500    continue
       if(idtable.eq.0) go to 600
       do j=1,idtable
         is=edtable(j)
         dtable(is)%active=.false.
         deallocate(dtable(is)%flow,dtable(is)%time,dtable(is)%tdelay,stat=ierr)
         if(ierr.ne.0)then
           write(amessage,520)
520        format('cannot de-allocate memory previously allocated to erased E_TABLE.')
           go to 9800
         end if
         nullify(dtable(is)%time,dtable(is)%flow,dtable(is)%tdelay)
         dtable(is)%nterm=0
         dtable(is)%series_name=' '
         write(*,521) trim(dtable(is)%name)
         write(recunit,521) trim(dtable(is)%name)
521      format(t5,'e_table "',a,'" erased.')
         dtable(is)%name=' '
       end do
600    continue
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

9800   call write_message(leadspace='yes',error='yes')
       call write_message(iunit=recunit,leadspace='yes')
       ifail=1

       return

end subroutine erase_entity




subroutine update_time(curtun,curtst,days,secs,dd,mm,yy,hh,nn,ss)

! -- Subroutine UPDATE_TIME is called by a modified version of one of the WDM
!    utilities. Its role is to update the elapased time on the basis of time units
!    and time step length. Note that it only actually uses and updates dates (ie.
!    the last six of the above subroutine arguments), when the time step is in
!    months.

       use defn
       use inter
       implicit none

       integer, intent(in)              :: curtun,curtst
       integer, intent(inout)           :: days,secs,dd,mm,yy,hh,nn,ss
       integer tdd

       if(curtun.eq.1)then
         secs=secs+1*curtst
       else if(curtun.eq.2)then
         secs=secs+60*curtst
       else if(curtun.eq.3)then
         secs=secs+3600*curtst
       else if(curtun.eq.4)then
         days=days+1*curtst
       else if(curtun.eq.5)then
         mm=mm+1*curtst
10       if(mm.gt.12)then
           yy=yy+1
           mm=mm-12
           go to 10
         end if
         tdd=dd
         if(dd.eq.31)then
           if((mm.eq.9).or.(mm.eq.4).or.(mm.eq.6).or.(mm.eq.11))then
             tdd=30
           end if
         end if
         if((mm.eq.2).and.(tdd.gt.28))then
           if(leap(yy))then
             tdd=29
           else
             tdd=28
           end if
         end if
         days=numdays(1,1,1970,tdd,mm,yy)
         secs=numsecs(0,0,0,hh,mm,ss)
       else if(curtun.eq.6)then
         yy=yy+1
         tdd=dd
         if((mm.eq.2).and.(dd.gt.28))then
           if(leap(yy))then
             tdd=29
           else
             tdd=28
           end if
         end if
         days=numdays(1,1,1970,tdd,mm,yy)
         secs=numsecs(0,0,0,hh,mm,ss)
       end if

20     if(secs.ge.86400)then
         secs=secs-86400
         days=days+1
         go to 20
       end if

       return

end subroutine update_time





! don't forget to initialise things to INACTIVE.
!  block works ok for days before 1970
! In the manual point out that equations have no continuation capacity, and that they can
!  be no more than 250 or so characters in length.
! The DEF_TIME keyword must NOT act on samples unless the time series is a day or greater!!!!!!
! Check that the entries in a dates file can be in any order (ie. that time spans don't
!  need to follow eachother.
! Check that only one parameter data file and parameter group file are cited
!   in a WRITE_PEST_FILES block.

!     Last change:  J    10 Sep 2004    0:00 am
subroutine reduce_span(ifail)

! -- Subroutine REDUCE_SPAN shortens the time-span of a time series.

       use tspvar
       use defn
       use inter
       implicit none

       integer, intent(out)   :: ifail

       integer dd1,mm1,yy1,hh1,nn1,ss1,dd2,mm2,yy2,hh2,nn2,ss2,ierr, &
       icontext,i,begdays,begsecs,enddays,endsecs,iterm,j,           &
       iseries,k,ibterm,ieterm,ixcon,ilikeseries
       character*10 aname,alikename
       character*15 aline
       character*25 aoption
       character*25 acontext(MAXCONTEXT)

       ifail=0
       currentblock='REDUCE_TIME_SPAN'

       write(*,10) trim(currentblock)
       write(recunit,10) trim(currentblock)
10     format(/,' Processing ',a,' block....')

       icontext=0
       iseries=0
       ilikeseries=-9999
       yy1=-9999
       hh1=-9999
       yy2=-9999
       hh2=-9999
       aname=' '
       alikename=' '
       ixcon=0

! -- The REDUCE_TIME_SPAN block is first parsed.

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
         if(aoption.eq.'DATE_1')then
           call read_date(ierr,dd1,mm1,yy1,'DATE_1')
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'DATE_2')then
           call read_date(ierr,dd2,mm2,yy2,'DATE_2')
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'TIME_1')then
           call read_time(ierr,hh1,nn1,ss1,'TIME_1')
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'TIME_2')then
           call read_time(ierr,hh2,nn2,ss2,'TIME_2')
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'NEW_SERIES_NAME')then
           call read_new_series_name(ierr,aname)
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'SERIES_NAME')then
           call read_series_name(ierr,iseries,'SERIES_NAME')
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'LIKE_SERIES_NAME')then
           call read_series_name(ierr,ilikeseries,'LIKE_SERIES_NAME')
           if(ierr.ne.0) go to 9800  
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
           go to 200
         else
           call num2char(iline,aline)
           call addquote(infile,astring)
           write(amessage,90) trim(aoption),trim(currentblock),trim(aline),trim(astring)
90         format('unexpected keyword - "',a,'" in ',a,' block at line ',a, &
           ' of file ',a)
           go to 9800
         end if
       end do

! -- The block has been read; now it is checked for correctness.

200    continue
       if(iseries.eq.0)then
         write(amessage,210) trim(currentblock)
210      format('no SERIES_NAME keyword provided in ',a,' block.')
         go to 9800
       end if
       if(aname.eq.' ')then
         write(amessage,230) trim(currentblock)
230      format('no NEW_SERIES_NAME keyword provided in ',a,' block.')
         go to 9800
       end if
       if(icontext.eq.0)then
         write(amessage,220) trim(currentblock)
220      format('no CONTEXT keyword(s) provided in ',a,' block.')
         go to 9800
       end if
       if((yy1.eq.-9999).and.(yy2.eq.-9999).and.(ilikeseries.eq.-9999))then
         write(amessage,235) trim(currentblock)
235      format('neither a DATE_1 keyword nor a DATE_2 nor a LIKE_SERIES_NAME keyword provided in ',a,' block')
         go to 9800
       end if
       
       if(ilikeseries.eq.-9999)then
           call date_check(ierr,yy1,mm1,dd1,hh1,nn1,ss1,yy2,mm2,dd2,hh2,nn2,ss2,  &
           begdays,begsecs,enddays,endsecs)
           if(ierr.ne.0) go to 9800           
       else
         begdays = series(ilikeseries)%days(1)
         begsecs = series(ilikeseries)%secs(1)
         enddays = series(ilikeseries)%days(series(ilikeseries)%nterm)
         endsecs = series(ilikeseries)%secs(series(ilikeseries)%nterm)
       end if
       call beg_end_check(ierr,iseries,begdays,begsecs,enddays,endsecs)
       if(ierr.ne.0) go to 9800
    ! -- The new series is now written. But first the number of terms in the new series
    !    is counted.

           call numterms(iterm,ibterm,ieterm,begdays,begsecs,enddays,endsecs,iseries)
           if(iterm.le.0)then
             write(amessage,315)
    315      format('there are no terms in the reduced-time-span series.')
             go to 9800
           end if    
           

       do i=1,MAXSERIES
         if(.not.series(i)%active) go to 515
       end do
       write(amessage,510)
510    format('no more time series available for data storage - increase MAXSERIES and ', &
       'recompile program.')
       go to 9800

515    allocate(series(i)%days(iterm),series(i)%secs(iterm),  &
       series(i)%val(iterm),stat=ierr)
       if(ierr.ne.0)then
         write(amessage,550)
550      format('cannot allocate memory for another time series.')
         go to 9800
       end if
       series(i)%active=.true.
       series(i)%name=aname
       series(i)%nterm=iterm
       series(i)%type='ts'
       k=0
       do j=ibterm,ieterm
         k=k+1
         series(i)%days(k)=series(iseries)%days(j)
       end do
       k=0
       do j=ibterm,ieterm
         k=k+1
         series(i)%secs(k)=series(iseries)%secs(j)
       end do
       k=0
       do j=ibterm,ieterm
         k=k+1
         series(i)%val(k)=series(iseries)%val(j)
       end do
       write(*,580) trim(aname)
       write(recunit,580) trim(aname)
580    format(t5,'Series "',a,'" successfully calculated.')
       return

9000   call num2char(iline,aline)
       call addquote(infile,astring)
       write(amessage,9010) trim(aline), trim(astring)
9010   format('cannot read line ',a,' of TSPROC input file ',a)
       go to 9800
9100   continue
       call addquote(infile,astring)
       write(amessage,9110) trim(astring), trim(currentblock)
9110   format('unexpected end encountered to TSPROC input file ',a,' while ', &
       ' reading ',a,' block.')
       go to 9800

9800   call write_message(leadspace='yes',error='yes')
       call write_message(iunit=recunit,leadspace='yes')
       ifail=1

       return

end subroutine reduce_span




subroutine statistics(ifail)

! -- Subroutine STATISTICS calculates summary statistics for a time series.

       use tspvar
       use defn
       use inter
       implicit none

       integer, intent(out)   :: ifail

       integer dd1,mm1,yy1,hh1,nn1,ss1,dd2,mm2,yy2,hh2,nn2,ss2,ierr, &
       icontext,i,begdays,begsecs,enddays,endsecs,iseries,jtrans,javerage, &
       jstddev,jmaximum,jminimum,jsum,j,ibterm,ieterm,iterm,iiterm,itemp,ixcon, &
       iitemp,jj,minaverage,maxaverage,ii,nnterm,jrange
       real tpower,tsum,tmin,tmax,rtemp,raverage,localsum,tminmean,tmaxmean
       character*3 aaa
       character*10 aname,atemp
       character*15 aline
       character*25 aoption
       character*25 acontext(MAXCONTEXT)

       ifail=0
       currentblock='SERIES_STATISTICS'

       write(*,10) trim(currentblock)
       write(recunit,10) trim(currentblock)
10     format(/,' Processing ',a,' block....')

       icontext=0
       iseries=0
       yy1=-9999
       hh1=-9999
       yy2=-9999
       hh2=-9999
       jtrans=0
       javerage=0
       jstddev=0
       jmaximum=0
       jminimum=0
       jrange=0
       jsum=0
       aname=' '
       tpower=-1.0e35
       ixcon=0
       minaverage=0
       maxaverage=0

! -- The SERIES_STATISTICS block is first parsed.

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
         if(aoption.eq.'DATE_1')then
           call read_date(ierr,dd1,mm1,yy1,'DATE_1')
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'DATE_2')then
           call read_date(ierr,dd2,mm2,yy2,'DATE_2')
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'TIME_1')then
           call read_time(ierr,hh1,nn1,ss1,'TIME_1')
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'TIME_2')then
           call read_time(ierr,hh2,nn2,ss2,'TIME_2')
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'NEW_S_TABLE_NAME')then
           call read_new_table_name(ierr,1,aname)
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'SERIES_NAME')then
           call read_series_name(ierr,iseries,'SERIES_NAME')
           if(ierr.ne.0) go to 9800
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
         else if(aoption.eq.'POWER')then
           call get_keyword_value(ierr,2,itemp,tpower,'POWER')
           if(ierr.ne.0) go to 9800
           if(tpower.eq.0.0)then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,125) trim(aline),trim(astring)
125          format('POWER must not be zero at line ',a,' of file ',a)
             go to 9800
           end if
         else if(aoption.eq.'LOG')then
           call get_yes_no(ierr,jtrans)
           if(ierr.ne.0) go to 9800
           if(jtrans.eq.1)then
             aaa='yes'
           else
             aaa='no'
           end if
           write(*,127) trim(aaa)
           write(recunit,127) trim(aaa)
127        format(t5,'LOG ',a)
         else if(aoption.eq.'MEAN')then
           call get_yes_no(ierr,javerage)
           if(ierr.ne.0) go to 9800
           if(javerage.eq.1)then
             aaa='yes'
           else
             aaa='no'
           end if
           write(*,128) trim(aaa)
           write(recunit,128) trim(aaa)
128        format(t5,'MEAN ',a)
         else if(aoption(1:8).eq.'MINMEAN_')then
           call get_yes_no(ierr,iitemp)
           if(ierr.ne.0) go to 9800
           if(iitemp.eq.1)then
             aaa='yes'
           else
             aaa='no'
             go to 178
           end if
           if(minaverage.ne.0)then
             write(amessage,156) trim(currentblock)
156          format('only one MINMEAN_* keyword is allowed in each ',a,' block.')
             go to 9800
           else
             minaverage=iitemp
           end if
           atemp=aoption(9:)
           call char2num(ierr,atemp,iitemp)
           if(ierr.ne.0)then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,154) trim(aline),trim(astring)
154          format('cannot read averaging count for MINMEAN_* keyword at line ',  &
             a,' of file ',a)
             go to 9800
           end if
           if(iitemp.le.0)then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,153) trim(aline),trim(astring)
153          format('illegal averaging count for MINMEAN_* keyword at line ',  &
             a,' of file ',a)
             go to 9800
           end if
           minaverage=iitemp
178        continue
           write(*,151) trim(aoption),trim(aaa)
           write(recunit,151) trim(aoption),trim(aaa)
151        format(t5,a,1x,a)
         else if(aoption(1:8).eq.'MAXMEAN_')then
           call get_yes_no(ierr,iitemp)
           if(ierr.ne.0) go to 9800
           if(iitemp.eq.1)then
             aaa='yes'
           else
             aaa='no'
             go to 179
           end if
           if(maxaverage.ne.0)then
             write(amessage,138) trim(currentblock)
138          format('only one MAXMEAN_* keyword is allowed in each ',a,' block.')
             go to 9800
           end if
           maxaverage=iitemp
           atemp=aoption(9:)
           call char2num(ierr,atemp,iitemp)
           if(ierr.ne.0)then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,149) trim(aline),trim(astring)
149          format('cannot read averaging count for MAXMEAN_* keyword at line ',  &
             a,' of file ',a)
             go to 9800
           end if
           if(iitemp.le.0)then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,139) trim(aline),trim(astring)
139          format('illegal averaging count for MAXMEAN_* keyword at line ',  &
             a,' of file ',a)
             go to 9800
           end if
           maxaverage=iitemp
179        continue
           write(*,151) trim(aoption),trim(aaa)
           write(recunit,151) trim(aoption),trim(aaa)
         else if((aoption.eq.'STD_DEV').or.(aoption.eq.'STANDARD_DEVIATION'))then
           call get_yes_no(ierr,jstddev)
           if(ierr.ne.0) go to 9800
           if(jstddev.eq.1)then
             aaa='yes'
           else
             aaa='no'
           end if
           write(*,129) trim(aaa)
           write(recunit,129) trim(aaa)
129        format(t5,'STD_DEV ',a)
         else if(aoption.eq.'MAXIMUM')then
           call get_yes_no(ierr,jmaximum)
           if(ierr.ne.0) go to 9800
           if(jmaximum.eq.1)then
             aaa='yes'
           else
             aaa='no'
           end if
           write(*,132) trim(aaa)
           write(recunit,132) trim(aaa)
132        format(t5,'MAXIMUM ',a)
         else if(aoption.eq.'MINIMUM')then
           call get_yes_no(ierr,jminimum)
           if(ierr.ne.0) go to 9800
           if(jminimum.eq.1)then
             aaa='yes'
           else
             aaa='no'
           end if
           write(*,133) trim(aaa)
           write(recunit,133) trim(aaa)
133        format(t5,'MINIMUM ',a)
         else if(aoption.eq.'RANGE')then
           call get_yes_no(ierr,jrange)
           if(ierr.ne.0) go to 9800
           if(jrange.eq.1)then
             aaa='yes'
           else
             aaa='no'
           end if
           write(*,136) trim(aaa)
           write(recunit,136) trim(aaa)
136        format(t5,'RANGE ',a)
         else if(aoption.eq.'SUM')then
           call get_yes_no(ierr,jsum)
           if(ierr.ne.0) go to 9800
           if(jsum.eq.1)then
             aaa='yes'
           else
             aaa='no'
           end if
           write(*,134) trim(aaa)
           write(recunit,134) trim(aaa)
134        format(t5,'SUM ',a)
         else if(aoption.eq.'END')then
           go to 200
         else
           call num2char(iline,aline)
           call addquote(infile,astring)
           write(amessage,90) trim(aoption),trim(currentblock),trim(aline),trim(astring)
90         format('unexpected keyword - "',a,'" in ',a,' block at line ',a, &
           ' of file ',a)
           go to 9800
         end if
       end do

! -- The block has been read; now it is checked for correctness.

200    continue
       if(iseries.eq.0)then
         write(amessage,210) trim(currentblock)
210      format('no SERIES_NAME keyword provided in ',a,' block.')
         go to 9800
       end if
       if(aname.eq.' ')then
         write(amessage,230) trim(currentblock)
230      format('no NEW_S_TABLE keyword provided in ',a,' block.')
         go to 9800
       end if
       if(icontext.eq.0)then
         write(amessage,220) trim(currentblock)
220      format('no CONTEXT keyword(s) provided in ',a,' block.')
         go to 9800
       end if
       call date_check(ierr,yy1,mm1,dd1,hh1,nn1,ss1,yy2,mm2,dd2,hh2,nn2,ss2,  &
       begdays,begsecs,enddays,endsecs)
       if(ierr.ne.0) go to 9800
       call beg_end_check(ierr,iseries,begdays,begsecs,enddays,endsecs)
       if(ierr.ne.0) go to 9800
       if((javerage.eq.0).and.(jstddev.eq.0).and.(jmaximum.eq.0)  &
         .and.(jminimum.eq.0).and.(jsum.eq.0).and.(maxaverage.eq.0)  &
         .and.(minaverage.eq.0).and.(jrange.eq.0))then
         write(amessage,240) trim(currentblock)
240      format('at least one of the MEAN, STD_DEV, MAXIMUM, MINIMUM, ', &
         'RANGE, SUM, MINMEAN_* or MAXMEAN_*  keywords must be supplied within a ',  &
         a,' block.')
         go to 9800
       end if
       if((jtrans.eq.1).and.(tpower.gt.-1.0e30))then
         write(amessage,245) trim(currentblock)
245      format('either the LOG or POWER keywords can be supplied ', &
         'in a ',a,' block, but not both.')
         go to 9800
       end if
       if((minaverage.ne.0).or.(maxaverage.ne.0))then
         if((jtrans.eq.1).or.(tpower.gt.-1.0d30))then
           write(amessage,246) trim(currentblock)
246        format('if a MINMEAN_* or MAXMEAN_* keyword is supplied in ',a,' block, ', &
           'then neither the LOG or POWER keywords can be supplied in the same block.')
           go to 9800
         end if
       end if
       if(minaverage.ne.0)then
         if(maxaverage.ne.0)then
           if(minaverage.ne.maxaverage)then
             write(amessage,247) trim(currentblock)
247          format('if both a MINMEAN_* and a MAXMEAN_* keyword are supplied ',   &
             'in a ',a,' block, then the averaging count must be the same for both.')
             go to 9800
           end if
         end if
       end if

! -- All is well with the block. The STABLE is filled with requested statistics.

       call numterms(iterm,ibterm,ieterm,begdays,begsecs,enddays,endsecs,iseries)
       if(iterm.eq.0)then
         write(amessage,270) trim(series(iseries)%name)
270      format('there are no terms in time series "',a,'" between the provided ', &
         'dates and times.')
         go to 9800
       end if
       if((minaverage.gt.iterm).or.(maxaverage.gt.iterm))then
         write(amessage,271)
271      format('the averaging count provided with the MINMEAN_* and/or ', &
         'MAXMEAN_* keyword is greater than the number of terms in the block.')
         go to 9800
       end if


       do i=1,MAXSTABLE
         if(.not.stable(i)%active) go to 300
       end do
       write(amessage,310)
310    format('no more S_TABLE''s available for data storage - increase MAXSTABLE and ', &
       'recompile program.')
       go to 9800
300    continue

       if((begdays.lt.series(iseries)%days(1)).or.  &
         ((begdays.eq.series(iseries)%days(1)).and. &
          (begsecs.lt.series(iseries)%secs(1))))then
         begdays=series(iseries)%days(1)
         begsecs=series(iseries)%secs(1)
       end if
       iiterm=series(iseries)%nterm
       if((enddays.gt.series(iseries)%days(iiterm)).or.  &
         ((enddays.eq.series(iseries)%days(iiterm)).and. &
          (endsecs.gt.series(iseries)%secs(iiterm))))then
         enddays=series(iseries)%days(iiterm)
         endsecs=series(iseries)%secs(iiterm)
       end if

       if(tpower.lt.-1.0e30)tpower=0.0
       stable(i)%active=.true.
       stable(i)%name=aname
       stable(i)%rec_icount=iterm
       stable(i)%series_name=series(iseries)%name
       stable(i)%rec_itrans=jtrans
       if(begdays.eq.-99999999)then
         stable(i)%rec_begdays=series(iseries)%days(1)
         stable(i)%rec_begsecs=series(iseries)%secs(1)
       else
         stable(i)%rec_begdays=begdays
         stable(i)%rec_begsecs=begsecs
       end if
       if(enddays.eq.99999999)then
         stable(i)%rec_enddays=series(iseries)%days(iiterm)
         stable(i)%rec_endsecs=series(iseries)%secs(iiterm)
       else
         stable(i)%rec_enddays=enddays
         stable(i)%rec_endsecs=endsecs
       end if
       stable(i)%rec_power=tpower

       tsum=0.0
       tmin=1.0e30
       tmax=-1.0e30
       tminmean=1.0e30
       tmaxmean=-1.0e30
       if(jtrans.eq.1)then
         do j=ibterm,ieterm
           rtemp=series(iseries)%val(j)
           if(rtemp.le.0.0)then
             write(amessage,350) trim(series(iseries)%name)
350          format('cannot compute statistics on basis of log transform of terms ', &
             'in series "',a,'" as there are zero or negative terms in this series.')
             go to 9800
           end if
           rtemp=log10(rtemp)
           tsum=tsum+rtemp
           if(rtemp.lt.tmin)tmin=rtemp
           if(rtemp.gt.tmax)tmax=rtemp
         end do
       else
         if(tpower.eq.0.0)then
           do j=ibterm,ieterm
             rtemp=series(iseries)%val(j)
             tsum=tsum+rtemp
             if(rtemp.lt.tmin)tmin=rtemp
             if(rtemp.gt.tmax)tmax=rtemp
             if((maxaverage.gt.0).or.(minaverage.gt.0))then
               localsum=0
               nnterm=max(minaverage,maxaverage)
               do ii=1,nnterm
                 jj=j+ii-1
                 if(jj.gt.ieterm) go to 359
                 localsum=localsum+series(iseries)%val(jj)
               end do
               localsum=localsum/nnterm
               if(maxaverage.gt.0)then
                 if(localsum.gt.tmaxmean)tmaxmean=localsum
               end if
               if(minaverage.gt.0)then
                 if(localsum.lt.tminmean)tminmean=localsum
               end if
359            continue
             end if
           end do
         else
           do j=ibterm,ieterm
             rtemp=series(iseries)%val(j)
             if((tpower.lt.0.0).and.(rtemp.eq.0.0))then
               write(amessage,355) trim(series(iseries)%name)
355            format('cannot compute statistics based on a negative POWER because ', &
               'at least one of the terms of series "',a,'" is zero.')
               go to 9800
             end if
             if((abs(tpower).lt.1.0).and.(rtemp.lt.0.0))then
               write(amessage,360) trim(series(iseries)%name)
360            format('cannot compute statistics based on a POWER with absolute value ', &
               'less than one because ', &
               'at least one of the terms of series "',a,'" is negative.')
               go to 9800
             end if
             rtemp=rtemp**tpower
             tsum=tsum+rtemp
             if(rtemp.lt.tmin)tmin=rtemp
             if(rtemp.gt.tmax)tmax=rtemp
           end do
         end if
       end if
       raverage=tsum/iterm
       if(jmaximum.eq.1)then
         stable(i)%maximum=tmax
       else
         stable(i)%maximum=-1.0e37
       end if
       if(jminimum.eq.1)then
         stable(i)%minimum=tmin
       else
         stable(i)%minimum=-1.0e37
       end if
       if(jrange.eq.1)then
         stable(i)%range=tmax-tmin
       else
         stable(i)%range=-1.0e37
       end if
       if(javerage.eq.1)then
         stable(i)%mean=raverage
       else
         stable(i)%mean=-1.0e37
       end if
       if(jsum.eq.1)then
         stable(i)%total=tsum
       else
         stable(i)%total=-1.0e37
       end if
       if(jstddev.eq.0)then
         stable(i)%stddev=-1.0e37
       else
         tsum=0
         if(jtrans.eq.1)then
           do j=ibterm,ieterm
             rtemp=series(iseries)%val(j)
             rtemp=log10(rtemp)-raverage
             tsum=tsum+rtemp*rtemp
           end do
         else
           if(tpower.eq.0.0)then
             do j=ibterm,ieterm
               rtemp=series(iseries)%val(j)
               rtemp=rtemp-raverage
               tsum=tsum+rtemp*rtemp
             end do
           else
             do j=ibterm,ieterm
               rtemp=series(iseries)%val(j)
               rtemp=rtemp**tpower-raverage
               tsum=tsum+rtemp*rtemp
             end do
           end if
         end if
         if(iterm.eq.1)then
!           tsum=sqrt(tsum)
           tsum=0.0
         else
           tsum=sqrt(tsum/(iterm-1))
         end if
         stable(i)%stddev=tsum
       end if
       stable(i)%avetime=0
       if(maxaverage.eq.0)then
         stable(i)%maxmean=-1.0e37
       else
         stable(i)%maxmean=tmaxmean
         stable(i)%avetime=nnterm
       end if
       if(minaverage.eq.0)then
         stable(i)%minmean=-1.0e37
       else
         stable(i)%minmean=tminmean
         stable(i)%avetime=nnterm
       end if

       write(6,380) trim(series(iseries)%name),trim(aname)
       write(recunit,380) trim(series(iseries)%name),trim(aname)
380    format(t5,'Statistics for time series "',a,'" stored in ', &
       'S_TABLE "',a,'".')
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

9800   call write_message(leadspace='yes',error='yes')
       call write_message(iunit=recunit,leadspace='yes')
       ifail=1

       return

end subroutine statistics


subroutine time_base(ifail)

! -- Subroutine TIME_BASE spatially interpolates one time series to the sample dates/times
!    of another.

       use tspvar
       use defn
       use inter
       implicit none

       integer, intent(out)   :: ifail

       integer ierr,icontext,i,iseries,j,itbseries,ntermtb,ndaysbtb, &
       nsecsbtb,ndaysftb,nsecsftb,ntermos,ndaysbos,nsecsbos,ndaysfos,nsecsfos,istart, &
       intday,intsec,ixcon
       real valinterp
       character*10 aname
       character*15 aline
       character*25 aoption
       character*25 acontext(MAXCONTEXT)

interface
	subroutine time_interp_s(ifail,nbore,ndays,nsecs,value,intday, &
	intsec,rnear,rconst,valinterp,extrap,direction,startindex)
          integer, intent(out)                    :: ifail
          integer, intent(in)                     :: nbore
          integer, intent(in), dimension(nbore)   :: ndays,nsecs
          real, intent(in), dimension(nbore)      :: value
          integer, intent(in)                     :: intday,intsec
	  real, intent(in)			  :: rnear,rconst
          real, intent(out)                       :: valinterp
	  character (len=*), intent(in),optional  :: extrap
	  character (len=*), intent(in),optional  :: direction
          integer, intent(inout), optional        :: startindex
	end subroutine time_interp_s
end interface


       ifail=0
       currentblock='NEW_TIME_BASE'

       write(*,10) trim(currentblock)
       write(recunit,10) trim(currentblock)
10     format(/,' Processing ',a,' block....')

       itbseries=0
       icontext=0
       iseries=0
       aname=' '
       ixcon=0

! -- The NEW_TIME_BASE block is first parsed.

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
         if(aoption.eq.'NEW_SERIES_NAME')then
           call read_new_series_name(ierr,aname)
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'SERIES_NAME')then
           call read_series_name(ierr,iseries,'SERIES_NAME')
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'TB_SERIES_NAME')then
           call read_series_name(ierr,itbseries,'TB_SERIES_NAME')
           if(ierr.ne.0) go to 9800
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
           go to 200
         else
           call num2char(iline,aline)
           call addquote(infile,astring)
           write(amessage,90) trim(aoption),trim(currentblock),trim(aline),trim(astring)
90         format('unexpected keyword - "',a,'" in ',a,' block at line ',a, &
           ' of file ',a)
           go to 9800
         end if
       end do

! -- The block has been read; now it is checked for correctness.

200    continue
       if(iseries.eq.0)then
         write(amessage,210) trim(currentblock)
210      format('no SERIES_NAME keyword provided in ',a,' block.')
         go to 9800
       end if
       if(aname.eq.' ')then
         write(amessage,230) trim(currentblock)
230      format('no NEW_SERIES_NAME keyword provided in ',a,' block.')
         go to 9800
       end if
       if(itbseries.eq.0)then
         write(amessage,218) trim(currentblock)
218      format('no TB_SERIES_NAME keyword provided in ',a,' block.')
         go to 9800
       end if
       if(icontext.eq.0)then
         write(amessage,220) trim(currentblock)
220      format('no CONTEXT keyword(s) provided in ',a,' block.')
         go to 9800
       end if

       ntermtb=series(itbseries)%nterm
       ndaysbtb=series(itbseries)%days(1)
       nsecsbtb=series(itbseries)%secs(1)
       ndaysftb=series(itbseries)%days(ntermtb)
       nsecsftb=series(itbseries)%secs(ntermtb)
       ntermos=series(iseries)%nterm
       ndaysbos=series(iseries)%days(1)
       nsecsbos=series(iseries)%secs(1)
       ndaysfos=series(iseries)%days(ntermos)
       nsecsfos=series(iseries)%secs(ntermos)
       if((ndaysbtb.lt.ndaysbos).or.         &
         ((ndaysbtb.eq.ndaysbos).and.(nsecsbtb.lt.nsecsbos)))go to 9200
       if((ndaysftb.gt.ndaysfos).or.         &
         ((ndaysftb.eq.ndaysfos).and.(nsecsftb.gt.nsecsfos)))go to 9200

! -- Memory is now allocated for the new series prior to its being filled.

       do i=1,MAXSERIES
         if(.not.series(i)%active) go to 250
       end do
       write(amessage,240)
240    format('no more time series available for data storage - increase MAXSERIES and ', &
       'recompile program.')
       go to 9800
250    allocate(series(i)%days(ntermtb),series(i)%secs(ntermtb),  &
       series(i)%val(ntermtb),stat=ierr)
       if(ierr.ne.0)then
         write(amessage,560)
560      format('cannot allocate memory for another time series.')
         go to 9800
       end if
       series(i)%active=.true.
       series(i)%name=aname
       series(i)%nterm=ntermtb
       series(i)%type='ts'
       do j=1,ntermtb
         series(i)%days(j)=series(itbseries)%days(j)
       end do
       do j=1,ntermtb
         series(i)%secs(j)=series(itbseries)%secs(j)
       end do

! -- Temporal interpolation is now undertaken.

       istart=0
       do j=1,ntermtb
         intday=series(i)%days(j)
         intsec=series(i)%secs(j)
         call time_interp_s(ierr,ntermos,series(iseries)%days,series(iseries)%secs, &
         series(iseries)%val,intday,intsec,1.0e20,0.0,valinterp,startindex=istart)
         series(i)%val(j)=valinterp
       end do

       write(*,580) trim(aname)
       write(recunit,580) trim(aname)
580    format(t5,'New series "',a,'" successfully calculated.')
       return

9000   call num2char(iline,aline)
       call addquote(infile,astring)
       write(amessage,9010) trim(aline), trim(astring)
9010   format('cannot read line ',a,' of TSPROC input file ',a)
       go to 9800
9100   continue
       call addquote(infile,astring)
       write(amessage,9110) trim(astring)
9110   format('unexpected end encountered to TSPROC input file ',a,' while ', &
       ' reading REDUCE_TIME_SPAN block.')
       go to 9800
9200   write(amessage,9210)
9210   format('the time span of the time base series is greater than that of the ', &
       'series to be interpolated. Reduce the time span of the time base series to ', &
       'that of the series to be interpolated using a REDUCE_SPAN block.')
       go to 9800

9800   call write_message(leadspace='yes',error='yes')
       call write_message(iunit=recunit,leadspace='yes')
       ifail=1

       return

end subroutine time_base



subroutine volume(ifail)

! -- Subroutine VOLUME accumulates volumes between user-specified dates and times.

       use tspvar
       use defn
       use inter
       implicit none

       integer, intent(out)   :: ifail

       integer ierr,icontext,iseries,itunit,iunit,jline,ndate,iv,nsterm,nsdays1, &
       nssecs1,nsdays2,nssecs2,dd,mm,yy,hh,nn,ss,ndays1,nsecs1,ndays2,nsecs2,itemp,ixcon
       real factor,fac,volcalc
       character*10 aname
       character*15 aline
       character*25 aoption
       character*120 datefile
       character*25 acontext(MAXCONTEXT)

       ifail=0
       currentblock='VOLUME_CALCULATION'

       write(*,10) trim(currentblock)
       write(recunit,10) trim(currentblock)
10     format(/,' Processing ',a,' block....')

       icontext=0
       iseries=0
       aname=' '
       factor=1.0
       itunit=0
       datefile=' '
       ixcon=0
       iunit=0

! -- The VOLUME_CALCULATION block is first parsed.

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
         if(aoption.eq.'SERIES_NAME')then
           call read_series_name(ierr,iseries,'SERIES_NAME')
           if(ierr.ne.0) go to 9800
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
         else if(aoption.eq.'NEW_V_TABLE_NAME')then
           call read_new_table_name(ierr,2,aname)
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'FLOW_TIME_UNITS')then
           call read_time_units(ierr,itunit,1)
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'FACTOR')then
           call get_keyword_value(ierr,2,itemp,factor,'FACTOR')
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'DATE_FILE')then
           call getfile(ierr,cline,datefile,left_word(2),right_word(2))
           if(ierr.ne.0)then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,140) trim(aline),trim(astring)
140          format('cannot read date file name from line ',a,' of file ',a)
             go to 9800
           end if
           call addquote(datefile,astring)
           write(*,145) trim(astring)
           write(recunit,145) trim(astring)
145        format(t5,'DATE_FILE ',a)
         else if(aoption.eq.'END')then
           go to 200
         else
           call num2char(iline,aline)
           call addquote(infile,astring)
           write(amessage,90) trim(aoption),trim(currentblock),trim(aline),trim(astring)
90         format('unexpected keyword - "',a,'" in ',a,' block at line ',a, &
           ' of file ',a)
           go to 9800
         end if
       end do

200    continue

! -- The block has been read; now it is checked for absences.

       if(iseries.eq.0)then
         write(amessage,210) trim(currentblock)
210      format('no SERIES_NAME keyword provided in ',a,' block.')
         go to 9800
       end if
       if(aname.eq.' ')then
         write(amessage,230) trim(currentblock)
230      format('no NEW_V_TABLE_NAME keyword provided in ',a,' block.')
         go to 9800
       end if
       if(itunit.eq.0)then
         write(amessage,218) trim(currentblock)
218      format('no FLOW_TIME_UNITS keyword provided in ',a,' block.')
         go to 9800
       end if
       if(icontext.eq.0)then
         write(amessage,220) trim(currentblock)
220      format('no CONTEXT keyword(s) provided in ',a,' block.')
         go to 9800
       end if
       if(datefile.eq.' ')then
         write(amessage,240) trim(currentblock)
240      format('no DATE_FILE keyword provided in ',a,' block.')
         go to 9800
       end if

! -- The date file is now opened and the number of lines within it read.

       iunit=nextunit()
       call addquote(datefile,astring)
       open(unit=iunit,file=datefile,status='old',iostat=ierr)
       if(ierr.ne.0)then
         write(amessage,300) trim(astring)
300      format('cannot open dates file ',a)
         go to 9800
       end if
       write(6,305) trim(astring)
       write(recunit,305) trim(astring)
305    format(t5,'Reading dates file ',a,'....')
       jline=0
       ndate=0
       do
         jline=jline+1
         read(iunit,'(a)',end=350) cline
         if(cline.eq.' ') cycle
         if(cline(1:1).eq.'#') cycle
         ndate=ndate+1
       end do
350    continue
       if(ndate.eq.0)then
         write(amessage,360) trim(astring)
360      format('no dates found in dates file ',a)
         go to 9800
       end if
       rewind(unit=iunit,iostat=ierr)
       if(ierr.ne.0)then
         write(amessage,370) trim(astring)
370      format('cannot rewind dates file ',a)
         go to 9800
       end if

! -- Memory is now allocated for the v_table.

       do iv=1,MAXVTABLE
         if(.not.vtable(iv)%active) go to 380
       end do
       write(amessage,390)
390    format('no more v_tables available for data storage - increase MAXVTABLE and ', &
       'recompile program.')
       go to 9800
380    continue
       vtable(iv)%active=.true.
       vtable(iv)%name=aname
       vtable(iv)%series_name=series(iseries)%name
       allocate(vtable(iv)%days1(ndate),vtable(iv)%secs1(ndate),vtable(iv)%days2(ndate), &
       vtable(iv)%secs2(ndate),vtable(iv)%vol(ndate),stat=ierr)
       if(ierr.ne.0)then
         write(amessage,395)
395      format('cannot allocate memory for storage of v_table data.')
         go to 9800
       end if

       if(itunit.eq.1)then
         fac=86400.0
       else if(itunit.eq.2)then
         fac=1440.0
       else if(itunit.eq.3)then
         fac=24.0
       else if(itunit.eq.4)then
         fac=1.0
       else if(itunit.eq.5)then
         fac=1.0*12/365.25
       else
         fac=1.0/365.25
       end if

! -- The date file is now re-read and volumes calculated.

       jline=0
       ndate=0
       nsterm=series(iseries)%nterm
       nsdays1=series(iseries)%days(1)
       nssecs1=series(iseries)%secs(1)
       nsdays2=series(iseries)%days(nsterm)
       nssecs2=series(iseries)%secs(nsterm)
       do
         jline=jline+1
         read(iunit,'(a)',end=500) cline
         if(cline.eq.' ') cycle
         if(cline(1:1).eq.'#') cycle
         ndate=ndate+1
         call linesplit(ierr,4)
         if(ierr.ne.0)then
           call num2char(jline,aline)
           write(amessage,410) trim(aline),trim(astring)
410        format('four entries expected on line ',a,' of dates file ',a)
           go to 9800
         end if
         call char2date(ierr,cline(left_word(1):right_word(1)),dd,mm,yy)
         if(ierr.ne.0) go to 9200
         ndays1=numdays(1,1,1970,dd,mm,yy)
         call char2time(ierr,cline(left_word(2):right_word(2)),hh,nn,ss,ignore_24=1)
         if(ierr.ne.0) go to 9200
         nsecs1=numsecs(0,0,0,hh,nn,ss)
         if(nsecs1.ge.86400)then
           nsecs1=nsecs1-86400
           ndays1=ndays1+1
         end if
         call char2date(ierr,cline(left_word(3):right_word(3)),dd,mm,yy)
         if(ierr.ne.0) go to 9200
         ndays2=numdays(1,1,1970,dd,mm,yy)
         call char2time(ierr,cline(left_word(4):right_word(4)),hh,nn,ss,ignore_24=1)
         if(ierr.ne.0) go to 9200
         nsecs2=numsecs(0,0,0,hh,nn,ss)
         if(nsecs2.ge.86400)then
           nsecs2=nsecs2-86400
           ndays2=ndays2+1
         end if
         if((ndays1.gt.ndays2).or.         &
           ((ndays1.eq.ndays2).and.(nsecs1.ge.nsecs2)))then
           call num2char(jline,aline)
           write(amessage,420) trim(aline),trim(astring)
420        format('first date/time must precede second date/time at line ',a,  &
           ' of file ',a)
           go to 9800
         end if
         if((ndays1.lt.nsdays1).or.        &
           ((ndays1.eq.nsdays1).and.(nsecs1.lt.nssecs1)))then
           call num2char(jline,aline)
           write(amessage,425) trim(aline),trim(astring),trim(series(iseries)%name)
425        format('the first date/time on line ',a,' of file ',a,' predates the ', &
           'commencement of time series "',a,'".')
           go to 9800
         end if
         if((ndays2.gt.nsdays2).or.         &
           ((ndays2.eq.nsdays2).and.(nsecs2.gt.nssecs2)))then
           call num2char(jline,aline)
           write(amessage,426) trim(aline),trim(astring),trim(series(iseries)%name)
426        format('the second date/time on line ',a,' of file ',a,' postdates the ', &
           'end of time series "',a,'".')
           go to 9800
         end if
         vtable(iv)%days1(ndate)=ndays1
         vtable(iv)%secs1(ndate)=nsecs1
         vtable(iv)%days2(ndate)=ndays2
         vtable(iv)%secs2(ndate)=nsecs2
         call volume_interp_s(ierr,nsterm,series(iseries)%days,series(iseries)%secs,  &
         series(iseries)%val,ndays1,nsecs1,ndays2,nsecs2,volcalc,fac)
         vtable(iv)%vol(ndate)=volcalc*factor
       end do
500    continue
       vtable(iv)%nterm=ndate
       close(unit=iunit)
       write(*,430) trim(astring)
       write(recunit,430) trim(astring)
430    format(t5,'File ',a,' read ok.')
       write(*,440) trim(aname)
       write(recunit,440) trim(aname)
440    format(t5,'Volumes calculated and stored in v_table "',a,'".')
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
9200   continue
       call num2char(jline,aline)
       write(amessage,9210) trim(aline),trim(astring)
9210   format('erroneous date or time at line ',a,' of file ',a)
       go to 9800
9800   call write_message(leadspace='yes',error='yes')
       call write_message(iunit=recunit,leadspace='yes')
       ifail=1
       if(iunit.ne.0)close(unit=iunit,iostat=ierr)

       return

end subroutine volume



subroutine time_duration(ifail)

! -- Subroutine TIME_DURATION calculations exceedence durations for certain flows.

       use tspvar
       use defn
       use inter
       implicit none

       integer, intent(out)   :: ifail

       logical on,oldon
       integer ierr,icontext,iseries,itunit,iflow,id,i,ndays,nsecs,j,oldndays,oldnsecs, &
               nnterm,ixcon,iuo
       real rtemp,fac,duration,fflow,vval,oldvval,timediff,accumulation,timedelay
       character*10 aname,atemp
       character*15 aline
       character*25 aoption
       character*25 acontext(MAXCONTEXT)

       ifail=0
       currentblock='EXCEEDENCE_TIME'


       write(*,10) trim(currentblock)
       write(recunit,10) trim(currentblock)
10     format(/,' Processing ',a,' block....')

       icontext=0
       iseries=0
       aname=' '
       itunit=0
       iflow=0
       ixcon=0
       iuo=-999
       do i=1,MAXTEMPDURFLOW
         tempdtable%tdelay(i)=-1.1e36
       end do

! -- The EXCEEDENCE-TIME block is first parsed.

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
         if(aoption.eq.'SERIES_NAME')then
           call read_series_name(ierr,iseries,'SERIES_NAME')
           if(ierr.ne.0) go to 9800
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
         else if(aoption.eq.'NEW_E_TABLE_NAME')then
           call read_new_table_name(ierr,3,aname)
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'EXCEEDENCE_TIME_UNITS')then
           call read_time_units(ierr,itunit,2)
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'UNDER_OVER')then
           call getfile(ierr,cline,atemp,left_word(2),right_word(2))
           if(ierr.ne.0)then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,57) trim(aline),trim(astring)
57           format('cannot read UNDER_OVER from line ',a,' of file ',a)
             go to 9800
           end if
           call casetrans(atemp,'lo')
           if(atemp(1:5).eq.'under')then
             iuo=0
           else if(atemp(1:5).eq.'over')then
             iuo=1
           else
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,58) trim(aline),trim(astring)
58           format('UNDER_OVER must be "under" or "over" at line ',a,' of file ',a)
             go to 9800
           end if
           call addquote(atemp,astring)
           write(*,59) trim(astring)
           write(recunit,59) trim(astring)
59         format(t5,'UNDER_OVER ',a)
         else if(aoption.eq.'FLOW')then
           iflow=iflow+1
           if(iflow.gt.MAXTEMPDURFLOW)then
             call num2char(MAXTEMPDURFLOW,aline)
             write(amessage,30) trim(aline), trim(currentblock)
30           format('a maximum of ',a,' FLOWs are allowed in an ',a,' block.')
             go to 9800
           end if
           call char2num(ierr,cline(left_word(2):right_word(2)),rtemp)
           if(ierr.ne.0)then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,120) trim(aline),trim(astring)
120          format('cannot read flow from line ',a,' of file ',a)
             go to 9800
           end if
           write(*,130) cline(left_word(2):right_word(2))
           write(recunit,130) cline(left_word(2):right_word(2))
130        format(t5,'FLOW ',a)
           tempdtable%flow(iflow)=rtemp
         else if(aoption.eq.'DELAY')then
           if(iflow.eq.0)then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,320) trim(aline),trim(astring)
320          format('DELAY not preceeded by FLOW at line ',a,' of file ',a)
             go to 9800
           end if
           if(tempdtable%tdelay(iflow).gt.-1.0e36)then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,330) trim(aline),trim(astring)
330          format('more than one DELAY associated with FLOW at line ',a,' of file ',a)
             go to 9800
           end if
           call char2num(ierr,cline(left_word(2):right_word(2)),rtemp)
           if(ierr.ne.0)then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,335) trim(aline),trim(astring)
335          format('cannot read time delay from line ',a,' of file ',a)
             go to 9800
           end if
           if(rtemp.lt.0.0)then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,336) trim(aline),trim(astring)
336          format('time delay cannot be negative at line ',a,' of file ',a)
             go to 9800
           end if
           write(*,340) cline(left_word(2):right_word(2))
           write(recunit,340) cline(left_word(2):right_word(2))
340        format(t5,'DELAY ',a)
           tempdtable%tdelay(iflow)=rtemp
         else if(aoption.eq.'END')then
           go to 200
         else
           call num2char(iline,aline)
           call addquote(infile,astring)
           write(amessage,90) trim(aoption),trim(currentblock),trim(aline),trim(astring)
90         format('unexpected keyword - "',a,'" in ',a,' block at line ',a, &
           ' of file ',a)
           go to 9800
         end if
       end do

200    continue

! -- The block has been read; now it is checked for absences.

       if(iseries.eq.0)then
         write(amessage,210) trim(currentblock)
210      format('no SERIES_NAME keyword provided in ',a,' block.')
         go to 9800
       end if
       if(aname.eq.' ')then
         write(amessage,230) trim(currentblock)
230      format('no NEW_E_TABLE_NAME keyword provided in ',a,' block.')
         go to 9800
       end if
       if(itunit.eq.0)then
         write(amessage,218) trim(currentblock)
218      format('no EXCEEDENCE_TIME_UNITS keyword provided in ',a,' block.')
         go to 9800
       end if
       if(icontext.eq.0)then
         write(amessage,220) trim(currentblock)
220      format('no CONTEXT keyword(s) provided in ',a,' block.')
         go to 9800
       end if
       if(iflow.eq.0)then
         write(amessage,225) trim(currentblock)
225      format('no FLOW keywords provided in ',a,' block.')
         go to 9800
       end if
       do i=1,iflow
         if (tempdtable%tdelay(i).gt.-1.0e36) go to 360
       end do
       go to 400
360    do i=1,iflow
         if(tempdtable%tdelay(i).lt.-1.0e36)then
           write(amessage,370) trim(currentblock)
370        format('if any FLOW is associated with a DELAY, than all flows must be associated ',  &
           'with a DELAY in ',a,' block')
           go to 9800
         end if
       end do
400    continue
       if(series(iseries)%nterm.eq.1)then
         write(amessage,250) trim(series(iseries)%name)
250      format('cannot calculate exceedence times because time series "',a,   &
         '" has only one term.')
         go to 9800
       end if

! -- Space is now allocated in a non-temporary E_TABLE.

       do id=1,MAXDTABLE
         if(.not.dtable(id)%active) go to 380
       end do
       write(amessage,390)
390    format('no more e_tables available for data storage - increase MAXDTABLE and ', &
       'recompile program.')
       go to 9800
380    continue
       dtable(id)%active=.true.
       dtable(id)%name=aname
       dtable(id)%series_name=series(iseries)%name
       dtable(id)%nterm=iflow
       allocate(dtable(id)%flow(iflow),dtable(id)%time(iflow),  &
                dtable(id)%tdelay(iflow),stat=ierr)
       if(ierr.ne.0)then
         write(amessage,395)
395      format('cannot allocate memory for storage of e_table data.')
         go to 9800
       end if
       do i=1,iflow
         dtable(id)%flow(i)=tempdtable%flow(i)
         if(tempdtable%tdelay(i).lt.-1.0e36)then
           dtable(id)%tdelay(i)=0.0
         else
           dtable(id)%tdelay(i)=tempdtable%tdelay(i)
         end if
       end do

       if(itunit.eq.1)then
         fac=1.0
         dtable(id)%time_units='secs'
       else if(itunit.eq.2)then
         fac=1.0/60.0
         dtable(id)%time_units='mins'
       else if(itunit.eq.3)then
         fac=1.0/3600.0
         dtable(id)%time_units='hrs'
       else if(itunit.eq.4)then
         fac=1.0/86400.0
         dtable(id)%time_units='days'
       else if(itunit.eq.5)then
         fac=1.0/86400.0/(356.25/12.0)
         dtable(id)%time_units='mths'
       else
         fac=1.0/86400.0/365.25
         dtable(id)%time_units='yrs'
       end if
       if((iuo.eq.-999).or.(iuo.eq.1))then
         dtable(id)%under_over=1
         iuo=1
       else
         dtable(id)%under_over=0
         iuo=0
       end if

! -- Durations are now calculated for each flow.

       nnterm=series(iseries)%nterm
       do i=1,iflow
         timedelay=dtable(id)%tdelay(i)/fac
         duration=0.0
         accumulation=0.0
         fflow=dtable(id)%flow(i)
         vval=series(iseries)%val(1)
         ndays=series(iseries)%days(1)
         nsecs=series(iseries)%secs(1)
         if(iuo.eq.1)then
           if(vval.ge.fflow)then
             on=.true.
           else
             on=.false.
           end if
         else
           if(vval.le.fflow)then
             on=.true.
           else
             on=.false.
           end if
         end if
         do j=2,nnterm
           oldon=on
           oldvval=vval
           oldndays=ndays
           oldnsecs=nsecs
           vval=series(iseries)%val(j)
           ndays=series(iseries)%days(j)
           nsecs=series(iseries)%secs(j)
           if(iuo.eq.1)then
             if(vval.ge.fflow)then
               on=.true.
             else
               on=.false.
             end if
           else
             if(vval.le.fflow)then
               on=.true.
             else
               on=.false.
             end if
           end if
           if((on).and.(oldon))then
!             duration=duration+timediff
             timediff=float(ndays-oldndays)*86400.0+float(nsecs-oldnsecs)
             accumulation=accumulation+timediff
           else if((on).and.(.not.oldon))then
             timediff=float(ndays-oldndays)*86400.0+float(nsecs-oldnsecs)
             accumulation=timediff*(vval-fflow)/(vval-oldvval)
!             duration=duration+timediff*(vval-fflow)/(vval-oldvval)
           else if((oldon).and.(.not.on))then
             timediff=float(ndays-oldndays)*86400.0+float(nsecs-oldnsecs)
             accumulation=accumulation+timediff*(oldvval-fflow)/(oldvval-vval)
             duration=duration+max(0.0,accumulation-timedelay)
             accumulation=0.0
!             duration=duration+timediff*(oldvval-fflow)/(oldvval-vval)
           end if
         end do
         duration=duration+max(0.0,accumulation-timedelay)
         dtable(id)%time(i)=duration*fac
       end do

! -- The total time encompassed by the time series is now calculated.

       oldndays=series(iseries)%days(1)
       oldnsecs=series(iseries)%secs(1)
       ndays=series(iseries)%days(nnterm)
       nsecs=series(iseries)%secs(nnterm)
       dtable(id)%total_time=(float(ndays-oldndays)*86400.0+float(nsecs-oldnsecs))*fac

       write(*,440) trim(aname)
       write(recunit,440) trim(aname)
440    format(t5,'Exceedence times calculated and stored in e_table "',a,'".')
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
9800   call write_message(leadspace='yes',error='yes')
       call write_message(iunit=recunit,leadspace='yes')
       ifail=1

       return

end subroutine time_duration



subroutine displace(ifail)

! -- Subroutine DISPLACE moves a time series by a user-supplied number of time increments.

       use tspvar
       use defn
       use inter
       implicit none

       integer, intent(out)   :: ifail

       integer ierr,icontext,iseries,lag,itemp,nsterm,ilags,j,nsecs,ndays, &
       dd,mm,yy,hh,nn,ss,i,ixcon
       real fill,rtemp
       character*10 aname
       character*15 aline
       character*25 aoption
       character*25 acontext(MAXCONTEXT)

       ifail=0
       currentblock='SERIES_DISPLACE'

       write(*,10) trim(currentblock)
       write(recunit,10) trim(currentblock)
10     format(/,' Processing ',a,' block....')

       icontext=0
       iseries=0
       aname=' '
       lag=-9999
       fill=-1.1e36
       ixcon=0

! -- The SERIES_DISPLACE block is first parsed.

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
         if(aoption.eq.'NEW_SERIES_NAME')then
           call read_new_series_name(ierr,aname)
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'SERIES_NAME')then
           call read_series_name(ierr,iseries,'SERIES_NAME')
           if(ierr.ne.0) go to 9800
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
         else if(aoption.eq.'LAG_INCREMENT')then
           call get_keyword_value(ierr,1,lag,rtemp,'LAG_INCREMENT')
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'FILL_VALUE')then
           call get_keyword_value(ierr,2,itemp,fill,'FILL_VALUE')
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'END')then
           go to 200
         else
           call num2char(iline,aline)
           call addquote(infile,astring)
           write(amessage,90) trim(aoption),trim(currentblock),trim(aline),trim(astring)
90         format('unexpected keyword - "',a,'" in ',a,' block at line ',a, &
           ' of file ',a)
           go to 9800
         end if
       end do

! -- The block has been read; now it is checked for correctness.

200    continue
       if(iseries.eq.0)then
         write(amessage,210) trim(currentblock)
210      format('no SERIES_NAME keyword provided in ',a,' block.')
         go to 9800
       end if
       if(aname.eq.' ')then
         write(amessage,230) trim(currentblock)
230      format('no NEW_SERIES_NAME keyword provided in ',a,' block.')
         go to 9800
       end if
       if(icontext.eq.0)then
         write(amessage,220) trim(currentblock)
220      format('no CONTEXT keyword(s) provided in ',a,' block.')
         go to 9800
       end if
       if(lag.eq.-9999)then
         write(amessage,225) trim(currentblock)
225      format('no LAG_INCREMENT keyword provided in ',a,' block.')
         go to 9800
       end if
       if(fill.lt.-1.0e36)then
         write(amessage,240) trim(currentblock)
240      format('no FILL_VALUE keyword provided in ',a,' block.')
         go to 9800
       end if

! -- The DISPLACE operation can only be performed if the input time series has equal
!    increments. This is now tested.

       nsterm=series(iseries)%nterm
       if(nsterm.lt.abs(lag)+1)then
         call num2char(nsterm,aline)
         write(amessage,250) trim(series(iseries)%name),trim(aline)
250      format('series "',a,'" has only ',a,' terms. This is insufficient to perform ', &
         'the requested displacement operation.')
         go to 9800
       end if
       if(nsterm.gt.2)then
         ilags=(series(iseries)%days(2)-series(iseries)%days(1))*86400+   &
                series(iseries)%secs(2)-series(iseries)%secs(1)
         do j=2,nsterm-1
           nsecs=series(iseries)%secs(j)+ilags
           ndays=series(iseries)%days(j)
260        if(nsecs.ge.86400)then
             ndays=ndays+1
             nsecs=nsecs-86400
             go to 260
           end if
           if((nsecs.ne.series(iseries)%secs(j+1)).or.   &
              (ndays.ne.series(iseries)%days(j+1)))then
               call newdate(series(iseries)%days(j),1,1,1970,dd,mm,yy)
               nsecs=series(iseries)%secs(j)
               hh=nsecs/3600
               nn=(nsecs-hh*3600)/60
               ss=nsecs-hh*3600-nn*60
               if(datespec.eq.1) then
                 write(amessage,280) trim(series(iseries)%name),dd,mm,yy,hh,nn,ss
               else
                 write(amessage,280) trim(series(iseries)%name),mm,dd,yy,hh,nn,ss
               end if
280            format('time interval between terms in time series "',a,'" is not ', &
               'constant. The first discrepancy occurs following the sample taken on ',  &
               i2.2,'/',i2.2,'/',i4,' at ',i2.2,':',i2.2,':',i2.2)
               go to 9800
           end if
         end do
       end if

! -- Space for a new series is allocated.

       do i=1,MAXSERIES
         if(.not.series(i)%active) go to 515
       end do
       write(amessage,510)
510    format('no more time series available for data storage - increase MAXSERIES and ', &
       'recompile program, or erase a series using an ERASE_SERIES block.')
       go to 9800

515    continue
       allocate(series(i)%days(nsterm),series(i)%secs(nsterm),  &
       series(i)%val(nsterm),stat=ierr)
       if(ierr.ne.0)then
         write(amessage,550)
550      format('cannot allocate memory for another time series.')
         go to 9800
       end if
       series(i)%active=.true.
       series(i)%name=aname
       series(i)%nterm=nsterm
       series(i)%type='ts'
       do j=1,nsterm
         series(i)%days(j)=series(iseries)%days(j)
       end do
       do j=1,nsterm
         series(i)%secs(j)=series(iseries)%secs(j)
       end do
       if(lag.eq.0)then
         do j=1,nsterm
           series(i)%val(j)=series(iseries)%val(j)
         end do
       else if(lag.gt.0)then
         do j=1+lag,nsterm
           series(i)%val(j)=series(iseries)%val(j-lag)
         end do
         do j=1,lag
           series(i)%val(j)=fill
         end do
       else if(lag.lt.0)then
         lag=-lag
         do j=1,nsterm-lag
           series(i)%val(j)=series(iseries)%val(j+lag)
         end do
         do j=nsterm-lag+1,nsterm
           series(i)%val(j)=fill
         end do
       end if

       write(*,580) trim(aname)
       write(recunit,580) trim(aname)
580    format(t5,'Series "',a,'" successfully calculated.')
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

9800   call write_message(leadspace='yes',error='yes')
       call write_message(iunit=recunit,leadspace='yes')
       ifail=1

       return

end subroutine displace


subroutine displace_constant(ifail)

! -- Subroutine DISPLACE moves a time series by a user-supplied number of time increments.

       use tspvar
       use defn
       use inter
       implicit none

       integer, intent(out)   :: ifail

       integer ierr,icontext,iseries,lag,itemp,nsterm,ilags,j,nsecs,ndays, &
       dd,mm,yy,hh,nn,ss,i,ixcon,lagdays,lagsecs
       real fill,rtemp,rconst
       character*10 aname
       character*15 aline
       character*25 aoption,aconstname
       character*25 acontext(MAXCONTEXT)

       ifail=0
       currentblock='SERIES_DISPLACE_CONSTANT'

       write(*,10) trim(currentblock)
       write(recunit,10) trim(currentblock)
10     format(/,' Processing ',a,' block....')

       icontext=0
       iseries=0
       aname=' '
       lag= 1
       fill=-1.1e36
       ixcon=0
       aconstname=' '

! -- The SERIES_DISPLACE_CONSTANT block is first parsed.

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
         if(aoption.eq.'NEW_SERIES_NAME')then
           call read_new_series_name(ierr,aname)
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'SERIES_NAME')then
           call read_series_name(ierr,iseries,'SERIES_NAME')
           if(ierr.ne.0) go to 9800
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
         else if(aoption.eq.'CONSTANT_NAME')then
           call read_file_name(ierr,aconstname)
           call casetrans(aconstname,'lo')
           if(ierr.ne.0) go to 9800         
         else if(aoption.eq.'FILL_VALUE')then
           call get_keyword_value(ierr,2,itemp,fill,'FILL_VALUE')
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'END')then
           go to 200
         else
           call num2char(iline,aline)
           call addquote(infile,astring)
           write(amessage,90) trim(aoption),trim(currentblock),trim(aline),trim(astring)
90         format('unexpected keyword - "',a,'" in ',a,' block at line ',a, &
           ' of file ',a)
           go to 9800
         end if
       end do

! -- The block has been read; now it is checked for correctness.

200    continue
       if(iseries.eq.0)then
         write(amessage,210) trim(currentblock)
210      format('no SERIES_NAME keyword provided in ',a,' block.')
         go to 9800
       end if
       if(aname.eq.' ')then
         write(amessage,230) trim(currentblock)
230      format('no NEW_SERIES_NAME keyword provided in ',a,' block.')
         go to 9800
       end if
       if(icontext.eq.0)then
         write(amessage,220) trim(currentblock)
220      format('no CONTEXT keyword(s) provided in ',a,' block.')
         go to 9800
       end if
       if(aconstname.eq.' ')then
         write(amessage,225) trim(currentblock)
225      format('no CONSTANT_NAME keyword provided in ',a,' block.')
         go to 9800
       end if
       if(fill.lt.-1.0e36)then
         write(amessage,240) trim(currentblock)
240      format('no FILL_VALUE keyword provided in ',a,' block.')
         go to 9800
       end if

!-- try to find the constant value
      do i=1,MAXCONST
        if(const(i)%name.eq.aconstname)then
          rconst = const(i)%value          
          goto 242
        end if
      end do
      write(amessage,241) trim(aconstname)
241          format('no CONSTANT found with name"',a)
      goto 9800          
242   continue
!-- process the real value constant into and int secs
     lagsecs = rconst * 86400.0
     do i=1,MAXSERIES
         if(.not.series(i)%active) go to 515
       end do
       write(amessage,510)
510    format('no more time series available for data storage - increase MAXSERIES and ', &
       'recompile program, or erase a series using an ERASE_SERIES block.')
       go to 9800



     
515  continue
     nsterm=series(iseries)%nterm
     allocate(series(i)%days(nsterm),series(i)%secs(nsterm),  &
     series(i)%val(nsterm),stat=ierr)
     if(ierr.ne.0)then
       write(amessage,550)
550    format('cannot allocate memory for another time series.')
       go to 9800
     end if
     series(i)%active=.true.
     series(i)%name=aname
     series(i)%nterm=nsterm
     series(i)%type='ts'
     do j=1,nsterm
       nsecs = series(iseries)%days(j) * 86400.0 + series(iseries)%secs(j)
       nsecs = nsecs + lagsecs
       ndays = nsecs / 86400.0
       nsecs = nsecs - ndays*86400
       series(i)%days(j)=ndays
       series(i)%secs(j)=nsecs
       series(i)%val(j)=series(iseries)%val(j)
     end do
         
         
         
!       end do
!       do j=1,nsterm
!         series(i)%secs(j)=series(iseries)%secs(j)
!       end do
!       if(lag.eq.0)then
!         do j=1,nsterm
!           series(i)%val(j)=series(iseries)%val(j)
!         end do
!       else if(lag.gt.0)then
!         do j=1+lag,nsterm
!           series(i)%val(j)=series(iseries)%val(j-lag)
!         end do
!         do j=1,lag
!           series(i)%val(j)=fill
!         end do
!       else if(lag.lt.0)then
!         lag=-lag
!         do j=1,nsterm-lag
!           series(i)%val(j)=series(iseries)%val(j+lag)
!         end do
!         do j=nsterm-lag+1,nsterm
!           series(i)%val(j)=fill
!         end do
!       end if

       write(*,580) trim(aname)
       write(recunit,580) trim(aname)
580    format(t5,'Series "',a,'" successfully calculated.')
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

9800   call write_message(leadspace='yes',error='yes')
       call write_message(iunit=recunit,leadspace='yes')
       ifail=1

       return

end subroutine displace_constant



 

subroutine series_block_drawdown(ifail)

! -- Subroutine SERIES_BLOCK_DRAWDOWN extracts a series of seasonal drawdown subseries from
!    an overall series.

       use tspvar
       use defn
       use inter
       implicit none

       integer, intent(out)   :: ifail

       integer ierr,icontext,iseries,iunit,jline,ndate,nsterm,nsdays1, &
       nssecs1,nsdays2,nssecs2,dd,mm,yy,hh,nn,ss,ixcon
       integer iswitch,newterm,ifyesno,iif,idate,i,iterm,j,irf
       real refvar
       character*3 ifaa,rfaa
       character*10 aname
       character*15 aline
       character*25 aoption
       character*200 datefile
       character*25 acontext(MAXCONTEXT)
       
       integer, allocatable :: ndays1(:),ndays2(:),nsecs1(:),nsecs2(:)

       ifail=0
       currentblock='SERIES_BLOCK_DRAWDOWN'

       write(*,10) trim(currentblock)
       write(recunit,10) trim(currentblock)
10     format(/,' Processing ',a,' block....')

       icontext=0
       iseries=0
       aname=' '
       datefile=' '
       ixcon=0
       iunit=0
       ifaa=' '

! -- The SERIES_BLOCK_DRAWDOWN block is first parsed.

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
         if(aoption.eq.'SERIES_NAME')then
           call read_series_name(ierr,iseries,'SERIES_NAME')
           if(ierr.ne.0) go to 9800
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
         else if(aoption.eq.'NEW_SERIES_NAME')then
           call read_new_series_name(ierr,aname)
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'DATE_FILE')then
           call getfile(ierr,cline,datefile,left_word(2),right_word(2))
           if(ierr.ne.0)then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,140) trim(aline),trim(astring)
140          format('cannot read date file name from line ',a,' of file ',a)
             go to 9800
           end if
           call addquote(datefile,astring)
           write(*,145) trim(astring)
           write(recunit,145) trim(astring)
145        format(t5,'DATE_FILE ',a)
         else if(aoption.eq.'INCLUDE_FIRST')then
           call get_yes_no(ierr,ifyesno)
           if(ierr.ne.0) go to 9800
           if(ifyesno.eq.1)then
             ifaa='yes'
           else
             ifaa='no'
           end if
           iif=1
           write(*,146) trim(ifaa)
           write(recunit,146) trim(ifaa)
146        format(t5,'INCLUDE_FIRST ',a)           
         else if (aoption.eq.'REFERENCE_TO_FIRST')then
           call get_yes_no(ierr,ifyesno)
           if(ierr.ne.0) go to 9800
           if(ifyesno.eq.1)then
             rfaa='yes'
           else
             rfaa='no'
           end if
           irf=1
           write(*,147) trim(rfaa)
           write(recunit,147) trim(rfaa)
147        format(t5,'REFERENCE_TO_FIRST ',a)           
         else if(aoption.eq.'END')then
           go to 200
         else
           call num2char(iline,aline)
           call addquote(infile,astring)
           write(amessage,90) trim(aoption),trim(currentblock),trim(aline),trim(astring)
90         format('unexpected keyword - "',a,'" in ',a,' block at line ',a, &
           ' of file ',a)
           go to 9800
         end if
       end do

200    continue

! -- The block has been read; now it is checked for absences.

       if(iseries.eq.0)then
         write(amessage,210) trim(currentblock)
210      format('no SERIES_NAME keyword provided in ',a,' block.')
         go to 9800
       end if
       if(aname.eq.' ')then
         write(amessage,230) trim(currentblock)
230      format('no NEW_SERIES_NAME keyword provided in ',a,' block.')
         go to 9800
       end if
       if(icontext.eq.0)then
         write(amessage,220) trim(currentblock)
220      format('no CONTEXT keyword(s) provided in ',a,' block.')
         go to 9800
       end if
       if(datefile.eq.' ')then
         write(amessage,240) trim(currentblock)
240      format('no DATE_FILE keyword provided in ',a,' block.')
         go to 9800
       end if
       if(ifaa.eq.' ')ifaa='yes'
       if(rfaa.eq.' ')rfaa='no'

! -- The date file is now opened and the number of lines within it read.

       iunit=nextunit()
       call addquote(datefile,astring)
       open(unit=iunit,file=datefile,status='old',iostat=ierr)
       if(ierr.ne.0)then
         write(amessage,300) trim(astring)
300      format('cannot open dates file ',a)
         go to 9800
       end if
       write(6,305) trim(astring)
       write(recunit,305) trim(astring)
305    format(t5,'Reading dates file ',a,'....')
       jline=0
       ndate=0
       do
         jline=jline+1
         read(iunit,'(a)',end=350) cline
         if(cline.eq.' ') cycle
         if(cline(1:1).eq.'#') cycle
         ndate=ndate+1
       end do
350    continue
       if(ndate.eq.0)then
         write(amessage,360) trim(astring)
360      format('no dates found in dates file ',a)
         go to 9800
       end if
       rewind(unit=iunit,iostat=ierr)
       if(ierr.ne.0)then
         write(amessage,370) trim(astring)
370      format('cannot rewind dates file ',a)
         go to 9800
       end if
       
! -- The dates in the dates file are now read and checked.

       allocate(ndays1(ndate),ndays2(ndate),nsecs1(ndate),nsecs2(ndate),stat=ierr)
       if(ierr.ne.0) then
         write(amessage,609)
609      format('cannot allocate sufficient memory to store date intervals.')
         go to 9800
       end if       
600    continue
       jline=0
       ndate=0
       nsterm=series(iseries)%nterm
       nsdays1=series(iseries)%days(1)
       nssecs1=series(iseries)%secs(1)
       nsdays2=series(iseries)%days(nsterm)
       nssecs2=series(iseries)%secs(nsterm)       
       do
         jline=jline+1
         read(iunit,'(a)',end=700) cline
         if(cline.eq.' ') cycle
         if(cline(1:1).eq.'#') cycle
         ndate=ndate+1
         call linesplit(ierr,4)
         if(ierr.ne.0)then
           call num2char(jline,aline)
           write(amessage,610) trim(aline),trim(astring)
610        format('four entries expected on line ',a,' of dates file ',a)
           go to 9800
         end if
         call char2date(ierr,cline(left_word(1):right_word(1)),dd,mm,yy)
         if(ierr.ne.0) go to 9200
         ndays1(ndate)=numdays(1,1,1970,dd,mm,yy)
         call char2time(ierr,cline(left_word(2):right_word(2)),hh,nn,ss,ignore_24=1)
         if(ierr.ne.0) go to 9200
         nsecs1(ndate)=numsecs(0,0,0,hh,nn,ss)
         if(nsecs1(ndate).ge.86400)then
           nsecs1(ndate)=nsecs1(ndate)-86400
           ndays1(ndate)=ndays1(ndate)+1
         end if
         call char2date(ierr,cline(left_word(3):right_word(3)),dd,mm,yy)
         if(ierr.ne.0) go to 9200
         ndays2(ndate)=numdays(1,1,1970,dd,mm,yy)
         call char2time(ierr,cline(left_word(4):right_word(4)),hh,nn,ss,ignore_24=1)
         if(ierr.ne.0) go to 9200
         nsecs2(ndate)=numsecs(0,0,0,hh,nn,ss)
         if(nsecs2(ndate).ge.86400)then
           nsecs2(ndate)=nsecs2(ndate)-86400
           ndays2(ndate)=ndays2(ndate)+1
         end if
         if((ndays1(ndate).gt.ndays2(ndate)).or.         &
           ((ndays1(ndate).eq.ndays2(ndate)).and.(nsecs1(ndate).ge.nsecs2(ndate))))then
           call num2char(jline,aline)
           write(amessage,620) trim(aline),trim(astring)
620        format('first date/time must precede second date/time at line ',a,  &
           ' of file ',a)
           go to 9800
         end if
         if((ndays1(ndate).lt.nsdays1).or.        &
           ((ndays1(ndate).eq.nsdays1).and.(nsecs1(ndate).lt.nssecs1)))then
           call num2char(jline,aline)
           write(amessage,625) trim(aline),trim(astring),trim(series(iseries)%name)
625        format('the first date/time on line ',a,' of file ',a,' predates the ', &
           'commencement of time series "',a,'".')
           go to 9800
         end if
         if((ndays2(ndate).gt.nsdays2).or.         &
           ((ndays2(ndate).eq.nsdays2).and.(nsecs2(ndate).gt.nssecs2)))then
           call num2char(jline,aline)
           write(amessage,626) trim(aline),trim(astring),trim(series(iseries)%name)
626        format('the second date/time on line ',a,' of file ',a,' postdates the ', &
           'end of time series "',a,'".')
           go to 9800
         end if
         if(ndate.gt.1)then
           if((ndays1(ndate).lt.ndays2(ndate-1)).or.                                       &
             ((ndays1(ndate).eq.ndays2(ndate-1)).and.(nsecs1(ndate).le.nsecs2(ndate-1))))then
             call num2char(jline,aline)             
             write(amessage,627) trim(aline),trim(astring)
627          format('the first date/time on line ',a,' of file ',a,' must postdate the ', &
             'last date/time of the previous time interval when the dates file is used by ',  &
             'the SERIES_BLOCK_DRAWDOWN block.')
             go to 9800
           end if
         end if
       end do
700    continue
       close(unit=iunit)
       write(*,730) trim(astring)
       write(recunit,730) trim(astring)
730    format(t5,'File ',a,' read ok.')

! -- The number of terms in the new time series is now evaluated.

       idate=1
       iswitch=0
       newterm=0
       do i=1,nsterm
         if(iswitch.eq.1)then
           if((series(iseries)%days(i).gt.ndays2(idate)).or.                    &
             ((series(iseries)%days(i).eq.ndays2(idate)).and.(series(iseries)%secs(i).gt.nsecs2(idate))))then
               iswitch=0
               idate=idate+1
               if(idate.gt.ndate) go to 750
           else
               newterm=newterm+1
           end if
         end if
         if(iswitch.eq.0)then
           if((series(iseries)%days(i).gt.ndays1(idate)).or.                    &
             ((series(iseries)%days(i).eq.ndays1(idate)).and.(series(iseries)%secs(i).ge.nsecs1(idate))))then                          
             if((series(iseries)%days(i).gt.ndays2(idate)).or.                    &
               ((series(iseries)%days(i).eq.ndays2(idate)).and.(series(iseries)%secs(i).gt.nsecs2(idate))))then
                 idate=idate+1
                 if(idate.gt.ndate) go to 750
             else                          
               iswitch=1
               if(ifaa.eq.'yes') newterm=newterm+1             
             end if
           end if
         end if
       end do
750    continue       
       if(newterm.eq.0)then
         write(amessage,731)
731      format('date intervals in date file are such that there are no terms in resultant ',  &
         'abridged time series within specified date span intervals.')
         go to 9800
       end if
       
! -- Memory is allocated for the new time series.

       do i=1,MAXSERIES
         if(.not.series(i)%active) go to 375
       end do
       write(amessage,372)
372    format('no more time series available for data storage - increase MAXSERIES and ', &
       'recompile program.')
       go to 9800
375    allocate(series(i)%days(newterm),series(i)%secs(newterm),  &
       series(i)%val(newterm),stat=ierr)
       if(ierr.ne.0)then
         write(amessage,560)
560      format('cannot allocate memory for another time series.')
         go to 9800
       end if
       series(i)%active=.true.
       series(i)%name=aname
       series(i)%nterm=newterm
       series(i)%type='ts'
       
! -- The series is now filled.

       idate=1
       iswitch=0
       iterm=0
       do j=1,nsterm
         if(iswitch.eq.1)then
           if((series(iseries)%days(j).gt.ndays2(idate)).or.                    &
             ((series(iseries)%days(j).eq.ndays2(idate)).and.(series(iseries)%secs(j).gt.nsecs2(idate))))then
               iswitch=0
               idate=idate+1
               if(idate.gt.ndate)go to 800
           else
               iterm=iterm+1
               if(rfaa.eq.'yes')then
                 series(i)%val(iterm)=refvar-series(iseries)%val(j)
               else
                 series(i)%val(iterm)=series(iseries)%val(j)
               end if
               series(i)%days(iterm)=series(iseries)%days(j)
               series(i)%secs(iterm)=series(iseries)%secs(j)               
           end if
         end if
         if(iswitch.eq.0)then
           if((series(iseries)%days(j).gt.ndays1(idate)).or.                    &
             ((series(iseries)%days(j).eq.ndays1(idate)).and.(series(iseries)%secs(j).ge.nsecs1(idate))))then
             if((series(iseries)%days(j).gt.ndays2(idate)).or.                    &
               ((series(iseries)%days(j).eq.ndays2(idate)).and.(series(iseries)%secs(j).gt.nsecs2(idate))))then
                 idate=idate+1
                 if(idate.gt.ndate) go to 800
             else             
               iswitch=1
               refvar=series(iseries)%val(j)
               if(ifaa.eq.'yes') then
                 iterm=iterm+1
                 if(rfaa.eq.'yes')then
                   series(i)%val(iterm)=0.0
                 else
                   series(i)%val(iterm)=series(iseries)%val(j)
                 end if
                 series(i)%days(iterm)=series(iseries)%days(j)
                 series(i)%secs(iterm)=series(iseries)%secs(j)               
               end if
             end if
           end if
         end if
       end do
800    continue       

       write(*,440) trim(aname)
       write(recunit,440) trim(aname)
440    format(t5,'Subseries values calculated and stored in series "',a,'".')
       go to 9900

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
9200   continue
       call num2char(jline,aline)
       write(amessage,9210) trim(aline),trim(astring)
9210   format('erroneous date or time at line ',a,' of file ',a)
       go to 9800
9800   call write_message(leadspace='yes',error='yes')
       call write_message(iunit=recunit,leadspace='yes')
       ifail=1
       if(iunit.ne.0)close(unit=iunit,iostat=ierr)

9900   continue
       if(allocated(ndays1))deallocate(ndays1,stat=ierr)
       if(allocated(ndays2))deallocate(ndays2,stat=ierr)       
       if(allocated(nsecs1))deallocate(nsecs1,stat=ierr)              
       if(allocated(nsecs2))deallocate(nsecs2,stat=ierr)                     
       
       return

end subroutine series_block_drawdown




subroutine series_time_average(ifail)

! -- Subroutine SERIES_TIME_AVERAGE averages terms of a series between a set of user-nominated
!    beginning and end time intervals, creating a new series in the process.

       use tspvar
       use defn
       use inter
       implicit none

       integer, intent(out)   :: ifail

       integer ierr,icontext,iseries,iunit,jline,ndate,nsterm,nsdays1, &
       nssecs1,nsdays2,nssecs2,dd,mm,yy,hh,nn,ss,ixcon
       integer iswitch,newterm,idate,i,iterm,j
       integer isamptime,icount,ddays,ssecs,iflag
       double precision sum
       character*10 samptime
       character*10 aname
       character*15 aline
       character*25 aoption
       character*200 datefile
       character*25 acontext(MAXCONTEXT)
       
       integer, allocatable :: ndays1(:),ndays2(:),nsecs1(:),nsecs2(:)

       ifail=0
       currentblock='SERIES_TIME_AVERAGE'

       write(*,10) trim(currentblock)
       write(recunit,10) trim(currentblock)
10     format(/,' Processing ',a,' block....')

       icontext=0
       iseries=0
       aname=' '
       datefile=' '
       ixcon=0
       iunit=0
       samptime=' '

! -- The SERIES_TIME_AVERAGE block is first parsed.

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
         if(aoption.eq.'SERIES_NAME')then
           call read_series_name(ierr,iseries,'SERIES_NAME')
           if(ierr.ne.0) go to 9800
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
         else if(aoption.eq.'NEW_SERIES_NAME')then
           call read_new_series_name(ierr,aname)
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'DATE_FILE')then
           call getfile(ierr,cline,datefile,left_word(2),right_word(2))
           if(ierr.ne.0)then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,140) trim(aline),trim(astring)
140          format('cannot read date file name from line ',a,' of file ',a)
             go to 9800
           end if
           call addquote(datefile,astring)
           write(*,145) trim(astring)
           write(recunit,145) trim(astring)
145        format(t5,'DATE_FILE ',a)
         else if(aoption.eq.'SAMPLE_TIME')then
           call getfile(ierr,cline,samptime,left_word(2),right_word(2))
           if(ierr.ne.0)then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,146) trim(aline),trim(astring)
146          format('cannot read sample time from line ',a,' of file ',a)
             go to 9800
           end if                                        
           call casetrans(samptime,'lo')
           if(samptime.eq.'start')then
             isamptime=-1
           else if(samptime.eq.'finish')then           
             isamptime=1
           else if(samptime.eq.'middle')then
             isamptime=0
           else
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,147) trim(aline),trim(astring)
147          format('sample time must be "start", "finish" or "middle" ', &
             'at line ',a,' of file ',a)
             go to 9800
           end if             
           write(*,148) trim(samptime)
           write(recunit,148) trim(samptime)
148        format(t5,'SAMPLE_TIME ',a)
         else if(aoption.eq.'END')then
           go to 200
         else
           call num2char(iline,aline)
           call addquote(infile,astring)
           write(amessage,90) trim(aoption),trim(currentblock),trim(aline),trim(astring)
90         format('unexpected keyword - "',a,'" in ',a,' block at line ',a, &
           ' of file ',a)
           go to 9800
         end if
       end do

200    continue

! -- The block has been read; now it is checked for absences.

       if(iseries.eq.0)then
         write(amessage,210) trim(currentblock)
210      format('no SERIES_NAME keyword provided in ',a,' block.')
         go to 9800
       end if
       if(aname.eq.' ')then
         write(amessage,230) trim(currentblock)
230      format('no NEW_SERIES_NAME keyword provided in ',a,' block.')
         go to 9800
       end if
       if(icontext.eq.0)then
         write(amessage,220) trim(currentblock)
220      format('no CONTEXT keyword(s) provided in ',a,' block.')
         go to 9800
       end if
       if(datefile.eq.' ')then
         write(amessage,240) trim(currentblock)
240      format('no DATE_FILE keyword provided in ',a,' block.')
         go to 9800
       end if
       if(samptime.eq.' ')then
         write(amessage,241) trim(currentblock)
241      format('no SAMPLE_TIME keyword provided in ',a,' block.')
         go to 9800
       end if

! -- The date file is now opened and the number of lines within it read.

       iunit=nextunit()
       call addquote(datefile,astring)
       open(unit=iunit,file=datefile,status='old',iostat=ierr)
       if(ierr.ne.0)then
         write(amessage,300) trim(astring)
300      format('cannot open dates file ',a)
         go to 9800
       end if
       write(6,305) trim(astring)
       write(recunit,305) trim(astring)
305    format(t5,'Reading dates file ',a,'....')
       jline=0
       ndate=0
       do
         jline=jline+1
         read(iunit,'(a)',end=350) cline
         if(cline.eq.' ') cycle
         if(cline(1:1).eq.'#') cycle
         ndate=ndate+1
       end do
350    continue
       if(ndate.eq.0)then
         write(amessage,360) trim(astring)
360      format('no dates found in dates file ',a)
         go to 9800
       end if
       rewind(unit=iunit,iostat=ierr)
       if(ierr.ne.0)then
         write(amessage,370) trim(astring)
370      format('cannot rewind dates file ',a)
         go to 9800
       end if
       
! -- The dates in the dates file are now read and checked.

       allocate(ndays1(ndate),ndays2(ndate),nsecs1(ndate),nsecs2(ndate),stat=ierr)
       if(ierr.ne.0) then
         write(amessage,609)
609      format('cannot allocate sufficient memory to store date intervals.')
         go to 9800
       end if       
600    continue
       jline=0
       ndate=0
       nsterm=series(iseries)%nterm
       nsdays1=series(iseries)%days(1)
       nssecs1=series(iseries)%secs(1)
       nsdays2=series(iseries)%days(nsterm)
       nssecs2=series(iseries)%secs(nsterm)       
       do
         jline=jline+1
         read(iunit,'(a)',end=700) cline
         if(cline.eq.' ') cycle
         if(cline(1:1).eq.'#') cycle
         ndate=ndate+1
         call linesplit(ierr,4)
         if(ierr.ne.0)then
           call num2char(jline,aline)
           write(amessage,610) trim(aline),trim(astring)
610        format('four entries expected on line ',a,' of dates file ',a)
           go to 9800
         end if
         call char2date(ierr,cline(left_word(1):right_word(1)),dd,mm,yy)
         if(ierr.ne.0) go to 9200
         ndays1(ndate)=numdays(1,1,1970,dd,mm,yy)
         call char2time(ierr,cline(left_word(2):right_word(2)),hh,nn,ss,ignore_24=1)
         if(ierr.ne.0) go to 9200
         nsecs1(ndate)=numsecs(0,0,0,hh,nn,ss)
         if(nsecs1(ndate).ge.86400)then
           nsecs1(ndate)=nsecs1(ndate)-86400
           ndays1(ndate)=ndays1(ndate)+1
         end if
         call char2date(ierr,cline(left_word(3):right_word(3)),dd,mm,yy)
         if(ierr.ne.0) go to 9200
         ndays2(ndate)=numdays(1,1,1970,dd,mm,yy)
         call char2time(ierr,cline(left_word(4):right_word(4)),hh,nn,ss,ignore_24=1)
         if(ierr.ne.0) go to 9200
         nsecs2(ndate)=numsecs(0,0,0,hh,nn,ss)
         if(nsecs2(ndate).ge.86400)then
           nsecs2(ndate)=nsecs2(ndate)-86400
           ndays2(ndate)=ndays2(ndate)+1
         end if
         if((ndays1(ndate).gt.ndays2(ndate)).or.         &
           ((ndays1(ndate).eq.ndays2(ndate)).and.(nsecs1(ndate).ge.nsecs2(ndate))))then
           call num2char(jline,aline)
           write(amessage,620) trim(aline),trim(astring)
620        format('first date/time must precede second date/time at line ',a,  &
           ' of file ',a)
           go to 9800
         end if
         if((ndays1(ndate).lt.nsdays1).or.        &
           ((ndays1(ndate).eq.nsdays1).and.(nsecs1(ndate).lt.nssecs1)))then
           call num2char(jline,aline)
           write(amessage,625) trim(aline),trim(astring),trim(series(iseries)%name)
625        format('the first date/time on line ',a,' of file ',a,' predates the ', &
           'commencement of time series "',a,'".')
           go to 9800
         end if
         if((ndays2(ndate).gt.nsdays2).or.         &
           ((ndays2(ndate).eq.nsdays2).and.(nsecs2(ndate).gt.nssecs2)))then
           call num2char(jline,aline)
           write(amessage,626) trim(aline),trim(astring),trim(series(iseries)%name)
626        format('the second date/time on line ',a,' of file ',a,' postdates the ', &
           'end of time series "',a,'".')
           go to 9800
         end if
         if(ndate.gt.1)then
           if((ndays1(ndate).lt.ndays2(ndate-1)).or.                                       &
             ((ndays1(ndate).eq.ndays2(ndate-1)).and.(nsecs1(ndate).le.nsecs2(ndate-1))))then
             call num2char(jline,aline)             
             write(amessage,627) trim(aline),trim(astring)
627          format('the first date/time on line ',a,' of file ',a,' must postdate the ', &
             'last date/time of the previous time interval when the dates file is used by ',  &
             'the SERIES_TIME_AVERAGE block.')
             go to 9800
           end if
         end if
       end do
700    continue
       close(unit=iunit)
       write(*,730) trim(astring)
       write(recunit,730) trim(astring)
730    format(t5,'File ',a,' read ok.')

! -- The number of terms in the new time series is now evaluated.

       idate=1
       iswitch=0
       newterm=0
       do i=1,nsterm
         if(iswitch.eq.1)then
           if((series(iseries)%days(i).gt.ndays2(idate)).or.                    &
             ((series(iseries)%days(i).eq.ndays2(idate)).and.(series(iseries)%secs(i).gt.nsecs2(idate))))then
               iswitch=0
               idate=idate+1
               if(idate.gt.ndate) go to 750
           else
               continue
           end if
         end if
         if(iswitch.eq.0)then
           if((series(iseries)%days(i).gt.ndays1(idate)).or.                    &
             ((series(iseries)%days(i).eq.ndays1(idate)).and.(series(iseries)%secs(i).ge.nsecs1(idate))))then             
             if((series(iseries)%days(i).gt.ndays2(idate)).or.                    &
               ((series(iseries)%days(i).eq.ndays2(idate)).and.(series(iseries)%secs(i).gt.nsecs2(idate))))then
                 idate=idate+1
                 if(idate.gt.ndate) go to 750
             else
               iswitch=1
               newterm=newterm+1
             end if
           end if
         end if
       end do
750    continue       
       if(newterm.eq.0)then
         write(amessage,731)
731      format('date intervals in date file are such that there are no terms in new time series.')
         go to 9800
       end if
       
! -- Memory is allocated for the new time series.

       do i=1,MAXSERIES
         if(.not.series(i)%active) go to 375
       end do
       do i=1,MAXSERIES
           write(recunit,*) series(i)%name
       end do    
       write(amessage,372)
372    format('no more time series available for data storage - increase MAXSERIES and ', &
       'recompile program.')
       go to 9800
375    allocate(series(i)%days(newterm),series(i)%secs(newterm),  &
       series(i)%val(newterm),stat=ierr)
       if(ierr.ne.0)then
         write(amessage,560)
560      format('cannot allocate memory for another time series.')
         go to 9800
       end if
       series(i)%active=.true.
       series(i)%name=aname
       series(i)%nterm=newterm
       series(i)%type='ts'
       
! -- The series is now filled.

       idate=1
       iswitch=0
       iterm=0
       icount=0
       sum=0.0d0
       do j=1,nsterm
         if(iswitch.eq.1)then
           if((series(iseries)%days(j).gt.ndays2(idate)).or.                    &
             ((series(iseries)%days(j).eq.ndays2(idate)).and.(series(iseries)%secs(j).gt.nsecs2(idate))))then
               iswitch=0               
               series(i)%val(iterm)=sum/icount
               sum=0.0d0                              
               icount=0
               if(isamptime.eq.1)then
                 series(i)%days(iterm)=ndays2(idate)
                 series(i)%secs(iterm)=nsecs2(idate)
               else if(isamptime.eq.-1)then
                 series(i)%days(iterm)=ndays1(idate)
                 series(i)%secs(iterm)=nsecs1(idate)                              
               else if(isamptime.eq.0)then
                 ddays=ndays2(idate)-ndays1(idate)
                 iflag=0
                 if((ddays/2)*2.ne.ddays)then
                   iflag=1
                   ddays=ddays-1
                 end if
                 ddays=ddays/2
                 ssecs=nsecs2(idate)-nsecs1(idate)
                 ssecs=ssecs/2
                 if(iflag.eq.1)ssecs=ssecs+86400/2
                 ddays=ddays+ndays1(idate)
                 ssecs=ssecs+nsecs1(idate)                 
                 if(ssecs.ge.86400)then
                   ssecs=ssecs-86400
                   ddays=ddays+1
                 else if(ssecs.lt.0)then
                   ssecs=ssecs+86400
                   ddays=ddays-1
                 end if
                 series(i)%secs(iterm)=ssecs
		 series(i)%days(iterm)=ddays
               end if
               idate=idate+1
               if(idate.gt.ndate)go to 800
           else
               icount=icount+1
               sum=sum+series(iseries)%val(j)
           end if
         end if
         if(iswitch.eq.0)then
           if((series(iseries)%days(j).gt.ndays1(idate)).or.                    &
             ((series(iseries)%days(j).eq.ndays1(idate)).and.(series(iseries)%secs(j).ge.nsecs1(idate))))then             
             if((series(iseries)%days(j).gt.ndays2(idate)).or.                    &
               ((series(iseries)%days(j).eq.ndays2(idate)).and.(series(iseries)%secs(j).gt.nsecs2(idate))))then
                 idate=idate+1
                 if(idate.gt.ndate) then
                     go to 800
                 end if                     
             else
               iswitch=1
               iterm=iterm+1
               icount=1
               sum=series(iseries)%val(j)
             end if
           end if
         end if
       end do
800    continue       

       write(*,440) trim(aname)
       write(recunit,440) trim(aname)
440    format(t5,'Averages calculated and stored in series "',a,'".')
       go to 9900

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
9200   continue
       call num2char(jline,aline)
       write(amessage,9210) trim(aline),trim(astring)
9210   format('erroneous date or time at line ',a,' of file ',a)
       go to 9800
9800   call write_message(leadspace='yes',error='yes')
       call write_message(iunit=recunit,leadspace='yes')
       ifail=1
       if(iunit.ne.0)close(unit=iunit,iostat=ierr)

9900   continue
       if(allocated(ndays1))deallocate(ndays1,stat=ierr)
       if(allocated(ndays2))deallocate(ndays2,stat=ierr)       
       if(allocated(nsecs1))deallocate(nsecs1,stat=ierr)              
       if(allocated(nsecs2))deallocate(nsecs2,stat=ierr)                     
       
       return

end subroutine series_time_average

!     Last change:  JD    4 Sep 2001    3:59 pm
subroutine equation(ifail)

! -- Subroutine EQUATION evaluates a relationship between time series.

       use tspvar
       use defn
       use inter
       implicit none

       integer, intent(out)   :: ifail

       integer icontext,ierr,ieqn,ncl,nterm,i,nser,isnum,j,iser,k,nsterm,iterm,nnterm, &
               dd,mm,yy,nn,ixcon,ddx,mmx,yyx,hhx,nnx,ssx,idx,nex,sex,lnx,lnxx,ixcount
       integer serno(maxeqnser)
       integer iinplace
       real rtime
       double precision dval,dtempx
       character*1   aa
       character*10  aname
       character*15  aline
       character*25  aoption,adate_atime,ainplace
       character*300 eqntext
       character*25  acontext(MAXCONTEXT)

       ifail=0
       currentblock='SERIES_EQUATION'

       write(*,10) trim(currentblock)
       write(recunit,10)trim(currentblock)
10     format(/,' Processing ',a,' block....')

       icontext=0
       aname=' '
       ieqn=0
       ixcon=0
       iinplace = 0
! -- The SERIES_EQUATION block is first parsed.

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
         if(aoption.eq.'NEW_SERIES_NAME')then
           call read_new_series_name(ierr,aname)
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'IN_PLACE') then
           ainplace = aname
           iinplace = 1
            write(*,42) 
            write(recunit,42) 
 42         format(t5,'EQUATION OPERATION IN PLACE USING FIRST SERIES IN EQUATION ')
        
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
           go to 200
         else if(aoption.eq.'EQUATION')then
           ieqn=ieqn+1
           if(ieqn.gt.1)then
             write(amessage,30) trim(currentblock)
30           format('only one EQUATION keyword can appear in a ',a,' block.')
             go to 9800
           
           end if
           aa=cline(left_word(2):left_word(2))
           if((aa.eq.'"').or.(aa.eq.'''')) then
             cline(left_word(2):left_word(2))=' '
             ncl=len_trim(cline)
             aa=cline(ncl:ncl)
             if((aa.ne.'"').and.(aa.ne.''''))go to 9200
             cline(ncl:ncl)=' '
             eqntext=cline(left_word(2)+1:)
             eqntext=adjustl(eqntext)
           else
             eqntext=cline(left_word(2):)
!             ncl=len_trim(eqntext)
!             aa=eqntext(ncl:ncl)
!             if((aa.eq.'''').or.(aa.eq.'"')) go to 9200
           end if
           call casetrans(eqntext,'lo')
           write(*,40) trim(eqntext)
           write(recunit,40) trim(eqntext)
40         format(t5,'EQUATION "',a,'"')
         else
           call num2char(iline,aline)
           call addquote(infile,astring)
           write(amessage,90) trim(aoption),trim(currentblock),trim(aline),trim(astring)
90         format('unexpected keyword - "',a,'" in ',a,' block at line ',a, &
           ' of file ',a)
           go to 9800
         end if
       end do
200    continue

! The data supplied in the block is now checked for absences.

       if(aname.eq.' '.and.iinplace.eq.0)then
         write(amessage,230) trim(currentblock)
230      format('no NEW_SERIES_NAME keyword provided in ',a,' block.')
         go to 9800
       end if
       if(icontext.eq.0)then
         write(amessage,220) trim(currentblock)
220      format('no CONTEXT keyword(s) provided in ',a,' block.')
         go to 9800
       end if
       if(ieqn.eq.0)then
         write(amessage,240) trim(currentblock)
240      format('no EQUATION keyword provided in ',a,' block.')
         go to 9800
       end if

! -- The equation is now analysed for correctness. First it is parsed.
! -- But first the @_days_"dd/mm/yy_hh/nn/ss" function is given special treatment.

       lnxx=len_trim(eqntext)
       idx=1
241    continue
       lnx=index(eqntext(idx:),'@_days_ ')
       if(lnx.ne.0) go to 9500
       lnx=index(eqntext(idx:),'@_days_')
       if(lnx.eq.0) go to 249
       idx=idx+lnx-1
       idx=idx+7
       if(eqntext(idx:idx+9).eq.'start_year') then
         go to 241
       else if((eqntext(idx:idx).eq.'"').or.(eqntext(idx:idx).eq.''''))then
         ixcount=0
243      idx=idx+1
         if(idx.gt.lnxx) go to 9500
         if((eqntext(idx:idx).eq.'"').or.(eqntext(idx:idx).eq.'''')) then
           if(ixcount.ne.2) go to 9500
           go to 241
         end if
         if(eqntext(idx:idx).eq.'/')then
           ixcount=ixcount+1
           if(ixcount.gt.2)go to 9500
           eqntext(idx:idx)='~'
         end if
         go to 243
       else
         go to 9500
       end if

249    continue
       call parse(ierr,maxterm,nterm,noper,eqntext,aterm,   &
       bterm,nfunct,funct,operat,rterm,0)
       if(ierr.ne.0) go to 9800
       call series_sub(ierr,NTERM,0)
       if(ierr.ne.0) go to 9800

! -- The series cited in the equation are now collected.

       nser=0
       do i=1,nterm
         if(aterm(i)(1:3).eq.'$~$')then
           call char2num(ierr,aterm(i)(4:),isnum)
           if(ierr.ne.0)then
             write(amessage,250)
250          format('internal error - contact programmer.')
             go to 9800
           end if
           if(nser.eq.0)then
             nser=nser+1
             serno(nser)=isnum
           else
             do j=1,nser-1
               if(serno(j).eq.isnum) go to 270
             end do
             nser=nser+1
             if(nser.gt.maxeqnser)then
               call num2char(maxeqnser,aline)
               write(amessage,260) trim(aline)
260            format('maximum of ',a,' different series names can be cited in a ', &
               'series equation.')
               go to 9800
             end if
             serno(nser)=isnum
270          continue
           end if
         end if
       end do
       if(nser.eq.0)then
         write(amessage,280)
280      format('at least one series name should be cited in a series equation.')
         go to 9800
       end if

 ! -- Now they are checked for time consitency.

       if(nser.eq.1) go to 350
       do iser =2,nser
         i=serno(iser)
         j=serno(iser-1)
         if(series(i)%nterm.ne.series(j)%nterm) go to 9300
         do k=1,series(i)%nterm
           if(series(i)%days(k).ne.(series(j)%days(k))) go to 9300
           if(series(i)%secs(k).ne.(series(j)%secs(k))) go to 9300
         end do
       end do

350    continue

! -- Space is allocated for the new series.

       do iser=1,MAXSERIES
         if(.not.series(iser)%active) go to 370
       end do
       write(amessage,360)
360    format('no more time series available for data storage - increase MAXSERIES and ', &
       'recompile program.')
       go to 9800

370    continue
       k=serno(nser)
       nsterm=series(k)%nterm
       allocate(series(iser)%days(nsterm),series(iser)%secs(nsterm),  &
       series(iser)%val(nsterm),stat=ierr)
       if(ierr.ne.0)then
         write(amessage,380)
380      format('cannot allocate memory for another time series.')
         go to 9800
       end if
       series(iser)%active=.true.
       series(iser)%name=aname
       series(iser)%nterm=nsterm
       series(iser)%type='ts'
       do j=1,nsterm
         series(iser)%days(j)=series(k)%days(j)
       end do
       do j=1,nsterm
         series(iser)%secs(j)=series(k)%secs(j)
       end do

! -- Numbers are identified and copied to the rterm array.

       do iterm=1,nterm
         aa=aterm(iterm)(1:1)
         if((aa.ne.'(').and.(aa.ne.')').and.(aa.ne.'+').and.(aa.ne.'-').and.   &
            (aa.ne.'*').and.(aa.ne.'/').and.(aa.ne.'^').and.                   &
            (aterm(iterm)(1:6).ne.'~#str_').and.                               &
            (aterm(iterm)(1:6).ne.'~#fin_').and.                               &
            (aterm(iterm)(1:3).ne.'$~$').and.                                  &
            (aterm(iterm)(1:2).ne.'@_'))then
              call char2num(ierr,aterm(iterm),rterm(iterm))
              if(ierr.ne.0)then
                write(amessage,395) trim(aterm(iterm))
395             format('the term "',a,'" in the series equation cannot be interpreted ', &
                'as a number, function or operator.')
                go to 9800
              end if
              aterm(iterm)='~!~'
         end if
       end do

! -- We now check for intrinsic functions.

       do iterm=1,nterm
         if(aterm(iterm)(1:2).eq.'@_')then
           if(aterm(iterm)(3:).eq.'days_start_year')then
             aterm(iterm)(3:)='1'
           else if(aterm(iterm)(3:).eq.'abs_val')then
             write(amessage,409) trim(aterm(iterm))
409          format('instrinsic function "',a,'" cannot be used in a series equation.')
             go to 9800
           else if(aterm(iterm)(3:7).eq.'days_')then
             lnx=len(aterm(iterm))
             do idx=1,lnx
               if(aterm(iterm)(idx:idx).eq.'~')aterm(iterm)(idx:idx)='/'
             end do
             call getfile(ierr,aterm(iterm),adate_atime,8,lnx)
             if(ierr.ne.0) go to 9400
             idx=index(adate_atime,'_')
             if(idx.eq.0) go to 9400
             call char2date(ierr,adate_atime(1:idx-1),ddx,mmx,yyx)
             if(ierr.ne.0) go to 9400
             call char2time(ierr,adate_atime(idx+1:),hhx,nnx,ssx,ignore_24=1)
             if(ierr.ne.0) go to 9400
             nex=numdays(1,1,1970,ddx,mmx,yyx)
             sex=numsecs(0,0,0,hhx,nnx,ssx)
             dtempx=dble(nex)+dble(sex)/86400.0d0
             aterm(iterm)(3:4)='3_'
             write(aterm(iterm)(5:),'(1pd22.14)') dtempx
           else
             go to 9400
           end if
         endif
       end do

! -- The series equation is now evaluated for each term in the series.

       nnterm=nterm
       do iterm=1,nterm
         cterm(iterm)=aterm(iterm)
       end do
       do iterm=1,nterm
         qterm(iterm)=rterm(iterm)
       end do
       do j=1,nsterm
         nterm=nnterm
         do iterm=1,nterm
           aterm(iterm)=cterm(iterm)
         end do
         do iterm=1,nterm
           rterm(iterm)=qterm(iterm)
         end do

! -- First the series numbers in the equation terms are replaced by series values.

         do iterm =1,nterm
           if(aterm(iterm)(1:3).eq.'$~$') then
             call char2num(ierr,aterm(iterm)(4:),isnum)
             rterm(iterm)=series(isnum)%val(j)
             aterm(iterm)='~!~'
!             write(aterm(iterm),'(e25.14e3)')series(isnum)%val(j)
           end if
         end do

! -- Any instinsic function evaluations are carried out.

         do iterm =1,nterm
           if(aterm(iterm)(1:3).eq.'@_1') then
             call newdate(series(isnum)%days(j),1,1,1970,dd,mm,yy)
             nn=numdays(1,1,yy,dd,mm,yy)
             rtime=float(nn)+float(series(isnum)%secs(j))/86400.0
             rterm(iterm)=rtime
             aterm(iterm)='~!~'
           else if(aterm(iterm)(1:3).eq.'@_3')then
             call char2num(ierr,aterm(iterm)(5:),dtempx)
             rterm(iterm)=dble(series(isnum)%days(j))+     &
                          dble(series(isnum)%secs(j))/86400.0d0-dtempx
             aterm(iterm)='~!~'
           end if
         end do

         call EVALUATE(ierr,MAXTERM,NTERM,NOPER,NFUNCT,ATERM,BTERM,   &
         OPERAT,FUNCT,IORDER,DVAL,rterm)
         if(ierr.ne.0) go to 9800
         if(iinplace.eq.0) then
            series(iser)%val(j)=dval
          else
            series(serno(1))%val(j)=dval
          endif  
       end do
       if (iinplace.eq.1)then
           deallocate(series(iser)%days,series(iser)%secs,series(iser)%val,stat=ierr)       
           nullify(series(iser)%days,series(iser)%secs,series(iser)%val)
           series(iser)%active=.false.
           series(iser)%nterm=0
           series(iser)%type=' '
           aname = series(1)%NAME
       end if
       
       
       write(*,580) trim(aname)
       write(recunit,580) trim(aname)
580    format(t5,'Series "',a,'" successfully calculated using series equation.')

!       close(unit=99)                !debug
       return


9000   call num2char(iline,aline)
       call addquote(infile,astring)
       write(amessage,9010) trim(aline),trim(astring)
9010   format('cannot read line ',a,' of TSPROC input file ',a)
       go to 9800
9100   continue
       call addquote(infile,astring)
       write(amessage,9110) trim(astring),trim(currentblock)
9110   format('unexpected end encountered to TSPROC input file ',a,  &
       ' while reading ',a,' block.')
       go to 9800
9200   call num2char(iline,aline)
       call addquote(infile,astring)
       write(amessage,9210) trim(aline),trim(astring)
9210   format('cannot read equation from line ',a,' of TSPROC input file ',a)
       go to 9800
9300   write(amessage,9310) trim(series(i)%name), trim(series(j)%name)
9310   format('all series cited in the series equation must have an identical time-base ', &
       '(ie. the same number of terms, with all dates and times coincident). Series ', &
       '"',a,'" and "',a,'" have different time bases.')
       go to 9800
9400   write(amessage,9410) trim(aterm(iterm))
9410   format('illegal intrinsic function "',a,'" in series equation.')
       go to 9800
9500   write(amessage,9510)
9510   format('illegal "@_days_" function in series equation.')
       go to 9800

9800   call write_message(leadspace='yes',error='yes')
       call write_message(iunit=recunit,leadspace='yes')
       ifail=1

       return

end subroutine equation




      SUBROUTINE PARSE(IFAIL,MAXTERM,NTERM,NOPER,eqntext,ATERM,   &
      BTERM,NFUNCT,FUNCT,OPERAT,rterm,itype)

! -- Subroutine PARSE breaks an expression up into elements.

       use defn
       use inter
       implicit none

      INTEGER IFAIL,MAXTERM,NTERM,NFUNCT,NOPER,ierr,itype
      INTEGER ICOUNT,NB,I,JFAIL,ITERM,J,IIFUN,NEG
      double precision rterm(maxterm)
      CHARACTER*30 ATEMP
      CHARACTER*1 AA
      CHARACTER*6 AATERM
      CHARACTER*10 BB
      CHARACTER*(*) ATERM(MAXTERM),BTERM(MAXTERM)
      CHARACTER*(*) eqntext
      CHARACTER*(*) FUNCT(NFUNCT)
      CHARACTER*(*) OPERAT(NOPER)

      IFAIL=0
      NTERM=0

! -- First a check is made to see if brackets are balanced.

      IF(eqntext.EQ.' ')GO TO 9000

      ICOUNT=0
      NB=len_trim(eqntext)
      DO 3 I=1,NB
        IF(eqntext(I:I).EQ.'(')THEN
          ICOUNT=ICOUNT+1
        ELSE IF(eqntext(I:I).EQ.')')THEN
          ICOUNT=ICOUNT-1
        END IF
3     CONTINUE
      IF(ICOUNT.NE.0)THEN
        if(itype.eq.0)then
          WRITE(amessage,4)
4         FORMAT('unbalanced parentheses in series equation.')
        else if(itype.eq.1)then
          write(amessage,2)
2         format('unbalanced parentheses in weights equation.')
        end if
        GO TO 9020
      END IF

      IF(INDEX(eqntext,'=').NE.0)GO TO 9000
5     CONTINUE
      CALL GETNEXT(JFAIL,NOPER,eqntext,ATEMP,OPERAT)
      IF(JFAIL.LT.0)THEN
        GO TO 50
      ELSE
        NTERM=NTERM+1
        IF(NTERM.GT.MAXTERM)GO TO 9100
        ATERM(NTERM)=ATEMP
        GO TO 5
      END IF
50    CONTINUE

! -- Functions are now dealt with.

      IIFUN=0
      IF(NTERM.LE.2) GO TO 400
      DO 200 ITERM=2,NTERM
        IF(ATERM(ITERM)(1:1).EQ.'(')THEN
          AA=ATERM(ITERM-1)(1:1)
          IF((AA.EQ.'+').OR.(AA.EQ.'-').OR.(AA.EQ.'*').OR.        &
             (AA.EQ.'/').OR.(AA.EQ.'^').OR.(AA.EQ.'(')) GO TO 200
          AATERM=ATERM(ITERM-1)(1:6)
          DO 70 J=1,NFUNCT
            IF(AATERM.EQ.FUNCT(J)) GO TO 80
70        CONTINUE
          if(itype.eq.0)then
            WRITE(amessage,75) trim(ATERM(ITERM-1))
75          FORMAT('illegal function name  "',A,'" in series equation.')
          else
            WRITE(amessage,76) trim(ATERM(ITERM-1))
76          FORMAT('illegal function name  "',A,'" in weights equation.')
          end if
          GO TO 9020
80        continue
          call num2char(j,bb)
!          CALL WRTINT(BB,J)
          ATERM(ITERM-1)='~#str_'//trim(BB)
          IIFUN=IIFUN+1
        END IF
200   CONTINUE
      IF(IIFUN.EQ.0) GO TO 400

      DO 300 ITERM=1,NTERM
        IF(ATERM(ITERM)(1:6).EQ.'~#str_') THEN
          ATERM(ITERM+1)(1:1)=CHAR(220)
          ICOUNT=1
          DO 280 J=ITERM+1,NTERM
            IF(ATERM(J)(1:1).EQ.'(')THEN
              ICOUNT=ICOUNT+1
            ELSE IF(ATERM(J)(1:1).EQ.')')THEN
              ICOUNT=ICOUNT-1
              IF(ICOUNT.EQ.0)THEN
                ATERM(J)='~#fin_'
                GO TO 300
              END IF
            END IF
280       CONTINUE
        END IF
300   CONTINUE

      CALL COMPRESS(MAXTERM,NTERM,ATERM,BTERM,rterm)

400   CONTINUE

! -- If the last item is an operator then the expression is invalid.



      AA=ATERM(NTERM)(1:1)
      IF((AA.EQ.'+').OR.(AA.EQ.'-').OR.(AA.EQ.'/').OR.(AA.EQ.'*').OR.   &
      (AA.EQ.'^')) GO TO 9000





! -- The "-" and the "+" signs are expanded as a function if appropriate.

490   CONTINUE
      DO 500 ITERM=1,NTERM
        IF((ATERM(ITERM)(1:1).EQ.'-').OR.            &
           (ATERM(ITERM)(1:1).EQ.'+'))THEN
          IF(ATERM(ITERM)(1:1).EQ.'+')THEN
            NEG=0
          ELSE
            NEG=1
          END IF
          IF(ITERM.EQ.1) THEN
            IF(NTERM.EQ.MAXTERM) GO TO 9100
            CALL EXPNEG(ierr,MAXTERM,NTERM,ITERM,ATERM,NEG)
            IF(ierr.NE.0) GO TO 9000
            GO TO 490
          ELSE IF(ATERM(ITERM-1)(1:6).EQ.'~#str_')THEN
            IF(NTERM.EQ.MAXTERM) GO TO 9100
            CALL EXPNEG(ierr,MAXTERM,NTERM,ITERM,ATERM,NEG)
            IF(ierr.NE.0) GO TO 9000
            GO TO 490
          ELSE
            AA=ATERM(ITERM-1)(1:1)
            IF((AA.EQ.'(').OR.(AA.EQ.'+').OR.(AA.EQ.'-').OR.  &
               (AA.EQ.'*').OR.(AA.EQ.'/').OR.(AA.EQ.'^'))THEN
               IF(NTERM.EQ.MAXTERM) GO TO 9100
               CALL EXPNEG(ierr,MAXTERM,NTERM,ITERM,ATERM,NEG)
               IF(ierr.NE.0) GO TO 9000
               GO TO 490
            END IF
          END IF
        END IF
500   CONTINUE

      RETURN

9000  continue
      if(itype.eq.0)then
        WRITE(amessage,9010)
9010    FORMAT('illegal series equation.')
      else if(itype.eq.1)then
        write(amessage,9011)
9011    format('illegal weights equation.')
      end if
      go to 9020
9100  continue
      if(itype.eq.0)then
        WRITE(amessage,9110)
9110    FORMAT('too many terms in series equation.')
      else if(itype.eq.1)then
        write(amessage,9111)
9111    format('too many terms in weights equation.')
      end if
      GO TO 9020

9020  IFAIL=1

      RETURN
      END


      SUBROUTINE EXPNEG(IFAIL,MAXTERM,NTERM,ITERM,ATERM,NEG)

! -- Subroutine EXPNEG expands a "-" sign into a function.

      INTEGER MAXTERM,NTERM,ITERM,IFAIL,ICOUNT,JTERM,I,NEG
      CHARACTER(*) ATERM(MAXTERM)

      IFAIL=0
      IF(NEG.EQ.1)THEN
        ATERM(ITERM)='~#str_15'
      ELSE
        ATERM(ITERM)='~#str_16'
      END IF
      ICOUNT=0
      DO 100 JTERM=ITERM+1,NTERM
        IF((ATERM(JTERM)(1:1).EQ.'-').OR.             &
           (ATERM(JTERM)(1:1).EQ.'+'))GO TO 100
        IF(ATERM(JTERM)(1:1).EQ.'(')THEN
          ICOUNT=ICOUNT+1
        ELSE IF(ATERM(JTERM)(1:1).EQ.')')THEN
          ICOUNT=ICOUNT-1
        ELSE IF(ATERM(JTERM)(1:6).EQ.'~#str_')THEN
          ICOUNT=ICOUNT+1
        ELSE IF(ATERM(JTERM)(1:6).EQ.'~#fin_')THEN
          ICOUNT=ICOUNT-1
        END IF
        IF(ICOUNT.LT.0)THEN
          IFAIL=1
          RETURN
        END IF
        IF(ICOUNT.EQ.0)THEN
          IF(JTERM.LT.NTERM)THEN
            DO 40 I=NTERM,JTERM+1,-1
              ATERM(I+1)=ATERM(I)
40          CONTINUE
          END IF
          ATERM(JTERM+1)='~#fin_'
          NTERM=NTERM+1
          RETURN
        END IF
100   CONTINUE

      RETURN
      END



      SUBROUTINE GETNEXT(IFAIL,NOPER,CLINE,ATERM,OPERAT)

! -- Subroutine GETNEXT splits off the next term of an expression.

      INTEGER IFAIL,I,J,NB,NOPER,L,K,IERR
      double precision DVAL
      character*10 AFMT
      CHARACTER*(*) CLINE
      CHARACTER*(*) ATERM
      CHARACTER*(*) OPERAT(NOPER)

      ATERM=' '
      IFAIL=0
      IF(CLINE.EQ.' ')THEN
        IFAIL=-1
        RETURN
      END IF

      DO 10 I=1,NOPER
        IF(CLINE(1:1).EQ.OPERAT(I))THEN
          ATERM(1:1)=OPERAT(I)
          CLINE=CLINE(2:)
          cline=adjustl(cline)
          GO TO 20
        END IF
10    CONTINUE
      GO TO 50

20    IF(ATERM(1:1).EQ.'*')THEN
        IF(CLINE(1:1).EQ.'*')THEN
          ATERM(1:1)='^'
          CLINE=CLINE(2:)
          cline=adjustl(cline)
        END IF
      END IF
      RETURN

50    CONTINUE
      NB=len_trim(CLINE)
      DO 100 I=2,NB
        DO 90 J=1,NOPER
          IF(CLINE(I:I).EQ.OPERAT(J)) THEN
            if(I.LE.2) go to 120
            if(I.EQ.NB) go to 120
            IF((J.NE.4).AND.(J.NE.5))go to 120
            if((CLINE(I-1:I-1).NE.'E').AND.(CLINE(I-1:I-1).NE.'e').AND.   &
               (CLINE(I-1:I-1).NE.'D').AND.(CLINE(I-1:I-1).NE.'d'))go to 120
            DO 190 K=I+1,NB
              DO 180 L=1,NOPER
                if(CLINE(K:K).EQ.OPERAT(L))go to 200
180           CONTINUE
190         CONTINUE
            K=NB+1
200         K=K-1
            afmt='(f    .0)'
            write(afmt(3:6),'(i4)')k
            read(cline(1:k),afmt,iostat=ierr) dval
            if(IERR.NE.0) go to 120
            go to 100
          end IF
90      CONTINUE
100   CONTINUE
      ATERM=CLINE(1:MIN(28,NB))
      CLINE=' '
      RETURN

120   ATERM=CLINE(1:I-1)
      CLINE=CLINE(I:)
      RETURN

      END


      SUBROUTINE COMPRESS(MAXTERM,NTERM,ATERM,BTERM,rterm)

! -- Subroutine COMPRESS removes "dead terms" from the expression.

      INTEGER MAXTERM,NTERM,I,JTERM
      double precision rterm(maxterm)
      CHARACTER*(*) ATERM(MAXTERM),BTERM(MAXTERM)

      DO 100 I=1,NTERM
        BTERM(I)=ATERM(I)
100   CONTINUE
      JTERM=0
      DO 200 I=1,NTERM
        IF(BTERM(I)(1:1).NE.CHAR(220))THEN
          JTERM=JTERM+1
          ATERM(JTERM)=BTERM(I)
          rterm(jterm)=rterm(i)
        END IF
200   CONTINUE
      NTERM=JTERM

      RETURN
      END


      SUBROUTINE series_sub(IFAIL,NTERM,itype)

! -- Subroutine SERIES_SUB replaces series names with their numbers.

       use tspvar
       use defn
       use inter
       implicit none

      INTEGER IFAIL,NTERM,ITERM,J,JERR,NB,is,itype
      DOUBLE PRECISION DTEMP
      character*10 as
      CHARACTER*25 AAPAR

      IFAIL=0
      DO 200 ITERM=1,NTERM
         if(aterm(iterm)(1:2).eq.'@_') go to 200
         IF(ATERM(ITERM)(1:2).EQ.'~#') GO TO 200
         DO 20 J=1,NOPER
           IF(ATERM(ITERM)(1:1).EQ.OPERAT(J)) GO TO 200
20       CONTINUE
         AAPAR=ATERM(ITERM)
         NB=len_trim(AAPAR)
         IF(INDEX(AAPAR(1:NB),' ').NE.0)THEN
           if(itype.eq.0)then
             WRITE(amessage,30) AAPAR(1:NB)
30           FORMAT('series name "',A,'" in series equation cannot include a ',  &
             'blank character.')
           else if(itype.eq.1)then
             WRITE(amessage,31) AAPAR(1:NB)
31           FORMAT('series name "',A,'" in weights equation cannot include a ',  &
             'blank character.')
           endif
           IFAIL=1
           RETURN
         END IF
         call char2num(jerr,aapar,dtemp)
!         CALL RLREAD(JERR,AAPAR,DTEMP)
         IF(JERR.EQ.0) GO TO 200
         do is=1,MAXSERIES
           if(.not.series(is)%active) cycle
           if(series(is)%name.ne.aapar)cycle
           call num2char(is,as)
           aterm(iterm)='$~$'//trim(as)
           go to 200
         end do
         if(itype.eq.0)then
           write(amessage,40) trim(aapar)
40         format('series "',a,'" appearing in the series equation is either ', &
           'undefined or has been erased.')
         else if(itype.eq.1)then
           write(amessage,41) trim(aapar)
41         format('series "',a,'" appearing in a weights equation is either ', &
           'undefined or has been erased.')
         end if
         ifail=1
         return
200   CONTINUE

      RETURN
      END



      SUBROUTINE EVALUATE(IFAIL,MAXTERM,NTERM,NOPER,NFUNCT,ATERM,BTERM,   &
      OPERAT,FUNCT,IORDER,DVAL,rterm)

       use defn
       use inter
       implicit none

      INTEGER NTERM,NOPER,NFUNCT,MAXTERM,ITERM,JERR,MAXORD,ICOUNT,I,      &
      IOPER,IFAIL
      INTEGER IORDER(MAXTERM)
      double precision rterm(maxterm)
      DOUBLE PRECISION DVAL,DTEMP1,DTEMP2
      CHARACTER*1 AA
      CHARACTER*6 AFUNCT
      CHARACTER*(*) ATERM(MAXTERM),BTERM(MAXTERM)
      CHARACTER*(*) OPERAT(NOPER),FUNCT(NFUNCT)

      IFAIL=0

! -- IF THERE IS ONLY ONE TERM LEFT, THE EXPRESSION HAS BEEN EVALUATED.

100   CONTINUE
!      write(99,*) (trim(aterm(iterm)),iterm=1,nterm)     !debug

      IF(NTERM.EQ.1)THEN
        dval=rterm(1)
!        CALL RLREAD(JERR,ATERM(1),DVAL)
!        IF(JERR.NE.0)THEN
!          WRITE(amessage,110)
!110       FORMAT('cannot evaluate series equation using current parameter values.')
!          go to 9999
!        END IF
        RETURN
      END IF

! -- IF THERE ARE ANY NUMBERS SURROUNDED BY BRACKETS, THEN THE BRACKETS ARE
!    REMOVED

      IF(NTERM.GE.3)THEN
        DO 150 ITERM=1,NTERM-2
          IF(ATERM(ITERM)(1:1).EQ.'(') THEN
            IF(ATERM(ITERM+2)(1:1).EQ.')')THEN
              ATERM(ITERM)(1:1)=CHAR(220)
              ATERM(ITERM+2)(1:1)=CHAR(220)
              CALL COMPRESS(MAXTERM,NTERM,ATERM,BTERM,rterm)
              GO TO 100
            END IF
          END IF
150     CONTINUE
      END IF

! -- CAN ANY FUNCTION EVALUATIONS NOW BE DONE?

      IF(NTERM.GE.3)THEN
        DO 300 ITERM=1,NTERM-2
          IF(ATERM(ITERM)(1:6).EQ.'~#str_')THEN
            IF(ATERM(ITERM+2)(1:6).EQ.'~#fin_')THEN
              CALL FUNCEVAL(JERR,NFUNCT,ATERM(ITERM),rterm(iterm+1),       &
              DVAL,FUNCT)
              IF(JERR.NE.0)THEN
                AFUNCT=FUNCT(JERR)
                WRITE(amessage,170) trim(AFUNCT)
170             FORMAT('cannot evaluate "',A,'" function in ',    &
                'series or weights equation because function argument is out of range ', &
                'for at least one term in the series time_span.')
                go to 9999
              END IF
              ATERM(ITERM)(1:1)=CHAR(220)
              rterm(iterm+1)=dval
              aterm(iterm+1)='~!~'
              ATERM(ITERM+2)(1:1)=CHAR(220)
              CALL COMPRESS(MAXTERM,NTERM,ATERM,BTERM,rterm)
              GO TO 100
            END IF
          END IF
300     CONTINUE
      END IF

! -- The operators are now ranked by their level of nesting.

      MAXORD=0
      DO 320 ITERM=1,NTERM
        IORDER(ITERM)=0
320   CONTINUE
      ICOUNT=1
      DO 350 ITERM=1,NTERM
        AA=ATERM(ITERM)(1:1)
        IF(AA.EQ.'(')THEN
          ICOUNT=ICOUNT+1
        ELSE IF(AA.EQ.')')THEN
          ICOUNT=ICOUNT-1
        ELSE IF(ATERM(ITERM)(1:6).EQ.'~#str_')THEN
          ICOUNT=ICOUNT+1
        ELSE IF(ATERM(ITERM)(1:6).EQ.'~#fin_')THEN
          ICOUNT=ICOUNT-1
        ELSE IF((AA.EQ.'+').OR.(AA.EQ.'-').OR.(AA.EQ.'*').OR.             &
        (AA.EQ.'/').OR.(AA.EQ.'^'))THEN
          IORDER(ITERM)=ICOUNT
          IF(ICOUNT.GT.MAXORD)MAXORD=ICOUNT
        ELSE
          IORDER(ITERM)=-1            ! It must be a number.
        END IF
350   CONTINUE

! -- We now look for a calculation to do, starting at the highest level.

      IF(NTERM.GE.3)THEN
        DO 400 I=MAXORD,1,-1
          DO 390 IOPER=1,5
            DO 380 ITERM=2,NTERM-1
              IF(IORDER(ITERM).EQ.I)THEN   !It is an operator
                IF(ATERM(ITERM)(1:1).EQ.OPERAT(IOPER))THEN
                  IF((IORDER(ITERM-1).LT.0).AND.                          &
                     (IORDER(ITERM+1).LT.0))THEN    !numbers either side
                     dtemp1=rterm(iterm-1)
                     dtemp2=rterm(iterm+1)
!                    CALL RLREAD(IFAIL,ATERM(ITERM-1),DTEMP1)
!                    CALL RLREAD(IFAIL,ATERM(ITERM+1),DTEMP2)
                    IF(IOPER.EQ.1)THEN
                      IF(DTEMP1.LT.0.0)THEN
                        IF(DTEMP2.NE.FLOAT(NINT(DTEMP2)))THEN
                          write(amessage,384)
384                       format('negative number raised to fractional power in series ', &
                          'or weights equation.')
                          go to 9999
                        end IF
                      end IF
                      DVAL=DTEMP1**DTEMP2
                    ELSE IF(IOPER.EQ.3)THEN
                      DVAL=DTEMP1*DTEMP2
                    ELSE IF(IOPER.EQ.2)THEN
                      IF(DTEMP2.EQ.0.0D0) THEN
                        WRITE(amessage,385)
385                     FORMAT('divide by zero in series or weights equation.')
                        go to 9999
                      END IF
                      DVAL=DTEMP1/DTEMP2
                    ELSE IF(IOPER.EQ.5)THEN
                      DVAL=DTEMP1+DTEMP2
                    ELSE IF(IOPER.EQ.4)THEN
                      DVAL=DTEMP1-DTEMP2
                    END IF
                    rterm(iterm)=dval
                    aterm(iterm)='~!~'
                    ATERM(ITERM-1)(1:1)=CHAR(220)
                    ATERM(ITERM+1)(1:1)=CHAR(220)
                    CALL COMPRESS(MAXTERM,NTERM,ATERM,BTERM,rterm)
                    GO TO 100
                  END IF
                END IF
              END IF
380         CONTINUE
390       CONTINUE
400     CONTINUE
      END IF
      WRITE(amessage,410)
410   FORMAT('cannot evaluate series equation.')
      go to 9999

9999  IFAIL=1
      RETURN
      END




      SUBROUTINE FUNCEVAL(JERR,NFUNCT,ATERM1,rterm,DVAL,FUNCT)

! -- Subroutine FUNCEVAL evaluates a function.

       use defn
       use inter
       implicit none


      INTEGER JERR,NFUNCT,IFN,IFAIL
      DOUBLE PRECISION DVAL,DTEMP,rterm
      CHARACTER*(*) ATERM1
      CHARACTER(*) FUNCT(NFUNCT)

! -- First we find out which function we are evaluating.

      JERR=0
      ATERM1(1:6)=' '
      aterm1=adjustl(aterm1)
      call char2num(ifail,aterm1,ifn)
      dtemp=rterm
!      CALL INREAD(IFAIL,ATERM1,IFN)
!      CALL RLREAD(IFAIL,ATERM2,DTEMP)
!      IF(IFAIL.NE.0) GO TO 9000
      IF(IFN.EQ.1)THEN
        DVAL=ABS(DTEMP)
      ELSE IF(IFN.EQ.2)THEN
        IF((DTEMP.GT.1.0D0).OR.(DTEMP.LT.-1.0D0))GO TO 9000
        DVAL=ACOS(DTEMP)
      ELSE IF(IFN.EQ.3)THEN
        IF((DTEMP.GT.1.0D0).OR.(DTEMP.LT.-1.0D0))GO TO 9000
        DVAL=ASIN(DTEMP)
      ELSE IF(IFN.EQ.4)THEN
        DVAL=ATAN(DTEMP)
      ELSE IF(IFN.EQ.5)THEN
        IF((DTEMP.GT.1.0D10).OR.(DTEMP.LT.-1.0D10))GO TO 9000
        DVAL=COS(DTEMP)
      ELSE IF(IFN.EQ.6)THEN
        DVAL=COSH(DTEMP)
      ELSE IF(IFN.EQ.7)THEN
        IF(DTEMP.GT.500.0D0) GO TO 9000
        DVAL=EXP(DTEMP)
      ELSE IF(IFN.EQ.8)THEN
        IF(DTEMP.LE.0.0D0) GO TO 9000
        DVAL=LOG(DTEMP)
      ELSE IF(IFN.EQ.9)THEN
        IF(DTEMP.LE.0.0D0) GO TO 9000
        DVAL=LOG10(DTEMP)
      ELSE IF(IFN.EQ.10)THEN
        IF((DTEMP.GT.1.0D10).OR.(DTEMP.LT.-1.0D10))GO TO 9000
        DVAL=SIN(DTEMP)
      ELSE IF(IFN.EQ.11)THEN
        DVAL=SINH(DTEMP)
      ELSE IF(IFN.EQ.12)THEN
        IF(DTEMP.LT.0.0D0) GO TO 9000
        DVAL=SQRT(DTEMP)
      ELSE IF(IFN.EQ.13)THEN
        IF((DTEMP.GT.1.0E10).OR.(DTEMP.LT.-1.0E10))GO TO 9000
        DVAL=TAN(DTEMP)
      ELSE IF(IFN.EQ.14)THEN
        DVAL=TANH(DTEMP)
      ELSE IF(IFN.EQ.15)THEN
        DVAL=-DTEMP
      ELSE IF(IFN.EQ.16)THEN
        DVAL=DTEMP
      END IF

      RETURN

! -- An error condition has occurred.

9000  JERR=IFN
      RETURN
      END





!     Last change:  J     9 Sep 2004   10:39 pm
subroutine pest_files(ifail,lastblock)

! -- Subroutine PEST_FILES generates a PEST input dataset.

       use tspvar
       use defn
       use inter
       implicit none

       integer, intent(out)   :: ifail
       integer, intent(in)    :: lastblock

! -- General parameters
       logical lexist
       integer ierr,icontext,itempfile,ioseries,iostable,iovtable,iodtable,i,iunit,j, &
       jline,numtempfile,ii1,ll,jj1,jj,kk,io,im,noterm,nmterm,iomseries,iomstable,  &
       iomvtable,iomdtable,iout,nsterm,iterm,il,siout,nobs,nobsgp,ieqnerr,nterm,nnterm, &
       isnum,dd,nn,yy,mm,k,ixcon,auiyesno,itempunit,isvd,iaui,itemp
       real rotemp,rmtemp,rprecis,weightmin,weightmax,totim,rtime,eigthresh
       integer obsseries(MAXSERIES),obsstable(MAXSTABLE),obsvtable(MAXVTABLE), &
       obsdtable(MAXDTABLE),modseries(MAXSERIES),modstable(MAXSTABLE), &
       modvtable(MAXVTABLE),moddtable(MAXDTABLE)
       real sweightmin(MAXSERIES),sweightmax(MAXSERIES),stweightmin(MAXSTABLE), &
       stweightmax(MAXSTABLE),vtweightmin(MAXVTABLE),vtweightmax(MAXVTABLE), &
       dtweightmin(MAXDTABLE),dtweightmax(MAXDTABLE)
       double precision dval,dtempx
       character*1 aa
       character*3 auiaa
       character*10 aoname,amname,anum,atrans
       character*15 aline,avariable
       character*30 aoption,correct_keyword,last_keyword,atemp,otherblock,aname
       character*120 pardatfile,pestctlfile,instructfile,modcomline,bstring,cstring, &
       micactlfile,pest2micacom
       character*25 acontext(MAXCONTEXT)
       character*12 basename(MAXSERIES+MAXVTABLE+MAXDTABLE),sbasename(MAXSTABLE), &
                    obgnme(MAXSERIES+MAXSTABLE+MAXVTABLE+MAXDTABLE)
       character*120 tempfile(MAXTEMPFILE),modfile(MAXTEMPFILE)
       character*150 sequation(MAXSERIES),stequation(MAXSTABLE),vtequation(MAXVTABLE), &
                     dtequation(MAXDTABLE),eqntext

! -- Variable used for dealing with parameter groups.

       integer                   :: igp,f_numpargp,npargp
       real,         allocatable :: f_derinc(:),f_derinclb(:),f_derincmul(:), derinc(:), &
                                    derinclb(:),derincmul(:)
       character*14              :: apargp
       character*120             :: pargroupfile
       character*14, allocatable :: f_pargpnme(:),f_inctyp(:),f_forcen(:),f_dermthd(:), &
                                    forcen(:),dermthd(:),pargpnme(:),inctyp(:)

! -- Variable used for dealing with parameter data.

       integer                   :: ipar,f_numpar,npar,tempunit,nnpar
       real, allocatable         :: f_parval1(:),f_parlbnd(:),f_parubnd(:),f_scale(:), &
                                    f_offset(:),parval1(:),parlbnd(:),parubnd(:),      &
                                    scale(:),offset(:)
       character*1               :: pardelim
       character*12              :: aapar
       character*12              :: apar(MAXPAR)
       character*14, allocatable :: f_parnme(:),f_parchglim(:),f_pargp(:), &
                                    parchglim(:),pargp(:)
       character*19, allocatable :: f_partrans(:),partrans(:)

       ifail=0
       currentblock='WRITE_PEST_FILES'
       ieqnerr=0

       write(*,10) trim(currentblock)
       write(recunit,10) trim(currentblock)
10     format(/,' Processing ',a,' block....')
       if(lastblock.ne.201)then
         write(amessage,15)
15       format('a WRITE_PEST_FILES block must immediately follow a LIST_OUTPUT block ', &
         'in a TSPROC input file.')
         go to 9800
       end if

! -- Initialisation

       isvd=0
       iaui=0
       auiyesno=0
       icontext=0
       itempfile=0
       tempfile=' '             ! tempfile is an array
       modfile=' '              ! modfile is an array

       sequation=' '            ! sequation is an array
       stequation=' '           ! stequation is an array
       vtequation=' '           ! vtequation is an array
       dtequation=' '           ! dtequation is an array

       ioseries=0
       iostable=0
       iovtable=0
       iodtable=0
       iomseries=0
       iomstable=0
       iomvtable=0
       iomdtable=0

       pardatfile=' '
       pargroupfile=' '
       pestctlfile=' '
       instructfile=' '
       modcomline=' '
       micactlfile=' '
       pest2micacom=' '
       
       sweightmin=-1.0e36              !sweightmin is an array
       sweightmax= 1.0e36              !sweightman is an array
       stweightmin=-1.0e36             !stweightmin is an array
       stweightmax= 1.0e36             !stweightmax is an array
       vtweightmin=-1.0e36              !vtweightmin is an array
       vtweightmax= 1.0e36             !vtweightmax is an array
       dtweightmin=-1.0e36             !dtweightmin is an array
       dtweightmax= 1.0e36             !dtweightmax is an array

       f_numpargp=0
       f_numpar=0
       ixcon=0
       iunit=0

! -- The PEST_FILES block is first parsed.

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
20         format('insufficient entries on line ',a,' of file ',a)
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
         if(aoption.eq.'TEMPLATE_FILE')then
           itempfile=itempfile+1
           if(itempfile.gt.MAXTEMPFILE)then
             call num2char(MAXTEMPFILE,aline)
             write (amessage,30) trim(aline),trim(currentblock)
30           format('only ',a,' template files can be cited in a ',a,' block.')
             go to 9800
           end if
           call getfile(ierr,cline,tempfile(itempfile),left_word(2),right_word(2))
           if(ierr.ne.0)then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,35) trim(aline),trim(astring)
35           format('cannot read template file name from line ',a,' of file ',a)
             go to 9800
           end if
           write(*,37) trim(aoption),trim(tempfile(itempfile))
           write(recunit,37) trim(aoption),trim(tempfile(itempfile))
37         format(t5,a,' ',a)
         else if(aoption.eq.'MODEL_INPUT_FILE')then
           correct_keyword='TEMPLATE_FILE'
           if(last_keyword.ne.correct_keyword)go to 9300
           call getfile(ierr,cline,modfile(itempfile),left_word(2),right_word(2))
           if(ierr.ne.0)then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,40) trim(aline),trim(astring)
40           format('cannot read model input file name from line ',a,' of file ',a)
             go to 9800
           end if
           write(*,37) trim(aoption),trim(modfile(itempfile))
           write(recunit,37) trim(aoption),trim(modfile(itempfile))
         else if(aoption.eq.'PARAMETER_DATA_FILE')then
           call getfile(ierr,cline,pardatfile,left_word(2),right_word(2))
           if(ierr.ne.0)then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,50) trim(aline),trim(astring)
50           format('cannot read parameter data file name from line ',a,' of file ',a)
             go to 9800
           end if
           write(*,37) trim(aoption),trim(pardatfile)
           write(recunit,37) trim(aoption),trim(pardatfile)
         else if(aoption.eq.'PARAMETER_GROUP_FILE')then
           call getfile(ierr,cline,pargroupfile,left_word(2),right_word(2))
           if(ierr.ne.0)then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,52) trim(aline),trim(astring)
52           format('cannot read parameter group file name from line ',a,' of file ',a)
             go to 9800
           end if
           write(*,37) trim(aoption),trim(pargroupfile)
           write(recunit,37) trim(aoption),trim(pargroupfile)
         else if(aoption.eq.'AUTOMATIC_USER_INTERVENTION')then
           call get_yes_no(ierr,auiyesno)
           if(ierr.ne.0) go to 9800
           if(auiyesno.eq.1)then
             auiaa='yes'
           else
             auiaa='no'
           end if
           iaui=1
           write(*,37) trim(aoption),trim(auiaa)
           write(recunit,37) trim(aoption),trim(auiaa)
         else if(aoption.eq.'TRUNCATED_SVD')then
           call get_keyword_value(ierr,2,itemp,eigthresh,aoption)
           if(ierr.ne.0) go to 9800
           if(eigthresh.le.0.0)then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,53) trim(aline),trim(astring)
53           format('SVD truncation limit must be positive at line ',a,' of file ',a)
             go to 9800
           end if
           isvd=1
         else if(aoption.eq.'NEW_PEST_CONTROL_FILE')then
           call getfile(ierr,cline,pestctlfile,left_word(2),right_word(2))
           if(ierr.ne.0)then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,55) trim(aline),trim(astring)
55           format('cannot read pest control file name from line ',a,' of file ',a)
             go to 9800
           end if
           write(*,37) trim(aoption),trim(pestctlfile)
           write(recunit,37) trim(aoption),trim(pestctlfile)
         else if(aoption.eq.'NEW_MICA_CONTROL_FILE')then
           call getfile(ierr,cline,micactlfile,left_word(2),right_word(2))
           if(ierr.ne.0)then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,155) trim(aline),trim(astring)
155          format('cannot read mica control file name from line ',a,' of file ',a)
             go to 9800
           end if
           write(*,37) trim(aoption),trim(micactlfile)
           write(recunit,37) trim(aoption),trim(micactlfile)
         else if(aoption.eq.'PEST2MICA_COMMAND')then
           call getfile(ierr,cline,pest2micacom,left_word(2),right_word(2))
           if(ierr.ne.0)then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,156) trim(aline),trim(astring)
156          format('cannot read PEST2MICA command from line ',a,' of file ',a)
             go to 9800
           end if
           write(*,37) trim(aoption),trim(pest2micacom)
           write(recunit,37) trim(aoption),trim(pest2micacom)
         else if(aoption.eq.'NEW_INSTRUCTION_FILE')then
           call getfile(ierr,cline,instructfile,left_word(2),right_word(2))
           if(ierr.ne.0)then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,56) trim(aline),trim(astring)
56           format('cannot read instruction file name from line ',a,' of file ',a)
             go to 9800
           end if
           write(*,37) trim(aoption),trim(instructfile)
           write(recunit,37) trim(aoption),trim(instructfile)
         else if(aoption.eq.'MODEL_COMMAND_LINE')then
           call getfile(ierr,cline,modcomline,left_word(2),right_word(2))
           if(ierr.ne.0)then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,57) trim(aline),trim(astring)
57           format('cannot read model command line from line ',a,' of file ',a)
             go to 9800
           end if
           write(*,37) trim(aoption),trim(modcomline)
           write(recunit,37) trim(aoption),trim(modcomline)
         else if(aoption.eq.'OBSERVATION_SERIES_NAME')then
           ioseries=ioseries+1
           if(ioseries.gt.MAXSERIES)then
             call num2char(MAXSERIES,aline)
             write(amessage,100) trim(aline),trim(currentblock)
100          format('a maximum of ',a,' series can be cited in a ',a,' block.')
             go to 9800
           end if
           call read_series_name(ierr,obsseries(ioseries),'OBSERVATION_SERIES_NAME')
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'OBSERVATION_S_TABLE_NAME')then
           iostable=iostable+1
           if(iostable.gt.MAXSTABLE)then
             call num2char(MAXSTABLE,aline)
             write(amessage,102) trim(aline),trim(currentblock)
102          format('a maximum of ',a,' s_tables can be cited in a ',a,' block.')
             go to 9800
           end if
           call read_table_name(ierr,obsstable(iostable),11)
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'OBSERVATION_C_TABLE_NAME')then
           write(amessage,109) 
109        format('current version of TSPROC does not allow C_TABLES to be ', &
           'used for parameter estimation.')
           go to 9800
         else if(aoption.eq.'OBSERVATION_V_TABLE_NAME')then
           iovtable=iovtable+1
           if(iovtable.gt.MAXVTABLE)then
             call num2char(MAXVTABLE,aline)
             write(amessage,103) trim(aline),trim(currentblock)
103          format('a maximum of ',a,' v_tables can be cited in a ',a,' block.')
             go to 9800
           end if
           call read_table_name(ierr,obsvtable(iovtable),12)
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'OBSERVATION_E_TABLE_NAME')then
           iodtable=iodtable+1
           if(iodtable.gt.MAXDTABLE)then
             call num2char(MAXDTABLE,aline)
             write(amessage,104) trim(aline),trim(currentblock)
104          format('a maximum of ',a,' e_tables can be cited in a ',a,' block.')
             go to 9800
           end if
           call read_table_name(ierr,obsdtable(iodtable),13)
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'MODEL_SERIES_NAME')then
           correct_keyword='OBSERVATION_SERIES_NAME'
           if(last_keyword.ne.correct_keyword) go to 9300
           iomseries=iomseries+1
           call read_series_name(ierr,modseries(iomseries),'MODEL_SERIES_NAME')
           if(ierr.ne.0) go to 9800
           if(iomseries.gt.1)then
             do k=1,iomseries-1
               if(modseries(k).eq.modseries(iomseries))then
                 write(amessage,105) trim(series(modseries(iomseries))%name)
105              format('time series "',a,'" has been provided as more than one ', &
                 'MODEL_SERIES_NAME.')
                 go to 9800
               end if
             end do
           end if
         else if(aoption.eq.'MODEL_S_TABLE_NAME')then
           correct_keyword='OBSERVATION_S_TABLE_NAME'
           if(last_keyword.ne.correct_keyword) go to 9300
           iomstable=iomstable+1
           call read_table_name(ierr,modstable(iomstable),21)
           if(ierr.ne.0) go to 9800
           if(iomstable.gt.1)then
             do k=1,iomstable-1
               if(modstable(k).eq.modstable(iomstable))then
                 write(amessage,106) trim(stable(modstable(iomstable))%name)
106              format('s_table "',a,'" has been provided as more than one ', &
                 'MODEL_S_TABLE_NAME.')
                 go to 9800
               end if
             end do
           end if
         else if(aoption.eq.'MODEL_C_TABLE_NAME')then
           write(amessage,109)
           go to 9800
         else if(aoption.eq.'MODEL_V_TABLE_NAME')then
           correct_keyword='OBSERVATION_V_TABLE_NAME'
           if(last_keyword.ne.correct_keyword) go to 9300
           iomvtable=iomvtable+1
           call read_table_name(ierr,modvtable(iomvtable),22)
           if(ierr.ne.0) go to 9800
           if(iomvtable.gt.1)then
             do k=1,iomvtable-1
               if(modvtable(k).eq.modvtable(iomvtable))then
                 write(amessage,107) trim(vtable(modvtable(iomvtable))%name)
107              format('v_table "',a,'" has been provided as more than one ', &
                 'MODEL_V_TABLE_NAME.')
                 go to 9800
               end if
             end do
           end if
         else if(aoption.eq.'MODEL_E_TABLE_NAME')then
           correct_keyword='OBSERVATION_E_TABLE_NAME'
           if(last_keyword.ne.correct_keyword) go to 9300
           iomdtable=iomdtable+1
           call read_table_name(ierr,moddtable(iomdtable),23)
           if(ierr.ne.0) go to 9800
           if(iomdtable.gt.1)then
             do k=1,iomdtable-1
               if(moddtable(k).eq.moddtable(iomdtable))then
                 write(amessage,108) trim(dtable(moddtable(iomdtable))%name)
108              format('e_table "',a,'" has been provided as more than one ', &
                 'MODEL_E_TABLE_NAME.')
                 go to 9800
               end if
             end do
           end if
         else if(aoption.eq.'SERIES_WEIGHTS_EQUATION')then
           correct_keyword='MODEL_SERIES_NAME'
           if(last_keyword.ne.correct_keyword) go to 9300
           call get_equation(ierr,sequation(ioseries),aoption)
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'S_TABLE_WEIGHTS_EQUATION')then
           correct_keyword='MODEL_S_TABLE_NAME'
           if(last_keyword.ne.correct_keyword) go to 9300
           call get_equation(ierr,stequation(iostable),aoption)
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'V_TABLE_WEIGHTS_EQUATION')then
           correct_keyword='MODEL_V_TABLE_NAME'
           if(last_keyword.ne.correct_keyword) go to 9300
           call get_equation(ierr,vtequation(iovtable),aoption)
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'E_TABLE_WEIGHTS_EQUATION')then
           correct_keyword='MODEL_E_TABLE_NAME'
           if(last_keyword.ne.correct_keyword) go to 9300
           call get_equation(ierr,dtequation(iodtable),aoption)
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'SERIES_WEIGHTS_MIN_MAX')then
           correct_keyword='SERIES_WEIGHTS_EQUATION'
           if(last_keyword.ne.correct_keyword) go to 9300
           call get_two_numbers(ierr,sweightmin(ioseries),sweightmax(ioseries),aoption)
           if(ierr.ne.0) go to 9800
           call check_weight_order(ierr,sweightmin(ioseries),sweightmax(ioseries))
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'S_TABLE_WEIGHTS_MIN_MAX')then
           correct_keyword='S_TABLE_WEIGHTS_EQUATION'
           if(last_keyword.ne.correct_keyword) go to 9300
           call get_two_numbers(ierr,stweightmin(iostable),stweightmax(iostable),aoption)
           if(ierr.ne.0) go to 9800
           call check_weight_order(ierr,stweightmin(iostable),stweightmax(iostable))
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'V_TABLE_WEIGHTS_MIN_MAX')then
           correct_keyword='V_TABLE_WEIGHTS_EQUATION'
           if(last_keyword.ne.correct_keyword) go to 9300
           call get_two_numbers(ierr,vtweightmin(iovtable),vtweightmax(iovtable),aoption)
           if(ierr.ne.0) go to 9800
           call check_weight_order(ierr,vtweightmin(iovtable),vtweightmax(iovtable))
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'E_TABLE_WEIGHTS_MIN_MAX')then
           correct_keyword='E_TABLE_WEIGHTS_EQUATION'
           if(last_keyword.ne.correct_keyword) go to 9300
           call get_two_numbers(ierr,dtweightmin(iodtable),dtweightmax(iodtable),aoption)
           if(ierr.ne.0) go to 9800
           call check_weight_order(ierr,dtweightmin(iodtable),dtweightmax(iodtable))
           if(ierr.ne.0) go to 9800
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
           go to 200
         else
           call num2char(iline,aline)
           call addquote(infile,astring)
           write(amessage,90) trim(aoption),trim(currentblock),trim(aline),trim(astring)
90         format('unexpected keyword - "',a,'" in ',a,' block at line ',a, &
           ' of file ',a)
           go to 9800
         end if
         last_keyword=aoption
       end do

200    continue

! -- Any absenses in the block are now looked for.

       if((ioseries.eq.0).and.(iostable.eq.0).and.(iovtable.eq.0).and.   &
          (iodtable.eq.0))then
         write(amessage,210) trim(currentblock)
210      format('no observation series or table names have been cited in ',a,' block.')
         go to 9800
       end if
       if(itempfile.eq.0)then
         write(amessage,220) trim(currentblock)
220      format('at least one TEMPLATE_FILE keyword must be provided in ',&
         'a ',a,' block.')
         go to 9800
       end if
       if(pestctlfile.eq.' ')then
         write(amessage,230) trim(currentblock)
230      format('a NEW_PEST_CONTROL_FILE keyword must be provided in a ',a,' block.')
         go to 9800
       end if
       if(instructfile.eq.' ')then
         write(amessage,240) trim(currentblock)
240      format('NEW_INSTRUCTION_FILE keyword is missing from the ',a,' block.')
         go to 9800
       end if
       if(ioseries.ne.0)then
         if(iomseries.ne.ioseries)then
           write(amessage,241) trim(currentblock)
241        format('a MODEL_SERIES_NAME keyword has not been provided for each ', &
             'OBSERVATION_SERIES_NAME cited in the ',a,' block.')
           go to 9800
         end if
         do i=1,ioseries
           if(sequation(i).eq.' ')then
             write(amessage,250) trim(currentblock)
250          format('a SERIES_WEIGHTS_EQUATION keyword has not been provided for each ', &
             'series cited in the ',a,' block.')
             go to 9800
           end if
         end do
       end if
       if(iostable.ne.0)then
         if(iomstable.ne.iostable)then
           write(amessage,251) trim(currentblock)
251        format('a MODEL_S_TABLE_NAME keyword has not been provided for each ', &
             'OBSERVATION_S_TABLE_NAME cited in the ',a,' block.')
           go to 9800
         end if
         do i=1,iostable
           if(stequation(i).eq.' ')then
             write(amessage,260) trim(currentblock)
260          format('an S_TABLE_WEIGHTS_EQUATION keyword has not been provided for each ', &
             's_table cited in the ',a,' block.')
             go to 9800
           end if
         end do
       end if
       if(iovtable.ne.0)then
         if(iomvtable.ne.iovtable)then
           write(amessage,261) trim(currentblock)
261        format('a MODEL_V_TABLE_NAME keyword has not been provided for each ', &
             'OBSERVATION_V_TABLE_NAME cited in the ',a,' block.')
           go to 9800
         end if
         do i=1,iovtable
           if(vtequation(i).eq.' ')then
             write(amessage,270) trim(currentblock)
270          format('a V_TABLE_WEIGHTS_EQUATION keyword has not been provided for each ', &
             'v_table cited in the ',a,' block.')
             go to 9800
           end if
         end do
       end if
       if(iodtable.ne.0)then
         if(iomdtable.ne.iodtable)then
           write(amessage,271) trim(currentblock)
271        format('a MODEL_E_TABLE_NAME keyword has not been provided for each ', &
             'OBSERVATION_E_TABLE_NAME cited in the ',a,' block.')
           go to 9800
         end if
         do i=1,iodtable
           if(dtequation(i).eq.' ')then
             write(amessage,280) trim(currentblock)
280          format('a E_TABLE_WEIGHTS_EQUATION keyword has not been provided for each ', &
             'e_table cited in the ',a,'block.')
             go to 9800
           end if
         end do
       end if
       if(icontext.eq.0)then
         write(amessage,290) trim(currentblock)
290      format('no CONTEXT keyword(s) provided in ',a,' block.')
         go to 9800
       end if
       if((micactlfile.ne.' ').and.(pest2micacom.eq.' '))then
         write(amessage,291)
291      format('if a NEW_MICA_CONTROL_FILE keyword is supplied, a PEST2MICA_COMMAND ', &
         'keyword must also be supplied.')
         go to 9800
       end if
       if((isvd.eq.1).and.(iaui.eq.1))then
         write(amessage,292) trim(currentblock)
292      format('only one of the TRUNCATED_SVD or AUTOMATIC_USER_INTERVENTION keywords ', &
         'must be supplied in ',a,' block.')
         go to 9800
       end if

! -- Before any processing is done, a check is made that the observation series and
!    tables correspond to the series and tables requested for output in the last
!    LIST_OUTPUT block.

       otherblock='LIST_OUTPUT'
       if((ioseries.ne.imseries).or.(iostable.ne.imstable).or.(iovtable.ne.imvtable).or. &
          (iodtable.ne.imdtable))then
          write(amessage,1010) trim(currentblock),trim(otherblock)
1010      format('the number of series, s_tables, e_tables and v_tables cited in the ', &
          a,' block does not correspond exactly to the number of these entities cited in ', &
          'the immediately-preceding ',a,' block.')
          go to 9800
       end if
       if(imctable.ne.0)then
         write(amessage,1011)
1011     format('a c_table features in the LIST_OUTPUT block preceding ', &
         'the WRITE_PEST_FILES block. The present version of TSPROC does not ', &
         'support the use of c_tables in the calibration process.')
         go to 9800
       end if
       if(ioseries.ne.0)then
         do i=1,ioseries
           io=obsseries(i)
           im=modseries(i)
           aoname=series(io)%name
           amname=series(im)%name
           if(io.eq.im) go to 1029
           noterm=series(io)%nterm
           nmterm=series(im)%nterm
           if(noterm.ne.nmterm)then
             write(amessage,1020) trim(aoname),trim(amname)
1020         format('OBSERVATION_SERIES "',a,'" has been matched to ', &
             'MODEL_SERIES "',a,'". However these series have different ', &
             'numbers of terms.')
             go to 9800
           end if
           do j=1,noterm
             if((series(io)%days(j).ne.series(im)%days(j)).or.   &
                (series(io)%secs(j).ne.series(im)%secs(j)))then
               write(amessage,1030) trim(aoname),trim(amname)
1030           format('OBSERVATION_SERIES "',a,'" has been matched to ', &
               'MODEL_SERIES "',a,'". However the dates and times in ', &
               'these SERIES do not correspond.')
               go to 9800
             end if
           end do
1029       continue
           do j=1,ioseries
             if(im.eq.outseries(j)) go to 1035
           end do
           write(amessage,1032) trim(amname),trim(currentblock)
1032       format('MODEL__SERIES "',a,'" is not listed in the ', &
           'LIST_OUTPUT block immediately preceding the ',a,' block.')
           go to 9800
1035       continue
         end do
       end if

       if(iostable.ne.0)then
         do i=1,iostable
           io=obsstable(i)
           im=modstable(i)
           aoname=stable(io)%name
           amname=stable(im)%name
           if(io.eq.im) go to 1039
           if(((stable(io)%maximum.lt.-1.0e36).and.(stable(im)%maximum.gt.-1.0e36)).or.  &
              ((stable(io)%maximum.gt.-1.0e36).and.(stable(im)%maximum.lt.-1.0e36)))then
             avariable='MAXIMUM'
             go to 9600
           end if
           if(((stable(io)%minimum.lt.-1.0e36).and.(stable(im)%minimum.gt.-1.0e36)).or.  &
              ((stable(io)%minimum.gt.-1.0e36).and.(stable(im)%minimum.lt.-1.0e36)))then
             avariable='MINIMUM'
             go to 9600
           end if
           if(((stable(io)%range.lt.-1.0e36).and.(stable(im)%range.gt.-1.0e36)).or.  &
              ((stable(io)%range.gt.-1.0e36).and.(stable(im)%range.lt.-1.0e36)))then
             avariable='RANGE'
             go to 9600
           end if
           if(((stable(io)%mean.lt.-1.0e36).and.(stable(im)%mean.gt.-1.0e36)).or.   &
              ((stable(io)%mean.gt.-1.0e36).and.(stable(im)%mean.lt.-1.0e36)))then
             avariable='MEAN'
             go to 9600
           end if
           if(((stable(io)%stddev.lt.-1.0e36).and.(stable(im)%stddev.gt.-1.0e36)).or.  &
              ((stable(io)%stddev.gt.-1.0e36).and.(stable(im)%stddev.lt.-1.0e36)))then
             avariable='STD_DEV'
             go to 9600
           end if
           if(((stable(io)%total.lt.-1.0e36).and.(stable(im)%total.gt.-1.0e36)).or.   &
              ((stable(io)%total.gt.-1.0e36).and.(stable(im)%total.lt.-1.0e36)))then
             avariable='SUM'
             go to 9600
           end if
           if(((stable(io)%minmean.lt.-1.0e36).and.(stable(im)%minmean.gt.-1.0e36)).or.   &
              ((stable(io)%minmean.gt.-1.0e36).and.(stable(im)%minmean.lt.-1.0e36)))then
             avariable='MINMEAN_*'
             go to 9600
           end if
           if(((stable(io)%maxmean.lt.-1.0e36).and.(stable(im)%maxmean.gt.-1.0e36)).or.   &
              ((stable(io)%maxmean.gt.-1.0e36).and.(stable(im)%maxmean.lt.-1.0e36)))then
             avariable='MAXMEAN_*'
             go to 9600
           end if
           if((stable(io)%maxmean.gt.-1.0e36).or.(stable(io)%minmean.gt.-1.0e36))then
             write(amessage,1023)
1023         format('The present version of TSPROC does not support the use of ', &
             'S_TABLE minimum or maximum sample count averages in the calibration process.')
             go to 9800
           end if
1039       continue
           do j=1,iostable
             if(im.eq.outstable(j)) go to 1038
           end do
           write(amessage,1037) 'S',trim(amname),trim(currentblock)
1037       format('MODEL_',a,'_TABLE "',a,'" is not listed in the ', &
           'LIST_OUTPUT block immediately preceding the ',a,' block.')
           go to 9800
1038       continue
         end do
       end if

       if(iovtable.ne.0)then
         do i=1,iovtable
           io=obsvtable(i)
           im=modvtable(i)
           aoname=vtable(io)%name
           amname=vtable(im)%name
           if(io.eq.im) go to 1047
           noterm=vtable(io)%nterm
           nmterm=vtable(im)%nterm
           if(noterm.ne.nmterm)then
             write(amessage,1040) trim(aoname),trim(amname)
1040         format('OBSERVATION_V_TABLE "',a,'" has been matched to ', &
             'MODEL_V_TABLE "',a,'". However these V_TABLES ', &
             'have different numbers of integration times.')
             go to 9800
           end if
           do j=1,noterm
             if((vtable(io)%days1(j).ne.vtable(im)%days1(j)).or.   &
                (vtable(io)%days2(j).ne.vtable(im)%days2(j)).or.   &
                (vtable(io)%secs1(j).ne.vtable(im)%secs1(j)).or.   &
                (vtable(io)%secs2(j).ne.vtable(im)%secs2(j)))then
               write(amessage,1050) trim(aoname),trim(amname)
1050           format('OBSERVATION_V_TABLE "',a,'" has been matched to ', &
               'MODEL_V_TABLE "',a,'". However the integration dates and ', &
               'times in these V_TABLES do not correspond.')
               go to 9800
             end if
           end do
1047       continue
           do j=1,iovtable
             if(im.eq.outvtable(j)) go to 1048
           end do
           write(amessage,1037) 'V',trim(amname),trim(currentblock)
           go to 9800
1048       continue
         end do
       end if

       if(iodtable.ne.0)then
         do i=1,iodtable
           io=obsdtable(i)
           im=moddtable(i)
           aoname=dtable(io)%name
           amname=dtable(im)%name
           if(io.eq.im) go to 1079
           noterm=dtable(io)%nterm
           nmterm=dtable(im)%nterm
           if(noterm.ne.nmterm)then
             write(amessage,1060) trim(aoname),trim(amname)
1060         format('OBSERVATION_E_TABLE "',a,'"  has been matched to ', &
             'MODEL E_TABLE "',a,'". However these E_TABLES ', &
             'have different numbers of flows.')
             go to 9800
           end if
           if(dtable(io)%under_over.ne.dtable(im)%under_over)then
             write(amessage,1061) trim(aoname),trim(amname)
1061         format('OBSERVATION_E_TABLE "',a,'"  has been matched to ', &
             'MODEL E_TABLE "',a,'". However these E_TABLES ', &
             'have different UNDER_OVER specifications.')
             go to 9800
           end if
           do j=1,noterm
             rotemp=dtable(io)%flow(j)
             rmtemp=dtable(im)%flow(j)
             rprecis=5*spacing(rmtemp)
             if((rotemp.lt.rmtemp-rprecis).or.(rotemp.gt.rmtemp+rprecis))then
               write(amessage,1070) trim(aoname),trim(amname)
1070           format('OBSERVATION_E_TABLE "',a,'"  has been matched to ', &
               'MODEL E_TABLE "',a,'". However the flows in ', &
               'these E_TABLES do not correspond.')
               go to 9800
             end if
           end do
           do j=1,noterm
             rotemp=dtable(io)%tdelay(j)
             rmtemp=dtable(im)%tdelay(j)
             rprecis=5*spacing(rmtemp)
             if((rotemp.lt.rmtemp-rprecis).or.(rotemp.gt.rmtemp+rprecis))then
               write(amessage,1071) trim(aoname),trim(amname)
1071           format('OBSERVATION_E_TABLE "',a,'"  has been matched to ', &
               'MODEL E_TABLE "',a,'". However the time delays in ', &
               'these E_TABLES do not correspond.')
               go to 9800
             end if
           end do
1079       continue
           do j=1,iodtable
             if(im.eq.outdtable(j)) go to 1078
           end do
           write(amessage,1037) 'D',trim(amname),trim(currentblock)
           go to 9800
1078       continue
         end do
       end if

! -- If present, the parameter group file is read.

       if(pargroupfile.eq.' ') go to 500
       call addquote(pargroupfile,astring)
       write(*,300) trim(astring)
       write(recunit,300) trim(astring)
300    format(t5,'Reading parameter group file ',a,' ....')
       iunit=nextunit()
       open(unit=iunit,file=pargroupfile,status='old',iostat=ierr)
       if(ierr.ne.0)then
         write(amessage,310) trim(astring)
310      format('cannot open parameter group file ',a)
         go to 9800
       end if

! -- The file is read a first time to find out the number of groups

       jline=0
       f_numpargp=0
       do
         jline=jline+1
         read(iunit,'(a)',err=9400,end=320) cline
         if(cline.eq.' ') cycle
         if(cline(1:1).eq.'#') cycle
         f_numpargp=f_numpargp+1
       end do
320    continue
       if(f_numpargp.eq.0)then
         write(amessage,322) trim(astring)
322      format('file ',a,' appears to contain no data.')
         go to 9800
       end if
       allocate(f_pargpnme(f_numpargp),f_inctyp(f_numpargp),f_derinc(f_numpargp), &
                f_derinclb(f_numpargp),f_forcen(f_numpargp),f_derincmul(f_numpargp), &
                f_dermthd(f_numpargp),stat=ierr)
       if(ierr.ne.0) go to 9200
       rewind(unit=iunit,iostat=ierr)
       if(ierr.ne.0) go to 9350

! -- Now it is read a second time to obtain the data.

       jline=0
       igp=0
325    jline=jline+1
       call num2char(jline,aline)
       READ(iunit,'(A)',ERR=9400,END=480) cline
       if(cline.eq.' ') go to 325
       if(cline(1:1).eq.'#') go to 325
       call casetrans(cline,'lo')
       call linesplit(ierr,7)
       if(ierr.ne.0) go to 9450
       atemp=cline(left_word(1):right_word(1))
       call remchar(atemp,'"')
       IF(len_trim(atemp).GT.12)THEN
         write(amessage,330) trim(atemp),trim(aline),trim(astring)
330      format('parameter group name "',a,'" greater than 12 characters ', &
         'at line ',a,' of file ',a)
         go to 9800
       end if
       igp=igp+1
       f_pargpnme(igp)=atemp
       IF(f_pargpnme(igp).EQ.'none') THEN
         write(amessage,340) trim(astring)
340      FORMAT('parameter group name "none" in file ',a,' is a reserved ', &
         'name, used for some fixed and tied parameters.')
         go to 9800
       END IF
       f_inctyp(igp)=cline(left_word(2):right_word(2))
       call remchar(f_inctyp(igp),'"')
       if((f_inctyp(igp).ne.'relative').and.(f_inctyp(igp).ne.'absolute').and.  &
          (f_inctyp(igp).ne.'rel_to_max'))then
          write(amessage,350) trim(aline),trim(astring)
350       format('INCTYP on line ',a,' of file ',a,' must be ',  &
          '"relative", "absolute" or "rel_to_max".')
          go to 9800
       end if
       call char2num(ierr,cline(left_word(3):right_word(3)),f_derinc(igp))
       if(ierr.ne.0)then
         write(amessage,590) 'DERINC',trim(aline),trim(astring)
         go to 9800
       end if
       if(f_derinc(igp).le.0.0)then
         write(amessage,370) 'DERINC',trim(aline),trim(astring)
370      format('value for ',a,' on line ',a,' of file ',a,' must be positive.')
         go to 9800
       end if
       call char2num(ierr,cline(left_word(4):right_word(4)),f_derinclb(igp))
       if(ierr.ne.0)then
         write(amessage,590) 'DERINCLB',trim(aline),trim(astring)
         go to 9800
       end if
       if(f_derinclb(igp).lt.0.0)then
         write(amessage,390) 'DERINCLB',trim(aline),trim(astring)
390      format('value for ',a,' on line ',a,' of file ',a,' must not be negative.')
         go to 9800
       end if
       f_forcen(igp)=cline(left_word(5):right_word(5))
       call remchar(f_forcen(igp),'"')
       if((f_forcen(igp).ne.'switch').and.(f_forcen(igp).ne.'always_2').and.  &
          (f_forcen(igp).ne.'always_3'))then
          write(amessage,400) trim(aline),trim(astring)
400       format('FORCEN must be "switch", "always_2" or "always_3" at line ',a,  &
          ' of file ',a)
          go to 9800
       end if
       call char2num(ierr,cline(left_word(6):right_word(6)),f_derincmul(igp))
       if(ierr.ne.0)then
         write(amessage,590) 'DERINCMUL',trim(aline),trim(astring)
         go to 9800
       end if
       if(f_derincmul(igp).le.0.0)then
         write(amessage,370) 'DERINCMUL',trim(aline),trim(astring)
         go to 9800
       end if
       f_dermthd(igp)=cline(left_word(7):right_word(7))
       call remchar(f_dermthd(igp),'"')
       if((f_dermthd(igp).ne.'parabolic').and.(f_dermthd(igp).ne.'best_fit')  &
          .and.(f_dermthd(igp).ne.'outside_pts'))then
          write(amessage,420) trim(aline),trim(astring)
420       format('DERMTHD must be "parabolic", "best_fit" or "outside_pts"',  &
          ' on line ',a,' of file ',a)
          go to 9800
       end if
       go to 325

480    continue

       if(f_numpargp.gt.1)then
         do i=1,f_numpargp-1
           do j=i+1,f_numpargp
             if(f_pargpnme(i).eq.f_pargpnme(j))then
               write(amessage,430) trim(astring)
430            format('2 parameter groups have the same name in file ',a)
               go to 9800
             end if
           end do
         end do
       end if

       call num2char(f_numpargp,aline)
       write(*,450) trim(aline),trim(astring)
       write(recunit,450) trim(aline),trim(astring)
450    format(t5,'- data for ',a,' parameter groups read from file ',a)
       close(unit=iunit)

500    continue

! -- If present, the parameter data file is read.

       if(pardatfile.eq.' ') go to 700
       call addquote(pardatfile,astring)
       write(*,510) trim(astring)
       write(recunit,510) trim(astring)
510    format(t5,'Reading parameter data file ',a,' ....')
       iunit=nextunit()
       open(unit=iunit,file=pardatfile,status='old',iostat=ierr)
       if(ierr.ne.0)then
         write(amessage,520) trim(astring)
520      format('cannot open parameter data file ',a)
         go to 9800
       end if

! -- The file is read a first time to obtain the number of parameters.

       jline=0
       f_numpar=0
       do
         jline=jline+1
         read(iunit,'(a)',err=9400,end=550) cline
         if(cline.eq.' ') cycle
         if(cline(1:1).eq.'#') cycle
         f_numpar=f_numpar+1
       end do
550    continue
       if(f_numpar.eq.0)then
         write(amessage,322) trim(astring)
         go to 9800
       end if
       allocate(f_parnme(f_numpar),f_partrans(f_numpar),f_parchglim(f_numpar), &
                f_parval1(f_numpar),f_parlbnd(f_numpar),f_parubnd(f_numpar), &
                f_pargp(f_numpar),f_scale(f_numpar),f_offset(f_numpar),stat=ierr)
       if(ierr.ne.0) go to 9200
       rewind(unit=iunit,iostat=ierr)
       if(ierr.ne.0) go to 9350

! -- Now it is read a second time to obtain the data.

       jline=0
       ipar=0
560    jline=jline+1
       call num2char(jline,aline)
       read(iunit,'(A)',ERR=9400,END=620) cline
       if(cline.eq.' ') go to 560
       if(cline(1:1).eq.'#') go to 560
       call casetrans(cline,'lo')
       call linesplit(ierr,9)
       if(ierr.ne.0) go to 9450
       atemp=cline(left_word(1):right_word(1))
       call remchar(atemp,'"')
       IF(len_trim(atemp).GT.12)THEN
         write(amessage,565) trim(atemp),trim(aline),trim(astring)
565      format('parameter name "',a,'" greater than 12 characters in length ', &
         'at line ',a,' of file ',a)
         go to 9800
       end if
       ipar=ipar+1
       f_parnme(ipar)=atemp
       f_partrans(ipar)=cline(left_word(2):right_word(2))
       call remchar(f_partrans(ipar),'"')
       if((f_partrans(ipar).ne.'log').and.(f_partrans(ipar).ne.'none').and.  &
          (f_partrans(ipar)(1:4).ne.'tied').and.(f_partrans(ipar).ne.'fixed'))then
          write(amessage,570) trim(aline),trim(astring)
570       format('PARTRANS on line ',a,' of file ',a,' must be ',  &
          '"none", "log", "fixed" or "tied_(parameter name)".')
          go to 9800
       end if
       if((f_partrans(ipar).eq.'tied').or.(f_partrans(ipar).eq.'tied_'))then
         write(amessage,572) trim(aline),trim(astring)
572      format('the parent parameter name must follow the "tied_" string at line ',a,  &
         ' of file ',a)
         go to 9800
       end if
       f_parchglim(ipar)=cline(left_word(3):right_word(3))
       call remchar(f_parchglim(ipar),'"')
       if((f_parchglim(ipar).ne.'relative').and.(f_parchglim(ipar).ne.'factor'))then
          write(amessage,580) trim(aline),trim(astring)
580       format('PARCHGLIM on line ',a,' of file ',a,' must be ',  &
          '"relative" or "factor".')
          go to 9800
       end if
       call char2num(ierr,cline(left_word(4):right_word(4)),f_parval1(ipar))
       if(ierr.ne.0)then
         write(amessage,590) 'PARVAL1',trim(aline),trim(astring)
590      format('cannot read value for ',a,' on line ',a,' of file ',a)
         go to 9800
       end if
       call char2num(ierr,cline(left_word(5):right_word(5)),f_parlbnd(ipar))
       if(ierr.ne.0)then
         write(amessage,590) 'PARLBND',trim(aline),trim(astring)
         go to 9800
       end if
       call char2num(ierr,cline(left_word(6):right_word(6)),f_parubnd(ipar))
       if(ierr.ne.0)then
         write(amessage,590) 'PARUBND',trim(aline),trim(astring)
         go to 9800
       end if
       atemp=cline(left_word(7):right_word(7))
       call remchar(atemp,'"')
       if(len_trim(atemp).GT.12)then
         write(amessage,330) trim(atemp),trim(aline),trim(astring)
         go to 9800
       end if
       f_pargp(ipar)=atemp
       call char2num(ierr,cline(left_word(8):right_word(8)),f_scale(ipar))
       if(ierr.ne.0)then
         write(amessage,590) 'SCALE',trim(aline),trim(astring)
         go to 9800
       end if
       call char2num(ierr,cline(left_word(9):right_word(9)),f_offset(ipar))
       if(ierr.ne.0)then
         write(amessage,590) 'OFFSET',trim(aline),trim(astring)
         go to 9800
       end if
       go to 560

620    continue

! -- Some checks are made of the parameter data.

       if(f_numpar.gt.1)then
         do i=1,f_numpar-1
           do j=i+1,f_numpar
             if(f_parnme(i).eq.f_parnme(j))then
               write(amessage,630) trim(astring)
630            format('2 parameters have the same name in file ',a)
               go to 9800
             end if
           end do
         end do
       end if

! -- If any parameters are tied, parameter linkages are now read.

       do ipar=1,f_numpar
         if(f_partrans(ipar)(1:4).eq.'tied')then
           atemp=f_partrans(ipar)(6:)
           if(atemp.eq.f_parnme(ipar))then
             write(amessage,635) trim(atemp),trim(astring)
635          format('parameter "',a,'" is tied to itself in file ',a)
             go to 9800
           end if
         end if
       end do

       call num2char(f_numpar,aline)
       write(*,640) trim(aline),trim(astring)
       write(recunit,640) trim(aline),trim(astring)
640    format(t5,'- data for ',a,' parameters read from file ',a)
       close(unit=iunit)

700    continue

! -- Next the names of all parameters are ascertained by reading template files.

        numtempfile=itempfile
	npar=0
	read_template_file: do itempfile=1,numtempfile
	  nnpar=0
          tempunit=nextunit()
          call addquote(tempfile(itempfile),astring)
          write(*,710) trim(astring)
          write(recunit,710) trim(astring)
710       format(t5,'Reading template file ',a,' ....')
          open(unit=tempunit,file=tempfile(itempfile),status='old',iostat=ierr)
          if(ierr.ne.0)then
            write(amessage,720) trim(astring)
720         format('cannot open template file ',a)
            go to 9800
          end if
          jline=1
	  read(tempunit,'(a)',err=9400,end=800) cline
          call casetrans(cline,'lo')
	  if(cline(1:3).ne.'ptf')then
	    write(amessage,730) trim(astring)
730	    format('"ptf" header missing from first line of file ',a)
            go to 9800
	  end if
	  pardelim=cline(5:5)
	  if((pardelim.eq.' ').or.   &
	     (index('1234567890,;:',pardelim).ne.0).or.    &
	     (index('abcdefghijklmnopqrstuvwxyz',pardelim).ne.0))then
	     write(amessage,740) trim(astring)
740	     format('invalid parameter delimeter on line 1 of file ',a)
             go to 9800
	  end if
	  read_a_line: do
	    ii1=1
	    jline=jline+1
	    read(tempunit,'(a)',err=9400,end=800) cline
	    ll=len(cline)
745	    j=index(cline(ii1:),pardelim)
	    if(j.eq.0) cycle read_a_line
	    if(j.gt.ll) cycle read_a_line
	    ii1=ii1+j-1
	    j=0
	    if(ii1.le.ll)j=index(cline(ii1+1:),pardelim)
	    if(j.eq.0)then
	      call num2char(jline,aline)
	      write(amessage,750) trim(aline),trim(astring)
750	      format('unbalanced parameter delimiters on line ',a,  &
	      ' of template file ',a)
	      go to 9800
	    end if
	    jj1=ii1+j
	    ii1=ii1+1
	    jj1=jj1-1
	    if(jj1-ii1+1.le.0)then
	      call num2char(jline,aline)
	      write(amessage,760) trim(aline),trim(astring)
760	      format('parameter space has zero width at line ',a,   &
	      ' of template file ',a)
	      go to 9800
	    end if
	    do jj=ii1,jj1
	      if(cline(jj:jj).ne.' ') then
	        do kk=jj,jj1
	          if(cline(kk:kk).eq.' ') go to 765
	        end do
	        kk=jj1+1
765	        kk=kk-1
	        go to 767
	      end if
	    end do
	    call num2char(jline,aline)
	    write(amessage,766) trim(aline), trim(astring)
766	    format('blank parameter space at line ',a,' of template ', &
	    'file ',a)
	    go to 9800
767	    continue
	    if(kk-jj+1.gt.12)then
	      call num2char(jline,aline)
	      write(amessage,768) trim(aline),trim(astring)
768	      format('parameter name greater than 12 characters in ',  &
	      'line ',a,' of template file ',a)
	      go to 9800
	    end if
            if(cline(kk+1:jj1).ne.' ')then
              call num2char(jline,aline)
              write(amessage,769) trim(aline),trim(astring)
769           format('parameter name includes a space character at line ',a,  &
              ' of file ',a)
              go to 9800
            end if
	    aapar=cline(jj:kk)
	    aapar=adjustl(aapar)
	    call casetrans(aapar,'lo')
	    if(npar.ne.0)then
	      do ipar=1,npar
	        if(aapar.eq.apar(ipar)) go to 785
	      end do
	      npar=npar+1
	      nnpar=nnpar+1
	      if(npar.gt.MAXPAR)then
                call num2char(MAXPAR,aline)
	        write(amessage,780) trim(aline)
780	        format('number of parameters cited in template files is limited ', &
                'to ',a,'. Increase MAXPAR and re-compile program.')
	        go to 9800
	      end if
	      apar(npar)=aapar
	    else
	      npar=1
	      nnpar=1
	      apar(npar)=aapar
	    end if
785	    ii1=jj1+2
	    go to 745
	  end do read_a_line
800	  continue
	  call num2char(nnpar,aline)
          if(itempfile.eq.1)then
	    write(*,795) trim(aline),trim(astring)
            write(recunit,795) trim(aline),trim(astring)
795	    format(t5,'- ',a,' parameter names read from file ',a)
          else
	    write(*,796) trim(aline),trim(astring)
            write(recunit,796) trim(aline),trim(astring)
796	    format(t5,'- ',a,' more parameter names read from file ',a)
          end if
	  close(unit=tempunit,err=9500)
	end do read_template_file

! -- Observations are named and the instruction file is now written.

       nobs=0
       nobsgp=0

       iunit=nextunit()
       call addquote(instructfile,astring)
       write(*,810) trim(astring)
       write(recunit,810) trim(astring)
810    format(t5,'Writing instruction file ',a,' ....')
       inquire(file=instructfile,exist=lexist)
       if(lexist)then
812      write(6,*)
813      write(*,815,advance='no') trim(astring)
815      format(' File ',a,' already exists. Overwrite it? [y/n]: ')
         read(5,'(a)') aa
         call casetrans(aa,'lo')
         if((aa.ne.'y').and.(aa.ne.'n')) go to 813
         if(aa.eq.'n')then
           write(*,820)
           write(recunit,820)
820        format(/,' Execution terminated so file not overwritten.')
           ifail=1
           return
         end if
       end if
       open(unit=iunit,file=instructfile,iostat=ierr)
       if(ierr.ne.0)then
         write(amessage,830) trim(astring)
830      format('cannot open file ',a,' for output.')
         go to 9800
       end if
       write(iunit,840)
840    format('pif $')

! -- First the time series instructions are written.

       iout=0
       if(ioseries.eq.0) go to 1100
       do i=1,ioseries
         iout=iout+1
         im=outseries(i)
         do j=1,ioseries
           if(im.eq.modseries(j)) go to 860
         end do
         write(amessage,850) trim(series(im)%name)
850      format('time series "',a,'" cited in the LIST_OUTPUT block immediately ', &
         'preceding the WRITE_PEST_FILES block is not cited as a ', &
         'MODEL_SERIES_NAME in the latter block.')
         go to 9800
860      io=obsseries(j)
         nsterm=series(io)%nterm
         aname=series(im)%name
         nobsgp=nobsgp+1
         obgnme(nobsgp)=aname
         call make_basename(ierr,iout,nsterm,aname,basename)
         if(ierr.ne.0) go to 9800
         atemp=basename(iout)
         do iterm=1,nsterm
           call num2char(iterm,anum)
           if(series_format.eq.'long')then
             aname='['//trim(atemp)//trim(anum)//']37:55'
           else
             aname='['//trim(atemp)//trim(anum)//']2:20'
           end if
           if(iterm.eq.1)then
             write(iunit,880) trim(aname)
880          format('l3',t6,a)
           else
             write(iunit,890) trim(aname)
890          format('l1',t6,a)
           end if
           nobs=nobs+1
         end do
       end do

! -- Next the S_TABLE instructions are written.

1100   continue
       if(iostable.eq.0) go to 1200
       siout=0
       do i=1,iostable
         il=0
         siout=siout+1
         im=outstable(i)
         do j=1,iostable
           if(im.eq.modstable(j)) go to 1120
         end do
         write(amessage,1110) 's',trim(stable(im)%name),'S'
1110     format(a,'_table "',a,'" cited in the LIST_OUTPUT block immediately ', &
         'preceding the WRITE_PEST_FILES block is not cited as a ', &
         'MODEL_',a,'_TABLE_NAME in the latter block.')
         go to 9800
1120     io=obsstable(j)
         aname=stable(im)%name
         nobsgp=nobsgp+1
         obgnme(nobsgp)=aname
         sbasename(siout)=aname(1:12)
         if(siout.gt.1)then
           do j=1,siout-1
             if(sbasename(j).eq.sbasename(siout))then
               write(amessage,1130)
1130           format('TSPROC cannot generate unique observation names from the ',  &
               'names of the MODEL_S_TABLES involved in the ', &
               'calibration process. Alter the first twelve letters of at least one ', &
               'of the model S_TABLE names.')
               go to 9800
             end if
           end do
         end if
         if(stable(io)%maximum.gt.-1.0e36)then
           il=il+1
           aname='['//trim(sbasename(siout))//OBSCHAR//'max]51:69'
           if(il.eq.1)then
             write(iunit,1140) trim(aname)
1140         format('l11',t6,a)
           else
             write(iunit,1150) trim(aname)
1150         format('l1',t6,a)
           end if
           nobs=nobs+1
         end if
         if(stable(io)%minimum.gt.-1.0e36)then
           il=il+1
           aname='['//trim(sbasename(siout))//OBSCHAR//'min]51:69'
           if(il.eq.1)then
             write(iunit,1140) trim(aname)
           else
             write(iunit,1150) trim(aname)
           end if
           nobs=nobs+1
         end if
         if(stable(io)%range.gt.-1.0e36)then
           il=il+1
           aname='['//trim(sbasename(siout))//OBSCHAR//'range]51:69'
           if(il.eq.1)then
             write(iunit,1140) trim(aname)
           else
             write(iunit,1150) trim(aname)
           end if
           nobs=nobs+1
         end if

         if(stable(io)%total.gt.-1.0e36)then
           il=il+1
           aname='['//trim(sbasename(siout))//OBSCHAR//'sum]51:69'
           if(il.eq.1)then
             write(iunit,1140) trim(aname)
           else
             write(iunit,1150) trim(aname)
           end if
           nobs=nobs+1
         end if
         if(stable(io)%mean.gt.-1.0e36)then
           il=il+1
           aname='['//trim(sbasename(siout))//OBSCHAR//'mean]51:69'
           if(il.eq.1)then
             write(iunit,1140) trim(aname)
           else
             write(iunit,1150) trim(aname)
           end if
           nobs=nobs+1
         end if
         if(stable(io)%stddev.gt.-1.0e36)then
           il=il+1
           aname='['//trim(sbasename(siout))//OBSCHAR//'sd]51:69'
           if(il.eq.1)then
             write(iunit,1140) trim(aname)
           else
             write(iunit,1150) trim(aname)
           end if
           nobs=nobs+1
         end if
       end do

! -- Next the V_TABLE instructions are written.

1200   continue

       if(iovtable.eq.0) go to 1300
       do i=1,iovtable
         iout=iout+1
         im=outvtable(i)
         do j=1,iovtable
           if(im.eq.modvtable(j)) go to 1220
         end do
         write(amessage,1110) 'v',trim(vtable(im)%name),'V'
         go to 9800
1220     io=obsvtable(j)
         nsterm=vtable(io)%nterm
         aname=vtable(im)%name
         nobsgp=nobsgp+1
         obgnme(nobsgp)=aname
         call make_basename(ierr,iout,nsterm,aname,basename)
         if(ierr.ne.0) go to 9800
         atemp=basename(iout)
         do iterm=1,nsterm
           call num2char(iterm,anum)
           aname='['//trim(atemp)//trim(anum)//']62:81'
           if(iterm.eq.1)then
             write(iunit,1230) trim(aname)
1230         format('l4',t6,a)
           else
             write(iunit,1240) trim(aname)
1240         format('l1',t6,a)
           end if
           nobs=nobs+1
         end do
       end do

! -- Next the E_TABLE instructions are written.

1300   continue

       if(iodtable.eq.0) go to 1400
       do i=1,iodtable
         iout=iout+1
         im=outdtable(i)
         do j=1,iodtable
           if(im.eq.moddtable(j)) go to 1320
         end do
         write(amessage,1110) 'e',trim(vtable(im)%name),'E'
         go to 9800
1320     io=obsdtable(j)
         nsterm=dtable(io)%nterm
         aname=dtable(im)%name
         nobsgp=nobsgp+1
         obgnme(nobsgp)=aname
         call make_basename(ierr,iout,nsterm,aname,basename)
         if(ierr.ne.0) go to 9800
         atemp=basename(iout)
         do iterm=1,nsterm
           call num2char(iterm,anum)
           aname='['//trim(atemp)//trim(anum)//']59:78'
           if(iterm.eq.1)then
             write(iunit,1230) trim(aname)
           else
             write(iunit,1240) trim(aname)
           end if
           nobs=nobs+1
         end do
       end do

1400   continue
       close(unit=iunit)
       write(*,1410) trim(astring)
       write(recunit,1410) trim(astring)
1410   format(t5,'- file ',a,' written ok.')


! -- Parameter and parameter group data are now assimilated on the basis of information
!    read from the parameter data file, the parameter group file and the template files.

       allocate(partrans(npar),parchglim(npar),parval1(npar),parlbnd(npar),  &
                parubnd(npar),pargp(npar),scale(npar),offset(npar), stat=ierr)
       if(ierr.ne.0) go to 9200

       allocate(pargpnme(npar),inctyp(npar),derinc(npar),derinclb(npar),forcen(npar), &
       derincmul(npar),dermthd(npar), stat=ierr)
       if(ierr.ne.0) go to 9200

       do ipar=1,npar
         aapar=apar(ipar)
         if(f_numpar.ne.0)then
           do j=1,f_numpar
             if(aapar.eq.f_parnme(j))then
               partrans(ipar)=f_partrans(j)
               parchglim(ipar)=f_parchglim(j)
               parval1(ipar)=f_parval1(j)
               parlbnd(ipar)=f_parlbnd(j)
               parubnd(ipar)=f_parubnd(j)
               pargp(ipar)=f_pargp(j)
               scale(ipar)=f_scale(j)
               offset(ipar)=f_offset(j)
               go to 1450
             end if
           end do
         end if
         partrans(ipar)='log'
         parchglim(ipar)='factor'
         parval1(ipar)=1.0
         parlbnd(ipar)=1.0e-10
         parubnd(ipar)=1e10
         pargp(ipar)=aapar
         scale(ipar)=1.0
         offset(ipar)=0.0
1450     continue
       end do

! -- If any parameters are tied to a parameter which does not exist, this is now
!    rectified.

       do ipar=1,npar
         if(partrans(ipar)(1:4).eq.'tied') then
           aapar=partrans(ipar)(6:)
           do i=1,npar
             if(aapar.eq.apar(i)) go to 1470
           end do
           partrans(ipar)='none'
1470       continue
         end if
       end do

! -- Parameter groups are now organised.

       npargp=0
       do ipar=1,npar
         apargp=pargp(ipar)
         if(apargp.eq.'none') then
           if((partrans(ipar).ne.'tied').and.(partrans(ipar).ne.'fixed'))then
             call addquote(pardatfile,astring)
              write(amessage,1471)trim(apar(ipar)),trim(astring)
1471         format('parameter "',a,'" has been assigned to parameter group "none" ', &
             'in file ',a,' but is not tied or fixed.')
             go to 9800
           else
             go to 1500
           end if
         end if
         if(ipar.ne.1)then
           do i=1,ipar-1
             if(pargp(i).eq.apargp) go to 1500
           end do
         end if
         if(f_numpargp.ne.0)then
           do i=1,f_numpargp
             if(apargp.eq.f_pargpnme(i))then
               npargp=npargp+1
               pargpnme(npargp)=f_pargpnme(i)
               inctyp(npargp)=f_inctyp(i)
               derinc(npargp)=f_derinc(i)
               derinclb(npargp)=f_derinclb(i)
               forcen(npargp)=f_forcen(i)
               derincmul(npargp)=f_derincmul(i)
               dermthd(npargp)=f_dermthd(i)
               go to 1500
             end if
           end do
         end if
         npargp=npargp+1
         pargpnme(npargp)=apargp
         inctyp(npargp)='relative'
         derinc(npargp)=0.01
         derinclb(npargp)=0.00
         forcen(npargp)='switch'
         derincmul(npargp)=2.0
         dermthd(npargp)='parabolic'
1500     continue
       end do

! -- The "* control data" section of the PEST control file is now written.

       iunit=nextunit()
       call addquote(pestctlfile,astring)
       write(*,1510) trim(astring)
       write(recunit,1510) trim(astring)
1510   format(t5,'Writing PEST control file ',a,' ....')
       inquire(file=pestctlfile,exist=lexist)
       if(lexist)then
         write(6,*)
1520     write(*,815,advance='no') trim(astring)
         read(5,'(a)') aa
         call casetrans(aa,'lo')
         if((aa.ne.'y').and.(aa.ne.'n')) go to 1520
         if(aa.eq.'n')then
           write(*,820)
           write(recunit,820)
           ifail=1
           return
         end if
       end if
       open(unit=iunit,file=pestctlfile,iostat=ierr)
       if(ierr.ne.0)then
         write(amessage,830) trim(astring)
         go to 9800
       end if
       write(iunit,1530)
1530   format('pcf')
       write(iunit,1540)
1540   format('* control data')
       write(iunit,1550)
1550   format('restart estimation')
       write(iunit,1560) npar,nobs,npargp,0,nobsgp
1560   format(5i7)
       write(iunit,1570) numtempfile,1
1570   format(2i6,'   single   point   1   0   0')
       if(isvd.eq.0)then
         write(iunit,1580)
1580     format('5.0   2.0    0.3    0.03    10  999')
       else
         write(iunit,1581)
1581     format(' 1e-1   -4.0   0.3  0.03    10	    999')
       end if
       write(iunit,1590)
1590   format('5.0   5.0   1.0e-3')
       if(auiyesno.eq.0)then
         write(iunit,1600)
1600     format('0.1  noaui')
       else
         write(iunit,1601)
1601   format('0.1   aui')
       end if
       write(iunit,1610)
1610   format('30   .005  4   4  .005   4')
       write(iunit,1620)
1620   format('1    1    1')
       if(isvd.eq.1)then
         write(iunit,1621)
1621     format('* singular value decomposition')
         write(iunit,1622)
1622     format('1')
         write(iunit,1633) npar,eigthresh
1633     format(i6,2x,1pg13.7)
         write(iunit,1634)
1634     format('0')
       end if

! -- The "* parameter groups" section of the PEST control file is now written.

       write(iunit,1630)
1630   format('* parameter groups')
       do igp=1,npargp
         write(iunit,1640)trim(pargpnme(igp)),trim(inctyp(igp)),derinc(igp), &
         derinclb(igp),trim(forcen(igp)),derincmul(igp), trim(dermthd(igp))
1640     format(a,t14,a,t27,1pg10.4,t39,1pg10.4,t51,a,t62,1pg10.4,2x,a)
       end do

! -- The "* parameter data" section of the PEST control file is now written.

       write(iunit,1650)
1650   format('* parameter data')
       do ipar=1,npar
         if(partrans(ipar)(1:4).eq.'tied')then
           atrans='tied'
         else
           atrans=partrans(ipar)
         end if
         write(iunit,1660) trim(apar(ipar)),trim(atrans),   &
         trim(parchglim(ipar)),parval1(ipar), &
         parlbnd(ipar),parubnd(ipar),trim(pargp(ipar)),scale(ipar),offset(ipar)
1660     format(a,t14,a,t21,a,t33,1pg12.5,t47,1pg12.5,t61,1pg12.5,t75,a,t89,1pg10.4,  &
         t101,1pg10.4,t113,'  1')
       end do
       do ipar=1,npar
         if(partrans(ipar)(1:4).eq.'tied')then
           write(iunit,1670) trim(apar(ipar)),trim(partrans(ipar)(6:))
1670       format(a,t14,a)
         end if
       end do

! -- The "* observation groups" section of the PEST control file is now written.

       write(iunit,1690)
1690   format('* observation groups')
       do i=1,nobsgp
         write(iunit,1700) trim(obgnme(i))
1700     format(a)
       end do

! -- The "* observation data" section of the PEST control file is now written.
! -- First the time series observations are dealt with.

       write(iunit,1705)
1705   format('* observation data')

       iout=0
       ieqnerr=0
       if(ioseries.eq.0) go to 2100
       do i=1,ioseries
         iout=iout+1
         im=outseries(i)
         do j=1,ioseries
           if(im.eq.modseries(j)) go to 1860
         end do
         write(amessage,850)
         go to 9800
1860     io=obsseries(j)
         nsterm=series(io)%nterm
         aname=series(im)%name
         call make_basename(ierr,iout,nsterm,aname,basename)
         atemp=basename(iout)
         weightmin=max(sweightmin(j),0.0)
         weightmax=min(sweightmax(j),1.0e36)

! -- The pertinent equation is parsed and prepared.

         eqntext=sequation(j)
         call prepare_eqn(ierr,nterm,sequation(j),io)
         if(ierr.ne.0) then
           ieqnerr=1
           go to 9800
         end if
         nnterm=nterm
         do iterm=1,nterm
           cterm(iterm)=aterm(iterm)
         end do
         do iterm=1,nterm
           qterm(iterm)=rterm(iterm)
         end do
         do j=1,nsterm
           nterm=nnterm
           do iterm=1,nterm
             aterm(iterm)=cterm(iterm)
           end do
           do iterm=1,nterm
             rterm(iterm)=qterm(iterm)
           end do
           call num2char(j,anum)
           aname=trim(atemp)//trim(anum)

! -- First the series numbers in the equation terms are replaced by series values.

           do iterm =1,nterm
             if(aterm(iterm)(1:3).eq.'$~$') then
               call char2num(ierr,aterm(iterm)(4:),isnum)
               rterm(iterm)=series(isnum)%val(j)
               aterm(iterm)='~!~'
             end if
           end do

! -- The weights equation instinsic function evaluations is carried out if necessary.

           do iterm =1,nterm
             if(aterm(iterm)(1:3).eq.'@_2') then
               rterm(iterm)=abs(series(io)%val(j))
               aterm(iterm)='~!~'
             else if(aterm(iterm)(1:3).eq.'@_1') then
               call newdate(series(io)%days(j),1,1,1970,dd,mm,yy)
               nn=numdays(1,1,yy,dd,mm,yy)
               rtime=float(nn)+float(series(io)%secs(j))/86400.0
               rterm(iterm)=rtime
               aterm(iterm)='~!~'
             else if(aterm(iterm)(1:3).eq.'@_3') then
               call char2num(ierr,aterm(iterm)(5:),dtempx)
               rterm(iterm)=dble(series(io)%days(j))+     &
                            dble(series(io)%secs(j))/86400.0d0-dtempx
               aterm(iterm)='~!~'
             end if
           end do

           call EVALUATE(ierr,MAXTERM,NTERM,NOPER,NFUNCT,ATERM,BTERM,   &
           OPERAT,FUNCT,IORDER,DVAL,rterm)
           if(ierr.ne.0) go to 9800
           if(dval.lt.weightmin)dval=weightmin
           if(dval.gt.weightmax)dval=weightmax
           write(iunit,1900) trim(aname),series(io)%val(j),dval,trim(series(im)%name)
1900       format(a,t22,1pg14.7,t40,1pg12.6,2x,a)
         end do
       end do

! -- Now we handle S_TABLE observations.

2100   continue
       if(iostable.eq.0) go to 2200
       siout=0
       do i=1,iostable
         siout=siout+1
         im=outstable(i)
         do j=1,iostable
           if(im.eq.modstable(j)) go to 2120
         end do
         write(amessage,1110) 's',trim(stable(im)%name),'S'
         go to 9800
2120     io=obsstable(j)
         aname=stable(im)%name
         sbasename(siout)=aname(1:12)
         weightmin=max(stweightmin(j),0.0)
         weightmax=min(stweightmax(j),1.0e36)
         eqntext=stequation(j)
         call prepare_eqn(ierr,nterm,stequation(j),0)
         if(ierr.ne.0) then
           ieqnerr=1
           go to 9800
         end if
         nnterm=nterm
         do iterm=1,nterm
           cterm(iterm)=aterm(iterm)
         end do
         do iterm=1,nterm
           qterm(iterm)=rterm(iterm)
         end do

         if(stable(io)%maximum.gt.-1.0e36)then
           aname=trim(sbasename(siout))//OBSCHAR//'max'
           nterm=nnterm
           do iterm=1,nterm
             aterm(iterm)=cterm(iterm)
           end do
           do iterm=1,nterm
             rterm(iterm)=qterm(iterm)
           end do
           do iterm =1,nterm
             if(aterm(iterm)(1:3).eq.'@_2') then
               rterm(iterm)=abs(stable(io)%maximum)
               aterm(iterm)='~!~'
             end if
           end do
           call EVALUATE(ierr,MAXTERM,NTERM,NOPER,NFUNCT,ATERM,BTERM,   &
           OPERAT,FUNCT,IORDER,DVAL,rterm)
           if(dval.lt.weightmin)dval=weightmin
           if(dval.gt.weightmax)dval=weightmax
           write(iunit,1900) trim(aname),stable(io)%maximum,dval,trim(stable(im)%name)
         end if

         if(stable(io)%minimum.gt.-1.0e36)then
           aname=trim(sbasename(siout))//OBSCHAR//'min'
           nterm=nnterm
           do iterm=1,nterm
             aterm(iterm)=cterm(iterm)
           end do
           do iterm=1,nterm
             rterm(iterm)=qterm(iterm)
           end do
           do iterm =1,nterm
             if(aterm(iterm)(1:3).eq.'@_2') then
               rterm(iterm)=abs(stable(io)%minimum)
               aterm(iterm)='~!~'
             end if
           end do
           call EVALUATE(ierr,MAXTERM,NTERM,NOPER,NFUNCT,ATERM,BTERM,   &
           OPERAT,FUNCT,IORDER,DVAL,rterm)
           if(dval.lt.weightmin)dval=weightmin
           if(dval.gt.weightmax)dval=weightmax
           write(iunit,1900) trim(aname),stable(io)%minimum,dval,trim(stable(im)%name)
         end if

         if(stable(io)%range.gt.-1.0e36)then
           aname=trim(sbasename(siout))//OBSCHAR//'range'
           nterm=nnterm
           do iterm=1,nterm
             aterm(iterm)=cterm(iterm)
           end do
           do iterm=1,nterm
             rterm(iterm)=qterm(iterm)
           end do
           do iterm =1,nterm
             if(aterm(iterm)(1:3).eq.'@_2') then
               rterm(iterm)=abs(stable(io)%range)
               aterm(iterm)='~!~'
             end if
           end do
           call EVALUATE(ierr,MAXTERM,NTERM,NOPER,NFUNCT,ATERM,BTERM,   &
           OPERAT,FUNCT,IORDER,DVAL,rterm)
           if(dval.lt.weightmin)dval=weightmin
           if(dval.gt.weightmax)dval=weightmax
           write(iunit,1900) trim(aname),stable(io)%range,dval,trim(stable(im)%name)
         end if

         if(stable(io)%total.gt.-1.0e36)then
           aname=trim(sbasename(siout))//OBSCHAR//'sum'
           nterm=nnterm
           do iterm=1,nterm
             aterm(iterm)=cterm(iterm)
           end do
           do iterm=1,nterm
             rterm(iterm)=qterm(iterm)
           end do
           do iterm =1,nterm
             if(aterm(iterm)(1:3).eq.'@_2') then
               rterm(iterm)=abs(stable(io)%total)
               aterm(iterm)='~!~'
             end if
           end do
           call EVALUATE(ierr,MAXTERM,NTERM,NOPER,NFUNCT,ATERM,BTERM,   &
           OPERAT,FUNCT,IORDER,DVAL,rterm)
           if(dval.lt.weightmin)dval=weightmin
           if(dval.gt.weightmax)dval=weightmax
           write(iunit,1900) trim(aname),stable(io)%total,dval,trim(stable(im)%name)
         end if

         if(stable(io)%mean.gt.-1.0e36)then
           aname=trim(sbasename(siout))//OBSCHAR//'mean'
           nterm=nnterm
           do iterm=1,nterm
             aterm(iterm)=cterm(iterm)
           end do
           do iterm=1,nterm
             rterm(iterm)=qterm(iterm)
           end do
           do iterm =1,nterm
             if(aterm(iterm)(1:3).eq.'@_2') then
               rterm(iterm)=abs(stable(io)%mean)
               aterm(iterm)='~!~'
             end if
           end do
           call EVALUATE(ierr,MAXTERM,NTERM,NOPER,NFUNCT,ATERM,BTERM,   &
           OPERAT,FUNCT,IORDER,DVAL,rterm)
           if(dval.lt.weightmin)dval=weightmin
           if(dval.gt.weightmax)dval=weightmax
           write(iunit,1900) trim(aname),stable(io)%mean,dval,trim(stable(im)%name)
         end if

         if(stable(io)%stddev.gt.-1.0e36)then
           aname=trim(sbasename(siout))//OBSCHAR//'sd'
           nterm=nnterm
           do iterm=1,nterm
             aterm(iterm)=cterm(iterm)
           end do
           do iterm=1,nterm
             rterm(iterm)=qterm(iterm)
           end do
           do iterm =1,nterm
             if(aterm(iterm)(1:3).eq.'@_2') then
               rterm(iterm)=abs(stable(io)%stddev)
               aterm(iterm)='~!~'
             end if
           end do
           call EVALUATE(ierr,MAXTERM,NTERM,NOPER,NFUNCT,ATERM,BTERM,   &
           OPERAT,FUNCT,IORDER,DVAL,rterm)
           if(dval.lt.weightmin)dval=weightmin
           if(dval.gt.weightmax)dval=weightmax
           write(iunit,1900) trim(aname),stable(io)%stddev,dval,trim(stable(im)%name)
         end if

       end do

! -- Next the V_TABLE observations are handled.

2200   continue
       if(iovtable.eq.0) go to 2300
       do i=1,iovtable
         iout=iout+1
         im=outvtable(i)
         do j=1,iovtable
           if(im.eq.modvtable(j)) go to 2220
         end do
         write(amessage,1110) 'v',trim(vtable(im)%name),'V'
         go to 9800
2220     io=obsvtable(j)
         nsterm=vtable(io)%nterm
         aname=vtable(im)%name
         call make_basename(ierr,iout,nsterm,aname,basename)
         if(ierr.ne.0) go to 9800
         atemp=basename(iout)
         weightmin=max(vtweightmin(j),0.0)
         weightmax=min(vtweightmax(j),1.0e36)
         eqntext=vtequation(j)
         call prepare_eqn(ierr,nterm,vtequation(j),0)
         if(ierr.ne.0) then
           ieqnerr=1
           go to 9800
         end if
         nnterm=nterm
         do iterm=1,nterm
           cterm(iterm)=aterm(iterm)
         end do
         do iterm=1,nterm
           qterm(iterm)=rterm(iterm)
         end do
         do j=1,nsterm
           nterm=nnterm
           do iterm=1,nterm
             aterm(iterm)=cterm(iterm)
           end do
           do iterm=1,nterm
             rterm(iterm)=qterm(iterm)
           end do
           call num2char(j,anum)
           aname=trim(atemp)//trim(anum)
           do iterm =1,nterm
             if(aterm(iterm)(1:3).eq.'@_2') then
               rterm(iterm)=abs(vtable(io)%vol(j))
               aterm(iterm)='~!~'
             end if
           end do
           call EVALUATE(ierr,MAXTERM,NTERM,NOPER,NFUNCT,ATERM,BTERM,   &
           OPERAT,FUNCT,IORDER,DVAL,rterm)
           if(dval.lt.weightmin)dval=weightmin
           if(dval.gt.weightmax)dval=weightmax
           write(iunit,1900) trim(aname),vtable(io)%vol(j),dval,trim(vtable(im)%name)
         end do
       end do

! -- Next the E_TABLE observations are handled.

2300   continue
       if(iodtable.eq.0) go to 2400
       do i=1,iodtable
         iout=iout+1
         im=outdtable(i)
         do j=1,iodtable
           if(im.eq.moddtable(j)) go to 2320
         end do
         write(amessage,1110) 'e',trim(vtable(im)%name),'E'
         go to 9800
2320     io=obsdtable(j)
         totim=dtable(io)%total_time
         nsterm=dtable(io)%nterm
         aname=dtable(im)%name
         call make_basename(ierr,iout,nsterm,aname,basename)
         if(ierr.ne.0) go to 9800
         atemp=basename(iout)
         weightmin=max(dtweightmin(j),0.0)        !chek
         weightmax=min(dtweightmax(j),1.0e36)
         eqntext=dtequation(j)
         call prepare_eqn(ierr,nterm,dtequation(j),0)
         if(ierr.ne.0) then
           ieqnerr=1
           go to 9800
         end if
         nnterm=nterm
         do iterm=1,nterm
           cterm(iterm)=aterm(iterm)
         end do
         do iterm=1,nterm
           qterm(iterm)=rterm(iterm)
         end do
         do j=1,nsterm
           nterm=nnterm
           do iterm=1,nterm
             aterm(iterm)=cterm(iterm)
           end do
           do iterm=1,nterm
             rterm(iterm)=qterm(iterm)
           end do
           call num2char(j,anum)
           aname=trim(atemp)//trim(anum)
           do iterm =1,nterm
             if(aterm(iterm)(1:3).eq.'@_2') then
               rterm(iterm)=abs(dtable(io)%time(j)/totim)
               aterm(iterm)='~!~'
             end if
           end do
           call EVALUATE(ierr,MAXTERM,NTERM,NOPER,NFUNCT,ATERM,BTERM,   &
           OPERAT,FUNCT,IORDER,DVAL,rterm)
           if(dval.lt.weightmin)dval=weightmin
           if(dval.gt.weightmax)dval=weightmax
           write(iunit,1900) trim(aname),dtable(io)%time(j)/totim,dval,trim(dtable(im)%name)
         end do
       end do

! -- The "* model command line" section of the PEST control file is written.

2400   continue

       write(iunit,2410)
2410   format('* model command line')
       if(modcomline.eq.' ')modcomline='model'
!       call addquote(modcomline,bstring)
!       write(iunit,2420) trim(bstring)
       write(iunit,2420) trim(modcomline)
2420   format(a)

! -- The "* model input/output" section of the PEST control file is written.

       write(iunit,2430)
2430   format('* model input/output')
       do i=1,numtempfile
         if(modfile(i).eq.' ')then
           call num2char(i,anum)
           modfile(i)='model'//trim(anum)//'.in'
         end if
         call addquote(tempfile(i),bstring)
         call addquote(modfile(i),cstring)
         write(iunit,2440) trim(bstring),trim(cstring)
2440     format(a,3x,a)
       end do
       call addquote(instructfile,bstring)
       call addquote(list_output_file,cstring)
       write(iunit,2440) trim(bstring),trim(cstring)
       close(unit=iunit)


       write(*,2460) trim(astring)
       write(recunit,2460) trim(astring)
2460   format(t5,'- file ',a,' written ok.')

! -- If a MICA control file was requested, it is now written.

       if(micactlfile.ne.' ')then
         call addquote(micactlfile,astring)
         write(*,2470) trim(astring)
         write(recunit,2470) trim(astring)
2470     format(t5,'Writing MICA control file ',a,' ....')
         inquire(file=micactlfile,exist=lexist)
         if(lexist)then
2471       write(6,*)
2472       write(*,815,advance='no') trim(astring)
           read(5,'(a)') aa
           call casetrans(aa,'lo')
           if((aa.ne.'y').and.(aa.ne.'n')) go to 2471
           if(aa.eq.'n') go to 2495
         end if
         itempunit=nextunit()
         open(unit=itempunit,file=micactlfile,status='old',iostat=ierr)
         if(ierr.eq.0)then
           close(unit=itempunit,status='delete')
         end if
         itempunit=nextunit()
         open(unit=itempunit,file='t###.###')
         call addquote(pestctlfile,cstring)
         write(itempunit,'(a)') trim(cstring)
         write(itempunit,'(a)') '1'
         write(itempunit,'(a)') trim(astring)
         close(unit=itempunit)
         call system(trim(pest2micacom)//' < t###.### > nul')
         inquire(file=micactlfile,exist=lexist)
         if(.not.lexist)then
           write(amessage,2480)
2480       format('could not write MICA control file - check PEST2MICA command.')           
           go to 9800
         else
           write(*,2460) trim(astring)
           write(recunit,2460) trim(astring)
         end if
       end if
2495   continue       
         
       go to 9900

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
9200   write(amessage,9210)
9210   format('cannot allocate sufficient memory to continue execution.')
       go to 9800
9300   call num2char(iline,aline)
       call addquote(infile,astring)
       write(amessage,9310) trim(aoption),trim(aline),trim(astring),trim(correct_keyword)
9310   format(a,' keyword at line ',a,' of TSPROC input file ',a,' should immediately ', &
       'follow ',a,' keyword.')
       go to 9800
9350   write(amessage,9360) trim(astring)
9360   format('cannot rewind file ',a)
       go to 9800
9400   call num2char(jline,aline)
       write(amessage,9410) trim(aline),trim(astring)
9410   format('cannot read line ',a,' of file ',a)
       go to 9800
9450   call num2char(jline,aline)
       write(amessage,9460) trim(aline),trim(astring)
9460   format('insufficient entries on line ',a,' of file ',a)
       go to 9800
9500   write(amessage,9510) trim(astring)
9510   format('cannot close file ',a)
       go to 9800
9600   write(amessage,9610) trim(aoname),trim(amname),trim(avariable)
9610   format('OBSERVATION_S_TABLE "',a,'"  has been matched to ', &
       'MODEL_S_TABLE "',a,'". However the ',a,' has been computed ', &
       'for one and not for the other.')
       go to 9800


9800   call write_message(leadspace='yes',error='yes')
       call write_message(iunit=recunit,leadspace='yes')
       if(ieqnerr.ne.0)then
         write(amessage,9810)
9810     format(' Offending equation follows:-')
         call write_message()
         call write_message(iunit=recunit)
         do i=1,len_trim(eqntext)
           if(eqntext(i:i).eq.char(196)) eqntext(i:i)='/'
         end do
         write(*,9820) trim(eqntext)
         write(recunit,9820) trim(eqntext)
9820     format(' "',a,'"')
       end if
       ifail=1
       if(iunit.ne.0)close(unit=iunit,iostat=ierr)

9900   deallocate(f_pargpnme,f_inctyp,f_derinc,f_derinclb,f_forcen,f_derincmul, &
                  f_dermthd,stat=ierr)
       deallocate(f_parnme,f_partrans,f_parchglim,f_parval1,f_parlbnd,f_parubnd, &
                  f_pargp,f_scale,f_offset,stat=ierr)
       deallocate(partrans,parchglim,parval1,parlbnd,parubnd,pargp,scale,offset, stat=ierr)
       deallocate(pargpnme,inctyp,derinc,derinclb,forcen,derincmul,dermthd,stat=ierr)


       return

end subroutine pest_files



subroutine prepare_eqn(ifail,nterm,eqntext,iseries)

! -- Subroutine PREPARE_EQN prepares a weights equation for use in weights calculation.

       use tspvar
       use defn
       use inter
       implicit none

       integer, intent(out)         :: ifail
       integer, intent(out)         :: nterm
       character*(*), intent(inout) :: eqntext
       integer, intent(in)          :: iseries

       integer ierr,iterm,k,isnum,i,ddx,mmx,yyx,hhx,nnx,ssx,idx,nex,sex,lnx
       double precision dtempx
       character*1 aa
       character*25 adate_atime

       ifail=0
       call parse(ierr,MAXTERM,nterm,noper,eqntext,aterm,bterm,nfunct,funct,  &
       operat,rterm,1)
       if(ierr.ne.0) then
         ifail=1
         return
       end if

! -- Series are identified in the weights equation.

       call series_sub(ierr,NTERM,1)
       if(ierr.ne.0) then
         ifail=1
         return
       end if

       do i=1,nterm
         if(aterm(i)(1:3).eq.'$~$')then
           if(iseries.eq.0)then
             write(amessage,5)
5            format('a series name cannot be cited in the weights equation for ', &
             'an s_table, v_table or e_table.')
             ifail=1
             return
           end if
           call char2num(ierr,aterm(i)(4:),isnum)
           if(ierr.ne.0)then
             write(amessage,250)
250          format('internal error - contact programmer.')
             ifail=1
             return
           end if
           if(series(iseries)%nterm.ne.series(isnum)%nterm) go to 9300
           do k=1,series(iseries)%nterm
             if(series(iseries)%days(k).ne.(series(isnum)%days(k))) go to 9300
             if(series(iseries)%secs(k).ne.(series(isnum)%secs(k))) go to 9300
           end do
         end if
       end do

! -- Numbers are identified and copied to the rterm array.

       do iterm=1,nterm
         aa=aterm(iterm)(1:1)
         if((aa.ne.'(').and.(aa.ne.')').and.(aa.ne.'+').and.(aa.ne.'-').and.   &
            (aa.ne.'*').and.(aa.ne.'/').and.(aa.ne.'^').and.                   &
            (aterm(iterm)(1:6).ne.'~#str_').and.                               &
            (aterm(iterm)(1:6).ne.'~#fin_').and.                               &
            (aterm(iterm)(1:3).ne.'$~$').and.                                  &
            (aterm(iterm)(1:2).ne.'@_'))then
            call char2num(ierr,aterm(iterm),rterm(iterm))
            if(ierr.ne.0)then
              write(amessage,1870) trim(aterm(iterm))
1870          format('the term "',a,'" in a weights equation cannot be interpreted ', &
              'as a number, function or operator.')
              ifail=1
              return
            end if
            aterm(iterm)='~!~'
         end if
       end do

! -- We now check for intrinsic functions.

       do iterm=1,nterm
         if(aterm(iterm)(1:2).eq.'@_')then
           if(aterm(iterm)(3:).eq.'abs_value')then
             aterm(iterm)(3:)='2'
           else if(aterm(iterm)(3:).eq.'days_start_year')then
             if(iseries.ne.0)then
               aterm(iterm)(3:)='1'
             else
               write(amessage,1875) trim(aterm(iterm))
1875           format('intrinsic function "',a,'" cannot be used in the ',  &
               'weights equation for an s_table, e_table or v_table.')
               ifail=1
               return
             end if
           else if(aterm(iterm)(3:7).eq.'days_')then
             lnx=len(aterm(iterm))
             do idx=1,lnx
               if(aterm(iterm)(idx:idx).eq.char(196))aterm(iterm)(idx:idx)='/'
             end do
             if(iseries.eq.0)then
               write(amessage,1875) trim(aterm(iterm))
               ifail=1
               return
             else
               call getfile(ierr,aterm(iterm),adate_atime,8,lnx)
               if(ierr.ne.0) go to 9400
               idx=index(adate_atime,'_')
               if(idx.eq.0) go to 9400
               call char2date(ierr,adate_atime(1:idx-1),ddx,mmx,yyx)
               if(ierr.ne.0) go to 9400
               call char2time(ierr,adate_atime(idx+1:),hhx,nnx,ssx,ignore_24=1)
               if(ierr.ne.0) go to 9400
               nex=numdays(1,1,1970,ddx,mmx,yyx)
               sex=numsecs(0,0,0,hhx,nnx,ssx)
               dtempx=dble(nex)+dble(sex)/86400.0d0
               aterm(iterm)(3:4)='3_'
               write(aterm(iterm)(5:),'(1pd22.14)') dtempx
             end if
           else
             go to 9400
           end if
         endif
       end do

       return

9300   write(amessage,9310)
9310   format('any series cited in a weights equation must have an identical time-base ', &
       '(ie. the same number of terms, with all dates and times coincident) as the ', &
       'observation time series.')
       ifail=1
       return
9400   write(amessage,9410) trim(aterm(iterm))
9410   format('illegal intrinsic function "',a,'" in weights equation.')
       ifail=1
       return

end subroutine prepare_eqn
!     Last change:  JD    4 Sep 2001    7:08 pm
subroutine series_clean(ifail)

! -- Subroutine CLEAN_SERIES removes or replaces terms between two user-supplied
!    thresholds.

       use tspvar
       use defn
       use inter
       implicit none

       integer, intent(out)   :: ifail

       integer icontext,iseries,ixcon,ierr,idelete,ilthresh,iuthresh,itemp,iterm,i,k,j, &
       isub
       real lthresh,uthresh,svalue,rtemp
       character*10 aname,atemp
       character*15 aline
       character*25 aoption
       character*25 acontext(MAXCONTEXT)

       ifail=0
       currentblock='SERIES_CLEAN'

       write(*,10) trim(currentblock)
       write(recunit,10) trim(currentblock)
10     format(/,' Processing ',a,' block....')

       icontext=0
       iseries=0
       aname=' '
       ixcon=0
       lthresh=1.1e37
       uthresh=-1.1e37
       ilthresh=0
       iuthresh=0
       idelete=0
       isub=0


! -- The CLEAN_SERIES block is first parsed.

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
         if(aoption.eq.'CONTEXT')then
           if(ixcon.ne.0)then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,41) trim(aline),trim(astring)
41           format('CONTEXT keyword in incorrect location at line ',a,' of file ',a)
             go to 9800
           end if
           call read_context(ierr,icontext,acontext)
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'LOWER_ERASE_BOUNDARY')then
           call get_keyword_value(ierr,2,itemp,lthresh,aoption)
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'UPPER_ERASE_BOUNDARY')then
           call get_keyword_value(ierr,2,itemp,uthresh,aoption)
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'SUBSTITUTE_VALUE')then
           isub=1
           call get_keyword_value(ierr,2,itemp,svalue,'SUBSTITUTE_VALUE')
           if(ierr.ne.0) then
             call casetrans(cline(left_word(2):right_word(2)),'lo')
             call getfile(ierr,cline,atemp,left_word(2),right_word(2))
             if(atemp.eq.'delete')then
               idelete=1
               write(*,44) trim(aoption)
               write(recunit,44) trim(aoption)
44             format(t5,a,1x,'delete')
             else
               call num2char(iline,aline)
               call addquote(infile,astring)
               write(amessage,50) trim(aline),trim(astring)
50             format('a real number or "delete" must be supplied with the ',  &
               'SUBSTITUTE_VALUE keyword at line ',a,' of file ',a)
               go to 9800
             end if
           end if
         else if(aoption.eq.'NEW_SERIES_NAME')then
           call read_new_series_name(ierr,aname)
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'SERIES_NAME')then
           call read_series_name(ierr,iseries,'SERIES_NAME')
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'END')then
           go to 200
         else
           call num2char(iline,aline)
           call addquote(infile,astring)
           write(amessage,90) trim(aoption),trim(currentblock),trim(aline),trim(astring)
90         format('unexpected keyword - "',a,'" in ',a,' block at line ',a, &
           ' of file ',a)
           go to 9800
         end if
       end do

! -- The block has been read; now it is checked for correctness.

200    continue
       if(iseries.eq.0)then
         write(amessage,210) trim(currentblock)
210      format('no SERIES_NAME keyword provided in ',a,' block.')
         go to 9800
       end if
       if(isub.eq.0)then
         write(amessage,211) trim(currentblock)
211      format('no SUBSTITUTE_VALUE keyword supplied in the ',a,' block.')
         go to 9800
       end if
       if((aname.eq.' ').and.(idelete.eq.1))then
         write(amessage,230) trim(currentblock)
230      format('if SUBSTITUTE_VALUE is supplied as "delete" then a ', &
         'NEW_SERIES_NAME must be supplied in the ',a,' block.')
         go to 9800
       end if
       if(icontext.eq.0)then
         write(amessage,220) trim(currentblock)
220      format('no CONTEXT keyword(s) provided in ',a,' block.')
         go to 9800
       end if
       if((lthresh.gt.1.0e37).and.(uthresh.lt.-1.0e37))then
         write(amessage,225) trim(currentblock)
225      format('neither an UPPER_ERASE_BOUNDARY nor a LOWER_ERASE_BOUNDARY ', &
         'has been supplied in the ',a,' block.')
         go to 9800
       else
         if(lthresh.lt.1.0e37)ilthresh=1
         if(uthresh.gt.-1.0e37)iuthresh=1
       end if
       if((ilthresh.eq.1).and.(iuthresh.eq.1))then
         if(lthresh.ge.uthresh)then
           write(amessage,235)
235        format('the upper erase boundary must be greater than the lower ', &
           'erase boundary.')
           go to 9800
         end if
       end if

! -- The new series is now written. But first the number of terms in the new series
!    is counted.

       if(idelete.eq.0)then
         iterm=series(iseries)%nterm
       else
         iterm=0
         if((ilthresh.eq.1).and.(iuthresh.eq.1))then
           do j=1,series(iseries)%nterm
             if((series(iseries)%val(j).lt.lthresh).or.      &
                (series(iseries)%val(j).gt.uthresh)) iterm=iterm+1
           end do
         else if(ilthresh.eq.1)then
           do j=1,series(iseries)%nterm
             if(series(iseries)%val(j).lt.lthresh) iterm=iterm+1
           end do
         else
           do j=1,series(iseries)%nterm
             if(series(iseries)%val(j).gt.uthresh) iterm=iterm+1
           end do
         end if
         if(iterm.eq.0)then
           write(amessage,240) trim(series(iseries)%name), trim(aname)
240        format('all terms in series "',a,'" have been erased, so the new ', &
           'series "',a,'" has no terms.')
           go to 9800
         end if
       end if

! -- If a new time series is warranted, then space is allocated for it.

       if(aname.ne.' ')then
         do i=1,MAXSERIES
           if(.not.series(i)%active) go to 515
         end do
         write(amessage,510)
510      format('no more time series available for data storage - increase MAXSERIES and ', &
         'recompile program.')
         go to 9800

515      allocate(series(i)%days(iterm),series(i)%secs(iterm),  &
         series(i)%val(iterm),stat=ierr)
         if(ierr.ne.0)then
           write(amessage,550)
550        format('cannot allocate memory for another time series.')
           go to 9800
         end if
         series(i)%active=.true.
         series(i)%name=aname
         series(i)%nterm=iterm
         series(i)%type='ts'
         k=0
         do j=1,series(iseries)%nterm
           if((ilthresh.eq.1).and.(iuthresh.eq.1))then
             if((series(iseries)%val(j).lt.lthresh).or.   &
                (series(iseries)%val(j).gt.uthresh)) go to 570
           else if(ilthresh.eq.1)then
             if(series(iseries)%val(j).lt.lthresh) go to 570
           else
             if(series(iseries)%val(j).gt.uthresh) go to 570
           end if
           if(idelete.eq.1) go to 580
           rtemp=svalue
           go to 575
570        continue
           rtemp=series(iseries)%val(j)
575        continue
           k=k+1
           series(i)%days(k)=series(iseries)%days(j)
           series(i)%secs(k)=series(iseries)%secs(j)
           series(i)%val(k)=rtemp
580        continue
         end do
       else
         do j=1,series(iseries)%nterm
           if((ilthresh.eq.1).and.(iuthresh.eq.1))then
             if((series(iseries)%val(j).ge.lthresh).and.  &
                (series(iseries)%val(j).le.uthresh)) &
                series(iseries)%val(j)=svalue
           else if(ilthresh.eq.1)then
             if(series(iseries)%val(j).ge.lthresh)series(iseries)%val(j)=svalue
           else
             if(series(iseries)%val(j).le.uthresh)series(iseries)%val(j)=svalue
           end if
         end do
       end if

       if(aname.ne.' ')then
         write(*,590) trim(aname)
         write(recunit,590) trim(aname)
590      format(t5,'Series "',a,'" successfully calculated.')
       else
         write(*,600) trim(series(iseries)%name)
         write(recunit,600) trim(series(iseries)%name)
600      format(t5,'Series "',a,'" successfully cleaned.')
       end if
       return

9000   call num2char(iline,aline)
       call addquote(infile,astring)
       write(amessage,9010) trim(aline), trim(astring)
9010   format('cannot read line ',a,' of TSPROC input file ',a)
       go to 9800
9100   continue
       call addquote(infile,astring)
       write(amessage,9110) trim(astring), trim(currentblock)
9110   format('unexpected end encountered to TSPROC input file ',a,' while ', &
       ' reading ',a,' block.')
       go to 9800

9800   call write_message(leadspace='yes',error='yes')
       call write_message(iunit=recunit,leadspace='yes')
       ifail=1

       return

end subroutine series_clean


subroutine bfilter(ifail)

! -- Subroutine BFILTER calculates Butterworth filter coefficients and 
!    carries out low, high or band pass filtering operations. It also
!    carries out "baseflow filtering" as described in Nathan and McMahon (1990).

       use tspvar
       use defn
       use inter
       implicit none

       integer, intent(out)   :: ifail

       integer ierr,icontext,iseries,itemp,nsterm,ilags,j,nsecs,ndays, &
       dd,mm,yy,hh,nn,ss,i,ixcon,ns,k,jclipzero,jclipinput,jfreq1,jfreq2, &
       jfreq,jns,jfilpass,jpass,jalpha,ipass,ip
       integer jrevstage2,jj
       real rtemp,freq,freq1,freq2,af,bf,cf,df,ef,tdelt,alpha,alpha1,fk_1, &
       yk1,yk,yk_1
       real a(3),b(3),c(3),d(3),e(3),rval(-3:5),gval(-3:5)
       character*3 aaa
       character*10 aname,filpass
       character*20 aline,filtype
       character*25 aoption
       character*25 acontext(MAXCONTEXT)

       ifail=0
       currentblock='DIGITAL_FILTER'

       write(*,10) trim(currentblock)
       write(recunit,10) trim(currentblock)
10     format(/,' Processing ',a,' block....')

       icontext=0
       iseries=0
       aname=' '
       ixcon=0
       filtype=' '
       filpass=' '
       jfilpass=0
       ns=1
       jns=0
       freq=-1.0e35
       freq1=-1.0e35
       freq2=-1.0e35
       jfreq=0
       jfreq1=0
       jfreq2=0       
       jclipzero=0
       jclipinput=0
       jalpha=0
       jpass=0
       jrevstage2=0

! -- The DIGITAL_FILTER block is first parsed.

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
         if(aoption.eq.'NEW_SERIES_NAME')then
           call read_new_series_name(ierr,aname)
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'SERIES_NAME')then
           call read_series_name(ierr,iseries,'SERIES_NAME')
           if(ierr.ne.0) go to 9800
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
         else if(aoption.eq.'FILTER_TYPE')then
           call getfile(ierr,cline,filtype,left_word(2),right_word(2))
           if(ierr.ne.0)then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,49) trim(aline),trim(astring)
49           format('cannot read filter type from line ',a,' of file ',a)
             go to 9800
           end if                                        
           call casetrans(filtype,'lo')
           if((filtype.ne.'butterworth').and.   &
              (filtype.ne.'baseflow_separation'))then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,55) trim(aline),trim(astring)
55           format('filter type must be "butterworth" or "baseflow_separation" ', &
             'at line ',a,' of file ',a)
             go to 9800
           end if             
           write(*,60) trim(filtype)
           write(recunit,60) trim(filtype)
60         format(t5,'FILTER_TYPE ',a)
         else if(aoption.eq.'FILTER_PASS')then
           call getfile(ierr,cline,filpass,left_word(2),right_word(2))
           if(ierr.ne.0)then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,50) trim(aline),trim(astring)
50           format('cannot read filter pass band type from line ',a,' of file ',a)
             go to 9800
           end if
           jfilpass=1
           call casetrans(filpass,'lo')
           if((filpass.ne.'high').and.(filpass.ne.'low').and.  &
              (filpass.ne.'band'))then
              call num2char(iline,aline)
              call addquote(infile,astring)
              write(amessage,53) trim(aline),trim(astring)
53            format('filter pass band type must be "high", "low" or "band" at line ',  &
              a,' of file ',a)
              go to 9800
           end if             
           write(*,54) trim(filpass)
           write(recunit,54) trim(filpass)
54         format(t5,'FILTER_PASS ',a)
         else if(aoption.eq.'STAGES')then
           call get_keyword_value(ierr,1,ns,rtemp,'STAGES')
           if(ierr.ne.0) go to 9800
           jns=1
         else if(aoption.eq.'CUTOFF_FREQUENCY')then
           call get_keyword_value(ierr,2,itemp,freq,'CUTOFF_FREQUENCY')
           if(ierr.ne.0) go to 9800
           if(freq.le.0.0)then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,65) trim(aline),trim(astring)
65           format('frequency must be positive at line ',a,' of file ',a)
             go to 9800
           end if
           jfreq=1
         else if(aoption.eq.'CUTOFF_FREQUENCY_1')then
           call get_keyword_value(ierr,2,itemp,freq1,'CUTOFF_FREQUENCY_1')
           if(ierr.ne.0) go to 9800
           if(freq1.le.0.0)then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,65) trim(aline),trim(astring)
             go to 9800
           end if
           jfreq1=1
         else if(aoption.eq.'CUTOFF_FREQUENCY_2')then
           call get_keyword_value(ierr,2,itemp,freq2,'CUTOFF_FREQUENCY_2')
           if(ierr.ne.0) go to 9800
           if(freq2.le.0.0)then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,65) trim(aline),trim(astring)
             go to 9800
           end if
           jfreq2=1
         else if(aoption.eq.'CLIP_ZERO')then
           call get_yes_no(ierr,jclipzero)
           if(ierr.ne.0) go to 9800
           if(jclipzero.eq.1)then
             aaa='yes'
           else
             aaa='no'
           end if
           write(*,70) trim(aaa)
           write(recunit,70) trim(aaa)
70         format(t5,'CLIP_ZERO ',a)
         else if(aoption.eq.'CLIP_INPUT')then
           call get_yes_no(ierr,jclipinput)
           if(ierr.ne.0) go to 9800
           if(jclipinput.eq.1)then
             aaa='yes'
           else
             aaa='no'
           end if
           write(*,71) trim(aaa)
           write(recunit,71) trim(aaa)
71         format(t5,'CLIP_INPUT ',a)
         else if(aoption.eq.'ALPHA')then
           call get_keyword_value(ierr,2,itemp,alpha,'ALPHA')
           if(ierr.ne.0) go to 9800
           if(alpha.le.0.0)then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,81) trim(aline),trim(astring) 
81           format('alpha must be positive at line ',a,' of file ',a)
             go to 9800
           end if
           jalpha=1
         else if(aoption.eq.'REVERSE_SECOND_STAGE')then
           call get_yes_no(ierr,jrevstage2)
           if(ierr.ne.0) go to 9800
           if(jrevstage2.eq.1)then
             aaa='yes'
           else
             aaa='no'
           end if
           write(*,72) trim(aaa)
           write(recunit,72) trim(aaa)
72         format(t5,'REVERSE_SECOND_STAGE ',a)
         else if(aoption.eq.'PASSES')then
           call get_keyword_value(ierr,1,ipass,rtemp,'PASSES')
           if(ierr.ne.0) go to 9800
           if((ipass.ne.1).and.(ipass.ne.3))then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,82) trim(aline),trim(astring) 
82           format('number of passes must be 1 or 3 at line ',a,' of file ',a)
             go to 9800
           end if
           jpass=1
         else if(aoption.eq.'END')then
           go to 200
         else
           call num2char(iline,aline)
           call addquote(infile,astring)
           write(amessage,90) trim(aoption),trim(currentblock),trim(aline),trim(astring)
90         format('unexpected keyword - "',a,'" in ',a,' block at line ',a, &
           ' of file ',a)
           go to 9800
         end if
       end do

! -- The block has been read; now it is checked for correctness.

200    continue
       if(iseries.eq.0)then
         write(amessage,210) trim(currentblock)
210      format('no SERIES_NAME keyword provided in ',a,' block.')
         go to 9800
       end if
       if(aname.eq.' ')then
         write(amessage,230) trim(currentblock)
230      format('no NEW_SERIES_NAME keyword provided in ',a,' block.')
         go to 9800
       end if
       if(icontext.eq.0)then
         write(amessage,220) trim(currentblock)
220      format('no CONTEXT keyword(s) provided in ',a,' block.')
         go to 9800
       end if
       if(filtype.eq.' ')then
         write(amessage,222) trim(currentblock)
222      format('no FILTER_TYPE keyword has been provided in ',a,' block.')
         go to 9800
       end if
       if(filtype(1:4).eq.'base')then
         if(jns.eq.1) go to 9300
         if(jfilpass.eq.1) go to 9300
         if((jfreq.eq.1).or.(jfreq1.eq.1).or.(jfreq2.eq.1)) go to 9300
       else if(filtype(1:3).eq.'but')then
         if(jpass.eq.1) go to 9350
         if(jalpha.eq.1) go to 9350
         if((jclipzero.eq.1).or.(jclipinput.eq.1)) go to 9370
       end if
       if(filtype(1:3).eq.'but')then
         if((ns.lt.1).or.(ns.gt.3))then
           write(amessage,245) trim(currentblock)
245        format('number of filter stages must be 1, 2, or 3 in ',a,' block.')
           go to 9800
         end if
         if((filpass.eq.'low').or.(filpass.eq.'high'))then
           if((freq1.gt.0.0).or.(freq2.gt.0.0))then
             write(amessage,250) trim(currentblock)
250          format('values for CUTOFF_FREQUENCY_1 and CUTOFF_FREQUENCY_2 ',  &
             'should be supplied only for band pass filter in ',a,' block.')
             go to 9800
           end if
           if(freq.lt.0.0)then
             write(amessage,255) trim(currentblock)
255          format('no value supplied for CUTOFF_FREQUENCY in ',a,' block.')
             go to 9800
           end if
         else if(filpass.eq.'band')then
           if((freq1.lt.0.0).or.(freq2.lt.0.0))then
             write(amessage,256) trim(currentblock)
256          format('values for both CUTOFF_FREQUENCY_1 and CUTOFF_FREQUENCY_2 ',  &
             'should be supplied for band pass filter in ',a,' block.')
             go to 9800
           end if
           if(freq.gt.0.0)then
             write(amessage,257) trim(currentblock)
257          format('no value should be supplied for CUTOFF_FREQUENCY for ', &
             'band pass filter in ',a,' block - only for CUTOFF_FREQUENCY_1 ',  &
             'and CUTOFF_FREQUENCY_2.')
             go to 9800
           end if
           if(freq2.le.freq1)then
             write(amessage,258) trim(currentblock)
258          format('CUTOFF_FREQUENCY_2 should be greater than CUTOFF_FREQUENCY_1 ', &
             'in ',a,' block.')
             go to 9800
           end if
         else if(filpass.eq.' ')then
           write(amessage,259) trim(currentblock)
259        format('no FILTER_PASS keyword provided in ',a,' block.')
           go to 9800
         end if
       else if(filtype(1:4).eq.'base')then
         if(jpass.eq.0)ipass=1
         if(jalpha.eq.0)then
           write(amessage,270) trim(currentblock)
270        format('no ALPHA keyword provided in ',a,' block.')
           go to 9800
         end if
       end if
       if(jrevstage2.eq.1)then
         if((filtype(1:3).ne.'but').or.(filpass.ne.'low').or.(ns.ne.2))then
           write(amessage,299)
299        format('REVERSE_SECOND_STAGE can only be set to "yes" when (a) butterworth ', &
           'filter is chosen, (b) number or stages is 2 and (c) the FILTER_PASS is "low".')
           go to 9800
         end if
       end if
                 
! -- Filtering can only be performed if the input time series has equal
!    increments. This is now tested.

       nsterm=series(iseries)%nterm
       if(nsterm.lt.20)then
         call num2char(nsterm,aline)
         write(amessage,300) trim(series(iseries)%name),trim(aline)
300      format('series "',a,'" has only ',a,' terms. This is insufficient to perform ', &
         'the requested filtering operation.')
         go to 9800
       end if
       if(nsterm.gt.2)then
         ilags=(series(iseries)%days(2)-series(iseries)%days(1))*86400+   &
                series(iseries)%secs(2)-series(iseries)%secs(1)
         do j=2,nsterm-1
           nsecs=series(iseries)%secs(j)+ilags
           ndays=series(iseries)%days(j)
260        if(nsecs.ge.86400)then
             ndays=ndays+1
             nsecs=nsecs-86400
             go to 260
           end if
           if((nsecs.ne.series(iseries)%secs(j+1)).or.   &
              (ndays.ne.series(iseries)%days(j+1)))then
               call newdate(series(iseries)%days(j),1,1,1970,dd,mm,yy)
               nsecs=series(iseries)%secs(j)
               hh=nsecs/3600
               nn=(nsecs-hh*3600)/60
               ss=nsecs-hh*3600-nn*60
               if(datespec.eq.1) then
                 write(amessage,280) trim(series(iseries)%name),dd,mm,yy,hh,nn,ss
               else
                 write(amessage,280) trim(series(iseries)%name),mm,dd,yy,hh,nn,ss
               end if
280            format('time interval between terms in time series "',a,'" is not ', &
               'constant. The first discrepancy occurs following the sample taken on ',  &
               i2.2,'/',i2.2,'/',i4,' at ',i2.2,':',i2.2,':',i2.2)
               go to 9800
           end if
         end do
       end if

! -- The filter coefficients are now calculated (butterworth filter).

       if(filtype(1:3).eq.'but')then
         tdelt=float(ilags)/86400.00
         if(filpass.eq.'low')then
           if(freq.ge.0.5/tdelt) go to 9200
           call lpdes(freq,tdelt,ns,a,b,c)          
         else if(filpass.eq.'high')then
           if(freq.ge.0.5/tdelt) go to 9200
           call hpdes(freq,tdelt,ns,a,b,c)
         else
           if((freq1.ge.0.5/tdelt).or.(freq2.ge.0.5/tdelt)) go to 9200
           call bpdes(freq1,freq2,tdelt,ns,a,b,c,d,e)        
         end if
       end if

! -- Space for a new series is allocated.

       do i=1,MAXSERIES
         if(.not.series(i)%active) go to 515
       end do
       write(amessage,510)
510    format('no more time series available for data storage - increase MAXSERIES and ', &
       'recompile program, or erase a series using an ERASE_SERIES block.')
       go to 9800

515    continue
       allocate(series(i)%days(nsterm),series(i)%secs(nsterm),  &
       series(i)%val(nsterm),stat=ierr)
       if(ierr.ne.0)then
         write(amessage,550)
550      format('cannot allocate memory for another time series.')
         go to 9800
       end if
       series(i)%active=.true.
       series(i)%name=aname
       series(i)%nterm=nsterm
       series(i)%type='ts'
       do j=1,nsterm
         series(i)%days(j)=series(iseries)%days(j)
       end do
       do j=1,nsterm
         series(i)%secs(j)=series(iseries)%secs(j)
       end do

! -- Now the butterworth filtering is carried out. But first a temporary time series is 
!    allocated if needed.

       if(filtype(1:4).eq.'base') go to 700
       if(ns.gt.1)then
         call alloc_tempseries(ierr,nsterm)
         if(ierr.ne.0) go to 9800
       end if
 
       do k=1,ns
         af=a(k)
         bf=b(k)
         cf=c(k)
         if((k.eq.2).and.(jrevstage2.eq.1))then
           af=a(1)
           bf=b(1)
           cf=c(1)
         end if
         if(filpass.eq.'band')then
           df=d(k)
           ef=e(k)
         end if
         if(k.eq.1)then
           do j=1,5
             rval(j)=series(iseries)%val(j)
           end do
         else
           do j=1,5
             rval(j)=tempseries%val(j)
           end do
         end if
!         rval(0)=rval(1)-(rval(2)-rval(1))
!         rval(-1)=rval(0)-(rval(1)-rval(0))
!         rval(-2)=rval(-1)-(rval(0)-rval(-1))
!         rval(-3)=rval(-2)-(rval(-1)-rval(-2))          
!         gval(-3)=rval(-3)
!         gval(-2)=rval(-2)
!         gval(-1)=rval(-1)
!         gval(0)=rval(0)
         rval(0)=rval(1)
         rval(-1)=rval(0)
         rval(-2)=rval(-1)
         rval(-3)=rval(-2)
         if(filpass.eq.'low')then
           gval(-3)=rval(-3)
           gval(-2)=rval(-2)
           gval(-1)=rval(-1)
           gval(0)=rval(0)
         else
           gval(-3)=0.0
           gval(-2)=0.0
           gval(-1)=0.0
           gval(0)=0.0           
         end if
         if(filpass.eq.'low')then
           do j=1,5
             gval(j)=af*(rval(j)+2.0*rval(j-1)+rval(j-2))-  &
             bf*gval(j-1)-cf*gval(j-2)
           end do
         else if(filpass.eq.'high')then
           do j=1,5
             gval(j)=af*(rval(j)-2.0*rval(j-1)+rval(j-2))-  &
             bf*gval(j-1)-cf*gval(j-2)
           end do
         else
           do j=1,5
             gval(j)=af*(rval(j)-2.0*rval(j-2)+rval(j-4))-bf*gval(j-1)-  &
             cf*gval(j-2)-df*gval(j-3)-ef*gval(j-4)
           end do
         end if
         do j=1,5
           series(i)%val(j)=gval(j)
         end do
         if(filpass.eq.'low')then
           if(k.ne.1)then
             do j=6,nsterm          
               series(i)%val(j)=af*(tempseries%val(j)+    &
               2.0*tempseries%val(j-1)+tempseries%val(j-2))-  &
               bf*series(i)%val(j-1)-cf*series(i)%val(j-2)
             end do           
           else
             do j=6,nsterm          
               series(i)%val(j)=af*(series(iseries)%val(j)+    &
               2.0*series(iseries)%val(j-1)+series(iseries)%val(j-2))-  &
               bf*series(i)%val(j-1)-cf*series(i)%val(j-2)
             end do
           end if
         else if(filpass.eq.'high')then
           if(k.ne.1)then
             do j=6,nsterm
               series(i)%val(j)=af*(tempseries%val(j)-     &
               2.0*tempseries%val(j-1)+tempseries%val(j-2))-  &
               bf*series(i)%val(j-1)-cf*series(i)%val(j-2)
             end do
           else
             do j=6,nsterm
               series(i)%val(j)=af*(series(iseries)%val(j)-     &
               2.0*series(iseries)%val(j-1)+series(iseries)%val(j-2))-  &
               bf*series(i)%val(j-1)-cf*series(i)%val(j-2)
             end do           
           end if
         else
           if(k.ne.1)then
             do j=6,nsterm
               series(i)%val(j)=af*(tempseries%val(j)-    &
               2.0*tempseries%val(j-2)+tempseries%val(j-4))-  &
               bf*series(i)%val(j-1)-cf*series(i)%val(j-2)-    &
               df*series(i)%val(j-3)-ef*series(i)%val(j-4)
               if(abs(series(i)%val(j)).gt.1.0e30) go to 9400
             end do           
           else
             do j=6,nsterm
               series(i)%val(j)=af*(series(iseries)%val(j)-    &
               2.0*series(iseries)%val(j-2)+series(iseries)%val(j-4))-  &
               bf*series(i)%val(j-1)-cf*series(i)%val(j-2)-    &
               df*series(i)%val(j-3)-ef*series(i)%val(j-4)
               if(abs(series(i)%val(j)).gt.1.0e30) go to 9400
             end do
           end if
         end if
         if(k.ne.ns)then
           if((k.eq.1).and.(jrevstage2.eq.1))then
             do j=1,nsterm
               tempseries%val(j)=series(i)%val(nsterm-j+1)
             end do
           else
             do j=1,nsterm
               tempseries%val(j)=series(i)%val(j)
             end do
           end if
         else
           if(jrevstage2.eq.1)then
             do j=1,nsterm/2
               jj=nsterm-j+1
               rtemp=series(i)%val(j)
               series(i)%val(j)=series(i)%val(jj)
               series(i)%val(jj)=rtemp
             end do
           end if
         end if
       end do
       go to 900
       
! -- Baseflow separation filtering is carried out.

700    continue

       call alloc_tempseries(ierr,nsterm)
       if(ierr.ne.0) go to 9800

       alpha1=(1.0+alpha)*0.5
       do ip=1,ipass
         if(ip.eq.1)then
           do j=1,nsterm
             tempseries%val(j)=series(iseries)%val(j)
           end do
         else if((ip.eq.2).or.(ip.eq.3))then
           do j=1,nsterm
             tempseries%val(j)=series(i)%val(nsterm+1-j)
           end do
         end if
         yk=tempseries%val(1)
         yk1=tempseries%val(2)
         yk_1=yk-(yk1-yk)
         fk_1=yk_1
         series(i)%val(1)=alpha*fk_1+alpha1*(yk-yk_1)
         do j=2,nsterm
           series(i)%val(j)=alpha*series(i)%val(j-1) + alpha1*  &
           (tempseries%val(j)-tempseries%val(j-1))
         end do
       end do

! -- The following applies to both types of filtering.

900    continue
       if(jclipzero.ne.0)then
         do j=1,nsterm
           if(series(i)%val(j).lt.0.0)series(i)%val(j)=0.0
         end do
       end if
       if(jclipinput.ne.0)then
         do j=1,nsterm
           if(series(i)%val(j).gt.series(iseries)%val(j))  &
              series(i)%val(j) =  series(iseries)%val(j)
         end do
       end if     
       
       write(*,580) trim(aname)
       write(recunit,580) trim(aname)
580    format(t5,'Series "',a,'" successfully calculated.')
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
9200   write(amessage,9210) trim(currentblock)
9210   format('filter cutoff frequency must be less than half of the ',  &
       'series sampling frequency in ',a,' block.')
       go to 9800
9300   write(amessage,9310) 
9310   format('if FILTER_TYPE is "baseflow_separation" then none of the STAGES ',   &
       'CUTOFF_FREQUENCY, CUTOFF_FREQUENCY_1, CUTOFF_FREQUENCY_2 ', &
       'or FILTER_PASS keywords must be provided.')
       go to 9800
9350   write(amessage,9360)
9360   format('if FILTER_TYPE is "butterworth" then neither of the PASSES, ', &
       'ALPHA, CLIP_ZERO nor CLIP_INPUT keywords must be provided.')
       go to 9800
9370   write(amessage,9380)
9380   format('if FILTER_TYPE is "butterworth" then CLIP_ZERO and CLIP_INPUT ',  &
       'should be omitted or set to "no".')
       go to 9800
9400   write(amessage,9410)
9410   format('bandpass filter is numerically unstable - consider using ', &
       'wider pass band.')
       go to 9800
       
9800   call write_message(leadspace='yes',error='yes')
       call write_message(iunit=recunit,leadspace='yes')
       ifail=1

       return

end subroutine bfilter


subroutine lpdes(fc,t,ns,a,b,c)

! -- Subroutine LPDES evaluates the coefficients for a low pass filter.

       implicit none
       integer, intent(in) :: ns
       real, intent(in)    :: fc,t
       real, intent(out)   :: a(ns),b(ns),c(ns)

       integer k
       real pi,wcp,cs,x
       
       pi=3.1415926536
       wcp=sin(fc*pi*t)/cos(fc*pi*t)
       do 120 k=1,ns
         cs=cos(float(2*(k+ns)-1)*pi/float(4*ns))
         x=1.0/(1.0+wcp*wcp-2.0*wcp*cs)
         a(k)=wcp*wcp*x
         b(k)=2.0*(wcp*wcp-1.0)*x
         c(k)=(1.0+wcp*wcp+2.0*wcp*cs)*x
120    continue
       return    

end subroutine lpdes

          
subroutine hpdes(fc,t,ns,a,b,c)

! -- Subroutine HPDES evaluates the coefficients for a high pass filter.

       implicit none
       integer, intent(in) :: ns
       real, intent(in)    :: fc,t
       real, intent(out)   :: a(ns),b(ns),c(ns)

       integer k
       real pi,wcp,cs

       pi=3.1415926536
       wcp=sin(fc*pi*t)/cos(fc*pi*t)
       do 120 k=1,ns
         cs=cos(float(2*(k+ns)-1)*pi/float(4*ns))
         a(k)=1.0/(1.0+wcp*wcp-2.0*wcp*cs)
         b(k)=2.0*(wcp*wcp-1.0)*a(k)
         c(k)=(1.0+wcp*wcp+2.0*wcp*cs)*a(k)
120    continue
       return    

end subroutine hpdes
          

subroutine bpdes(f1,f2,t,ns,a,b,c,d,e)

! -- Subroutine BPDES evaluates the coefficients for a band pass filter.

       implicit none
       integer, intent(in) :: ns
       real, intent(in)    :: f1,f2,t
       real, intent(out)   :: a(ns),b(ns),c(ns),d(ns),e(ns)

       integer k
       real pi,w1,w2,wc,q,s,cs,p,r,x

       pi=3.1415926536
       w1=sin(f1*pi*t)/cos(f1*pi*t)
       w2=sin(f2*pi*t)/cos(f2*pi*t)
       wc=w2-w1
       q=wc*wc+2.0*w1*w2
       s=w1*w1*w2*w2
       do k=1,ns
         cs=cos(float(2*(k+ns)-1)*pi/float(4*ns))
         p=-2.0*wc*cs
         r=p*w1*w2
         x=1.0+p+q+r+s
         a(k)=wc*wc/x
         b(k)=(-4.0-2.0*p+2.0*r+4.0*s)/x
         c(k)=(6.0-2.0*q+6.0*s)/x
         d(k)=(-4.0+2.0*p-2.0*r+4.0*s)/x
         e(k)=(1.0-p+q-r+s)/x
       end do
       
       return
       
end subroutine bpdes




subroutine compare_series(ifail)

! -- Subroutine COMPARE_SERIES calculates comparison statistics between time series.

       use tspvar
       use defn
       use inter
       implicit none

       integer, intent(out)   :: ifail

       integer isseries,ioseries,jbias,jse,jrbias,jrse,jns,jce,jia,  &
       ibseries,ibbterm,ibeterm,ibterm,exponent,l
       integer dd1,mm1,yy1,hh1,nn1,ss1,dd2,mm2,yy2,hh2,nn2,ss2,ierr, &
       icontext,i,begdays,begsecs,enddays,endsecs, &
       j,isbterm,iobterm,iseterm,ioeterm,iiterm,ixcon,isterm,ioterm,k
       real rtemp,rtemp1,tsum1,tsum2,tsum3,tsum4
       character*3 aaa
       character*10 aname
       character*15 aline
       character*25 aoption
       character*25 acontext(MAXCONTEXT)

       ifail=0
       currentblock='SERIES_COMPARE'

       write(*,10) trim(currentblock)
       write(recunit,10) trim(currentblock)
10     format(/,' Processing ',a,' block....')

       icontext=0
       isseries=0
       ioseries=0
       ibseries=0
       jbias=0
       jse=0
       jrbias=0
       jrse=0
       jns=0
       jce=0
       jia=0
       exponent=-9999
       yy1=-9999
       hh1=-9999
       yy2=-9999
       hh2=-9999
       aname=' '
       ixcon=0

! -- The COMPARE_SERIES block is first parsed.

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
         if(aoption.eq.'NEW_C_TABLE_NAME')then
           call read_new_table_name(ierr,4,aname)
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'DATE_1')then
           call read_date(ierr,dd1,mm1,yy1,'DATE_1')
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'DATE_2')then
           call read_date(ierr,dd2,mm2,yy2,'DATE_2')
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'TIME_1')then
           call read_time(ierr,hh1,nn1,ss1,'TIME_1')
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'TIME_2')then
           call read_time(ierr,hh2,nn2,ss2,'TIME_2')
           if(ierr.ne.0) go to 9800           
         else if(aoption.eq.'SERIES_NAME_SIM')then
           if(isseries.ne.0)then
             write(amessage,26)
26           format('more than one SERIES_NAME_SIM entry in SERIES_COMPARE block.')
             go to 9800
           end if
           call read_series_name(ierr,isseries,'SERIES_NAME_SIM')
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'SERIES_NAME_OBS')then
           if(ioseries.ne.0)then
             write(amessage,27)
27           format('more than one SERIES_NAME_OBS entry in SERIES_COMPARE block.')
             go to 9800
           end if         
           call read_series_name(ierr,ioseries,'SERIES_NAME_OBS')
           if(ierr.ne.0) go to 9800
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
         else if(aoption.eq.'BIAS')then
           call get_yes_no(ierr,jbias)
           if(ierr.ne.0) go to 9800
           if(jbias.eq.1)then
             aaa='yes'
           else
             aaa='no'
           end if
           write(*,128) trim(aaa)
           write(recunit,128) trim(aaa)
128        format(t5,'BIAS ',a)
         else if(aoption.eq.'STANDARD_ERROR')then
           call get_yes_no(ierr,jse)
           if(ierr.ne.0) go to 9800
           if(jse.eq.1)then
             aaa='yes'
           else
             aaa='no'
           end if
           write(*,129) trim(aaa)
           write(recunit,129) trim(aaa)
129        format(t5,'STANDARD_ERROR ',a)
         else if(aoption.eq.'RELATIVE_BIAS')then
           call get_yes_no(ierr,jrbias)
           if(ierr.ne.0) go to 9800
           if(jrbias.eq.1)then
             aaa='yes'
           else
             aaa='no'
           end if
           write(*,132) trim(aaa)
           write(recunit,132) trim(aaa)
132        format(t5,'RELATIVE_BIAS ',a)
         else if(aoption.eq.'RELATIVE_STANDARD_ERROR')then
           call get_yes_no(ierr,jrse)
           if(ierr.ne.0) go to 9800
           if(jrse.eq.1)then
             aaa='yes'
           else
             aaa='no'
           end if
           write(*,133) trim(aaa)
           write(recunit,133) trim(aaa)
133        format(t5,'RELATIVE_STANDARD_ERROR ',a)
         else if(aoption.eq.'NASH_SUTCLIFFE')then
           call get_yes_no(ierr,jns)
           if(ierr.ne.0) go to 9800
           if(jns.eq.1)then
             aaa='yes'
           else
             aaa='no'
           end if
           write(*,134) trim(aaa)
           write(recunit,134) trim(aaa)
134        format(t5,'NASH_SUTCLIFFE ',a)
         else if(aoption.eq.'COEFFICIENT_OF_EFFICIENCY')then
           call get_yes_no(ierr,jce)
           if(ierr.ne.0) go to 9800
           if(jce.eq.1)then
             aaa='yes'
           else
             aaa='no'
           end if
           write(*,135) trim(aaa)
           write(recunit,135) trim(aaa)
135        format(t5,'COEFFICIENT_OF_EFFICIENCY ',a)           
         else if(aoption.eq.'INDEX_OF_AGREEMENT')then
           call get_yes_no(ierr,jia)
           if(ierr.ne.0) go to 9800
           if(jia.eq.1)then
             aaa='yes'
           else
             aaa='no'
           end if
           write(*,136) trim(aaa)
           write(recunit,136) trim(aaa)
136        format(t5,'INDEX_OF_AGREEMENT ',a)
         else if(aoption.eq.'EXPONENT')then
           call get_keyword_value(ierr,1,exponent,rtemp,'EXPONENT')
           if(ierr.ne.0) go to 9800
           if((exponent.ne.1).and.(exponent.ne.2))then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,138) trim(aline),trim(astring) 
138          format('exponent must be 1 or 2 at line ',a,  &
             ' of file ',a)
             go to 9800
           end if
         else if(aoption.eq.'SERIES_NAME_BASE')then
           call read_series_name(ierr,ibseries,'SERIES_NAME_BASE')
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'END')then
           go to 200
         else
           call num2char(iline,aline)
           call addquote(infile,astring)
           write(amessage,90) trim(aoption),trim(currentblock),trim(aline),trim(astring)
90         format('unexpected keyword - "',a,'" in ',a,' block at line ',a, &
           ' of file ',a)
           go to 9800
         end if
       end do

! -- The block has been read; now it is checked for correctness.

200    continue
       if(isseries.eq.0)then
         write(amessage,210) trim(currentblock)
210      format('no SERIES_NAME_SIM keyword provided in ',a,' block.')
         go to 9800
       end if
       if(ioseries.eq.0)then
         write(amessage,211) trim(currentblock)
211      format('no SERIES_NAME_OBS keyword provided in ',a,' block.')
         go to 9800
       end if
       
       if(aname.eq.' ')then
         write(amessage,230) trim(currentblock)
230      format('no NEW_C_TABLE keyword provided in ',a,' block.')
         go to 9800
       end if
       if(icontext.eq.0)then
         write(amessage,220) trim(currentblock)
220      format('no CONTEXT keyword(s) provided in ',a,' block.')
         go to 9800
       end if
       call date_check(ierr,yy1,mm1,dd1,hh1,nn1,ss1,yy2,mm2,dd2,hh2,nn2,ss2,  &
       begdays,begsecs,enddays,endsecs)
       if(ierr.ne.0) go to 9800
       call beg_end_check(ierr,isseries,begdays,begsecs,enddays,endsecs)
       if(ierr.ne.0) go to 9800
       call beg_end_check(ierr,ioseries,begdays,begsecs,enddays,endsecs)
       if(ierr.ne.0) go to 9800       
       if((jbias.eq.0).and.(jse.eq.0).and.(jrbias.eq.0)  &
         .and.(jrse.eq.0).and.(jns.eq.0).and.(jce.eq.0).and.(jia.eq.0))then
         write(amessage,240) trim(currentblock)
240      format('at least one of the BIAS, STANDARD_ERROR, RELATIVE_BIAS, ',     &
         'RELATIVE_STANDARD_ERROR, NASH_SUTCLIFFE, ', &
         'COEFFICIENT_OF_EFFICIENCY or INDEX_OF_AGREEMENT keywords must ', &
         'be supplied within a ',a,' block.')
         go to 9800
       end if
       if(ibseries.ne.0)then
         if((jce.eq.0).and.(jia.eq.0))then
           write(amessage,245) trim(currentblock)
245        format('a SERIES_NAME_BASE keyword can only be supplied ', &
           'if a COEFFICIENT_OF_EFFICIENCY and/or INDEX_OF_AGREEMENT ',   &
           'keyword is supplied in a ',a,' block.')
           go to 9800
         end if
       end if
       if((jia.ne.0).or.(jce.ne.0))then
         if(exponent.eq.-9999)then
           write(amessage,250) trim(currentblock)
250        format('if a COEFFICIENT_OF_EFFICIENCY or INDEX_OF_AGREEMENT ',  &
           'keyword is supplied, an EXPONENT keyword must be supplied in ', &
           a,' block.')
           go to 9800
         end if
       end if
       if(exponent.ne.-9999)then
         if((jia.eq.0).and.(jce.eq.0))then
           write(amessage,251) trim(currentblock)
251        format('if an EXPONENT keyword is supplied, then a ',  &
           'COEFFICIENT_OF_EFFICIENCY or INDEX_OF_AGREEMENT keyword must ', &
           'also be supplied in a ',a,' block.')
           go to 9800
         end if
       end if           

! -- The two (maybe three) time series are checked for time consitency.

       call numterms(isterm,isbterm,iseterm,begdays,begsecs,enddays,endsecs,isseries)
       if(isterm.eq.0)then
         write(amessage,270) trim(series(isseries)%name)
270      format('there are no terms in time series "',a,'" between the provided ', &
         'dates and times.')
         go to 9800
       end if
       call numterms(ioterm,iobterm,ioeterm,begdays,begsecs,enddays,endsecs,ioseries)
       if(ioterm.eq.0)then
         write(amessage,270) trim(series(ioseries)%name)
         go to 9800
       end if
       if(isterm.ne.ioterm) go to 9300
       if(isterm.le.2) then
         write(amessage,271)
271      format('there must be at least two terms in the comparison time ', &
         'window of the nominated series.')
         go to 9800
       end if
       
       i=iobterm-1
       do j=isbterm,iseterm
         i=i+1
         if(series(isseries)%days(j).ne.(series(ioseries)%days(i))) go to 9300
         if(series(isseries)%secs(j).ne.(series(ioseries)%secs(i))) go to 9300
       end do
       
       if(ibseries.ne.0)then
         call numterms(ibterm,ibbterm,ibeterm,begdays,begsecs,enddays,endsecs,ibseries)
         if(ibterm.eq.0)then
           write(amessage,270) trim(series(ibseries)%name)
           go to 9800
         end if
         if(ibterm.ne.ioterm) go to 9400
         i=iobterm-1
         do j=ibbterm,ibeterm
           i=i+1
           if(series(ibseries)%days(j).ne.(series(ioseries)%days(i))) go to 9400
           if(series(ibseries)%secs(j).ne.(series(ioseries)%secs(i))) go to 9400
         end do
       end if

! The new c_table is initialized.

       do i=1,MAXCTABLE
         if(.not.ctable(i)%active) go to 300
       end do
       write(amessage,310)
310    format('no more C_TABLE''s available for data storage - increase MAXCTABLE and ', &
       'recompile program.')
       go to 9800
300    continue

       ctable(i)%active=.true.
       ctable(i)%name=aname
       ctable(i)%rec_icount=isterm
       ctable(i)%series_name_sim=series(isseries)%name
       ctable(i)%series_name_obs=series(ioseries)%name
       if(begdays.le.-99999990)then
         ctable(i)%rec_begdays=series(isseries)%days(1)
         ctable(i)%rec_begsecs=series(isseries)%secs(1)
       else
         ctable(i)%rec_begdays=begdays
         ctable(i)%rec_begsecs=begsecs
       end if
       if(enddays.ge.99999990)then
         iiterm=series(isseries)%nterm
         ctable(i)%rec_enddays=series(isseries)%days(iiterm)
         ctable(i)%rec_endsecs=series(isseries)%secs(iiterm)
       else
         ctable(i)%rec_enddays=enddays
         ctable(i)%rec_endsecs=endsecs
       end if

! -- The comparison statistics are now calculated.       
       
       tsum1=0.0
       tsum2=0.0
       tsum3=0.0
       tsum4=0.0 
       k=iobterm-1
       do j=isbterm,iseterm
         k=k+1
         rtemp=series(ioseries)%val(k)
!         if((jrbias.ne.0).or.(jrse.ne.0).or.(jns.ne.0))then
!           if(rtemp.le.0.0)then
!             write(amessage,280)
!280          format('RELATIVE_BIAS, RELATIVE_STANDARD_ERROR or NASH_SUTCLIFFE ', &
!             'coefficient cannot be calculated because at least one term in the ', &
!             'observation time series has a value equal to, or less than, zero.')
!             go to 9800
!           end if
!         end if
         rtemp1=series(isseries)%val(j)-rtemp
         tsum1=tsum1+rtemp1
         tsum2=tsum2+rtemp1*rtemp1
         tsum3=tsum3+rtemp
         if((jia.ne.0).or.(jce.ne.0))then
           tsum4=tsum4+abs(rtemp1)**exponent
         end if
       end do
       tsum3=tsum3/isterm
       if(jbias.ne.0)then
         ctable(i)%bias=tsum1/isterm
       else
         ctable(i)%bias=-1.0e37
       end if
       if(jse.ne.0)then
         ctable(i)%se=sqrt(tsum2/(isterm-1))
       else
         ctable(i)%se=-1.0e37
       end if
       if(jrbias.ne.0)then
         if(tsum3.eq.0.0)then
           ctable(i)%rbias=1.0e30
         else
           ctable(i)%rbias=tsum1/isterm/tsum3
         end if
       else
         ctable(i)%rbias=-1.0e37
       end if
       if((jrse.ne.0).or.(jns.ne.0))then
         tsum1=0.0
         k=iobterm-1
         do j=isbterm,iseterm
           k=k+1
           rtemp1=series(ioseries)%val(k)-tsum3
           tsum1=tsum1+rtemp1*rtemp1
         end do
         if(tsum1.le.0.0)then
           write(amessage,390) trim(series(ioseries)%name)
390        format('cannot compute RELATIVE_STANDARD_ERROR or NASH_SUTCLIFFE ', &
           'coefficient because observation time series "',a,'" is uniform ', &
           'in observation time window.')
           go to 9800
         end if
         if(jrse.ne.0)then
           ctable(i)%rse=sqrt(tsum2/(isterm-1))/sqrt(tsum1/(isterm-1))
         else
           ctable(i)%rse=-1.0e37
         end if
         if(jns.ne.0)then
           ctable(i)%ns=1.0-tsum2/tsum1
         else
           ctable(i)%ns=-1.0e37
         end if
       else
           ctable(i)%rse=-1.0e37
           ctable(i)%ns=-1.0e37           
       end if
       if(jce.ne.0)then
         tsum1=0.0
         k=iobterm-1
         if(ibseries.eq.0)then
           do j=isbterm,iseterm
             k=k+1
             rtemp1=(abs(series(ioseries)%val(k)-tsum3))**exponent
             tsum1=tsum1+rtemp1
           end do
           if(tsum1.le.0.0)then           
             write(amessage,410) trim(series(ioseries)%name)
410          format('cannot compute COEFFICIENT_OF_EFFICIENCY ', &
             'because observation time series "',a,'" is uniform ', &
             'in observation time window.')
             go to 9800
           end if
         else
           do j=ibbterm,ibeterm
             k=k+1
             rtemp1=(abs(series(ioseries)%val(k)-series(ibseries)%val(j)))**exponent
             tsum1=tsum1+rtemp1
           end do
           if(tsum1.le.0.0)then
             write(amessage,420) trim(series(ioseries)%name),  &
                                 trim(series(ibseries)%name)
420          format('cannot compute COEFFICIENT_OF_EFFICIENCY ', &
             'because observation time series "',a,'" is equal to ', &
             'baseline time series "',a,'" in observation time window.')             
             go to 9800
           end if
         end if
         ctable(i)%ce=1.0-tsum4/tsum1
       else
         ctable(i)%ce=-1.0e37
       end if
       if(jia.ne.0)then
         tsum1=0.0
         k=iobterm-1
         l=isbterm-1
         if(ibseries.eq.0)then
           do j=isbterm,iseterm
             k=k+1
             rtemp1=(abs(series(ioseries)%val(k)-tsum3)+   &
                     abs(series(isseries)%val(j)-tsum3))**exponent
             tsum1=tsum1+rtemp1
           end do
           if(tsum1.le.0.0)then
             write(amessage,430) trim(series(ioseries)%name), &
                                 trim(series(isseries)%name)
430          format('cannot compute INDEX_OF_AGREEMENT ', &
             'because observation time series "',a,'" and simulation ', &
             'time series "',a,'" are uniform and equal ', &
             'in observation time window.')
             go to 9800
           end if
         else
           do j=ibbterm,ibeterm
             k=k+1
             l=l+1
             rtemp1=(abs(series(ioseries)%val(k)-series(ibseries)%val(j))+  &
                     abs(series(isseries)%val(l)-series(ibseries)%val(j)))  &
                     **exponent
             tsum1=tsum1+rtemp1
           end do
           if(tsum1.le.0.0)then
             write(amessage,440) 
440          format('cannot compute INDEX_OF_AGREEMENT ', &
             'because observation time series, simulation time series ', &
             'and baseline time series are all equal in observation time ', &
             'window.')             
             go to 9800
           end if
         end if
         ctable(i)%ia=1.0-tsum4/tsum1
       else
         ctable(i)%ia=-1.0e37
       end if

       write(6,380) trim(aname)
       write(recunit,380) trim(aname)
380    format(t5,'Comparison statistics stored in C_TABLE "',a,'".')
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
9300   write(amessage,9310) 
9310   format('the two series cited in the COMPARE_SERIES block must have ',   &
       'identical sample dates and times within the comparison time ',  &
       'window. Maybe the use of a NEW_TIME_BASE block will rectify the problem.')       
       go to 9800
9400   write(amessage,9410)
9410   format('the baseline series cited in the COMPARE_SERIES block must ',   &
       'have identical sample dates and times within the comparison time ',    &
       'window to the simulated and observed series. Maybe the use of a ',     &
       'NEW_TIME_BASE block will rectify the problem.')
       go to 9800       

9800   call write_message(leadspace='yes',error='yes')
       call write_message(iunit=recunit,leadspace='yes')
       ifail=1

       return

end subroutine compare_series
!     Last change:  JD   24 Aug 2003    9:11 am
subroutine get_mul_series_tetrad(ifail)

! -- Subroutine GET_MUL_SERIES_TETRAD reads multiple series fron a TETRAD
!    PLT file.

       use tspvar
       use defn
       use inter
       implicit none

       integer, intent(out)   :: ifail

       integer dd1,mm1,yy1,hh1,nn1,ss1,dd2,mm2,yy2,hh2,nn2,ss2,ierr, &
       icontext,i,iunit,begdays,begsecs,enddays,endsecs,jline,j, &
       jseries,kseries,iwellname,ivarname,ddr,mmr,yyr,hhr,ssr,nnr,rdays,  &
       rsecs,nplot,ixcon,mdays,msecs,k,iterm,isplit,iseriesname,jj,kk
       integer jjseries(MAXSERIES),iname(MAXSERIES),iiterm(MAXSERIES)
       real rtemp,rtime
       character*12 atemp
       character*15 aline
       character*25 aoption
       character*120 afile
       character*12 wellname(MAXSERIES),varname(MAXSERIES)
       character*25 acontext(MAXCONTEXT)
       character*10 aname(MAXSERIES)

       ifail=0
       currentblock='GET_SERIES_TETRAD'

       write(*,10) trim(currentblock)
       write(recunit,10) trim(currentblock)
10     format(/,' Processing ',a,' block....')

       afile=' '
       icontext=0
       ixcon=0
       yy1=-9999
       hh1=-9999
       yy2=-9999
       hh2=-9999
       yyr=-9999
       hhr=-9999
       iwellname=1
       iseriesname=0
       ivarname=0
       jseries=0
       kseries=0
       iiterm=0               ! iiterm is a series.
       iunit=0

! -- The GET_SERIES_TETRAD block is first parsed.

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
         else if(aoption.eq.'DATE_2')then
           call read_date(ierr,dd2,mm2,yy2,'DATE_2')
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'TIME_1')then
           call read_time(ierr,hh1,nn1,ss1,'TIME_1')
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'TIME_2')then
           call read_time(ierr,hh2,nn2,ss2,'TIME_2')
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'WELL_NAME')then
           if(iwellname.eq.0)then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,42) trim(currentblock),trim(aline),trim(astring)
42           format('WELL_NAME keyword in wrong position in ',a,' block at line ',a, &
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
           call getfile(ierr,cline,wellname(jseries),left_word(2),right_word(2))
           if(ierr.ne.0)then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,57) trim(aline),trim(astring)
57           format('cannot read WELL_NAME from line ',a,' of file ',a)
             go to 9800
           end if
           call casetrans(wellname(jseries),'lo')
           call addquote(wellname(jseries),astring)
           write(*,46) trim(astring)
           write(recunit,46) trim(astring)
46         format(t5,'WELL_NAME ',a)
           iwellname=0
           ivarname=1
         else if(aoption.eq.'OBJECT_NAME')then
           if(ivarname.eq.0)then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,47) trim(currentblock),trim(aline),trim(astring)
47           format('OBJECT_NAME keyword can only follow a WELL_NAME keyword in ',  &
             a,' block at line ',a,' of file ',a)
             go to 9800
           end if
           call getfile(ierr,cline,varname(jseries),left_word(2),right_word(2))
           if(ierr.ne.0)then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,58) trim(aline),trim(astring)
58           format('cannot read OBJECT_NAME from line ',a,' of file ',a)
             go to 9800
           end if
           call casetrans(varname(jseries),'lo')
           call addquote(varname(jseries),astring)
           write(*,51) trim(astring)
           write(recunit,51) trim(astring)
51         format(t5,'OBJECT_NAME ',a)
           ivarname=0
           iseriesname=1
           aname(jseries)=' '
         else if(aoption.eq.'NEW_SERIES_NAME')then
           if(iseriesname.eq.0)then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,43) trim(currentblock),trim(aline),trim(astring)
43           format('NEW_SERIES_NAME keyword can only follow a OBJECT_NAME ',  &
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
           iwellname=1
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
         else if(aoption.eq.'MODEL_REFERENCE_DATE')then
           call read_date(ierr,ddr,mmr,yyr,'MODEL_REFERENCE_DATE')
           if(ierr.ne.0) go to 9800
           rdays=numdays(1,1,1970,ddr,mmr,yyr)
         else if(aoption.eq.'MODEL_REFERENCE_TIME')then
           call read_time(ierr,hhr,nnr,ssr,'MODEL_REFERENCE_TIME')
           if(ierr.ne.0) go to 9800
           rsecs=hhr*3600+nnr*60+ssr
         else if(aoption.eq.'END')then
           if(iseriesname.eq.1)then
             write(amessage,48) trim(currentblock)
48           format(a,' block END encountered before finding ', &
             'expected NEW_SERIES_NAME keyword.')
             go to 9800
           end if
           if(ivarname.eq.1)then
             write(amessage,56) trim(currentblock)
56           format(a,' block END encountered before finding ', &
             'expected NEW_OBJECT_NAME keyword.')
             go to 9800
           end if
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

! -- If there are any absences in the GET_SERIES_TETRAD block, these are now reported.

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
       if(jseries.eq.0)then
         call addquote(infile,astring)
         write(amessage,125) trim(currentblock),trim(astring)
125      format('no WELL_NAME keyword provided in ',a,' block in file ',a)
         go to 9800
       end if
       call date_check(ierr,yy1,mm1,dd1,hh1,nn1,ss1,yy2,mm2,dd2,hh2,nn2,ss2,  &
       begdays,begsecs,enddays,endsecs)
       if(ierr.ne.0) go to 9800
       if(begsecs.ge.86400)then
         begsecs=begsecs-86400
         begdays=begdays+1
       end if
       if(endsecs.ge.86400)then
         endsecs=endsecs-86400
         enddays=enddays+1
       end if
       if(yyr.eq.-9999)then
         call addquote(infile,astring)
         write(amessage,126) trim(currentblock),trim(astring)
126      format('no MODEL_REFERENCE_DATE keyword provided in ',a,' block in file ',a)
         go to 9800
       end if
       if(hhr.eq.-9999)then
         call addquote(infile,astring)
         write(amessage,127) trim(currentblock),trim(astring)
127      format('no MODEL_REFERENCE_TIME keyword provided in ',a,' block in file ',a)
         go to 9800
       end if
       if(jseries.gt.1)then
         do j=2,jseries
           do i=1,j-1
             if((wellname(j).eq.wellname(i)).and.(varname(j).eq.varname(i)))then
               call addquote(infile,astring)
               write(amessage,401) trim(currentblock),trim(astring)
401            format('two series possess the same WELL NAME and OBJECT NAME ',  &
               'in ',a,' block of file ',a)
               go to 9800
             end if
           end do
         end do
       end if

! -- There appear to be no errors in the block, so now it is processed.

       call addquote(afile,astring)
       write(*,179) trim(astring)
       write(recunit,179) trim(astring)
179    format(t5,'Reading TETRAD output file ',a,'....')
       iunit=nextunit()
       open(unit=iunit,file=afile,status='old',iostat=ierr)
       if(ierr.ne.0)then
         write(amessage,180) trim(astring),trim(currentblock)
180      format('cannot open file ',a,' cited in ',a,' block.')
         go to 9800
       end if

! -- The file is perused a first time to find out the storage requirements of the
!    time series.

       jline=0
190    continue
       do
         jline=jline+1
         read(iunit,'(a)',end=400) cline
         if(index(cline,'NPLOT').ne.0) exit
       end do
191    jline=jline+1
       read(iunit,'(a)',end=9300) cline
       call linesplit(ierr,3)
       if(ierr.ne.0)then
         call num2char(jline,aline)
         write(amessage,200) trim(aline),trim(astring)
200      format('there should be 3 entries on line ',a,' of file ',a)
         go to 9800
       end if
       call char2num(ierr,cline(left_word(1):right_word(1)),nplot)
       if(ierr.ne.0)then
         call num2char(jline,aline)
         write(amessage,220) trim(aline),trim(astring)
220      format('cannot read NPLOT from line ',a,' of file ',a)
         go to 9800
       end if
       if(nplot.gt.NUM_WORD_DIM)then
         call num2char(jline,aline)
         write(amessage,221) trim(aline),trim(astring)
221      format('NPLOT too large at line ',a,' of file ',a,'. Increase ',  &
         'NUM_WORD_DIM and re-compile program.')
         go to 9800
       end if
       call char2num(ierr,cline(left_word(2):right_word(2)),rtime)
       if(ierr.ne.0)then
         call num2char(jline,aline)
         write(amessage,223) trim(aline),trim(astring)
223      format('cannot read TIME from line ',a,' of file ',a)
         go to 9800
       end if
       mdays=rtime
       msecs=(rtime-mdays)*86400
       mdays=mdays+rdays
       msecs=msecs+rsecs
224    if(msecs.ge.86400)then
         msecs=msecs-86400
         mdays=mdays+1
         go to 224
       end if
       if((mdays.lt.begdays).or.((mdays.eq.begdays).and.(msecs.lt.begsecs)))then
         do
           jline=jline+1
           read(iunit,'(a)',end=400) cline
           if((index(cline,'NPLOT ').ne.0).and.(index(cline,' TIME').ne.0)) go to 191
         end do
       end if
       if((mdays.gt.enddays).or.                                  &
         ((mdays.eq.enddays).and.(msecs.gt.endsecs))) go to 400
       jline=jline+1
       read(iunit,'(a)',end=9300) cline
       jline=jline+1
       read(iunit,'(a)',end=9300) cline
       call linesplit(ierr,1)
       if(ierr.ne.0)then
         call num2char(jline,aline)
         write(amessage,230) trim(aline),trim(astring)
         go to 9800
       end if
       atemp=cline(left_word(1):right_word(1))
       call casetrans(atemp,'hi')
       if(atemp(1:5).ne.'NAMEW')then
         call num2char(jline,aline)
         write(amessage,230) trim(aline),trim(astring)
230      format('"NAMEW" string expected as first entry in line ',a,' of file ',a)
         go to 9800
       end if
       cline=cline(right_word(1)+1:)
       cline=adjustl(cline)
       iname=0                        ! iname is an array
       call linesplit(ierr,nplot)
       if(ierr.ne.0)then
         call num2char(jline,aline)
         write(amessage,240) trim(aline),trim(astring)
240      format('insufficient entries on line ',a,' of file ',a)
         go to 9800
       end if
       do i=1,nplot
         atemp=cline(left_word(i):right_word(i))
         call casetrans(atemp,'lo')
         do j=1,jseries
           if(varname(j).eq.atemp)then
             if(iname(j).ne.0)then
               call num2char(jline,aline)
               write(amessage,245) trim(aline),trim(astring)
245            format('object name mentioned twice on line ',a,' of file ',a)
               go to 9800
             end if
             iname(j)=i
           end if
         end do
       end do
       do
         jline=jline+1
         read(iunit,'(a)',end=400) cline
         if(cline.eq.' ') cycle
         if((index(cline,'NPLOT ').ne.0).and.(index(cline,' TIME').ne.0)) go to 191
         call linesplit(ierr,1)
         atemp=cline(left_word(1):right_word(1))
         call casetrans(atemp,'lo')
         do j=1,jseries
           if((wellname(j).eq.atemp).and.(iname(j).ne.0))iiterm(j)=iiterm(j)+1
         end do
       end do

400    continue

! -- Space is now allocated for the new series.

       do j=1,jseries
         k=jjseries(j)
         iterm=iiterm(j)
         if(iterm.eq.0)then
           write(amessage,405) trim(wellname(j)),trim(varname(j)),trim(astring)
405        format('no data can be assigned to the series pertaining to WELL NAME "', &
           a,'" and OBJECT NAME "',a,'" from file ',a)
           go to 9800
         end if
         allocate(series(k)%days(iterm),series(k)%secs(iterm),  &
         series(k)%val(iterm),stat=ierr)
         if(ierr.ne.0)then
           write(amessage,550)
550        format('cannot allocate memory for another time series.')
           go to 9800
         end if
         series(k)%active=.true.
         series(k)%name=aname(j)
         series(k)%type='ts'
         series(k)%nterm=iiterm(j)
       end do

! -- The TETRAD output file is now re-read and the time-series are imported.

       rewind(unit=iunit,iostat=ierr)
       if(ierr.ne.0)then
         write(amessage,460) trim(astring)
460      format('cannot rewind file ',a,' to import time series data.')
         go to 9800
       end if

       iiterm=0                 !iiterm is an array
       jline=0
490    continue
       do
         jline=jline+1
         read(iunit,'(a)',end=800) cline
         if(index(cline,'NPLOT').ne.0) exit
       end do
491    jline=jline+1
       read(iunit,'(a)',end=9300) cline
       call linesplit(ierr,3)
       call char2num(ierr,cline(left_word(1):right_word(1)),nplot)
       call char2num(ierr,cline(left_word(2):right_word(2)),rtime)
       mdays=rtime
       msecs=(rtime-mdays)*86400
       mdays=mdays+rdays
       msecs=msecs+rsecs
424    if(msecs.ge.86400)then
         msecs=msecs-86400
         mdays=mdays+1
         go to 424
       end if
       if((mdays.lt.begdays).or.((mdays.eq.begdays).and.(msecs.lt.begsecs)))then
         do
           jline=jline+1
           read(iunit,'(a)',end=400) cline
           if((index(cline,'NPLOT ').ne.0).and.(index(cline,' TIME').ne.0)) go to 491
         end do
       end if
       if((mdays.gt.enddays).or.                              &
         ((mdays.eq.enddays).and.(msecs.gt.endsecs))) go to 800
       jline=jline+1
       read(iunit,'(a)',end=9300) cline
       jline=jline+1
       read(iunit,'(a)',end=9300) cline
       call linesplit(ierr,1)
       cline=cline(right_word(1)+1:)
       cline=adjustl(cline)
       iname=0                        ! iname is an array
       call linesplit(ierr,nplot)
       do i=1,nplot
         atemp=cline(left_word(i):right_word(i))
         call casetrans(atemp,'lo')
         do j=1,jseries
           if(varname(j).eq.atemp)then
             iname(j)=i
           end if
         end do
       end do
       do
         jline=jline+1
         read(iunit,'(a)',end=800) cline
         if(cline.eq.' ') cycle
         if((index(cline,'NPLOT ').ne.0).and.(index(cline,' TIME').ne.0)) go to 491
         call linesplit(ierr,1)
         isplit=0
         atemp=cline(left_word(1):right_word(1))
         call casetrans(atemp,'lo')
         do j=1,jseries
           if(wellname(j).eq.atemp)then
             if(iname(j).ne.0)then
               if(isplit.eq.0)then
                 isplit=1
                 cline=cline(right_word(1)+1:)
                 call linesplit(ierr,nplot)
               end if
               jj=iname(j)
               call char2num(ierr,cline(left_word(jj):right_word(jj)),rtemp)
               if(ierr.ne.0)then
                 call num2char(jline,aline)
                 write(amessage,520) trim(varname(j)),trim(aline),trim(astring)
520              format('cannot read "',a,'" object from line ',a,' of file ',a)
                 go to 9800
               end if
               k=jjseries(j)
               iiterm(j)=iiterm(j)+1
               kk=iiterm(j)
               series(k)%val(kk)=rtemp
               series(k)%days(kk)=mdays
               series(k)%secs(kk)=msecs
               if(kk.gt.1)then
                 if((series(k)%days(kk).eq.series(k)%days(kk-1)).and.   &
                    (series(k)%secs(kk).eq.series(k)%secs(kk-1)))then
                    call num2char(jline,aline)
                    write(amessage,551) trim(wellname(j)),trim(aline),trim(astring)
551                 format('well "',a,'" appears twice in one block at line ',a,  &
                    ' of file ',a)
                    go to 9800
                 end if
               end if
             end if
           end if
         end do
465      continue
       end do

800    continue
       do j=1,jseries
         write(*,860) trim(aname(j)),trim(astring)
         write(recunit,860) trim(aname(j)),trim(astring)
860      format(t5,'Series "',a,'" successfully imported from file ',a)
       end do

       go to 9900

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
9300   continue
       write(amessage,9310) trim(astring)
9310   format('premature end encountered to TETRAD output file ',a)
       go to 9800

9800   call write_message(leadspace='yes',error='yes')
       call write_message(iunit=recunit,leadspace='yes')
       ifail=1

9900   if(iunit.ne.0)close(unit=iunit,iostat=ierr)
       return


end subroutine get_mul_series_tetrad



subroutine get_mul_series_ssf(ifail)

! -- Subroutine GET_MUL_SERIES_SSF reads multiple series fron a site
!    sample file.

       use tspvar
       use defn
       use inter
       implicit none

       integer, intent(out)   :: ifail

       integer dd1,mm1,yy1,hh1,nn1,ss1,dd2,mm2,yy2,hh2,nn2,ss2,ierr, &
       icontext,i,iunit,begdays,begsecs,enddays,endsecs,jline,j, &
       jseries,kseries,ixcon,k,isite,iseriesname,jj,iactive,nn,ss,iterm
       integer jjseries(MAXSERIES),iiterm(MAXSERIES)
       double precision dvalue
       character*10 bsite,lastsite
       character*15 aline
       character*25 aoption
       character*120 afile
       character*10 site(MAXSERIES)
       character*25 acontext(MAXCONTEXT)
       character*10 aname(MAXSERIES)

       ifail=0
       currentblock='GET_MUL_SERIES_SSF'

       write(*,10) trim(currentblock)
       write(recunit,10) trim(currentblock)
10     format(/,' Processing ',a,' block....')

       afile=' '
       icontext=0
       ixcon=0
       yy1=-9999
       hh1=-9999
       yy2=-9999
       hh2=-9999
       isite=1
       iseriesname=0
       jseries=0
       kseries=0
       iiterm=0               ! iiterm is a series.

! -- The GET_MUL_SERIES_SSF block is first parsed.

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
         else if(aoption.eq.'DATE_2')then
           call read_date(ierr,dd2,mm2,yy2,'DATE_2')
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'TIME_1')then
           call read_time(ierr,hh1,nn1,ss1,'TIME_1')
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'TIME_2')then
           call read_time(ierr,hh2,nn2,ss2,'TIME_2')
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'SITE')then
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
           call getfile(ierr,cline,site(jseries),left_word(2),right_word(2))
           if(ierr.ne.0)then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,57) trim(aline),trim(astring)
57           format('cannot read SITE name from line ',a,' of file ',a)
             go to 9800
           end if
           call casetrans(site(jseries),'lo')
           call addquote(site(jseries),astring)
           write(*,46) trim(astring)
           write(recunit,46) trim(astring)
46         format(t5,'SITE ',a)
           isite=0
           iseriesname=1
           aname(jseries)=' '
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
           if(iseriesname.eq.1)then
             write(amessage,48) trim(currentblock)
48           format(a,' block END encountered before finding ', &
             'expected NEW_SERIES_NAME keyword.')
             go to 9800
           end if
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

! -- If there are any absences in the GET_MUL_SERIES_SSF block, these are now reported.

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
       if(jseries.eq.0)then
         call addquote(infile,astring)
         write(amessage,125) trim(currentblock),trim(astring)
125      format('no SITE keyword provided in ',a,' block in file ',a)
         go to 9800
       end if
       call date_check(ierr,yy1,mm1,dd1,hh1,nn1,ss1,yy2,mm2,dd2,hh2,nn2,ss2,  &
       begdays,begsecs,enddays,endsecs)
       if(ierr.ne.0) go to 9800
       if(begsecs.ge.86400)then
         begsecs=begsecs-86400
         begdays=begdays+1
       end if
       if(endsecs.ge.86400)then
         endsecs=endsecs-86400
         enddays=enddays+1
       end if
       if(jseries.gt.1)then
         do j=2,jseries
           do i=1,j-1
             if(site(j).eq.site(i))then
               call addquote(infile,astring)
               write(amessage,401) trim(currentblock),trim(astring)
401            format('two series possess the same SITE name ',  &
               'in ',a,' block of file ',a)
               go to 9800
             end if
           end do
         end do
       end if

! -- There appear to be no errors in the block, so now it is processed.

       call addquote(afile,astring)
       write(*,179) trim(astring)
       write(recunit,179) trim(astring)
179    format(t5,'Reading site sample file ',a,'....')
       iunit=nextunit()
       open(unit=iunit,file=afile,status='old',iostat=ierr)
       if(ierr.ne.0)then
         write(amessage,180) trim(astring),trim(currentblock)
180      format('cannot open file ',a,' cited in ',a,' block.')
         go to 9800
       end if

! -- The file is perused a first time to find out the storage requirements of the
!    time series.

       iiterm=0          ! iiterm is an array
       jline=0
       lastsite=' '
       iactive=0
       do
         jline=jline+1
         read(iunit,'(a)',err=9200,end=500)cline
         call linesplit(ierr,4)
         if(ierr.lt.0) then
           cycle
         else if(ierr.gt.0)then
           call num2char(jline,aline)
           write(amessage,375) trim(aline),trim(astring)
375        format('four entries expected on line ',a,' of site sample file ',a)
           go to 9800
         end if
         bsite=cline(left_word(1):right_word(1))
         call casetrans(bsite,'lo')
         if(bsite.ne.lastsite)then
           lastsite=bsite
           do j=1,jseries
             if(bsite.eq.site(j))then
               iactive=1
               go to 376
             end if
           end do
           iactive=0
376        continue
         end if
         if(iactive.eq.0) cycle
         if(cline(right_word(4):).ne.' ')then
           do k=right_word(4)+1,len_trim(cline)
             if(cline(k:k).ne.' ')then
               if(cline(k:k).eq.'x') go to 379
               go to 378
             end if
           end do
         end if
378      continue
         call read_rest_of_sample_line(ierr,4,nn,ss,dvalue,jline,afile)
         if(ierr.ne.0)then
           call write_message(iunit=recunit,leadspace='yes',error='yes')
           ifail=1
           return
         end if
         if(ss.ge.86400)then
           ss=ss-86400
           nn=nn+1
         end if
         if(iiterm(j).eq.0)then
           if((nn.lt.begdays).or.((nn.eq.begdays).and.(ss.lt.begsecs))) &
           cycle
         end if
         if((nn.gt.enddays).or.((nn.eq.enddays).and.(ss.gt.endsecs))) then
           iactive=0
           go to 379
         end if
         iiterm(j)=iiterm(j)+1
379      continue
       end do

500    continue

! -- Space is now allocated for the new series.

       do j=1,jseries
         k=jjseries(j)
         iterm=iiterm(j)
         if(iterm.eq.0)then
           write(amessage,405) trim(site(j)),trim(astring)
405        format('no data can be assigned to the series pertaining to SITE "', &
           a,'" from file ',a)
           go to 9800
         end if
         allocate(series(k)%days(iterm),series(k)%secs(iterm),  &
         series(k)%val(iterm),stat=ierr)
         if(ierr.ne.0)then
           write(amessage,550)
550        format('cannot allocate memory for another time series.')
           go to 9800
         end if
         series(k)%active=.true.
         series(k)%name=aname(j)
         series(k)%type='ts'
         series(k)%nterm=iiterm(j)
       end do

! -- The site sample file is now read a second time and the data is imported.

       rewind(unit=iunit,iostat=ierr)
       if(ierr.ne.0)then
         write(amessage,370) trim(astring)
370      format('cannot re-wind site sample file ',a)
         go to 9800
       end if

       iiterm=0          ! iiterm is an array
       jline=0
       lastsite=' '
       iactive=0
       do
         jline=jline+1
         read(iunit,'(a)',err=9200,end=800)cline
         call linesplit(ierr,4)
         if(ierr.lt.0) cycle
         bsite=cline(left_word(1):right_word(1))
         call casetrans(bsite,'lo')
         if(bsite.ne.lastsite)then
           lastsite=bsite
           do j=1,jseries
             if(bsite.eq.site(j))then
               iactive=1
               jj=jjseries(j)
               go to 576
             end if
           end do
           iactive=0
576        continue
         end if
         if(iactive.eq.0) cycle
         if(cline(right_word(4):).ne.' ')then
           do k=right_word(4)+1,len_trim(cline)
             if(cline(k:k).ne.' ')then
               if(cline(k:k).eq.'x') go to 579
               go to 578
             end if
           end do
         end if
578      continue
         call read_rest_of_sample_line(ierr,4,nn,ss,dvalue,jline,afile)
         if(ss.ge.86400)then
           ss=ss-86400
           nn=nn+1
         end if
         if(iiterm(j).eq.0)then
           if((nn.lt.begdays).or.((nn.eq.begdays).and.(ss.lt.begsecs))) &
           cycle
         end if
         if((nn.gt.enddays).or.((nn.eq.enddays).and.(ss.gt.endsecs))) then
           iactive=0
           go to 579
         end if
         iiterm(j)=iiterm(j)+1
         iterm=iiterm(j)
         series(jj)%days(iterm)=nn
         series(jj)%secs(iterm)=ss
         series(jj)%val(iterm)=dvalue
579      continue
       end do

800    continue
       do j=1,jseries
         write(*,860) trim(aname(j)),trim(astring)
         write(recunit,860) trim(aname(j)),trim(astring)
860      format(t5,'Series "',a,'" successfully imported from file ',a)
       end do

       go to 9900

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

9900   close(unit=iunit,iostat=ierr)
       return


end subroutine get_mul_series_ssf


subroutine series_base_level(ifail)

! -- Subroutine SERIES_BASE_LEVEL subtracts a constant amount from a series, this
!    amount being an element of the same or another series.

       use tspvar
       use defn
       use inter
       implicit none

       integer, intent(out)   :: ifail

       integer icontext,iseries,ixcon,ierr,isub,jseries,bseries,ddb,mmb,yyb, &
       hhb,nnb,ssb,daysb,secsb,iterm,i,j,ineg
       real rbase
       character*10 aname,atemp
       character*15 aline
       character*25 aoption
       character*25 acontext(MAXCONTEXT)

       ifail=0
       currentblock='SERIES_BASE_LEVEL'

       write(*,10) trim(currentblock)
       write(recunit,10) trim(currentblock)
10     format(/,' Processing ',a,' block....')

       icontext=0
       iseries=0
       aname=' '
       ixcon=0
       isub=-9999
       jseries=-9999
       bseries=-9999
       ddb=-9999
       hhb=-9999
       ineg=0

! -- The SERIES_BASE_LEVEL block is first parsed.

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
         if(aoption.eq.'CONTEXT')then
           if(ixcon.ne.0)then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,41) trim(aline),trim(astring)
41           format('CONTEXT keyword in incorrect location at line ',a,' of file ',a)
             go to 9800
           end if
           call read_context(ierr,icontext,acontext)
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'SUBSTITUTE')then
           call getfile(ierr,cline,atemp,left_word(2),right_word(2))
           if(atemp.eq.'yes')then
             isub=1
           else if(atemp.eq.'no')then
             isub=0
           else
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,42) trim(aline),trim(astring)
42           format('"yes" or "no" should follow the SUBSTITUTE ', &
             'keyword at line ',a,' of file ',a)
             go to 9800
           end if
           write(*,44) trim(aoption),trim(atemp)
           write(recunit,44) trim(aoption),trim(atemp)
44         format(t5,a,1x,a)
         else if(aoption.eq.'NEW_SERIES_NAME')then
           call read_new_series_name(ierr,aname)
           if(ierr.ne.0) go to 9800
           jseries=1
         else if(aoption.eq.'SERIES_NAME')then
           call read_series_name(ierr,iseries,'SERIES_NAME')
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'BASE_LEVEL_SERIES_NAME')then
           call read_series_name(ierr,bseries,'BASE_LEVEL_SERIES_NAME')
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'BASE_LEVEL_DATE')then
           call read_date(ierr,ddb,mmb,yyb,'BASE_LEVEL_DATE')
           if(ierr.ne.0) go to 9800
           daysb=numdays(1,1,1970,ddb,mmb,yyb)
         else if(aoption.eq.'BASE_LEVEL_TIME')then
           call read_time(ierr,hhb,nnb,ssb,'BASE_LEVEL_TIME')
           if(ierr.ne.0) go to 9800
           secsb=hhb*3600+nnb*60+ssb
         else if(aoption.eq.'NEGATE')then
           call getfile(ierr,cline,atemp,left_word(2),right_word(2))
           if(atemp.eq.'yes')then
             ineg=1
           else if(atemp.eq.'no')then
             ineg=0
           else
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,49) trim(aline),trim(astring)
49           format('"yes" or "no" should follow the NEGATE ', &
             'keyword at line ',a,' of file ',a)
             go to 9800
           end if
           write(*,44) trim(aoption),trim(atemp)
           write(recunit,44) trim(aoption),trim(atemp)
         else if(aoption.eq.'END')then
           go to 200
         else
           call num2char(iline,aline)
           call addquote(infile,astring)
           write(amessage,90) trim(aoption),trim(currentblock),trim(aline),trim(astring)
90         format('unexpected keyword - "',a,'" in ',a,' block at line ',a, &
           ' of file ',a)
           go to 9800
         end if
       end do

! -- The block has been read; now it is checked for correctness.

200    continue
       if(iseries.eq.0)then
         write(amessage,210) trim(currentblock)
210      format('no SERIES_NAME keyword provided in ',a,' block.')
         go to 9800
       end if
       if(isub.eq.-9999)then
         write(amessage,211) trim(currentblock)
211      format('no SUBSTITUTE keyword supplied in ',a,' block.')
         go to 9800
       end if
       if((isub.eq.1).and.(jseries.ne.-9999))then
         write(amessage,220) trim(currentblock)
220      format('if SUBSTITUTE is set to "yes" then a NEW_SERIES_NAME ', &
         'keyword must not be supplied in ',a,' block.')
         go to 9800
       end if
       if((isub.eq.0).and.(jseries.eq.-9999))then
         write(amessage,222) trim(currentblock)
222      format('if SUBSTITUTE is set to "no" then a NEW_SERIES_NAME ', &
         'keyword must be supplied in ',a,' block.')
         go to 9800
       end if
       if(bseries.eq.-9999)then
         write(amessage,230) trim(currentblock)
230      format('no BASE_LEVEL_SERIES_NAME keyword supplied in ',a,' block.')
         go to 9800
       end if
       if(ddb.eq.-9999)then
         write(amessage,240) trim(currentblock)
240      format('no BASE_LEVEL_DATE keyword supplied in ',a,' block.')
         go to 9800
       end if
       if(hhb.eq.-9999)then
         write(amessage,250) trim(currentblock)
250      format('no BASE_LEVEL_TIME keyword supplied in ',a,' block.')
         go to 9800
       end if
       if(secsb.ge.86400)then
         daysb=daysb+1
         secsb=secsb-86400
       end if
       if(icontext.eq.0)then
         write(amessage,260) trim(currentblock)
260      format('no CONTEXT keyword(s) provided in ',a,' block.')
         go to 9800
       end if

! -- The new series base level is now determined.

       do i=1,series(bseries)%nterm
         if((series(bseries)%days(i).eq.daysb).and.  &
            (series(bseries)%secs(i).eq.secsb))then
            rbase=series(bseries)%val(i)
            go to 300
         end if
       end do
       write(amessage,280) trim(series(bseries)%name),trim(currentblock)
280    format('no member of BASE_LEVEL_SERIES "',a,'" has a date and time ', &
       'corresponding to those supplied with the BASE_LEVEL_DATE and ', &
       'BASE_LEVEL_TIME keywords in ',a,' block.')
       go to 9800
300    continue

! -- If no new series is required, the base level change is now undertaken.

       if(jseries.eq.-9999)then
         if(ineg.eq.0)then
           do i=1,series(iseries)%nterm
             series(iseries)%val(i)=series(iseries)%val(i)-rbase
           end do
         else
           do i=1,series(iseries)%nterm
             series(iseries)%val(i)=rbase-series(iseries)%val(i)
           end do
         end if
         go to 900
       end if

! -- If a new time series is warranted, then space is allocated for it.

       if(jseries.ne.-9999)then
         do i=1,MAXSERIES
           if(.not.series(i)%active) go to 515
         end do
         write(amessage,510)
510      format('no more time series available for data storage - increase MAXSERIES and ', &
         'recompile program.')
         go to 9800

515      continue
         iterm=series(iseries)%nterm
         allocate(series(i)%days(iterm),series(i)%secs(iterm),  &
         series(i)%val(iterm),stat=ierr)
         if(ierr.ne.0)then
           write(amessage,550)
550        format('cannot allocate memory for another time series.')
           go to 9800
         end if
         series(i)%active=.true.
         series(i)%name=aname
         series(i)%nterm=iterm
         series(i)%type='ts'
         do j=1,series(iseries)%nterm
           series(i)%days(j)=series(iseries)%days(j)
         end do
         do j=1,series(iseries)%nterm
           series(i)%secs(j)=series(iseries)%secs(j)
         end do
         if(ineg.eq.0)then
           do j=1,series(iseries)%nterm
             series(i)%val(j)=series(iseries)%val(j)-rbase
           end do
         else
           do j=1,series(iseries)%nterm
             series(i)%val(j)=rbase-series(iseries)%val(j)
           end do
         end if
       end if

900    continue
       if(jseries.eq.-9999)then
         write(*,910) trim(series(iseries)%name)
         write(recunit,910) trim(series(iseries)%name)
910      format(t5,'New base level applied to series "',a,'".')
       else
         write(*,920) trim(series(i)%name)
         write(recunit,920) trim(series(i)%name)
920      format(t5,'New series "',a,'" successfully calculated.')
       end if
       return

9000   call num2char(iline,aline)
       call addquote(infile,astring)
       write(amessage,9010) trim(aline), trim(astring)
9010   format('cannot read line ',a,' of TSPROC input file ',a)
       go to 9800
9100   continue
       call addquote(infile,astring)
       write(amessage,9110) trim(astring), trim(currentblock)
9110   format('unexpected end encountered to TSPROC input file ',a,' while ', &
       ' reading ',a,' block.')
       go to 9800

9800   call write_message(leadspace='yes',error='yes')
       call write_message(iunit=recunit,leadspace='yes')
       ifail=1

       return

end subroutine series_base_level



subroutine vol_to_series(ifail)

! -- Subroutine VOL_TO_SERIES stores a V_TABLE as an S_TABLE.

       use tspvar
       use defn
       use inter
       implicit none

       integer, intent(out)   :: ifail

       integer ivtable,nsterm,idiff,ihalf,isecs,icontext,ixcon,ierr,iser, &
       j,idays
       character*10 aname,abscissa
       character*15 aline
       character*25 aoption
       character*25 acontext(MAXCONTEXT)

       ifail=0
       currentblock='V_TABLE_TO_SERIES'

       write(*,10) trim(currentblock)
       write(recunit,10) trim(currentblock)
10     format(/,' Processing ',a,' block....')

       ivtable=0
       icontext=0
       abscissa=' '
       aname=' '
       ixcon=0

! -- The V_TABLE_TO_SERIES block is first parsed.

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
         if(aoption.eq.'V_TABLE_NAME')then
           call read_table_name(ierr,ivtable,2)
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'NEW_SERIES_NAME')then
           call read_new_series_name(ierr,aname)
           if(ierr.ne.0) go to 9800
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
         else if(aoption.eq.'TIME_ABSCISSA')then
           call getfile(ierr,cline,abscissa,left_word(2),right_word(2))
           if(ierr.ne.0)then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,49) trim(aline),trim(astring)
49           format('cannot read time abscissa from line ',a,' of file ',a)
             go to 9800
           end if                                        
           call casetrans(abscissa,'lo')
           if(abscissa.eq.'center')abscissa='centre'
           if((abscissa.ne.'start').and.   &
              (abscissa.ne.'centre').and.  &
              (abscissa.ne.'end'))then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,55) trim(aline),trim(astring)
55           format('time abscissa must be "start", "centre" or "end" ', &
             'at line ',a,' of file ',a)
             go to 9800
           end if             
           write(*,60) trim(abscissa)
           write(recunit,60) trim(abscissa)
60         format(t5,'TIME_ABSCISSA ',a)
         else if(aoption.eq.'END')then
           go to 200
         else
           call num2char(iline,aline)
           call addquote(infile,astring)
           write(amessage,90) trim(aoption),trim(currentblock),trim(aline),trim(astring)
90         format('unexpected keyword - "',a,'" in ',a,' block at line ',a, &
           ' of file ',a)
           go to 9800
         end if
       end do

! -- The block has been read; now it is checked for correctness.

200    continue
       if(ivtable.eq.0)then
         write(amessage,210) trim(currentblock)
210      format('no V_TABLE_NAME keyword provided in ',a,' block.')
         go to 9800
       end if
       if(aname.eq.' ')then
         write(amessage,230) trim(currentblock)
230      format('no NEW_SERIES_NAME keyword provided in ',a,' block.')
         go to 9800
       end if
       if(icontext.eq.0)then
         write(amessage,220) trim(currentblock)
220      format('no CONTEXT keyword(s) provided in ',a,' block.')
         go to 9800
       end if
       if(abscissa.eq.' ')then
         write(amessage,235) trim(currentblock)
235      format('no TIME_ABSCISSA keyword provided in ',a,' block.')
         go to 9800
       end if         

! -- The new time series is now written.

       do iser=1,MAXSERIES
         if(.not.series(iser)%active) go to 370
       end do
       write(amessage,360)
360    format('no more time series available for data storage - increase MAXSERIES and ', &
       'recompile program.')
       go to 9800

370    continue
       nsterm=vtable(ivtable)%nterm
       allocate(series(iser)%days(nsterm),series(iser)%secs(nsterm),  &
       series(iser)%val(nsterm),stat=ierr)
       if(ierr.ne.0)then
         write(amessage,380)
380      format('cannot allocate memory for another time series.')
         go to 9800
       end if
       series(iser)%active=.true.
       series(iser)%name=aname
       series(iser)%nterm=nsterm
       series(iser)%type='ts'
       if(abscissa.eq.'start')then
         do j=1,nsterm
           series(iser)%days(j)=vtable(ivtable)%days1(j)
         end do
         do j=1,nsterm
           series(iser)%secs(j)=vtable(ivtable)%secs1(j)
         end do
       else if(abscissa.eq.'end')then
         do j=1,nsterm
           series(iser)%days(j)=vtable(ivtable)%days2(j)
         end do
         do j=1,nsterm
           series(iser)%secs(j)=vtable(ivtable)%secs2(j)
         end do
       else
         do j=1,nsterm
           idiff=vtable(ivtable)%days2(j)-vtable(ivtable)%days1(j)
           ihalf=idiff/2
           idays=vtable(ivtable)%days1(j)+ihalf
           if(ihalf*2.eq.idiff)then
             isecs=(vtable(ivtable)%secs1(j)+vtable(ivtable)%secs2(j))/2
           else
             isecs=(vtable(ivtable)%secs1(j)+vtable(ivtable)%secs2(j))/2+43200
           end if
385        if(isecs.ge.86400)then
             isecs=isecs-86400
             idays=idays+1
             go to 385
           end if
           series(iser)%days(j)=idays
           series(iser)%secs(j)=isecs
         end do
       end if                     
       do j=1,nsterm
         series(iser)%val(j)=vtable(ivtable)%vol(j)
       end do
       
       write(6,390) trim(aname)
       write(recunit,390) trim(aname)
390    format(t5,'Data from v_table stored in series "',a,'".')
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

9800   call write_message(leadspace='yes',error='yes')
       call write_message(iunit=recunit,leadspace='yes')
       ifail=1

       return

end subroutine vol_to_series



subroutine moving_window(ifail)

! -- Subroutine MOVING is still quick and dirty. It calculates the minimum sample
!    value within a window consisting of an odd number of terms.

       use tspvar
       use defn
       use inter
       implicit none

       integer, intent(out)   :: ifail

       integer icontext,iseries,ixcon,ierr,itemp,iterm,i,j,wt2,l,winterms,imode,  &
       icount,is,ie,iiterm,k
       real rtemp,first_value,last_value
       character*10 aname,atemp
       character*15 aline,amode
       character*25 aoption
       character*25 acontext(MAXCONTEXT)

       ifail=0
       currentblock='MOVING_MINIMUM'

       write(*,10) trim(currentblock)
       write(recunit,10) trim(currentblock)
10     format(/,' Processing ',a,' block....')

       icontext=0
       iseries=0
       aname=' '
       winterms=-99999999
       ixcon=0
       amode=' '
       first_value=-1.1e30
       last_value=-1.1e30

! -- The MOVING_MINIMUM block is first parsed.

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
         if(aoption.eq.'CONTEXT')then
           if(ixcon.ne.0)then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,41) trim(aline),trim(astring)
41           format('CONTEXT keyword in incorrect location at line ',a,' of file ',a)
             go to 9800
           end if
           call read_context(ierr,icontext,acontext)
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'TERMS_IN_WINDOW')then
           call get_keyword_value(ierr,1,winterms,rtemp,aoption)
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'FIRST_VALUE')then
           call get_keyword_value(ierr,2,itemp,first_value,aoption)
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'LAST_VALUE')then
           call get_keyword_value(ierr,2,itemp,last_value,aoption)
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'NEW_SERIES_NAME')then
           call read_new_series_name(ierr,aname)
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'SERIES_NAME')then
           call read_series_name(ierr,iseries,'SERIES_NAME')
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'MODE')then
           amode=cline(left_word(2):right_word(2))
           call casetrans(amode,'lo')
           write(*,89) trim(amode)
           write(recunit,89) trim(amode)
89         format(t5,'MODE ',a)
         else if(aoption.eq.'END')then
           go to 200
         else
           call num2char(iline,aline)
           call addquote(infile,astring)
           write(amessage,90) trim(aoption),trim(currentblock),trim(aline),trim(astring)
90         format('unexpected keyword - "',a,'" in ',a,' block at line ',a, &
           ' of file ',a)
           go to 9800
         end if
       end do

! -- The block has been read; now it is checked for correctness.

200    continue
       if(iseries.eq.0)then
         write(amessage,210) trim(currentblock)
210      format('no SERIES_NAME keyword provided in ',a,' block.')
         go to 9800
       end if
       if(aname.eq.' ')then
         write(amessage,230) trim(currentblock)
230      format('no NEW_SERIES_NAME provided in ',a,' block.')
         go to 9800
       end if
       if(amode.eq.' ')then
         write(amessage,231) trim(currentblock)
231      format('no MODE keyword provided in ',a,' block.')
         go to 9800
       end if
       if(icontext.eq.0)then
         write(amessage,220) trim(currentblock)
220      format('no CONTEXT keyword(s) provided in ',a,' block.')
         go to 9800
       end if
       if(winterms.eq.-99999999)then
         write(amessage,225) trim(currentblock)
225      format('no TERMS_IN_WINDOW keyword(s)provided in ',a,' block.')
         go to 9800
       else
         if(winterms.le.0)then
           write(amessage,226) trim(currentblock)
226        format('value for TERMS_IN_WINDOW must be positve in ',a,' block.')
           go to 9800
         end if
         if((winterms/2)*2.eq.winterms)then
           write(amessage,227) trim(currentblock)
227        format('TERMS_IN_WINDOW must be an odd number in ',a,' block.')
           go to 9800
         end if
       end if
       if(amode.eq.'continuous')then
         imode=1
       else if(amode.eq.'discrete')then
         imode=2
       else
         write(amessage,228) trim(currentblock)
228      format('MODE must be "discrete" or "continuous" in ',a,' block.')
         go to 9800
       end if
       if(imode.eq.2)then
         if(first_value.lt.-1.0e30)then
           write(amessage,340) trim(currentblock)
340        format('no FIRST_VALUE keyword supplied in ',a,' block.')
           go to 9800
         end if
         if(last_value.lt.-1.0e30)then
           write(amessage,341) trim (currentblock)
341        format('no LAST_VALUE keyword supplied in ',a,' block.')
           go to 9800
         end if
       end if

! -- The new series is now written.

       if(imode.eq.2) go to 900
       iterm=series(iseries)%nterm
       do i=1,MAXSERIES
         if(.not.series(i)%active) go to 515
       end do
       write(amessage,510)
510    format('no more time series available for data storage - increase MAXSERIES and ', &
       'recompile program.')
       go to 9800

515    allocate(series(i)%days(iterm),series(i)%secs(iterm),  &
       series(i)%val(iterm),stat=ierr)
       if(ierr.ne.0)then
         write(amessage,550)
550      format('cannot allocate memory for another time series.')
         go to 9800
       end if
       series(i)%active=.true.
       series(i)%name=aname
       series(i)%nterm=iterm
       series(i)%type='ts'
       do j=1,iterm
         series(i)%days(j)=series(iseries)%days(j)
       end do
       do j=1,iterm
         series(i)%secs(j)=series(iseries)%secs(j)
       end do
       wt2=winterms/2
       if(iterm.le.wt2*2)then
         do j=1,iterm
           series(i)%val(j)=series(iseries)%val(j)
         end do
       else
         do j=1,wt2
           series(i)%val(j)=series(iseries)%val(j)
         end do
         itemp=iterm-wt2+1
         do j=itemp,iterm
           series(i)%val(j)=series(iseries)%val(j)
         end do
         do j=wt2+1,itemp-1
           rtemp=1e30
           do l=j-wt2,j+wt2
             if(series(iseries)%val(l).lt.rtemp)rtemp=series(iseries)%val(l)
           end do
           series(i)%val(j)=rtemp
         end do
       end if

       write(*,590) trim(aname)
       write(recunit,590) trim(aname)
590    format(t5,'Series "',a,'" successfully calculated.')
       return

900    continue

! -- The following refers to discrete mode.
!    First we find out how many terms will be required.

       icount=0
       iterm=series(iseries)%nterm
       wt2=winterms/2
       is=wt2+1
       ie=iterm-wt2
       do j=is,ie
         rtemp=series(iseries)%val(j)
         do k=j-wt2,j+wt2
            if(j.eq.k) cycle
           if(rtemp.ge.series(iseries)%val(k)) go to 930
         end do
         icount=icount+1
930      continue
       end do

       do i=1,MAXSERIES
         if(.not.series(i)%active) go to 1515
       end do
       write(amessage,510)
       go to 9800
1515   continue
       iiterm=icount+2
       allocate(series(i)%days(iiterm),series(i)%secs(iiterm),  &
       series(i)%val(iiterm),stat=ierr)
       if(ierr.ne.0)then
         write(amessage,550)
         go to 9800
       end if
       series(i)%active=.true.
       series(i)%name=aname
       series(i)%nterm=iiterm
       series(i)%type='ts'
       series(i)%val(1)=first_value
       series(i)%days(1)=series(iseries)%days(1)
       series(i)%secs(1)=series(iseries)%secs(1)
       series(i)%val(iiterm)=last_value
       series(i)%days(iiterm)=series(iseries)%days(iterm)
       series(i)%secs(iiterm)=series(iseries)%secs(iterm)
       icount=1
       do j=is,ie
         rtemp=series(iseries)%val(j)
         do k=j-wt2,j+wt2
           if(j.eq.k) cycle
           if(rtemp.ge.series(iseries)%val(k)) go to 950
         end do
         icount=icount+1
         series(i)%val(icount)=series(iseries)%val(j)
         series(i)%days(icount)=series(iseries)%days(j)
         series(i)%secs(icount)=series(iseries)%secs(j)
950      continue
       end do

       return

9000   call num2char(iline,aline)
       call addquote(infile,astring)
       write(amessage,9010) trim(aline), trim(astring)
9010   format('cannot read line ',a,' of TSPROC input file ',a)
       go to 9800
9100   continue
       call addquote(infile,astring)
       write(amessage,9110) trim(astring), trim(currentblock)
9110   format('unexpected end encountered to TSPROC input file ',a,' while ', &
       ' reading ',a,' block.')
       go to 9800

9800   call write_message(leadspace='yes',error='yes')
       call write_message(iunit=recunit,leadspace='yes')
       ifail=1

       return

end subroutine moving_window



subroutine get_ufore_series(ifail)

! -- Subroutine get_ufore_series reads a time series from a UFORE-HYDRO file.

       use tspvar
       use defn
       use inter
       implicit none

       integer, intent(out)   :: ifail

       integer dd1,mm1,yy1,hh1,nn1,ss1,dd2,mm2,yy2,hh2,nn2,ss2,ierr,k,ixcon, &
       icontext,i,iunit,begdays,begsecs,enddays,endsecs,iterm,jline,j, &
       dds,mms,yys,hhs,nns,sss,deltat,refdays,refsecs,nterm,tt1secs,tt2secs,  &
       totsecs,secs,days,jj
       real rtemp
       character*10 aname
       character*15 aline
       character*20 atemp
       character*25 aoption
       character*120 afile,bstring
       character*25 acontext(MAXCONTEXT)

       ifail=0
       currentblock='GET_SERIES_UFORE_HYDRO'

       write(*,10) trim(currentblock)
       write(recunit,10) trim(currentblock)
10     format(/,' Processing ',a,' block....')

       afile=' '
       acontext(1)=' '
       aname=' '
       icontext=0
       yy1=-9999
       hh1=-9999
       yy2=-9999
       hh2=-9999
       yys=-9999
       hhs=-9999
       deltat=-9999
       ixcon=0
       iunit=0

! -- The GET_SERIES_UFORE_HYDRO block is first parsed.

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
         else if(aoption.eq.'DATE_2')then
           call read_date(ierr,dd2,mm2,yy2,'DATE_2')
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'TIME_1')then
           call read_time(ierr,hh1,nn1,ss1,'TIME_1')
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'TIME_2')then
           call read_time(ierr,hh2,nn2,ss2,'TIME_2')
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'NEW_SERIES_NAME')then
           call read_new_series_name(ierr,aname)
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'MODEL_REFERENCE_DATE')then
           call read_date(ierr,dds,mms,yys,'MODEL_REFERENCE_DATE')
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'MODEL_REFERENCE_TIME')then
           call read_time(ierr,hhs,nns,sss,'MODEL_REFERENCE_TIME')
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'TIME_INCREMENT')then
           call get_keyword_value(ierr,1,deltat,rtemp,'TIME_INCREMENT')
           if(ierr.ne.0) go to 9800
           if(deltat.le.0)then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,30) trim(aline),trim(astring)
30           format('time increment must be positive at line ',a,' of file ',a)
             go to 9800
           end if
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

! -- If there are any absences in the GETSERIES block, this is now reported.

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
       if(aname.eq.' ')then
         call addquote(infile,astring)
         write(amessage,125) trim(currentblock),trim(astring)
125      format('no NEW_SERIES_NAME keyword provided in ',a,' block in file ',a)
         go to 9800
       end if
       if(yys.eq.-9999)then
         call addquote(infile,astring)
         write(amessage,126) trim(currentblock),trim(astring)
126      format('no MODEL_REFERENCE_DATE keyword provided in ',a,' block in file ',a)
         go to 9800
       end if
       if(hhs.eq.-9999)then
         call addquote(infile,astring)
         write(amessage,127) trim(currentblock),trim(astring)
127      format('no MODEL_REFERENCE_TIME keyword provided in ',a,' block in file ',a)
         go to 9800
       end if
       if(deltat.eq.-9999)then
         call addquote(infile,astring)
         write(amessage,128) trim(currentblock),trim(astring)
128      format('no TIME_INCREMENT keyword provided in ',a,' block in file ',a)
         go to 9800
       end if
       call date_check(ierr,yy1,mm1,dd1,hh1,nn1,ss1,yy2,mm2,dd2,hh2,nn2,ss2,  &
       begdays,begsecs,enddays,endsecs)
       if(ierr.ne.0) go to 9800
       refdays=numdays(1,1,1970,dds,mms,yys)
       refsecs=numsecs(0,0,0,hhs,nns,sss)
       if(refsecs.ge.86400)then
         refsecs=refsecs-86400
         refdays=refdays+1
       end if
       if(yy1.ne.-9999)then
         if(((begdays.eq.refdays).and.(begsecs.lt.refsecs)).or.    &
            (begdays.lt.refdays))then
            write(amessage,130) trim(currentblock),trim(astring)
130         format('DATE_1 and TIME_1 keywords provide a date and time that ', &
            'precedes the model reference date and time in ',a,' block of ',   &
            'file ',a)
            go to 9800
         end if
       end if

! -- There appear to be no errors in the block, so now it is processed.

       call addquote(afile,astring)
       write(*,179) trim(astring)
       write(recunit,179) trim(astring)
179    format(t5,'Reading UFORE-HYDRO file ',a,'....')
       iunit=nextunit()
       open(unit=iunit,file=afile,status='old',iostat=ierr)
       if(ierr.ne.0)then
         write(amessage,180) trim(astring),trim(currentblock)
180      format('cannot open UFORE-HYDRO file ',a,' cited in ',a,' block.')
         go to 9800
       end if

! -- The first line on the file is read.

       jline=1
       read(iunit,*,err=9200,end=9300) nterm
       if(nterm.le.0)then
         call addquote(afile,astring)
         write(amessage,190) trim(astring)
190      format('number-of-entries header cannot be zero or negative at ',  &
         'first line of UFORE-HYDRO file ',a)
         go to 9800
       end if

! -- If the date and time corresponding to DATE_2 and TIME_2 postdates
!    the end of the series, this is now evaluated.

       if(yy2.ne.-9999)then
         totsecs=nterm*deltat+refdays*86400+refsecs
         tt2secs=enddays*86400+endsecs
         if(tt2secs.gt.totsecs)then
           call addquote(infile,astring)
           call addquote(afile,bstring)
           write(amessage,200) trim(currentblock),trim(astring),trim(bstring)
200        format('date and time corresponding to DATE_2 and TIME_2 in ',   &
           a,' block of file ',a,' postdates end of time series contained ',  &
           'in UFORE-HYDRO file ',a)
           go to 9800
         end if
       else
         tt2secs=huge(i)
       end if

! -- The total number of terms in the new series is evaluated given the
!    entries in the DATE_1, TIME_1, DATE_2 and TIME_2 strings.

        if((yy1.eq.-9999).and.(yy2.eq.-9999))then
          iterm=nterm
        else
          secs=refdays*86400+refsecs
          if(yy1.eq.-9999)then
            tt1secs=-9999
          else
            tt1secs=begdays*86400+begsecs
          end if
          iterm=0
          do i=1,nterm
            secs=secs+deltat
            if(secs.ge.tt1secs)then
              if(secs.le.tt2secs)then
                iterm=iterm+1
              else
                go to 220
              end if
            end if
          end do
220       continue
        end if
        if(iterm.eq.0)then
          call addquote(afile,astring)
          write(amessage,222) trim(astring)
222       format('time series of zero length is requested from UFORE-HYDRO ',  &
          'file ',a,'. Alter DATE_1, TIME_1, DATE_2, TIME_2 settings.')
          go to 9800
        end if

! -- Storage for the new series is now allocated.

       do i=1,MAXSERIES
         if(.not.series(i)%active) go to 515
       end do
       write(amessage,510)
510    format('no more time series available for data storage - increase MAXSERIES and ', &
       'recompile program.')
       go to 9800

515    allocate(series(i)%days(iterm),series(i)%secs(iterm),  &
       series(i)%val(iterm),stat=ierr)
       if(ierr.ne.0)then
         write(amessage,550)
550      format('cannot allocate memory for another time series.')
         go to 9800
       end if
       series(i)%active=.true.
       series(i)%name=aname
       series(i)%nterm=iterm
       series(i)%type='ts'

! -- The series is now read in.

       days=refdays
       secs=refsecs
       if((yy1.eq.-9999).and.(yy2.eq.-9999))then
         do j=1,nterm
           jline=jline+1
           read(iunit,*,err=9200,end=9300) series(i)%val(j)
           secs=secs+deltat
551        continue
           if(secs.ge.86400)then
             secs=secs-86400
             days=days+1
             go to 551
           end if
           series(i)%days(j)=days
           series(i)%secs(j)=secs
         end do
       else
         if(yy1.eq.-9999)begdays=-9999
         if(yy2.eq.-9999)enddays=huge(i)
         jj=0
         do j=1,nterm
           jline=jline+1
           read(iunit,*,err=9200,end=9300) rtemp
           secs=secs+deltat
           if(secs.ge.86400)then
             secs=secs-86400
             days=days+1
           end if
           if((days.gt.begdays).or.                          &
              ((days.eq.begdays).and.(secs.ge.begsecs)))then
              if((days.lt.enddays).or.                        &
                 ((days.eq.enddays).and.(secs.le.endsecs)))then
                 jj=jj+1
                 series(i)%val(jj)=rtemp
                 series(i)%days(jj)=days
                 series(i)%secs(jj)=secs
              else
                go to 300
              end if
           end if
         end do
300      continue
       end if

       call addquote(afile,astring)
       write(*,580) trim(aname),trim(astring)
       write(recunit,580) trim(aname),trim(astring)
580    format(t5,'Series "',a,'" successfully imported from file ',a)
       go to 9900

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
9210   format('unable to read line ',a,' of UFORE-HYDRO file ',a)
       go to 9800
9300   call addquote(afile,astring)
       write(amessage,9310) trim(astring)
9310   format('unexpected end encountered to UFORE-HYDRO file ',a)
       go to 9800

9800   call write_message(leadspace='yes',error='yes')
       call write_message(iunit=recunit,leadspace='yes')
       ifail=1

9900   if(iunit.ne.0)close(unit=iunit,iostat=ierr)
       return

end subroutine get_ufore_series

!     Last change:  JD    1 Apr 2009    2:24 am
subroutine get_mul_series_gsflow_gage(ifail)

! -- Subroutine GET_MUL_SERIES_GSFLOW_GAGE reads multiple series fron a GSFLOW gage file.

       use tspvar
       use defn
       use inter
       implicit none

       integer, intent(out)   :: ifail

       integer dd1,mm1,yy1,hh1,nn1,ss1,dd2,mm2,yy2,hh2,nn2,ss2,ierr, &
       icontext,i,iunit,begdays,begsecs,enddays,endsecs,jline,j, &
       jseries,kseries,ixcon,k,isite,iseriesname,iterm
       integer ddr,mmr,yyr,hhr,nnr,ssr,refdays,refsecs,itemp,jfail, &
       ncol,icount,jcount,timecol,maxcol,ddays,dsecs
       integer jjseries(MAXSERIESREAD)
       integer datcol(MAXSERIESREAD)
       double precision dtime, time_per_day
       character*15 aline
       character*25 aoption
       character*200 afile
       character*30 atemp
       character*30 site(MAXSERIESREAD)
       character*25 acontext(MAXCONTEXT)
       character*10 aname(MAXSERIESREAD)

!       make sure that i have done the right thing changing MAXSERIES to MAXSERIESREAD
!       if so, do it in other subroutines as well that read multiple series.

       ifail=0
       currentblock='GET_MUL_SERIES_GSFLOW_GAGE'

       write(*,10) trim(currentblock)
       write(recunit,10) trim(currentblock)
10     format(/,' Processing ',a,' block....')

       afile=' '
       icontext=0
       ixcon=0
       yy1=-9999
       hh1=-9999
       yy2=-9999
       hh2=-9999
       yyr=-9999
       hhr=-9999
       isite=1
       iseriesname=0
       jseries=0
       kseries=0
       time_per_day=1.0d0

! -- The GET_MUL_SERIES_GSFLOW_GAGE block is first parsed.

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
         else if(aoption.eq.'DATE_2')then
           call read_date(ierr,dd2,mm2,yy2,'DATE_2')
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'TIME_1')then
           call read_time(ierr,hh1,nn1,ss1,'TIME_1')
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'TIME_2')then
           call read_time(ierr,hh2,nn2,ss2,'TIME_2')
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'MODEL_REFERENCE_DATE')then
           call read_date(ierr,ddr,mmr,yyr,'MODEL_REFERENCE_DATE')
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'MODEL_REFERENCE_TIME')then
           call read_time(ierr,hhr,nnr,ssr,'MODEL_REFERENCE_TIME')
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'TIME_UNITS_PER_DAY')then
           call get_keyword_value_double(ierr,2,itemp,time_per_day,'TIME_UNITS_PER_DAY')
           if(ierr.ne.0) go to 9800
           if(time_per_day.le.0.0d0)then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,65) trim(aline),trim(astring)
65           format('time units per day must be positive at line ',a,' of file ',a)
             go to 9800
           end if
         else if(aoption.eq.'DATA_TYPE')then
           if(isite.eq.0)then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,42) trim(currentblock),trim(aline),trim(astring)
42           format('DATA_TYPE keyword in wrong position in ',a,' block at line ',a, &
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
           call getfile(ierr,cline,site(jseries),left_word(2),right_word(2))
           if(ierr.ne.0)then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,57) trim(aline),trim(astring)
57           format('cannot read DATA_TYPE string from line ',a,' of file ',a)
             go to 9800
           end if
           call casetrans(site(jseries),'lo')
           call addquote(site(jseries),astring)
           write(*,46) trim(astring)
           write(recunit,46) trim(astring)
46         format(t5,'DATA_TYPE ',a)
           isite=0
           iseriesname=1
           aname(jseries)=' '
         else if(aoption.eq.'NEW_SERIES_NAME')then
           if(iseriesname.eq.0)then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,43) trim(currentblock),trim(aline),trim(astring)
43           format('NEW_SERIES_NAME keyword can only follow a DATA_TYPE ',  &
             'keyword in ',a,' block at line ',a,' of file ',a)
             go to 9800
           end if
           call read_new_series_name(ierr,aname(jseries))
           if(ierr.ne.0) go to 9800
           if(jseries.gt.1)then
             do j=1,jseries-1
               if(aname(jseries).eq.aname(j))then
                 write(amessage,146) trim(aname(jseries)),trim(currentblock)
146              format('SERIES_NAME "',a,'" used more than once in ',a,' block.')
                 go to 9800
               end if
             end do
           end if
           iseriesname=0
           isite=1
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
           if(iseriesname.eq.1)then
             write(amessage,48) trim(currentblock)
48           format(a,' block END encountered before finding ', &
             'expected NEW_SERIES_NAME keyword.')
             go to 9800
           end if
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

! -- If there are any absences in the GET_MUL_SERIES_SSF block, these are now reported.

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
       if(jseries.eq.0)then
         call addquote(infile,astring)
         write(amessage,125) trim(currentblock),trim(astring)
125      format('no DATA_TYPE keyword provided in ',a,' block in file ',a)
         go to 9800
       end if
       call date_check(ierr,yy1,mm1,dd1,hh1,nn1,ss1,yy2,mm2,dd2,hh2,nn2,ss2,  &
       begdays,begsecs,enddays,endsecs)
       if(ierr.ne.0) go to 9800
       if(begsecs.ge.86400)then
         begsecs=begsecs-86400
         begdays=begdays+1
       end if
       if(endsecs.ge.86400)then
         endsecs=endsecs-86400
         enddays=enddays+1
       end if
       if(jseries.gt.1)then
         do j=2,jseries
           do i=1,j-1
             if(site(j).eq.site(i))then
               call addquote(infile,astring)
               write(amessage,401) trim(currentblock),trim(astring)
401            format('two series possess the same DATA_TYPE name ',  &
               'in ',a,' block of file ',a)
               go to 9800
             end if
           end do
         end do
       end if
       if(yyr.eq.-9999)then
         call addquote(infile,astring)
         write(amessage,402) trim(currentblock),trim(astring)
402      format('no MODEL_REFERENCE_DATE keyword provided in ',a,' block in file ',a)
         go to 9800
       end if
       if(hhr.eq.-9999)then
         call addquote(infile,astring)
         write(amessage,403) trim(currentblock),trim(astring)
403      format('no MODEL_REFERENCE_TIME keyword provided in ',a,' block in file ',a)
         go to 9800
       end if
       refdays=numdays(1,1,1970,ddr,mmr,yyr)
       refsecs=numsecs(0,0,0,hhr,nnr,ssr)
404    continue
       if(refsecs.ge.86400)then
         refsecs=refsecs-86400
         refdays=refdays+1
         go to 404
       end if

! -- There appear to be no errors in the block, so now it is processed.

       call addquote(afile,astring)
       write(*,179) trim(astring)
       write(recunit,179) trim(astring)
179    format(t5,'Reading GSFLOW gage file ',a,'....')
       iunit=nextunit()
       open(unit=iunit,file=afile,status='old',iostat=ierr)
       if(ierr.ne.0)then
         write(amessage,180) trim(astring),trim(currentblock)
180      format('cannot open file ',a,' cited in ',a,' block.')
         go to 9800
       end if

! -- The file is perused a first time to find out the storage requirements of the
!    time series.

       jline=1
       read(iunit,'(a)',err=9200,end=9200) cline
       jline=jline+1
       read(iunit,'(a)',err=9200,end=9200) cline
       call remchar(cline,'"')
       call casetrans(cline,'lo')
       cline=adjustl(cline)
       if(cline(1:5).ne.'data:') go to 9300
       cline=cline(6:)
! -- Establish the exact number of columns.
       do i=1,NUM_WORD_DIM
         call linesplit(jfail,i)
         if(jfail.ne.0) go to 380
       end do
       write(amessage,371) trim(astring)
371    format('too many data columns in file ',a,'. Increase NUM_WORD_DIM and ',  &
       're-compile program.')
       go to 9800
380    ncol=i-1
! -- Read the column headers and identify which columns we need to read.
       datcol=0               ! an array
       icount=0
       do i=1,ncol
         atemp=cline(left_word(i):right_word(i))
         do j=1,jseries
           if(site(j).eq.atemp)then
             datcol(j)=i
             icount=icount+1
             if(icount.lt.jseries)then
               go to 390
             else
               go to 400
             end if
           end if
         end do
390      continue
       end do
400    continue
       if(icount.lt.jseries)then
         do i=1,jseries
           if(datcol(i).eq.0)then
             write(amessage,410) trim(site(i)),trim(astring)
410          format('data type column header "',a,'" not found in file ',a,'.')
             go to 9800
           end if
         end do
       end if
       do i=1,ncol
         atemp=cline(left_word(i):right_word(i))
         if(atemp.eq.'time')then
           timecol=i
           go to 421
         end if
       end do
       write(amessage,420) trim(astring)
420    format('no "time" data header found in file ',a,'.')
       go to 9800
421    continue

! -- The file is now read a first time in order to establish memory requirements.

       icount=0
       jcount=0
       maxcol=0
       do i=1,jseries
         if(datcol(i).gt.maxcol)maxcol=datcol(i)
       end do
       do
         jline=jline+1
         read(iunit,'(a)',err=9200,end=450) cline
         if(cline.eq.' ') cycle
         call linesplit(jfail,timecol)
         if(jfail.ne.0)then
           call num2char(jline,aline)
           write(amessage,422) trim(aline),trim(astring)
422        format('insufficient entries on line ',a,' of file ',a)
           go to 9800
         end if
         dtime=char2double(jfail,timecol)
         if(jfail.ne.0)then
           call num2char(jline,aline)
           write(amessage,430) trim(aline),trim(astring)
430        format('cannot read time from line ',a,' of file ',a)
           go to 9800
         end if
         jcount=jcount+1
         dtime=dtime/time_per_day
         ddays=floor(dtime)
         dsecs=nint((dtime-dble(ddays))*86400.0d0)
         ddays=ddays+refdays
         dsecs=dsecs+refsecs
440      continue
         if(dsecs.ge.86400)then
           ddays=ddays+1
           dsecs=dsecs-86400
           go to 440
         end if
         if((ddays.lt.begdays).or.((ddays.eq.begdays).and.(dsecs.lt.begsecs))) cycle
         if((ddays.gt.enddays).or.((ddays.eq.enddays).and.(dsecs.gt.endsecs))) cycle
         icount=icount+1
       end do
450    continue
       if(jcount.eq.0)then
         write(amessage,460) trim(astring)
460      format('no data is present within file ',a)
         go to 9800
       end if
       if(icount.eq.0)then
         write(amessage,470) trim(astring)
470      format('no data is present within file ',a,' within requested date/time limits.')
         go to 9800
       end if
       iterm=icount

! -- Space is now allocated for the new series.

       do j=1,jseries
         k=jjseries(j)
         allocate(series(k)%days(iterm),series(k)%secs(iterm),  &
         series(k)%val(iterm),stat=ierr)
         if(ierr.ne.0)then
           write(amessage,550)
550        format('cannot allocate memory for another time series.')
           go to 9800
         end if
         series(k)%active=.true.
         series(k)%name=aname(j)
         series(k)%type='ts'
         series(k)%nterm=iterm
       end do

! -- The file is now read a second time and the data is imported.

       rewind(unit=iunit,iostat=ierr)
       if(ierr.ne.0)then
         write(amessage,370) trim(astring)
370      format('cannot re-wind GSFLOW output file ',a)
         go to 9800
       end if
       jline=1
       read(iunit,'(a)',err=9200,end=9200) cline
       jline=jline+1
       read(iunit,'(a)',err=9200,end=9200) cline

       icount=0
       do
         jline=jline+1
         read(iunit,'(a)',err=9200,end=700) cline
         if(cline.eq.' ') cycle
         call linesplit(ifail,maxcol)
         if(ifail.ne.0)then
           call num2char(jline,aline)
           write(amessage,372) trim(aline),trim(astring)
372        format('insufficient entries on line ',a,' of file ',a)
           go to 9800
         end if
         dtime=char2double(ifail,timecol)
         dtime=dtime/time_per_day
         ddays=floor(dtime)
         dsecs=nint((dtime-dble(ddays))*86400.0d0)
         ddays=ddays+refdays
         dsecs=dsecs+refsecs
640      continue
         if(dsecs.ge.86400)then
           ddays=ddays+1
           dsecs=dsecs-86400
           go to 640
         end if
         if((ddays.lt.begdays).or.((ddays.eq.begdays).and.(dsecs.lt.begsecs))) cycle
         if((ddays.gt.enddays).or.((ddays.eq.enddays).and.(dsecs.gt.endsecs))) go to 700
         icount=icount+1
         do i=1,jseries
           k=jjseries(i)
           series(k)%days(icount)=ddays
           series(k)%secs(icount)=dsecs
           j=datcol(i)
           series(k)%val(icount)=char2real(jfail,j)
           if(jfail.ne.0)then
             call num2char(jline,aline)
             write(amessage,650) trim(site(i)),trim(aline),trim(astring)
650          format('cannot read data value for data type "',a,'" from line ',a,  &
             ' of file ',a)
             go to 9800
           end if
         end do
       end do
700    continue

       do j=1,jseries
         write(*,860) trim(aname(j)),trim(astring)
         write(recunit,860) trim(aname(j)),trim(astring)
860      format(t5,'Series "',a,'" successfully imported from file ',a)
       end do

       go to 9900

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
9300   call addquote(afile,astring)
       write(amessage,9310) trim(astring)
9310   format('unexpected components in header lines to GSFLOW gage file ',a,'.')
       go to 9800

9800   call write_message(leadspace='yes',error='yes')
       call write_message(iunit=recunit,leadspace='yes')
       ifail=1

9900   close(unit=iunit,iostat=ierr)
       return


end subroutine get_mul_series_gsflow_gage



subroutine spacesub(astring)

      integer i,j,k,n
      character*1 bb
      character*(*) astring

      bb=char(211)
      n=len_trim(astring)
      k=1
10    continue
      if(k.gt.n) go to 100
      do i=k,n
        if((astring(i:i).eq.'''').or.(astring(i:i).eq.'"'))then
          astring(i:i)=' '
          do j=i+1,n
            if((astring(j:j).eq.'''').or.(astring(j:j).eq.'"'))then
              astring(j:j)=' '
              k=j+1
              go to 10
            end if
            if(astring(j:j).eq.' ')astring(j:j)=bb
          end do
          go to 100
        end if
      end do

100   continue
      return

end subroutine spacesub




subroutine get_mul_series_statvar(ifail)

! -- Subroutine GET_MUL_SERIES_STATVAR reads multiple series from an MMS/GSFLOW statvar file.

       use tspvar
       use defn
       use inter
       implicit none

       integer, intent(out)   :: ifail

       integer dd1,mm1,yy1,hh1,nn1,ss1,dd2,mm2,yy2,hh2,nn2,ss2,ierr, &
       icontext,i,iunit,begdays,begsecs,enddays,endsecs,jline,j, &
       jseries,kseries,ixcon,k,isite,iseriesname,iterm
       integer itemp,jfail,icount,jcount,ddays,dsecs,ilocid,nstatseries,   &
       ibeg,iend
       integer modday,yys,mms,dds,hhs,nns,sss
       integer jjseries(MAXSERIESREAD)
       integer datcol(MAXSERIESREAD),locid(MAXSERIESREAD)
       real, allocatable :: rval(:)
       real rtemp
       character*15 aline,aadate,aatime
       character*25 aoption
       character*100 varname
       character*200 afile
       character*30 atemp
       character*50 site(MAXSERIESREAD)
       character*25 acontext(MAXCONTEXT)
       character*10 aname(MAXSERIESREAD)

!       make sure that i have done the right thing changing MAXSERIES to MAXSERIESREAD
!       if so, do it in other subroutines as well that read multiple series.

       ifail=0
       currentblock='GET_MUL_SERIES_STATVAR'

       write(*,10) trim(currentblock)
       write(recunit,10) trim(currentblock)
10     format(/,' Processing ',a,' block....')

       afile=' '
       icontext=0
       ixcon=0
       yy1=-9999
       hh1=-9999
       yy2=-9999
       hh2=-9999
       ilocid=0
       isite=1
       iseriesname=0
       jseries=0
       kseries=0

! -- The GET_MUL_SERIES_STATVAR block is first parsed.

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
         else if(aoption.eq.'DATE_2')then
           call read_date(ierr,dd2,mm2,yy2,'DATE_2')
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'TIME_1')then
           call read_time(ierr,hh1,nn1,ss1,'TIME_1')
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'TIME_2')then
           call read_time(ierr,hh2,nn2,ss2,'TIME_2')
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'VARIABLE_NAME')then
           if(isite.eq.0)then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,42) trim(currentblock),trim(aline),trim(astring)
42           format('VARIABLE_NAME keyword in wrong position in ',a,' block at line ',a, &
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
           if(jseries.gt.MAXSERIESREAD)then
             write(amessage,461) trim(currentblock)
461          format('too many new series cited in ',a,' block. Increase MAXSERIESREAD ', &
             'and re-compile program.')
             go to 9800
           end if

           if(series(kseries)%active) go to 45
           jjseries(jseries)=kseries
           call getfile(ierr,cline,site(jseries),left_word(2),right_word(2))
           if(ierr.ne.0)then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,57) trim(aline),trim(astring)
57           format('cannot read VARIABLE_NAME string from line ',a,' of file ',a)
             go to 9800
           end if
           call casetrans(site(jseries),'lo')
           call addquote(site(jseries),astring)
           write(*,46) trim(astring)
           write(recunit,46) trim(astring)
46         format(t5,'VARIABLE_NAME ',a)
           isite=0
           ilocid=1
         else if(aoption.eq.'LOCATION_ID')then
           if(ilocid.eq.0)then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,441) trim(currentblock),trim(aline),trim(astring)
441          format('LOCATION_ID keyword in wrong position in ',a,' block at line ',a, &
             ' of file ',a)
             go to 9800
           end if
           call get_keyword_value(ierr,1,locid(jseries),rtemp,'LOCATION_ID')
           if(ierr.ne.0) go to 9800
           iseriesname=1
           aname(jseries)=' '
           ilocid=0
         else if(aoption.eq.'NEW_SERIES_NAME')then
           if(iseriesname.eq.0)then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,43) trim(currentblock),trim(aline),trim(astring)
43           format('NEW_SERIES_NAME keyword can only follow a LOCATION_ID ',  &
             'keyword in ',a,' block at line ',a,' of file ',a)
             go to 9800
           end if
           call read_new_series_name(ierr,aname(jseries))
           if(ierr.ne.0) go to 9800
           if(jseries.gt.1)then
             do j=1,jseries-1
               if(aname(jseries).eq.aname(j))then
                 write(amessage,146) trim(aname(jseries)),trim(currentblock)
146              format('SERIES_NAME "',a,'" used more than once in ',a,' block.')
                 go to 9800
               end if
             end do
           end if
           iseriesname=0
           isite=1
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
           if(iseriesname.eq.1)then
             write(amessage,48) trim(currentblock)
48           format(a,' block END encountered before finding ', &
             'expected NEW_SERIES_NAME keyword.')
             go to 9800
           end if
           if(ilocid.eq.1)then
             write(amessage,49) trim(currentblock)
49           format(a,' block END encountered before finding ', &
             'expected LOCATION_ID keyword.')
             go to 9800
           end if
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

! -- If there are any absences in the GET_MUL_SERIES_STATVAR block, these are now reported.

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
       if(jseries.eq.0)then
         call addquote(infile,astring)
         write(amessage,125) trim(currentblock),trim(astring)
125      format('no VARIABLE_NAME keyword provided in ',a,' block in file ',a)
         go to 9800
       end if
       call date_check(ierr,yy1,mm1,dd1,hh1,nn1,ss1,yy2,mm2,dd2,hh2,nn2,ss2,  &
       begdays,begsecs,enddays,endsecs)
       if(ierr.ne.0) go to 9800
       if(begsecs.ge.86400)then
         begsecs=begsecs-86400
         begdays=begdays+1
       end if
       if(endsecs.ge.86400)then
         endsecs=endsecs-86400
         enddays=enddays+1
       end if
       if(jseries.gt.1)then
         do j=2,jseries
           do i=1,j-1
             if((site(j).eq.site(i)).and.(locid(j).eq.locid(i)))then
               call addquote(infile,astring)
               write(amessage,401) trim(currentblock),trim(astring)
401            format('two series possess the same VARIABLE_NAME ',  &
               'and LOCATION_ID in ',a,' block of file ',a)
               go to 9800
             end if
           end do
         end do
       end if

! -- There appear to be no errors in the block, so now it is processed.

       call addquote(afile,astring)
       write(*,179) trim(astring)
       write(recunit,179) trim(astring)
179    format(t5,'Reading STATVAR file ',a,'....')
       iunit=nextunit()
       open(unit=iunit,file=afile,status='old',iostat=ierr)
       if(ierr.ne.0)then
         write(amessage,180) trim(astring),trim(currentblock)
180      format('cannot open file ',a,' cited in ',a,' block.')
         go to 9800
       end if

! -- The header to the file is perused in its entirety.

       jline=1
       read(iunit,'(a)',err=9200,end=9200) cline
       if(cline.eq.' ') go to 9350
       call linesplit(ifail,1)
       nstatseries=char2int(jfail,1)
       if(jfail.ne.0) go to 9350
       if(nstatseries.le.0) go to 9350
       datcol=0               ! an array
       icount=0
       do i=1,nstatseries
         jline=jline+1
         read(iunit,'(a)',err=9200,end=9200) cline
         ibeg=1
         iend=len_trim(cline)
         call getfile(jfail,cline,varname,ibeg,iend)
         if(jfail.ne.0)then
           call num2char(jline,aline)
           write(amessage,370) trim(aline),trim(astring)
370        format('cannot read varable name from line ',a,' of file ',a)
           go to 9800
         end if
         call casetrans(varname,'lo')
         ibeg=iend+1
         cline=cline(ibeg:)
         call linesplit(jfail,1)
         if(jfail.ne.0) then
           call num2char(jline,aline)
           write(amessage,380) trim(aline),trim(astring)
380        format('cannot read location id from line ',a,' of file ',a,'.')
           go to 9800
         end if
         itemp=char2int(jfail,1)
         if(jfail.ne.0)then
           call num2char(jline,aline)
           write(amessage,380) trim(aline),trim(astring)
           go to 9800
         end if
         if(icount.lt.jseries)then
           do j=1,jseries
             if((site(j).eq.varname).and.(itemp.eq.locid(j))) then
               datcol(j)=i
               icount=icount+1
               go to 390
             end if
           end do
390        continue
         end if
       end do
       if(icount.lt.jseries)then
         do i=1,jseries
           if(datcol(i).eq.0)then
             call num2char(locid(i),atemp)
             write(amessage,410) trim(site(i)),trim(atemp),trim(astring)
410          format('VARIABLE_NAME "',a,'", LOCATION_ID ',a,' not found in file ',a,'.')
             go to 9800
           end if
         end do
       end if

! -- The file is now read a first time in order to establish memory requirements.
       allocate(rval(nstatseries),stat=ierr)
       if(ierr.ne.0)then
         write(amessage,420)
420      format('cannot allocate memory for temporary array storage.')
         go to 9800
       end if
       icount=0
       jcount=0
       do
         read(iunit,*,err=9270,end=450) modday,yys,mms,dds,hhs,nns,sss,(rval(i),i=1,nstatseries)
         jcount=jcount+1
         ddays=numdays(1,1,1970,dds,mms,yys)
         dsecs=numsecs(0,0,0,hhs,nns,sss)
440      continue
         if(dsecs.ge.86400)then
           ddays=ddays+1
           dsecs=dsecs-86400
           go to 440
         end if
         if((ddays.lt.begdays).or.((ddays.eq.begdays).and.(dsecs.lt.begsecs))) cycle
         if((ddays.gt.enddays).or.((ddays.eq.enddays).and.(dsecs.gt.endsecs))) cycle
         icount=icount+1
       end do
450    continue
       if(jcount.eq.0)then
         write(amessage,460) trim(astring)
460      format('no data is present within file ',a)
         go to 9800
       end if
       if(icount.eq.0)then
         write(amessage,470) trim(astring)
470      format('no data is present within file ',a,' within requested date/time limits.')
         go to 9800
       end if
       iterm=icount

! -- Space is now allocated for the new series.

       do j=1,jseries
         k=jjseries(j)
         allocate(series(k)%days(iterm),series(k)%secs(iterm),  &
         series(k)%val(iterm),stat=ierr)
         if(ierr.ne.0)then
           write(amessage,550)
550        format('cannot allocate memory for another time series.')
           go to 9800
         end if
         series(k)%active=.true.
         series(k)%name=aname(j)
         series(k)%type='ts'
         series(k)%nterm=iterm
       end do

! -- The file is now read a second time and the data is imported.

       rewind(unit=iunit,iostat=ierr)
       if(ierr.ne.0)then
         write(amessage,371) trim(astring)
371      format('cannot re-wind STATVAR file ',a)
         go to 9800
       end if
       do i=1,nstatseries+1
         read(iunit,'(a)') cline
       end do
       icount=0
       jcount=0
       do
         read(iunit,*,err=9270,end=700) modday,yys,mms,dds,hhs,nns,sss,(rval(i),i=1,nstatseries)
         jcount=jcount+1
         ddays=numdays(1,1,1970,dds,mms,yys)
         dsecs=numsecs(0,0,0,hhs,nns,sss)
442      continue
         if(dsecs.ge.86400)then
           ddays=ddays+1
           dsecs=dsecs-86400
           go to 442
         end if
         if((ddays.lt.begdays).or.((ddays.eq.begdays).and.(dsecs.lt.begsecs))) cycle
         if((ddays.gt.enddays).or.((ddays.eq.enddays).and.(dsecs.gt.endsecs))) go to 700
         icount=icount+1
         do i=1,jseries
           k=jjseries(i)
           series(k)%days(icount)=ddays
           series(k)%secs(icount)=dsecs
           j=datcol(i)
           series(k)%val(icount)=rval(j)
         end do
       end do
700    continue

       do j=1,jseries
         write(*,860) trim(aname(j)),trim(astring)
         write(recunit,860) trim(aname(j)),trim(astring)
860      format(t5,'Series "',a,'" successfully imported from file ',a)
       end do

       go to 9900

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
9210   format('unable to read line ',a,' of STATVAR file ',a)
       go to 9800
9270   if(jcount.eq.0)then
         call addquote(afile,astring)
         write(amessage,9280) trim(astring)
9280     format('cannot read first data line from STATVAR file ',a,'.')
         go to 9800
       else
         if(datespec.eq.1)then
           write(aadate,9281) dds,mms,yys
9281       format(i2.2,'/',i2.2,'/',i4)
         else
           write(aadate,9281) mms,dds,yys
         end if
         write(aatime,9282) hhs,nns,sss
9282     format(i2.2,':',i2.2,':',i2.2)
         call addquote(afile,astring)
         write(amessage,9283) trim(astring),trim(aadate),trim(aatime)
9283     format('error reading STATVAR file ',a,'. Error occured for date=',a,', ', &
         'time=',a,' or for the entry after that.')
         go to 9800
       end if
9300   call addquote(afile,astring)
       write(amessage,9310) trim(astring)
9310   format('unexpected components in header lines to GSFLOW gage file ',a,'.')
       go to 9800
9350   call addquote(afile,astring)
       write(amessage,9360) trim(astring)
9360   format('positive integer expected on first line of STATVAR file ',a)
       go to 9800

9800   call write_message(leadspace='yes',error='yes')
       call write_message(iunit=recunit,leadspace='yes')
       ifail=1

9900   close(unit=iunit,iostat=ierr)
       if(allocated(rval)) deallocate(rval,stat=ierr)
       return


end subroutine get_mul_series_statvar




subroutine new_series_uniform(ifail)

! -- Subroutine NEW_SERIES_UNIFORM generates a uniform, equispaced, time series.

       use tspvar
       use defn
       use inter
       implicit none

       integer, intent(out)   :: ifail

       integer dd1,mm1,yy1,hh1,nn1,ss1,dd2,mm2,yy2,hh2,nn2,ss2,ierr, &
       icontext,i,begdays,begsecs,enddays,endsecs,ixcon,iterm,ifac
       integer time_interval,time_unit,ival,tterm,iseries,dd,mm,yy,itemp
       integer ilike
       real rtemp,rval
       double precision timediff,timeinc
       character*10 aname,alikename
       character*15 aline
       character*25 aoption,aconstname
       character*30 atemp
       character*25 acontext(MAXCONTEXT)

       ifail=0
       currentblock='NEW_SERIES_UNIFORM'

       write(*,10) trim(currentblock)
       write(recunit,10) trim(currentblock)
10     format(/,' Processing ',a,' block....')

       icontext=0
       ixcon=0
       yy1=-9999
       hh1=-9999
       yy2=-9999
       hh2=-9999
       time_unit=-9999
       time_interval=-9999
       ival=-9999
       aname=' '
       alikename=''
       ilike = 0

! -- The NEW_SERIES_UNIFORM block is first parsed.

       do
11       continue
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
         if(aoption.eq.'DATE_1')then
           call read_date(ierr,dd1,mm1,yy1,'DATE_1')
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'DATE_2')then
           call read_date(ierr,dd2,mm2,yy2,'DATE_2')
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'TIME_1')then
           call read_time(ierr,hh1,nn1,ss1,'TIME_1')
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'TIME_2')then
           call read_time(ierr,hh2,nn2,ss2,'TIME_2')
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'TIME_INTERVAL')then
           call get_keyword_value(ierr,1,time_interval,rtemp,'TIME_INTERVAL')
           if(ierr.ne.0) go to 9800
           if(time_interval.le.0)then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,65) trim(aline),trim(astring)
65           format('time interval must be positive at line ',a,' of file ',a)
             go to 9800
           end if
         else if(aoption.eq.'TIME_UNIT')then
           call getfile(ierr,cline,atemp,left_word(2),right_word(2))
           if(ierr.ne.0)then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,50) trim(aline),trim(astring)
50           format('cannot read time unit from line ',a,' of file ',a)
             go to 9800
           end if
           call casetrans(atemp,'lo')
           if(atemp(1:3).eq.'sec') then
             time_unit=1
             atemp='seconds'
           else if(atemp(1:3).eq.'min')then
             time_unit=2
             atemp='minutes'
           else if(atemp(1:3).eq.'hou')then
             time_unit=3
             atemp='hours'
           else if(atemp(1:3).eq.'day')then
             time_unit=4
             atemp='days'
           else if(atemp(1:3).eq.'mon')then
             time_unit=5
             atemp='months'
           else if(atemp(1:3).eq.'yea')then
             time_unit=6
             atemp='years'
           else
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,51) trim(aline),trim(astring)
51           format('illegal time unit at line ',a,' of file ',a)
             go to 9800
           end if
           write(*,54) trim(atemp)
           write(recunit,54) trim(atemp)
54         format(t5,'TIME UNIT ',a)
         else if(aoption.eq.'NEW_SERIES_NAME')then
           call read_new_series_name(ierr,aname)
           if(ierr.ne.0) go to 9800
         else if (aoption.eq.'LIKE_SERIES')then
           ilike = 1
           call read_file_name(ierr,alikename)
           call casetrans(alikename,'lo')
           if(ierr.ne.0) go to 9800
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
         else if(aoption.eq.'NEW_SERIES_VALUE')then
           call get_keyword_value(ierr,2,itemp,rval,'NEW_SERIES_VALUE')
           if(ierr.ne.0) go to 9800
           ival=1
         else if(aoption.eq.'CONSTANT')then
            call read_file_name(ierr,aconstname)
            call casetrans(aconstname,'lo')
            if(ierr.ne.0) go to 9800
            do i=1,MAXCONST
                if(const(i)%name.eq.aconstname)then
                  rval = const(i)%value
                  ival=1
                  goto 11
                end if
            end do
            write(amessage,79) trim(aconstname)
79          format('no CONSTANT found with name"',a)
            goto 9800          
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

! -- If there are any absences in the GET_MUL_SERIES_SSF block, these are now reported.

100    continue
       if(icontext.eq.0)then
         call addquote(infile,astring)
         write(amessage,122) trim(currentblock),trim(astring)
122      format('no CONTEXT keyword provided in ',a,' block in file ',a)
         go to 9800
       end if
       if(ival.ne.1.and.ival.ne.2)then
         write(amessage,123) trim(currentblock),trim(astring)
123      format('no NEW_SERIES_VALUE or CONSTANT keyword provided in ',a,' block in file ',a)
         go to 9800
       end if
       if(time_unit.eq.-9999.and.ilike.eq.0)then
         write(amessage,124) trim(currentblock),trim(astring)
124      format('no TIME_UNIT keyword provided in ',a,' block in file ',a)
         go to 9800
       end if
       if(aname.eq.' ')then
         write(amessage,129) trim(currentblock),trim(astring)
129      format('no NEW_SERIES_NAME keyword provided in ',a,' block in file ',a)
         go to 9800
       end if
       if(time_interval.eq.-9999.and.ilike.eq.0)then
         write(amessage,125) trim(currentblock),trim(astring)
125      format('no TIME_INTERVAL keyword provided in ',a,' block in file ',a)
         go to 9800
       end if
       !--if LIKE_SERIES was not passed...
       if (ilike.eq.0) then
           if((yy1.eq.-9999).or.(hh1.eq.-9999).or.(yy2.eq.-9999).or.(hh2.eq.-9999))then
             write(amessage,126) trim(currentblock),trim(astring)
126         format('all of DATE_1, TIME_1, DATE_2, TIME_2 keywords must be provided in ',a,  &
             ' block in file ',a)
             go to 9800
           end if      
           call date_check(ierr,yy1,mm1,dd1,hh1,nn1,ss1,yy2,mm2,dd2,hh2,nn2,ss2,  &
           begdays,begsecs,enddays,endsecs)
           if(ierr.ne.0) go to 9800
           if(begsecs.ge.86400)then
             begsecs=begsecs-86400
             begdays=begdays+1
           end if
           if(endsecs.ge.86400)then
             endsecs=endsecs-86400
             enddays=enddays+1
           end if
      
! -- Some errors are checked for.

           if(time_unit.eq.5)then
             if(dd1.gt.28)then
               write(amessage,82)
    82         format('if TIME_UNIT is set to "month" then the day in DATE_1 must ',  &
               'not be greater than 28.')
               go to 9800
             end if
           end if
           if(time_unit.eq.6)then
             if((dd1.gt.28).and.(mm1.eq.2))then
               write(amessage,83)
    83         format('if TIME_UNIT is set to "year" then DATE_1 must not be ',   &
               '28th or 29th February.')
               go to 9800
             end if
           end if

    ! -- Roughly the number of terms in the series is now evaluated so that memory can
    !    be allocated for the temporary series.

           timediff=dble(enddays-begdays)*86400.0d0+dble(endsecs-begsecs)
           timeinc=dble(time_interval)
           if(time_unit.eq.1)then
             timeinc=timeinc*1.0d0
           else if(time_unit.eq.2)then
             timeinc=timeinc*60.0d0
           else if(time_unit.eq.3)then
             timeinc=timeinc*3600.0d0
           else if(time_unit.eq.4)then
             timeinc=timeinc*86400.0d0
           else if(time_unit.eq.5)then
             timeinc=timeinc*28.0d0*86400.0d0
           else if(time_unit.eq.6)then
             timeinc=timeinc*365.0d0*86400.0d0
           end if
           tterm=ceiling(timediff/timeinc)+20       

    ! -- The temporary series is allocated.

           call alloc_tempseries(ierr,tterm)
           if(ierr.ne.0) go to 9800

    ! -- Terms of the temporary series are now created.

           if(time_unit.le.3)then
             ifac=1
             if(time_unit.eq.2)then
               ifac=60
             else if(time_unit.eq.3)then
               ifac=3600
             end if
             tempseries%days(1)=begdays
             tempseries%secs(1)=begsecs
             i=1
             do
               i=i+1
               tempseries%days(i)=tempseries%days(i-1)
               tempseries%secs(i)=tempseries%secs(i-1)+time_interval*ifac
    120        continue
               if(tempseries%secs(i).ge.86400)then
                 tempseries%secs(i)=tempseries%secs(i)-86400
                 tempseries%days(i)=tempseries%days(i)+1
                 go to 120
               end if
               if((tempseries%days(i).gt.enddays).or.                     &
                 ((tempseries%days(i).eq.enddays).and.(tempseries%secs(i).gt.endsecs)))then
                   iterm=i-1
                   go to 500
               end if
             end do
           else if(time_unit.eq.4)then
             tempseries%days(1)=begdays
             tempseries%secs(1)=begsecs
             i=1
             do
               i=i+1
               tempseries%days(i)=tempseries%days(i-1)+time_interval
               tempseries%secs(i)=tempseries%secs(i-1)
               if((tempseries%days(i).gt.enddays).or.                     &
                 ((tempseries%days(i).eq.enddays).and.(tempseries%secs(i).gt.endsecs)))then
                 iterm=i-1
                 go to 500
               end if
             end do
           else if(time_unit.eq.5)then
             tempseries%days(1)=begdays
             tempseries%secs(1)=begsecs
             dd=dd1
             mm=mm1
             yy=yy1
             i=1
             do
               i=i+1
               mm=mm+time_interval
    180        continue
               if(mm.gt.12)then
                 mm=mm-12
                 yy=yy+1
                 go to 180
               end if
               tempseries%days(i)=numdays(1,1,1970,dd,mm,yy)
               tempseries%secs(i)=tempseries%secs(i-1)
               if((tempseries%days(i).gt.enddays).or.                     &
                 ((tempseries%days(i).eq.enddays).and.(tempseries%secs(i).gt.endsecs)))then
                   iterm=i-1
                   go to 500
               end if
             end do
           else if(time_unit.eq.6)then
             tempseries%days(1)=begdays
             tempseries%secs(1)=begsecs
             dd=dd1
             mm=mm1
             yy=yy1
             i=1
             do
               i=i+1
               yy=yy+time_interval
               tempseries%days(i)=numdays(1,1,1970,dd,mm,yy)
               tempseries%secs(i)=tempseries%secs(i-1)
               if((tempseries%days(i).gt.enddays).or.                     &
                 ((tempseries%days(i).eq.enddays).and.(tempseries%secs(i).gt.endsecs)))then
                   iterm=i-1
                   go to 500
               end if
             end do
           end if
       
       
       !--else find the like series name 
       else
        do iseries=1,MAXSERIES
          if (series(iseries)%name.eq.alikename)then
             iterm = series(iseries).nterm
             ilike = iseries
             goto 500
          end if
        end do
        write(amessage,499) alikename
499     format('cannot find active series to replicate:"',a)           
         go to 9800       
       endif 
! -- The series has been generated and is now copied from the temporary series.

500    continue

       do iseries=1,MAXSERIES
         if(series(iseries)%active) cycle
         go to 510
       end do
510    continue
       allocate(series(iseries)%days(iterm),series(iseries)%secs(iterm),  &
       series(iseries)%val(iterm),stat=ierr)
       if(ierr.ne.0)then
         write(amessage,550)
550      format('cannot allocate memory for another time series.')
         go to 9800
       end if
       series(iseries)%active=.true.
       series(iseries)%name=aname
       series(iseries)%type='ts'
       series(iseries)%nterm=iterm
       if(ilike.eq.0)then
           do i=1,iterm
             series(iseries)%days(i)=tempseries%days(i)
             series(iseries)%secs(i)=tempseries%secs(i)
             series(iseries)%val(i)=rval
           end do
       else
            do i=1,iterm
             series(iseries)%days(i)=series(ilike)%days(i)
             series(iseries)%secs(i)=series(ilike)%secs(i)
             series(iseries)%val(i)=rval
            end do
       end if

       write(*,580) trim(aname)
       write(recunit,580) trim(aname)
580    format(t5,'Series "',a,'" successfully created.')

       go to 9900

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

9800   call write_message(leadspace='yes',error='yes')
       call write_message(iunit=recunit,leadspace='yes')
       ifail=1

9900   continue
       return


end subroutine new_series_uniform



subroutine series_difference(ifail)

! -- Subroutine SERIES_DIFFERENCE computes a new series based on differences of consecutive
!    terms in an existing time series.

       use tspvar
       use defn
       use inter
       implicit none

       integer, intent(out)   :: ifail

       integer icontext,iseries,ixcon,ierr,iterm,i,j
       character*10 aname
       character*15 aline
       character*25 aoption
       character*25 acontext(MAXCONTEXT)

       ifail=0
       currentblock='SERIES_DIFFERENCE'

       write(*,10) trim(currentblock)
       write(recunit,10) trim(currentblock)
10     format(/,' Processing ',a,' block....')

       icontext=0
       iseries=0
       aname=' '
       ixcon=0

! -- The CLEAN_SERIES block is first parsed.

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
         if(aoption.eq.'CONTEXT')then
           if(ixcon.ne.0)then
             call num2char(iline,aline)
             call addquote(infile,astring)
             write(amessage,41) trim(aline),trim(astring)
41           format('CONTEXT keyword in incorrect location at line ',a,' of file ',a)
             go to 9800
           end if
           call read_context(ierr,icontext,acontext)
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'NEW_SERIES_NAME')then
           call read_new_series_name(ierr,aname)
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'SERIES_NAME')then
           call read_series_name(ierr,iseries,'SERIES_NAME')
           if(ierr.ne.0) go to 9800
         else if(aoption.eq.'END')then
           go to 200
         else
           call num2char(iline,aline)
           call addquote(infile,astring)
           write(amessage,90) trim(aoption),trim(currentblock),trim(aline),trim(astring)
90         format('unexpected keyword - "',a,'" in ',a,' block at line ',a, &
           ' of file ',a)
           go to 9800
         end if
       end do

! -- The block has been read; now it is checked for correctness.

200    continue
       if(iseries.eq.0)then
         write(amessage,210) trim(currentblock)
210      format('no SERIES_NAME keyword provided in ',a,' block.')
         go to 9800
       end if
       if(icontext.eq.0)then
         write(amessage,220) trim(currentblock)
220      format('no CONTEXT keyword(s) provided in ',a,' block.')
         go to 9800
       end if
       if(series(iseries)%nterm.eq.1)then
         write(amessage,213) trim(series(iseries)%name),trim(currentblock)
213      format('specified series "',a,'" must have more than one term in ',a,' block.')
         go to 9800
       end if
       if(aname.eq.' ')then
         write(amessage,214) trim(currentblock)
214      format('no NEW_SERIES_NAME keyword provided in ',a,' block.')
         go to 9800
       end if

! -- Space is allocated for the new time series.

       iterm=series(iseries)%nterm-1
       do i=1,MAXSERIES
         if(.not.series(i)%active) go to 515
       end do
       write(amessage,510)
510    format('no more time series available for data storage - increase MAXSERIES and ', &
       'recompile program.')
       go to 9800

515    allocate(series(i)%days(iterm),series(i)%secs(iterm),  &
       series(i)%val(iterm),stat=ierr)
       if(ierr.ne.0)then
         write(amessage,550)
550      format('cannot allocate memory for another time series.')
         go to 9800
       end if
       series(i)%active=.true.
       series(i)%name=aname
       series(i)%nterm=iterm
       series(i)%type='ts'
       do j=2,series(iseries)%nterm
         series(i)%days(j-1)=series(iseries)%days(j)
         series(i)%secs(j-1)=series(iseries)%secs(j)
         series(i)%val(j-1)=series(iseries)%val(j)-series(iseries)%val(j-1)
       end do

       write(*,590) trim(aname)
       write(recunit,590) trim(aname)
590    format(t5,'Series "',a,'" successfully calculated.')
       return

9000   call num2char(iline,aline)
       call addquote(infile,astring)
       write(amessage,9010) trim(aline), trim(astring)
9010   format('cannot read line ',a,' of TSPROC input file ',a)
       go to 9800
9100   continue
       call addquote(infile,astring)
       write(amessage,9110) trim(astring), trim(currentblock)
9110   format('unexpected end encountered to TSPROC input file ',a,' while ', &
       ' reading ',a,' block.')
       go to 9800

9800   call write_message(leadspace='yes',error='yes')
       call write_message(iunit=recunit,leadspace='yes')
       ifail=1

       return

end subroutine series_difference


!     Last change:  JD   22 Sep 2001    9:36 pm
subroutine read_new_series_name(ifail,aname)

! -- Subroutine READ_NEW_SERIES_NAME retreives a new series name from a block in
!    the TSPROC input file.

       use tspvar
       use defn
       use inter
       implicit none

       integer, intent(out)         :: ifail
       character(*), intent(out)    :: aname
       integer ierr,nn,i
       character*20 atemp,aline

       ifail=0
       call getfile(ierr,cline,atemp,left_word(2),right_word(2))
       if(ierr.ne.0)then
         call num2char(iline,aline)
         call addquote(infile,astring)
         write(amessage,71) trim(aline), trim(astring)
71       format('cannot read NEW_SERIES_NAME from line ',a,' of file ',a)
         go to 9800
       end if
       nn=len_trim(atemp)
       if(nn.gt.10)then
         call num2char(iline,aline)
         call addquote(infile,astring)
         write(amessage,77) trim(atemp),trim(aline),trim(astring)
77       format('series name "',a,'" greater than 10 characters at line ',a,  &
         ' of file ',a)
         go to 9800
       end if
       aname=atemp(1:10)
       if(isspace(aname))then
         call num2char(iline,aline)
         call addquote(infile,astring)
         write(amessage,81) trim(aname),trim(aline),trim(astring)
81       format('space character in NEW_SERIES_NAME "',a,'" at line ',a,' of file ',a)
         go to 9800
       end if
       call casetrans(aname,'lo')
       write(*,74) trim(aname)
       write(recunit,74) trim(aname)
74     format(t5,'NEW_SERIES_NAME ',a)
       do i=1,MAXSERIES
         if(series(i)%active)then
            if(series(i)%name.eq.aname)then
              call num2char(iline,aline)
              call addquote(infile,astring)
              write(amessage,68) trim(aname),trim(aline),trim(astring)
68            format('the name "',a,'" at line ',a,' of file ',a,' is already used by ', &
              'another active series.')
              go to 9800
            end if
         end if
       end do
         do i=1,MAXSTABLE
           if(stable(i)%active)then
             if(stable(i)%name.eq.aname)then
               call num2char(iline,aline)
               call addquote(infile,astring)
               write(amessage,61) trim(aname),trim(aline),trim(astring)
61             format('the name "',a,'" at line ',a,' of file ',a,' is already used by ', &
               'an active s_table.')
               go to 9800
             end if
           end if
         end do
         do i=1,MAXVTABLE
           if(vtable(i)%active)then
             if(vtable(i)%name.eq.aname)then
               call num2char(iline,aline)
               call addquote(infile,astring)
               write(amessage,69) trim(aname),trim(aline),trim(astring)
69             format('the name "',a,'" at line ',a,' of file ',a,' is already used by ', &
               'an active v_table.')
               go to 9800
             end if
           end if
         end do
         do i=1,MAXDTABLE
           if(dtable(i)%active)then
             if(dtable(i)%name.eq.aname)then
               call num2char(iline,aline)
               call addquote(infile,astring)
               write(amessage,66) trim(aname),trim(aline),trim(astring)
66             format('the name "',a,'" at line ',a,' of file ',a,' is already used by ', &
               'an active e_table.')
               go to 9800
             end if
           end if
         end do


       return

9800   ifail=1
       return

end subroutine read_new_series_name


subroutine read_file_name(ifail,afile)

! -- Subroutine READFILE retreives a file name from a data block on
!    the TSPROC input file.

       use tspvar
       use defn
       use inter
       implicit none

       integer, intent(out)         :: ifail
       character(*), intent(out)    :: afile
       integer ierr
       character*20 aline

       ifail=0
       call getfile(ierr,cline,afile,left_word(2),right_word(2))
       if(ierr.ne.0)then
         call num2char(iline,aline)
         call addquote(infile,astring)
         write(amessage,30) trim(aline),trim(astring)
30       format('cannot read filename from line ',a,' of file ',a)
         go to 9800
       end if
       call addquote(afile,astring)
       write(*,40) trim(astring)
       write(recunit,40) trim(astring)
40     format(t5,'FILE ',a)
       return

9800   ifail=1
       return

end subroutine read_file_name


subroutine read_date(ifail,dd1,mm1,yy1,alabel)

! -- Subroutine READ_DATE reads a date from a block of the TSPROC input file.

       use tspvar
       use defn
       use inter
       implicit none

       integer, intent(out)         :: ifail
       integer, intent(inout)       :: dd1,mm1,yy1
       character(*), intent(in)     :: alabel

       integer ierr
       character*20 aline,adate

       ifail=0
       adate=cline(left_word(2):right_word(2))
       call char2date(ierr,adate,dd1,mm1,yy1)
       if(ierr.ne.0)then
         call num2char(iline,aline)
         call addquote(infile,astring)
         write(amessage,60) trim(aline),trim(astring)
60       format('illegal date at line ',a,' of TSPROC input file ',a)
         go to 9800
       end if
       write(*,65) trim(alabel),trim(adate)
       write(recunit,65) trim(alabel), trim(adate)
65     format(t5,a,' ',a)
       return

9800   ifail=1
       return

end subroutine read_date



subroutine read_time(ifail,hh1,nn1,ss1,alabel)

! -- Subroutine READ_TIME reads a time from a block of the TSPROC input file.

       use tspvar
       use defn
       use inter
       implicit none

       integer, intent(out)          :: ifail
       integer, intent(inout)        :: hh1,nn1,ss1
       character*(*), intent(in)     :: alabel

       integer ierr
       character*20 aline,atime

       ifail=0
       atime=cline(left_word(2):right_word(2))
       call char2time(ierr,atime,hh1,nn1,ss1,ignore_24=1)
       if(ierr.ne.0)then
          call num2char(iline,aline)
          call addquote(infile,astring)
          write(amessage,70) trim(aline),trim(astring)
70        format('illegal time at line ',a,' of TSPROC input file ',a)
          go to 9800
        end if
        write(*,75) trim(alabel),trim(atime)
        write(recunit,75) trim(alabel),trim(atime)
75      format(t5,a,' ',a)
        return

9800   ifail=1
       return

end subroutine read_time



subroutine read_context(ifail,icontext,acontext)

! -- Subroutine READ_CONTEXT reads a context string from a block of the
!    TSPROC input file.

       use tspvar
       use defn
       use inter
       implicit none

       integer, intent(out)            :: ifail
       integer, intent(inout)          :: icontext
       character*(*), intent(inout)    :: acontext(MAXCONTEXT)

       integer ierr
       character*20 aline,aaline

       ifail=0

       icontext=icontext+1
       if(icontext.gt.MAXCONTEXT)then
         call num2char(MAXCONTEXT,aline)
         call num2char(iline,aaline)
         call addquote(infile,astring)
         write(amessage,69) trim(aline),trim(aaline),trim(astring)
69       format('maximum of ',a,' CONTEXTs can be supplied in a ', &
         'TSPROC block. Violation at line ',a,' of file ',a)
         go to 9800
       end if
       call getfile(ierr,cline,acontext(icontext),left_word(2),right_word(2))
       if(ierr.ne.0)then
         call num2char(iline,aline)
         call addquote(infile,astring)
         write(amessage,78) trim(aline),trim(astring)
78       format('cannot read CONTEXT from line ',a,' of file ',a)
         go to 9800
       end if
       if(isspace(acontext(icontext)))then
         call num2char(iline,aline)
         call addquote(infile,astring)
         write(amessage,82) trim(acontext(icontext)),trim(aline),trim(astring)
82       format('space character in CONTEXT string "',a,'" at line ',a,' of file ',a)
         go to 9800
       end if
       call casetrans(acontext(icontext),'lo')
       write(*,79) trim(acontext(icontext))
       write(recunit,79) trim(acontext(icontext))
79     format(t5,'CONTEXT ',a)
       return

9800   ifail=1
       return

end subroutine read_context



subroutine read_series_name(ifail,iseries,aword)

! -- Subroutine READ_SERIES_NAME reads a series name from a block of the
!    TSPROC input file. It is assumed that the series name represents an already
!    active time series.

       use tspvar
       use defn
       use inter
       implicit none

       integer, intent(out)            :: ifail
       integer, intent(inout)          :: iseries

       integer ierr,nn,i
       character*10 aname
       character*20 aline,atemp
       character*(*) aword

       ifail=0

       call getfile(ierr,cline,atemp,left_word(2),right_word(2))
       if(ierr.ne.0)then
         call num2char(iline,aline)
         call addquote(infile,astring)
         write(amessage,110) trim(aline),trim(astring)
110      format('cannot read series name from line ',a,' of file ',a)
         go to 9800
       end if
       nn=len_trim(atemp)
       if(nn.gt.10)then
         call num2char(iline,aline)
         call addquote(infile,astring)
         write(amessage,120) trim(atemp),trim(aline),trim(astring)
120      format('series name "',a,'" greater than 10 characters at line ',a, &
         ' of file ',a)
         go to 9800
       end if
       aname=atemp(1:10)
       if(isspace(aname))then
         call num2char(iline,aline)
         call addquote(infile,astring)
         write(amessage,121) trim(aname),trim(aline),trim(astring)
121      format('space character in series name "',a,'" at line ',a,' of file ',a)
         go to 9800
       end if
       call casetrans(aname,'lo')
       write(*,140) trim(aword),trim(aname)
       write(recunit,140) trim(aword),trim(aname)
140    format(t5,a,' ',a)
       do i=1,MAXSERIES
         if(.not.series(i)%active) cycle
         if(series(i)%name.eq.aname)then
           iseries=i
           go to 130
         end if
       end do
       call num2char(iline,aline)
       call addquote(infile,astring)
       write(amessage,160) trim(aname),trim(aline),trim(astring)
160    format('series name "',a,'" at line ',a,' of TSPROC input file ',a,  &
       ' has not been read or calculated, or has been erased.')
       go to 9800
130    continue
       return

9800   ifail=1
       return

end subroutine read_series_name



subroutine read_table_name(ifail,itable,jtype)

! -- Subroutine READ_TABLE_NAME reads a table name from a block of the
!    TSPROC input file. It is assumed that the table name represents an already
!    active table.

       use tspvar
       use defn
       use inter
       implicit none

       integer, intent(out)            :: ifail
       integer, intent(inout)          :: itable
       integer, intent(in)             :: jtype

       integer ierr,nn,i,itype
       character*10 aname
       character*20 aline,atemp

       ifail=0
       itype=jtype

       do
         if(itype.lt.10)exit
         itype=itype-10
       end do
       call getfile(ierr,cline,atemp,left_word(2),right_word(2))
       if(ierr.ne.0)then
         call num2char(iline,aline)
         call addquote(infile,astring)
         write(amessage,110) trim(aline),trim(astring)
110      format('cannot read table name from line ',a,' of file ',a)
         go to 9800
       end if
       nn=len_trim(atemp)
       if(nn.gt.10)then
         call num2char(iline,aline)
         call addquote(infile,astring)
         write(amessage,120) trim(atemp),trim(aline),trim(astring)
120      format('table name "',a,'" greater than 10 characters at line ',a, &
         ' of file ',a)
         go to 9800
       end if
       aname=atemp(1:10)
       if(isspace(aname))then
         call num2char(iline,aline)
         call addquote(infile,astring)
         write(amessage,121) trim(aname),trim(aline),trim(astring)
121      format('space character in table name "',a,'" at line ',a,' of file ',a)
         go to 9800
       end if
       call casetrans(aname,'lo')
       if(jtype.eq.1)then
         write(*,140) trim(aname)
         write(recunit,140) trim(aname)
140      format(t5,'S_TABLE_NAME ',a)
       else if(jtype.eq.2)then
         write(*,141) trim(aname)
         write(recunit,141) trim(aname)
141      format(t5,'V_TABLE_NAME ',a)
       else if(jtype.eq.3)then
         write(*,142) trim(aname)
         write(recunit,142) trim(aname)
142      format(t5,'E_TABLE_NAME ',a)
       else if(jtype.eq.4)then
         write(*,151) trim(aname)
         write(recunit,151) trim(aname)
151      format(t5,'C_TABLE_NAME ',a)
       else if(jtype.eq.11)then
         write(*,143) trim(aname)
         write(recunit,143) trim(aname)
143      format(t5,'OBSERVATION_S_TABLE_NAME ',a)
       else if(jtype.eq.12)then
         write(*,144) trim(aname)
         write(recunit,144) trim(aname)
144      format(t5,'OBSERVATION_V_TABLE_NAME ',a)
       else if(jtype.eq.13)then
         write(*,145) trim(aname)
         write(recunit,145) trim(aname)
145      format(t5,'OBSERVATION_E_TABLE_NAME ',a)
       else if(jtype.eq.21)then
         write(*,146) trim(aname)
         write(recunit,146) trim(aname)
146      format(t5,'MODEL_S_TABLE_NAME ',a)
       else if(jtype.eq.22)then
         write(*,147) trim(aname)
         write(recunit,147) trim(aname)
147      format(t5,'MODEL_V_TABLE_NAME ',a)
       else if(jtype.eq.23)then
         write(*,148) trim(aname)
         write(recunit,148) trim(aname)
148      format(t5,'MODEL_E_TABLE_NAME ',a)
       end if
       if(itype.eq.1)then
         do i=1,MAXSTABLE
           if(.not.stable(i)%active) cycle
           if(stable(i)%name.eq.aname)then
             itable=i
             go to 130
           end if
         end do
         call num2char(iline,aline)
         call addquote(infile,astring)
         write(amessage,160) trim(aname),trim(aline),trim(astring)
160      format('S_TABLE "',a,'" cited at line ',a,' of file ',a,   &
         ' has not been read or calculated, or has been erased.')
         go to 9800
130      continue
       else if(itype.eq.2)then
         do i=1,MAXVTABLE
           if(.not.vtable(i)%active) cycle
           if(vtable(i)%name.eq.aname)then
             itable=i
             go to 131
           end if
         end do
         call num2char(iline,aline)
         call addquote(infile,astring)
         write(amessage,161) trim(aname),trim(aline),trim(astring)
161      format('V_TABLE "',a,'" cited at line ',a,' of file ',a,   &
         ' has not been read or calculated, or has been erased.')
         go to 9800
131      continue
       else if(itype.eq.3)then
         do i=1,MAXDTABLE
           if(.not.dtable(i)%active) cycle
           if(dtable(i)%name.eq.aname)then
             itable=i
             go to 132
           end if
         end do
         call num2char(iline,aline)
         call addquote(infile,astring)
         write(amessage,162) trim(aname),trim(aline),trim(astring)
162      format('E_TABLE "',a,'" cited at line ',a,' of file ',a,    &
         ' has not been read or calculated, or has been erased.')
         go to 9800
132      continue
       else if(itype.eq.4)then
         do i=1,MAXCTABLE
           if(.not.ctable(i)%active) cycle
           if(ctable(i)%name.eq.aname)then
             itable=i
             go to 172
           end if
         end do
         call num2char(iline,aline)
         call addquote(infile,astring)
         write(amessage,171) trim(aname),trim(aline),trim(astring)
171      format('C_TABLE "',a,'" cited at line ',a,' of file ',a,    &
         ' has not been read or calculated, or has been erased.')
         go to 9800
172      continue
       end if
       return

9800   ifail=1
       return

end subroutine read_table_name





subroutine date_check(ifail,yy1,mm1,dd1,hh1,nn1,ss1,yy2,mm2,dd2,hh2,nn2,ss2,  &
       begdays,begsecs,enddays,endsecs)

! -- Subroutine DATE_CHECK checks the integrity of date and time information
!    supplied through a TSPROC data block.

       use tspvar
       use defn
       use inter
       implicit none

       integer, intent(out)            :: ifail
       integer, intent(inout)          :: yy1,mm1,dd1,hh1,nn1,ss1,  &
                                          yy2,mm2,dd2,hh2,nn2,ss2
       integer, intent(out)            :: begdays,begsecs,enddays,endsecs

       integer nn,ss

       ifail=0

       if(yy1.eq.-9999)then
         if(hh1.ne.-9999)then
           write(amessage,530) trim(currentblock)
530        format('TIME_1 specifier provided, but no DATE_1 specifier in ',a,' block.')
           go to 9800
         end if
       end if
       if(yy2.eq.-9999)then
         if(hh2.ne.-9999)then
           write(amessage,540) trim(currentblock)
540        format('TIME_2 specifier provided, but no DATE_2 specifier in ',a,' block.')
           go to 9800
         end if
       end if
       if(hh1.EQ.-9999)then
!         hh1=0
         hh1=24
         nn1=0
         ss1=0
       end if
       if(hh2.EQ.-9999)then
!         hh2=0
         hh2=24
         nn2=0
         ss2=0
       end if
       if((yy1.ne.-9999).and.(yy2.ne.-9999))then
         nn=numdays(dd1,mm1,yy1,dd2,mm2,yy2)
         ss=numsecs(hh1,nn1,ss1,hh2,nn2,ss2)
         if((nn.lt.0).or.((nn.eq.0).and.(ss.le.0)))then
           write(amessage,570) trim(currentblock)
570        format('first date/time does not precede second date/time in ',a,' block.')
           go to 9800
         end if
       end if
       if(yy1.ne.-9999)then
         begdays=numdays(1,1,1970,dd1,mm1,yy1)
       else
         begdays=-99999999
       end if
       begsecs=numsecs(0,0,0,hh1,nn1,ss1)
571    if(begsecs.ge.86400)then
         begsecs=begsecs-86400
         begdays=begdays+1
         go to 571
       end if
       if(yy2.ne.-9999)then
         enddays=numdays(1,1,1970,dd2,mm2,yy2)
       else
         enddays=99999999
       end if
       endsecs=numsecs(0,0,0,hh2,nn2,ss2)
572    if(endsecs.ge.86400)then
         endsecs=endsecs-86400
         enddays=enddays+1
         go to 572
       end if
       if((begdays.eq.enddays).and.(begsecs.eq.endsecs))then
         write(amessage,570) trim(currentblock)
         go to 9800
       end if

       return

9800   ifail=1
       return

end subroutine date_check



subroutine test_context(ifail,icontext,acontext)

! -- Subroutine TEST_CONTEXT checks whether the context is such that processing
!    should continue.

       use tspvar
       use defn
       use inter
       implicit none

       integer, intent(out)            :: ifail
       integer, intent(in)             :: icontext
       character*(*), intent(in)       :: acontext(icontext)

       integer i
       character*10 aline

       ifail=0
       if(icontext.eq.0)then
         call num2char(iline,aline)
         call addquote(infile,astring)
         write(amessage,10) trim(aline),trim(astring)
10       format('one of more CONTEXT keywords should lead any TSPROC block at ', &
         'line ',a,' of file ',a)
         ifail=1
         return
       end if
       do i=1,icontext
         if(acontext(i).eq.context)go to 174
         if(acontext(i).eq.'all') go to 174
       end do
       write(*,175)
       write(recunit,175)
175    format(t5,'Requested actions not undertaken because no CONTEXT option in the')
       write(*,176)
       write(recunit,176)
176    format(t5,' block coincides with the current run context.')
       ifail=-1
       return

174    continue
       return

end subroutine test_context



subroutine alloc_tempseries(ifail,iterm)


! -- Subroutine ALLOC_TEMPSERIES allocates (or re-allocates) memory for the temporary
!    time series.

       use tspvar
       use defn
       use inter
       implicit none

       integer, intent(out)            :: ifail
       integer, intent(in)             :: iterm

       integer ierr

       ifail=0

       if(.not.tempseries%active)then
         allocate(tempseries%days(iterm),tempseries%secs(iterm), &
         tempseries%val(iterm),stat=ierr)
         if(ierr.ne.0)then
           write(amessage,340)
340        format('cannot allocate sufficient memory to continue execution.')
           go to 9800
         end if
         tempseries%nterm=iterm
         tempseries%active=.true.
       else
         if(iterm.gt.tempseries%nterm)then
           deallocate(tempseries%days,tempseries%secs,tempseries%val,stat=ierr)
           if(ierr.ne.0)then
             write(amessage,355)
355          format('error #1 in expanding memory allocation for temporary time series.')
             go to 9800
           end if
           nullify(tempseries%days,tempseries%secs,tempseries%val)
           allocate(tempseries%days(iterm),tempseries%secs(iterm), &
           tempseries%val(iterm),stat=ierr)
           if(ierr.ne.0)then
             write(amessage,360)
360          format('cannot expand memory allocation for temporary time series')
             go to 9800
           end if
           tempseries%nterm=iterm
         end if
       end if
       return

9800   ifail=1
       return

end subroutine alloc_tempseries


subroutine get_yes_no(ifail,iyesno)

! -- Subroutine GET_YES_NO reads "yes" or "no" from a TSPROC input file.

       use tspvar
       use defn
       use inter
       implicit none

       integer, intent(out)            :: ifail
       integer, intent(inout)          :: iyesno

       integer ierr
       character*10 atemp,aline
       character*3 ayesno

       ifail=0
       call getfile(ierr,cline,atemp,left_word(2),right_word(2))
       if(ierr.ne.0) go to 9000
       if(len_trim(atemp).gt.3) go to 9000
       ayesno=atemp(1:3)
       call casetrans(ayesno,'lo')
       if(ayesno.eq.'yes')then
         iyesno=1
       else if(ayesno.eq.'no')then
         iyesno=0
       else
         go to 9000
       end if
       return

9000   ifail=1
       call num2char(iline,aline)
       call addquote(infile,astring)
       write(amessage,9010) trim(aline),trim(astring)
9010   format('"yes" or "no" expected as the second entry at line ',a,' of file ',a)
       return

end subroutine



subroutine beg_end_check(ifail,iseries,begdays,begsecs,enddays,endsecs)

! -- Subroutine BEG_END_CHECK checks that DATE_1, DATE_2, TIME_1 and TIME_2
!    are compatible with a given time series.

       use tspvar
       use defn
       use inter
       implicit none

       integer, intent(out)            :: ifail
       integer, intent(in)             :: iseries,begdays,begsecs,enddays,endsecs

       integer jterm

       ifail=0

       jterm=series(iseries)%nterm
       if((begdays.gt.series(iseries)%days(jterm)).or.        &
         ((begdays.eq.series(iseries)%days(jterm)).and.       &
          (begsecs.gt.series(iseries)%secs(jterm)))) then
          write(amessage,240) trim(series(iseries)%name)
240       format('DATE_1 and TIME_1 postdate the end of time series "',a,'".')
          go to 9800
       end if
       if((enddays.lt.series(iseries)%days(1)).or.            &
         ((enddays.eq.series(iseries)%days(1)).and.           &
          (endsecs.lt.series(iseries)%secs(1)))) then
          write(amessage,250) trim(series(iseries)%name)
250       format('DATE_2 and TIME_2 precede the start of time series "',a,'".')
          go to 9800
       end if

       return

9800   ifail=1
       return

end subroutine beg_end_check



subroutine numterms(iterm,ibterm,ieterm,begdays,begsecs,enddays,endsecs,iseries)

! -- Subroutine NUMTERMS counts the number of terms in a series between two dates
!    and times.

       use tspvar
       use defn
       use inter
       implicit none

       integer, intent(in)             :: iseries,begdays,begsecs,enddays,endsecs
       integer, intent(out)            :: iterm,ibterm,ieterm

       integer i,jterm

       ibterm=0
       ieterm=0
       iterm=0
       jterm=series(iseries)%nterm
       do i=1,jterm
         if((begdays.gt.series(iseries)%days(i)).or.          &
           ((begdays.eq.series(iseries)%days(i)).and.         &
            (begsecs.gt.series(iseries)%secs(i)))) cycle
            if(ibterm.eq.0)ibterm=i
         if((enddays.lt.series(iseries)%days(i)).or.           &
           ((enddays.eq.series(iseries)%days(i)).and.          &
            (endsecs.lt.series(iseries)%secs(i))))go to 300
         iterm=iterm+1
       end do
       ieterm=jterm
       go to 310
300    ieterm=i-1
310    continue

       return

end subroutine numterms



subroutine time_interp_s(ifail,nbore,ndays,nsecs,value,intday,intsec, &
rnear,rconst,valinterp,extrap,direction,startindex)

! -- Subroutine time_interp_s interpolates an array of times and values to a
!    user-supplied time. It is slightly modified from time_interp, the only
!    change being that the value array is now single precision, as is the
!    interpolated value.

! -- Arguments are as follows:-
!       ifail:     returned as zero unless an error condition arises
!       nbore:     number of times and corresponding values to be interpolated
!       ndays:     elapsed days corresponding to each value
!       nsecs:     elpased seconds corresponding to each value
!       value:     array of time-based values to be interpolated
!       intday:    the day to be interpolated to, expressed as elapsed days
!       intsec:    the time to be intepolated to, expressed as elapsed seconds
!       rnear:     maximum permitted days to nearest sample
!       rconst:    maximum days to nearest sample if interpolation cannot take
!                  place
!       valinterp: interpolated value
!       extrap:    'yes' if use linear extrapolation to (within rconst) if
!                  interpolation cannot take place
!       direction: 'lo' if extrapolation from two previous points,
!                  'hi' if extrapolation from two following points,
!                  'med' if interpolation if possible, otherwise extrapolation
!                  (note: 'med' is the default)
!       startindex: index of bore index at which to start the search through the
!                   table


	use defn
	use inter

	integer, intent(out)                    :: ifail
	integer, intent(in)                     :: nbore
	integer, intent(in), dimension(nbore)   :: ndays,nsecs
	real, intent(in), dimension(nbore)      :: value
	integer, intent(in)                     :: intday,intsec
	real, intent(in)                        :: rnear,rconst
	real, intent(out)                       :: valinterp
	character (len=*), intent(in), optional :: extrap
	character (len=*), intent(in), optional :: direction
        integer, intent(inout), optional        :: startindex

	integer                                 :: i,ie,id,istart,is
	double precision                        :: secfac,diff,diff1,dentime
	character (len=3)                       :: atemp


	ie=0
	if(present(extrap)) then
	  atemp=extrap
	  call casetrans(atemp,'lo')
	  if(atemp.eq.'yes')then
	    ie=1
	  else if(atemp.eq.'no') then
	    ie=0
	  else
	    call sub_error('TIME_INTERP_S')
	  end if
	end if

	id=0
	if(present(direction))then
	  atemp=direction
	  call casetrans(atemp,'lo')
	  if(atemp.eq.'lo')then
	    id=-1
	  else if(atemp.eq.'hi')then
	    id=1
	  else if(atemp.eq.'med')then
	    id=0
	  else
	    call sub_error('TIME_INTERP')
	  end if
	end if

	if((id.ne.0).and.(ie.eq.0))then
	  call sub_error('TIME_INTERP')
	end if

        if(present(startindex))then
          istart=startindex
          is=1
        else
          istart=1
          is=0
        end if
        if(istart.lt.1)istart=1
        if(istart.gt.nbore-1) istart=nbore-1

	ifail=0
	secfac=1.0d0/86400.0d0
	if(nbore.eq.1) then
	  diff=dble(intday-ndays(1))+dble(intsec-nsecs(1))*secfac
	  if(abs(diff).le.rconst)then
	    valinterp=value(1)
	  else
	    if(diff.gt.0)then
	      valinterp=-9.1e37
	    else
	      valinterp=-8.1e37
	    end if
	  end if
	  return
	end if

!	do i=1,nbore-1
!	  if((ndays(i).gt.ndays(i+1)).or. &
!	    ((ndays(i).eq.ndays(i+1)).and.(nsecs(i).ge.nsecs(i+1))))then
!	    ifail=1
!	    return
!	  end if
!	end do

	do i=istart,nbore
	  diff=dble(ndays(i)-intday)+dble(nsecs(i)-intsec)*secfac
	  if(diff.ge.0)then
	    if(i.eq.1)then
	      if(diff.le.rconst)then
	        if(ie.eq.1)then
	          if((value(1).lt.-1.0e38).or.(value(2).lt.-1.0e38))then
	            valinterp=value(1)
	          else
	            dentime=dble(ndays(i+1)-ndays(i))+ &
                            dble(nsecs(i+1)-nsecs(i))*secfac 
	            if(dentime.le.0) then
	              ifail=1
	              go to 9000
	            else
	              valinterp=value(i)-(value(i+1)-value(i))*diff/dentime
	            end if
	          end if
	        else
		  valinterp=value(1)
	        end if
	      else
		valinterp=-8.1e37
	      end if
	      go to 9000
	    end if

	    if(id.eq.-1)then
	      if(i.eq.2)then
	        diff1=dble(intday-ndays(1))+dble(intsec-nsecs(1))*secfac
	        if(diff1.gt.rnear)then               !note - not rconst
	          valinterp=-7.1e37
	        else
	          valinterp=value(1)
	        end if
	        if(value(1).lt.-1.0e38) valinterp=-1.1e38
	      else
	        dentime=dble(ndays(i-1)-ndays(i-2))+ &
                        dble(nsecs(i-1)-nsecs(i-2))*secfac
	        if(dentime.lt.0.0d0)then
	          ifail=1
	          go to 9000
	        else
	          diff1=dble(intday-ndays(i-1))+  &
                  dble(intsec-nsecs(i-1))*secfac
	          if(diff1.gt.rnear)then
	            valinterp=-7.1e37
	          else
	            if(value(i-1).lt.-1.0e38)then
	              valinterp=-1.1e38
	            else if(value(i-2).lt.-1.0e38) then
	              valinterp=value(i-1)
	            else
	              valinterp=value(i-1)+ &
                      (value(i-1)-value(i-2))/dentime*diff1
	            end if
	          end if
	        end if
	      end if
	      go to 9000
	    else if(id.eq.1)then
	      if(i.eq.nbore)then
	        if(diff.gt.rnear)then
	          valinterp=-7.1e37
	        else
	          valinterp=value(i)
	        end if
	        if(value(i).lt.-1.0e38)valinterp=-1.1e38
	      else
	        dentime=dble(ndays(i+1)-ndays(i))+      &
	                dble(nsecs(i+1)-nsecs(i))*secfac
	        if(dentime.le.0)then
	          ifail=1
	          go to 9000
	        else
	          if(diff.gt.rnear)then
	            valinterp=-7.1e37
	          else
	            if(value(i).lt.-1.0e38)then
	              valinterp=-1.1e38
	            else if(value(i+1).lt.-1.0e38)then
	              valinterp=value(i)
	            else
	              valinterp=value(i)-  &
                      (value(i+1)-value(i))/dentime*diff
	            end if
	          end if
	        end if
	      end if
	      go to 9000
	    else 

	      dentime=dble(ndays(i)-ndays(i-1))+ &
	      dble(nsecs(i)-nsecs(i-1))*secfac
	      if(dentime.le.0)then
	        ifail=1
	        go to 9000
	      else 
	        diff1=dentime-diff
	        if((diff1.gt.rnear).and.(diff.gt.rnear))then
		  valinterp=-7.1e37
	        else
		  valinterp=value(i-1)+(value(i)-value(i-1))/dentime*diff1
	        end if
	        if(value(i).lt.-1.0e38)then
		  if(diff1.le.rconst)then
		    valinterp=value(i-1)
		  else
		    valinterp=-1.1e38
		  end if
	        else if(value(i-1).lt.-1.0e38)then
		  if(diff.le.rconst)then
		    valinterp=value(i)
		  else
		    valinterp=-1.1e38
		  end if
	        end if
	      end if
	    go to 9000
	    end if
	  end if
	end do

	diff1=dble(intday-ndays(nbore))+dble(intsec-nsecs(nbore))*secfac
	if(diff1.le.rconst)then
	  if(ie.eq.1) then
	    if((value(nbore).lt.-1.0e38).or.(value(nbore-1).lt.-1.0e38)) then
	      valinterp=value(nbore)
	    else
	      dentime=dble(ndays(nbore)-ndays(nbore-1))    &
                     +dble(nsecs(nbore)-nsecs(nbore-1))*secfac
	      if(dentime.le.0) then
	        ifail=1
	        go to 9000
	      else
	        valinterp=value(nbore)+(value(nbore)-value(nbore-1))*    &
                diff1/dentime
	      end if
	    end if
	  else
	    valinterp=value(nbore)
	  end if
	else
	  valinterp=-9.1e37
	end if

9000    continue
        if(is.eq.1)then
          if(ifail.eq.0)then
            startindex=i
          else
            startindex=0
          end if
        end if

	return
end subroutine time_interp_s



subroutine read_new_table_name(ifail,itype,aname)

! -- Subroutine READ_NEW_TABLE_NAME reads the name of a new table.

       use tspvar
       use defn
       use inter
       implicit none

       integer, intent(out)            :: ifail
       integer, intent(in)             :: itype
       character*(*), intent(out)      :: aname

       integer ierr,nn,i
       character*20 aline,atemp

       ifail=0

       call getfile(ierr,cline,atemp,left_word(2),right_word(2))
       if(ierr.ne.0)then
         call num2char(iline,aline)
         call addquote(infile,astring)
         write(amessage,71) trim(aline), trim(astring)
71       format('cannot read new table name from line ',a,' of file ',a)
         go to 9800
       end if
       nn=len_trim(atemp)
       if(nn.gt.10)then
         call num2char(iline,aline)
         call addquote(infile,astring)
         write(amessage,77) trim(atemp),trim(aline),trim(astring)
77       format('table name "',a,'" greater than 10 characters at line ',a,  &
         ' of file ',a)
         go to 9800
       end if
       aname=atemp(1:10)
       if(isspace(aname))then
         call num2char(iline,aline)
         call addquote(infile,astring)
         write(amessage,81) trim(aname),trim(aline),trim(astring)
81       format('space character in new table name "',a,'" at line ',a,' of file ',a)
         go to 9800
       end if
       call casetrans(aname,'lo')
       if(itype.eq.1)then
         write(*,74) trim(aname)
         write(recunit,74) trim(aname)
74       format(t5,'NEW_S_TABLE_NAME ',a)
       else if (itype.eq.2)then
         write(*,75) trim(aname)
         write(recunit,75) trim(aname)
75       format(t5,'NEW_V_TABLE_NAME ',a)
       else if(itype.eq.3)then
         write(*,76) trim(aname)
         write(recunit,76) trim(aname)
76       format(t5,'NEW_E_TABLE_NAME ',a)
       else if(itype.eq.4)then
         write(*,78) trim(aname)
         write(recunit,78) trim(aname)
78       format(t5,'NEW_C_TABLE_NAME ',a)       
       end if
!       if(itype.eq.1)then
         do i=1,MAXSTABLE
           if(stable(i)%active)then
             if(stable(i)%name.eq.aname)then
               call num2char(iline,aline)
               call addquote(infile,astring)
               write(amessage,68) trim(aname),trim(aline),trim(astring)
68             format('the name "',a,'" at line ',a,' of file ',a,' is already used ', &
               'by an active s_table.')
               go to 9800
             end if
           end if
         end do
!       else if(itype.eq.2)then
         do i=1,MAXVTABLE
           if(vtable(i)%active)then
             if(vtable(i)%name.eq.aname)then
               call num2char(iline,aline)
               call addquote(infile,astring)
               write(amessage,69) trim(aname),trim(aline),trim(astring)
69             format('the name "',a,'" at line ',a,' of file ',a,' is already used ', &
               'by an active v_table.')
               go to 9800
             end if
           end if
         end do
!       else if(itype.eq.3)then
         do i=1,MAXDTABLE
           if(dtable(i)%active)then
             if(dtable(i)%name.eq.aname)then
               call num2char(iline,aline)
               call addquote(infile,astring)
               write(amessage,66) trim(aname),trim(aline),trim(astring)
66             format('the name "',a,'" at line ',a,' of file ',a,' is already used ', &
               'by an active e_table.')
               go to 9800
             end if
           end if
         end do
!       else if(itype.eq.4)then
         do i=1,MAXCTABLE
           if(ctable(i)%active)then
             if(ctable(i)%name.eq.aname)then
               call num2char(iline,aline)
               call addquote(infile,astring)
               write(amessage,67) trim(aname),trim(aline),trim(astring)
67             format('the name "',a,'" at line ',a,' of file ',a,' is already used ', &
               'by an active c_table.')
               go to 9800
             end if
           end if
         end do
!       end if
         do i=1,MAXSERIES
           if(series(i)%active)then
             if(series(i)%name.eq.aname)then
               call num2char(iline,aline)
               call addquote(infile,astring)
               write(amessage,63) trim(aname),trim(aline),trim(astring)
63             format('the name "',a,'" at line ',a,' of file ',a,' is already used ', &
               'by an active series.')
               go to 9800
             end if
           end if
         end do

       return

9800   ifail=1
       return

end subroutine read_new_table_name



subroutine read_time_units(ifail,itunit,itype)

! -- Subroutine READ_TIME_UNITS reads time units from a TSPROC input file.

       use tspvar
       use defn
       use inter
       implicit none

       integer, intent(out)            :: ifail
       integer, intent(out)            :: itunit
       integer, intent(in)             :: itype

       integer ierr
       character*10 aunit
       character*20 aline,atemp

       ifail=0

       call getfile(ierr,cline,atemp,left_word(2),right_word(2))
       if(ierr.ne.0) go to 9000
       call casetrans(atemp,'lo')
       if(atemp(1:4).eq.'year')then
         itunit=6
         aunit='years'
       else if(atemp(1:5).eq.'month')then
         itunit=5
         aunit='months'
       else if(atemp(1:3).eq.'day')then
         itunit=4
         aunit='days'
       else if(atemp(1:4).eq.'hour')then
         itunit=3
         aunit='hours'
       else if(atemp(1:3).eq.'min')then
         itunit=2
         aunit='minutes'
       else if(atemp(1:3).eq.'sec')then
         itunit=1
         aunit='seconds'
       else
         go to 9000
       end if
       if(itype.eq.1)then
         write(*,120) trim(aunit)
         write(recunit,120) trim(aunit)
120      format(t5,'FLOW_TIME_UNITS ',a)
       else if(itype.eq.2)then
         write(*,121) trim(aunit)
         write(recunit,120) trim(aunit)
121      format(t5,'EXCEEDENCE_TIME_UNITS ',a)
       end if
       return

9000   call num2char(iline,aline)
       call addquote(infile,astring)
       write(amessage,9010) trim(aline), trim(astring)
9010   format('cannot read time units from line ',a,' of file ',a)
       go to 9800

9800   ifail=1
       return

end subroutine read_time_units




subroutine volume_interp_s(ifail,num,days,secs,flows,bdays,bsecs,fdays,fsecs,vol,fac)

! -- Subroutine volume_interp calculates the extracted volume between two dates
!    on the basis of flow rates recorded at certain times. It is a modified version
!    of volume_interp such that the input time series does not need to be double precision.

! -- Arguments are as follows:-
!      num:    number of flow rate samples
!      days:   days since 1/1/1970 pertaining to each flow sample
!      secs:   seconds since midnight pertaining to each flow sample
!      bdays:  days since 1/1/1970 at which volume begins accumulating
!      bsecs:  seconds since midnight at which volume begins accumulating
!      fdays:  days since 1/1/1970 at which volume ceases accumulating
!      fsecs:  seconds since midnight at which volume ceases accumulating
!      vol:    accumulated volume
!      fac:    factor by which to multiply volumes


       integer, intent(out)            :: ifail
       integer, intent(in)             :: num
       integer, intent(in)             :: days(num),secs(num)
       real, intent(in)                :: flows(num)
       integer, intent(in)             :: bdays,bsecs,fdays,fsecs
       real, intent(out)               :: vol
       real, intent(in)                :: fac

       integer i,ndd,j,ndt
       double precision tdd,tdt,m,volb,volm,volf


       ifail=0

! It is assumed that the following checks have already been made.
!       if(bdays.lt.days(1)) go to 9000
!       if(bdays.eq.days(1))then
!         if(bsecs.lt.secs(1)) go to 9000
!       end if
!       if(bdays.gt.days(num)) go to 9100
!       if(bdays.eq.days(num))then
!         if(bsecs.gt.secs(num)) go to 9100
!       end if
!       if(fdays.gt.days(num)) go to 9200
!       if(fdays.eq.days(num))then
!         if(fsecs.gt.secs(num)) go to 9200
!       end if

! -- The volume in the first interval is calculated.

       do i=2,num
         if((days(i).gt.bdays).or.  &
           ((days(i).eq.bdays).and.(secs(i).ge.bsecs))) go to 50
       end do
       go to 9100
50     ndd=days(i)-days(i-1)
       ndt=days(i)-bdays
       tdd=dble(ndd)*86400.0d0+dble(secs(i)-secs(i-1))
       tdt=dble(ndt)*86400.0d0+dble(secs(i)-bsecs)
       if(tdd.le.0.0d0) go to 9400
       m=(flows(i)-flows(i-1))/tdd
       volb=tdt*(flows(i)-m*0.5d0*tdt)

! -- Now we traverse sample intervals until we find the last interval

       volm=0.0d0
       j=i
       do i=j,num
         if((days(i).gt.fdays).or.   &
           ((days(i).eq.fdays).and.(secs(i).ge.fsecs)))go to 100
         if(i.ne.j)then
           ndd=days(i)-days(i-1)
           tdd=dble(ndd)*86400.0d0+dble(secs(i)-secs(i-1))
           volm=volm+0.5*(flows(i)+flows(i-1))*tdd
         end if
       end do
       go to 9200
100    ndd=days(i)-days(i-1)
       ndt=fdays-days(i-1)
       tdd=dble(ndd)*86400.0d0+dble(secs(i)-secs(i-1))
       tdt=dble(ndt)*86400.0d0+dble(fsecs-secs(i-1))
       if(tdd.eq.0.0d0) go to 9400
       m=(flows(i)-flows(i-1))/tdd
       volf=tdt*(flows(i-1)+m*0.5d0*tdt)
       if(i.eq.j)then
         ndd=days(i)-days(i-1)
         tdd=dble(ndd)*86400.0d0+dble(secs(i)-secs(i-1))
         volm=-0.5*(flows(i)+flows(i-1))*tdd
       end if

       vol=(volb+volm+volf)*fac/86400.0d0
       return

!9000   vol=-5.1e37
!       go to 9999
9100   vol=-4.1e37
       go to 9999
9200   vol=-3.1e37
       go to 9999
9400   ifail=1
       go to 9999


9999   return

end subroutine volume_interp_s


subroutine get_keyword_value(ifail,itype,ival,rval,aword)

! -- Subroutine GET_KEYWORD_VALUE retreives a keyword value from a TSPROC input file.

       use tspvar
       use defn
       use inter
       implicit none

       integer, intent(out)        :: ifail
       integer, intent(in)         :: itype
       integer, intent(inout)      :: ival
       real, intent(inout)         :: rval
       character*(*), intent(in)   :: aword

       integer ierr
       character*20 aline

       ifail=0
       if(itype.eq.1)then
         call char2num(ierr,cline(left_word(2):right_word(2)),ival)
       else
         call char2num(ierr,cline(left_word(2):right_word(2)),rval)
       end if
       if(ierr.ne.0)then
         call num2char(iline,aline)
         call addquote(infile,astring)
         write(amessage,120) trim(aword),trim(aline),trim(astring)
120      format('cannot read ',a,' from line ',a,' of file ',a)
         go to 9800
       end if
       if(itype.eq.1)then
         call num2char(ival,aline)
       else
         call num2char(rval,aline,9)
       end if
       write(*,130) trim(aword),trim(aline)
       write(recunit,130) trim(aword),trim(aline)
130    format(t5,a,' ',a)
       return

9800   ifail=1
       return

end subroutine get_keyword_value


subroutine get_keyword_value_double(ifail,itype,ival,rval,aword)

! -- Subroutine GET_KEYWORD_VALUE_DOUBLE retreives a keyword value from a TSPROC input file.
!    It differs from GET_KEYWORD_VALUE in that the value read from the input file
!    can be double precision. This is a little rough. I should have modified
!    GET_KEYWORD_VALUE and put in an optional argumment. But it is quick.

       use tspvar
       use defn
       use inter
       implicit none

       integer, intent(out)                :: ifail
       integer, intent(in)                 :: itype
       integer, intent(inout)              :: ival
       double precision, intent(inout)     :: rval
       character*(*), intent(in)           :: aword

       integer ierr
       character*20 aline

       ifail=0
       if(itype.eq.1)then
         call char2num(ierr,cline(left_word(2):right_word(2)),ival)
       else
         call char2num(ierr,cline(left_word(2):right_word(2)),rval)
       end if
       if(ierr.ne.0)then
         call num2char(iline,aline)
         call addquote(infile,astring)
         write(amessage,120) trim(aword),trim(aline),trim(astring)
120      format('cannot read ',a,' from line ',a,' of file ',a)
         go to 9800
       end if
       if(itype.eq.1)then
         call num2char(ival,aline)
       else
         call num2char(rval,aline,9)
       end if
       write(*,130) trim(aword),trim(aline)
       write(recunit,130) trim(aword),trim(aline)
130    format(t5,a,' ',a)
       return

9800   ifail=1
       return

end subroutine get_keyword_value_double




subroutine get_equation(ifail,eqntext,atext)

       use tspvar
       use defn
       use inter
       implicit none

       integer, intent(out)        :: ifail
       character*(*), intent(out)  :: eqntext
       character*(*), intent(in)   :: atext

       integer ierr,ncl,lnxx,idx,lnx,ixcount
       character*1 aa
       character*20 aline

       ifail=0
       aa=cline(left_word(2):left_word(2))
       if((aa.eq.'"').or.(aa.eq.'''')) then
         cline(left_word(2):left_word(2))=' '
         ncl=len_trim(cline)
         aa=cline(ncl:ncl)
         if((aa.ne.'"').and.(aa.ne.''''))go to 9200
!         call getfile(ierr,cline,eqntext,left_word(2),ncl)
!         if(ierr.ne.0) go to 9200
         cline(ncl:ncl)=' '
         eqntext=cline(left_word(2)+1:)
         eqntext=adjustl(eqntext)
       else
         eqntext=cline(left_word(2):)
!         ncl=len_trim(eqntext)
!         aa=eqntext(ncl:ncl)
!         if((aa.eq.'''').or.(aa.eq.'"')) go to 9200
       end if
       call casetrans(eqntext,'lo')
       write(*,40) trim(atext),trim(eqntext)
       write(recunit,40) trim(atext),trim(eqntext)
40     format(t5,a,' "',a,'"')

! -- Before control is returned, "~" is substituted for "/" in the
!    @_days_"dd/mm/yyyy_hh:mm:ss" function.

       lnxx=len_trim(eqntext)
       idx=1
241    continue
       lnx=index(eqntext(idx:),'@_days_ ')
       if(lnx.ne.0) go to 9500
       lnx=index(eqntext(idx:),'@_days_')
       if(lnx.eq.0) go to 249
       idx=idx+lnx-1
       idx=idx+7
       if(eqntext(idx:idx+9).eq.'start_year') then
         go to 241
       else if((eqntext(idx:idx).eq.'"').or.(eqntext(idx:idx).eq.''''))then
         ixcount=0
243      idx=idx+1
         if(idx.gt.lnxx) go to 9500
         if((eqntext(idx:idx).eq.'"').or.(eqntext(idx:idx).eq.'''')) then
           if(ixcount.ne.2) go to 9500
           go to 241
         end if
         if(eqntext(idx:idx).eq.'/')then
           ixcount=ixcount+1
           if(ixcount.gt.2)go to 9500
           eqntext(idx:idx)=char(196)
         end if
         go to 243
       else
         go to 9500
       end if
249    continue

       return

9200   call num2char(iline,aline)
       call addquote(infile,astring)
       write(amessage,9210) trim(aline),trim(astring)
9210   format('cannot read equation from line ',a,' of TSPROC input file ',a)
       ifail=1
       return

9500   write(amessage,9510)
9510   format('illegal "@_days_" function in weights equation.')
       ifail=1
       return


end subroutine get_equation



subroutine get_two_numbers(ifail,rnum1,rnum2,atext)

       use tspvar
       use defn
       use inter
       implicit none

       integer, intent(out)        :: ifail
       real, intent(out)           :: rnum1,rnum2
       character*(*), intent(in)   :: atext

       integer ierr
       character*13 anum1,anum2

       ifail=0
       cline=cline(left_word(2):)
       call linesplit(ierr,2)
       if(ierr.ne.0) go to 9000
       call char2num(ierr,cline(left_word(1):right_word(1)),rnum1)
       if(ierr.ne.0) go to 9000
       call char2num(ierr,cline(left_word(2):right_word(2)),rnum2)
       if(ierr.ne.0) go to 9000
       call num2char(rnum1,anum1,9)
       call num2char(rnum2,anum2,9)
       write(*,40) trim(atext),trim(anum1),trim(anum2)
       write(recunit,40) trim(atext),trim(anum1),trim(anum2)
40     format(t5,a,' ',a,'   ',a)
       return

9000   continue
       call num2char(iline,anum1)
       call addquote(infile,astring)
       write(amessage,9010) trim(atext),trim(anum1),trim(astring)
9010   format('cannot read two numbers following ',a,' keyword on line ',a,' of file ',a)
       ifail=1
       return

end subroutine get_two_numbers



subroutine check_weight_order(ifail,rmin,rmax)

       use tspvar
       use defn
       use inter
       implicit none

       integer, intent(out)        :: ifail
       real, intent(in)            :: rmin,rmax
       character*15 aline

       ifail=0

       if(rmax.le.rmin)then
         call num2char(iline,aline)
         call addquote(infile,astring)
         write(amessage,10) trim(aline),trim(astring)
10       format('minimum exceeds maximum at line ',a,' of file ',a)
         ifail=1
       end if

       return

end subroutine check_weight_order


subroutine remchar(astring,ach)

       implicit none

       character*(*), intent(inout) :: astring
       character*(*), intent(in)    :: ach

       integer ll,ii,icount

       icount=0
       ll=len_trim(ach)

10     ii=index(astring,ach)
       if(ii.eq.0) then
         if(icount.eq.0)return
         go to 20
       end if
       icount=icount+1
       astring(ii:ii-1+ll)=' '
       go to 10

20     astring=adjustl(astring)
       return

end subroutine remchar



subroutine make_basename(ifail,iout,nsterm,aname,basename)

! -- Subroutine MAKE_BASENAME formulates the basename of observation names pertaining
!    to a SERIES, V_TABLE or E_TABLE.

       use tspvar
       use defn
       use inter
       implicit none

       integer, intent(out)               :: ifail
       integer, intent(in)                :: iout,nsterm
       character*(*), intent(in)          :: aname
       character*(*), intent(inout)       :: basename(MAXSERIES+MAXVTABLE+MAXDTABLE)

       integer ndig,baselen,itemp,j
       character*10 atemp

       ifail=0

       call num2char(nsterm,atemp)
       ndig=len_trim(atemp)
       baselen=19-ndig
       itemp=len_trim(aname)
       if(itemp.lt.baselen)baselen=itemp
       basename(iout)=aname(1:baselen)//OBSCHAR
       if(iout.gt.1) then
         do j=1,iout-1
           if(basename(iout).eq.basename(j))then
             write(amessage,10)
10           format('TSPROC cannot generate unique observation names from the ',  &
             'names of the model SERIES, V_TABLES, and E_TABLES involved in the ', &
             'calibration process. Alter the first few letters of the longest ', &
             'of these names, or of those SERIES with the most terms.')
             go to 9800
           end if
         end do
       end if
       return

9800   ifail=1
       return

end subroutine make_basename


subroutine find_end(ifail)

! -- Subroutine FIND_END locates the end of a block when it is out of context.

       use tspvar
       use defn
       use inter
       implicit none

       integer, intent(out)       :: ifail
       integer ierr
       character*15 aline
       character*30 aoption

       ifail=0
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
         if(aoption.eq.'END')return
       end do

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

9800   ifail=1
       return

end subroutine find_end



subroutine nextwdmunit(ifail,nunit,afile)

! -- Function nextunit determines whether a new WDM file needs to be opened
!    or whether an already open one can be used.

       use tspvar
       use defn
       use inter
       implicit none

       integer, intent(out)           :: ifail
       integer, intent(out)           :: nunit
       integer j
       character*(*), intent(in)      :: afile
       character*15 anum
       character*120 bfile

       ifail=0
       bfile=afile
       call casetrans(bfile,'lo')
       if(iwdopn.eq.0) go to 100
       do j=1,iwdopn
         if(bfile.eq.wdmfil(j))then
           nunit=-wdmun(j)
           return
         end if
       end do

100    nunit=nextunit()
       iwdopn=iwdopn+1
       if(iwdopn.gt.MAXWDOPN)then
         call num2char(MAXWDOPN,anum)
         write(amessage,10) trim(anum)
10       format('a maximum of ',a,' WDM files can be open at any one time.')
         ifail=1
         return
       end if
       wdmun(iwdopn)=nunit
       wdmfil(iwdopn)=bfile
       return

end subroutine nextwdmunit



subroutine close_files

! -- Subroutine close_files closes all open files.

! -- Revision history:-
!       June-November, 1995: version 1.

	integer         :: i,ierr

	do i=10,100
	  close(unit=i,iostat=ierr)
	end do
	return

end subroutine close_files
!     Last change:  JD   23 Dec 2000    8:30 pm
subroutine open_output_file(ifail,aprompt,outfile,outunit)

! -- Subroutine open_output_file opens a file for data output.

! -- Subroutine arguments are as follows:-
!       ifail:    returned as non-zero in case of failure
!       aprompt:  user prompt for filename
!       outfile:  name of output file
!       outunit:  unit number of output file

! -- Revision history:-
!       June-November, 1995: version 1.

	use defn
	use inter

	integer, intent(out)            :: ifail
	character (len=*)               :: aprompt,outfile
	integer, intent(out)            :: outunit
	integer                         :: ierr,nbb,ifail1
	logical                         :: lexist,lopened
	character (len=1)               :: aa
        character (len=200)             :: atempf

! -- The user is prompted for the name of the output file.

	imessage=0
	ifail=0
10      write(6,'(a)',advance='no') aprompt(1:len_trim(aprompt)+1)
	read(5,'(a)')outfile
	!outfile = 'tsproc.rec'
	if(outfile.eq.' ') go to 10
	outfile=adjustl(outfile)
	if(index(eschar,outfile(1:2)).ne.0) then
	  escset=1
	  return
	end if
        nbb=len_trim(outfile)
        call getfile(ifail1,outfile,atempf,1,nbb)
        if(ifail1.ne.0) go to 10
        outfile=atempf
	inquire(file=outfile,opened=lopened)
	if(lopened)then
	  write(amessage,30) trim(outfile)
30        format(' File ',a,' is already open  - try again.')
	  call write_message(increment=1)
	  go to 10
	end if
	inquire(file=outfile,exist=lexist)
!       if(lexist) then
!40        write(6,50,advance='no')
!50        format(' File already exists: overwrite it?  [y/n] ')
!         read(5,'(a)') aa
!         call casetrans(aa,'lo')
!         if((aa.eq.'e').or.(aa.eq.'n'))then
!           write(6,*)
!           go to 10
!         end if
!         if(aa.ne.'y') go to 40
!       end if

! -- The file is opened.

	outunit=nextunit()
	open(unit=outunit,file=outfile,status='new',iostat=ierr)
	if(ierr.ne.0) then
	 open(unit=outunit,file=outfile,status='replace',iostat=ierr)
	end if
	if(ierr.ne.0) then
	  if(imessage.gt.5) then
	    ifail=1
	    return
	  end if
	  write(amessage,100) trim(outfile)
100       format(' Unable to open file ',a,' - try again.')
	  call write_message(increment=1)
	  go to 10
	end if

	return

end subroutine open_output_file
!     Last change:  JD   28 Dec 2000    9:08 pm

subroutine addquote(afile,aqfile)

! -- Subroutine ADDQUOTE adds quotes to a filename if it has a space in it.

! -- Arguments are as follows:-
!        afile:       the name of the file
!        aqfile:      the name of the file with quotes added

        character (len=*), intent(in)   :: afile
        character (len=*), intent(out)  :: aqfile
        integer nbb

        if(index(trim(afile),' ').eq.0)then
          aqfile=afile
        else
          aqfile(1:1)='"'
          aqfile(2:)=trim(afile)
          nbb=len_trim(aqfile)+1
          aqfile(nbb:nbb)='"'
        end if

        return
end subroutine addquote


integer function nextunit()

! -- Function nextunit determines the lowest unit number available for
! -- opening.

! -- Revision history:-
!       June-November, 1995: version 1.

	logical::lopen

	do nextunit=10,100
	  inquire(unit=nextunit,opened=lopen)
	  if(.not.lopen) return
	end do
	write(6,10)
10      format(' *** No more unit numbers to open files ***')
	stop

end function nextunit
!     Last change:  JD   31 Jul 2001   11:51 pm

subroutine getfile(ifail,cline,filename,ibeg,iend)

! Subroutine getfile extracts a filename from a string.

! -- Arguments are as follows:-
!       ifail: returned as zero if filename successfully read
!       cline: a character string containing the file name
!       filename: the name of the file read from the string
!       ibeg: character position at which to begin search for filename
!       iend: on input  - character position at which to end search for filename
!             on output - character postion at which filename ends


        integer, intent(out)               :: ifail
        integer, intent(in)                :: ibeg
        integer, intent(inout)             :: iend
        character (len=*), intent(in)      :: cline
        character (len=*), intent(out)     :: filename

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
            filename=cline(i+1:j-1)
          end if
        else
          do j=i+1,iend
            if((cline(j:j).eq.' ').or.(cline(j:j).eq.',').or.(cline(j:j).eq.char(9)))then
              k=j-1
              go to 100
            end if
          end do
          k=iend
100       filename=cline(i:k)
          if(cline(k:k).eq.'"')then
            ifail=1
            return
          else if(cline(k:k).eq.'''')then
            ifail=1
            return
          end if

          iend=k
        end if
        filename=adjustl(filename)
        return

end subroutine getfile


subroutine write_message(increment,iunit,error,leadspace,endspace)

! -- Subroutine write_message formats and writes a message.

! -- Arguments are as follows:-
!       increment:  the increment to the message counter
!       iunit:      the unit number to which the message is written
!       error:      if "yes" precede message with "Error"
!       leadspace   if "yes" precede message with blank line
!       endspace    if "yes" follow message by blank line

! -- Revision history:-
!       June-November, 1995: version 1.

	use defn
	use inter

	integer, intent(in), optional           ::increment,iunit
	integer                                 ::jend,i,nblc,junit,leadblank
	integer                                 ::itake,j
	character (len=*), intent(in), optional ::error,leadspace,endspace
	character (len=20) ablank

	ablank=' '
	itake=0
	j=0
	if(present(increment)) imessage=imessage+increment
	if(present(iunit))then
	  junit=iunit
	else
	  junit=6
	end if
	if(present(leadspace))then
	  if(leadspace.eq.'yes') write(junit,*)
	endif
	if(present(error))then
	  if(index(error,'yes').ne.0)then
	    nblc=len_trim(amessage)
	    amessage=adjustr(amessage(1:nblc+8))
	    if(nblc+8.lt.len(amessage)) amessage(nblc+9:)=' '
	    amessage(1:8)=' Error: '
	  end if
	end if

	do i=1,20
	  if(amessage(i:i).ne.' ')exit
20      end do
	leadblank=i-1
	nblc=len_trim(amessage)
5       jend=j+78-itake
	if(jend.ge.nblc) go to 100
	do i=jend,j+1,-1
	if(amessage(i:i).eq.' ') then
	  if(itake.eq.0) then
	     write(junit,'(a)',err=200) amessage(j+1:i)
	     itake=2+leadblank
	  else
	     write(junit,'(a)',err=200) ablank(1:leadblank+2)//amessage(j+1:i)
	  end if
	  j=i
	  go to 5
	end if
	end do
	if(itake.eq.0)then
	  write(junit,'(a)',err=200) amessage(j+1:jend)
	  itake=2+leadblank
	else
	  write(junit,'(a)',err=200) ablank(1:leadblank+2)//amessage(j+1:jend)
	end if
	j=jend
	go to 5
100     jend=nblc
	if(itake.eq.0)then
	write(junit,'(a)',err=200) amessage(j+1:jend)
	  else
	write(junit,'(a)',err=200) ablank(1:leadblank+2)//amessage(j+1:jend)
	  end if
	if(present(endspace))then
	  if(endspace.eq.'yes') write(junit,*)
	end if
	return

200     call exit(100)

end subroutine write_message
subroutine casetrans(string,hi_or_lo)

! -- Subroutine casetrans converts a string to upper or lower case.

! -- Arguments are as follows:-
!      string:	  contains the string whose case must be changed
!      hi_or_lo:  must be either 'lo' or 'hi' to indicate
!                 change of case direction.

! -- Revision history:-
!       June-November, 1995: version 1.

	use inter

	character (len=*), intent(inout)        :: string
	character (len=*), intent(in)           :: hi_or_lo
	character                               :: alo, ahi
	integer                                 :: inc,i

	if(hi_or_lo.eq.'lo') then
	  alo='A'; ahi='Z'; inc=iachar('a')-iachar('A')
	else if(hi_or_lo.eq.'hi') then
	  alo='a'; ahi='z'; inc=iachar('A')-iachar('a')
	else
	  call sub_error('CASETRANS')
	endif

	do i=1,len_trim(string)
	  if((string(i:i).ge.alo).and.(string(i:i).le.ahi)) &
	  string(i:i)=achar(iachar(string(i:i))+inc)
	end do

	return

end subroutine casetrans
!*****************************************************************************
! subprograms for reading and parsing data (mainly from files) ------->
!*****************************************************************************

subroutine linesplit(ifail,num)

! -- subroutine linesplit splits a line into whitespace-delimited words

! -- Arguments are as follows:-
!       ifail:   returned as -1 if line is blank
!                returned as  1 if less than num segments
!       num:     number of words to be extracted

!    Revision history:-
!       June-November, 1995: version 1.

	use defn
	use inter

	integer, intent(out)            :: ifail
	integer, intent(in)             :: num
	integer                         :: nblc,j,i,nw
	character (len=3)               :: aspace

	ifail=0; nw=0; j=0
	aspace=' ,'//achar(9)   
	if(num.gt.NUM_WORD_DIM) call sub_error('LINESPLIT')
	nblc=len_trim(cline)
	if(nblc.eq.0) then
	  ifail=-1
	  return
	end if

5       if(nw.eq.num) return
	do i=j+1,nblc
	  if(index(aspace,cline(i:i)).eq.0) go to 20
	end do
	ifail=1
	return
20      nw=nw+1
	left_word(nw)=i
	do i=left_word(nw)+1,nblc
	  if(index(aspace,cline(i:i)).ne.0) go to 40
	end do
	right_word(nw)=nblc
	if(nw.lt.num) ifail=1
	return
40      right_word(nw)=i-1
	j=right_word(nw)
	go to 5

end subroutine linesplit


integer function char2int(ifail,num)

! -- Function char2int extracts an integer from a word demarcated by subroutine
!    linesplit.

! -- Arguments are as follows:-
!       ifail:    returned as zero unless an error condition arises
!       num:      the number of the word previously extracted by linesplit
!       returns   value of integer read from word

! -- Revision history:-
!       June-November, 1995: version 1.

	use defn

	integer, intent(in)             :: num
	integer, intent(out)            :: ifail
	character (len=8)               :: afmt

	if(num.gt.NUM_WORD_DIM) call sub_error('CHAR2INT')
	if((right_word(num).lt.left_word(num)).or. &
	  (left_word(num).le.0)) call sub_error('CHAR2INT')

	ifail=0
	afmt='(i   )'
	write(afmt(3:5),'(i3)') right_word(num)-left_word(num)+1
	read(cline(left_word(num):right_word(num)),afmt,err=100) char2int
	return

100     ifail=1
	return

end function char2int


real function char2real(ifail,num)

! -- Function char2real extracts a real number from a word demarcated by
!    subroutine linesplit.

! -- Arguments are as follows:-
!       ifail:    returned as zero unless an error condition arises
!       num:      the number of the word previously extracted by linesplit
!       returns   value of real number read from word

! -- Revision history:-
!       June-November, 1995: version 1.

	use defn

	integer, intent(in)             :: num
	integer, intent(out)            :: ifail
	integer                         :: ierr
	character (len=10)              :: afmt

	if(num.gt.NUM_WORD_DIM) call sub_error('CHAR2REAL')
	if((right_word(num).lt.left_word(num)).or. &
	  (left_word(num).le.0)) call sub_error('CHAR2REAL')

	ifail=0
	afmt='(f   .0)'
	write(afmt(3:5),'(i3)') right_word(num)-left_word(num)+1
	read(cline(left_word(num):right_word(num)),afmt, iostat=ierr) char2real
	if(ierr.ne.0) go to 110
	return

110     ifail=1
	return

end function char2real


double precision function char2double(ifail,num)

! -- Function char2double extracts a double precision number from a word
!    demarcated by subroutine linesplit.

! -- Arguments are as follows:-
!       ifail:    returned as zero unless an error condition arises
!       num:      the number of the word previously extracted by linesplit
!       returns   value of double precision number read from word

! -- Revision history:-
!       June-November, 1995: version 1.

	use defn

	integer, intent(in)             :: num
	integer, intent(out)            :: ifail
	integer                         :: ierr
	character (len=10)              :: afmt

	if(num.gt.NUM_WORD_DIM) call sub_error('CHAR2DOUBLE')
	if((right_word(num).lt.left_word(num)).or. &
	  (left_word(num).le.0)) call sub_error('CHAR2DOUBLE')

	ifail=0
	afmt='(f   .0)'
	write(afmt(3:5),'(i3)') right_word(num)-left_word(num)+1
	read(cline(left_word(num):right_word(num)),afmt, iostat=ierr) char2double
	if(ierr.ne.0) go to 110
	return

110     ifail=1
	return

end function char2double
!     Last change:  JD   29 Jun 2001    4:34 pm
subroutine read_rest_of_sample_line(ifail,cols,ndays,nsecs,value,iline,sampfile)

! -- Subroutine read_rest_of_sample_line reads the date, time, value and
!    optional fifth column from a line of a site sample file.

! -- Arguments are as follows:-
!       ifail:     returned as zero unless an error condition is encountered
!       cols:      number of data columns in the line
!       ndays:     number of days from 1/1/1970 until sample date
!       nsecs:     number of seconds from midnight until sample time
!       value:     sample value
!       iline:     current line number of site sample file
!       sampfile:  name of site sample file

! -- Revision history:-
!       June-November, 1995: version 1.

	use defn
	use inter

	integer, intent(out)            :: ifail
	integer, intent(in)             :: cols
	integer, intent(out)            :: ndays,nsecs
	double precision, intent(out)   :: value
	integer, intent(in)             :: iline
	character (len=*), intent(in)   :: sampfile
	integer                         :: dd,mm,yy,hhh,mmm,sss
	character (len=15)              :: aline
	character (len=2)               :: aa

	ifail=0
	call char2date(ifail,cline(left_word(2):right_word(2)),dd,mm,yy)
	if(ifail.ne.0) then
	  call num2char(iline,aline)
	  write(amessage,150) trim(aline),trim(sampfile)
150       format('illegal date at line ',a,' of site sample file ',a)
	  call write_message(error='yes',leadspace='yes')
	  go to 9800
	end if
	ndays=numdays(1,1,1970,dd,mm,yy)

	call char2time(ifail,cline(left_word(3):right_word(3)),hhh,mmm,sss)
	if(ifail.ne.0) then
	  call num2char(iline,aline)
	  write(amessage,160) trim(aline),trim(sampfile)
160       format('illegal time at line ',a,' of site sample file ',a)
	  call write_message(error='yes',leadspace='yes')
	  go to 9800
	end if
	nsecs=numsecs(0,0,0,hhh,mmm,sss)

	value=char2double(ifail,4)
	if(ifail.ne.0)then
	  call num2char(iline,aline)
	  write(amessage,180) trim(aline),trim(sampfile)
180       format('cannot read sample value at line ',a,' of site sample file ',a)
	  call write_message(error='yes',leadspace='yes')
	  go to 9800
	end if
	if(value.lt.-1.0e37) then
	  call num2char(iline,aline)
	  write(amessage,190) trim(aline),trim(sampfile)
190       format('illegal sample value at line ',a,' of site sample file ',a, &
	  '; lower limit is -1.0E37.')
	  call write_message(error='yes',leadspace='yes')
	  go to 9800
	end if
	if(cols.eq.5)then
	  aa=cline(left_word(5):right_word(5))
	  call casetrans(aa,'lo')
	  if(aa.eq.'x ') then
	    value=-1.1e38
	  else
	    call num2char(iline,aline)
	    write(amessage,210) trim(aline),trim(sampfile)
210         format('illegal optional fifth item on line ',a,' of site sample ',&
	    'file ',a,'; item must be "x" if present.')
	    call write_message(error='yes',leadspace='yes')
	    go to 9800
	  end if
	end if
	return

9800    ifail=1
	return

end subroutine read_rest_of_sample_line
subroutine newdate(ndays,day1,mon1,year1,day2,mon2,year2)

! -- Subroutine NEWDATE evaluates the date after NDAYS days have elapsed from
!    a provided date. NDAYS may be negative.

! -- Arguments are as follows:-
!       ndays:            elapsed number of days
!       day1,mon1,year1:  days, month and year of first date
!       day2,mon2,year2:  days, month and year of second date

! -- Revision history:-
!       June-November, 1995: version 1.

	use inter
	implicit none

	integer, intent(in)     :: ndays,day1,mon1,year1
	integer, intent(out)    :: day2,mon2,year2

	integer  :: yearref,newdays,idays,iyear,jdays,i
	integer, dimension(12) :: monthdays

	data monthdays /31,28,31,30,31,30,31,31,30,31,30,31/

! -- First a reference date is chosen. This is the beginning of the first
! -- year. Alternatively the reference date is the beginning of a year prior
! -- to the likely calculated date if NDAYS is negative.

	if(ndays.ge.0) then
	  yearref=year1
	else
	  yearref=year1-abs(ndays)/365-1
	end if
	newdays=numdays(31,12,yearref-1,day1,mon1,year1)
	newdays=ndays+newdays
	if(newdays.lt.0) call sub_error('NEWDATE')

! -- Next days are counted, starting at the new reference date.

	idays=0
	iyear=yearref
	do
	  jdays=idays+365
	  if(leap(iyear)) jdays=jdays+1
	  if(jdays.ge.newdays) go to 20
	  iyear=iyear+1
	  idays=jdays
	end do
	call sub_error('NEWDATE')
20      year2=iyear

	do i=1,12
	  jdays=idays+monthdays(i)
	  if((i.eq.2).and.(leap(year2))) jdays=jdays+1
	  if(jdays.ge.newdays) go to 40
	  idays=jdays
	end do
	call sub_error('NEWDATE')
40      mon2=i
	day2=newdays-idays
!	if((day2.le.0).or.(mon2.le.0).or.(year2.le.0)) call sub_error('NEWDATE')
	if((day2.le.0).or.(mon2.le.0)) call sub_error('NEWDATE')
	return

end subroutine newdate  
integer function numsecs(h1,m1,s1,h2,m2,s2)

! -- Subroutine NUMSECS calculates the number of seconds between two times.

! -- Arguments are as follows:-
!       h1,m1,s1:   hours, minutes seconds of first time
!       h2,m2,y2:   hours, minutes seconds of second time

! -- Revision history:-
!       June-November 1995: version 1.

	integer, intent(in)             :: h1,m1,s1,h2,m2,s2

	numsecs=(h2-h1)*3600+(m2-m1)*60+s2-s1

end function numsecs
integer function numdays(DR,MR,YR,D,M,Y)

! -- Function numdays calculates the number of days between dates
!    D-M-Y and DR-MR-YR. If the former preceeds the latter the answer is
!    negative.

! -- Arguments are as follows:-
!       dr,mr,yr:     days, months and years of first date
!       d,m,y:        days, months and years of second date
!       numdays returns the number of elapsed days

! -- Revision history:-
!       22 July 1994:  version 1
!       13 September 1995:  modified for Groundwater Data Utilities


	integer, intent(in)     :: dr,mr,yr,d,m,y

	INTEGER FLAG,I,J,DA(12),YE,ME,DE,YL,ML,DL
	logical leap

	DATA DA /31,28,31,30,31,30,31,31,30,31,30,31/

! --    THE SMALLER OF THE TWO DATES IS NOW CHOSEN TO DO THE COUNTING FROM.

	IF(Y.LT.YR)GO TO 10
	IF((Y.EQ.YR).AND.(M.LT.MR)) GO TO 10
	IF((Y.EQ.YR).AND.(M.EQ.MR).AND.(D.LT.DR)) GO TO 10
	FLAG=0
	YE=YR
	ME=MR
	DE=DR
	YL=Y
	ML=M
	DL=D
	GO TO 20
10      FLAG=1
	YE=Y
	ME=M
	DE=D
	YL=YR
	ML=MR
	DL=DR

! --    IN THE ABOVE THE POSTSCRIPT "E" STANDS FOR EARLIER DATE, WHILE
!       "L" STANDS FOR THE LATER DATE.

20      numdays=0
	IF((ME.EQ.ML).AND.(YL.EQ.YE))THEN
	numdays=DL-DE
	IF(FLAG.EQ.1) numdays=-numdays
	RETURN
	END IF

	DO 30 J=ME,12
	IF((ML.EQ.J).AND.(YE.EQ.YL))GOTO 40
	numdays=numdays+DA(J)
	IF((J.EQ.2).AND.(leap(ye)))numdays=numdays+1
30      CONTINUE
	GO TO 50
40      numdays=numdays+DL-DE
	IF(FLAG.EQ.1)numdays=-numdays
	RETURN

50      DO 60 I=YE+1,YL
	DO 70 J=1,12
	IF((YL.EQ.I).AND.(ML.EQ.J))GO TO 80
	numdays=numdays+DA(J)
	IF((J.EQ.2).AND.(leap(i))) numdays=numdays+1
70      CONTINUE
60      CONTINUE
	call sub_error('NUMDAYS')
	RETURN

80      numdays=numdays+DL-DE
	IF(FLAG.EQ.1) numdays=-numdays

	RETURN
end function numdays
logical function leap(year)

! -- Function LEAP returns .true. if a year is a leap year.

! -- Revision history:-
!       June-November, 1995: version 1.

	integer, intent(in)     :: year

        leap = ( mod(year,4).eq.0 .and. mod(year,100).ne.0 ) .or. &
               ( mod(year,400).eq.0 .and. year.ne.0 )

	return
end function leap
!     Last change:  JD   24 Aug 2001    4:15 pm
subroutine char2time(ifail,atime,hh,mm,ss,ignore_24)

! -- Subroutine CHAR2TIME extracts the time from a string.

! -- Arguments are as follows:-
!       ifail:     indicates failure if returned as non-zero
!       atime:     a string containing the time in ASCII format
!       hh,mm,ss   hours, minutes and seconds extracted from the atime string.

! -- Revision history:-
!       June-November, 1995: version 1.

	use defn
	use inter

	integer, intent(out)            :: ifail
	character (len=*), intent(in)   :: atime
	integer, intent(out)            :: hh,mm,ss
        integer, optional,intent(in)    :: ignore_24
	integer                         :: lentime,i,j,ig_24
	character (len=2)               :: asep
	character (len=20)              :: btime

	ifail=0
        if(.not.present(ignore_24)) then
          ig_24=0
        else
          ig_24=ignore_24
        end if

	asep=':.'
	if(atime.eq.' ') go to 9000
	btime=adjustl(atime)
	lentime=len_trim(btime)
	if(lentime.lt.5) go to 9000

	do i=1,lentime
	  if(index(asep,btime(i:i)).ne.0) go to 20
	end do
	go to 9000

! -- The first integer is extracted from the string. This represents hours.

20      if(i.eq.1) go to 9000
	call char2num(ifail,btime(1:i-1),hh)
	if(ifail.ne.0) go to 9000
        if(ig_24.eq.0)then
	  if((hh.lt.0).or.(hh.gt.23)) go to 9000
        else
          if((hh.lt.0).or.(hh.gt.24)) go to 9000
        end if

	i=i+1
	if(lentime-i.lt.2) go to 9000
	do j=i,lentime
	  if(index(asep,btime(j:j)).ne.0) go to 40
	end do
	go to 9000

! -- The second integer (representing minutes) is extracted from the string.

40      if(j.eq.i) go to 9000
	call char2num(ifail,btime(i:j-1),mm)
	if(ifail.ne.0) go to 9000
	if((mm.lt.0).or.(mm.gt.59)) go to 9000

! -- The third integer (representing seconds) is extracted from the string.

	j=j+1
	if(lentime-j.lt.0) go to 9000
	call char2num(ifail,btime(j:lentime),ss)
	if(ifail.ne.0) go to 9000
	if((ss.lt.0).or.(ss.gt.59)) go to 9000

        if(ig_24.ne.0)then
          if(hh.eq.24)then
            if((mm.ne.0).or.(ss.ne.0)) go to 9000
          end if
        end if
	ifail=0
	return

9000    ifail=1
	return

end subroutine char2time
subroutine char2date(ifail,adate,dd,mm,yy)

! -- Subroutine CHAR2DATE extracts the date from a string.


! -- Arguments are as follows:-
!      ifail:      returns a non-zero value if an error condition is encountered
!      adate:      the string containing the date
!      dd,mm,yy    the day, month and year read from the date string

! --  Revision history:-
!       June-November, 1995: version 1.

	use defn
	use inter

	integer, intent(out)    :: ifail
	character (len=*), intent(in)   :: adate
	integer, intent(out) :: dd,mm,yy
	integer :: lendate,i,j
	character (len=2)       :: asep
	character (len=20)      :: bdate

	ifail=0
	asep=':/'
	if(adate.eq.' ') go to 9000
	bdate=adjustl(adate)
	lendate=len_trim(bdate)
	if(lendate.lt.8) go to 9000

	do i=1,lendate
	  if(index(asep,bdate(i:i)).ne.0) go to 20
	end do
	go to 9000

! -- The first integer is extracted from the date string. This is either days
!    or months depending on the contents of file settings.fig.

20      if(i.eq.1) go to 9000
	if(datespec.ne.1) then
	   call char2num(ifail,bdate(1:i-1),mm)
	else
	   call char2num(ifail,bdate(1:i-1),dd)
	end if
	if(ifail.ne.0) go to 9000

	i=i+1
	if(lendate-i.lt.5) go to 9000
	do j=i,lendate
	  if(index(asep,bdate(j:j)).ne.0) go to 40
	end do
	go to 9000

! -- The second integer is extracted from the date string. This is either months
!    or days depending on the contents of file settings.fig.

40      if(j.eq.i) go to 9000
	if(datespec.ne.1) then
	  call char2num(ifail,bdate(i:j-1),dd)
	else
	  call char2num(ifail,bdate(i:j-1),mm)
	end if
	if(ifail.ne.0) go to 9000
	if((dd.le.0).or.(dd.gt.31)) go to 9000
	if((mm.le.0).or.(mm.gt.12)) go to 9000
	if(dd.eq.31)then
	  if((mm.eq.2).or.(mm.eq.4).or.(mm.eq.6).or.(mm.eq.9).or.&
	  (mm.eq.11)) go to 9000
	end if
	if((mm.eq.2).and.(dd.eq.30)) go to 9000

! -- The third integer is extracted from the date string. This is years.

	j=j+1
	if(lendate-j.ne.3) go to 9000
	call char2num(ifail,bdate(j:lendate),yy)
	if(ifail.ne.0) go to 9000
	if(.not.leap(yy))then
	  if((mm.eq.2).and.(dd.eq.29)) go to 9000
	end if
	ifail=0
	return

9000    ifail=1
	return

end subroutine char2date
subroutine get_wdm_series(ifail)

       use tspvar
       use defn
       use inter
       implicit none
       integer, intent(out) :: ifail

       ifail=1
       write(amessage,10)
10     format('subroutine GET_WDM_SERIES is not avalable in this version ',  &
       'of TSPROC.') 

9800   call write_message(leadspace='yes',error='yes')
       call write_message(iunit=recunit,leadspace='yes')

       return

end subroutine get_wdm_series

subroutine sub_error(subname)

! -- Subroutine sub_error names the subroutine causing a run-time error.

! -- Arguments are as follows:-
!       subname:  name of offending subroutine

! -- Revision history:-
!       June-November, 1995: version 1.

	character (len=*)               ::subname

	write(6,10) trim(subname)
10      format(/,' *** PROGRAMMING ERROR CALLING SUBROUTINE ',a,' ***')
	stop

end subroutine sub_error
!*****************************************************************************
! subroutines comprising the generic subroutine NUM2CHAR ------->
!*****************************************************************************

! -- Subroutine num2char writes the character equivalent of a number.

! -- Arguments are as follows:-
!       value:   the number to be expressed in character form
!       string:  the number expressed in character form
!       nchar:   the maximum number of characters in which to express number

! -- Revision history:-
!       June-November, 1995: version 1.

subroutine i2a(value,string,nchar)

	use inter

	integer, intent(in)             :: value
	character (len=*), intent(out)  :: string
	integer, intent(in), optional   :: nchar
	character (len=12)              :: afmt
	integer                         :: llen

	string=' '
	afmt='(i    )'
	llen=min(30,len(string))
	if(present(nchar)) llen=min(llen,nchar)
	write(afmt(3:6),'(i4)') llen
	write(string(1:llen),afmt,err=100) value
	string=adjustl(string)
	if(string(1:1).eq.'*') go to 100
	return

100     string(1:llen)=repeat('#',llen)
	return

end subroutine i2a


subroutine d2a(value,string,nchar)

	use inter

	double precision, intent(in)    :: value
	character (len=*), intent(out)  :: string
	integer, intent(in), optional   :: nchar
	integer                         :: llen, ifail
	double precision                :: value_check
	character (len=32)              :: word

	string=' '
	llen=min(29,len(string))
	if(present(nchar)) llen=min(llen,nchar)
	call wrtsig(ifail,value,word,llen,1,value_check,0)
	if(ifail.lt.0) then
	  call sub_error('D2A')
	else if(ifail.gt.0) then
	  string(1:llen)=repeat('#',llen)
	else
	  string=adjustl(word)
	end if
	return

end subroutine d2a


subroutine r2a(value,string,nchar)

	use inter

	real,intent(in)                 :: value
	character (len=*), intent(out)  :: string
	integer, intent(in), optional   :: nchar
	integer                         :: llen,ifail
	double precision                :: dvalue,dvalue_check
	character (len=32)              :: word

	string=' '
	llen=min(29,len(string))
	if(present(nchar)) llen=min(llen,nchar)
	dvalue=value
	call wrtsig(ifail,dvalue,word,llen,0,dvalue_check,0)
	if(ifail.lt.0) then
	  call sub_error('R2A')
	else if(ifail.gt.0) then
	  string(1:llen)=repeat('#',llen)
	else
	  string=adjustl(word)
	end if
	return

end subroutine r2a

	
	SUBROUTINE WRTSIG(IFAIL,VAL,WORD,NW,PRECIS,TVAL,NOPNT)
! --
! -- SUBROUTINE WRTSIG WRITES A NUMBER INTO A CONFINED SPACE WITH MAXIMUM
! -- PRECISION
! --

! -- Revision history:-
!       July, 1993: version 1.
!       August 1994: modified for unix version (#ifdef's added)
!       August, 1995: #ifdefs commented out for inclusion in Groundwater
!                     Data Utilities

!       failure criteria:
!           ifail= 1 ...... number too large or small for single precision type
!           ifail= 2 ...... number too large or small for double precision type
!           ifail= 3 ...... field width too small to represent number
!           ifail=-1 ...... internal error type 1
!           ifail=-2 ...... internal error type 2
!           ifail=-3 ...... internal error type 3

	INTEGER PRECIS,LW,POS,INC,D,P,W,J,JJ,K,JEXP,N,JFAIL,NW, &
	EPOS,PP,NOPNT,KEXP,IFLAG,LEXP
	INTEGER IFAIL
	DOUBLE PRECISION VAL,TVAL
	CHARACTER*29 TWORD,TTWORD,FMT*14
	CHARACTER*(*) WORD

	LEXP=0
	IFLAG=0
	WORD=' '
	POS=1
	IF(VAL.LT.0.0D0)POS=0
!#ifdef USE_D_FORMAT
!        WRITE(TWORD,'(1PD23.15D3)') VAL
!#else
	WRITE(TWORD,'(1PE23.15E3)') VAL
!#endif
	READ(TWORD(20:23),'(I4)') JEXP
	EPOS=1
	IF(JEXP.LT.0)EPOS=0

	JFAIL=0
	IFAIL=0
	IF(PRECIS.EQ.0)THEN
	  LW=MIN(15,NW)
	ELSE
	  LW=MIN(23,NW)
	END IF

	N=0
	IF(NOPNT.EQ.1)N=N+1
	IF(POS.EQ.1)N=N+1
	IF(PRECIS.EQ.0)THEN
	  IF(ABS(JEXP).GT.38)THEN
	    IFAIL=1
	    RETURN
	  END IF
	  IF(POS.EQ.1) THEN
	    IF(LW.GE.13) THEN
	      WRITE(WORD,'(1PE13.7)',ERR=80) VAL
	      GO TO 200
	    END IF
	  ELSE
	    IF(LW.GE.14)THEN
	      WRITE(WORD,'(1PE14.7)',ERR=80) VAL
	      GO TO 200
	    END IF
	  END IF
	  IF(LW.GE.14-N) THEN
	    LW=14-N
	    GO TO 80
	  END IF
	ELSE
	  IF(ABS(JEXP).GT.275)THEN
	    IFAIL=2
	    RETURN
	  END IF
	  IF(POS.EQ.1) THEN
	    IF(LW.GE.22) THEN
!#ifdef USE_D_FORMAT
!              WRITE(WORD,'(1PD22.15D3)',ERR=80) VAL
!#else
	      WRITE(WORD,'(1PE22.15E3)',ERR=80) VAL
!#endif
	      GO TO 200
	    END IF
	  ELSE
	    IF(LW.GE.23) THEN
!#ifdef USE_D_FORMAT
!              WRITE(WORD,'(1PD23.15D3)',ERR=80) VAL
!#else
	      WRITE(WORD,'(1PE23.15E3)',ERR=80) VAL
!#endif
	      GO TO 200
	    END IF
	  END IF
	  IF(LW.GE.23-N)THEN
	    LW=23-N
	    GO TO 80
	  END IF
	END IF

	IF(NOPNT.EQ.1)THEN
	  IF((JEXP.EQ.LW-2+POS).OR.(JEXP.EQ.LW-3+POS))THEN
	    WRITE(FMT,15)LW+1
15          FORMAT('(F',I2,'.0)')
	    WRITE(WORD,FMT,ERR=19) VAL
	    IF(INDEX(WORD,'*').NE.0) GO TO 19
	    IF(WORD(1:1).EQ.' ') GO TO 19
	    WORD(LW+1:LW+1)=' '
	    GO TO 200
	  END IF
	END IF
19      D=MIN(LW-2+POS,LW-JEXP-3+POS)
20      IF(D.LT.0) GO TO 80
	WRITE(FMT,30) LW,D
30      FORMAT('(F',I2,'.',I2,')')
	WRITE(WORD,FMT,ERR=80) VAL
	IF(INDEX(WORD,'*').NE.0) THEN
	  D=D-1
	  GO TO 20
	END IF
	K=INDEX(WORD,'.')
	IF(K.EQ.0)THEN
	  IFAIL=-1
	  RETURN
	END IF
	IF((K.EQ.1).OR.((POS.EQ.0).AND.(K.EQ.2)))THEN
	  DO 70 J=1,3
	  IF(K+J.GT.LW) GO TO 75
	  IF(WORD(K+J:K+J).NE.'0') GO TO 200
70        CONTINUE
	  GO TO 80
75        IFAIL=3
	  RETURN
	END IF
	GO TO 200

80      WORD=' '
	IF(NOPNT.EQ.0)THEN
	  D=LW-7
	  IF(POS.EQ.1) D=D+1
	  IF(EPOS.EQ.1) D=D+1
	  IF(ABS(JEXP).LT.100) D=D+1
	  IF(ABS(JEXP).LT.10) D=D+1
	  IF((JEXP.GE.100).AND.(JEXP-(D-1).LT.100))THEN
	    P=1+(JEXP-99)
	    D=D+1
	    LEXP=99
	  ELSE IF((JEXP.GE.10).AND.(JEXP-(D-1).LT.10))THEN
	    P=1+(JEXP-9)
	    D=D+1
	    LEXP=9
	  ELSE IF((JEXP.EQ.-10).OR.(JEXP.EQ.-100)) THEN
	    IFLAG=1
	    D=D+1
	  ELSE
	    P=1
	  END IF
	  INC=0
85        IF(D.LE.0) GO TO 300
	  IF(IFLAG.EQ.0)THEN
	    WRITE(FMT,100,ERR=300) P,D+7,D-1
	  ELSE
	    WRITE(FMT,100,ERR=300) 0,D+8,D
	  END IF
	  WRITE(TWORD,FMT) VAL
	  IF(IFLAG.EQ.1) GO TO 87
	  READ(TWORD(D+4:D+7),'(I4)',ERR=500) KEXP
	  IF(((KEXP.EQ.10).AND.((JEXP.EQ.9).OR.(LEXP.EQ.9))).OR. &
	  ((KEXP.EQ.100).AND.((JEXP.EQ.99).OR.LEXP.EQ.99))) THEN
	    IF(INC.EQ.0)THEN
	      IF(LEXP.EQ.0)THEN
		IF(D-1.EQ.0) THEN
		  D=D-1
		ELSE
		  P=P+1
		END IF
	      ELSE IF(LEXP.EQ.9)THEN
		IF(JEXP-(D-2).LT.10) THEN
		  P=P+1
		ELSE
		  D=D-1
		END IF
	      ELSE IF(LEXP.EQ.99)THEN
		IF(JEXP-(D-2).LT.100)THEN
		  P=P+1
		ELSE
		  D=D-1
		END IF
	      END IF
	      INC=INC+1
	      GO TO 85
	    END IF
	  END IF
!#ifdef USE_D_FORMAT
!87        J=INDEX(TWORD,'D')
!#else
87        J=INDEX(TWORD,'E')
!#endif
	  GO TO 151
	END IF
	INC=0
	P=LW-2
	PP=JEXP-(P-1)
	IF(PP.GE.10)THEN
	  P=P-1
	  IF(PP.GE.100)P=P-1
	ELSE IF(PP.LT.0)THEN
	  P=P-1
	  IF(PP.LE.-10)THEN
	    P=P-1
	    IF(PP.LE.-100)P=P-1
	  END IF
	END IF
	IF(POS.EQ.0)P=P-1
90      CONTINUE
	D=P-1
	W=D+8
	WRITE(FMT,100) P,W,D
	IF(D.LT.0)THEN
	  IF(JFAIL.EQ.1) GO TO 300
	  JFAIL=1
	  P=P+1
	  GO TO 90
	END IF
!#ifdef USE_D_FORMAT
!100     FORMAT('(',I2,'pD',I2,'.',I2,'D3)')
!#else
100     FORMAT('(',I2,'pE',I2,'.',I2,'E3)')
!#endif
	WRITE(TWORD,FMT) VAL
!#ifdef USE_D_FORMAT
!        J=INDEX(TWORD,'D')
!#else
	J=INDEX(TWORD,'E')
!#endif
	IF(TWORD(J-1:J-1).NE.'.')THEN
	  IFAIL=-1
	  RETURN
	END IF
	N=1
	IF(TWORD(J+1:J+1).EQ.'-') N=N+1
	IF(TWORD(J+2:J+2).NE.'0') THEN
	  N=N+2
	  GO TO 120
	END IF
	IF(TWORD(J+3:J+3).NE.'0') N=N+1
120     N=N+1
	IF(J+N-2-POS.LT.LW)THEN
	  IF(INC.EQ.-1) GO TO 150
	  TTWORD=TWORD
	  P=P+1
	  INC=1
	  GO TO 90
	ELSE IF(J+N-2-POS.EQ.LW) THEN
	  GO TO 150
	ELSE
	  IF(INC.EQ.1)THEN
	    TWORD=TTWORD
	    GO TO 150
	  END IF
	  IF(JFAIL.EQ.1) GO TO 300
	  P=P-1
	  INC=-1
	  GO TO 90
	END IF

150     J=INDEX(TWORD,'.')
151     IF(POS.EQ.0)THEN
	  K=1
	ELSE
	 K=2
	END IF
	WORD(1:J-K)=TWORD(K:J-1)
	JJ=J
	J=J-K+1
	IF(PRECIS.EQ.0)THEN
	  WORD(J:J)='E'
	ELSE
	  WORD(J:J)='D'
	END IF
	JJ=JJ+2
	IF(NOPNT.EQ.0) JJ=JJ-1
	IF(TWORD(JJ:JJ).EQ.'-')THEN
	  J=J+1
	  WORD(J:J)='-'
	END IF
	IF(TWORD(JJ+1:JJ+1).NE.'0')THEN
	  J=J+2
	  WORD(J-1:J)=TWORD(JJ+1:JJ+2)
	  GO TO 180
	END IF
	IF(TWORD(JJ+2:JJ+2).NE.'0')THEN
	  J=J+1
	  WORD(J:J)=TWORD(JJ+2:JJ+2)
	END IF
180     J=J+1
	WORD(J:J)=TWORD(JJ+3:JJ+3)
	IF(IFLAG.EQ.1)THEN
	  IF(POS.EQ.1)THEN
	    JJ=1
	  ELSE
	    JJ=2
	  END IF
	  N=len_trim(WORD)
	  DO 190 J=JJ,N-1
190       WORD(J:J)=WORD(J+1:J+1)
	  WORD(N:N)=' '
	END IF

200     IF(len_trim(WORD).GT.LW)THEN
	  IFAIL=-2
	  RETURN
	END IF
	WRITE(FMT,30) LW,0
	READ(WORD,FMT,ERR=400) TVAL
	RETURN
300     IFAIL=3
	RETURN
400     IFAIL=-3
	RETURN
500     IFAIL=-2
	RETURN
	END

!*****************************************************************************
! subroutines comprising the generic subroutine CHAR2NUM ------->
!*****************************************************************************


! -- The subroutines comprising char2num convert a string to either an integer,
!    a real number, or a double precision number.

! -- Arguments are as follows:-
!      ifail:   indicates failure if returned as non-zero
!      string:  a character string containing a number
!      num:     an integer (for a2i), real (for a2r), or double precision (for
!               a2d) number extracted from the string.

! -- Revision history:-
!       June-November, 1995: version 1.


subroutine a2i(ifail,string,num)

	integer, intent(out)            :: ifail
	character (len=*), intent(in)   :: string
	integer, intent(out)            :: num
	character (len=10)              :: afmt

        if(string.eq.' ') go to 10
	ifail=0
	afmt='(i    )'
	write(afmt(3:6),'(i4)')len(string)
	read(string,afmt,err=10) num
	return

10      ifail=1
	return

end subroutine a2i


subroutine a2r(ifail,string,num)

	integer, intent(out)            :: ifail
	character (len=*), intent(in)   :: string
	real, intent(out)               :: num
	character (len=10)              :: afmt

        if(string.eq.' ') go to 10
	ifail=0
	afmt='(f    .0)'
	write(afmt(3:6),'(i4)')len(string)
	read(string,afmt,err=10) num
	return

10      ifail=1
	return

end subroutine a2r


subroutine a2d(ifail,string,num)

	integer, intent(out)            :: ifail
	character (len=*), intent(in)   :: string
	double precision, intent(out)   :: num
	character (len=10)              :: afmt

        if(string.eq.' ') go to 10
	ifail=0
	afmt='(f    .0)'
	write(afmt(3:6),'(i4)')len(string)
	read(string,afmt,err=10) num
	return

10      ifail=1
	return

end subroutine a2d

!     Last change:  JD   31 Jul 2001   10:05 am
logical function isspace(astring)

! -- Subroutine ISSPACE checks whether there is a space within a string.

! -- Arguments are as follows:-
!        astring:     the name of the string to be checked.

        character (len=*), intent(in)   :: astring
        integer nbb

        if(index(trim(astring),' ').eq.0)then
          isspace=.false.
        else
          isspace=.true.
        end if

        return
end function isspace




subroutine get_constants(ifail)

       use tspvar
       use defn
       use inter
       implicit none

       integer, intent(out)   :: ifail

       integer ierr,ixcon,icontext,nn,ss,i,iunit,jline,j
       double precision dvalue       
       character*15 aline       
       character*25 aoption,constname
       character*120 afile
       character*25 acontext(MAXCONTEXT)

       ifail=0
       currentblock='GET_CONSTANTS'

       write(*,10) trim(currentblock)
       write(recunit,10) trim(currentblock)
10     format(/,' Processing ',a,' block....')

       afile=' '     
       acontext(1)=' '
       icontext=0       
       iunit=0
       ixcon=0

! -- The GET_CONSTANTS block is first parsed.

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

! -- If there are any absences , this is now reported.

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


! -- There appear to be no errors in the block, so now it is processed.

       call addquote(afile,astring)
       write(*,179) trim(astring)
       write(recunit,179) trim(astring)
179    format(t5,'Reading constants file ',a,'....')
       
       iunit=nextunit()
       open(unit=iunit,file=afile,status='old',iostat=ierr)
       if(ierr.ne.0)then
         write(amessage,180) trim(astring),trim(currentblock)
180      format('cannot open constants file ',a,' cited in ',a,' block.')
         go to 9800
       end if

! -- The file is read and the name and value of the constants are loaded in               
       jline=0
       do
         jline=jline+1
         read(iunit,'(a)',err=9200,end=500)cline
         call linesplit(ierr,2)
         if(ierr.lt.0) then
           cycle
         else if(ierr.gt.0)then
           call num2char(jline,aline)
           write(amessage,375) trim(aline),trim(astring)
375        format('two entries expected on line ',a,' of constants file ',a)
           go to 9800
         end if
         constname=cline(left_word(1):right_word(1))         
         call casetrans(constname,'lo')         
         
         dvalue = char2double(ierr,2)
         if(ierr.ne.0)then
           call write_message(iunit=recunit,leadspace='yes',error='yes')
           ifail=1
           return
         end if
         !--get the next inactive constant
         do i=1,MAXCONST
           if(.not.const(i)%active) goto 400          
         end do
400      continue
         const(i)%name = trim(constname)
         const(i)%value = dvalue
         const(i)%active = .true.   
       end do
500    continue
       goto 9900




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

9900   if(iunit.ne.0)close(unit=iunit,iostat=ierr)
       return

end subroutine get_constants



 
