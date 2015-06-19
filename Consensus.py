#!/usr/bin/env python

"""USAGE: python Consensus.py -t 0.5 -m 20 -f *.al """

import argparse
import re
from sys import argv
parser = argparse.ArgumentParser(description='This is a program, to write consensus sequences')

parser.add_argument('-t', action= 'store', dest = 'T', default = 1.0, type = float,  help='Specify frequency threshold' ) 
parser.add_argument('-m', action = 'store', dest = 'M', default = 18, type = int, help='minimum lenght of good conserved regions' )
parser.add_argument('-f', action = 'append', dest = 'targets', type = str, nargs= '*',  default = None,  help = 'files to process(fasta alignment)')  

arguments= parser.parse_args()
print arguments
T = arguments.T
M = arguments.M


def is_ID(Line):
    """Evaluates if a string correspond to fasta identifier. Herein broadly defined by starting with th e '>' symbol"""
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
    '''This functiom returns the sites where all the aligemnet positions match on the same nucleotide. this is a T% consensus'''
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
    '''Rhis funcion takes as inputs a consensus sequence and returns blocks of M contibuos base pairs in that consensus (Conserved sites of  a given length)'''
    GoodBlocks =''
    block = ''
    for site in Consensus:
        if site !='-':
            block+=site
        elif site =='-' and len(block)>0:
            if len(block) >= M:
                GoodBlocks += block + '-'
                block = ''
            else:
                GoodBlocks += len(block) * '-' + '-'
                block = ''
        else:
            GoodBlocks += '-'   
    GoodBlocks+=block
    return GoodBlocks

###SHOWTIME###
if arguments.targets != None:
    for File in  arguments.targets[0]:
        F = Fasta_Parser(File)
        FileName= File.split('.')
        Out =open('Output.fasta', 'a')
        Con = make_Consensus(F, T)
        Res = Good_Blocks(Con, M) 
        Out.write('>' + FileName[0] + '\n')
        Out.write(Res + '\n')
    Out.close()
