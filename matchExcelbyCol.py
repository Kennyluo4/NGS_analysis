'''handy script for matching excel files. Similar to vlookup'''
import pandas as pd
import sys

args = sys.argv
try:
    FromF, ToF, colID = args[1], args[2], args[3]
    print('\t Append <%s> to <%s> by "%s"' % (FromF, ToF, colID))
except KeyError:
    print("Use: python matchExcelbyCol.py <source_file> <target_file> <column_name>")
    print("\t Append <source file> to <target file> by <column_name_to_search>")
# test
# ToF='DEG2_lowerStandard2021.8.20.xlsx'
# FromF = 'All_transcript_gene_annotation5.7.2020_Lite.xlsx'
# colID = "#gene_id"

print('reading file 1: %s' % FromF)
if '.csv' in FromF:
    df1 = pd.read_csv(FromF)
else:
    df1 = pd.read_excel(FromF, sheet_name=0)  # change sheet name accordingly

print('reading file 2: %s' % ToF)
if '.csv' in ToF:
    df2 = pd.read_csv(ToF)
else:
    df2 = pd.read_excel(ToF, sheet_name=0)  # default 1st sheet, change value depend on your file
# print(df2.head())
colID = str(colID)
print("df1:")
print(df1.head(3))
print("df2:")
print(df2.head(3))
res = df2.merge(df1, on=colID, how='left')
# how: left - use key on the df2, keep the key even there is no match
targetfile = ToF.split('.')[0]
sourcefile = FromF.split('.')[0]
resname = targetfile + '_' + sourcefile + '_merged.xlsx'
res.to_excel(resname)
print('Output merged file: %s', resname)
