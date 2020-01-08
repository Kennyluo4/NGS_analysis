def help():
    print("Use:\npython find_orthogroup.py Orthogroups.txt\n"
          "#Find the orthologs for transcripts from orthogroup result in Orthofinder")

import csv
import sys
try:
    file = sys.argv[1]
except IndexError:
    help()
    exit()

res = {}
#define a list containing other species' abbriviation (ortholog species)
spc = ['ahy|', 'lja|', 'glm|', 'mtr|']
for lines in open(file):          #each line is an orthogroup
# for lines in open('orthotest.txt'):
    if 'seq' in lines and any([i in lines for i in spc]):       #if orthogroup has target transcript(start with 'seq|') and other species protein
        itms = lines.strip().replace('OG\d*: ', '').replace('\t', ' ').split(' ')
        ortho = ""
        for prot in itms:     #collect the orthologs from other species
            if any(i in prot for i in spc):
                ortho += " " + prot
        for prot in itms:     #append collected orthologs to targeted transcripts
            if 'seq' in prot:  #find targeted transcripts
                if prot not in res.keys():
                    res[prot] = ortho
                else:
                    res[prot] += " " + ortho

with open("ortho_result.csv", "w") as file:
    writer = csv.writer(file)
    for key, value in res.items():
        ln = [key,value]
        writer.writerow(ln)