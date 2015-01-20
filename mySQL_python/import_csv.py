#! /usr/bin/env python 
""" This scripts will import delimited text files as Tables into mySQL database.
Usage: python import_csv.py filename.csv
"""
#Modules used
from sys import argv
import re

script, csv = argv

#UNIVERSAL VARIABLES
Separator = str(raw_input('What character separates the fields?-->  ' ))
print Separator
InputFile = open(csv, 'r')
LineNum=0

for Line in InputFile:
    Line = Line.strip('\n')
    Elements = Line.split(Separator)
    if LineNum == 0:
        print 'This is the order of fields in your file:'
        print Elements
        #print DBTableColumns
        LineNum += 1
    if  LineNum > 0:
        print "Working on it"
        LineNum += 1
