#! /usr/bin/env python
import re
import os
from sys import argv
from math import fsum
import argparse

parser = argparse.ArgumentParser(description='This script to prune orthologs from gene trees. Input trees are provided  as a single newick file with one or more trees or a list of many input files')
parser.add_argument('-in', dest = 'Trees', type = str, default= None, nargs= '+',  help = 'file or files to prune wirth tree in newick format), required =False')
parser.add_argument('-iP', dest= 'inParalogs', type =str, default= 'True', help ='When True, inparalogues will  be included as orthologues, default = False')
parser.add_argument('-m', dest= 'minTaxa', type = int, default= '4', help ='Specify the minimum number of taxa to include in orthogroups')
parser.add_argument('-R', dest= 'Reference', type = str, default= 'None', help ='A fasta file with the source fasta sequences in the input tree. If provided, a fasta file will be created for each ortholog found')
parser.add_argument('-S', dest= 'Support', type = float, default = 0.0, help='Specify a minimum support value for the ortholog split.')
args = parser.parse_args()
#print args

#GLOBAL VARIABLES. MODIFY IF NEEDED
sep='|'
gsep=re.escape(sep)

#CLASS DEFINITIONS
class split():
    def __init__(self):
        self.vecs=None
        self.branch_length=None
        self.support=None
        self.name=None
        
    def vecs(self):
        return [self.vec, self.covec]
    
class myPhylo():
    '''A class for newick trees'''
    def __init__(self, N):
        self.leaves = get_leaves(N)
        self.splits = []
        self.ortho=[]
        self.costs={} # Dictionary of leaf cost for inparalog evaluation'
        self.newick = N
        for leaf in self.leaves:
             self.costs[leaf] = 1.0
        split_decomposition(self)   

#FUNCTION DEFINITIONS

def get_leaves(String):
    pattern = "[A-Za-z0-9_]+%s[A-Za-z0-9_]+" %gsep
    Leaves =re.findall(pattern, String)
    return Leaves

def spp_in_list(alist):
    '''return the species from a list of sequece identifiers'''
    spp = re.findall('([A-Z_a-z0-9]+)%s' %gsep , (',').join(alist))
    return spp
    
def complement(Sub, Whole):
    complement=[]
    for i in Whole:
        if i not in Sub:
            complement.append(i)
    return complement

def split_decomposition(Tree):
    '''Add a list of splits class objects to myPhylo Class objetc'''
    #Part I. Where we identify matching parenthesis in the newick.  
    newick = Tree.newick
    leaves = Tree.leaves
    P = {} #Empty dictionary where to store parenthesis identifiers and a list of string index.
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
#Part II: Where we use string operations  and to identify components parts of each split.
    Inspected= []
    for Key in P.iterkeys():
        r_vec=newick[P[Key][0]: P[Key][1]]
        vec = sorted(get_leaves(r_vec))
        covec = sorted(complement(vec, Tree.leaves))
        if vec not in Inspected and covec not in Inspected:
            mySplits = split()
            mySplits.vecs = [vec, covec]
            exp = re.escape(r_vec) + r'\)([0-9\.]*:[0-9\.]+)'
            BranchVal=re.findall(exp, Tree.newick)
            if len(BranchVal) == 1:
                mySplits.branch_length = BranchVal[0].split(':')[1]
                mySplits.support = BranchVal[0].split(':')[0]
            Tree.splits.append(mySplits)
            Inspected.append(vec)
            Inspected.append(covec)
    for leaf in leaves:
        vec=[leaf]
        covec = sorted(complement(vec,leaves))
        if leaf not in Inspected:
            Inspected.append(leaf)
            mySplits =split()
            mySplits.vecs = [vec, covec]
            exp = re.escape(leaf) + r'\:([0-9\.]+)'
            BranchVal =  re.findall(exp, Tree.newick)
            if len(BranchVal) == 1:
                mySplits.branch_length = BranchVal[0]
            elif len(BranchVal) == 0:
                print 'The input tree h[as no branch values'
            else:
                print 'Alert: The terminal: %s  occurs %d times in the tree' % (leaf, len (BranchVals))
            Tree.splits.append(mySplits)
            
