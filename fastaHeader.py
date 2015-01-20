#!/usr/bin/env python

import os
import re

input_name = raw_input(">")
species_name = raw_input(>"")
fasta_idline = r('^>')
output_name = re.sub('pep', 'fa', input_name)






def remove_tail(x):
""" This function will remove everything  but the unique identifier"""
    open(input_name, 'r')
    open(output)
    for line in:     
        if re.seacrh(fasta_idline, line):
            rplc = re.sub()
            output_name.write(rplc)
        else:
            output_name.write(line)

            
