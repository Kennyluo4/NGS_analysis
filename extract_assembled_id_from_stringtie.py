'''usage: python extract_assembled_id_from_stringtie.py [your gff file]
    extract the corresponding Stringtie gene ID, transcript ID and ref gene ID for each transcripts Stringtie assembled'''
import sys
argvs = sys.argv
file = argvs[1]
f = open(file)
# f = open('assembed_transcripts_pe.gtf')
res = ['stringtie_geneID\ttranscriptID\tref+geneID\tgeneID_used_for_gffcompare\n']
for lines in f:
    if lines.startswith('#'):
        continue
    itms = lines.strip().split('	')
    type,ids = itms[2], itms[8]
    if type == 'transcript':
        idlist = ids.replace(';','').split(' ')
        if len(idlist)<=4:
            res.append(idlist[1] + '\t' + idlist[3] + '\t\t' + idlist[1] + '\n')
        else:
            res.append(idlist[1] + '\t' + idlist[3] + '\t' + idlist[7] + '\t' + idlist[5] + '\n')
with open('geneID_transcriptID_from_gff', 'w') as handle:
    handle.writelines(res)
