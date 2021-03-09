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
geneGO = []
geneKO = []
for index, row in df.iterrows():
    #loop through each row based on their colnames
    GOs = ""
    geneID, transcriptID, blastxGO, blastpGO, pfamGO, KEGGID = row["#gene_id"], row["transcript_id"], row["gene_ontology_BLASTX"], row["gene_ontology_BLASTP"], row["gene_ontology_Pfam"], row["Kegg"]
    #if there is GOID acquired from 1 database, add to the GOs for this gene.
    #record the GeneID to avoid redundancy
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
            # term2gene.append([GOterm, geneID])
            term2trans.append([GOterm, transcriptID])
            generecord = geneID + GOterm
            if generecord not in geneGO:
                term2gene.append([GOterm, geneID])
                geneGO.append(generecord)
            else:
                continue

    # get the KEGG ID and corresponding gene
    if KEGGID != ".":
        for KEGGcol in KEGGID.split("`"):
            if "KO:" in KEGGcol:
                KEGGID = KEGGcol.split("KO:")[-1]
                # kegg2gene.append([KEGGID, geneID])
                generecord2 = geneID + KEGGID
                kegg2trans.append([KEGGID, transcriptID])
                if generecord2 not in geneKO:
                    kegg2gene.append([KEGGID, geneID])
                    geneKO.append(generecord2)
                else:
                    continue
# if KAAS mapped KO id is used, use following code instead to get KO
    # if KEGGID != ".":
    #     for KEGGcol in KEGGID.split("`"):
    #         if "KO:" in KEGGcol:
    #             KID = KEGGcol.split("KO:")[-1]
    #             KOs.append(KID)
    # if KAAS != ".":
    #     KOs.append(KAAS)
    # if len(KOs) != 0:
    #     uniqKO = set(KOs)
    #     for KOterm in uniqKO:
    #         kegg2gene.append([KOterm, geneID])
    #         kegg2trans.append([KOterm, transcriptID])

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