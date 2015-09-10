#! /usr/bin/env python
import re
import os
from sys import argv
from math import fsum
import argparse

parser = argparse.ArgumentParser(description='Script for finding orthologs from gene family trees using un-rooted phylogenetic orthology criterion. Input trees are provided as a newick file(s) with one or more trees.')
parser.add_argument('-in', dest = 'Trees', type = str, default= None, nargs= '+',  help = 'file or files to prune wirth tree in newick format.')
parser.add_argument('-iP', dest= 'inParalogs', action ='store_true', default= False, help ='When the flag is present, inparalogues will  be included as orthologues, default = False.')
parser.add_argument('-m', dest= 'minTaxa', type = int, default= '4', help ='Specify the minimum number of taxa for orthogroup evaluation.')
parser.add_argument('-ouT', dest='out_trees', action = 'store_true', default =False, help ='When this flag is present  orthobranches  will be witten to its own file in newick format.')
parser.add_argument('-R', dest= 'Reference', type = str, default= None, help ='If provided this argument points to a fasta file to be used as the source of sequences to write individual multiple sequence fasta file for each of the orthogroups found. Requires BlastResultsCluster.py and its dependencies.')
parser.add_argument('-S', dest= 'Support', type = float, default = 0.0, help='Specify a minimum support value for the orthology evaluation.')
parser.add_argument('-d', dest = 'delimiter', type = str, default = '|', help = 'Specify custom field delimiter character separating species name from other sequence identifiers. Species should be the first element for proper parsing. Default is: "|".')
args = parser.parse_args()
#print args

#GLOBAL VARIABLES. MODIFY IF NEEDED
sep=args.delimiter
gsep=re.escape(sep)

#CLASS DEFINITIONS
class split():
    def __init__(self):
        self.vecs=None
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
        self.newick = N.strip('\n')
        for leaf in self.leaves: #Cost initilized
             self.costs[leaf] = 1.0
        split_decomposition(self)   

#FUNCTION DEFINITIONS

def get_leaves(String):
    pattern = "([A-Za-z0-9_]+%s[A-Za-z0-9_%s]+)" % (gsep, gsep)
    Leaves = re.findall(pattern, String)
    return Leaves

def spp_in_list(alist):
    '''return the species from a list of sequece identifiers'''
    spp =[]
    for i in alist:
        spp.append(i.split(sep)[0])
    return spp
    
def complement(Sub, Whole):
    """Return element in Whole that are not present in Sub"""
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
            P[idc].append(Pos)
            closed.append(idc)
        Pos+=1
#Part II: Where we use string operations  and to identify components parts of each split.
    Inspected= []
    for Key in P.iterkeys(): # this extracs splits from the parenthethical notattion using the parenthesis mapping dictionary.
        r_vec=newick[P[Key][0]: P[Key][1]]
        vec = sorted(get_leaves(r_vec))
        covec = sorted(complement(vec, Tree.leaves)) #Complementary splits are inferred as the set of leaves not included in the parenthesis grouping.
        if vec not in Inspected and covec not in Inspected:
            mySplits = split()
            mySplits.vecs = [vec, covec]
            exp = re.escape(r_vec) + r'\)([0-9\.]*:[0-9\.]+)'
            BranchVal=re.findall(exp, Tree.newick)
            try: 
                mySplits.branch_length = BranchVal[0].split(':')[1]
                mySplits.support = BranchVal[0].split(':')[0]
            except:
                print 'No branch value'
            Tree.splits.append(mySplits)
            Inspected.append(vec)
            Inspected.append(covec)
    for leaf in leaves: #Splits leading to each terminal are included.
        vec=[leaf]
        covec = sorted(complement(vec,leaves))
        if leaf not in Inspected:
            Inspected.append(leaf)
            mySplits =split()
            mySplits.vecs = [vec, covec]
            exp = re.escape(leaf) + r'\:([0-9\.]+)'
            BranchVal =  re.findall(exp, Tree.newick)
            try:
                mySplits.branch_length = BranchVal[0]
            except:
                print "No branch value"
            Tree.splits.append(mySplits)
            
