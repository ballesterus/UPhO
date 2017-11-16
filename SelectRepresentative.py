#!/usr/bin/env python

import argparse
import UPhO
import Consensus
import Al2Phylo
import re
from sys import argv


###Function definitions

def representative(dic, criterion):
    if criterion=='longest':
        long = 0
        maxk = ''
        for k in dic.iterkeys():
            c = len([ x for x in dic[k] if x not in ['-', '?'] ])
            if c > long:
                long = c
                maxk = k
        return '>%s\n%s\n' %(maxk, dic[maxk])    
    elif criterion =='consensus':
        r=Consensus.make_Consensus(dic, 1.0)
        nid=dic.keys()[0] + " consensus"
        return '>%s\n%s\n' % (nid, r)    
    
def main(fastaFile, treeFile, criterion):
    Seq=Consensus.Fasta_to_Dict(fastaFile)
    T= open(treeFile, 'r')
    newick_str=T.readline()
    T.close()
    P=UPhO.myPhylo(newick_str)
    OutFile=open('%s_rep.fasta' %fastaFile.split('.')[0], 'w+')
    collapsible=[]
    collapsed=[]
    for S in P.splits:
        for isplit in S.vecs:
            Otus = UPhO.spp_in_list(isplit)
            if  len(set(Otus)) == 1 and len(Otus) > 1: # find splits representing in-paralogs and update costs
                collapsible.append(isplit)
    collapsible=UPhO.LargestBox(collapsible)
#    print collapsible
    for i in collapsible:
        staged={}
        for k in i:
            staged[k]=Seq[k]
#        print staged
        selected=representative(staged, criterion)
#        print selected
        OutFile.write(selected)
        collapsed.extend(i)
    for Rec in Seq.iterkeys():
        if Rec not in collapsed:
            OutFile.write('>%s\n' % Rec)
            OutFile.write(Seq[Rec] + '\n')
    OutFile.close()
            
                
    

    ######MAIN######
parser = argparse.ArgumentParser(description="Script for selecting a represemnatitve sequence in a FASTA file for groups of sequences of the same species forming monophyletic groups in a reference tree. Two criterions are enabled: longest and strict consensus sequences. NOTE: the script assumes leave and sequence names are identical in sequence and tree files and sequecnes must be aligned for using the consensus option.")
parser.add_argument('-s', dest = 'fasta', type = str, help = 'Sequence file in FASTA format')  
parser.add_argument('-t', dest = 'tree', type = str,  help = 'Tree File in NEWICK format.') 
parser.add_argument('-c', dest = 'criterion', type = str, default = 'longest', help= 'Criterion for selecting one representaive sequence. Options: longest (default), consensus. Note: for the consensus option, the sequence input files must be aligned')
args, unknown = parser.parse_known_args()

#print args

if __name__ == "__main__":
    fastaFile=args.fasta
    treeFile=args.tree
    criterion=args.criterion
    main(fastaFile, treeFile, criterion)

