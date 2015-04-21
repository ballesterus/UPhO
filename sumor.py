#! /usr/bin/env python
import os
import glob
import re
import shutil
import readline
import ete2

'''This script contains functions to summariz the distribution of orthologous on a tree.'''

readline.parse_and_bind("tab: complete")
#Global Variables. Modify if needed.

Separator = '|'
outgroup1 = 'H_pococki'
outgroup2= 'S_lineatus'

# Function definitions

def count_identifiers(file):
    Counter =0
    Handle = open(file, 'r')
    for line in Handle:
        if re.search(r'^>', line):
            Counter+= 1
    print counter


def min_leaves(infile, Quant):
    '''takes a file with one or more trees and return as file with the trees that have more pr equal leaves than the minimum specified by Quant'''
    with open(infile, 'r') as F:
        OutName = infile.split('.')[0] + str(Quant) +'.' + infile.split('.')[1]
        Out = open(OutName, 'w')
        for Line in F:
            #print Line
            if Line.startswith('(') and Line.endswith(';\n'): #simple check if line looks like a
                Leaves = re.findall(r"[A-Z_a-z]+", Line)
                #print Leaves
                if len(set(Leaves)) >= int(Quant):
                    Out.write(Line)
    F.close()
    Out.close()


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

def OGSummary_to_Dict(OGsum):
    '''the anti fu nction of line_writter. TRasnform OG_summary file into a python Dict'''
    Dict={}
    with open(OGsum, 'r') as OgS:
        for Line in OgS:
            Line = Line.strip('\n')
            Parts = Line.split(',')
            Og = Parts[0]
            IdSeq = Parts[1] + Separator + Parts[2]
            if not Line.startswith('OGnumber'):
                if Og not in Dict.keys():
                    Dict[Og] = []
                    Dict[Og].append(IdSeq)
                else:
                    Dict[Og].append(IdSeq)
    return Dict

def No_OG_subsets(Dict):
    Log = open('OG_clean.log', 'w')
    D={}
    TotalSubsets=0
    TotalInters=0
    Pair_inspected=[]
    for k,v in Dict.iteritems():
        score = 0
        for i,f in Dict.iteritems():
            if set(v).issubset(f):
                if i != k:
                    Log.write('SUBSET: Ortho group %s s a subset of Orthogroup %s\n' %(k, i))
                    score +=1
                    TotalSubsets+=1
            elif set([k,i])not in Pair_inspected and len(set(v)&set(f)) > 0:
                Log.write('ALERT: %s and %s share some seqs:\n\t%s\n' %(k, i, ','.join(set(v)&set(f))))
                Pair_inspected.append([k,i])
                TotalInters += 1
        if score < 2:
            D[k] = v
    
    Log.write(str(TotalSubsets)+'subsets  and ' + str(TotalInters))
    return D

def line_writer(P_attern):
    for file in glob.glob('*%s' % P_attern):
        Handle = open(file, 'r')
        OrtG = file.strip('%s' % P_attern)
        Output.write('OGnumber,Species_code,Seq_Id\n')
        for Line in Handle:
            if re.search (r'^>', Line):
                Line = Line.strip('\n')
                Line = re.sub(' ', Separator, Line) # unique sequence identifiers should not conatain spaces and this data will not be included in the annotation.
                Div = re.sub('>','',Line).split(Separator)
                OutLine = '%s,%s,%s' % (OrtG, Div[0], Div[1])
                Output.write(OutLine)
        Handle.close()

