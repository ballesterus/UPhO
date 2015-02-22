#! /usr/bin/env python
import os
import glob
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ete2
from sys import argv
#from matplotlib_venn import venn3, venn3_circles 
'''This script summarizes the distribution of orthologous by taxa.
 Usage: pythin sumor.py <> <> '''

W_path = '.'
P_attern = 'faa'

def count_identifiers(file):
    Counter =0
    Handle = open(file, 'r')
    for line in Handle:
        if re.search(r'^>', line):
            Counter+= 1
    print counter

os.chdir(W_path)
def header_writer():
    Output.write('OGnumber,Species_code,counSeq_Id\n')

def line_writer():
    for file in glob.glob('*.%s' % P_attern):
        Handle = open(file, 'r')
        OrtG = file.strip('.%s' % P_attern)
        for line in Handle:
            if re.search (r'^>', line):
               Div = re.sub('>','',line).split('|')
               OutLine = '%s,%s,%s' % (OrtG, Div[0], Div[1])
               Output.write(OutLine)
        Handle.close()

def Set_of_FastaID():
    FilesUniqComsId = []
    setsInspected = []
    for file in glob.glob('*.%s' % P_attern):
        Handle = open(file, 'r')
        OrtG = file.strip('.%s' % P_attern)
        for line in Handle:
            IdsinFile=[]
            if re.search (r'^>', line):
                FastaId = line.strip('>')
                IdsinFile.add(FastaId)
            IdsFile = sort(IdsinFile)
            if IdsInFile not in setsInspected:
                UniqComsId.append(IdsinFile)
                setsIspectec.add(IdsinFile)
        Handle.close()
        

def tree_ortho_annotator(summary, phylo):
    inFile= open(summary, 'r')
    T = ete2.Tree(phylo)
    outgroup1 = 'H_pococki'
    outgroup2= 'S_lineatus'
    if T.get_leaves_by_name(outgroup1) != []:
        T.set_outgroup(outgroup1)
    else:
        T.set_outgroup(outgroup2)
    #Declare node name varaibles
    Tetra = T.get_common_ancestor('L_venusta','T_kauensis', 'T_perreira', 'T_versicolor')
    Tetra.add_feature('name', 'Tetragnathidae')
    Aran=T.get_common_ancestor('M_gracilis', 'N_arabesca','G_hasselti')
    Aran.add_feature('name','Araneidae')
    Theri = T.get_common_ancestor('T_californicum','L_tredecimguttatus','T_sp')
    Theri.add_feature('name','Theridiidae')
    Araneoid = T.get_common_ancestor('Tetragnathidae', 'Araneidae', 'Theridiidae')
    Araneoid.add_feature('name', 'Araneoidea')
    for node in T.traverse():
        node.add_feature('OgCompo', [])
    for line in inFile:
        if re.search('^myOG', line) or re.search('^CD_',line):
            items= line.split(',')
            Sp_Code = items[1]
            OG_num = items[0]
            CNode = T&Sp_Code
            CCompo = CNode.OgCompo
            CCompo.append(OG_num)
            CNode.add_feature('OgCompo', CCompo)
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
    for node in T.traverse():
        OG_count= len(node.OgCompo)
        node.add_feature('Total', OG_count)
    return T

def CdsSets_by_Treatment(treat):
    D1 = open(treat, 'r')
    Set =[]
    for line in D1:
        if  not line.startswith('OGnumber'):
            list=line.split(',')
            element = list[1] + list[2]
            Set.append(element)
    return Set

def get_orthoSet_by_node(Phylo, NodeName):
    T = Phylo
    N = T&NodeName
    Set= N.OgCompo
    return Set
Ny
def tree_plot(phylo):
    T = phylo
    ts = ete2.TreeStyle()
    ts.show_leaf_name = False
    for n in T.traverse():
        if n.is_leaf():
            Nlabel = ete2.AttrFace('name', fsize =14, ftype='Arial', fstyle='italic')
            n.add_face(face =Nlabel,column=0, position ='aligned')
        NOg = ete2.AttrFace('Total', fsize= 10, ftype='Arial') 
        n.add_face(face=NOg,column=0, position =  'branch-bottom')
        #Set custum node style
        nstyle = ete2.NodeStyle()
        nstyle["fgcolor"] = 'Red'
        nstyle["shape"] = "circle"
        nstyle["hz_line_color"]="Gray"
        nstyle["hz_line_width"]=2
        nstyle["vt_line_width"]=2
        nstyle["vt_line_color"]="Gray"
        nstyle["size"] = n.Total/100
        n.set_style(nstyle)
        #Custum style for specific nodes
        Tetra = T&'Tetragnathidae'
        Tetra.img_style["fgcolor"] = 'MediumAquaMarine'
        Araneoid = T&'Araneoidea'
        Araneoid.img_style["fgcolor"] = 'Blue'
        L = T&'L_venusta'
        L.img_style["fgcolor"] = 'Green'
    T.show(tree_style=ts)

#header_writer()
#line_writer()
#Output.close()
# computing frequecies

