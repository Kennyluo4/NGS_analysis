#!/usr/bin/env python
import csv, sys
def help():
    print('Usage: python class_transform.py <target_csv_file>')
    print('Use python3 for the script')

def read_file():
    args = sys.argv
    if len(args) < 2:
        print('No file is assigned')
        help()
    elif len(args) > 2:
        print('Too many input')
        help()
    else:
        print('Output file is transformed_file.csv')
        return args[1]

file = read_file()
# print("arg read:", file)
# file = 'test.csv'
all_species = []
res = []
with open(file, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for rows in csvreader:
        trans_row = [rows[0]]
        species = {}
        for sp_genes in rows[1:]:
            try:
                spec, geneID = sp_genes.split('|')[0], sp_genes.split('|')[1]
            except IndexError:
                continue
            if spec in species.keys() and geneID not in species[spec]:  #for each class, if
                species[spec] += ', ' + geneID
            else:
                species[spec] = geneID
            if spec not in all_species:        #summarize all the species in the analysis
                all_species.append(spec)
        for spe_col in all_species:
            if spe_col in species.keys():
                trans_row.append(species[spe_col])
            else:
                trans_row.append('')
        res.append(trans_row)
title = ['class'] + all_species
res.insert(0,title)

with open('transformed_file.csv', 'w') as file:
    filewriter = csv.writer(file)
    for row in res:
        filewriter.writerow(row)