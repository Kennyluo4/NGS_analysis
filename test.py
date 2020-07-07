#!/usr/bin/env python

### read each file
    # create dictionary for one mature miRNA, set value as list(multiple read count from different location)
    # after reading the file, caulculate the average read count for one mature mirna
    # output dictionary with dic[mirna_seq] = average_count
# file = open("result_S6123.csv")
# f_reader = csv.reader(f,delimiter = "\t")
# for row in f_reader:
#     if "estimated probability that the miRNA candidate is a true positive" in row:
#         print(row)

def read_result_file():
    res = []
    mirnalist = []
    file_dic = {}
    import glob, csv, statistics
    fs = glob.glob("result*.csv")
    for f in fs:
        sampleID = f.replace("result_","").replace(".csv", "")
        file = open(f)
        f_reader = csv.reader(file, delimiter = "\t" ) #the result.csv file from mirDeep2 actually uses "\t" as delimiter instead of ","
        temp_res = {} #for storing mirna result for one sample/file
        for row in f_reader:
            if len(row) != 0 and row[0].startswith("arahy"):   #the mirdeep2 identified mature and novel mirna start with a tag ID of chromosome + number
                if any("ahy-" in col for col in row):  #for known miRNA
                    mirna = row[9] #+ ":" + row[14]
                    if mirna not in mirnalist:      #add mirna ID to total mirna id list for all sample
                      mirnalist.append(mirna)
                    if mirna not in temp_res.keys():  # add mirna count to each mirna
                        temp_res[mirna] = [int(row[5])]
                    else:
                        temp_res[mirna].append(int(row[5]))
                else:     #for novel miRNA
                    if row[10] == "-":
                        mirna = row[13]      # use sequence as ID
                        if mirna not in mirnalist:
                            if len([m for m in mirnalist if mirna[1:-1] in m]) == 0:#trim first 1 and last NT to avoid novel mirna variant between different samples
                                mirnalist.append(mirna)    #add to mirnalist if there is not variant
                            else:    #if the trimmed sequencing is already in there, used that one as the mirna ID
                                mirna = str([m for m in mirnalist if mirna[1:-1] in m][0])
                    else:
                        mirna = row[10]      # use ortholog miRNA in other specie  as ID
                        if mirna not in mirnalist:  # add mirna ID to total mirna id list for all sample
                            mirnalist.append(mirna)
                    if mirna not in temp_res.keys():    #add mirna count to each mirna
                        temp_res[mirna] = [int(row[5])]  # list of mature counts as value
                    else:
                        temp_res[mirna].append(int(row[5]))  # add to list for mirna in different location
            else:
                continue
        # get the sample ID, dic[novel RNA] = [count1, count2]
        for k, v in temp_res.items():
            temp_res[k] = int(statistics.mean(v))     # calculate the mean count for each miRNA
        file_dic[sampleID] = temp_res
    header = ["mirna"]
    for rna in mirnalist:
        oneline = []
        oneline.append(rna)
        for sample, mirnadic in file_dic.items():
            if sample not in header:
                header.append(sample)
            if rna in mirnadic.keys():
                oneline.append(mirnadic[rna])
            else:
                oneline.append('NA')
        res.append(oneline)

    with open('mirdeep2_identified_mirna_count.csv', 'w') as file:
        file_writer = csv.writer(file)
        file_writer.writerow(header)
        for row in res:
            file_writer.writerow(row)


print("teting")
read_result_file()

