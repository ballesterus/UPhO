#! /usr/bin/env python
import re
import os
from sys import argv
from math import fsum
import argparse

parser = argparse.ArgumentParser(description='This script to prune orthologs from gene trees. Input trees are provided  as a single newick file with one or more trees or a list of many input files')
parser.add_argument('-in', dest = 'Trees', type = str, default= None, nargs= '+',  help = 'file or files to prune wirth tree in newick format), required =False')
parser.add_argument('-iP', dest= 'inParalogs', type =str, default= 'True', help ='When True, inparalogues will  be included as orthologues, default = False')
parser.add_argument('-m', dest= 'Min', type = int, default= '0', help ='Specify the minimum number of taxa to include in orthogroups')
parser.add_argument('-R', dest= 'Reference', type = str, default= 'None', help ='A fasta file with the source fasta sequences in the input tree. If provided, a fasta file will be created for each ortholog found')
parser.add_argument('-S', dest= 'Support', type = float, default = None, help='Specify a minimum support value for the ortholog split.')
#parser.add_argument('-t'. dest= 'Chopper', type = str, default = 'True', help ='When True orthologous branches are written to a newick file with the same topology and annogations than the original source tree.')
args = parser.parse_args()
#print args

#GLOBAL VARIABLES. MODIFY IF NEEDED
sep='|'
gsep=re.escape(sep)

#CLASS DEFINITIONS
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
        self.splits = []
        self.ortho=[]
        self.costs={} # Dictionary of leaf cost for inparalog evaluation'
        self.newick = N
        for leaf in self.leaves:
             self.costs[leaf] = 1.0
        split_decomposition(self)   
#FUNCTION DEFINITIONS

def get_leaves(String):
    pattern = r"[(,]([A-Z _ a-z 0-9]+" + gsep + r"[0-9 A-Z a-z _ ]+)[:,)]"
    Leaves =re.findall(pattern, String)
    return Leaves

def spp_in_list(alist):
    '''return the species from a list of sequece identifiers'''
    spp = []
    map((lambda x: spp.append(x.split(sep)[0])), alist )
    return spp
    
def complement(Sub, Whole):
    complement=[]
    for i in Whole:
        if i not in Sub:
            complemeexnt.append(i)
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
#    print P
#Part II: Where we use regex and to identify components of each split.
    for Key in P.iterkeys():
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
                mySplits.branch_length = BranchVal[0].split(':')[1]
                mySplits.support = BranchVal[0].split(':')[0]
            Tree.splits.append(mySplits)
        else:
            print 'split already recognized'
    for leaf in leaves:
        vec=leaf
        covec = complement(vec,leaves)
        if not any (leaf == S.vec or leaf == S.covec for S in Tree.splits):
            mySplits =split()
            mySplits.vec = [vec]
            mySplits.covec = covec
            exp = re.escape(leaf) + r'\:([0-9\.]+)'
            BranchVal =  re.findall(exp, Tree.newick)
            if len(BranchVal) == 1:
                mySplits.branch_length = BranchVal[0]
            elif len(BranchVal) == 0:
                print 'The input tree h[as no branch values'
            else:
                print 'The terminal: %s  occurs %d times in the tree' % (leaf, len (BranchVals))
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

def ortho_prune(Phylo, minTax):
    OrthoBranch = []
    for S in Phylo.splits:       
        for i_split in [S.vec, S.covec]:
            Otus = spp_in_list(i_split)
            #print Otus
            if len(set(Otus))==len(Otus) and len(Otus) >= minTax: # Eval orthologous split without inparalogues
                ob = [i_split , S.support]
                if ob not in OrthoBranch:
                    OrthoBranch.append(ob)
            if len(set(Otus)) == 1 and len(Otus) > 1: # find splits representing in-paralogs and update costs
                for leaf in i_split:
                    ICost = 1.0/len(Otus)
                    if ICost < Phylo.costs[leaf]:
                        Phylo.costs[leaf] = ICost #Reduce count value of inparlogue copies in poportion to the number of inparalogs involved.
    if  args.inParalogs == 'True':
        for S in Phylo.splits:
            for i_split in [S.vec, S.covec]:
                Otus =spp_in_list(i_split)
                cCount = fsum(Phylo.costs[i] for i in i_split)
                if len(set(Otus)) == cCount and cCount >= minTax:
                    ob = [i_split, S.support]
                    if ob not in OrthoBranch:
                        OrthoBranch.append(ob)
                #print OrthoBranch
    Phylo.ortho=OrthoBranch


#MAIN
if __name__ == "__main__":
    OrList = open('UPhO_Pruned.txt', 'w')
    Total = 0
    for tree in args.Trees:
        T = open(tree, 'r')
        name=tree.split('.')[0]
        count = 0
        for line in  T:
            P = myPhylo(line)
            orthos= []
            ortNum=0
            ortho_prune(P, args.Min)
            if args.Support != None:
                for co in P.ortho:
                     if co[1] == None or float(co[1]) >= args.Support:
                         print '%r > %f' %(co[1], args.Support)
                         orthos.append(co[0])
                     else:
                        print 'split rejected due to low support: %s' %co[1]
            else:
                for co in P.ortho:
                    orthos.append(co[0])
            orthos=LargestBox(orthos)               
            for group in orthos:
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
