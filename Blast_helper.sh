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
input=$1
query=$2

if [ -z "$2"  ]
then query=$1
fi

#echo $query


#functions

CreateBlastDB ()
{
    if ! [ -d $ldb_path ]
    then mkdir $ldb_path;
	echo 'Creating local blast database at ' ldb_path  
    fi
    makeblastdb -dbtype $db_type -in $input -input_type fasta -out local_db/localDB
}

AllvsAll ()
{
    echo 'Starting All vs All'
    cat $query | parallel  --block 100k --pipe --recstart '>' blastp -evalue 0.001 -outfmt 10 -db local_db/localDB -query - > BLAST_results.csv

}

### Main
CreateBlastDB
AllvsAll
exit $?
