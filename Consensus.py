#!/usr/bin/env python

import argparse
import re
from sys import argv


#Globals

NT= ('A','C','G','T','U','R','Y','K','M','S','W','B','D','H','V','N', '-', '?')
AA =('A','B','C','D','E','F','G','H','I','K','L','M','N','P','Q','R','S','T','U','V','W','Y','Z','X', '-', '*', '?')

#dictionary of ambiguity:
Ambigs = {
    'A': ['A'],
    'G': ['G'],
    'C': ['C'],
    'T': ['T'],  
    'M': [ 'A', 'C'],
    'R': [ 'A', 'G'], 
    'W': [ 'A', 'T'], 
    'S': [ 'C', 'G'], 
    'Y': [ 'C', 'T'], 
    'K': [ 'G', 'T'],
    'V': [ 'A', 'C', 'G'], 
    'H': [ 'A', 'C', 'T'], 
    'D': [ 'A', 'G', 'T'], 
    'B': [ 'C', 'G', 'T'], 
    'N': [ 'G', 'A', 'T', 'C'] 
}

###############


def string_type(string):
    if  all (i in NT for i in list(string)):
        return 'NT'
    elif  all (i in AA for i in list(string)):
        return 'AA'
    else:
        return 'ERROR: NOT AA or NT'

def Is_NT_or_AA(Fasta_Dict):
    ''' Returns NT is the sequence is composed of Nucleotide symbols or AA if symbols are aminoacids'''
    if all(string_type(Fasta_Dict[key]) == 'NT' for key in Fasta_Dict.iterkeys()):
        return 'NT'
    elif all(string_type(Fasta_Dict[key]) == 'AA' for key in Fasta_Dict.iterkeys()):
        return 'AA'
    else:
        for k in Fasta_Dict.iterkeys():
            for i in Fasta_Dict[k]:
                if i not in AA:
                    print i
                    
def return_amb(list_of_nuc):
    """Returns a  one letter ambiguity code form a list of nucleotides. """
    nts=[Ambigs[x] for x in list_of_nuc]
    nts=[u for x in nts for u in x]
    for code in Ambigs.iterkeys():
        if set(Ambigs[code]) == set(nts):
            return code

def is_ID(Line):
    """Evaluates if a string correspond to fasta identifier. Herein broadly defined by starting with th e '>' symbol"""
    if Line.startswith('>'):
        return True
    else:
        return False
                
def Fasta_to_Dict(File):
    '''Creates a dictionary of FASTA sequences in a File, with seqIs as key to the sequences.'''
    with open(File, 'r') as F:
        Records = {}
        Seqid='null'
        Records['null']=''
        for Line in F:
            if Line.startswith('>'):
                Seqid = Line.strip('>').strip('\n')
                Seq= ''
                Records[Seqid] = Seq
            else:
                Seq = Records[Seqid] + Line.strip('\n')
                Records[Seqid] = Seq.upper()
        del Records['null']
        return Records

def make_Consensus(Dict, T):
    '''This functiom returns the sites where all the aligemnet positions match on the same nucleotide. this is a T% consensus, for AA seqs, the most common aminoacid equal or greater than the threshold will be used, and ambiguities replaced by  "?" '''
    Type = Is_NT_or_AA(Dict)
    ignore=['-', '?']
    Consensus=''
    for i in range(0, len(Dict[Dict.keys()[0]])):
        compo = [seq[i] for seq in Dict.itervalues()]
        compo = [x for x in compo if x not in ignore]
        if  len(compo) < 1:
            Consensus+='-'
        else:
            MFB = max(set(compo), key=compo.count)
            G = compo.count(MFB)
            if float(G)/len(compo) >= T:
                Consensus+=MFB
            elif Type == 'NT':
                AmbC = return_amb(compo)
                Consensus+=str(AmbC)
            else:
                Consensus += 'X'
    return Consensus

def Good_Blocks(Consensus, M):
    '''This funcion takes as inputs a consensus sequence and returns blocks of M contiguous base pairs in that consensus (Conserved sites of  a given length)'''
    GoodBlocks =''
    block = ''
    for site in Consensus:
        if site not in  ['-','N', '?']:
            block+=site
        elif site in ['-','N', '?' ] and len(block)>0:
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
if __name__ =='__main__': 
    parser = argparse.ArgumentParser(description='This is a program to write consensus sequences')
    parser.add_argument('-i', dest = 'alignments', type = str, nargs= '+', help = 'Input alignment(s) in FASTA format.')
    parser.add_argument('-t', action= 'store', dest = 'percentage', default = 1.0, type = float,  help='Specify percentage threshold to make consensus, default 1.0' )
    parser.add_argument('-B', action = 'store', dest = 'blocks', default = 0, type = int, help='look for conserved regions in the alignement (blocks) of the minimum size provided')
    parser.add_argument('-d', dest = 'delimiter', type = str, default = '|', help = 'Specify custom field delimiter character separating species name from other sequence identifiers. Species name should be the first element for proper parsing. Default is: "|".')
    arguments= parser.parse_args()

    #print arguments
    T = arguments.percentage
    M = arguments.blocks
    D = arguments.delimiter
    for File in arguments.alignments:
        F = Fasta_to_Dict(File)
        Con = make_Consensus(F, T)
        with open ("%s_consensus.fasta" % File.split('.')[0], 'w') as out:
            out.write('>%s consensus sequence\n%s\n' % (File, Con)) 
            if M > 0:
                Out = open ('Good_Blocks.fasta', 'w')
                Res = Good_Blocks(Con, M)
                if re.search(r'[ACGT]+', Res):
                    print 'Consensus from orthogroup %s have conserevd regions' % FileName[0]
                    Out.write('>' + FileName[0] + '\n')
                    Out.write(Res + '\n')
                else:
                    print 'Consensus from orthogroup %s does not look promissing' % FileName[0]
                    Out.close()
