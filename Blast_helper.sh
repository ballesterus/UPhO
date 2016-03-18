#!/bin/sh
############################
#Usage:
#
# Blast_helper.sh <input.fasta>
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
    cat $input | parallel  --block 100k --pipe --recstart '>' blastp -evalue 0.001 -outfmt 10 -db local_db/localDB -query - > AllvsAll_results.csv

}

### Main
CreateBlastDB
AllvsAll
exit $?
