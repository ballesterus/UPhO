#!/usr/bin/env python

import argparse
import re
from sys import argv

parser = argparse.ArgumentParser(description='This  script returns alignments/sequences for phylogenetic analyses, no duplicate sequence identifieer and no taxon duplication, in which case the longest sequence is retained. Additionally performs a basic sanitation of this alignments, removing ambiguous sequences from the alignemnet. A sequences is considered ambiguous when it shows less than N sites  unaumbiguous.')

parser.add_argument('-in', dest = 'input)', type = str, nargs= '+',  help = 'Files to process(fasta alignment)')  
parser.add_argument('-m', dest = 'minalnL', type = int, default= '0',  help = 'Minimun alignemnet lenght.') 
parser.add_argument('-d', dest = 'delimiter', type = str, default= '|',  help = 'Custom character separating fields of sequence identifier.')
parser.add_argument('-r', dest ='representative', action='store_true', default = False, help ='When the flag is present, one representative sequence per species(the longets) retained in the alignement ')
args= parser.parse_args()
print arguments

def is_ID(Line):
    """Evaluates if a string correspond to fasta identifier. herein broadly defined by starting with th e '>' symbol"""
    if Line.startswith('>'):
        return True
    else:
        return False
    
def seq_leng_nogaps(Str):
    """Returns the lenght of a sequence without conting and ambiguous positions"""
    return len(Str.replace('-', ''))
    
def Fasta_Parser(File):
    """This function returns a dictionary containing FastaId(key) and Seqs"""
    Records = {}
    with open(File, 'r') as F:
        Seq=''
        for Line in F:
            if is_ID(Line) and len(Seq) == 0:
                seqid =Line.replace('\n', '').strip('>')
                Records[seqid]=[]
            elif is_ID(Line) and len(Seq) > 0:
                Records[Sp].append(Seq)
                seqid =Line.replace('\n', '').strip('>')
                if seqid not in Records.keys():
                    Records[seqid]=[]
                Seq=''
            else:
                Part=Line.replace('\n','')
                Seq = Seq + Part
        Records[seqid].append(Seq) #get the very last seq
    F.close()

def OneOTU(SppDict):
    role=[]
    for oldkey in SppDict.iterkeys():
        newkey = oldkey.split(delimiter)[0]
        if newkey not in role:
            role.append(newkey)
            SppDict[newkey] = SppDict[oldkey]
            del SppDict[oldkey]
        else:
            Longest = max(SppDict[oldkey], SppDict[newkey], key=seq_leng_nogaps) 
            SppDict[newkey] = Longest
            del SppDict[oldkey]
    return SppDict

def is_Alignment(Arg):
    """Return True or False after evaluating that the length of all sequences in the input file are the same length. inputs are either file names, or Fasta_record objects."""
    if type(Arg) != dict:
        Arg=Fasta_Parser(Arg)
        Ref = Arg.keys()[0]
        Len= Arg[Ref].SeqLen # obtain a reference from the 1st dict entry.                   
        if all(Len == Arg[key].SeqLen for key in Arg.iterkeys()):
            return True
        else:
            for key in Arg.iterkeys():
                print Arg[key].SeqId
                print Arg[key].SeqLen
            return False
    else:
        Ref = Arg.keys()[0]
        Len= Arg[Ref].SeqLen # obtain a reference from the 1st dict entry.                                           
        if all(Len == Arg[key].SeqLen for key in Arg.iterkeys()):
            return True
        else:
            for key in Arg.iterkeys():
                print Arg[key].SeqId
                print Arg[key].SeqLen
            return False
        
def Sanitize_aln(Dict):
    for otu in Dict.iterkeys():
        if seq_leng_nogaps(Dic[otu]) < args.minAln:
            print "Sequence %s will be removed from alignement."
            delete Dict[otu]
    return Dict   

######MAIN######
if __name__ == "__main__":
    for File in  arguments.input:
        F = Fasta_Parser(File)
        #print F.keys()
        FileName= File.split('.')
        OutName = FileName[0] + '_ready.' + FileName[1] 
        Out = open(OutName, 'w')
        print 'Sanitizing alignment %s by removing sequences with less than %n ' % FileName
        F = Sanitize_aln(F)
        if args.representative:
            '''Selecting one representative sequence per species'''
            F =OneOTU(F)        
        for Rec in F.iterkeys():
            Out.write('>%s\n' % Rec)
            Out.write(F[Rec] + '\n')
        Out.close()

