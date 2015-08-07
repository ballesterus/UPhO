#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import argparse
import os
import re


parser = argparse.ArgumentParser(description='This scrip produces clusters of homologs from a csv formatted blast output file.')
parser.add_argument('-in', dest = 'input', type = str, default= 'None', help = 'Blast output file to process')
parser.add_argument('-s', dest= 'separator', type =str, default= 'False', help ='Custom character separating the otu_name from the sequence identifier')
parser.add-argument('-r' dest= 'type',  type =str, default= 'r', help ='Specify is cluster can contain more than one sequnce per species (r) or only single copy (sc) clusters')
parser.add-argument('-mcl' dest= 'mcl' type = bool, default= 'False', help = 'When true, a "abc" filer is produce for use in the Markov Cluster Algorithm.')
parser.add-argument('-e' dest='expectation', type=str, default = '1e-5', help ='Additional expectation value trhreshold, default 1e-5')
parser.add-argument('-m' desr='minTaxa', type=str, default = '4', help = 'minimum number of different taxa to keep in each cluster')
args = parser.parse_args()


#Global variables

sep=args.separator
gsep =re.escape(sep)

#Function definitions

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



def clusters(blastout, expectation):
        """This function take two arguments: 1) the blast csv output, and 2) an E Value threshold for the formation of clusters. The output is text file with the identifiers of the sequenes clustered  on a single line, a hidden parameter in this function is the alignment lenght, Im using 50 ut can be  modified."""
	myOut = open("cluster_%s.txt", 'w' %expectation)
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

def non_redundant(reference, minTaxa):
        """This function filters out clusters with redundant species. Takes as input a cluster file, like the one produces by the fuction clusters, and a minimum number of different species"""

	inFile = open(reference, 'rw')
	outFile =open("non_redundantOG.txt", "w")
        SetsInspected = []
        for line in inFile:
                spp = re.findall(r'([A-Z_a-z0-9]+)%s', line %gsep)
                SeqIds = line.strip('\n').split(', ')
                nr = set(spp)
                if len(spp) == len(nr) and len(spp) >= int(minTaxa) and sorted(SeqIds) not in SetsInspected:
                        SetsInspected.append(sorted(SeqIds))
                        outFile.write(line)
        print SetsInspected
        print len(SetsInspected)
        outFile.close()
				
def redundant(reference, minTaxa):
        """Proudeces homolog-groups with at least N different OTU's, allowing redundancy but removing groups made of exclusively one OTU """
        inFile = open(reference, "rw")
	outFile =open("redundants_%s.txt", "w" %reference)

        SetsInspected = []
        for line in inFile:
		spp = re.findall(r'[A-Z0-9_a-z]+%s', line %gsep)
		SeqIds = line.strip('\n').split(', ')
                nr = set(spp)
                if len(nr) >= int(minTaxa) and sorted(SeqIds) not in SetsInspected:
                        SetsInspected.append(sorted(SeqIds))
                        outFile.write(line)
        outFile.close()


def retrieve_fasta(in_file, Outdir, Type, Reference):
	from Bio import SeqIO
        """ Takes a series of sequence comma separated Identifiers from orthogroups (one per line), and produces fasta files for each orthoGroup (line) """
        handle = open(in_file, 'r')
        if not os.path.exists(Outdir):
                os.makedirs(Outdir)
        else:
                print 'The output directory already exist!'
        OG_number = 0
        seqSource = SeqIO.to_dict(SeqIO.parse(open(Reference), 'fasta'))
        for line in handle:
		if len(line) > 0: # do not process empty lines
                        line = line.replace(' ', '' ) # remove white spaces
			qlist = line.strip('\n').split(',')
                        if line.startswith('#'):
                                Name = qlist.pop(0)
                                OG_filename = Name.strip('#') + '.faa'
                                OG_outfile = open(Outdir + '/' + OG_filename, 'w')
                        else:
                                OG_filename = Type + "_" + str(OG_number) + ".faa" 
                                OG_outfile = open(Outdir + '/' + OG_filename, 'w')
                                OG_number += 1
			for seqId in qlist:
                                SeqIO.write(seqSource[seqId], OG_outfile, 'fasta')
			print "successfully created %s" % OG_filename 
			OG_outfile.close()



#MAIN

#MAIN
if __name__ == "__main__":
	clusters(args.input, args.expectation)
	if args.type == 'r':
		redundant('clusters_%s.txt', args.minTax % args.expectation)
		retrive_fasta(,'r_clusters', 'bcl' )
		
	elif args.type =='sc':
		non_redundant('clusters_%s.txt', args.minTax % args.expectation)
	
