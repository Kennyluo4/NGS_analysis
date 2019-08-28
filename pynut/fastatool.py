#!/usr/bin/env python


__author__ = "Ziliang Luo"

def read_fasta(file):
    '''read fasta file, for redundant ID with different sequence, 'Copy' will be added to the redundant ID. Redundant sequence will be removed'''
    dic = {}
    redundant_id = []
    f = open(file)
    ith = 0
    for lines in f:
        if lines.startswith('>'):
            seq = ''
            id = lines.strip().split(' ')[0]
            if id not in dic.keys():
                dic[id] = seq
            else:
                ith += 1
                id += "Copy" + str(ith)
                redundant_id.append(id)
                dic[id] = seq
        else:
            line = lines.strip()
            dic[id] += line
    f.close()
    num_redundantID = len(redundant_id)
    if num_redundantID > 0:
        print("%d redundent ID detected, tag 'Copy' is added" % num_redundantID)
    return dic

