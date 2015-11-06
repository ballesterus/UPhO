#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import argparse
import os
import re
import glob

parser = argparse.ArgumentParser(description='This script produces clusters of homolog sequences from a csv formatted blast output file.')
parser.add_argument('-in', dest = 'input', type = str, default= None, help = 'Blast output file to process, if no input is provided the program will try to process a file with extension "csv" in the working diretory.')
parser.add_argument('-d', dest= 'delimiter', type =str, default= '|', help ='Custom character separating the otu_name from the sequence identifier')
parser.add_argument('-t', dest= 'type',  type =str, default= 'r', help ='Specify the type cluster to perform, options are to create clusters with redundancy in spp. composition (r) or find only single copy clusters (sc).')
parser.add_argument('-mcl', dest= 'mcl', action='store_true', default= False, help = "When true, a 'abc' file is produced to use as input for Markov Clustering with Stijn van Dongen's  program mcl.")
parser.add_argument('-e', dest='expectation', type=float, default = 1e-5, help ='Additional expectation value trhreshold, default 1e-5.')
parser.add_argument('-m', dest='minTaxa', type=int, default = 4, help = 'minimum number of different species to keep in each cluster.')
parser.add_argument('-R', dest='reference', type=str, default = 'All.fasta', help= 'Name of the reference file from where to extract individual squences to form cluster files, if non is provided thi is asumed to be a file named "All.fasta" in the working directory')

args, unknown = parser.parse_known_args()

#Global variables

sep=args.delimiter
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
        """This function take two arguments: 1) the blast csv output, and 2) an E Value threshold for the formation of clusters. The output is text file with the identifiers of the sequenes clustered  on a single line, a hidden parameter in this function is the alignment lenght, Im using 50 but can be  modified."""
	myOut = open("clusters_%s.txt"  % expectation, 'w')
	in_file = open(blastout, 'r')
	previous_query = ''
	for line in in_file:
		(queryId, subjectId, percIdentity, alnLength, mismatchCount, gapOpenCount, queryStart, queryEnd, subjectStart, subjectEnd, eVal, bitScore) = line.split(",")
		current_query = queryId
		if (queryId != subjectId) and (int(alnLength) >= 50) and float(eVal) <= float(expectation):
			if previous_query != current_query:
				myOut.write("\n"+current_query + "," + subjectId)
				previous_query = current_query
			else:
				myOut.write("," + subjectId)

def non_redundant(cluster, minTaxa):
        """This function filters out clusters with redundant species. Takes as input a cluster file, like the one produces by the fuction clusters, and a minimum number of different species"""
	inFile = open(cluster, 'rw')
	outFile =open("ClustNR_m%d.txt" %minTaxa, "w")
        SetsInspected = []
        for line in inFile:
                SeqIds = line.strip('\n').split(',')
		spp = spp_in_list(SeqIds, sep)
                if len(spp) == len(set(spp)) and len(spp) >= int(minTaxa) and sorted(SeqIds) not in SetsInspected:
                        SetsInspected.append(sorted(SeqIds))
                        outFile.write(line)
        outFile.close()


def spp_in_list(alist, delim):
    """Return the species from a list of sequece identifiers"""
    spp =[]
    for i in alist:
        spp.append(i.split(delim)[0])
    return spp

				
def redundant(cluster, minTaxa):
        """Produces homolog-groups with at least N different OTU's, allowing redundancy but removing groups including less than a minimum different OTUs """
        inFile = open(cluster, "rw")
	outFile =open("ClustR_m%d.txt" %minTaxa, "w" )
        SetsInspected = []
        for line in inFile:
		SeqIds = line.strip('\n').split(',')
		spp = spp_in_list(SeqIds,sep)
                nr = set(spp)
                if len(nr) >= int(minTaxa) and sorted(SeqIds) not in SetsInspected:
                        SetsInspected.append(sorted(SeqIds))
                        outFile.write(line)
        outFile.close()


#MAIN
if __name__ == "__main__":
	if args.input == None:
		print 'No blast output file was provided'
		csvs=glob.glob("*.csv")
		if len(csvs) > 0:
			csv = csvs[0]
			print 'No blast output  provided the file %s in the wd will be tried' % csv
		else:
			print 'Error: A blast output file is required to produce clusters. None available!'
	else:
		csv = args.input
	if args.mcl:
		print 'Creating a abc file for mcl'
		mcl_abc(args.input, args.expectation)
	else:
		print 'E value filtering and clustering started'
		clusters(csv, args.expectation)
		clustFile = 'clusters_%s.txt' %args.expectation
		if args.type == 'r':
			print 'minimum taxa and clustering started'
			redundant(clustFile, args.minTaxa)
                        from Get_fasta_from_Ref import Retrieve_Fasta
			Retrieve_Fasta("ClustR_m%d.txt" % args.minTaxa, 'ClusteRs', 'bcl', args.reference )		
		elif args.type =='sc':
			non_redundant(clustFile, args.minTaxa)
                        from Get_fasta_from_Ref import Retrieve_Fastaa
			Retrieve_Fasta('ClustNR_m%d.txt' %args.minTaxa,'ClusterSC', 'bcl', args.reference)
