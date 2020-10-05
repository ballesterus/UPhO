#!/usr/bin/env python3

import argparse
import re
from sys import argv
from Consensus import *

delim = '|'

def count_char(char,string):
    n=0
    for i in string:
        if i == char:
            n+=1
    return n

def count_alphabet(datstring, setAlpha):
    msize=len(datstring)
    result=[]
    for i in list(AA):
        result.append(count_char(i,datstring)/msize)
    return result


def seqTypefreq(datastring):
    check=[i for i in datastring if i not in ['-', '?']]
    denom=len(check)
    freqs = count_alphabet(check, ["A", "C", "G", "T"])
    nutsprop = sum(freqs)/denom
    if  all (i in NT for i in list(datastring)) and nutsprop >= 0.5: 
        result=count_alphabet(datastring, AA)
        return ["NT"] + result
    elif  all (i in AA for i in list(datastring)):
        result=count_alphabet(datastring, AA)
        return ["AA"] + result
    else:
        return 'ERROR: NOT AA or NT'
    

def aln_stats(Dict):
    numSeqs = len(Dict.keys())
    Spp = set([i.split(delim)[0] for i in Dict.keys()])
    Allseq = ''.join(Dict.values())
    freqs= seqTypefreq(Allseq)
    typeseq= freqs.pop(0)
    sites = len(Allseq)
    avgSeqL = float(sites)/numSeqs
#    print "missing: %f" % (float(Missing)/sites)
    return [ typeseq, numSeqs, len(Spp), sites, avgSeqL ] + freqs

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
        header=["File", "seqType", "numSeqs", "numSpp", "numSites", "avgSeqLen"] + list(AA) + ["consAmbi", "conIdent", "ConsSeq"]
        out.write("%s\n" % "\t".join(header))
        for F in arguments.Alignments:
            Al = Fasta_to_Dict(F)
            alstat= aln_stats(Al)
            cambig=0
            try:
                C = make_Consensus(Al, arguments.threshold)
                AlnL=len(C)
                if alstat[0] == "NT":
                    for c in C:
                        if c not in  ['A', 'C', 'G', 'T']:
                            cambig+=1
                else:
                    for c in C:
                        if c =="X":
                            cambig+=1
                    
                Ident = (AlnL - cambig) / float(AlnL)
                Ambigperc = cambig/ float(AlnL)
                out.write("%s\t%s\t%s\t%s\t%s\n" % (F, "\t".join(map(str,alstat)),Ambigperc, Ident, C))
            except:
                print ("Cant make consensus, probably not an alignement")
                out.write("%s\t%s\n" % (F, "\t".join(map(str,alstat))))
        print ("Summary stats written to alns_stats.tsv")
