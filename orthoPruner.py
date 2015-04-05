#! /usr/bin/env python

import re
import os


class myPhylo():
    def __init__(self, newick):
        self.leaves = get_leaves(newick)
        self.OTUs = []
        self.splits= split_decomposition(newick)
        self.newick = newick
        for leaf in self.leaves:
            self.OTUs.append(leaf.split('|')[0])
        

def get_leaves(String):
    Leaves =re.findall("[A-Z_a-z]+\|[0-9a-z_]+", String)
    return Leaves


def complement(Sub, Whole):
    for i in Whole:
        if i not in Sub:
            Sub.append(i)
    return Sub


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

    for Key in P.iterkeys():
        vec=newick[P[Key][0]: P[Key][1]]
        vec= get_leaves(vec)
        vec.append('&')
        vec = complement(vec, leaves)
        vec = (','.join(vec))
        split = re.sub(',&,', '&', vec)
        splits.append(split)
    
    for leaf in leaves:
        vec=[]
        vec.append(leaf)
        vec.append('&')
        vec =complement(vec, leaves)
        vec = (','.join(vec))
        split = re.sub(',&,', '&', vec)
        splits.append(split)

    return splits
