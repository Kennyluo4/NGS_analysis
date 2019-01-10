'''usage: python get_align_stat.py [alignment log file]'''
__author__ = "Ziliang"

import sys
import csv
def get_file():
	argvs = sys.argv
	if len(argvs) <= 1:
		print("no file")
	elif len(argvs) >2:
		print("too many input")
	else:
		return argvs[1]

res = []
row = []
sampleID = "sample ID"
total_read = "Total reads"
paired_read = "paired reads"
unpaired_read = "unpaied reads"
pair_once = "paired unique aligned"
unpair_once = "unpaired unique aligned"
overall_rate = "overall aligned rate"
type = "single end reads"
file = get_file()
# file = "align_pe_combine_log.out"

for lines in open(file):
    itms = lines.split(" ")
    if ".fq" in lines or ".fastq" in lines:      #identify samples. must print sampleID before each hisat2 run
        row = [sampleID, total_read, paired_read, pair_once, unpaired_read, unpair_once, overall_rate]
        res.append(row)
        sampleID = lines.strip()
        total_read = ""
        pair_once = ""
        unpair_once = ""
        paired_read = ""
        unpaired_read = ""
        overall_rate = ""
    if "reads; of these" in lines:       #total reads
        total_read = itms[0]
    if lines.startswith("    ") and len(itms) <= 11:     #third level
        if "aligned concordantly exactly 1 time" in lines:
            pair_once = itms[4] + itms[5]
            type = "paired end reads"
        elif "aligned exactly 1 time" in lines:
            unpair_once = itms[4] + itms[5]
    elif lines.startswith("  ") and len(itms)<= 11:      #second level,
        if "were paired; of these" in lines:
            paired_read = itms[2] + itms[3]
        elif"were unpaired; of these" in lines:
            unpaired_read = itms[2] + itms[3]
    if "overall alignment rate" in lines:
            overall_rate = itms[0]
print("the reads for alignment is %s" % type)
with open("alignment_stat.csv", "w") as file:
    writer = csv.writer(file)
    for lst in res:
        writer.writerow(lst)