def Set_of_FastaID(extension):
    '''This fuction inspect iteratively acrooss the composition of sequence identifiers of all files in the current directoty  (fasta sequence list, alignements and trees). Fisrt ocurrence of seqId sets are marked with the added extension '.2'. The collection of marked files constitue then non redundant collection of trees or sequences, based on seqIds only. Not: this function does not verifies identity in the whole file content (sequeces or topologies)   
'''
    Report = open('redundancyReport.txt', 'w')
    UniqComsId = []
    setsInspected = []
    for File in glob.glob('*%s' % extension):
        Handle = open(File, 'r')
        IdsinFile=[]
        for line in Handle:
            if line.startswith('>'):
                FastaId = line.strip('>')
                FastaId = FastaId.replace('\n', '')
                IdsinFile.append(FastaId)
            elif line.startswith('('):
                IdsinFile= re.findall(r'[A-Z]_[a-z]+\|[a-z , 0-9, _]+', line)           
                IdsinFile = sorted(IdsinFile)
        if IdsinFile not in setsInspected:
            UniqComsId.append(File)
            setsInspected.append(IdsinFile)
            shutil.copyfile(File, File + '.2')
        else:
            Index = setsInspected.index(IdsinFile)
            AlreadySet = UniqComsId[Index]
            Report.write('The FastaId compososition of %r is represented in file %r' % (File, AlreadySet))
        Handle.close()
    Report.write('The are %d different groups' % len(UniqComsId))
    Report.write(UniqComsId)

def tree_ortho_annotator(summary, phylo):
    inFile= open(summary, 'r')
    T = ete2.Tree(phylo)
    if T.get_leaves_by_name(outgroup1) != []:
        T.set_outgroup(outgroup1)
    else:
        T.set_outgroup(outgroup2)
    for node in T.traverse():
        node.add_feature('OgCompo', []) #initialize the OrthoGroup (OG) composition in each node
    for line in inFile: #pasre the OG summary file and add the OG composition to each leaf
        if not re.search('^OGnumber', line):
            items= line.split(',')
            Sp_Code = items[1]
            OG_num = items[0]
            CNode = T&Sp_Code #get leaf node
            CCompo = CNode.OgCompo #access the list compositon of each leaf
            if OG_num not in CCompo: # conditional to avoid count twice the same orthogroup per leaf, which occurs when there are inParalogs
                CCompo.append(OG_num)
                CNode.add_feature('OgCompo', CCompo)
    I_node = 0 #initialize counter to use as node name
    for node in T.traverse():
        if node.is_leaf() == False and node.is_root() == False:
            Left = node.children[0]
            Right = node.children[1]
            Outs =  set(T.get_leaves()) - set(node.get_leaves())
            Lun = []
            Run = []
            Oun = []
            for leaf in Left.iter_leaves():
                Lun= set(Lun) | set(leaf.OgCompo)
            for leaf in Right.iter_leaves():
                Run= set(Run) | set(leaf.OgCompo)
            for Sp in Outs:
                leafN =Sp.name
                leaf = T&leafN
                Oun= set(Oun) | set(leaf.OgCompo)
            Inter = set(Lun) & set (Run) & set(Oun)
            node.add_feature('OgCompo', Inter)
            node.add_feature('name', str(I_node))
            I_node += 1
    for node in T.traverse():
        OG_count= len(node.OgCompo)
        node.add_feature('Total', OG_count)
    return T

def CdsSets_by_Treatment(treat):
    D1 = open(treat, 'r')
    Seqs =[]
    for line in D1:
        if  not line.startswith('OGnumber'):
            list=line.split(',')
            element = list[1] + Separator + list[2]
            Set.append(element)
    return set(Seqs)

def get_orthoSet_by_node(Phylo, NodeNumber):
    T = Phylo
    N = T&"%s" % NodeNumber
    Compo = N.OgCompo
    return Compo

def tree_plot(phylo, Bsize = 1.0):
    T = phylo
    ts = ete2.TreeStyle()
    ts.show_leaf_name = False
    for n in T.traverse():
        if n.is_leaf():
            Nlabel = ete2.AttrFace('name', fsize =14, ftype='Arial', fstyle='italic')
            n.add_face(face =Nlabel,column=0, position ='aligned')
        NOg = ete2.AttrFace('Total', fsize= 10, ftype='Arial') 
        n.add_face(face=NOg,column=0, position =  'branch-bottom')
        #Set node style
        nstyle = ete2.NodeStyle()
        nstyle["fgcolor"] = 'Red'
        nstyle["shape"] = "circle"
        nstyle["hz_line_color"]="Gray"
        nstyle["hz_line_width"]=2
        nstyle["vt_line_width"]=2
        nstyle["vt_line_color"]="Gray"
        nstyle["size"] = n.Total * Bsize
        n.set_style(nstyle)
    return ts
