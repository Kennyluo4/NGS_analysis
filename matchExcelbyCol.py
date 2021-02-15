import pandas as pd
import sys

args = sys.argv
try:
    ToF2, FromF1, colID = args[1], args[2], args[3]
    print('\t Append <%s> to <%s> by "%s"' % (FromF1, ToF2, colID))
except:
    print("Use: python matchExcelbyCol.py <target_file> <source_file> <column_name_to_search>")
    print("\t Append <source file> to <target file> by <column_name_to_search>")

if '.csv' in FromF1:
    df1 = pd.read_csv(ToF2)
else:
    df1 = pd.read_excel(ToF2, sheet_name=0)
if '.csv' in FromF1:
    df2 = pd.read_csv(FromF1)
else:
    df2 = pd.read_excel(FromF1, sheet_name=0)
colID = str(colID)
# print(df1)
# print(df2)
res = df1.merge(df2, on=colID, how='left')
# how: left - use key on the df2, keep the key even there is no match
targetfile = ToF2.split('/')[-1].strip('.xlsx').strip('.csv')
sourcefile = FromF1.split('/')[-1].strip('.xlsx').strip('.csv')
resname = targetfile + '_' + sourcefile + 'merged.xlsx'
res.to_excel(resname)
