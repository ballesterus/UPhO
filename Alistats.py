#!/usr/bin/env python3

import argparse
import re
from sys import argv
from Consensus import *

delim = '|'

def aln_stats(Dict):
    typeseq=string_type(Dict[list(Dict.keys())[0]])
    numSeqs = len(Dict.keys())
    Spp = set([i.split(delim)[0] for i in Dict.keys()])
    Allseq = ''.join(Dict.values())
    sites = len(Allseq)
    Gaps=0
    Missing=0
    ambig=0
    AT=0
    GC=0
    for i in Allseq:
        if i == "-":
            Gaps +=1
        elif i =="?":
            Missing +=1
        if typeseq == "NT":
            if i in ["A", "T"]:
                AT+=1
            elif i in ["G", "C"]:
                GC+=1
            else:
                ambig += 1
        else:
            if i == "X":
                ambig += 1

    avgSeqL = float(sites)/numSeqs
#    print "missing: %f" % (float(Missing)/sites)
    return [ typeseq,numSeqs, len(Spp), float(AT)/sites, float (GC)/sites, float(Gaps)/sites, float(Missing)/sites, float(ambig)/sites, avgSeqL]

#MAIN
if __name__=='__main__':
    parser = argparse.ArgumentParser(description='This is a program, to write TAB separated statistics from FASTA sequence files, specially those containing UPhO orthologs.')
    parser.add_argument('-in', dest = 'Alignments', type = str, nargs= '+', required=True,  help = 'Input file(s) to create the report from.')
    parser.add_argument('-t', action= 'store', dest = 'threshold', default = 1.0, type = float,  help='Specify frequency threshold for consensus, default 1.0' ) 
    parser.add_argument('-d', dest = 'delimiter', type = str, default = '|', help = 'Specify custom field delimiter character separating species name from other sequence identifiers. Species name should be the first element for proper parsing. Default is: "|".')
    arguments= parser.parse_args()
    #Global variables
    delim = arguments.delimiter 
    with open('alns_stats.tsv', 'w') as out:
        out.write("File\tType\tnumSeq\tnumSpp\tAlnLen\tATper\tGCper\tGapperr\tMissingPerc\tambigperc\tidentpe\tConsensus\n")
        for F in arguments.Alignments:
            Al = Fasta_to_Dict(F)
            typeseq,numSeq, numSpp, ATper, GCper, Gapper,Missper,Ambigperc,avgSeqL = aln_stats(Al)
            cambig=0
            try:
                C = make_Consensus(Al, arguments.threshold)
                AlnL=len(C)
                if typeseq == "NT":
                    for c in C:
                        if c not in  ['A', 'C', 'G', 'T']:
                            cambig+=1
                else:
                    for c in C:
                        if c =="X":
                            cambig+=1
                    
                Ident = (AlnL - cambig) / float(AlnL)
                out.write("%s\t%s\t%d\t%d\t%d\t%f\t%f\t%f\t%f\t%f\t%f\t%s\n"  % (F, typeseq, numSeq, numSpp, AlnL, ATper, GCper, Gapper, Missper, Ambigperc, Ident, C))
            except:
                print ("Cant make consensus, probably not an alignement")
                out.write("%s\t%s\t%d\t%d\t%f\t%f\t%f\t%f\t%f\t%f\n"  % (F, typeseq, numSeq, numSpp, avgSeqL, ATper, GCper, Gapper, Missper, Ambigperc))
        print ("Summary stats written to alns_stats.tsv")
