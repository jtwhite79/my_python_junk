from datetime import datetime
import numpy as np
import pandas
import xlrd

f = open('..\\_nwis\\spec_chl_regress_parameters.dat','r')
f.readline()
m,b = f.readline().strip().split(',')
m = float(m)
b = float(b)
f.close()

chl_seawater = 19400.0

wb = xlrd.open_workbook('SALT_DATA.xls')
sheet_names = wb.sheet_names()
dfs = []
for sheet in sheet_names:
    print sheet
    sh = wb.sheet_by_name(sheet)
    #--get the elevation of the top of the casing  - column 1, row 7
    case_elev = float(sh.cell(6,0).value.split()[0])
    #--get the dates of measurement row 9, columns except 1
    date_row = sh.row(8)
    dates = []
    for i,xldate in enumerate(date_row[1:]):       
        dt_tup = xlrd.xldate_as_tuple(xldate.value,wb.datemode)
        dt = datetime(*dt_tup)
        dates.append(dt)

    #--get the depths and convert to elev column 1, starting at row 11
    depth_col = sh.col(0)
    elevs = []
    for d in depth_col[10:]:
        if d.ctype != 2:
            break
        elevs.append(case_elev-d.value)

    #--now load the data - use a dict for pandas
    #--will be transposed relative to original spreadsheet
    data = {}    
    #--starting at row 11
    for i,e in enumerate(elevs):
        dlist = []
        dcol = sh.row(10+i)
        for j,dt in enumerate(dates):
            if dcol[j].ctype == 2:
                dlist.append(dcol[j].value)
            else:
                dlist.append(np.NaN)
        data[e] = dlist
    #--make a dataframe and save
    df = pandas.DataFrame(data=data,index=dates)
    df.to_csv('dataframes\\'+sheet+'.csv',index_label='datetime')
    df = (df * m) + b
    df[df < 0.0] = 0.0
    df.to_csv('dataframes\\'+sheet+'_chl.csv',index_label='datetime')
    df /= chl_seawater
    df.to_csv('dataframes\\'+sheet+'_relconc.csv',index_label='datetime')




