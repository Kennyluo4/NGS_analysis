#!usr/bin/python

'''format fasta to single line format, remove redundant sequence and report'''

import sys, getopt

def help():
    print('Usage: python fasta_handle.py -i <input file> -o <output file> [options]')
    print('  Script will automatically remove redundant sequence, and tag redundant ID(with different sequence) with "Copy"')
    print('     option:\n'
          '     -l cutoff length If assigned with value, only sequence length greater than that value will be kept\n'
          '     -c count sequence length.')
def read_fasta(file):
    '''read fasta file, for redundant ID with different sequence, 'Copy' will be added to the redundant ID. Redundant sequence will be removed'''
    dic = {}
    redundant_id = []
    f = open(file)
    for lines in f:
        if lines.startswith('>'):
            seq = ''
            id = lines.strip().split(' ')[0]
            if id not in dic.keys():
                dic[id] = seq
            else:
                id += "Copy"
                redundant_id.append(id)
                dic[id] = seq
        else:
            line = lines.strip()
            dic[id] += line
    f.close()
    return dic, redundant_id


def read_argv(argv):
    cutoff = ''
    file = ''
    output = 'output.fasta'
    count = 'no'
    try:
        opts, agrs = getopt.getopt(argv, 'hi:o:l:c', ['ifile=','ofile=', 'length=', 'count='])
    except:
        print('getopt error')
        help()
        sys.exit(2)
    if len(opts) == 0:
        help()
    for opt, arg in opts:
        if opt == '-h':
            help()
        elif opt in ('-i', '--ifile'):
            file = arg
        elif opt in ('-o', '--ofile'):
            output = arg
        elif opt in ('-l', '--length'):
            cutoff = arg
            print('length cutoff is:', cutoff)
        elif opt in ('-c', '--count'):
            count = 'yes'
            print('sequence length will be calculate, output as:fasta_length_count')
    print('input file is:', file)
    print('output file is:', output)
    return file, output, cutoff, count

def sum_fasta(file, output, cutoff, count):
    res = []
    non_redun_dic = {}
    uniq = 0
    same_seq = 0
    cutoff_num = 0
    len_res = []
    fasta_dic, redundant_id = read_fasta(file)
    if type(cutoff) is str:                 #no length cutoff
        for k, v in fasta_dic.items():
            if v not in non_redun_dic.values():
                uniq += 1
                lenth = str(len(v))
                len_res.append(k + ':' + lenth + '\n')   #sum the sequence length
                non_redun_dic[k] = v
                res.append(k + '\n' + v + '\n')
            else:
                same_seq += 1
    else:
        for k, v in fasta_dic.items():
            if v not in non_redun_dic.values():
                uniq += 1
                if v >= cutoff:
                    cutoff_num += 1
                    lenth = str(len(v))
                    len_res.append(k + ':' + lenth + '\n')
                    non_redun_dic[k] = v
                    res.append(k + '\n' + v + '\n')
            else:
                same_seq += 1

    if count == 'no':
        with open('%s' % output, 'w') as file:
            file.writelines(res)
        print('redundant IDs:', redundant_id)
        print('there is %d unique sequence' % uniq)
        print('there is %d redundant sequences' % same_seq)
        if type(cutoff) is not str:
            print('There is %d nonredundant sequence >= cutoff length')
    else:
        with open('fasta_length_count', 'w') as file2:
            file2.writelines(len_res)
        with open('%s' % output, 'w') as file:
            file.writelines(res)
        print('redundant IDs:', redundant_id)
        print('there is %d unique sequence' % uniq)
        print('there is %d redundant sequences' % same_seq)
        if type(cutoff) is not str:
            print('There is %d nonredundant sequence >= cutoff length')
            
if __name__ == '__main__':
    ifile, outfile, lenth, count = read_argv(sys.argv[1:])
    if ifile == '':
        exit()
    else:
        sum_fasta(ifile, outfile, lenth, count)