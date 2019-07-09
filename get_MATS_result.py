import glob
def help():
    print("usage: python get_MATS_result.py"
          "put *JC.txt and *JCEC.txt in the same directory with the script"
          "summary and integrate all the significant alternative splicing event (default Pvalue = 0.01) from MATS."
          "output result in MATS_JCEC_result.txt and MATS_JC_result.txt")



file_list1 = glob.glob("*JC.txt") #evaluates splicing with only reads that span splicing junctions
file_list2 = glob.glob("*JCEC.txt") #evaluates splicing with reads that span splicing junctions and reads on target

def result_filter(file, p_thredshold=0.01):
    print("The pvalue for selection is\t%s" % p_thredshold)
    res = []
    num = 0  #number of significant alternative splicing event
    genes = []
    AS_type = file.split('.')[0]     #read the alternative splicing type from the file title
    line_num = 1
    for lines in open(file):
        itms = lines.strip().split("\t")
        if line_num == 1:
            pvalue_index = itms.index('PValue')
        line_num += 1
        geneName, p_value = itms[2], itms[pvalue_index]
        try:
            p_value = float(p_value)
        except ValueError:
            res.append(lines)
            continue
        if p_value <= p_thredshold:
            res.append(AS_type +'\t' + lines)
            num += 1
            genes.append(geneName)
        else:
            continue
    genes = set(genes)
    num_gene_AS = len(genes)
    print("There are %d significantly %s splicing events in %d genes" % (num, AS_type, num_gene_AS))
    return res

if __name__ == '__main__' :
    help()
    final_res1 = []
    final_res2 = []
    for fs in file_list1:       #read JC.txt result files
        print("processing\t%s" % fs)
        res_f = result_filter(fs)
        final_res1 += res_f
    with open("MATS_JC_result.txt", "w") as handle:
        handle.writelines(final_res1)
    print("result with P-value<=0.01 from *JC.txt is in MATS_JC_result.txt")

    for fs in file_list2:       #read JCEC.txt result files
        print("Processing\t%s" % fs)
        res_f = result_filter(fs)
        final_res2 += res_f
    with open("MATS_JCEC_result.txt", "w") as handle:
        handle.writelines(final_res2)
    print("result with P-value<=0.01 from *JCEC.txt is in MATS_JCEC_result.txt")
