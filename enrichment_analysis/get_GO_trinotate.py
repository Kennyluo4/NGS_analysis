#!/usr/bin/env python
import pandas as pd

df = pd.read_excel("Trinotate_test.xlsx")
# df.head()
print(f'File size: {df.shape}')
df = df[(df['gene_ontology_blast'] != '-') | (df['Kegg']!= '-')]           # remove rows without GO/KO annotation (either "na", "-" or "."), make processing big file faster 
print(f'File size after removing no-annotations: {df.shape}')

## work on GOs: split the GO colomn to make gene-go 1 to 1 relation by pandas.explode
# df_go = df.explode('GO')   
## in case delimiter is not ',' which explode doesn't recognize. split string within cell first
df = df.assign(GOs_full = df['gene_ontology_blast'].str.strip().str.split('GO:').str[1:]).explode('GOs_full')   # GOs_full: GO# ^ GO term
df = df.assign(GOs = df['GOs_full'].str.split('^').str[0]) # take the GO number to make a new column
df_go_sub = df[['GOs', '#gene_id']]    # take only GO and geneID
df_go_sub = df_go_sub[df_go_sub.GOs != '-'].drop_duplicates()    # remove '-' and duplicates
# df_go_sub.head()

## work on KOs:
df_ko = df.assign(KOs = df['Kegg'].str.strip().str.split('KO:').str[1]).explode('KOs')   # be caution about the output format, here each cell only has 1 KO term in my data
df_ko_sub = df_ko[['KOs', '#gene_id']]    # take only GO and geneID
df_ko_sub = df_ko_sub[df_ko_sub.KOs != '-'].drop_duplicates() 

## write files
df_go_sub.to_csv('go2gene.csv', index=False)
df_ko_sub.to_csv('kegg2gene.csv', index=False)



