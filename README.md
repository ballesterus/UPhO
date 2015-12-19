# UPhO

UPhO find orthologs with and without inparalogs from input gene family trees. Reter to the Documentation.pdf for instructions on usage installation and dependencies. Type UPhO.py -h for help.

The only input requierement for UPhO is a tree (or trees) in newick format in which the leaves are named with a species idenfifier, a field separator, and sequence identifier. By defauul the field separator is the charateer "|"  but custom delimiters can be defined. Examples of trees to test UPhO are provided in the  TestData folder.

Additional scripts are provided for a variety of task including:

<li>**minreID.py**  Rename sequence identifiers adding species (OTU) name and field delimiters character.
<li>**blast_helper.sh** Assist in  all vs. all blastp search.
<li>**BlastResultCluster.py** Cluster genes in gene families based on e vales threshold and a minimum number of OTUs.
<li>**paMATRAX+.sh** Wrapper of gnu-parallel mafft, trimAl and raxml (or fastree) for parallel estimation of phylogenetic trees..
<li>**UPhO.py** The orthology evaluation tool. 
<li>**Get_Fasta_from_Ref.py** Create fasta files from lists of sequence identifiers.
<li>**Al2phylo.py** A script to prepare MSA for phylogenetic inference with sanitation and representative sequences options.
<li>**Consensus.py**  Find conserved regions in MSA. Not quite useful for this pipeline... I might move it at some point somewhere else.
<li>**distOrth.py** Functions for annotating the didtribution of orthologs on a tree.
<li>**distOrth_interactive.py** interactive helper for distOrth.

Each script has its own  -help flag for detail on its usage.
