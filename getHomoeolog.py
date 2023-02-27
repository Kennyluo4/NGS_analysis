'''use: python getHomoeolog.py [directory]'''

import glob, sys
import pandas as pd

def readFiles(path, reg_expr):
    path = path.strip('/')
    dir = path + '/' + reg_expr
    print('Search: %s' % dir)
    files = glob.glob(dir)
    num_f = len(files)
    print('Working on %s detected files...' % num_f)
    return files

def main():
    args = sys.argv
    if len(args) == 2:  #check if directory is provided
        path = args[1]
    elif len(args) == 1: 
        path = './'
    else:
        print("Input error. use: python getHomoeolog.py [directory]")

    fs = readFiles(path, '*.fa')      # read fasta file (.fa)
    res = []
    for f in fs:
        pair = []    # 1 file has only 1 pair homoeologs
        for ln in open(f):
            if ln.startswith('>'):
                geneID = ln.strip().split('|')[1]
                pair.append(geneID)
            else:
                continue
        res.append(pair)
    df = pd.DataFrame(res, columns = ['gene1', 'gene2'])
    df.to_excel('Single_Copy_Homoeologs.xlsx', index=False)

if __name__ == '__main__':
    main()
            