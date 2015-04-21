#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from sys import argv
import os
import re
import pandas
import matplotlib.pyplot as plt
from Bio import SeqIO

def mcl_abc(blastout, expectation):
        """Create input file abc for mcl,from a csv blast out and a expectation file """
        outName = 'mcl_%s.abc' % str(expectation)
	myOut = open(outName, 'w')
	in_file = open(blastout, 'r')
	for line in in_file:
                (queryId, subjectId, percIdentity, alnLength, mismatchCount, gapOpenCount, queryStart, queryEnd, subjectStart, subjectEnd, eVal, bitScore) = line.split(",")
                if int(alnLength) >= 50 and float(eVal) <= float(expectation):
                        string ="%s\t%s\t%s\n"%(queryId, subjectId, eVal)
                        myOut.write(string)
        in_file.close()
        myOut.close()


def plot_eval(blastout):
        """This fuction creates takes as an argument a file name (str) of a csv format  Blast+ output and creates a histogram of the frequency of eValues""
        """
        file = pandas.read_csv(blastout, names=['queryId', 'subjectId', 'percIdentity', 'alnLength', 'mismatchCount', 'gapOpenCount', 'queryStart', 'queryEnd', 'subjectStart', 'subjectEnd', 'eVal', 'bitScore'])
        eValues = list(file.eVal)
        plt.hist(eValues, bins = 20, )
        plt.title(" E values Histogram")
        plt.xlabel("EValue")
        plt.ylabel("Frequency")
        plt.show()


def clusters(blastout, expectation):
        """This function take two arguments: 1) the blast csv output, and 2) an E Value threshold for the formation of clusters. The output is text file with the identifiers of the sequenes clustered  on a single line, a hidden parameter in this function is the alignment lenght, Im using 50 ut can be  modified."""
	myOut = open("cluster_" +  str(expectation) + '.txt', 'w')
	in_file = open(blastout, 'r')
	n = 1
	previous_query = "none"
	for line in in_file:
		(queryId, subjectId, percIdentity, alnLength, mismatchCount, gapOpenCount, queryStart, queryEnd, subjectStart, subjectEnd, eVal, bitScore) = line.split(",")
		current_query = queryId
		if (current_query != subjectId) and (int(alnLength) >= 50) and float(eVal) <= float(expectation):
			if previous_query != current_query:
				myOut.write("\n"+current_query + ", " + subjectId)
				previous_query = current_query
				n += 1
			else:
				myOut.write(", " + subjectId)

def non_redundant(reference, min_sp):
        """This filters non species redundant orthoGroups, Takes as input a cluster file, like the one produces by the uction clusters, and a minimum number of different species"""

	inFile = open(reference, 'rw')
	outFile =open("non_redundantOG.txt", "w")
        SetsInspected = []
        for line in inFile:
                spp = re.findall(r'[A-Z]_[a-z]+', line)
                SeqIds = line.strip('\n').split(', ')
                nr = set(spp)
                if len(spp) == len(nr) and len(spp) >= int(min_sp) and sorted(SeqIds) not in SetsInspected:
                        SetsInspected.append(sorted(SeqIds))
                        outFile.write(line)
        print SetsInspected
        print len(SetsInspected)
        outFile.close()
				
def redundant(reference, minTaxa):
        """"Proudeces Orthogroups with at least N different OTU's, allowing redundancy but removing orthogroups made of exclusively one OTU """
        inFile = open(reference, "rw")
	outFile =open("redundantsOG_%s.txt", "w" %reference)
        SetsInspected = []
        for line in inFile:
		spp = re.findall(r'[A-Z]_[a-z]+', line)
		SeqIds = line.strip('\n').split(', ')
                nr = set(spp)
                if len(nr) >= int(minTaxa) and sorted(SeqIds) not in SetsInspected:
                        SetsInspected.append(sorted(SeqIds))
                        outFile.write(line)
        outFile.close()



def retrieve_fasta(in_file, Outdir, Type, Reference):
        """ Takes a series of sequence comma separated Identifiers from orthogroups (one per line), and produces fasta files for each orthoGroup (line) """
        handle = open(in_file, 'r')
        if not os.path.exists(Outdir):
                os.makedirs(Outdir)
        else:
                print 'The output dir already exist!'
        OG_number = 0
        seqSource = SeqIO.to_dict(SeqIO.parse(open(Reference), 'fasta'))
        for line in handle:
		if len(line) > 0: # do not process empty lines
			line = line.replace(' ', '' ) # remove white spaces
			qlist = line.strip('\n').split(',')
                        if line.startswith('#'):
                                Name = qlist.pop(0)
                                OutFileName = Name.strip('#') + '.fasta'
                                OG_out_file = open(Outdir+ '/' + OutFileName, 'w')
                        else:
                                OG_filename = Type + "_" + str(OG_number) + ".faa" 
                                OG_outfile = open(Outdir+ '/' + OG_filename, 'w')
			for seqId in qlist:
                        SeqIO.write(seqSource[seqId], OG_outfile, 'fasta')
			OG_number += 1
			print "successfully created %s" % OG_filename 
			OG_outfile.close()
