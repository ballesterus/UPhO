#!/usr/bin/env python

"""Usage: python minreID file SP_CODE """
import os
import re
from sys import argv

script, infile, SP_code  = argv

inp_F = open(infile, 'r')
out_name = SP_code + "_withid.fst"
#species = raw_input(">Type the species name NO SPACES:")
#species_Name = "|" + species
#type_of_seq=raw_input('>What type of sequence is this?')
out_F = open(out_name, 'w')
counter = 1

for line in inp_F:
    id_Line= re.search(r'^>', line)
    idNum = format(counter, '06d')
    unique_id= '>' + SP_code +'|' + idNum
    if id_Line:
        nl0=re.sub(r'cds\.', '', line)
        nl1 = re.sub(r'\|.+', '', nl0)
        nl2 = re.sub(r'^>', unique_id, nl1) # add unique identifier 
        out_F.write(nl2)
        counter += 1 
    else:
        out_F.write(line)
