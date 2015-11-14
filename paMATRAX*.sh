#!/bin/sh
######################################################################
# paMATRAX*.sh: A shell script for sequentially execute multiple 
# sequence alignment (mafft), trimming (TRimal) and tree-estimation (raxml or fastree).
# Of you use this script you should cite all programs in the dependencies: 
# 
# The following programs are requiered and should be installed in the 
# $PATH. Depeending on your 
#
#  *gnu-parallel
#  *raxmlHPC 
#  *trimal 
#  *FastTree  
#  *mafft 
#  *Al2Phylo.py
######################################################################

mafft_cmd='mafft --anysymbol --auto --thread 2'
trimal_cmd=
raxml_cmd=
fastree_cmd=
Al2Phylo_cmd=

case {<<EOF
usage: %0 options

This script runs the phylogetic pipeline Align -> Trim-> Sanitize-> Tree
on all sequences on the cwd. It calls  gnu-parallel, mafft, trimAL, RAxML or
FastTree. Users should inspect and modify this script accordingly.
Please cite the appropiate programs used on each of the steps.

-h  |  Print this help
-e  |  Extension if the unaligned sequences (deafault: fasta)
-a  |  Stop after alignment
-t  |  Stop after trimming
-s  |  Stop after sanitation
-c  |  Sanitize trimmed alignments with Al2Phylo.py
-f  |  Use FastTree for building trees (default raxml).

This are the default parameters for each program. Modify accordingly:



EOF
}

if [ $# -eq 0 ] 
then Tree_estimator='X' 
else Tree_estimator=$1 
fi

echo $Tree_estimator

#Part I. MSA using mafft on all files  in the cwd with estension ''
als=`ls -1 *.al 2>/dev/null | wc -l` 
if [ $als = 0 ]
then parallel -j+0 $mafft_cmd {} > {.}.al' ::: *.fasta; 
else echo "There are $als aligment files (*.al) in the working folder. Will procede with trimming" 
fi
#Part II: Masking gappy regions with trimal
#Test if trimmed als exits in the wd 
# Edit masking parameters in line 43
trims=`ls -1 *.fa 2>/dev/null | wc -l` 
if [ $trims = 0 ]
then parallel -j+0 'trimal -in {} -out {.}.fa -fasta -gappyout' ::: *.al; 
else 
echo "There are $trims trimed aligment files (*.fa) in the working folder. Will procede with tree estimation" 
fi

#Test if trees exist in the WD 
trees=`ls -1 *.tre 2>/dev/null | wc -l`
if [ $trees = 0 ] 
then 
    if [ $Tree_estimator == 'F' ] 
    then parallel -j+0 'FastTreeMP {} > {.}.tre' ::: *.fa;
    elif [ $Tree_estimator == 'X' ] 
    then parallel -j+0 'raxmlHPC-AVX -s {} -f a -p12345 -x12345 -#1000 -m PROTGAMMAAUTO -n {.}.rxOUT' ::: *.fa;
    fi 
else echo "There are $trees tree files (*.tre) in the working folder" echo "Nothing else to do. Good Bye" 
fi
