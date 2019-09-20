""""extract the GO id from the gff3 annotation file
    use: extractGOfromGFF.py filename.gff3
    only works if the GO ID were grouped in Onthology_term column"""""


import sys, csv
argvs = sys.argv
res = []
file = argvs[1]
# file = "arahy.Tifrunner.gnm1.ann1.CCJH.gene_models_main.gff3"
num = 0
go_num = 0
for lines in open(file):
    if lines.startswith("#"):
        continue

    anno, identifier = lines.split("\t")[8], lines.split("\t")[2]
    if identifier == "gene":
        num += 1
        go = [i.replace("Ontology_term=","") for i in anno.split(";") if i.startswith("Ontology_term")]
        if len(go) != 0:
            go_num += 1
        gene_name = anno.split(";")[1].replace("Name=", "")
        go.insert(0, gene_name)
        res.append(go)

print("gene number:%d, %d genes have GO id" % (num, go_num))
with open("ref_gene_GO.csv", "w") as file:
    writer = csv.writer(file)
    writer.writerow(["gene name", "GOs"])
    for list in res:
        writer.writerow(list)


