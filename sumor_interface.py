#! /usr/bin/env python
import os
from sumor import *

##### YEAH_SHOWDOWN ######

print "This script will help us annotate a phylogenies, from a colection of fasta (orthologs) .Select from the following options"
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

    print """Select from the following options:
    
    1: Create a OG_sumary file
    2: Annotate and load tree (loads summary).
    3: Plot(see) the tree.
    4: Save  current tree image or load and savea new tree to image file (PDF, SVG or PNG).
    5: Select a node and query the composition on specific node (requires loaded tree).
    6: Return non-redundant orthogroups, from all in summary or from selected node, and save to file (.txt) 

    q: Exit"""
    selection = raw_input("Enter your selection: ")
    if selection  not in ['1','2','3','4', '5', '6','q']:
        print "ERROR type the number of your selection"
    elif selection == '1':
        W_path = raw_input('Select the Path to process: ')
        Pattern = raw_input('Type the extension of files to process: ')
        os.chdir(W_path)
        line_writer(Pattern)
        print "Orthology composition written to OG_summary.csv" 

    elif selection == '2':
        Tree = raw_input('Input name of tree file (newick): ')
        Summary = raw_input('Input OG_summary file: ')
        T = tree_ortho_annotator(Summary, Tree)
    
    elif selection == '3':
        B_size=  float(raw_input('Bubble ize factor: '))
        ts =tree_plot(T, B_size)
        T.show(tree_style=ts)
    elif selection == '4':
        B_size=  float(raw_input('Bubble ize factor: '))
        name = raw_input('Name of otput image file: ')
        Type = raw_input('Type of file (pdf, svg, or  png: ')
        OutName = name + '.' + Type
        ts =tree_plot(T, B_size)
        T.render(OutName, tree_style = ts)
        
    elif selection=='5':
        if T ==None:
            print 'Error: first load a tree:' 
        else:
            NodeNum = raw_input('Select  a node number from the tree above: ' )
            Result = get_orthoSet_by_node(T, str(NodeNum))
            NodeS = [NodeNum, Result]
            print NodeS

    elif selection == '6':
        if Summary == None:
            print "ERROR: load a summary and a tree first."
        else:
            print "Loading Ortholgs and sequence compostion"
            Ogs = OGSummary_to_Dict(Summary)
            nOgs= No_OG_subsets(Ogs)
            while selection =='6':
                print "Redundancies esolved and log file written to OG_clean.log"
                print """Options:
                1: Create resolved OG from ALL orthologs in Summary.
                2: Create resolved OG from ortholgs in SELECTED node.
                3: Do Nothing.
                """
                answer=raw_input('Select option from above: ') 
                if answer not in ['1','2','3']:
                    print "ERROR select the number of the option"
                elif answer == '1':
                    Out =open('NS_ortho_from_AlL.txt', 'w')
                    for k, v in nOgs.iteritems():
                        line = ','.join(v) + '\n'
                        Out.write('#' + k + ',')
                        Out.write(line)
                elif answer =='2':
                    if NodeS==None:
                        print 'Error: No node is selected'
                    else:
                        OName ='NS_ortho_from_node_%s.txt' % NodeS[0]
                        Out =open(OName, 'w')
                        for entry in NodeS[1]:
                            if entry in nOgs.keys():
                                line =','.join(nOgs[entry]) + '\n'
                                Out.write('#' + entry + ',')
                                Out.write(line)
                elif answer =='3':
                    selection = None
    elif selection=='q':
        Q = False
