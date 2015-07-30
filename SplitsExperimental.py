#! /usr/bin/env python
import re
import os
from sys import argv
import argparse


#GLOBAL VARIABLE. MODIFY IF NEEDED
sep=''
gsep=''
#CLASS AND FUNTION DEFINITION

class newick():
    def __init__(self, N):
        self.leaves = get_leaves(N)
        self.newick = N
        self.splits[]
        new_splits(N)
        S_0=split()
        S_0.vec = self.leaves
        self.splits.append(S_0)
        

        
class split():
    def __init__(self):
        self.vec=None
        self.covec=None
        self.branch_length=None
        self.support=None
        self.name=None
        

class myPhylo():
    '''A class for newick trees'''
    def __init__(self, N):
        self.leaves = get_leaves(N)
        self.Dict = {} # dictionary of OTU (keys), and the Unique identifiers in the newick
        self.splits = split_decomposition(N)
        self.ortho=[]
        self.costs={} # Dictionary of cost for inparalog evaluation'
        self.newick = N
        for leaf in self.leaves:
            otu =leaf.split(sep)[0]
            uid =leaf.split(sep)[1]
            if otu not in self.Dict:
                self.Dict[otu] = [] 
            self.Dict[otu].append( uid )
            self.costs[leaf] = 1.0

def new_splits_decom(T):
    #new split  fuction using regex
    reg= '\(([^\(\)]+)\)([0-9:\.]+)'
    base = re.findall(reg, T.newick)
    count=1
    for i in base:
        S_name = 'S_'+ str(count)
        S_name =split()
        S_name.vec = get_leaves(i)
        S_name.covec= complemet(A.vec, T.leaves)
        if len(i)!=1:
            parts = i[1].split(':')
            if len(parts[0]) != 0:
                S_name.supp= parts[0]
            if len(parts[1]) != 0:
                S_name.branch_lengh=parts[1]
        T.splits.append(S_name)
        count +=1
    for leaf in T.leaves:
        S_name = 'S_'+ str(count)
        S_name.vec=leaf
        S_name.covec=complement(leaf, T.leaves)
        parts = re.findall(leaf + '([0-9:\.]+)', T.newick)
        S_name.branch_leenght=parts
        T.splits.append(S_name)
        count += 1
    

def get_leaves(String):
    pattern = r"[(,]([A-Z _ a-z 0-9]+" + gsep + r"[0-9 A-Z a-z _ ]+)[:,)]"
    Leaves =re.findall(pattern, String)
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
                        Phylo.costs[leaf] = ICost #Reduce count value of inparlogue copies in poportion to the number of inparalogs involved. 
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
