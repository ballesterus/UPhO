#! /usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv
import re
import os
import sqlite3

"""USAGE: This script finds clusters of similar sequences using NCBI blast. It provides the option of filtering groups using Salicos & Rokas (2011)  'r' parameter.
"""

#PART I: where we incorportate all soyce seqeunces into a sqlite3 database
conn = sqlite3.connect('masterDB.sql')
c = conn.cursor()
c.execute("PRAGMA foreign_keys = ON;")
c.execute('''CREATE TABLE IF NOT EXISTS Species
(Species_ID INTEGER PRIMARY KEY UNIQUE,
Genus TEXT,
Species TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS Transcrip
(Transcrip_ID  INTEGER PRIMARY KEY UNIQUE,
FastaHeader TEXT,
FastaSeq TEXT,
Species_ID INTEGER,
FOREIGN KEY(Species_ID) REFERENCES Species(Species_ID)
);''')

c.execute('''CREATE TABLE IF NOT EXISTS CDS
(CDS_ID INTEGER PRIMARY KEY UNIQUE,
FastaHeader TEXT,
SeqAA TEXT,
SeqNT TEXT,
STranscrip INTEGER,
FOREIGN KEY(STranscrip) REFERENCES Transcrip(Transcrip_ID)
);''')

c.execute('''CREATE TABLE IF NOT EXISTS Annotation
(Annotation_ID  INTEGER PRIMARY KEY UNIQUE,
FOREIGN KEY(Annotation_ID) REFERENCES CDS(CDS_ID)
);''')


c.execute('''CREATE TABLE IF NOT EXISTS Orthology
(Ortho_ID INTEGER PRIMARY KEY UNIQUE,
OrthoName TEXT,
OrthoMethod TEXT
);''')

c.execute('''CREATE TABLE IF NOT EXISTS CDS_has_Orthology
(Ortho_ID INTEGER,
CDS_ID INTEGER,
FOREIGN KEY(Ortho_ID) REFERENCES Orthology(OrthoID),
FOREIGN KEY(CDS_ID) REFERENCES CDS(CDS_ID)
);''')


class FastaRecord():
    """Class for storing sequence records and related data"""
    def __init__(self, IdLine):
        self.SeqId = IdLine.replace('\n', '').strip('>')
    

def is_ID(Line):
    if Line.startswith('>'):
        return True
    else:
        return False


def Fasta_Parser(File):
    """This function returns a dictionary containing FastaId(key) and Seqs"""
    Records = {}
    with open(File, 'r') as F:
        Seq=''
        for Line in F:
            if is_ID(Line) and len(Seq) == 0:
                Header =Line.replace('\n', '').strip('>')
            elif is_ID(Line) and len(Seq) > 0:
                Records[Header]=Seq
                Header =Line.replace('\n', '').strip('>')
                Seq = ''
            else:
                Part=Line.replace('\n','')
                Seq = Seq + Part
        Records[Header]=Seq
    return Records
    F.close()


def Insert_Trasncriptome(File, SpCode):
    SpCode = int(SpCode)
    Records = Fasta_Parser(File)
    for Key in Records.iterkeys():
        c.execute("INSERT INTO Transcrip VALUES (NULL, ?, ?, ?);", (Key, Records[Key], SpCode))


def insert_Trasnscript(SpCode, File, Type):
    if Type == 'AA':
        


print "NOW LEST START POPULATING THE DATABASE"
print "FIRST LETS GET IN THE ORIGINAL TRANSCRIPTOME"
print "ADD TRANSDECODER PEP FILE PER SPECIES"
print "ADD THE TRANSDECODER  CDS FILE"

print ""


