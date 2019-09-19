#!/usr/bin/env python
'''use: python prepare_mireap_map.py mapfile_to_genome.arf'''
import sys

f = sys.argv[1]
res =[]
newf = f.replace("_to_genome.arf", "_map.txt")
print("start working on %s" % f)
print("output file is %s" % newf)

with open(f,'r') as handle:
    with open(newf, 'w') as outhandle:
        for lines in handle:
            itms = lines.strip().split('\t')
            read, chr, start, end, strand = itms[0].split("_x")[0] + "_x", itms[5], itms[7], itms[8], itms[10]
            outhandle.write(read + "\t" + chr + "\t" + start + "\t" + end + "\t" + strand + "\n")
