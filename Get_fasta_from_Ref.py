#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import os
import re
from Bio import SeqIO
import argparse

parser = argparse.ArgumentParser(description='This script creates fasta files from a list of sequence idetifiers. It takes as input a file in which each line is  list of of sequence identifiers to be written in multi-fasta file; and a Reference file, which contains the identifiers and their sequences. Fasta id in query and Reference should be identical. The output files are named with using a user defined prefix and a counter, or if a name defined by the user is preferred, this should be given as the firts elementvof tge list and identified by starting with  "#" ')
parser.add_argument('-q', dest = 'query', type = str, default= 'None',  help = 'file with fasta identifiers separated by ",". ')
parser.add_argument('-o', dest= 'outdir', type =str, default= '.', help ='Name of the directory to use as utput, if does no exist this wll be created. Default "."')
parser.add_argument('-p', dest= 'prefix', type = str, default= 'Group', help ='Prefix to use whe no group name is provided')
parser.add_argument('-r', dest= 'Reference', type = str, default= 'None', help ='A fasta file with the source fasta sequences in the input tree. If provided, a fasta file will be created for each ortholog found')
parser.add_argument('-c', dest= 'clean', type = str, default= 'False', help ='When true, redundancies are resolved (no subsets, no overalap ro same ortho-group). I produces clean log output')


args = parser.parse_args()
#print args

#GLOBAL VARIABLE. MODIFY IF NEEDED
sep = '|'

#Function definitions
def No_OG_subsets (File):
    '''Takes a UPho_Pruned.txt. It writes a similar formated file with one Orthologs per line but with out-subsets '''
    Log = open('OG_clean_II.log', 'w')
    Out = open('OG_cleaned_II.txt', 'w')
    M_List = open(File).readlines()
    F = open(File, 'r')
    TotalSubsets=0
    print 'Master list contains %d elements' % len(M_List)
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
    Log.write(str(TotalSubsets)+' xsubsets processed')
    Log.close()
    Out.close()
    F.close()
def No_Same_OG_Intesec(File):
    Log = open('OG_clean_I.log', 'w')
    Out = open('OG_cleaned_I.txt', 'w')
    F = open(File, 'r')
    Current =''
    Independent = []
    for Line in F:
        A = Line.strip('\n').split(',')  
        Pattern = re.findall("#[a-zA-Z0-9]+_[0-9]+_",A[0])
        if Pattern == Current:
            for i in Independent:
                if A  not in Independent:
                    if len(set(A)&set(i)) > 0:
                        Independent.remove(i)
                        Winner= max([A,i], key=len)
                        Independent.append(Winner)
                        Log_st= 'The groups %s (%d seqs) and %s (%d seqs) share %d sequences\n' % (i[0], len(i)-1, A[0], len(A) -1 , len(set(A)&set(i)))
                        print Log_st
                        Log.write(Log_st)
                        
                    else:
                        Independent.append(A)
        else:
            print 'The independent set derived from tree %s has %d seqsIds' % (Current, len(Independent))
            for i in Independent:
                Out.write(','.join(i) + '\n')
            Current = Pattern
            Independent = []
            Independent.append(A)
                                 
                                              
def Retrieve_Fasta(in_file, Outdir, Type, Reference):
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
                                OG_filename = Type + "_" + str(Counter) + ".fasta" 
                                OG_outfile = open(Outdir+ '/' + OG_filename, 'w')
                                Counter += 1
			for seqId in qlist:
                                SeqIO.write(seqSource[seqId], OG_outfile, 'fasta')
			print "successfully created %s" % OG_filename 
			OG_outfile.close()

#RUNNING OPERATIONS
if args.clean == 'True':
    print "Cleaning the input file of type I redunduancies: overlap of orthogroups derived from the same gene tree"
    No_Same_OG_Intesec(File):
    print 'Done cleaning type I, proceeding to clean subsets'
    No_OG_subsets(File):
    print "Cleaning is done, check log files for details. Proceeding to retrived clened sequences from the reference."
    Retrieve_Fasta('OG_cleaned_II.txt', args.outdir, args.prefix, args.Reference)
elif args.clean == 'False':
    Retrieve_Fasta(args.query, args.outdir, args.prefix, args.Reference)
else:
    print "Error: use 'True' or 'False' for the -c flag "
