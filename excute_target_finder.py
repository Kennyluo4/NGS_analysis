import sys, os

def help():
    print("Usage:\npython excute_target_finder.py <miRNA.fasta> <path/targetfinder script> <transcriptfile>")

try:
    argvs = sys.argv
    seqfile = argvs[1]
    targetfinder = argvs[2]
    transcriptfile = argvs[3]
    print("miRNA sequence file is %s" % seqfile)
    print("the targetfinder script with full path: %s" % targetfinder)
except IndexError:
    help()

    # print("excute:\nperl %s -s %s -d transcripts.adj.fa "% (targetfinder, seq))
for lines in open(seqfile):
    if lines.startswith(">"):
        mirnaID = lines.strip().replace(">", "")
        continue
    elif lines.startswith("#"):
        continue
    else:
        seq = lines.strip()
    os.system("perl %s -s %s -d %s -p table -q %s -t 4" % (targetfinder, seq, transcriptfile, mirnaID))
