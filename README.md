# UPhO

UPhO find orthologs with and without in paralogs from input genefamily trees.
Additional scripts are proivided for a variety of task inclufing:
<li>minreID.py Rename sequence identifiers adding species (OTU) name
<li>blast_helper.sh generate all vs all blas search
<li>BlastResultCluster.py Cluster genes in gene families based on e vales threshold and a minimum number os OTUs.
<li>paMatrax.sh wrapper of gnu-parallelmaff, trimal and raxml (or fastree) for parallel esrimation of phylogenetic trees.
<li>UPhO.py The orthology evaluation tool. 
<li>GetFastafromRef.py Create fasta files from lists of sequence identifiers.
<li>Al2phylo.py A script to prepare MSA for phylogentic infernece where only one squence pero otu is retained and unique sequence identifiers removed.
<li>Consensus.py: Find conserved regions in MSA.
<li>sumor.py: Functions for annoatating thr didtribution of orthologs on a tree.
<li>sumorIntrface: interactive helper for sumor.
Each script has its own  -help flag for detail on its usage.

