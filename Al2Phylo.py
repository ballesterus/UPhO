#!/usr/bin/env python

import argparse
import re
from sys import argv

parser = argparse.ArgumentParser(description='This  script returns alignments/sequences for phylogenetic analyses, no duplicate sequence identifieer and no taxon duplication, in which case the longest sequence is retained ')

parser.add_argument('-f', dest = 'targets', type = str, nargs= '+',  help = 'files to process(fasta alignment)')  

arguments= parser.parse_args()
print arguments


def is_ID(Line):
    """Evaluates if a string correspond to fasta identifier. herein broadly defined by starting with th e '>' symbol"""
    if Line.startswith('>'):
        return True
    else:
        return False
                
def Fasta_Parser_keep_longest(File):
    """This function returns a dictionary containing FastaId(key) and Seqs"""
    Records = {}
    with open(File, 'r') as F:
        Seq=''
        for Line in F:
            if is_ID(Line) and len(Seq) == 0:
                Header =Line.replace('\n', '').strip('>')
                Sp = Header.split('|')[0]
                Records[Sp]=[]
            elif is_ID(Line) and len(Seq) > 0:
                Records[Sp].append(Seq)
                Header =Line.replace('\n', '').strip('>')
                Sp = Header.split('|')[0]
                if Sp not in Records.keys():
                    Records[Sp]=[]
                Seq=''
            else:
                Part=Line.replace('\n','')
                Seq = Seq + Part
        Records[Sp].append(Seq) #get the very last seq
    F.close()
    for Sp in Records.iterkeys():
        #print [len(i) for i in Records[Sp]]
        Records[Sp] = max(Records[Sp], key=len)
        #print len(Records[Sp])
    return Records
    

#####SHOWTIME######
if len(argv) >= 3:
    for File in  arguments.targets:
        F = Fasta_Parser_keep_longest(File)
        #print F.keys()
        FileName= File.split('.')
        OutName = FileName[0] + '_ready.' + FileName[1] 
        Out = open(OutName, 'w')
        for Rec in F.iterkeys():
            Out.write('>%s\n' % Rec)
            Out.write(F[Rec] + '\n')
        Out.close()



