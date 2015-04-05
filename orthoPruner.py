#! /usr/bin/env python

import re
import os


class myPhylo():
    def __init__(self, N):
        self.leaves = get_leaves(N)
        self.OTUs = []
        self.splits = split_decomposition(N)
        self.ortho=[]
        self.newick = N
        for leaf in self.leaves:
            if leaf.split('|')[0] not in self.OTUs:
                self.OTUs.append(leaf.split('|')[0])

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
    '''Takes a list of list and returns a list wih unique not'''
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
    Splits = Phylo.splits
    for Split in Splits:
        SplitsVecs = Split.split('&')
        for Vec in SplitsVecs:
            leaves = Vec.split(',')
            Otus =[]
            for leaf in leaves:
                Otus.append(leaf.split('|')[0])
            if len(set(Otus))==len(Otus) and len(Otus) >= minTax:
                OrthoBranch.append(leaves)
    OrthoBranch = deRedundance(OrthoBranch)
    Phylo.ortho=OrthoBranch
                
        