# UPhO

UPhO find orthologs with and without inparalogs from input gene family trees.
Additional scripts are provided for a variety of task including:
<li>minreID.py Rename sequence identifiers adding species (OTU) name and field delimiters character.
<li>blast_helper.sh Assist in  all vs. all blastp search
<li>BlastResultCluster.py Cluster genes in gene families based on e vales threshold and a minimum number of OTUs.
<li>paMATRAX_F.sh wrapper of gnu-parallel mafft, trimAl and raxml (or fastree) for parallel estimation of phylogenetic trees.
<li>UPhO.py The orthology evaluation tool. 
<li>GetFastafromRef.py Create fasta files from lists of sequence identifiers.
<li>Al2phylo.py A script to prepare MSA for phylogenetic inference where only one sequence per otu is retained and unique sequence identifiers removed.
<li>Consensus.py: Find conserved regions in MSA.
<li>distOrth.py: Functions for annotating the didtribution of orthologs on a tree.
<li>distOrth_interactive.py: interactive helper for sumor.
Each script has its own  -help flag for detail on its usage.

