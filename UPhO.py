#! /usr/bin/env python
import re
import os
from sys import argv
import argparse

parser = argparse.ArgumentParser(description='This script to prune orthologs from gene trees. Input treesa re provided  as a single newick  file or a list of many input files')
parser.add_argument('-t', dest = 'Trees', type = str, default= 'None', nargs= '+',  help = 'file or files to prune wirth tree in newick format), required =False')
parser.add_argument('-iP', dest= 'inParalogs', type = bool, default= False, help ='When true, inparalogues will  be included as orthologues, default = False')
parser.add_argument('-m', dest= 'Min', type = int, default= '0', help ='Specify the minimus taxa to include in orthigroups')
parser.add_argument('-R', dest= 'Reference', type = str, default= 'None', help ='A fasta file with the source fasta sequences in the input tree. If provided, a fasta file will be created for each ortholog found')
args = parser.parse_args()
#print arguments


class myPhylo():
    def __init__(self, N):
        self.leaves = get_leaves(N)
        self.Dict = {} # dicionary of OTU (keys), and the Unique identifiers in the newick
        self.splits = split_decomposition(N)
        self.ortho=[]
        self.newick = N
        for leaf in self.leaves:
            self.Dict[leaf.split('|')[0]] = [] 
        for leaf in self.leaves:
            self.Dict[leaf.split('|')[0]].append(leaf.split('|')[1])

def get_leaves(String):
    Leaves =re.findall("[A-Z_a-z]+\|[0-9 A-Z a-z_]+", String)
    return Leaves


def complement(Sub, Whole):
    complement=[]
    for i in Whole:
        if i not in Sub:
            complement.append(i)
    return complement


def split_decomposition(newick):
    'returns a list of splits'
    leaves = get_leaves(newick)
    splits = []
    P = {}
    id =0
    idc =0
    Pos =0
    closed = []
    
    for l in newick:
        if l == '(':
            id +=1
            P[id]=[Pos]
        elif l ==')':
            idc = id
            while idc in closed and idc != 0:
                idc = idc-1
                #print idc
            P[idc].append(Pos)
            closed.append(idc)
        Pos+=1
    #print P
    vecIns = []
    for Key in P.iterkeys():
        vec=newick[P[Key][0]: P[Key][1]]
        vec= get_leaves(vec)
        coVec = complement(vec,leaves)
        if sorted(vec) not in vecIns and sorted(coVec) not in vecIns:
            vecIns.append(sorted(vec))
            vecIns.append(sorted(coVec))
            vec.append('&')
            vec = vec + coVec
            vec = (','.join(vec))
            split = re.sub(',&,', '&', vec)
            splits.append(split)
    
    for leaf in leaves:
        vec=[]
        coVec = complement(vec,leaves)
        if sorted(vec) not in vecIns and sorted(coVec) not in vecIns:
            vecIns.append(sorted(vec))
            vecIns.append(sorted(coVec))
            vec.append('&')
            vec = vec + coVec
            vec = (','.join(vec))
            split = re.sub(',&,', '&', vec)
            splits.append(split)

    return splits


def deRedundance(LoL):
    '''Takes a list of list and returns a list where no list is a subset of the others'''
    NR =[]
    for L in LoL:
        score=0
        for J in LoL:
            if set(L).issubset(J):
                score +=1
        if score <2:
            NR.append(L)
    return NR


def ortho_prune(Phylo, minTax):
    OrthoBranch= []
    Inpar = []
    Splits = Phylo.splits
    for Split in Splits:
        SplitsVecs = Split.split('&')
        for Vec in SplitsVecs:
            leaves = Vec.split(',')
            Otus = []
            for leaf in leaves:
                Otus.append(leaf.split('|')[0])
            if len(set(Otus)) == 1 and len(Otus) > 1:
                for leaf in leaves:
                    Inpar.append(leaf)
            if len(set(Otus))==len(Otus) and len(Otus) >= minTax:
                OrthoBranch.append(leaves)
    if args.inParalogs:
        for Split in Splits:
            SplitsVecs = Split.split('&')
            for Vec in SplitsVecs:
                leaves = Vec.split(',')
                Otus = []
                paralogues=0
                for leaf in leaves:
                    Otus.append(leaf.split('|')[0])
                    if leaf in Inpar:
                        paralogues +=1
                cOtus= len(Otus)- paralogues + 1
                if len(set(Otus))== cOtus  and cOtus >= minTax:
                    OrthoBranch.append(leaves)
    OrthoBranch = deRedundance(OrthoBranch)
    Phylo.ortho=OrthoBranch


if args.Trees != 'None':
    OrList = open('UPhO_Pruned.txt', 'w')
    Total = 0
    for tree in args.Trees:
        count = 0
        with open(tree, 'r') as T:
            for line in  T:
                P = myPhylo(line)
                ortho_prune(P, args.Min)
                for group in P.ortho:
                    G = ','.join(group)
                    G = G.strip(',')
                    OrList.write(G + '\n')
                    count += 1
                    Total +=1
        print " %d orthogroups were found in the tree %s" % (count, tree)
        T.close()
    print 'Total  orthogroups found: %d' % Total
    OrList.close()
    if args.Reference != 'None':
        from BlastResultsCluster import retrieve_fasta
        print "Proceeding to create a fasta file for each ortholog"    
        retrieve_fasta( 'UPhO_Pruned.txt','uPhOrthogs','upho', args.Reference)
