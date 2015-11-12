#!/usr/bin/env python

import argparse
import re
from sys import argv

parser = argparse.ArgumentParser(description="This  script returns alignments processed for phylogenetic analyses. It  performs a basic sanitation on the input files removing poorly overlapping  sequences from the alignment. A sequence is considered 'poor' when it shows less than 'm' unambiguous sites or the length of unambiguous sites  extends less than a proportion 'p' of the total alignment length. It can additionally output MSA with only one sequence per OTU, removing additional sequence identifiers and retaining only the longest sequence. Unless a new threshold is provided (-t) the cleaned alignments have the same taxon composition as the input.")
parser.add_argument('-in', dest = 'input', type = str, nargs= '+',  help = 'Files to process(fasta alignment)')  
parser.add_argument('-m', dest = 'minalnL', type = int, default= 0,  help = 'Minimum alignment length.') 
parser.add_argument('-p', dest = 'percentage', type = float, default = 0.0, help= 'Minimum alignment relative overlap (float 0-1).')
parser.add_argument('-d', dest = 'delimiter', type = str, default= '|',  help = 'Custom character separating fields of sequence identifier.')
parser.add_argument('-t', dest ='minTax', type=int, default = 1, help ='Minimum Taxa in cleaned alignment')
parser.add_argument('-r', dest ='representative', action='store_true', default = False, help ='When the flag is present, one representative sequence per species(the longest) retained in the alignment.')
args, unknown = parser.parse_known_args()

#print args

###Function definitions
def is_ID(Line):
    """Evaluates if a string correspond to fasta identifier. herein broadly defined by starting with the e '>' symbol"""
    if Line.startswith('>'):
        return True
    else:
        return False
    
def seq_leng_nogaps(Str):
    """Returns the length of a sequence without counting and ambiguous positions"""
    return len(Str.replace('-', ''))
    
def Fasta_Parser(File):
    """Returns a dictionary from a fasta file containing FastaId(key) and Seqs"""
    Records = {}
    with open(File, 'r') as F:
        Seq=''
        for Line in F:
            if is_ID(Line) and len(Seq) == 0:
                seqid =Line.replace('\n', args.delimiter).strip('>') #replace ends of line with the delimiter character thus ids with s single field ids.
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
        #print seqid
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


def spp_in_list(alist, delim):
    """Return the species from a list of sequece identifiers"""
    spp =[]
    for i in alist:
        spp.append(i.split(delim)[0])
    return spp

def Aln_L(Dict):
    """Returns False if the sequences in the dict are nor the same length, thus probably not aligned, or the length of the alignment"""
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
    """Remove sequence with high content of gaps"""
    Cleaned = {}
    AlnL= Aln_L(Dict)
    if AlnL != False:
        print "The aligmnment to clean is %d long" % AlnL
        for otu in Dict.iterkeys():
            SeL=seq_leng_nogaps(Dict[otu])
            if float(SeL)/AlnL > args.percentage and SeL > args.minalnL:
                Cleaned[otu] = Dict[otu]
            else:
                print "Sequence %s is shorter than the thresholds (%d sites) and will be removed from the alignment." % (otu, SeL)
        return Cleaned

######MAIN######
if __name__ == "__main__":
    from BlastResultsCluster import spp_in_list
    for File in  args.input:
        FileName= File.split('.')
        print '\nWorking on %s' %File
        F = Fasta_Parser(File)
        if args.minTax !=1:
            SppinAln = args.minTax
        else:
            SppinAln = len(set(spp_in_list(F.keys(), args.delimiter)))
        print SppinAln
        if args.percentage > 0.0 or args.minalnL > 0:        
            print '\tSanitizing alignment %s by removing sequences with less than %d or less than %.2f percent occupancy.' % (FileName[0], args.minalnL, args.percentage)
            F = Sanitize_aln(F)
            if not F:
                print "\tAlert: Not a single  clean sequence was found in %s" %File
        if args.representative:
            print '''\tSelecting one representative sequence per species'''
            F =OneOTU(F)
        SppinCleaned =  len(set(spp_in_list(F.keys(), args.delimiter)))
        if SppinCleaned >= SppinAln:
            OutName = FileName[0] + '_clean.' + FileName[-1]
            print '\tCleaned alignment written to %s' % OutName
            Out = open(OutName, 'w')
            for Rec in F.iterkeys():
                Out.write('>%s\n' % Rec)
                Out.write(F[Rec] + '\n')
            Out.close()
        else:
            print '\tAlert: The cleaned alignment contains less species than the original and wont be written to a clean file.'
