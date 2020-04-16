import sys
arg = sys.argv
input = arg[1]
print("input file is %s" % input)
res = []

# for lines in open("test.gtf"):
for lines in open(input):
    if lines.startswith("#"):
        continue
    else:
        cols = lines.strip().split('\t')
        if cols[2] == 'transcript':
            IDs = cols[8]
            trans, gene = IDs.split(';')[0], IDs.split(';')[1]
            transID = trans.replace('transcript_id ', '').strip('"')
            geneID = gene.replace(' gene_id ', '').strip('"')
            res.append(geneID + '\t' + transID + '\n')

with open('gene_trans_map', 'w') as handle:
    handle.writelines(res)