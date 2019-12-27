#!/bin/bash
############################
#Usage:
#
# Blast_helper.sh <input.fasta> <query.fasta>
# Note: To produce comaparable results the effective  database size set to 34355436272, the number 
#aminoacids in uniprot release  2017_12 of 20-Dec-201
#Requires:
#
#    -gnu-parallel
#    -blast+ (tested with versions 2.2.30)
# 
############################

#Global variable definitions

ldb_path='local_db'
db_type='prot'
type=''
input=''
query=''


#echo $query



#functions

CreateBlastDB ()
{
    if ! [ -d $ldb_path ]
    then mkdir $ldb_path;
	echo 'Creating local blast database at ' ldb_path  
    fi
    makeblastdb -dbtype $db_type -in $input -input_type 'fasta' -out local_db/localDB
}

AllvsAll ()
{
    find . -empty -delete
    echo 'Starting BLAST search' $query 'vs.' $input 'using' $type.
    if [ ! -e BLAST_results_${query%.*}.csv ]
    then
	cat $query | parallel --block 100k --pipe --recstart '>' $type -evalue 0.001 -outfmt 10 -db local_db/localDB -dbsize 34355436272 -query - > BLAST_results_${query%.*}.csv
    else
	echo 'A BLAST output file matching the query name exist in the wd.'
	#Lets try to restart the BLAST search from where it was left.
	# Firts lets see what is the last record written  to the output file
	last=`tail -n1 BLAST_results_${query%.*}.csv | cut -f 1 -d ','`
	qline=`grep -n  $last $query | cut -f 1 -d ':'`
	#remove last query from the output
	sed -i -e "/^"$last"/d" BLAST_results_${query%.*}.csv
	#start from previous last query
	echo "Re-starting from line:" $qline "=" $last 
	tail -n +$qline $query | parallel  --block 100k --pipe --recstart '>' $type -evalue 0.001 -outfmt 10 -db local_db/localDB -dbsize 34355436272  -query - >> BLAST_results_${query%.*}.csv
    fi
}


usage() {
cat <<EOF

usage: $0 <options>

This script helps the user to perform local BLAST searches for protein
homology assesment. It takes as input a file with sequences in FASTA format 
from which a local BLAST database is created. This same file is use as the
query unless otherwise specified trough -q.  GNU parallel and BLAST+
should be in installed and properly cited when using this script.

-h   |  Print this help
-i   |  The input FASTA file (aminoacids) to build a BLASTDB   
-q   |  Specify a query file, otherwise all vs. all will be performed using the "-i" file.
-t   |  Specify the blast algorithm to use:  blastp (defaukt), blastx, or psiblast


EOF
}

### Main
OPTIND=1
while getopts "ht:q:i:" opt; do

    case "${opt}" in
	h)
	    usage
	    exit 0
	    ;;
	
	i)
	    input=$OPTARG
	    ;;

	q) 
	    query=$OPTARG
	    ;;
	
	t)
	    type=$OPTARG
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
if [ "$query" = "" ]
then
    query=$input
fi

if [ "$type" = "" ]
then
    type="blastp"
fi


if [ "$input" != "" ]
then
    if ls local_db/localDB* 1> /dev/null 2>&1;
    then
	echo "A local BLAST database exist, proceeding to the search step";
	AllvsAll;
    else
	echo "Creating local BLAST database."
	CreateBlastDB && AllvsAll;
    fi
else
    echo "ERROR: Input file needed [-i]"
    exit 1
    
fi
exit $?
