#! /usr/bin/env python
# -*- coding: utf-8 -*-
from sys import argv
import re
import os
import sqlite3

"""USAGE: This script finds clusters of similar sequences using NCBI blast. It provides the option of filtering groups using Salicos & Rokas (2011)  'r' parameter.
"""

#PART I: where we incorportate all soyce seqeunces into a sqlite3 database
conn = sqlite3.connect('sequences.db')
c = c.cursor()
c.execute('''CREATE TABLE trasncripts
(transcriptID INTEGER PRIMARY KEY UNIQUE,
sequence TEXT,
trinity_identifier TEXT,
len INT,
path TEXT,
genus TEXT,
species TEXT,
tissue TEXT)
''')

#Feed the database
file = raw_input('provide file name: ')
infile = open(file, 'r')

def one_line_entry(file):
    temp = open('temp_out.txt', 'rw')
    for line in file:
        if re.search(r'^>', line):
            nl= re.sub(r'^(.+)\n', '\\1    ', line)
            temp.write(nl)
        else:
            sle_source1.write(re.sub(r'\n', '', line))
            sle_source1= open("sle.fa", 'r')
            sle_ready = open('sle_ready.fa', 'w')
            for line in sle_source1:
                nl = re.sub(r'>', "\\n>", line)
                sle_ready.write(nl)
os.remove("sle1.fa")
