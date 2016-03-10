#!/bin/sh
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
#  *FastTree  
#  *mafft 
#  *Al2Phylo.py
######################################################################

#Program specific commands. User should modify this accordingly.
mafft_cmd="mafft --anysymbol --auto --thread 2"
trimal_cmd="trimal -fasta -gappyout"
raxml_cmd="raxmlHPC-AVX -f a -p 767 -x 97897 -#100 -m PROTGAMMAUTO"
fasttree_cmd="FastTreeMP"
Al2Phylo_cmd="Al2Phylo.py -m 50 -p 0.50"

export mafft_cmd
export trimal_cmd
export raxml_cmd
export Al2Phylo_cmd
export fasttree_cmd

#Initialize variables
EXT="fasta"
AFLAG=1
TFLAG=1
SFLAG=1
CFLAG=0
TinEXT='_clean.fa'
TREE_BUILDER=0

function usage() {
cat <<EOF

usage: $0 <options>

This script runs the phylogetic pipeline Align -> Trim-> Sanitize-> Tree
on all sequences in the cwd. It calls  gnu-parallel, mafft, trimAL, RAxML or
FastTree. If an output file is found it would be skipped.
Please cite the appropriate programs used on each step.

-h  |  Print this help
-e  |  Extension of the unaligned sequences (default: fasta)
-a  |  Stop after alignment
-t  |  Stop after trimming
-s  |  Stop after sanitation
-c  |  Sanitize trimmed alignments with Al2Phylo.py
-f  |  Use FastTree for building trees (default raxml).

These are the default parameters for each program. Modify accordingly:

    mafft:    $mafft_cmd
   trimAl:    $trimal_cmd
 Al2Phylo:    $Al2Phylo_cmd
    raxml:    $raxml_cmd
 fasttree:    $fasttree_cmd

EOF
}

while getopts "he:atscf" opt; do

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
	s) SFLAg=0
	    ;;
	c) CFLAG=1
	    ;;
	f)
	    TREE_BUILDER=1
	    ;;
	?)
	    usage >&2
	    exit 1
	    ;;
    esac

done

function main () {
    echo "Starting MSA"
    parallel --env mafft_cmd  -j+0 'if [ ! -e {.}.al  ]; then $mafft_cmd {} > {.}.al 2>>mafft.log; fi' ::: *.$EXT;
    if [ $AFLAG -eq 0 ]
    then
	echo "Pipeline stopped after alignement."
	exit 0
    else
	echo "Starting trimming"
	parallel --env trimal_cmd  -j+0 'if [ ! -e {.}.fa  ]; then $trimal_cmd -in {} -out {.}.fa; fi' ::: *.al;     
	
	if [ $TFLAG -eq 0 ]
	then
	    echo "Pipeline stoped after trimming."
	    exit 0
	else
	
	    if [ $CFLAG -eq 1 ]
		
	    then
		echo "Starting cleaning"
		parallel --env Al2Phylo_cmd -j+0 'if [ ! -e *cleaned.fa ]; then $Al2Phylo_cmd -in {} >> Al2Phylo.log; fi' ::: *.fa; 
		TinEXT='_clean.fa'
	    fi    
	    
	    if [ $SFLAG -eq 0 ]
	    then
		echo "Pipeline stopped after sanitation."
		exit 0
	    else		
		if [ $TREE_BUILDER -eq 0 ]
		then
		    echo "Starting tree estimation with raxml"
		    parallel --env raxml_cmd -j+0 'if [ ! -e RAxML_info.{.}.out  ]; then  $raxml_cmd -s {} -n {.}.out 2>> raxml.log; fi' ::: *$TinEXT;
		else
		    echo "Starting tree estimation with FastTree"
		    parallel --env fasttree_cmd -j+0 'if [ ! -e {.}.tre  ]; then  $fasttree_cmd  {} > {.}.tre  2>> fasttree.log; fi' ::: *$TinEXT;
		fi
	    fi
	fi	
    fi
}
	    

shift $((OPTIND-1))
als=`ls -1 *.$EXT 2>/dev/null | wc -l` 
#echo $als
if [ $als -lt 1 ]
then
    echo "ERROR: No input files found in the current directory"
else
    find -empty -delete
    echo "$als files found in the current directory" 
    main
fi
exit

