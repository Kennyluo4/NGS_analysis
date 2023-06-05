#!/usr/bin/env python
import csv
res = []
row = []
f = open('go.obo')

for lines in f:
    if lines.startswith("id: GO:"):
        GO = lines.strip().replace("id: ", "")
        row = [GO]
    elif lines.startswith("name:"):
        name = lines.strip().replace("name: ", "")
        row.append(name)
    elif lines.startswith("namespace: "):
        cls = lines.strip().replace("namespace: ", "")
        row.append(cls)
        res.append(row)

with open("GO2term.csv", "w") as file:
    writer = csv.writer(file)
    writer.writerow(["GO", "name", "class"])
    for ln in res:
        writer.writerow(ln)


