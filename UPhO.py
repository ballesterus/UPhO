#! /usr/bin/env python3
import re
import os
from sys import argv
from math import fsum
import argparse


#GLOBAL VARIABLES. MODIFY IF NEEDED
sep='|'
gsep=re.escape(sep)

#CLASS DEFINITIONS
class split:
    def __init__(self):
        self.vecs=None
        self.branch_length=None
        self.support=None
        self.name=None
        self.label=[]

class myPhylo():
    '''A class for newick trees'''
    def __init__(self, N):
        self.leaves = get_leaves(N)
        self.splits = []
        self.ortho=[]
        self.costs={} # Dictionary of leaf cost for inparalog evaluation'
        self.newick = N.strip('\n')
        for leaf in self.leaves: #Cost initialized
             self.costs[leaf] = 1.0
        split_decomposition(self)   

#FUNCTION DEFINITIONS

def get_leaves(String):
    '''Find leaves names in newick files using regexp. Leaves names are composed of alpha numeric characters, underscore and a special field delimiter'''
    pattern = "(?<=[,\(])\w.*?(?=[,:;\)])"
#    pattern = "[^\(\),;:\[\]]+%s[^\(\),;:\[\]]+" % gsep
    Leaves = re.findall(pattern, String)
    return Leaves

def spp_in_list(alist):
    '''Return the species from a list of sequence identifiers'''
    spp =[]
    for i in alist:
        spp.append(i.split(sep)[0])
    return spp
    
def complement(Sub, Whole):
    '''Return elements in Whole that are not present in Sub'''
    complement=set(Whole) - set(Sub)
    return list(complement)

def split_decomposition(Tree):
    '''Add a list of splits class objects to myPhylo Class object'''
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
            P[idc].append(Pos+1)# ensure the string incldues the closing parenthesis
            closed.append(idc)
        Pos+=1
#Part II: Where we use string operations to identify components parts of each split.
    Inspected= []
    missBval = 0
    for Key in P.keys(): # This extracs splits deduced from the parenthetical notation ussing mappings in dictionary P.
        r_vec=newick[P[Key][0]: P[Key][1]]
#        print r_vec
        vec = sorted(get_leaves(r_vec))
        covec = sorted(complement(vec, Tree.leaves)) #Complementary splits are inferred as the set of leaves not included in the parenthesis grouping.
        if vec not in Inspected and covec not in Inspected:
            mySplits = split()
            mySplits.vecs = [vec, covec]
            exp = re.escape(r_vec) + r'([0-9\.]*:[0-9\.]+)'
            BranchVal=re.findall(exp, Tree.newick)
            try: 
                mySplits.branch_length = BranchVal[0].split(':')[1]
                mySplits.support = BranchVal[0].split(':')[0]
            except:
                missBval+=1
            Tree.splits.append(mySplits)
            Inspected.append(vec)
            Inspected.append(covec)
    for leaf in leaves: #Splits leading to each terminal are included.
        vec=[leaf]
        covec = sorted(complement(vec,leaves))
        if vec not in Inspected:
            Inspected.append(leaf)
            mySplits = split()
            mySplits.vecs = [vec, covec]
            exp = re.escape(leaf) + r'\:([0-9\.]+)'
            BranchVal =  re.findall(exp, Tree.newick)
            try:
                mySplits.branch_length = BranchVal[0]
            except:
                missBval+=1
            Tree.splits.append(mySplits)

def No_OG_subsets(File):
    '''Takes a UPho_orthogroups.csv. It writes a similar formated file with one orthologroup per line but without subsets'''
    Log = open('OG_no_subsets.log', 'w')
    Out = open('OG_no_subsets.txt', 'w')
    M_List = open(File).readlines()
    F = open(File, 'r')
    TotalSubsets=0
    print ('Master list contains %d elements' % len(M_List))
    F = open(File, 'r')
    for Line in F:
        Score = 0
        A = Line.strip('\n').split(',')
        Aid = A.pop(0)
        for B in M_List:
            B = B.strip('\n').split(',')
            Bid = B.pop(0)
            #print B
            if set(A).issubset(B) and A != B:
                Log.write('SUBSET: Ortho group %s is a subset of Orthogroup %s\n' %(Aid, Bid))
                Score +=1
                TotalSubsets += 1
        if Score < 1:
            Out.write(Line)
    Log.write(str(TotalSubsets)+' subsets processed')
    Log.close()
    Out.close()
    F.close()

