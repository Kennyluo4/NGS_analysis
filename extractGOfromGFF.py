""""extract the GO id from the gff3 annotation file
    use: extractGOfromGFF.py filename.gff3"""""


import sys, csv
argvs = sys.argv
res = []
file = argvs[1]

for lines in open(file):
    if lines.startswith("#"):
        continue
    elif "marker\tgene\t" in lines:
        anno = lines.split("\t")[8]
        go = [i.replace("Ontology_term=","") for i in anno.split(";") if i.startswith("Ontology_term")]
        gene_name = anno.split(";")[1]
        go.insert(0, gene_name)
        res.append(go)

with open("ref_gene_GO.csv", "w") as file:
    writer = csv.writer(file)
    writer.writerow(["gene name", "GOs"])
    for list in res:
        writer.writerow(list)


