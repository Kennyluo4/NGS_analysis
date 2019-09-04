#!/usr/bin/env python
"""read report.log files from mirdeep2.pl result"""
# import pandas,glob,sys,os,re
__author__ = "Kenny Luo"

def help():
    print("use: python mirdeep_res_handle.py [option]. \n"
          "Put result file in the same directory,\textract the mapping statistics of mirdeep2 result\n"
          "\t[option] -r or --rename: rename the files, replacing time tag by sample ID\n"
          "\t[option] -c or --count: summarize the read count of all known miRNA from quantifier module and novel/known mirna count from mirdeep2 module")

def get_argvs():
    import sys, getopt
    rename = False
    countread = False
    try:
        opts, remainder = getopt.getopt(sys.argv[1:], "hrc", ["help", "rename", "count"])
    except:
        help()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            help()
            sys.exit()
        elif opt in ("-r", "--rename"):
            rename = True
        elif opt in ("-c", "--count"):
            countread = True
    return rename, countread

def read_logfile():
    """matching time tag with sampleID
        retrieve mapping statistics on known miRNA"""
    import glob, re
    logfiles = glob.glob("*_report.log")
    IDdic = {} #collect the time tag by mirdeep and connect it to sample ID
    res = ["sample#	total	mapped	unmapped	%mapped	%unmapped\n"] #collect the Mapping statistics to known miRNA/precursor
    for filename in logfiles:
        sampleID = filename.split("_")[0]
        for lines in open(filename):
            if lines.startswith("mkdir mirdeep_runs"):    #identify the line containing time tag
                timeID = lines.strip().split("/")[1].replace("run_", "")
                IDdic[timeID] = sampleID
            if re.match("total\: \d*\t", lines): #identify the line with mapping statistic
                stats = lines.replace("total", sampleID)
                res.append(stats)
    return IDdic, res

def renameFile(IDdictionary): #IDditionanry is dic of {"current Tag": "Sample ID"}
    """rename files in current directory based on input ID dictionary"""
    import os
    pwd = os.getcwd()
    print("Rename files in:" + pwd)
    fileNames = os.listdir(pwd)
    for files in fileNames:
        for key, value in IDdictionary.items():
            if key in files:
                newFileName = files.replace(key, value)
                os.rename(files, newFileName)
            elif value in files:
                print("sample ID alread added to %s" % files)
                continue

def extractRawCount():
    """read read count file for known miRNA then merge the total read count for each sample"""
    import glob
    import pandas as pd
    res = pd.DataFrame()
    countFiles = glob.glob("miRNAs_expressed_all_samples*.csv")
    # f_num = 0
    file_dic = {}
    for f in countFiles:
        sampleID = f.replace("miRNAs_expressed_all_samples_", "").replace(".csv", "")
        file_dic[f] = pd.read_csv(f, '\t')   #read each file as dataframe by pandas
        # file_dic["f%d" % f_num].rename(columns = {"read_count":sampleID+"_reads"})
        if "#miRNA" not in res.columns:
            res["#miRNA"] = file_dic[f]["#miRNA"]
        res[sampleID+"_ReadCount"] = file_dic[f]["read_count"]
    res.to_csv("known_miRNA_reads_count_all.csv")
    print("raw read counts of all samples write to known_miRNA_reads_count_all.csv")

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
                if "TRUE" in row or "STAR" in row:  #for known miRNA
                    mirna = row[10] #+ ":" + row[14]
                    if mirna not in mirnalist:      #add mirna ID to total mirna id list for all sample
                      mirnalist.append(mirna)
                    if mirna not in temp_res.keys():  # add mirna count to each mirna
                        temp_res[mirna] = [int(row[6])]
                    else:
                        temp_res[mirna].append(int(row[6]))
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
            temp_res[k] = statistics.mean(v)     # calculate the mean count for each miRNA
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
        print("read counts of mirdeep2 predicted mirna write to mirdeep2_identified_mirna_count.csv")

def main():
    renameOpt, readcount = get_argvs()
    IDpair, mapingstats = read_logfile()
    if renameOpt:
        renameFile(IDpair)
    if readcount:
        extractRawCount()
        read_result_file()
    with open("mapping_stat.txt", "w") as file:
        file.writelines(mapingstats)


if __name__ == "__main__":
    main()
    # renameOpt = get_argvs()
    # IDpair, mapingstats = read_logfile()
    # if renameOpt:
    #     renameFile(IDpair)
    # with open("mapping_stat.txt", "w") as file:
    #     file.writelines(mapingstats)
