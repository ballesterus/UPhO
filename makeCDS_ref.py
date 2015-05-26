#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from sys import argv
import os
import re
from Bio import SeqIO


def regexKey(pattern, Dic):
	for K in Dic.iterkeys():
		if re.search(pattern, K):
			return K


def retrieve_fasta(in_file, Outdir, Ref1):
        """ Takes a series of sequence comma separated Identifiers from orthogroups (one per line), and produces fasta files for each orthoGroup (line) """
        handle = open(in_file, 'r')
        Probl = open('Problematics.out', 'w')
        if not os.path.exists(Outdir):
                os.makedirs(Outdir)
        else:
                print 'The output dir already exist!'
        Out =open(Outdir +'/F_communis_v1.cds', 'a+')
        seqSource1 = SeqIO.to_dict(SeqIO.parse(open(Ref1), 'fasta'))
        for Line in handle:
                if len(Line) > 0: # do not process empty linesq
                        query =re.findall('>(.+\|m\.[0-9]*).+', Line)
			Id = query[0].replace('|', '\|')
			Id = Id.replace('.', '\.')
			print Id
			qId = regexKey(Id, seqSource1)
			if qId != None and len(query)==1:
				SeqIO.write(seqSource1[qId],Out, 'fasta') 
                                print qId + " written"
			else:
                                Probl.write(','.join(query) + '\n')
        print 'done'

def faa_2_cds(FAA, FST_comb):
        faa = open(FAA, 'r')
        seqSource1 = SeqIO.to_dict(SeqIO.parse(open(FST_comb), 'fasta'))
        Probl = open('Problematics.out', 'w')
        Out = open('F_communis_v2.cds', 'a+')
        for line in faa:
                if line.startswith('>'):
                        query = re.findall('>([0-9a-z_|\.]+) .+', line)
                        qId = query[0] 
                        print qId
                        if qId != None:
                                SeqIO.write(seqSource1[qId], Out, 'fasta') 
                                print qId + " written"
			else:
                                Probl.write(str(qId) + '\n')
                                
faa_2_cds('T_perreirai_nr1.pep', 'T_perreira.combined2.cds')
