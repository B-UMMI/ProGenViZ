from Bio import SeqIO
from BCBio import GFF
from Bio.Blast import NCBIXML
from Bio.Blast.Applications import NcbiblastnCommandline
import sys
import os
import re

array = sys.argv
geneSequence=array[1]
genomeDB=array[2]
evalue=array[3]
MinAlign=int(array[4])
pathWhere=array[5]


fnaFileOutput="uploads/" + pathWhere + "/" + "reference.ffn"
name = "uploads/" + pathWhere + "/blastdbs/" + "reference_db"
nameFASTA = "uploads/" + pathWhere + "/queryBLAST.ffn"
inputSequence = "uploads/" + pathWhere + "/" + pathWhere +"_inputWithSequences.json"


def CreateFastaFromInput(genome):
    inputSeq=open(inputSequence, 'r')
    fastaOut=open(fnaFileOutput, 'w')
    linesS = inputSeq.readlines()
    lastlineS=len(linesS)
    for i in range(0,lastlineS):
        try:
            line=linesS[i].split('"')
            genomeLine=line[7]
            if genomeLine==genome:
                fastaOut.write(">gn|"  + line[3]+ "|\n" + line[11] +"\n")
        except IndexError:
            genomeLine=""
    fastaOut.close()
    inputSeq.close()

#Criar a Blast DB:

def Create_Blastdb( questionDB ):
        if not os.path.isfile(name + ".nin") and not os.path.isfile(name + ".nhr") and not os.path.isfile(name + ".nsq"):
                os.system( "/usr/local/ncbi/blast/bin/makeblastdb -in " + questionDB  + " -out " + name + " -dbtype nucl -logfile " + name + "_blast.log" )
        else:
                os.remove(name + ".nin")
                os.remove(name + ".nhr")
                os.remove(name + ".nsq")
                os.remove(name + "_blast.log")
                os.system( "/usr/local/ncbi/blast/bin/makeblastdb -in " + questionDB  + " -out " + name + " -dbtype nucl -logfile " + name + "_blast.log" )
                #print "BLAST DB files found. Using existing DBs.."
        return( name )

def Create_FASTAquery(geneSequence):
        of_handle=open(nameFASTA, 'w')
        os.chmod(nameFASTA, 0755)
        of_handle.write(">gn|queryGene|\n" + geneSequence +"\n")
        of_handle.close()

Create_FASTAquery(geneSequence)
lengthSeq=len(geneSequence)
#if os.path.isfile(IfExistsModified):
#        if typefileDB!='fasta':
 #               ExtractFASTAforFeatureGene(IfExistsModified,fnaFileOutput)
#else:
 #       if typefileDB!='fasta':
 #               ExtractFASTAforFeatureGene(path,fnaFileOutput)
#if typefileDB=='fasta':
#        Create_Blastdb(path)
#else:
genomedb=genomeDB.split("...")[0]
CreateFastaFromInput(genomedb)
Create_Blastdb(fnaFileOutput)

#if typefileDB!='fasta':
#os.remove(fnaFileOutput)


#Correr a Query:

blast_out_file = "uploads/" + pathWhere + "/blastdbs/" + "blastResults_blastout" + "_subj.xml"
#cline = NcbiblastnCommandline(query=nameFASTA, db=name,evalue=evalue, out=blast_out_file, outfmt=5, num_alignments=7000, num_descriptions=7000)
#stdout, stderr = cline()
blastCommand = "/usr/local/ncbi/blast/bin/blastn -out "+blast_out_file+" -outfmt 5 -query "+nameFASTA+" -db "+name+" -evalue "+str(evalue)+" -max_target_seqs 7000"
#print blastCommand
os.system(blastCommand)
rec2 = open(blast_out_file)
blast_records = NCBIXML.parse(rec2)
os.remove(blast_out_file)

#Fazer parse aos resultados:

E_VALUE_THRESH = 0.04
BestMatchResults= []
identities=[]
length=[]
evalueArray=[]
alignment_posStart=[]
matches=[]
sbjct_start=[]
sbjct_end=[]
strands=[]
sbjct=[]
query=[]
score=[]
matcheslen=[]
prevAlignName=""
countResults=0
for blast_record in blast_records:
        if len(blast_record.alignments)==0:
                print 'not exists'
        else:
                for alignment in blast_record.alignments:
                        for hsp in alignment.hsps:
                                Score=hsp.score
                                #or re.search("ENA|",alignment.title)
                                if "NODE_" in alignment.title or 'ENA|' in alignment.title:
                                        geneName=alignment.title.split("|")[3]
                                else:
                                        try:
                                            geneName=alignment.title.split("|")[6]
                                        except IndexError:
                                            geneName=alignment.title.split("|")[3]
                                if hsp.expect < float(evalue) and MinAlign <= hsp.align_length:
                                        countResults+=1
                                        #Done='yes'
                                        #print('****Alignment****')
                                        #print('sequence:', alignment.title)
                                        #print('e value:', hsp.expect)
                                        #print('identities:', hsp.identities)
                                        #print(hsp.query[0:75] + '...')
                                        #print(hsp.match[0:75] + '...')
                                        #print(hsp.sbjct[0:75] + '...')
                                        #identities.append(str(percentageIdentity))
                                        BestMatchResults.append(genomeDB + str(geneName).strip()+'BLASTsearch')
                                        length.append(str(hsp.align_length-1))
                                        score.append(str(Score))
                                        alignment_posStart.append(str(hsp.query_start))
                                        sbjct_start.append(str(hsp.sbjct_start))
                                        sbjct_end.append(str(hsp.sbjct_end))
                                        sbjct.append(str(hsp.sbjct))
                                        query.append(str(hsp.query))
                                        matches.append(str(hsp.match))

#print '---'.join([str(x) for x in identities])

#print len(BestMatchResults)
#print len(length)
#print len(score)
#print len(alignment_posStart)
#print len(sbjct_start)
#print len(sbjct_end)
#print len(sbjct)
#print len(query)
#print len(matches)

if countResults>0:
    print '---'.join([str(x) for x in BestMatchResults])
    print '---'.join([str(x) for x in length])
    print '---'.join([str(x) for x in alignment_posStart])
    print '---'.join([str(x) for x in score])
    print '---'.join([str(x) for x in sbjct_start])
    print '---'.join([str(x) for x in sbjct_end])
    print '...'.join([str(x) for x in query])
    print '...'.join([str(x) for x in sbjct])
    print '...'.join([str(x) for x in matches])


#print '---'.join([str(x) for x in alignment_posStart])
