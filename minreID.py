#!/usr/bin/env python3

import os
import re
from sys import argv

if len(argv) == 4:
    script, infile, SP_code, sep  = argv
    inp_F = open(infile, 'r')
    out_name = SP_code + "_withid.fst"
    out_F = open(out_name, 'w')
    counter = 1

    for line in inp_F:
        id_Line= re.search(r'^>', line)
        idNum = format(counter, '06d')
        unique_id= '>' + SP_code + sep + idNum + sep
        if id_Line:
            nl1 = re.sub(r'\s.+', '', line) # remove additional annotations
            nl2 = re.sub(r'^>', unique_id, nl1) # add unique identifier 
            out_F.write(nl2)
            counter += 1 
        else:
            out_F.write(line)
else:
    print("ERROR: Wrong number of arguments, see Usage below.")
    print ("""Usage: minreID.py  <INPUT_FASTA> <SP_CODE>  <SEPARATOR>""")