def No_Same_OG_Intesec(File):
    Log = open('OG_no_intersec.log', 'w')
    Out = open('OG_no_intersec.txt', 'w')
    F = open(File, 'r')
    Current =''
    Independent = []
    for Line in F:
        A = Line.strip('\n').split(',')  
        Pattern = re.sub("_[0-9]+$", "",A[0])
        if Pattern == Current:
            for i in Independent:
                if A  not in Independent:
                    if len(set(A)&set(i)) > 0:
                        Independent.remove(i)
                        Winner= max([A,i], key=len)
                        Independent.append(Winner)
                        Log_st= 'The groups %s (%d seqs) and %s (%d seqs) share %d sequences\n' % (i[0], len(i)-1, A[0], len(A) -1 , len(set(A)&set(i)))
                        print (Log_st)
                        Log.write(Log_st)                       
                    else:
                        Independent.append(A)
        else:
            print ('The tree %s has %d independent orthogroups' % (Current, len(Independent)))
            for i in Independent:
                Out.write(','.join(i) + '\n')
            Current = Pattern
            Independent = []
            Independent.append(A)
    for i in Independent:
        Out.write(','.join(i) + '\n')
    F.close()
    Out.close()
    Log.close()

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

def orthologs(Phylo, minTaxa, bsupport):
    '''This function returns populates the list of orthologs in the PhyloClass object'''
    OrthoBranch=[]
    #if in-paralogs are to be included, update cost value of each terminals. 
    if args.inParalogs:
        for S in Phylo.splits:
            if S.support in [None, ''] or float(S.support) >= bsupport:
                for i_split in S.vecs:
                    Otus = spp_in_list(i_split)
                    if  len(set(Otus)) == 1 and len(Otus) > 1: # find splits representing in-paralogs and update costs
                        for leaf in i_split:
                            ICost = 1.0/len(Otus)
                            if ICost < Phylo.costs[leaf]:
                                Phylo.costs[leaf] = ICost #Reduce cost value of inparlogue copies in poportion to the number of inparalogs inplied by this split.
    for S in Phylo.splits:
        if S.support in [None, ''] or float(S.support) >= bsupport:
            for i_split in S.vecs:
                Otus = spp_in_list(i_split)
                cCount = fsum(Phylo.costs[i] for i in i_split)
#                print ("%s:%f" % (','.join(Otus), cCount))
                if len(set(Otus)) == cCount and cCount >= minTaxa:
                    if i_split not in OrthoBranch:
                        OrthoBranch.append(i_split)
    OrthoBranch = LargestBox(OrthoBranch)
    Phylo.ortho=OrthoBranch

def aggregate_splits(small,large):
    '''Takes two newick like splits where small is a subset of large and returns partial newick incluiding the two input groupings'''
    aggregate=large
    contents = get_leaves("(%s)" %small)
    placeholder= contents.pop()
    aggregate=aggregate.replace("%s," % placeholder, "@@@,")
    aggregate=aggregate.replace("%s)" % placeholder, "@@@)")
    placeholder="@@@"
    for i in contents: #remove from aggregate all leaves in small except the placeholder
        aggregate=aggregate.replace('%s,' %i , "")
        aggregate=aggregate.replace('%s)' %i , ")")
    aggregate = aggregate.replace(placeholder, small) 
    return aggregate


def leaf_len(string):
    L=get_leaves(string)
    return len(L)

def subNewick(alist, myPhylo):
    '''This function takes a list of leaves forming a branch and a source tree, returning the newick subtree'''
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
    relevant = sorted(relevant, key=leaf_len, reverse=True) # order is important
    for e in relevant:
#        print (e)
        partial = aggregate_splits(e, partial)
    partial = re.sub('None:', ':', partial)
    partial = re.sub(':None', ':1', partial)
    return partial
 
