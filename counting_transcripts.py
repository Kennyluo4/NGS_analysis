def help():
    print("usage: python counting_transcripts.py GTF file"
          "counting the transcripts number in a GTF file")
import sys
argv = sys.argv
try:
    f = argv[1]
except  IndexError:
    help()
print(f)
# f = open("stringtie_merged_pe_IDmodified.gtf")
num = 0
for lines in open(f):
    if lines.startswith("#"):
        continue
    else:
        trans = lines.split('\t')[2]
        if trans == "transcript":
            num += 1
            print(lines.strip())
print("Total transcript number is %d" % num)