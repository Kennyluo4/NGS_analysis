#!/usr/bin/env python
"""read report.log files from mirdeep2.pl result"""
# import pandas,glob,sys,os,re
__author__ = "Kenny Luo"

def help():
    print("use: python mirdeep_res_handle.py [option]. \n"
          "Put result file in the same directory,\textract the mapping statistics of mirdeep2 result\n"
          "\t[option] -r or --rename: rename the files, replacing time tag by sample ID\n"
          "\t[option] -c or --count: summarize the read count of all known miRNA from quantifier module")

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

def main():
    renameOpt, readcount = get_argvs()
    IDpair, mapingstats = read_logfile()
    if renameOpt:
        renameFile(IDpair)
    if readcount:
        extractRawCount()
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
