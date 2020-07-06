import os, glob
id_dic = {}
for lns in open('sampleIDconvert'):
    cols = lns.strip().split('\t')
    sraid, sampleid = cols[0], cols[9]
    id_dic[sraid] = sampleid

oldfiles = glob.glob('*.fastq')
sample_num = len(oldfiles)
print('%s samples detected' % sample_num)

for ids in oldfiles:
    id_base = ids.split('_')[0]
    try:
        converter = id_dic[id_base]
    except KeyError:
        continue
    newfile = ids.replace(id_base, converter)
    os.rename(ids, newfile)