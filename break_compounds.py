""" 
take a multisheet xlsx and for each sheet break its compound statements into more rows of data
Usage: python break_compounds.py
"""
import sys
import csv
import numpy as np
import pandas as pd
import nltk
from nltk import sent_tokenize
#nltk.download('punkt')
import coding_helper

input_file = sys.argv[1]
output_file = sys.argv[2]

### HELPER
def break_compounds_sheet( sheet, verbose=False ):
    #### counters for sanity, debugging, and info
    row_count = 0
    row_count_n = 0
    rows_out = []
    for i, row in sheet.iterrows():  # For each row of the sheet ...
        #print( "for each row", type( row ))
        an_is = row["Institutional Statement"]
        ### ... break into several IS's if necessary
        ###     this code retokenizes the same string each sheet. not worth optimizing.
        an_is = an_is.replace(r'\n', ' ')
        an_is = an_is.replace(r'\\', ' ')
        iss = nltk.sent_tokenize( an_is )
        row_count += 1
        if len(iss) == 1:
            rows_out.append( row )
            row_count_n += 1
        else:
            ### if IS was compund, break it into identical rows
            for an_is_new in iss:
                row_new = row.copy()
                row_new['Institutional Statement'] = an_is_new
                row_new['Text Type'] = 'IS_recovered'
                rows_out.append( row_new )
                row_count_n += 1
    print("Sheet {} had {} rows, now has {} rows".format( sheet_name, row_count, row_count_n ))
    sheet_out = pd.DataFrame( rows_out )
    return( sheet_out )

### SCRIPT
#read document
xls = pd.ExcelFile( input_file )
sheets = xls.sheet_names
for sheet_name in sheets:
    ### only stretch sheets with data
    if not sheet_name.startswith('statements_'):
        continue
    sheet = pd.read_excel(input_file, sheet_name)
    sheet_out = break_compounds_sheet( sheet ) # <- creates new sheet with compunds fractured into new rows
    sheet_out.to_excel(output_file, sheet_name=sheet_name)
