'''link DSS DMR result.csv with nearby/overlapped gene in a gtf file
    upstream and downstream 2k
    Usage: python3 LinkDMR2Gene.py DMR_file GTFfile'''
import pandas as pd
import sys

def read_gtf(gtff):
    #take the transcript coordinate first. merge transcript with same genes.
    chrDic = {}
    # gDic = {}
    for lines in open(gtff):
        if lines.startswith('#'):
            continue
        elif 'Gnomon\ttranscript' in lines: #take only transcript information
            col = lines.strip().split('\t')
            chr, start, end, note = col[0], int(col[3]), int(col[4]), col[8]
            subcol = note.split("; ")
            geneID = subcol[1].replace('"', '').replace('gene_id ', '')
            if chr not in chrDic.keys():
                chrDic[chr] = {}
                if geneID not in chrDic[chr].keys():
                    chrDic[chr][geneID] = [start, end]
                else:# if the gene is recorded, but the new transcript start or end is outside of that gene(start < g_start, end >g_end), extend the gene range.
                    if start < chrDic[chr][geneID][0]:
                        chrDic[chr][geneID][0] = start
                    if end > chrDic[chr][geneID][1]:
                        chrDic[chr][geneID][1] = end
            else:
                if geneID not in chrDic[chr].keys():
                    chrDic[chr][geneID] = [start, end]
                else:
                    if start < chrDic[chr][geneID][0]:
                        chrDic[chr][geneID][0] = start
                    if end > chrDic[chr][geneID][1]:
                        chrDic[chr][geneID][1] = end
    return chrDic

def overlap(s1, e1, s2, e2):
    '''determine the position of obj1 corresponding to obj2'''
    #check if coordinates are in order
    if e1 - s1 < 0 or e2 - s2 < 0:
        print("error: the oder of start and end is opposite")
        exit()
    type = ''
    if s2 - e1 > 2000:
        type = 'not overlap'
    elif 0 <= s2 - e1 <= 2000:
        type = 'upstream 2k'
    elif s2 < e1 <= e2 or s2 <= s1 < e2:
        type = 'overlap'
    elif 0 <= s1 - e2 <= 2000:
        type = 'downstream 2k'
    else:
        type = 'not overlap'
    return type

def main():
    argvs = sys.argv
    dmrf = argvs[1]
    gtff = argvs[2]
    print('DMR file is %s, and GTF file is %s' % (dmrf, gtff))
    # gtff = 'test.gtf'
    # dmrf = 'dmr_CG_2hpi.csv'
    outfile = dmrf.replace('.csv', '_with_genes.csv')
    df = pd.read_csv(dmrf)
    g_coord = read_gtf(gtff)

    for index, row in df.iterrows():
        DMRchr, DMRstart, DMRend = row['chr'], int(row['start']), int(row['end'])
        try:  # in case
            genes = g_coord[DMRchr]
        except KeyError:
            # print('warning: %s doesn\'t have gene in the gtf file ' % DMRchr)
            continue
        nearbygenesList = []
        for geneID, coordinates in genes.items():
            Gstart, Gend = coordinates[0], coordinates[1]
            gene_position = overlap(Gstart, Gend, DMRstart, DMRend)
            if gene_position in ['overlap','upstream 2k','downstream 2k']:
                nearbygenesList.append(geneID + ': ' + str(Gstart) + '-' + str(Gend) + ' (' + gene_position + ')')
            else:
                continue
        nearbygenes = ';'.join(nearbygenesList)
        df.loc[index, 'nearby_gene'] = nearbygenes
    df.to_csv(outfile)
    print('output file: %s' % outfile)

if __name__=='__main__':
    main()



