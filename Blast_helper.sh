#!/bin/bash
############################
#Usage:
#
# Blast_helper.sh <input.fasta> <query.fasta>
#
#Requires:
#
#    -gnu parallel
#    -blast+
# 
############################

#Global variable definitions

ldb_path='local_db'
db_type='prot'
type='blastp'
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
    echo 'Starting BLAST search' $query 'vs.' $input 'using' $type.
    cat $query | parallel  --block 100k --pipe --recstart '>' $type -evalue 0.001 -outfmt 10 -db local_db/localDB -query - > BLAST_results.csv

}


usage() {
cat <<EOF

usage: $0 <options>

This script helps the user to perform local BLAST searches for protein
homology assesment. It takes as input a file in FASTA format from
which a local BLAST database is created. This same file is use as the
query unless otherwise specified trough -q.  GNU parallel and BLAST+
should be in installed and properly cited when using this script.

-h   |  Print this help
-i   |  The input fasta file to build a   
-q   |  Specify a query file, otherwise allvsall will be performed using the "-in" file..
-p   |  Use psiblast instead of blastp


EOF
}

### Main


while getopts "hepq:i:" opt; do

    case "$opt" in
	h)
	    usage
	    exit 0
	    ;;
	
	i)
	    input=$OPTARG
	    query=$OPTARG
	    ;;

	q) 
	    query=$OPTARG
	    ;;
	
	p)
	    type='psiblast'
	    ;;


	?)
	    usage >&2
	    exit 1
	    ;;
    esac

done

shift $((OPTIND-1))


CreateBlastDB && AllvsAll;
exit $?
