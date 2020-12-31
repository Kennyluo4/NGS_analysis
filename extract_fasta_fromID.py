#!usr/bin/python

'''get the fasta sequence from the provided sequence ID list
'''

import sys, getopt

def help():
    print('Usage: python extract_fasta_fromID.py <input.fasta> <list.txt> <output.fasta>')
    print('\t Extract fasta sequences based on the ID provided in list.txt')
    print('\t Only exactly matched ID will be extracted')
    print('\t Annotations for the input.fasta IDs will be truncated')

def readFasta(f1):
    print("...Reading fasta file: %s" % f1)
    seq_dic = {}
    seq_num = 0
    for line in open(f1):
        if line.startswith('>'):
            seq_num += 1
            id = str(line.strip().replace('>', '').split('\t')[0])
            if id not in seq_dic.keys():
                seq_dic[id] = ''
            else:
                print('warning: duplicated ID: %s,' % id)
                id += '_dup'
                seq_dic[id] = ''
                continue
        elif line.startswith('#'):
            continue
        else:
            seq = line.strip()
            seq_dic[id] += seq
    print('...%s sequence in the input fastafile' % seq_num)
    return seq_dic

def extractFa(seqs, IDfile):
    print('...extracting sequence from %s' % IDfile)
    res = {}
    notfind = []
    list_num = 0
    for ln in open(IDfile):
        id = ln.strip().replace('>', '')
        if id in seqs.keys():
            res[id] = seqs[id]
            list_num += 1
        else:
            # notfind.append(id + '\n')
            continue
    print('...%s fasta extracted from the ID list' % list_num)
    # print(notfind)
    return res

if __name__ == '__main__':
    argvs = sys.argv
    try:
        infasta, inlist, output = argvs[1], argvs[2], argvs[3]
        # infasta, inlist, output = 'sorf_osa_combined_cdhit99.fasta', 'clustered_ribocode_list.txt', 'clutered_ribocode.fasta'
        allseqs = readFasta(infasta)
        selectedseq = extractFa(allseqs, inlist)
        print('output file is %s' % output)
        with open(output, 'w') as handle:
            for k,v in selectedseq.items():
                handle.writelines('>' + k + '\n' + v + '\n')
    except:
        help()
 


