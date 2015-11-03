#!/usr/bin/env python

import argparse
import re
from sys import argv

parser = argparse.ArgumentParser(description='This  script returns alignments processed for phylogenetic analyses. It performs a basic sanitation  by of this alignments, removing ambiguous sequences from the alignemnet. A sequences is considered ambiguous when it shows less than N sites  unaumbiguous.')

parser.add_argument('-in', dest = 'input', type = str, nargs= '+',  help = 'Files to process(fasta alignment)')  
parser.add_argument('-m', dest = 'minalnL', type = int, default= 0,  help = 'Minimun alignemnet lenght.') 
parser.add_argument('-p', dest = 'percentage', type = float, default = 0.0, help= 'Minimum alignenent realtive overlap.')
parser.add_argument('-d', dest = 'delimiter', type = str, default= '|',  help = 'Custom character separating fields of sequence identifier.')
parser.add_argument('-r', dest ='representative', action='store_true', default = False, help ='When the flag is present, one representative sequence per species(the longets) retained in the alignement ')
args= parser.parse_args()
print args

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
                seqid =Line.replace('\n', args.delimiter).strip('>')
                Records[seqid]=''
            elif is_ID(Line) and len(Seq) > 0:
                Records[seqid] = Records[seqid] + Seq
                seqid =Line.replace('\n', args.delimiter).strip('>')
                if seqid not in Records.keys():
                    Records[seqid]=''
                Seq=''
            else:
                Part=Line.replace('\n','')
                Seq = Seq + Part
        print seqid
        Records[seqid]=Records[seqid] + Seq #get the very last seq
    F.close()
    return Records

def OneOTU(SppDict):
    rSpp={}
    for oldkey in SppDict.iterkeys():
        newkey = oldkey.split(args.delimiter)[0]
        if newkey not in rSpp.keys():
            rSpp[newkey] = SppDict[oldkey]
        else:
            Longest = max(SppDict[oldkey], rSpp[newkey], key=seq_leng_nogaps) 
            rSpp[newkey] = Longest
    return rSpp

def Aln_L(Dict):
    Ref = Dict.keys()[0]
    Len= len(Dict[Ref]) # obtain a reference from the 1st dict entry.                                           
    if all(Len == len(Dict[key]) for key in Dict.iterkeys()):
        return Len
    else:
        for key in Dict.iterkeys():
            print '''Error: Verify alignment. It contains sequences of different lenght.'''
            print  "%s : %d sites" % (key, len(Dict[key]))
        return False
        
def Sanitize_aln(Dict):
    Cleaned = {}
    AlnL= Aln_L(Dict)
    if AlnL != False:
        print "The aligmnment is %d long" % AlnL
        for otu in Dict.iterkeys():
            SeL=seq_leng_nogaps(Dict[otu])
            if float(SeL)/AlnL > args.percentage and SeL > args.minalnL:
                Cleaned[otu] = Dict[otu]
            else:
                print "Sequence %s is shorter than the thresholds (%d sites) and will be removed from the alignement." % (otu, SeL)
        return Cleaned

######MAIN######
if __name__ == "__main__":
    for File in  args.input:
        FileName= File.split('.')
        print 'Workinng on %s' %FileName
        F = Fasta_Parser(File)
        print 'Sanitizing alignment %s by removing sequences with less than %d or less than %f percent occupancy.' % (FileName[0], args.minalnL, args.percentage)
        F = Sanitize_aln(F)
        if len(F.keys())==0:
            print "Error: No cleaned sequences found"
        else:
            if args.representative:
                '''Selecting one representative sequence per species'''
                F =OneOTU(F)
            if Aln_L(F) > 50 and len(F.keys()) > 5:
                OutName = FileName[0] + '_clean.' + FileName[1] 
                Out = open(OutName, 'w')
                for Rec in F.iterkeys():
                    Out.write('>%s\n' % Rec)
                    Out.write(F[Rec] + '\n')
                Out.close()
            else:
                print 'Alignement too short, discarding it'

            
        