def LargestBox(LoL):
    '''Takes a list of list and returns a list where no list is a subset of the others, retaining only the largest'''
    NR =[]
    for L in LoL:
        score=0
        for J in LoL:
            if set(L).issubset(J):
                score +=1
        if score < 2:
            NR.append(L)
    return NR

def orthologs(Phylo, minTaxa):
    OrthoBranch=[]
    #if in paralogs are to be included, update cost parameter per terminals. 
    if args.inParalogs=='True':
        for S in Phylo.splits:
            if S.support in [None, ''] or float(S.support) >= args.Support:
                for i_split in S.vecs:
                    Otus = spp_in_list(i_split)
                    if  len(set(Otus)) == 1 and len(Otus) > 1: # find splits representing in-paralogs and update costs
                        for leaf in i_split:
                            ICost = 1.0/len(Otus)
                            if ICost < Phylo.costs[leaf]:
                                Phylo.costs[leaf] = ICost #Reduce cost value of inparlogue copies in poportion to the number of inparalogs involved.
    for S in Phylo.splits:
        if S.support in [None, ''] or float(S.support) >= args.Support:
            for i_split in S.vecs:
                Otus = spp_in_list(i_split)
                cCount = fsum(Phylo.costs[i] for i in i_split)
                if len(set(Otus)) == cCount and cCount >= minTaxa:
                    if i_split not in OrthoBranch:
                        OrthoBranch.append(i_split)
    orthos = LargestBox(OrthoBranch)
    Phylo.ortho=orthos

def aggregate_splits(small,large):
    aggregate=large
    contents = get_leaves(small)
    placeholder= contents.pop()
    for i in contents:
        aggregate=aggregate.replace(i+',', "")
    aggregate = aggregate.replace(placeholder, small)
    return aggregate

def subNewick(alist, myPhylo):
    '''this fuction takkes a list of split members and source tree, returning the newick subtree'''
    relevant = []
    root =''
    for split in myPhylo.splits:
        for vec in split.vecs:
            if set(vec).issubset(set(alist)) and len(vec) > 0:
                if  len (vec) == len(alist):
                    root =  "(%s)%s:%s" %(','.join(vec), str(split.support), str(split.branch_length))
                    break
                elif  len (vec) == 1:
                    rep = '%s:%s' %(vec[0], str(split.branch_length))
                else:
                    rep =  "(%s)%s:%s" %(','.join(vec), str(split.support), str(split.branch_length))
                relevant.append(rep)
    print relevant
    partial = root
    for e in relevant:
            partial = aggregate_splits(e, partial)
    partial = re.sub('None:', ':', partial)
    partial = re.sub(':None', ':1', partial)
    return partial
 
#MAIN
if __name__ == "__main__":
    OrList = open('UPhO_Pruned.csv', 'w')
    Total = 0
    for tree in args.Trees:
        name=tree.split('.')[0]
        count = 0
        with open(tree, 'r') as T:
            for line in  T:
                P = myPhylo(line)
                #ortho_prune(P, args.minTaxa)
                orthologs(P, args.minTaxa)
                ortNum=0
                for group in P.ortho:
                    FName= '#%s_%d,' %(name,ortNum)
                    G = ','.join(group).strip(',')
                    OrList.write(FName + G + '\n')
                    count += 1
                    Total += 1
                    ortNum += 1
        print " %d orthogroups were found in the tree %s" % (count, tree)
    print 'Total  orthogroups found: %d' % Total
    OrList.close()
    if args.Reference != 'None':
        from BlastResultsCluster import retrieve_fasta
        print "Proceeding to create a fasta file for each ortholog"    
        retrieve_fasta( 'UPhO_Pruned.txt','uPhOrthogs','upho', args.Reference)
