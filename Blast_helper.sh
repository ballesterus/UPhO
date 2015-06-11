#!/bin/sh

#Global variable definitions
query=
database=
results=
ldb_path='local_db'
db_type='prot'
input=
#Defining function

function CreateBlastDB()
{
    if ! [ -d $ldb_path ]
    then mkdir $ldb_path
    fi
    makeblastdb -dbtype $db_type -in $input -input_type 'fasta'-out 'local_db/'$input
}

function AllvsAll ()
{
    echo "In construction"
}



### Main
$(CreateBlastDB)
