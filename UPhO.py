#! /usr/bin/env python
import re
import os
from sys import argv
import argparse

parser = argparse.ArgumentParser(description='This script to prune orthologs from gene trees. Input treesa re provided  as a single newick  file or a list of many input files')
parser.add_argument('-t', dest = 'Trees', type = str, default= 'None', nargs= '+',  help = 'file or files to prune wirth tree in newick format), required =False')
parser.add_argument('-iP', dest= 'inParalogs', type =str, default= 'False', help ='When true, inparalogues will  be included as orthologues, default = False')
parser.add_argument('-m', dest= 'Min', type = int, default= '0', help ='Specify the minimus taxa to include in orthogroups')
parser.add_argument('-R', dest= 'Reference', type = str, default= 'None', help ='A fasta file with the source fasta sequences in the input tree. If provided, a fasta file will be created for each ortholog found')
parser.add_argument('-O', dest= 'Overlaps', type = str, default= 'False', help ='When true the pruned ortholgs do not overlap in any of the leaves.')
args = parser.parse_args()
print args

#GLOBAL VARIABLE. MODIFY IF NEEDED
sep = '|'

#CLASS AND FUNTION DEFINITION

class myPhylo():
    '''A class for newick trees'''
    def __init__(self, N):
        self.leaves = get_leaves(N)
        self.Dict = {} # dicionary of OTU (keys), and the Unique identifiers in the newick
        self.splits = split_decomposition(N)
        self.ortho=[]
        self.costs={}
        self.newick = N
        for leaf in self.leaves:
            self.Dict[leaf.split(sep)[0]] = [] 
            self.costs[leaf] = 1.0
        for leaf in self.leaves:
            self.Dict[leaf.split(sep)[0]].append(leaf.split(sep)[1])
    def No_overlap(self):
        cOrtho =[]
        AA = self.ortho
        BB = self.ortho
        print AA
        print BB
        inspected = []
        for A in AA:
            for B in BB:
                if A !=B and len(set(A)&set(B)) > 0:
                    Winner= max([A,B], key=len)
                        cOrtho.append(Winner)
        self.ortho = cOrtho

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
#    print P
    vecIns = []
    for Key in P.iterkeys():#Find splits inmplied bt the parenthesis in newick
        vec=newick[P[Key][0]: P[Key][1]]
        vec= get_leaves(vec)
        coVec = complement(vec,leaves)
        if sorted(vec) not in vecIns and sorted(coVec) not in vecIns:
            vecIns.append(sorted(vec))
            vecIns.append(sorted(coVec))
            vec.append('&')
            vec = vec + coVec
            split = (','.join(vec))
            splits.append(split)
    
    for leaf in leaves:
        vec=[leaf]
        coVec = complement(vec,leaves)
        if sorted(vec) not in vecIns and sorted(coVec) not in vecIns:
            vecIns.append(sorted(vec))
            vecIns.append(sorted(coVec))
            vec.append('&')
            vec = vec + coVec
            split = (','.join(vec))
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
        #print score
        if score < 2:
            NR.append(L)
    return NR


def ortho_prune(Phylo, minTax):
    OrthoBranch= []
    Splits = Phylo.splits
    #print Splits
    for Split in Splits:
        SplitsVecs = Split.split('&')
        for Vec in SplitsVecs:
            leaves = Vec.split(',')
            leaves.remove('')
            Otus = []
            for leaf in leaves:
                Otus.append(leaf.split(sep)[0])
            if len(set(Otus))==len(Otus) and len(Otus) >= minTax: # Eval orthologous split without inparalogues
                OrthoBranch.append(leaves)
            if len(set(Otus)) == 1 and len(Otus) > 1: # find splits representing in-paralogs
                for leaf in leaves:
                    ICost = 1.0/len(Otus)
                    if ICost < Phylo.costs[leaf]:
                        Phylo.costs[leaf] = ICost #Reduce count value of inparlogue copies in poportion to te number of inparalogues involved. 
    if  args.inParalogs == 'True':
        for Split in Splits:
            SplitsVecs = Split.split('&')
            for Vec in SplitsVecs:
                leaves = Vec.split(',')
                leaves.remove('')
                Otus = []
                cCount = 0    
                for leaf in leaves:
                    Otus.append(leaf.split(sep)[0])
                    cCount += Phylo.costs[leaf]
                cCount = round(cCount, 2) # Fix floating point approximation by rounding up!
                if len(set(Otus)) == cCount and cCount >= minTax:
                    if leaves not in OrthoBranch:
                        OrthoBranch.append(leaves)
    OrthoBranch = deRedundance(OrthoBranch)
    #print OrthoBranch
    Phylo.ortho=OrthoBranch


if args.Trees != 'None':
    OrList = open('UPhO_Pruned.txt', 'w')
    Total = 0
    for tree in args.Trees:
        name=tree.split('.')[0]
        count = 0
        with open(tree, 'r') as T:
            for line in  T:
                P = myPhylo(line)
                ortNum=0
                ortho_prune(P, args.Min)
                #print P.ortho
                if args.Overlaps == 'True':
                    P.No_overlap()
                    print P.ortho
                for group in P.ortho:
                    FName= '#%s_%d,' %(name,ortNum)
                    G = ','.join(group)
                    G = G.strip(',')
                    OrList.write(FName + G + '\n')
                    count += 1
                    Total += 1
                    ortNum += 1
        print " %d orthogroups were found in the tree %s" % (count, tree)
        T.close()
    print 'Total  orthogroups found: %d' % Total
    OrList.close()
    if args.Reference != 'None':
        from BlastResultsCluster import retrieve_fasta
        print "Proceeding to create a fasta file for each ortholog"    
        retrieve_fasta( 'UPhO_Pruned.txt','uPhOrthogs','upho', args.Reference)
