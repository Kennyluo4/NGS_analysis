#!/usr/bin/env python
import pandas as pd
import numpy as np
import csv
import sys
argvs = sys.argv
try:
    file = argvs[1]
except:
    print("Use: python RetriveAnnoFromTrinotate.py <TrinotateFile>"
          )
df = pd.read_excel(file)
# df.head()
term2gene = []
term2trans = []
# term2name = []
kegg2gene = []
kegg2trans = []
for index, row in df.iterrows():
    #loop through each row based on their colnames
    GOs = ""
    geneID, transcriptID, blastxGO, blastpGO, pfamGO, KEGGID = row["#gene_id"], row["transcript_id"], row["gene_ontology_BLASTX"], row["gene_ontology_BLASTP"], row["gene_ontology_Pfam"], row["Kegg"]
    #if there is GOID acquired from 1 database, add to the GOs for this gene.
    if blastxGO != ".":
        GOs += blastxGO
    if blastpGO != ".":
        GOs += "`" + blastpGO
    if pfamGO != ".":
        GOs += "`" + blastpGO
    if GOs != "":
        allGOs = [GOcol.split("^")[0] for GOcol in GOs.split("`")]
        #remove redundant GOs
        uniqAllGOs = set(allGOs)
        for GOterm in uniqAllGOs:
            term2gene.append([GOterm, geneID])
            term2trans.append([GOterm, transcriptID])

    # get the KEGG ID and corresponding gene
    if KEGGID != ".":
        for KEGGcol in KEGGID.split("`"):
            if "KO:" in KEGGcol:
                KEGGID = KEGGcol.split("KO:")[-1]
                kegg2gene.append([KEGGID, geneID])
                kegg2trans.append([KEGGID, transcriptID])

    # This part of older version required preprocessing of the trinotate file, add KAAS result and genome annotated GOIDs
    # geneID, transcriptID, blastGO, pfamGO, KEGGID = row["#gene_id"], row["transcript_id"], row["gene_ontology_blast"], row["gene_ontology_pfam"], row["Kegg"]
    # #get the GO ID and corresponding gene
    # if blastGO != ".":
    #     for GOcol in blastGO.split("`"):
    #         GOterm, GOname = GOcol.split("^")[0], GOcol.split("^")[2]
    #         term2gene.append([GOterm, geneID])
    #         term2trans.append([GOterm, transcriptID])
    #         term2name.append([GOterm, GOname])
    # elif pfamGO !=".":
    #     for GOcol in pfamGO.split("`"):
    #         GOterm, GOname = GOcol.split("^")[0], GOcol.split("^")[2]
    #         term2gene.append([GOterm, geneID])
    #         term2trans.append([GOterm, transcriptID])
    #         term2name.append([GOterm, GOname])
    # else:
    #     continue
    # # get the KEGG ID and corresponding gene
    # if KEGGID != ".":
    #     for KEGGcol in KEGGID.split("`"):
    #         if "KO:" in KEGGcol:
    #             KEGGID = KEGGcol.split("KO:")[-1]
    #             kegg2gene.append([KEGGID, geneID])
    #             kegg2trans.append([KEGGID, transcriptID])
# # remove redundant gene-GO rows
# term2gene = set(map(tuple,term2gene))
# kegg2gene = set(map(tuple,kegg2gene))

with open("go2gene.csv", "w") as file:
    writer = csv.writer(file)
    for list in term2gene:
        writer.writerow(list)
with open("go2transcript.csv", "w") as file:
    writer = csv.writer(file)
    for list in term2trans:
        writer.writerow(list)
# with open("term2name.csv", "w") as file:
#     writer = csv.writer(file)
#     for list in term2name:
#         writer.writerow(list)
with open("kegg2gene.csv", "w") as file:
    writer = csv.writer(file)
    for list in kegg2gene:
        writer.writerow(list)
with open("kegg2trans.csv", "w") as file:
    writer = csv.writer(file)
    for list in kegg2trans:
        writer.writerow(list)