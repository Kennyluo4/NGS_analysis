'''usage: python fastq_length_filter.py [cutoff]
from trimmomatic result fastq files. classify reads with different length range based on the cutoff'''
import sys
import glob

def cutoff_set():
    cutoff = 30
    argvs = sys.argv
    print(argvs)
    if len(argvs) < 2:
        print('no length cutoff assigned, default is 30bp')
    elif len(argvs) > 2:
        print('too many arguments, cutoff of 30 bp will be used ')
    else:
        cutoff = argvs[1]
        print('cutoff length set as %s' % cutoff)
    return cutoff

if __name__ == '__main__' :
    import gzip

    cut = int(cutoff_set())
    sample_list = []
    obj = {}
    file_list = glob.glob('*.fastq.gz')
    for finame in file_list:     #for each sample, create a list for storing long and short reads
        sample_id = finame.split('_')[0]
        if sample_id not in sample_list:
            obj[sample_id + '_long'] = []
            obj[sample_id + '_short'] = []
            sample_list.append(sample_id)
    for file in file_list:
        samples = file.split('_')[0]
        f = gzip.open(file, 'rt').readlines() #default 'rb' is for read as binary. 'rt' read as text
        for i in range(0, len(f), 4):    #read every four lines in fastq for each sequence
            seq = f[i + 1].strip()
            if len(seq) >= cut:
                obj[samples + '_long'] += f[i:(i+4)]
            else:
                obj[samples + '_short'] += f[i:(i+4)]

    for keys in obj.keys():
        with open('%s_reads.fastq' % keys, 'w') as handle:
            handle.writelines(obj[keys])


