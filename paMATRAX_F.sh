#!/bin/bash
################################################################################################################################################
#paMATRAX_F: My bash script for parallel  alignmenty (mafft), trimming (TRimal) and tree-estimation (raxml or fastree)                         #
#USAGE:                                                                                                                                        #
# Call the script from the wd whet the aligned fasta files are located. The extennsion of these is expected to be '.faa'                       #
#                                                                                                                                              #
#./paMATRAX_F.sh X                                                                                                                             #                
#                                                                                                                                              #
#The script takes one  'X' of 'F' which specifies the tree estimator for raxml of fasttree respectiveely. If none is specified raxml is used.  #
#The script assumes the following dependencies are installed and in the path:                                                                  #        
# *gnu-parallel                                                                                                                                #      
# *raxmlHPC                                                                                                                                    #
# *trimal                                                                                                                                      #
# *FastTre                                                                                                                                     #
# *mafft                                                                                                                                       #
################################################################################################################################################

if [ $# -eq 0 ]
then
    Tree_estimator='X'
else
    Tree_estimator=$1
fi

echo $Tree_estimator

#Test if  aligmenets exist in the wd
als=`ls -1 *.al 2>/dev/null | wc -l`
if [ $als = 0 ] 
then
    parallel -j+0 'mafft --auto --thread 2 {} > {.}.al' ::: *.faa; 
else
    echo "There are $als aligment files (*.al) in the working folder. Will procede with trimming"
fi

#Test if trimmed als exits in the wd
trims=`ls -1 *.fa 2>/dev/null | wc -l`
if [ $trims = 0 ]
then
    parallel -j+0 'trimal -in {} -out {.}.fa -fasta -gappyout' ::: *.al;
else
  echo "There are $trims trimed aligment files (*.fa) in the working folder. Will procede with trimming"
fi

#Test if trees exist in the WD
trees=`ls -1 *.tre 2>/dev/null | wc -l`
if [ $trees = 0 ]
then
    if [ $Tree_estimator == 'F' ]
    then
	parallel -j+0 'FastTreeMP {} > {.}.tre' ::: *.fa
    elif [ $Tree_estimator == 'X'  ]
    then
	parallel -j+0 'raxmlHPC-AVX -s {} -f a -p12345  -x12345 -#100 -m PROTGAMMAAUTO -n {.}.rxOUT' ::: *.fasta
    fi
else
   echo "There are $trees tree files (*.tre) in the working folder"
   echo "Nothing else to do. Good Bye"
fi
