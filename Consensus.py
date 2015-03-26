#!/usr/bin/env python
import os
from sys import argv

Script=argv[0] 
Codon=argv[1]
argv.remove(Script)
argv.remove(Codon)
Targets=argv



NT=['A','C','G','T']
AA =['A','B','C','D','E','F','G','H','I','K','L','M','N','P','Q','R','S','T','U','V','W','Y','Z']

##FUNCTION DEFINITIONS


def Is_NT_or_AA(String):
    ''' Returns True  is the sequence is composed of Nucleotide symbols'''
    NT= ('A','C','G','T','U','R','Y','K','M','S','W','B','D','H','V','N')
    AA =('A','B','C','D','E','F','G','H','I','K','L','M','N','P','Q','R','S','T','U','V','W','Y','Z','X')
    Comp = set(String)
    if all([i in NT for i in Comp]):
        return 'NT'
    elif all([i in AA for i in Comp]):
        return 'AA'
    else:
        return 'UNKNOW'
    

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



def make_Consenus(Dict):
    '''This functiom returns the sites where all the aligemnet positions match on the same nucleotide. this is a 100% consensus'''
    for i in range(0, len(Dict[Dict.keys()[0]])):
        Compo = {}
        for seq in Dict.itervalues():
            site = seq[i]
            if site  not in Compo:
                Compo[site]=1
            else:
                Compo[site]+=1
        print Compo
    




    for record in Records_Dict:
        Consensus = ''
        mySeq=Records_Dict[record]
        NSeq=''
        if len(Consensus)==0:
            Consensus = mySeq
        elif len(Consensus)==len(mySeq):
            for i in range(0, len(mySeq)):
                if mySeq[i] =='-' and Consensus[i] in NT:
                    NSeq +=Consensus[i]
                elif mySeq[i] in NT  and Consensus[i] == mySeq[i]:
                    NSeq+=Consensus[i]
                else:
                    NSeq+='-'
            Consensus = NSeq
        else:
            print "ERROR this seqences are not alignend!"
            break
    return Consensus



def Good_Blocks(Consensus):
    GoodBlocks =[]
    Blocks = re.split('-+', Consensus)
    for Block in Blocks:
        if len(Block) >= 18:
            GoodBlocks.append(Block)


            
