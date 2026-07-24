#!/bin/bash
############################
#Usage:
#
# Diamond.sh <REFERENCE> <QUERY> <TYPE> <OUTFMT>
#
# 
#Requires:
# 
#
#    - Diamond (tested on version 2.2.4) 
# 
# 
############################

#Global variable definitions



#echo $query



#functions

CreateDiamondDB ()
{
    if ! [ -d 'dmnd_db' ]
    then
	mkdir -p 'dmnd_db';
    fi
    if ! [ -f $DB_PATH ]
    then
	diamond makedb --in ${REFERENCE} --db ${DB_PATH}
	echo "Diamond database was created"
    else
	echo "A Diamond database named ${REFERENCE%.*}.dmnd already exist. We'll use us that one"
    fi
    
}

DiamondSearch ()
{
    find dmnd_out/ -empty -delete
    if ! [ -d 'dmnd_out' ]
    then
	mkdir -p 'dmnd_out';
    fi
    if ! [ -f "${OUT_NAME}" ]
    then 
	echo "Starting DIAMOND search of  $QUERY vs. $REFERENCE using' $SE_type"
	
	diamond ${SE_TYPE} --query ${QUERY} --db ${DB_PATH} --evalue 1E-5 --outfmt ${OUT_FMT} --out ${OUT_NAME}

    else
	echo "An output file named ${OUT_NAME} exist."
    fi
}


usage() {
cat <<EOF

usage: $0 <options>

This script helps the user to perform DIAMIS searches for protein
homology assesment. It takes as input a file with sequences in FASTA format 
from which a local BLAST database is created. This same file is use as the
query unless otherwise specified trough -q. 

Diamond should be in installed and properly cited when using this script.

-h   |  Print this help
-d   |  The input FASTA file (aminoacids) to build a diamond database  
-q   |  Specify a query file, otherwise REFERENCE vs. REFERENCE will be performed using the file provided as  "-d" .
-t   |  Specify the Diamond algorithm to use:  blastp (default), blastx
-f   |  Specify the output format to use defaukl = "outfmt -6"

EOF
}

### Main
OPTIND=1
while getopts "htf:q:d:" opt; do

    case "${opt}" in
	h)
	    usage
	    exit 0
	    ;;
	
	d)
	    REFERENCE=$OPTARG
	    ;;

	q) 
	    QUERY=$OPTARG
	    ;;
	
	t)
	    SE_TYPE=$OPTARG
	    ;;
	f)
	    OUT_FMT=$OPTARG
	    ;;
	
	'?')
	    usage 
	    exit 1
	    ;;
	:)
	    usage
	    exit 1
	    ;;
    esac

done

shift $((OPTIND-1))
if [ "$QUERY" = "" ]
then
    QUERY=$REFERENCE
fi

if [ "$SE_TYPE" = "" ]
then
    SE_TYPE="blastp"
fi

if [ "$OUT_FMT" = "" ]
then
    OUTFMT="6"
fi

if [ "$REFERENCE" = "" ]
then
    echo "ERROR: Input file needed [-d]"
    
    exit 1
else
    SE_TYPE="blastp"
    DB_PATH="dmnd_db/${REFERENCE%%.*}.dmnd"
    OUT_NAME="dmnd_out/${QUERY%%.*}_v_${REFERENCE%%.*}.dout"
    OUT_FMT="6"

    echo $DB_PATH
    echo $QUERY
    CreateDiamondDB
    DiamondSearch
fi

exit $?
