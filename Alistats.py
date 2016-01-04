#!/usr/bin/env python
from sys import argv

    
sep = '|'

def Fasta_to_Dict(File):
    '''BETTER FASTA PARSER'''
    with open(File, 'r') as F:
        Records = {}
        for Line in F:
            if Line.startswith('>'):
                Seqid = Line.strip('>').strip('\n')
                Seq= ''
                Records[Seqid] = Seq
            else:
                Seq = Records[Seqid] + Line.strip('\n')
                Records[Seqid] = Seq 
        return Records

def aln_stats(Dict):
    Spp = set([i.split(sep)[0] for i in Dict.iterkeys()])
    Allseq = ''.join(Dict.values())
    AT = Allseq.count('A') + Allseq.count('T')
    GC = Allseq.count('G') + Allseq.count('C')
    Gaps = Allseq.count('-')
    sites = len(Allseq)
    return [ len(Dict.keys()), len(Spp), float(AT)/sites, float (GC)/sites, float(Gaps)/sites]

def make_Consensus(Dict, T):
    '''This functiom returns the sites where all the alignment  positions match on the same nucleotide. this is a T% consensus'''
    Consensus=''
    for i in range(0, len(Dict[Dict.keys()[0]])):
        compo = [seq[i] for seq in Dict.itervalues()]
        G = 0 
        MFB = ''
        for base in set(compo):
            freq = compo.count(base)
            if freq > G:
                G = freq
                MFB = base
        if float(G)/len(Dict.keys()) >= T:
            Consensus+=MFB
        else:
            Consensus+='N'
    return Consensus


#MAIN
if __name__=='__main__': 
    Script = argv[0]
    argv.remove(Script)
    Targets = argv
#    print Targets
    with open('alns_stats.tsv', 'w') as out:
        out.write("File\tnumSeq\tnumSpp\tAlnLen\tATper\tGCper\tGapper\identper\tConsensus\n")
        for F in Targets:
            Al = Fasta_to_Dict(F)
            numSeq, numSpp, ATper, GCper, Gapper = aln_stats(Al)
            C = make_Consensus(Al, 1.0)
            Ident = (C.count('A') + C.count('T') + C.count('C') + C.count('G')) / float(len(C))
            out.write("%s\t%d\t%d\t%d\t%f\t%f\t%f\t%f\t%s\n"  % (F, numSeq, numSpp, len(C), ATper, GCper, Gapper, Ident, C))
