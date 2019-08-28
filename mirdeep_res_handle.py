#!/usr/bin/env python
"""read report.log files from mirdeep2.pl result"""

def help():
    print("use: python mirdeep_res_handle.py [option]. \n"
          "Put result file in the same directory,\textract the mapping statistics of mirdeep2 result\n"
          "\t[option] -r or --rename: rename the files, replacing time tag by sample ID")

def get_argvs():
    import sys, getopt
    rename = False
    try:
        opts, remainder = getopt.getopt(sys.argv[1:], "hr", ["help", "rename"])
    except:
        help()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            help()
            sys.exit()
        elif opt in ("-r", "--rename"):
            rename = True
    return rename

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

def main():
    renameOpt = get_argvs()
    IDpair, mapingstats = read_logfile()
    if renameOpt:
        renameFile(IDpair)
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
