import xlrd

#--need to save as an xls file
fname = 'PRLNDS_TAET.xls'
#--create an xlrd workbook instance
wb = xlrd.open_workbook(fname)
#--get all of the sheet names in this workbook
sh_names = wb.sheet_names()

#--loop over each sheet name
for sh_name in sh_names:
    #--get the sheet instance
    sheet = wb.sheet_by_name(sh_name)
    #--if this sheet has at least one row of something
    if sheet.nrows > 0:
        #--assume the values in row 1 (index 0) are the column titles
        header = sheet.row_values(0)        
        #--create a python dict to store everything
        sheet_dict = {}        
        #--loop over each column
        for colnum in range(sheet.ncols):
            #--set the a key,value pair in the dict. 
            #--The key is the header value for this column
            #--the value is actually a list of the values in this column. 
            #--The [1:] index chops off the header
            #--since it comes back as part of col_values()
            sheet_dict[header[colnum]] = sheet.col_values(colnum)[1:] 
        #--to access the data in the dict, use iteritems() like this
        for header,values in sheet_dict.iteritems():
            print header
            print values
        #--or like this
        print sheet_dict['DSN']
        print sheet_dict['LOCATION']
        print sheet_dict['CONSTITUENT']

