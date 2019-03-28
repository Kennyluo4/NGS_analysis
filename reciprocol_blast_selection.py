Usage = """python reciprocol_blast_selection.py BLASTout1 BLASTout2 OutputFile """

import sys, re
def get_argv():
	if len(sys.argv) != 4:
		print(Usage)
	else:
		in1 = sys.argv[1]
		in2 = sys.argv[2]
		out = sys.argv[3]
	return in1, in2, out
try:
	infile1, infile2, outfile = get_argv()
except UnboundLocalError:
	exit()

#parse first BLAST results
FL1 = open(infile1, 'r')
D1 = {} #dictionary for BLAST file ONE
for Line in FL1:
	if Line[0] != '#':
		Line.strip()
		Elements = re.split('\t', Line)
		queryId = Elements[0]
		subjectId = Elements[1]
		if queryId not in D1.keys():
			D1[queryId] = subjectId  #pick the first hit


#parse second BLAST results
FL2 = open(infile2, 'r')
D2 = {}
for Line in FL2:
	if Line[0] != '#':
		Line.strip()
		Elements = re.split('\t', Line)
		queryId = Elements[0]
		subjectId = Elements[1]
		if queryId not in D2.keys():
			D2[queryId] = subjectId  #pick the first hit

#Now, pick the share pairs

SharedPairs = {}
for k1, v1 in D1.items():
	if v1 in D2.keys() and D2[v1] == k1:
		SharedPairs[k1] = v1

with open(outfile, 'w') as file:
	for k1 in SharedPairs.keys():
		line = k1 + '\t' + SharedPairs[k1] + '\n'
		file.write(line)
file.close()

