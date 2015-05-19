#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import os
import re
from Bio import SeqIO
import argparse

parser = argparse.ArgumentParser(description='This script creates fasta files from a list of sequence idetifiers. It takes as input a file in which each line is  list of of fasta identifiers to be written in fasta format; and a Reference file, which contains the sequences. Fasta id in query and Reference should be identical. The output files are named with using a user defined prefix and a counter, or if a name defined by the user is preferred, this should be given as the firts elementvof tge list and identified by starting with  "#" ')
parser.add_argument('-q', dest = 'query', type = str, default= 'None',  help = 'file with fasta identifiers separated by ",". ')
parser.add_argument('-o', dest= 'outdir', type =str, default= '.', help ='Name of the directory to use as utput, if does no exist this wll be created. Default "."')
parser.add_argument('-p', dest= 'prefix', type = str, default= 'Group', help ='Prefix to use whe no group name is provided')
parser.add_argument('-r', dest= 'Reference', type = str, default= 'None', help ='A fasta file with the source fasta sequences in the input tree. If provided, a fasta file will be created for each ortholog found')
parser.add_argument('-c', dest= 'clean', type = str, default= 'False', help ='When true, redundancies are resolved (no subsets, no overalap ro same ortho-group). I produces clean log output')

args = parser.parse_args()
print args

#GLOBAL VARIABLE. MODIFY IF NEEDED
sep = '|'



def retrieve_fasta(in_file, Outdir, Type, Reference):
        """ Takes a series of sequence comma separated Identifiers from orthogroups (one per line), and produces fasta files for each orthoGroup (line) """
        handle = open(in_file, 'r')
        if not os.path.exists(Outdir):
                os.makedirs(Outdir)
        else:
                print 'The output dir already exist!'
        Counter = 0
        seqSource = SeqIO.to_dict(SeqIO.parse(open(Reference), 'fasta'))
        for line in handle:
		if len(line) > 0: # do not process empty lines
                        line = line.replace(' ', '' ) # remove white spaces
			qlist = line.strip('\n').split(',')
                        if line.startswith('#'):
                                Name = qlist.pop(0)
                                OG_filename = Name.strip('#') + '.fasta'
                                OG_outfile = open(Outdir+ '/' + OG_filename, 'w')
                        else:
                                OG_filename = Type + "_" + str(OG_number) + ".fasta" 
                                OG_outfile = open(Outdir+ '/' + OG_filename, 'w')
                                OG_number += 1
			for seqId in qlist:
                                SeqIO.write(seqSource[seqId], OG_outfile, 'fasta')
			print "successfully created %s" % OG_filename 
			OG_outfile.close()
