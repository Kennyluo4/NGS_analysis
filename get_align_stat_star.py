'''get the alignment statistics from STAR aligner output files:{prefix}Log.final.out'''
import glob
import pandas as pd
import datetime

time = datetime.datetime.now()

## add time tag: year_month_day_hourmin
run_date = '%s_%s_%s_%s%s' % (time.year, time.month, time.day, time.hour, time.minute)

def readFiles(reg_expr):
    files = glob.glob(reg_expr)
    num_f = len(files)
    print('%s samples (STAR output files) detected in current directory' % num_f)
    return files

def readStats(f):
    print('reading file ... %s' % f)
    sampleID = f.replace('Log.final.out','')
    total = 0
    uniq = 0
    multi = 0
    multi_toomany = 0
    unmapped = 0
    for lines in open(f):
        if 'Number of input reads |' in lines:
            total = int(lines.split('|')[1].strip())
        elif 'Uniquely mapped reads number' in lines:
            uniq = int(lines.split('|')[1].strip())
        elif 'Number of reads mapped to multiple loci' in lines:
            multi = int(lines.split('|')[1].strip())
        elif 'Number of reads mapped to too many loci' in lines:
            multi_toomany = int(lines.split('|')[1].strip())
        elif 'Number of reads unmapped: too many mismatches' in lines or 'Number of reads unmapped: too short' in lines or 'Number of reads unmapped: other' in lines:
            unmapped += int(lines.split('|')[1].strip())
    row = [sampleID, total, uniq, multi, multi_toomany, unmapped]
    return row

def main():
    files = readFiles('*Log.final.out')
    outfile = 'STAR_alignment_statistics_' + run_date + '.xlsx'
    data = []
    for f in files:
        alignment = readStats(f)
        data.append(alignment)
    df = pd.DataFrame(data, columns = ['Sample ID', 'TotalReadsPair', 'UniqueAlign', 'Multi-Align', 'TooManyAlign(>10)', 'Unmapped'])
    df['unique%'] = df['UniqueAlign'] / df['TotalReadsPair']
    df['overall%'] = (df['UniqueAlign'] + df['Multi-Align'] + df['TooManyAlign(>10)'])/df['TotalReadsPair']
    df.to_excel(outfile,index=False)
    print(f'Outupt file: {outfile}')

if __name__ == "__main__":
    main()