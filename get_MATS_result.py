import glob, os, sys
import pandas as pd
import numpy as np
from datetime import date

def help():
    print("usage: python get_MATS_result.py <rmats_result_folder>\n"
          "default is current directory\n"
          "summary and integrate all the significant alternative splicing event (default Pvalue = 0.05) from MATS.\n"
          "output result in MATS_JCEC_result.txt and MATS_JC_result.txt")

def result_filter(file, p_thredshold=0.05):
    # res = []
    # num = 0  #number of significant alternative splicing event
    # genes = []
    AS_type = file.split('.')[0]     #read the alternative splicing type from the file title
    # line_num = 1
    df = pd.read_table(file)
    sig_df = df[df['FDR']<=0.05]
    sig_df['AS_type'] = AS_type
    # for lines in open(file):
    #     itms = lines.strip().split("\t")
    #     if line_num == 1:
    #         adjp_index = itms.index('FDR')
    #     line_num += 1
    #     geneName, p_value = itms[2], itms[adjp_index]
    #     try:
    #         p_value = float(p_value)
    #     except ValueError:
    #         res.append("AStype\t" + lines)
    #         continue
    #     if p_value <= p_thredshold:
    #         res.append(AS_type +'\t' + lines)
    #         num += 1
    #         genes.append(geneName)
    #     else:
    #         continue
    # genes = set(genes)
    # num_gene_AS = len(genes)
    num_AS = sig_df.shape[0]
    num_gene = len(sig_df.GeneID.value_counts())
    print("There are %d significantly %s splicing events in %d genes\n" % (num_AS, AS_type, num_gene))
    return sig_df

def main():
    argvs = sys.argv
    try:
        cpath = argvs[1].replace('/', '')
        print('Input result folder is %s' % cpath)
    except IndexError:
        help()
        exit()
    os.chdir(cpath)
    file_list1 = glob.glob('*MATS.JC.txt')
    file_list2 = glob.glob('*MATS.JCEC.txt')
    final_res1 = []
    final_res2 = []
    for fs in file_list1:       #read JC.txt result files
        print("Processing\t%s" % fs)
        res_f = result_filter(fs)
        final_res1.append(res_f) 
    res1 = pd.concat(final_res1)
    # with open("MATS_JC_result.txt", "w") as handle:
    #     handle.writelines(final_res1)
    # print("***result with P-value<=0.05 from *JC.txt is in MATS_JC_result.txt***")

    for fs2 in file_list2:       #read JCEC.txt result files
        print("Processing\t%s" % fs2)
        res_f2 = result_filter(fs2)
        final_res2.append(res_f2) 
    res2 = pd.concat(final_res2)

    #move AS type to first column
    ID1 = res1.pop('AS_type')
    res1.insert(0, 'AS_type', ID1)
    ID2 = res2.pop('AS_type')
    res2.insert(0, 'AS_type', ID2)

    #write to excel file
    today = str(date.today())
    if cpath == '.':
        filename = ''.join(['rMATS_summary_',today,'.xlsx'])
    else:
        filename = ''.join([cpath, 'rMATS_summary_',today,'.xlsx'])
    writer = pd.ExcelWriter(filename,engine='xlsxwriter')
    res1.to_excel(writer, sheet_name='JC', index=False)
    res2.to_excel(writer, sheet_name='JCEC', index=False)
    writer.save()
    # with open("MATS_JCEC_result.txt", "w") as handle:
    #     handle.writelines(final_res2)
    # print("***result with P-value<=0.01 from *JCEC.txt is in MATS_JCEC_result.txt***")

if __name__ == '__main__' :
    main()