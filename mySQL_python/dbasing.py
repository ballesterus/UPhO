#!/usr/bin/env python

from add_record_2DB import *
from termcolor import colored


welcome = colored('WELCOME TO THE INTERFACE THE CL INTERFACE TO INPUT DATA IN TO mySpecimens database', 'red', attrs=['bold'])
print(welcome)

Mydb = MySQLdb.connect(host="localhost", user="root", passwd="", db="mySpecimens", charset='utf8')
Mycursor = Mydb.cursor()

e = True
while e == True:
    
    print """What do you ant to do?',
    '1) Add a specimen?',
    '2) Add determination to an existing specimen',
    '3) Add a new locality'
    '4) Add a new collection event'
    '5) EXIT'"""
    selection = raw_input('Enter your selection: ')
    if selection == '5':
        e = False
        quit()
    elif selection == '1':
        add_specimen()
    else:
        print 'Under construction, come back later.x'

db_close()
