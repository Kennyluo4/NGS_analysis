
def help():
    print("use: python filter_alignments.py [options] -i <inputFile>\n"
          "This is for filter small RNA reads alignment  used in miRDP2\n"
          "-i, --input <blastfile>: assign the input blast file\n"
          "-m, --max [int]: the maximum number of multi-alignment, default is 15\n"
          "-f, --fasta <fastafile>: assign the fasta file needded to be filtered by -m option\n")

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
    #count the alignment file, output the dictionray[read ID] = number of alignment hit
    readDic = {}
    for line in open(f):
        reads = line.strip().split('\t')[0]
        if reads not in readDic.keys():
            readDic[reads] = 1
        else:
            readDic[reads] += 1
    return readDic

def filterFasta(file, countDic,filter=15):
    outf = file.split(".")[0] + "_filtered" + ".fa"
    print('output filtered fasta file is %s.' % outf)
    f = open(file).readlines()
    line = 0
    with open(outf, "w") as handle:
        for i in range(0, len(f), 2):
            readID = f[i].strip().replace(">", "")
            line +=1
            if line % 5000 == 0:
                # print process for every 5k alignment
                print("processed %s reads" % line)
            if readID in countDic.keys():  
                if countDic[readID] <= filter:
                    handle.write(f[i])
                    handle.write(f[i+1])

def main():
    import sys
    argvs = sys.argv
    input = argvs[1]
    input, alignment, fastafile = getoptions()
    # input = "GSM2094927.bst"
    # alignment = 15
    # fastafile = "GSM2094927.fa"
    output = input.split(".")[0] + "_filter" + str(alignment) + ".bst"
    print('output filtered file is %s.' % output)
    read_dic = read_alignment_query(input)
    line = 0
    with open(input, "r") as handle:
        with open(output, "w") as outhandle:
            for ln in handle:
                line += 1
                reads = ln.strip().split('\t')[0]
                if read_dic[reads] <= int(alignment):
                    outhandle.write(ln)
                if line%5000 == 0:
                    #print process for every 5k alignment
                    print("processed %s alignment" % line)
    if fastafile:
        filterFasta(fastafile, read_dic, int(alignment))


if __name__=="__main__":
    main()
