#!/bin/env python3
#Usage: python mstrg_prep.py stringtie_merged_se.gtf > stringtie_merged_se_IDmodified.gtf
#appending refgene ID to stringtie assigned ID (MSTRG.*) if the gene region includes a ref gene

import re, fileinput
g = {}     #gene_id => {ref_gene_ids}
prep = []  #array of [line, mstrg_id]
for line in fileinput.input():
# for line in open("stringtie_merged_pe.gtf"):
    line = line.rstrip()
    t = line.split('\t')
    if len(t) < 9:
        print(line)
        continue
    mgid = re.search('gene_id "(MSTRG\.\d+)"', t[8])     #search if GeneID in annotation column .
    if mgid:
        gid = mgid.group(1)            #if matched geneID, assign to mgid
        prep.append([line, gid])        #append original line and extracted gene ID
        #mrn = re.search('ref_gene_id "([^"]+)', t[8])
        g_name = re.search('gene_name "([^"]+)', t[8])     #find the gene_name
        if g_name:
            gn = g_name.group(1)     #if find gene_name, assign to gn
            h = g.get(gid)
            if h:         #if gid in gene dic
                h.add(gn)
            else:
              g[gid] = {gn}
    else:
        print(line)

prevgid, gadd = '', ''
for [line, gid] in prep:
    if prevgid != gid:
        gadd = ''
        h = g.get(gid)
        if h:
            gadd = '|'+'|'.join(sorted(g[gid]))
    if len(gadd) > 0:
        line = re.sub('gene_id "MSTRG\.\d+', 'gene_id "'+gid+gadd, line)
    print(line)
