#! /usr/bin/env python

import os
import glob
import re
import pandas as pd
import matplotlib.pyplot as plt
import ete2

''' This script summarizes the distribution of orthologous by taxa'''

W_path = '.'
P_attern = 'faa'
Output = open('OGsummary.csv', 'w')   
T = ete2.Tree('Forest_NR101.tre')

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

def tree_plotter():
    inFile = open('OGsummary.csv', 'r')
    for node in T.traverse():
        node.add_feature('OgCompo', [])
    for line in inFile:
        if re.search('^myOG', line):
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
    ts = TreeStyle()
    ts.show_leaf_name = True
    for n in T.traverse():
        nstyle = NodeStyle()
        nstyle["fgcolor"] = "red"
        nstyle["size"] = n.Total
        n.set_style(nstyle)
    T.show(tree_style=ts)
       # print 'The node %s has %s OGs' %(node.name, node.Total)


#header_writer()
#line_writer()
#Output.close()
# computing frequecies

