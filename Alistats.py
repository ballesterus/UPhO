#!/usr/bin/env python

import argparse
import re
from sys import argv
from Consensus import *

delim = '|'

def aln_stats(Dict):
    Spp = set([i.split(delim)[0] for i in Dict.iterkeys()])
    Allseq = ''.join(Dict.values())
    AT = Allseq.count('A') + Allseq.count('T')
    GC = Allseq.count('G') + Allseq.count('C')
    Gaps = Allseq.count('-')
    sites = len(Allseq)
    return [ len(Dict.keys()), len(Spp), float(AT)/sites, float (GC)/sites, float(Gaps)/sites,]

#MAIN
if __name__=='__main__':
    parser = argparse.ArgumentParser(description='This is a program, to write tab separated statistics from  FASTA sequence files, specially those containing UPhP orthologs.')
    parser.add_argument('-in', dest = 'Alignments', type = str, nargs= '+', required=True,  help = 'Input file(s) to create the report from.')
    parser.add_argument('-t', action= 'store', dest = 'threshold', default = 1.0, type = float,  help='Specify frequency threshold for consensus, default 1.0' ) 
    parser.add_argument('-d', dest = 'delimiter', type = str, default = '|', help = 'Specify custom field delimiter character separating species name from other sequence identifiers. Species name should be the first element for proper parsing. Default is: "|".')
    arguments= parser.parse_args()
    #Global variables
    delim = arguments.delimiter 
    with open('alns_stats.tsv', 'w') as out:
        out.write("File\tnumSeq\tnumSpp\tAlnLen\tATper\tGCper\tGapperr\tambigperc\tidentpe\tConsensus\n")
        for F in arguments.Alignments:
            Al = Fasta_to_Dict(F)
            numSeq, numSpp, ATper, GCper, Gapper = aln_stats(Al)
            C = make_Consensus(Al, arguments.threshold)
            AlnL = len(C)
            Ident = (C.count('A') + C.count('T') + C.count('C') + C.count('G')) / float(AlnL)
            Ambper = ((AlnL - C.count('-')) / float(AlnL)) - Ident
            out.write("%s\t%d\t%d\t%d\t%f\t%f\t%f\t%f\t%f\t%s\n"  % (F, numSeq, numSpp, AlnL, ATper, GCper, Gapper, Ambper, Ident, C))
        print "Summary stats written to alns_stats.tsv"
