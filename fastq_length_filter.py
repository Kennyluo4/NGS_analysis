'''usage: python fastq_length_filter.py [cutoff]
from trimmomatic result fastq files. classify reads with different length range based on the cutoff'''
import sys, glob, gzip

def cutoff_set():
    cutoff = 30
    argvs = sys.argv
    #print(argvs)
    if len(argvs) < 2:
        print('no length cutoff assigned, default is 30bp')
    elif len(argvs) > 2:
        print('too many arguments, cutoff of 30 bp will be used ')
    else:
        cutoff = argvs[1]
        print('cutoff length set as %s' % cutoff)
    return cutoff

def read_file():
    sample_list = []
    obj = {}
    file_list = glob.glob('*.fq.gz')
    if len(file_list) == 0:
        file_list = glob.glob('*.fastq.gz')
    if len(file_list) == 0:
        print("no file (.fq.gz or .fastq.gz) detected.")
    #for each sample, create a list for storing long and short reads
    for finame in file_list:
        sample_id = finame.split('_')[0].split('.')[0]
        if sample_id not in sample_list:
            sample_list.append(sample_id)
    if len(file_list)/len(sample_list) > 1:   #paired reads file, one sample have 4 files after trimming by Trimmomatic
        type = 'pe'
        print('Detected paired reads files')
        for samples in sample_list:
            obj[samples + '_pair1_long'] = []
            obj[samples + '_pair2_long'] = []
            obj[samples + '_pair1_short'] = []
            obj[samples + '_pair2_short'] = []
            obj[samples + '_unpaired_long'] = []
            obj[samples + '_unpaired_short'] = []
    else:
        type = 'se'
        print('Detected single end reads files')
        for samples in sample_list:
            obj[samples + '_unpaired_long'] = []
            obj[samples + '_unpaired_short'] = []
    return obj, file_list, sample_list, type

if __name__ == '__main__' :
    cut = int(cutoff_set())
    # sample_list = []
    # obj = {}
    # file_list = glob.glob('*.fq.gz')
    # if len(file_list) == 0:
    #     file_list = glob.glob('*.fastq.gz')
    # if len(file_list) == 0:
    #     print("no file (.fq.gz or .fastq.gz) detected.")
    # for finame in file_list:     #for each sample, create a list for storing long and short reads
    #     sample_id = finame.split('_')[0].split('.')[0]
    #     if sample_id not in sample_list:
    #         obj[sample_id + '_long'] = []
    #         obj[sample_id + '_short'] = []
    #         sample_list.append(sample_id)
    obj, filelist, samplelist, filetype = read_file()
    paired_files = {}
    for file in filelist:
        # (1)handle unpaired reads file
        if 'U' in file or 'Unpair' in file:
            samples = file.split('.')[0].split('_')[0]
            f = gzip.open(file, 'rt').readlines()     #default 'rb' is for read as binary. 'rt' read as text
            for i in range(0, len(f), 4):             #read every four lines in fastq for each sequence
                seq = f[i + 1].strip()
                if len(seq) >= cut:
                    obj[samples + '_unpaired_long'] += f[i:(i+4)]
                else:
                    obj[samples + '_unpaired_short'] += f[i:(i+4)]
        # (2.1)handle paired reads file, first collect paired files by sample
        elif 'P' in file or 'Pair' in file:
            samples = file.split('.')[0].split('_')[0]
            if samples not in paired_files.keys():
                paired_files[samples] = [file]
            else:
                paired_files[samples].append(file)

    for sample, pairfiles in paired_files.items():
        pair1 = {}
        pair2 = {}
        #paired files should include 'pair' or 'P'. e.g. '1P', '2P'(standard output from Trimmomatic), or 'pair1','pair2'
        if 'Pair1' in pairfiles[0] or '1P' in pairfiles[0]:
            f1 = gzip.open(pairfiles[0], 'rt').readlines()
            f2 = gzip.open(pairfiles[1], 'rt').readlines()
        else:
            f1 = gzip.open(pairfiles[1], 'rt').readlines()
            f2 = gzip.open(pairfiles[0], 'rt').readlines()
        #for paird reads in paired files, collect the sequence for each read
        for i in range(0, len(f1), 4):
            readID = f1[i].split(' ')[0]
            pair1[readID] = f1[i:(i + 4)]
        for i in range(0, len(f2), 4):
            readID = f2[i].split(' ')[0]
            pair2[readID] = f2[i:(i + 4)]
        paired_read = set(pair1.keys()) & set(pair2.keys())     # paired reads ID
        #(2.2)pick up unpaired reads in paired files
        unpaired_reads = (pair1.keys() - pair2.keys()) | (pair2.keys() - pair1.keys())
        #(2.3)for each paired reads present in two files, classify them by cutoff length
        for k in paired_read:
            if len(pair1[k][1]) > cut or len(pair2[k][1]) >= cut:
                obj[sample + '_pair1_long'] += pair1[k]
                obj[sample + '_pair2_long'] += pair2[k]
            else:
                obj[sample + '_pair1_short'] += pair1[k]
                obj[sample + '_pair2_short'] += pair2[k]
        for ky in unpaired_reads:
            if ky in pair1.keys():
                if len(pair1[ky][1]) > cut:
                    obj[samples + '_unpaired_long'] += pair1[ky]
                elif len(pair2[ky][1]) < cut:
                    obj[samples + '_unpaired_short'] += pair1[ky]
            elif ky in pair2.keys():
                if len(pair2[ky][1]) > cut:
                    obj[samples + '_unpaired_long'] += pair2[ky]
                elif len(pair2[ky][1]) < cut:
                    obj[samples + '_unpaired_short'] += pair2[ky]

    for keys in obj.keys():
        print(keys)
        if obj[keys] == []:
            print("empty file is: %s" % keys)
        with gzip.open('%s_reads.fq.gz' % keys, 'wt') as handle:
            handle.writelines(obj[keys])


