#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import os
import re
from Bio import SeqIO
import argparse

parser = argparse.ArgumentParser(description='This script creates fasta files from a list of sequence idetifiers. It takes as input a file in which each line is  list of of sequence identifiers to be written in multi-fasta file; and a Reference file, which contains the identifiers and their sequences. Fasta id in query and Reference should be identical. The output files are named with using a user defined prefix and a counter, or if a name defined by the user is preferred, this should be given as the first element of the list and identified by starting with  "#" ')
parser.add_argument('-q', dest = 'query', type = str, default= 'None',  help = 'File with wanted fasta identifiers separated by ",". ')
parser.add_argument('-o', dest= 'outdir', type =str, default= '.', help ='Name of the directory to use as output, if does no exist this wll be created. Default "."')
parser.add_argument('-p', dest= 'prefix', type = str, default= 'Group', help ='Prefix to use whe no group name is provided')
parser.add_argument('-R', dest= 'Reference', type = str, default= 'None', help ='A fasta file with the source fasta sequences in the input tree. If provided, a fasta file will be created for each ortholog found')
#parser.add_argument('-c', dest= 'clean', action='store_true', default= False, help ='When true, redundancies are resolved (no subsets, no overalap ro same ortho-group). I produces clean log output')
parser.add_argument('-d', dest = 'delimiter', type = str, default = '|', help = 'Specify custom field delimiter character separating species name from other sequence identifiers. Species name should be the first element for proper parsing. Default is: "|".')
args, unknown = parser.parse_known_args()

#print args

#GLOBAL VARIABLE. MODIFY IF NEEDED
sep = args.delimiter

#Function definitions

                                                                               
def Retrieve_Fasta(in_file, Outdir, prefix, Reference):
        """ Creates fasta files from a csv input file (in_file) where the sequence identifiers to be written to sigle file are each separated by a comma. User provides otput directory, a prefix to use in naming the files,  and a reference from quere to extract the sequences. It requires  Biopython SeqIO."""
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
                        if line.startswith('#'): #means that filenames are provided in the input this being the fisrt field in the csv.
                                Name = qlist.pop(0)
                                OG_filename = Name.strip('#') + '.fasta'
                                OG_outfile = open(Outdir+ '/' + OG_filename, 'w')
                        else:
                                OG_filename = prefix + "_" + str(Counter) + ".fasta" 
                                OG_outfile = open(Outdir+ '/' + OG_filename, 'w')
                                Counter += 1
			for seqId in qlist:
                                SeqIO.write(seqSource[seqId], OG_outfile, 'fasta')
			print "Successfully created file: %s" % OG_filename 
			OG_outfile.close()

#RUNNING OPERATIONS
if __name__ == "__main__":
    Retrieve_Fasta(args.query, args.outdir, args.prefix, args.Reference)
    # if args.clean:
    #     print "Cleaning the input file of type I redunduancies: overlap of orthogroups derived from the same gene tree"
    #     No_Same_OG_Intesec(args.query)
    #     print 'Done cleaning type I, proceeding to clean subsets'
    #     No_OG_subsets('OG_cleaned_I.txt')
    #     print "Cleaning is done, check log files for details. Proceeding to retrived clened sequences from the reference."
    #     Retrieve_Fasta('OG_cleaned_II.txt', args.outdir, args.prefix, args.Reference)
    # elif not args.clean:

  