def LargestBox(LoL):
    '''Takes a list of lists (lol) and returns a lol where no list is a subset of the others, retaining only the largest'''
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
    """This function returns populates the list of orthologs in the PhyloClass object"""
    OrthoBranch=[]
    #if in paralogs are to be included, update cost parameter per terminals. 
    if args.inParalogs:
        for S in Phylo.splits:
            for i_split in S.vecs:
                Otus = spp_in_list(i_split)
                if  len(set(Otus)) == 1 and len(Otus) > 1: # find splits representing in-paralogs and update costs
                    for leaf in i_split:
                        ICost = 1.0/len(Otus)
                        if ICost < Phylo.costs[leaf]:
                            Phylo.costs[leaf] = ICost #Reduce cost value of inparlogue copies in poportion to the number of inparalogs inplied by this split.
    for S in Phylo.splits:
        if S.support in [None, ''] or float(S.support) >= args.Support:
            for i_split in S.vecs:
                Otus = spp_in_list(i_split)
                cCount = fsum(Phylo.costs[i] for i in i_split)
                if len(set(Otus)) == cCount and cCount >= minTaxa:
                    if i_split not in OrthoBranch:
                        OrthoBranch.append(i_split)
    Phylo.ortho=OrthoBranch

def aggregate_splits(small,large):
    """Takes two newick like splits where small is a subset of large and returns partial newick incluiding the two input groupings"""
    aggregate=large
    contents = get_leaves(small)
    placeholder= contents.pop()
    for i in contents: #remove from aggregate all leaves in small except the placeholder
        aggregate=aggregate.replace(i + ',' , "")
    aggregate = aggregate.replace(placeholder, small) 
    return aggregate

def subNewick(alist, myPhylo):
    '''this fuction takes a list of leaves forming a branch and a source tree, returning the newick subtree'''
    relevant = []
    seed =''
    for split in myPhylo.splits:
        for vec in split.vecs:
            if set(vec).issubset(set(alist)) and len(vec) > 0:
                if  len (vec) == len(alist):
                    seed =  "(%s)%s:%s;" %(','.join(vec), str(split.support), str(split.branch_length))
                elif  len (vec) == 1:
                    rep = '%s:%s' %(vec[0], str(split.branch_length))
                    relevant.append(rep)
                else:
                    rep =  "(%s)%s:%s" %(','.join(vec), str(split.support), str(split.branch_length))
                    relevant.append(rep)
    partial = seed
    relevant = sorted(relevant, key=len, reverse=True) # order is important
    for e in relevant:
        partial = aggregate_splits(e, partial)
    partial = re.sub('None:', ':', partial)
    partial = re.sub(':None', ':1', partial)
    return partial
 
def main_wTrees ():
    Total = 0
    for tree in args.Trees:
        name=tree.split('.')[0]
        count = 0
        with open(tree, 'r') as T:
            for line in  T:
                P = myPhylo(line)
                orthologs(P, args.minTaxa)
                ortNum=0
                for group in P.ortho:
                    FName= '#%s_%d,' %(name,ortNum)
                    OrtBranch=open('%s_%s.tre' %(name,ortNum), 'w')
                    G = ','.join(group).strip(',')
                    OrtList.write(FName + G + '\n')
                    if set(group) == set(P.leaves): # if the whole input tree represents an orthobranch
                        branch = P.newick
                    else:
                        branch = subNewick(group, P)
                    OrtBranch.write(branch + '\n')
                    print "subtree  written to: %s_%s.tre" %(name,ortNum)
                    count += 1
                    Total += 1
                    ortNum += 1
                    OrtBranch.close()
        print "%d orthogroups were found in the tree file %s" % (count, tree)
    print 'Total  orthogroups found: %d' % Total
                            
def main():
    Total = 0
    for tree in args.Trees:
        name=tree.split('.')[0]
        count = 0
        with open(tree, 'r') as T:
            for line in  T:
                P = myPhylo(line)
                orthologs(P, args.minTaxa)
                ortNum=0
                for group in P.ortho:
                    FName= '#%s_%d,' %(name,ortNum)
                    G = ','.join(group).strip(',')
                    OrtList.write(FName + G + '\n')
                    count += 1
                    Total += 1
                    ortNum += 1
        print "%d orthogroups were found in the tree file %s" % (count, tree)

#MAIN
if __name__ == "__main__":
    print  "Begining orthology assesment. Support threshold = %1.2f; inparalogs = %s" % (args.Support, args.inParalogs) 
    OrtList = open('UPhO_orthogroups.csv', 'w')
    if not args.out_trees:
        main()
    else:
        main_wTrees()
    OrtList.close()
    if args.Reference != None:
        from BlastResultsCluster import retrieve_fasta
        print "Proceeding to create a fasta file for each ortholog"    
        retrieve_fasta( 'UPhO_Pruned.txt','uPhOrthogs','upho', args.Reference)