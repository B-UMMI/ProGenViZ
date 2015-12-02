from Bio import SeqIO
from BCBio import GFF
from Bio.Blast import NCBIXML
from Bio.Blast.Applications import NcbiblastnCommandline
import sys
import os
import re

array = sys.argv
genomeQuery=array[1]
fileSequencepath=array[2]
genomeDB=array[3]
evalue=float(array[4])
MinAlign=int(array[5])
pathWhere=array[6]

fnaFileOutput="uploads/" + pathWhere + "/" + "reference.ffn"
name = "uploads/" + pathWhere + "/blastdbs/" + "reference_db"
nameFASTA = "uploads/" + pathWhere + "/" + genomeQuery.split("...")[1] + "_query.ffn"
inputSequence = "uploads/" + pathWhere + "/" + pathWhere +"_inputWithSequences.json"

sequenceFile=open(fileSequencepath, 'r')
lines = sequenceFile.readlines()

geneSequence=lines[1]

sequenceFile.close()

def ExtractFASTAforFeatureGene(input_file,output_file):
        genome=SeqIO.read(open(input_file),'genbank')
        fastafileDB=open(output_file, 'w')
        os.chmod(output_file, 0755)
        for i,feature in enumerate(genome.features):
                if feature.type=='source':
                        name=feature.qualifiers['organism'][0]
                if feature.type=='CDS':
                        begin = feature.location.start.position
                        end = feature.location.end.position
                        if feature.location == 1:
                                strand = '+'
                        else:
                                strand = '-'
                        locus_tag=feature.qualifiers['locus_tag'][0]
                        product=feature.qualifiers['product'][0]
                        dbref=feature.qualifiers['db_xref'][0].split(":")[1]
                        protein_id=feature.qualifiers['protein_id'][0]
                        translation=feature.qualifiers['translation'][0]
                        Nsequence=feature.extract(genome.seq)
                        try:
                                genes = feature.qualifiers['gene'][0]
                        except KeyError:
                                genes = feature.qualifiers['locus_tag'][0]
                        fastafileDB.write(">gi|" + dbref + "|ref|" + genes + "|" + product + "[" + name + "]\n" + str(Nsequence) +"\n")

        fastafileDB.close()

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
                os.system( "/usr/local/ncbi/blast/bin/makeblastdb -in " + questionDB  + " -out " + name + " -dbtype nucl -logfile " + name + "_blast.log")
        else:
                os.remove(name + ".nin")
                os.remove(name + ".nhr")
                os.remove(name + ".nsq")
                #os.remove(name + "_blast.log")
                os.system( "/usr/local/ncbi/blast/bin/makeblastdb -in " + questionDB  + " -out " + name + " -dbtype nucl -logfile " + name + "_blast.log" )
                #print "BLAST DB files found. Using existing DBs.."
        return( name )

def Create_FASTAquery(geneName,geneSequence):
        of_handle=open(nameFASTA, 'w')
        os.chmod(nameFASTA, 0755)
        of_handle.write(">gn|"  + geneName + "|\n" + geneSequence +"\n")
        of_handle.close()

Create_FASTAquery(genomeQuery,geneSequence)

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
#cline = NcbiblastnCommandline(query=nameFASTA, db=name,evalue=evalue, out=blast_out_file, outfmt=5, max_target_seqs=7000)
#stdout, stderr = cline()
blastCommand = "/usr/local/ncbi/blast/bin/blastn -out "+blast_out_file+" -outfmt 5 -query "+nameFASTA+" -db "+name+" -evalue "+str(evalue)+" -max_target_seqs 7000"
os.system(blastCommand)
rec2 = open(blast_out_file)
blast_records = NCBIXML.parse(rec2)
#os.remove(blast_out_file)

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
                                        BestMatchResults.append(genomeDB + str(geneName).strip())
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

def Align_sort_key(Result):
    AlignPos=Result.split(";")[1]
    return int(AlignPos)

if len(alignment_posStart) > 0:
        openwhere='uploads/' + pathWhere + '/Search_Results/'+ genomeQuery.split("...")[1] +'_SearchResults.txt'
        openwhich='uploads/' + pathWhere + '/'+ pathWhere +'_inputProv.json'
        fileResult=open(openwhere, 'w')
        fileProv=open(openwhich, 'r')
        linesIP = fileProv.readlines()
        lastlineIP=len(linesIP)
        os.chmod(openwhere, 0755)
        numResults = len(alignment_posStart)
        FinalResults1=[]
        fileResult.write("#GeneAligned;AlignStart;AlignEnd;GenePosStart;GenePosEnd\n")
        prevGene=""
        BeginEnd=""
        prevEnd=-1
        FinalResults=[]
        for i in range(0,numResults):
            if prevGene==BestMatchResults[i]:
                prevGene=BestMatchResults[i]
            else:
                for j in range(1, lastlineIP):
                    if linesIP[j].split('"')[11]==BestMatchResults[i]:
                        parts=linesIP[j].split('"')
                        BeginEnd=parts[19]+';'+parts[23]
                        break
                if 'Undefined' in BestMatchResults[i]:
                    prevGene=prevGene
                else:
                    FinalResults1.append(BestMatchResults[i]+";"+alignment_posStart[i]+";"+str(int(alignment_posStart[i])+int(length[i]))+";"+BeginEnd+"\n")
                prevGene=BestMatchResults[i]
        
        FinalResults1.sort(key=Align_sort_key)

        for i in range(0,len(FinalResults1)):
            alignB=int(FinalResults1[i].split(";")[1])
            alignE=int(FinalResults1[i].split(";")[2])
            FinalResults.append(FinalResults1[i])
            #if alignB>prevEnd:
                #FinalResults.append(FinalResults1[i])
                #prevEnd=alignE
            #else:
                #prevEnd=alignE

        numFResults = len(FinalResults)
        for i in range(0,numFResults):
            fileResult.write(FinalResults[i])
        fileResult.close()

os.remove(nameFASTA)
os.remove(fnaFileOutput)
