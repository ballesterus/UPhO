#!/usr/bin/env python
"""USAGE: python Consensus.py -t 0.5 -m 20 -f *.al """


import argparse
import re

parser = argparse.ArgumentParser(description='This is a program, to write consensus sequences')

parser.add_argument('-t', action= 'store', dest = 'T', default = 1.0, type = float,  help='Specify frequency threshold' ) 
parser.add_argument('-m', action = 'store', dest = 'M', default = 18, type = int, help='minimum lenght of good conserved regions' )
parser.add_argument('-f', action = 'append', dest = 'targets',  help = 'files to process(fasta alignment)')  

arguments= parser.parse_args()
print arguments
T = arguments.T
M = arguments.M
Files = arguments.targets

def is_ID(Line):
    """Evaluates if a string correspond to fasta identifier. herein broadly defined by starting with th e '>' symbol"""
    if Line.startswith('>'):
        return True
    else:
        return False

                
def Fasta_Parser(File):
    """This function returns a dictionary containing FastaId(key) and Seqs"""
    Records = {}
    with open(File, 'r') as F:
        Seq=''
        for Line in F:
            if is_ID(Line) and len(Seq) == 0:
                Header =Line.replace('\n', '').strip('>')
            elif is_ID(Line) and len(Seq) > 0:
                Records[Header]=Seq
                Header =Line.replace('\n', '').strip('>')
                Seq = ''
            else:
                Part=Line.replace('\n','')
                Seq = Seq + Part
        Records[Header]=Seq
    return Records
    F.close()



def make_Consensus(Dict, T):
    '''This functiom returns the sites where all the aligemnet positions match on the same nucleotide. this is a 100% consensus'''
    Consensus=''
    for i in range(0, len(Dict[Dict.keys()[0]])):
        compo = []
        for seq in Dict.itervalues():
            site = seq[i]
            if site != '-':
                compo.append(site)
        N = len(compo)
        G = 0 
        MFB = ''
        for base in set(compo):
            freq = compo.count(base)
            if freq > G:
                G = freq
                MFB = base
        if G/N >= T:
            Consensus+=MFB
        else:
            
            Consensus+='-'
    return Consensus


def Good_Blocks(Consensus, M):
    GoodBlocks =[]
    Blocks = re.split('-+', Consensus)
    for Block in Blocks:
        if len(Block) >= M:
            GoodBlocks.append(Block)

    return GoodBlocks


#####SHOWTIME######

for File in Files:
    F = Fasta_Parser(File)
    FileName= File.split('.')
    Out =open('Output.fasta', 'wb+')
    Con = make_Consensus(F, T)
    Out.write('>' + FileName[0] + '\n')
    Out.write(Con)
        



