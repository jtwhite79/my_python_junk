import urllib

source1="http://my.sfwmd.gov/dbhydroplsql/web_io.report_process?v_period=uspec&v_start_date=19960101&v_end_date=20041231&v_report_type=format6&v_target_code=screen&v_run_mode=onLine&v_js_flag=Y&v_db_request_id=1642302&v_where_clause=&v_dbkey="
source2="&v_os_code=Win&v_interval_count=5"
#source="http://my.sfwmd.gov/dbhydroplsql/web_io.report_process?v_period=uspec&v_start_date=19800716&v_end_date=20090430&v_report_type=format6&v_target_code=screen&v_run_mode=onLine&v_js_flag=Y&v_db_request_id=1642302&v_where_clause=&v_dbkey=15753&v_os_code=Win&v_interval_count=5"

monthdict=({'JAN':'01','FEB':'02','MAR':'03','APR':'04','MAY':'05','JUN':'06',
	          'JUL':'07','AUG':'08','SEP':'09','OCT':'10','NOV':'11','DEC':'12'})

filename="output.smp"
f=open(filename,'w')

dbkeyfile=open('dbkeys.txt')
print 'opened: dbkeys.txt'

for dbkey in dbkeyfile:
	print 'processing dbkey: ',dbkey
	source=source1+str(dbkey[0:5])+source2
	data=urllib.urlopen(source).readlines()
	for x in data:
		record=x.split()
		if len(record) > 3:
			if record[1]==dbkey[0:5]:
				dd,mm,yyyy=record[2].split('-')
				date=monthdict.get(mm) + '/' + str(dd) + '/' + str(yyyy)
				line=record[0] + ' ' + date + ' 12:00:00 ' + record[3] + '\n'
				f.write(line)
dbkeyfile.close()
f.close()
