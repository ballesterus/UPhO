#!/usr/bin/env python

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

def Fasta_to_Dict(File):
    '''BETTER FASTA PARSER'''
    with open(File, 'r') as F:
        Records = {}
        for Line in F:
            if Line.startswith('>'):
                Seqid = Line.strip('>').strip('\n')
                Seq= ''
                Records[Seqid] = Seq
            else:
                Seq = Records[Seqid] + Line.strip('\n')
                Records[Seqid] = Seq 
        return Records

def make_Consensus(Dict, T):
    '''This functiom returns the sites where all the aligemnet positions match on the same nucleotide. this is a T% consensus'''
    Consensus=''
    for i in range(0, len(Dict[Dict.keys()[0]])):
        compo = []
        for seq in Dict.itervalues():
            site = seq[i]
            compo.append(site)
        N = len(compo)
        G = 0 
        MFB = ''
        for base in set(compo):
            freq = compo.count(base)
            if freq > G:
                G = freq
                MFB = base
        if float(G)/N >= T:
            Consensus+=MFB
        else:
            Consensus+='N'
    return Consensus

def Good_Blocks(Consensus, M):
    '''This funcion takes as inputs a consensus sequence and returns blocks of M contibuos base pairs in that consensus (Conserved sites of  a given length)'''
    GoodBlocks =''
    block = ''
    for site in Consensus:
        if site not in  ['-','N']:
            block+=site
        elif site in ['-','N' ] and len(block)>0:
            if len(block) >= M:
                GoodBlocks += block.upper() + site
                block = ''
            else:
                GoodBlocks += block.lower() + site
                block = ''
        else:
            GoodBlocks += site
            block = ''
    GoodBlocks+=block.lower()
    return GoodBlocks

###MAIN###
if arguments.targets != None:
    Out =open('Output.fasta', 'w')
    for File in  arguments.targets[0]:
        F = Fasta_Parser(File)
        FileName= File.split('.')
        Con = make_Consensus(F, T)
#        print Con
        Res = Good_Blocks(Con, M) 
#        print Res
        if re.search(r'[ACGT]+', Res):
            print 'Consensus from orthogroup %s have conserevd regions' % FileName[0]
            Out.write('>' + FileName[0] + '\n')
            Out.write(Res + '\n')
        else:
            print 'Consensus from orthogroup %s does not look promissing' % FileName[0]
    Out.close()
