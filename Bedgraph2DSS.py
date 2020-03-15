#!/usr/bin/python
'''usage: python Bedgraph2DSS.py inputBedgraphFile > outputDSSfile'''
# -*- coding: utf-8 -*-
# transfer bedgraph format:
# chr start end pct mth unmethy
# arahy.Tifrunner.gnm1.Arahy.01   4386    4389    7       1       13
# to a DSS format
# chr, coor, total, meth


import sys

args = sys.argv
input  = args[1]
res = []
print('chr' + '\t' + 'pos' + '\t' + 'N' + '\t' + 'X')
# with open("DSS_format", 'w') as outhandle:
for lines in open(input):
    if lines.startswith("track type"):
        #print(lines)
        continue
    else:
        cols = lines.strip().split('\t')
        #print(cols)
        chr, start, meth, unmeth = cols[0], cols[1], cols[4], cols[5]
        total = int(meth) + int(unmeth)
        total = str(total)
        # res.append(chr + '\t' + start + '\t' + total +'\t' + meth +'\n')
        print(chr + '\t' + start + '\t' + total + '\t' + meth)
#    outhandle.writelines(res)