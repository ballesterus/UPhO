#!/bin/bash

######################################################################
# paMATRAX*.sh: A shell script for sequentially execute multiple 
# sequence alignment (mafft), trimming (trimAl) and tree-estimation 
#(raxml or fastree).
# If you use this script you should cite the actual
# programs in the dependencies list: 
# 
# The following programs are required and should be referenced
# in the  $PATH.
#
#  *gnu-parallel
#  *raxmlHPC 
#  *trimal
#  *iqtree
#  *FastTree  
#  *mafft 
#  *Al2Phylo.py
######################################################################

#Program specific commands. User should modify this accordingly.
mafft_cmd="mafft --anysymbol --auto --quiet --thread 2"
trimal_cmd="trimal -fasta -gappyout"
raxml_cmd="raxmlHPC-PTHREADS-AVX -f a -p $RANDOM -x $RANDOM -#100 -m PROTGAMMAAUTO -T 4"
iqtree_cmd="iqtree -st AA -fast -mset LG,WAG,JTT,DAYHOFF  -lbp 1000 -nt AUTO"
fasttree_cmd="fasttree -slownni -wag"
Al2Phylo_cmd="Al2Phylo.py -m 50 -p 0.50 -t 4"

export mafft_cmd
export trimal_cmd
export raxml_cmd
export Al2Phylo_cmd
export fasttree_cmd
export iqtree_cmd
#Initialize variables
EXT="fasta"
AFLAG=1
TFLAG=1
SFLAG=1
CFLAG=0
TinEXT='.al'
TREE_BUILDER=0

usage() {
cat <<EOF

usage: $0 <options>

This script runs the phylogenetic pipeline: Align -> Trim-> Sanitize-> Tree
on all sequences in the current working directory. It calls  gnu-parallel, mafft, trimAL, RAxML or
FastTree. If an output file is found it would be skipped.
Please cite the appropriate programs used on each step.

-h  |  Print this help
-e  |  Extension of the unaligned sequences (default: fasta)
-a  |  Stop after alignment
-t  |  Stop after trimming
-s  |  Stop after sanitation
-c  |  Trim (trimAl) and sanitize trimmed alignments (Al2Phylo)
-f  |  Use FastTree for building trees (default raxml).
-q  |  Use IQ-Tree or building trees
    
These are the default parameters for each program. Modify accordingly:

    mafft:    $mafft_cmd
   trimAl:    $trimal_cmd
 Al2Phylo:    $Al2Phylo_cmd
    raxml:    $raxml_cmd
 fasttree:    $fasttree_cmd
   iqtree:    $iqtree_cmd
EOF
}

while getopts "he:atscfq" opt; do

    case "$opt" in
	h)
	    usage
	    exit 0
	    ;;
	e)
	    EXT=$OPTARG
	    ;;
	a) 
	    AFLAG=0
	    ;;
	t)
	    TFLAG=0
	    ;;
	s)
	    SFLAg=0
	    ;;
	c)
	    CFLAG=1
	    ;;
	f)
	    TREE_BUILDER=1
	    ;;
	q)
	    TREE_BUILDER=2
	    ;;
	?)
	usage >&2
	exit 1
	;;
    esac

done

main () {
    printf "\nStarting MSA"
    parallel --env mafft_cmd -j+0 'if [ ! -e {.}.al  ]; then $mafft_cmd {} > {.}.al 2>>mafft.log; fi' ::: *.$EXT;
    printf "\nAll alignemnets are completed. Alignments files writen with extension with extension .al"
    if [ $AFLAG -eq 0 ]
    then
	printf "\nPipeline stopped after alignment."
	exit 0
    else
	if [ $CFLAG -eq 1 ]	
	then
	    printf "\n\nStarting trimming using trimal."
	    parallel --env trimal_cmd  -j+0 'if [ ! -e {.}.fa  ]; then $trimal_cmd -in {} -out {.}.fa; fi' ::: *.al;     
	    printf "\nAll alignments were trimmed. Trimmed alignments written with extension .fa"
	    if [ $TFLAG -eq 0 ]
	    then
		printf "\nPipeline stoped after trimming."
		exit 0
	    else
		printf "\n\nStarting cleaning"
		parallel --env Al2Phylo_cmd -j+0 'if [[ ! -e {.}_clean.fa && ! -e {= s:_clean\.fa::; =}_clean.fa ]]; then $Al2Phylo_cmd -in {} >> Al2Phylo.log; fi' ::: *.fa; 
		TinEXT='_clean.fa'
		printf '\nAll alignments were cleaned. Cleaned alignments end with _clean.fa'
	    fi    
	    
	    if [ $SFLAG -eq 0 ]
	    then
		printf "\nPipeline stopped after sanitation."
		exit 0		
	    fi
	fi
	if [ $TREE_BUILDER -eq 2 ]
	then
	    printf "\n\nStarting tree estimation using iqtree"
	    parallel --env iqtree_cmd -j+0 'if [ ! -e {.}.tre  ]; then  $iqtree_cmd  -s {}  2>> iqtree.log; fi' ::: *$TinEXT;
	else if [ $TREE_BUILDER -eq 1 ]
	     then
		 printf "\n\nStarting tree estimation using FastTree"
		 parallel --env fasttree_cmd -j+0 'if [ ! -e {.}.tre  ]; then  $fasttree_cmd  {} > {.}.tre  2>> fasttree.log; fi' ::: *$TinEXT;
	     else
		 printf "\n\nStarting tree estimation using raxml"
		 parallel --env raxml_cmd -j+0 'if [ ! -e RAxML_info.{.}.out  ]; then  $raxml_cmd -s {} -n {.}.out 2>> raxml.log; fi' ::: *$TinEXT;
	     fi
	fi
    fi	
}
	    

shift $((OPTIND-1))
als=`ls -1 *.$EXT 2>/dev/null | wc -l` 
#printf $als
if [ $als -lt 1 ]
then
    printf "ERROR: No input files found in the current directory"
else
    find . -empty -delete
    printf "\n%s%d%s" "There are " $als " files found in the current directory." 
    main
    printf "\n\nAll files in the directory have been processed. We are done with paMATRAX+.\n"
fi
exit

