#! /usr/bin/env python

import sumor

##### YEAH_SHOWDOWN ######

print "This script will help us annotate a phylogenies, from a colection of fasta (orthologs) .Select from the following options"
T = None
Q = True 
while Q == True:
    if T == None:
        print "No trees in the oven"
    else:
        print  T.get_ascii(attributes=["name"], show_internal=True)
        
    print """Select from the following options:
    
        1: Create a OG_sumary file
        2: Annotate and plot (see) the tree.
        3: Save  current tree image or load and savea new tree to image file (PDF, SVG or PNG).
        4: Query the composition on specific node (requires loaded tree).
        5: Store treatment compositions to ompare them later.

        q: Exit
        
        """
    selection = raw_input("Enter your selection: ")
    if selection  not in ['1','2','3','4', '5', 'q']:
        print "ERROR type the number of your selection"
    elif selection == '1':
        W_path = raw_input('Select the Path to process: ')
        Pattern = raw_input('Type the extension of files to process: ')
        os.chdir(W_path)
        Output = open('OG_summary.csv', 'w')
        line_writer(Pattern)
        print "Orthology composition written to %s" % Output
        Output.close()
    elif selection == '2':
        Tree = raw_input('Input name of tree file (newick): ')
        Summary = raw_input('Input OG_summary file: ')
        T = tree_ortho_annotator(Summary, Tree)
        B_size=  float(raw_input('Bubble ize factor: '))
        ts =tree_plot(T, B_size)
        Quest = raw_input('Show tree now?(y/n): ')
        if Quest == 'y':
            T.show(tree_style=ts)
    elif selection== '3':
        if T == 0:
            Tree = raw_input('Input name of tree file (newick): ')
            Summary = raw_input('Input OG_summary file: ')
            B_size=  float(raw_input('Bubble ize factor: '))
            name = raw_input('Name of otput image file: ')
            Type = raw_input('Type of file (pdf, svg, or  png: ')
            OutName = name + '.' + Type
            T = tree_ortho_annotator(Summary, Tree) 
            ts =tree_plot(T, B_size)
            T.render(OutName, tree_style = ts)
        else:
            name = raw_input('Name of otput image file: ')
            Type = raw_input('Type of file (pdf, svg, or  png: ')
            OutName = name + '.' + Type
            ts = tree_plot(T, B_size)
            T.render(OutName, tree_style = ts)
    elif selection=='4':
        if T ==None:
            print 'Error: first load a tree firts:' 
        else:
            NodeNum = raw_input('Select  a node number from the tree above?' )
            Result = get_orthoSet_by_node(T, str(NodeNum))
            print Result
    elif selection=='q':
        Q = False
