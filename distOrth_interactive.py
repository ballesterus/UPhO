#! /usr/bin/env python
import os
from distOrth import *

##### MAIN ######

print "This script will help us annotate a phylogenies, from a collection of fasta (orthologs). Select from the following options"
T = None
Summary= None
NodeS= None
Q = True 
while Q == True:
    os.system('clear')
    if T == None:
        print "No trees loaded."
    else:
        print  T.get_ascii(attributes=["name"], show_internal=True)
    if Summary !=None:
        print "Summary file loaded"
    if NodeS != None:
        print "The node %s is selected" %NodeS[0]
    print 'Outgroups: ' + ','.join(outgroups)


    print """Select from the following options:
    
    1: Create a OG_summary file (UPhO_orthogroups.csv can be used instead)
    2: Annotate and load tree (loads summary).
    3: Plot(see) the tree.
    4: Save  current tree image or load and save new tree to image file (PDF, SVG or PNG).
    5: Select a node and query the composition on specific node (requires loaded tree).
    6: Declare outgroups
    7: Resolve redundancies

    q: Exit"""
    selection = raw_input("Enter your selection: ")
    if selection  not in ['1','2','3','4', '5', '6','7','q']:
        print "ERROR type the number of your selection"
    elif selection == '1':
        W_path = raw_input('Select the Path to process: ')
        Pattern = raw_input('Type the extension of files to process: ')
        os.chdir(W_path)
#        line_writer(Pattern)
        OG_summary_maker(Pattern)
        print "Orthology composition written to OG_summary.csv" 

    elif selection == '2':
        Tree = raw_input('Input name of tree file (newick): ')
        Summary = raw_input('Input OG_summary file: ')
        Separator = raw_input('Field delimiter character: ' )
        T = tree_ortho_annotator(Summary, Tree)
    
    elif selection == '3':
        B_size=  float(raw_input('Bubble size factor: '))
        ts =tree_plot(T, B_size)
        T.show(tree_style=ts)
    elif selection == '4':
        B_size=  float(raw_input('Bubble size factor: '))
        name = raw_input('Name of otput image file: ')
        Type = raw_input('Type of file (pdf, svg, or  png: ')
        OutName = name + '.' + Type
        ts =tree_plot(T, B_size)
        T.render(OutName, tree_style = ts)
        
    elif selection=='5':
        if T == None:
            print 'Error: first load a tree:' 
        else:
            NodeNum = raw_input('Select  a node number from the tree above: ' )
            Result = get_orthoSet_by_node(T, str(NodeNum))
            print 'There are %d orthogroups mapped to node %s.' % (len(Result), NodeNum)
            NodeS = [NodeNum, Result]
           # In = open(raw_input('Orthogroups text file:'), 'r')
            Out = open('compo_node_%s.txt' %NodeNum, 'w' )
            for Line in Summary:
                M=Line.split(',')
                if M[0].strip('#') in Result:
                    Out.write(Line)
    elif selection =='6':
        outG = raw_input('Enter an outgroup: ')
        outgroups.append(outG)
        T = tree_ortho_annotator(Summary,Tree)

    elif selection == '7':
        target = raw_input("Name of the file to remove redundancies: ")
        print """Select an option from below:
        a:  Remove orthogrops that are subsets of others
        b:  If two orthogroups derived from the same homolog 
        and are not mutually exclusive, remove the smaller.

        """
        type_of_clean = raw_input("Selection: ")
        if type_of_clean == 'a':
            print "Removing subsets"
            No_OG_subsets(target)
        elif type_of_clean=='b':
            print("Removing overlapping orthogroups from same gene-family")
            No_Same_OG_Intesec(target)

        else:
            break
    elif selection=='q':
        Q = False
