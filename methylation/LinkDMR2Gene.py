'''link DSS DMR result.csv with nearby/overlapped gene in a gtf file
    upstream and downstream 2k
    Usage: python3 LinkDMR2Gene.py DMR_file GTFfile
    the position of DMR is given, eg. DMR at upstream of a gene
    Make sure GTF file is sorted by chromosome'''
import pandas as pd
import sys
import HTSeq

def read_gtf(gtff):
    '''read each transcript record  the gene and gene postion by chromosome {chr:{gene:start,end}}'''
    chrDic = {}
    gDic = {}
    gff_file = HTSeq.GFF_Reader(gtff, end_included=True)
    for feature in gff_file:
        if feature.type == "transcript":
        # print(feature)
            # print(feature.attr)
            gene_id = feature.attr['gene_id']
            chr = feature.iv.chrom
            start = feature.iv.start
            end = feature.iv.end
            if gene_id not in gDic:
                gDic[gene_id] = [chr, start, end]
    return gDic

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
    df = pd.read_csv(dmrf)         #DMR pandas.DataFrame
    g_coord = read_gtf(gtff)     #{geneID:[chr,start,end]}

    #compare the position for each DMR
    for index, row in df.iterrows():
        DMRchr, DMRstart, DMRend = row['chr'], int(row['start']), int(row['end'])
        # nearbygenesList = []
        for geneID, coordinates in g_coord.items():
            Gchr, Gstart, Gend = coordinates[0], coordinates[1], coordinates[2]
            if Gchr == DMRchr:
                gene_position = overlap(Gstart, Gend, DMRstart, DMRend)
                if gene_position in ['overlap','upstream 2k','downstream 2k']:
                    df.loc[index, 'nearby_gene'] = geneID
                    df.loc[index, 'gene_location2DMR'] = gene_position
                    df.loc[index, 'geneInteval'] = str(Gstart) + '-' + str(Gend)
                else:
                    df.loc[index, 'nearby_gene'] = "NA"
                    df.loc[index, 'gene_location2DMR'] = "NA"
                    df.loc[index, 'geneInteval'] = "NA"
                    continue
            else:
                continue
    df.to_csv(outfile)
    print('output file: %s' % outfile)

if __name__=='__main__':
    main()
