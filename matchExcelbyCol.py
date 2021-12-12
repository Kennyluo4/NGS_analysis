import pandas as pd
import sys

args = sys.argv
try:
    ToF, FromF, colID = args[1], args[2], args[3]
    print('\t Append <%s> to <%s> by "%s"' % (FromF, ToF, colID))
except KeyError:
    print("Use: python matchExcelbyCol.py <target_file> <source_file> <column_name_to_search>")
    print("\t Append <source file> to <target file> by <column_name_to_search>")
# test
# ToF='DEG2_lowerStandard2021.8.20.xlsx'
# FromF = 'All_transcript_gene_annotation5.7.2020_Lite.xlsx'
# colID = "#gene_id"

print('reading file 1: %s' % ToF)
if '.csv' in ToF:
    df1 = pd.read_csv(ToF)
else:
    df1 = pd.read_excel(ToF, sheet_name=2)
# print(df1.head())
colID = str(colID)
print('reading file 2: %s' % FromF)
if '.csv' in FromF:
    df2 = pd.read_csv(FromF)
else:
    df2 = pd.read_excel(FromF, sheet_name=0) #change sheet name accordingly
print("df1:")
print(df1.head())
print("df2:")
print(df2.head())
res = df1.merge(df2, on=colID, how='left')
# how: left - use key on the df2, keep the key even there is no match
targetfile = ToF.split('.')[0]
sourcefile = FromF.split('.')[0]
resname = targetfile + '_' + sourcefile + '_merged.xlsx'
res.to_excel(resname)
