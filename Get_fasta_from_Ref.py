#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import os
import re
import argparse


#Function definitions
def Fasta_to_Dict(File):
    '''Creates a dictionary of FASTA sequences in a File, with seqIs as key to the sequences.'''
    with open(File, 'r') as F:
        Records = {}
        for Line in F:
            if Line.startswith('>'):
                Seqid = Line.split(' ')[0].strip('>').strip('\n')
                Seq= ''
                Records[Seqid] = Seq
            else:
                Seq = Records[Seqid] + Line.strip('\n')
                Records[Seqid] = Seq.upper() 
        return Records

def FastaRetriever(seqId, FastaDict):
    """Returns a FASTA formated record from  a seqID and a fastaDict where fasta Id is key in FastaDict"""
    try:
        seq=FastaDict[seqId]
        return ">%s\n%s\n" %(seqId,seq)
    except:
        print "%s not found in the source Fasta file" % seqId

def main(query, outdir, prefix, reference):
    handle = open(query, 'r')
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    else:
        print 'The output dir already exist!'
    Counter = 0
    seqSource = Fasta_to_Dict(reference)
    for line in handle:
	if len(line) > 0: # do not process empty lines
            line = line.replace(' ', '' ) # remove white spaces
	    qlist = line.strip('\n').split(',')
            if line.startswith('#'): #means that filenames are provided in the input this being the fisrt field in the csv.
                Name = qlist.pop(0)
                OG_filename = Name.strip('#') + '.fasta'
                OG_outfile = open(outdir + '/' + OG_filename, 'w')
            else:
                OG_filename = prefix + "_" + str(Counter) + ".fasta" 
                OG_outfile = open(outdir + '/' + OG_filename, 'w')
                Counter += 1
            for seqId in qlist:
                OG_outfile.write(FastaRetriever(seqId, seqSource))
	    print "Successfully created file: %s" % OG_filename
	    OG_outfile.close()
                                


if __name__=='__main__':
    parser = argparse.ArgumentParser(description='This script creates fasta files from a list of sequence idetifiers. It takes as input a file in which each line is  list of of sequence identifiers to be written in multi-fasta file; and a Reference file, which contains the identifiers and their sequences. Fasta id in query and Reference should be identical. The output files are named with using a user defined prefix and a counter, or if a name defined by the user is preferred, this should be given as the first element of the list and identified by starting with  "#" ')
    parser.add_argument('-q', dest = 'query', type = str, default= 'None',  help = 'File with wanted fasta identifiers separated by ",". ')
    parser.add_argument('-o', dest= 'outdir', type =str, default= '.', help ='Name of the directory to use as output, if does no exist this wll be created. Default "."')
    parser.add_argument('-p', dest= 'prefix', type = str, default= 'Group', help ='Prefix to use whe no group name is provided')
    parser.add_argument('-R', dest= 'Reference', type = str, default= 'None', help ='A fasta file with the source fasta sequences in the input tree. If provided, a fasta file will be created for each ortholog found')
    args, unknown = parser.parse_known_args()

    main(args.query, args.outdir, args.prefix,  args.Reference)