def main_wTrees ():
    '''Main program execution when trees are to be written'''
    if not os.path.exists('UPhO_branches'):
        os.makedirs('UPhO_branches')
    Total = 0
    for tree in args.Trees:
        name=tree.split('.')[0]
        name=name.replace('/','_')
        count = 0
        with open(tree, 'r') as T:
            for line in  T:
                P = myPhylo(line)
                orthologs(P, args.minTaxa, args.Support)
                ortNum=0
                for group in P.ortho:
                    FName= '#%s_%d,' %(name,ortNum)
                    OrtBranch=open('UPhO_branches/%s_%s.tre' %(name,ortNum), 'w')
                    G = ','.join(group).strip(',')
                    OrtList.write(FName + G + '\n')
                    if set(group) == set(P.leaves): # if the whole input tree represents an orthobranch
                        branch = P.newick
                    else:
                        branch = subNewick(group, P)
                    OrtBranch.write(branch + '\n')
                    print ("subtree  written to: %s_%s.tre" %(name,ortNum))
                    count += 1
                    Total += 1
                    ortNum += 1
                    OrtBranch.close()
        print ("%d orthogroups were found in the tree file %s" % (count, tree))
    print ('Total  orthogroups found: %d' % Total)
                            
def main():
    '''Main program execution when trees are not written'''
    Total = 0
    for tree in args.Trees:
        name=tree.split('.')[0]
        count = 0
        with open(tree, 'r') as T:
            for line in  T:
                P = myPhylo(line)
                orthologs(P, args.minTaxa, args.Support)
                ortNum=0
                for group in P.ortho:
                    FName= '#%s_%d,' %(name,ortNum)
                    G = ','.join(group).strip(',')
                    OrtList.write(FName + G + '\n')
                    count += 1
                    Total += 1
                    ortNum += 1
        print ("%d orthogroups were found in the tree file %s" % (count, tree))
    print ('Total  orthogroups found: %d' % Total)

#MAIN
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script for finding orthologs from gene family trees using Unrooted Phylogenetic Orthology criterion. Input trees are provided as a newick file(s) with one or more trees.')
    parser.add_argument('-in', dest = 'Trees', type = str, nargs= '+', required=True,  help = 'Input file(s) to evaluate, with tree(s) in newick format.')
    parser.add_argument('-iP', dest= 'inParalogs', action ='store_true', default= False, help ='Include inparalogs in the orthogroups, default = False.')
    parser.add_argument('-m', dest= 'minTaxa', type = int, default= '4', help ='Specify the minimum number of OTUs in an orthogroup.')
    parser.add_argument('-ouT', dest='out_trees', action = 'store_true', default =False, help ='Write orthologous branches to newick file.')
    parser.add_argument('-R', dest= 'Reference', type = str, default= None, help ='Points to a fasta file to be used as the source of sequences to write individual multiple sequence fasta file for each of the orthogroups found. Requires Get_fasta_from_Ref.py and its dependencies.')
    parser.add_argument('-S', dest= 'Support', type = float, default = 0.0, help='Minimum support value for the orthology evaluation.')
    parser.add_argument('-d', dest = 'delimiter', type = str, default = '|', help = 'Specify custom field delimiter character separating species name from other sequence identifiers. Species name should be the first element for proper parsing. Default is: "|".')
    args = parser.parse_args()
    sep=args.delimiter
    gsep=re.escape(sep)
    OrtList = open('UPhO_orthogroups.csv', 'a')

    print  ("Begining orthology assesment. Support threshold = %1.2f; inparalogs = %s" % (args.Support, args.inParalogs))

    if not args.out_trees:
        main()
    else:
        main_wTrees()
    print ("Removing redundancies. Ambiguous orthology assignments will favor larger orthogroup.")
    OrtList.close()
    No_OG_subsets("UPhO_orthogroups.csv")
    No_Same_OG_Intesec("OG_no_subsets.txt")
    os.remove("OG_no_subsets.txt")
    os.rename("OG_no_intersec.txt", "UPhO_nr_orthogroups.csv")
    print ("Non redundant orthougroups written to UPhO_nr_orthogroups.csv. Dont forget to filter redundant orthobranches if subtrees were produced.")
    OrtList.close()
    if args.Reference != None:
        import Get_fasta_from_Ref as GFR
        print ("Proceeding to create a fasta file for each ortholog")    
        GFR.main('UPhO_orthogroups.csv','UPhO_Seqs','upho', args.Reference)
