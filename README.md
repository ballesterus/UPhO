# UPhO

<img src="/misc/UPhO_logo.png" width="250" align="left"> UPhO finds orthologs with and without inparalogs from input gene family trees. Refer to the Documentation.pdf for more detailed explanations on its usage, installation and dependencies. Type UPhO.py -h for help.

The only input requierement for UPhO is a tree (or trees) in Newick format in which the leaves are named with a species idenfifier, a field separator, and sequence identifier. By default, the field separator is the character "|"  but custom delimiters can be defined. Examples of trees to test UPhO are provided in the TestData folder.

Additional scripts are provided for a variety of task including:

<li>**minreID.py**  Renames sequence identifiers adding species (OTU) name and field delimiters character.
<li>**blast_helper.sh** Assists in  all vs. all blastp search.
<li>**BlastResultCluster.py** Clusters genes in gene families based on e values threshold and a minimum number of OTUs.
<li>**paMATRAX+.sh** Wrapper of gnu-parallel mafft, trimAl and RAxML (or FastTree) for parallel estimation of phylogenetic trees.
<li>**UPhO.py** The orthology evaluation tool.
<li>**UPhO_wt.py** UPhO with an additional parameter to tolerate some (n) paralogous. Maybe useful in cases where few spurious or misplaced sequences discard  a whole orthogroup. Also, this feature could be useful for rooting this orthobranch. 
<li>**Get_Fasta_from_Ref.py** Creates fasta files from lists of sequence identifiers.
<li>**Al2phylo.py** A simple script to prepare MSA for phylogenetic inference with sanitation and representative sequences options.
<li>**Consensus.py**  Finds conserved regions in MSA. Not quite useful for this pipeline... I might move it somewhere else or repurpose it.
<li> **Alistats.py**  Writes a simple report as (tsv) from input alignments, includind number of species, GC content, and gaps content.
<li>**distOrth.py** Functions for annotating the distribution of orthologs on a tree.
<li>**distOrth_interactive.py** interactive helper for distOrth.

Each script has  (or should have) its own  -help flag for details on its usage, .

##Disclaimer:

This software is experimental, in active development and comes without warranty.
UPhO scripts were developed and tested using Python 2.7 on Linux (RHLE and Debian) and MacOS. Versions of these scripts using Python3 are being tested.

##Citation

Ballesteros JA and Hormiga G. 2016. A new orthology assessment method for phylogenomic data: Unrooted Phylogenetic Orthology.
*Molecular Biology and Evolution*, doi: 10.1093/molbev/msw069<url>
