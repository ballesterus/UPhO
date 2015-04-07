#!/usr/bin/env python

import argparse
import re
from sys import argv

parser = argparse.ArgumentParser(description='This is scriopt returns alignments ready for Phylogenetic analyses, no duplicate sequence identifieer and no taxon duplication, in which case the longest sequence is retained ')

parser.add_argument('-f', dest = 'targets', type = str, nargs= '+',  help = 'files to process(fasta alignment)')  

arguments= parser.parse_args()
print arguments

def is_ID(Line):
    """Evaluates if a string correspond to fasta identifier. herein broadly defined by starting with th e '>' symbol"""
    if Line.startswith('>'):
        return True
    else:
        return False
                
def Fasta_Parser_keepLongest(File):
    """This function returns a dictionary containing FastaId(key) and Seqs"""
    Records = {}
    with open(File, 'r') as F:
        Seq=''
        for Line in F:
            if is_ID(Line) and len(Seq) == 0:
                Header =Line.replace('\n', '').strip('>')
                Sp = Header.split('|')[0]
                Records[Sp]=''
            elif is_ID(Line) and len(Seq) > 0:
                if Sp in Records.keys() and len(Seq) <= len(Records[Sp]):
                    Records[Sp]=Records[sp]
                    Header =Line.replace('\n', '').strip('>')
                    Sp = Header.split('|')[0]
                    Records[Sp]=''
                else:
                    Records[Sp]=Seq
                    Header =Line.replace('\n', '').strip('>')
                    Sp = Header.split('|')[0]
                    Records[Sp]=''
            else:
                Part=Line.replace('\n','')
                Seq = Seq + Part
        if Sp in Records.keys() and len(Seq) > len(Records[Sp]):
            Records[Sp]=Seq
    return Records
    F.close()


#####SHOWTIME######
if len(argv) >= 3:
    for File in  arguments.targets:
        F = Fasta_Parser_keepLongest(File)
        #print F.keys()
        FileName= File.split('.')
        OutName = FileName[0] + '_ready.' + FileName[1] 
        Out = open(OutName, 'w')
        for Rec in F.iterkeys():
            Out.write('>%s\n' % Rec)
            Out.write(F[Rec] + '\n')
        Out.close()



