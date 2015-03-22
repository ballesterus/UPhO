#! /usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv
import re
import os
import sqlite3

"""Creates, populates database for trasncritome-orthology pipeline.
"""

#PART I: Create new  SQLITE3 database & schema IF one does not exist.
conn = sqlite3.connect('masterDB.sql')
c = conn.cursor()
c.execute("PRAGMA foreign_keys = ON;")
c.execute('''CREATE TABLE IF NOT EXISTS Species
(Species_ID INTEGER PRIMARY KEY UNIQUE,
Genus TEXT,
Species TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS Transcript
(Transcript_ID  INTEGER PRIMARY KEY UNIQUE,
FastaHeader TEXT,
Name TEXT,
Len TEXT,
FastaSeq TEXT,
Species_ID INTEGER,
FOREIGN KEY(Species_ID) REFERENCES Species(Species_ID)
);''')

c.execute('''CREATE TABLE IF NOT EXISTS CDS
(CDS_ID INTEGER PRIMARY KEY UNIQUE,
FastaHeader TEXT,
TranscripttName TEXT,
SeqAA TEXT,
SeqNT TEXT,
STranscript INTEGER,
FOREIGN KEY(STranscript) REFERENCES Transcript(Transcript_ID)
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


#PART II. Function definitions to query and populate the database

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


def search_Sp(query):
    sql = "SELECT * FROM Species WHERE Species LIKE '%s' OR Genus LIKE '%s';" % (query, query)
    c.execute(sql)
    result = c.fetchall()
    print result


def Insert_Sp():
    Genus = raw_input('Type the Genus: ')
    Species = raw_input('Type the species: ')
    sql = "INSERT INTO Species VALUES (NULL, '%s', '%s');" % (Genus, Species)
    print sql
    c.execute(sql)
    conn.commit()


def Insert_Transcripttome(File, SpCode):
    SpCode = int(SpCode)
    Records = Fasta_Parser(File)
    for Key in Records.iterkeys():
        Name = Key.split(' ')[0]
        Len = Key.split(' ')[1]
        Len = int(Len.replace('len=',''))
        sql ="INSERT INTO Transcript VALUES (NULL, '%s', '%s', %d, '%s', %d);" % (Key,Name, Len,  Records[Key], SpCode)
        c.execute(sql)
        conn.commit()



def Is_NT_or_AA(String):
    ''' Returns AA is the sequence ismade of aminoacids, NT if is made of nucleotides'''
    NT= ('A','C','G','T','U','R','Y','K','M','S','W','B','D','H','V','N')
    AA =('A','B','C','D','E','F','G','H','I','K','L','M','N','P','Q','R','S','T','U','V','W','Y','Z','X')
    Comp = set(String)
    if all([i in NT for i in Comp]):
        return 'NT'
    elif all([i in AA for i in Comp]):
        return 'AA'
    else:
        return 'Not valid sequence'
    
        
def Insert_CDS(File, SpId):
    Records = Fasta_Parser(File)
    for Key in Records.iterkeys():
        sql = "SELECT CDS_ID FROM CDS WHERE FastaHeader LIKE '%s'" % Key
        c.execute(sql)
        Check = c.fetchall()
        if len(Check) == 0: #The CDS is not in the Database. Enter CDS
            TName = Key.split['|'][0]
            sql = "SELECT TranscriptId FROM Transcript WHERE SpeciesId = %d AND NAME = %s" % (SpId, TName)
            c.execute(sql)
            TrasncriptId = c.fetchall()
            if len(TranscripttID) == 1:
                STranscript = TrancscriptId[0]
                Type = Is_NT_or_AA(Records[Key])
                sql="INSERT INTO CDS VALUES();"
                c.execute(sql)
                conn.commit()
            else:
                print 'ERROR MORE THAN ONE TRANSCRIPT MATCH!'
                break
        elif len(Check) ==1: # The CDS is in the DB. Proceed to Update SeqData
            Type = Is_NT_or_AA(Records[Key])
            sql = "UPDATE CDS SET %sSeq =="

for record in records:
    id = record[0]
    name = record[1]
    occupation = record[2]
    location = record[3


# PART III. Interactively Populate the database
print "NOW LEST START POPULATING THE DATABASE"
print "FIRST LETS GET IN THE ORIGINAL TRANSCRIPTOME"
print "ADD TRANSDECODER PEP FILE PER SPECIES"
print "ADD THE TRANSDECODER  CDS FILE"

