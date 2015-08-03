#! /usr/bin/env python
import re
import os
from sys import argv
import argparse


#GLOBAL VARIABLE. MODIFY IF NEEDED
sep='|'
gsep='\|'
#CLASS AND FUNTION DEFINITION

class newick():
    def __init__(self, N):
        self.leaves = get_leaves(N)
        self.otus = set()
        self.newick = N
        self.splits=[]
        for leaf in self.leaves:
           self.otus.add(leaf.split(sep)[0]) 
        
class split():
    def __init__(self):
        self.vec =None
        self.covec=None
        self.branch_length=None
        self.support=None
        self.name=None
        

class myPhylo():
    '''A class for newick trees'''
    def __init__(self, N):
        self.leaves = get_leaves(N)
        self.sp_seqs = {} # dictionary of OTU (keys), and the Unique identifiers in the newick
        self.splits = []
        self.ortho=[]
        self.costs={} # Dictionary of leaf cost for inparalog evaluation'
        self.newick = N
        for leaf in self.leaves:
            otu =leaf.split(sep)[0]
            uid =leaf.split(sep)[1]
            if otu not in self.sp_seqs:
                self.sp_seqs[otu] = [] 
            self.sp_seqs[otu].append( uid )
            self.costs[leaf] = 1.0


            
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

def split_decomposition(Tree):
    'returns an unordered collection of splits class objects'
    newick = Tree.newick
    leaves = Tree.leaves
    P = {}
    ids = 0
    idc =0
    Pos =0
    closed = []
    for l in newick:
        if l == '(':
            ids +=1
            P[ids]=[Pos]
        elif l ==')':
            idc = ids
            while idc in closed and idc != 0:
                idc = idc-1
                #print idc
            P[idc].append(Pos)
            closed.append(idc)
        Pos+=1
#    print P
    vecIns = []
    for Key in P.iterkeys():#Find splits implied by the parenthesis in newick
        r_vec=newick[P[Key][0]: P[Key][1]]
        vec = get_leaves(r_vec)
        covec = complement(vec, Tree.leaves)
        if not any (sorted(vec) == sorted(S.vec) or sorted(vec) == sorted(S.covec) for S in Tree.splits):
            mySplits = split()
            mySplits.vec = vec
            mySplits.covec = covec
            exp = re.escape(r_vec) + r'\)([0-9\.]+\:[0-9\.]+)'
            BranchVal=re.findall(exp, Tree.newick)
            if len(BranchVal) == 1:
                mySplits.branch_lenght = BranchVal[0].split(':')[1]
                mySplits.support = BranchVal[0].split(':')[0]
            elif len(BranchVal) ==0:
                print 'Error: This branch  has no values'
            else:
                print 'Error: The branch occurs %d times in the tree' % len(BranchVals)
            Tree.splits.append(mySplits)
        else:
            print 'yop'
    for leaf in leaves:
        vec=leaf
        covec = complement(vec,leaves)
        if any (leaf == S.vec or leaf == S.covec for S in Tree.splits):
            mySplit =split()
            mySplits.vec = vec
            mySplits.covec = covec
            exp = re.escape(leaf) + r'\:([0-9\.]+)'
            BranchVal =  re.findall(exp, Tree.newick)
            if len(BranchVal) == 1:
                mySplits.branch_lenght = BranchVal[0]
            elif len(BranchVal) == 0:
                print 'The input tree has no branch values'
            else:
                print 'The terminal: %s  occurs %d times in the tree' % (leaf, len (BranchVals))
            Tree.splits.append(mySplit)
        else:
            print 'yap'

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
