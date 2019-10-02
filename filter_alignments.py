
def help():
    print("use: python filter_alignments.py [options] -i <inputFile>"
          "This is for filter small RNA reads alignment  used in miRDP2"
          "-i, --input <blastfile>: assign the input blast file"
          "-m, --max [int]: the maximum number of multi-alignment, default is 15"
          "-f, --fasta <fastafile>: assign the fasta file needded to be filtered by -m option")

import getopt, sys
def getoptions():
    align = 15
    blstfile, fastafile = None, None
    try:
        opts, agrs = getopt.getopt(sys.argv[1:], "hi:m:f:", ["help", "input=", "max=", "fasta="])
    except:
        help()
        sys.exit(2)
    if len(opts) == 0:
        help()
    for opt, arg in opts:
        if opt == '-h':
            help()
        if opt in ("-i", "--input"):
            blstfile = arg
            print("input file is %s" % blstfile)
        if opt in ("-m", "--max"):
            align = arg
        if opt in ("-f", "--fasta"):
            fastafile = arg
            print("input fasta file is   %s" % fastafile)
    print("filter out reads multi-aligned greater than %d" % int(align))
    return blstfile, align, fastafile

def read_alignment_query(f):
    readDic = {}
    for line in open(f):
        reads = line.strip().split('\t')[0]
        if reads not in readDic.keys():
            readDic[reads] = 1
        else:
            readDic[reads] += 1
    return readDic

def filterFasta(file, countDic,filter=15):
    outf = file.split(".")[0] + "_filtered" + str(filter) + ".fa"
    print('output filtered fasta file is %s.' % outf)
    f = open(file).readlines()
    with open(outf, "w") as handle:
        for i in range(0, len(f), 2):
            readID = f[i].strip().replace(">", "")
            if countDic[readID] <= filter:
                handle.write(f[i])
                handle.write(f[i+1])

def main():
    # import sys
    # argvs = sys.argv
    # input = argvs[1]
    input, alignment, fastafile = getoptions()
    output = input.split(".")[0] + "_filtered" + str(alignment) + ".bst"
    print('output filtered file is %s.' % output)
    read_dic = read_alignment_query(input)
    with open(input, "r") as handle:
        with open(output, "w") as outhandle:
            for ln in handle:
                reads = ln.strip().split('\t')[0]
                if read_dic[reads] <= int(alignment):
                    outhandle.write(ln)
    if fastafile:
        filterFasta(fastafile, read_dic, int(alignment))


if __name__=="__main__":
    main()
