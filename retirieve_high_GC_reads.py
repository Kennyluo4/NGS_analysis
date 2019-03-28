'''retrieve high GC content (>0.7) reads in fq.gz file. You need to specifiy file name and cutoff in the script'''


def cal_GC(seq):
    seq = seq.strip().upper()
    read_length = len(seq)
    GC_count = 0
    for i in seq:
        if i == "G" or i == "C":
            GC_count += 1
    GC_content = GC_count/read_length
    return GC_content
import gzip
res = []
f = gzip.open('10_S22_R_1U.fq.gz', 'rt').readlines()
for i in range(0,len(f),4):
    id = f[i].split(' ')[0]
    seq = f[i + 1].strip()
    gc_content = cal_GC(seq)
    if gc_content >=0.7:
        res.append('>' + id + '\n' + seq + '\n')

with open('high_gc_content.fasta', 'w') as file:
    file.writelines(res)
