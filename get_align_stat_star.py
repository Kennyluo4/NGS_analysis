'''get the alignment statistics from STAR aligner output files:{prefix}Log.final.out'''
import glob
import pandas as pd

def readFiles():
    files = glob.glob('*Log.final.out')
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
    files = readFiles()
    data = []
    for f in files:
        alignment = readStats(f)
        data.append(alignment)
    df = pd.DataFrame(data, columns = ['Sample ID', 'TotalReadsPair', 'UniqueAlign', 'Multi-Align', 'TooManyAlign', 'Unmapped'])
    df['overall%'] = (df['UniqueAlign'] + df['Multi-Align'])/df['TotalReadsPair']
    df.to_excel('STAR_alignment_statistics.xlsx',index=False)

if __name__ == "__main__":
    main()