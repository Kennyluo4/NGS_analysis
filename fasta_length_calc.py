##usage:   python count_fa.py input.fa>length.txt
##  recommend use nohup conmandline&

#!/usr/bin/python
import sys,os,re


def process_file(reader):
    '''Open, read,and print a file'''
    names = []
    index = 0
    dict = {}
    for line in reader:
        if line.startswith('>'):
           if index >=1:    ##### read the seuqnce name
               names.append(line)
           index =index+1
           name=line[:-1]
           seq = ''
        else:
           seq += line[:-1]
           dict[name]=seq         ######create library{sequence name: sequence}
    return dict


if __name__ == "__main__":
    input_file = open(sys.argv[1], "r")
    reader = input_file.readlines()
    items = process_file(reader)
    for key in items:
        length = int(len(items[key]))
        print("%s\t%d" % (key, length))
    input_file.close()
