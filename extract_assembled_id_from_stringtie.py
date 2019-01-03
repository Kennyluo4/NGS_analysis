'''usage: python extract_assembled_id_from_stringtie.py [your gff file]
    extract the corresponding Stringtie gene ID, transcript ID and ref gene ID for each transcripts Stringtie assembled
    summarize the unique Stringtie gene ID that have reference gene ID '''
import sys
argvs = sys.argv
file = argvs[1]
f = open(file)
# f = open('assembed_transcripts_pe.gtf')
res = ['stringtie_geneID\ttranscriptID\tref+geneID\tgeneID_used_for_gffcompare\n']
ref_gene_dic = {}
for lines in f:
    if lines.startswith('#'):
        continue
    itms = lines.strip().split('	')
    type,ids = itms[2], itms[8]
    if type == 'transcript':
        idlist = ids.replace(';','').replace('"', '').split(' ')
        if len(idlist)<=4:
            res.append(idlist[1] + '\t' + idlist[3] + '\t\t' + idlist[1] + '\n')
            if idlist[1] not in ref_gene_dic.keys():
                ref_gene_dic[idlist[1]] = ''
        else:
            res.append(idlist[1] + '\t' + idlist[3] + '\t' + idlist[7] + '\t' + idlist[5] + '\n')
            if idlist[1] not in ref_gene_dic.keys():
                ref_gene_dic[idlist[1]] = idlist[7]
            else:
                if ref_gene_dic[idlist[1]].startswith(''):    #add ref gene if other isoform is not ref gene
                    ref_gene_dic[idlist[1]] = idlist[7]

with open('unique_geneID.csv', 'w') as csvf:
    writer = csv.writer(csvf)
    writer.writerow(['unique_geneID', 'ref_gene_ID'])
    for k, v in ref_gene_dic.items():
        writer.writerow([k,v])
        
with open('geneID_transcriptID_from_gff', 'w') as handle:
    handle.writelines(res)
