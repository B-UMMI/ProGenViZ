from Bio import SeqIO
from BCBio import GFF
from Bio.Blast import NCBIXML
from Bio.Blast.Applications import NcbiblastnCommandline
from Bio.Blast.Applications import NcbiblastpCommandline
import sys
import os
import re
import HTSeq
import subprocess
from Bio.Seq import Seq
from CommonFastaFunctions import LoadAlelleFasta
from CommonFastaFunctions import LoadAlellicProfileGeneric
from CommonFastaFunctions import WriteFasta
from CommonFastaFunctions import runBlast
from CommonFastaFunctions import runBlastParser
from os import listdir
from os.path import isfile, join
from datetime import datetime


startTime = datetime.now()
#print datetime.now() - startTime



def ExtractFASTAforFeatureGene(input_file,output_file,isBSR, numberToStart):
        genome=SeqIO.read(open(input_file),'genbank')
        fastafileDB=open(output_file, 'w')
        countGenes = 0
        numberGenesRef=0
        idGene = numberToStart
        for i,feature in enumerate(genome.features):
                if feature.type=='source':
                        name=feature.qualifiers['organism'][0]
                if feature.type=='CDS':
                        #or feature.type=='tRNA' or feature.type=='rRNA' or feature.type=='ncRNA' or feature.type=='tmRNA'
                        countGenes+=1
                        idGene+=1
                        try:
                            locus_tag=feature.qualifiers['locus_tag'][0]
                        except KeyError:
                            locus_tag='-'
                        try:
                            product=feature.qualifiers['product'][0]
                        except KeyError:
                            product='-'
                        try:
                            dbref=feature.qualifiers['db_xref'][0].split(":")[1]
                        except KeyError:
                            dbref='-'
                        try:
                            protein_id=feature.qualifiers['protein_id'][0]
                        except KeyError:
                            protein_id='-'
                        try:
                            translation=feature.qualifiers['translation'][0]
                        except KeyError:
                            translation='-'
                        try:
                            begin = feature.location.start.position
                        except KeyError:
                            begin='-'
                        try:
                            end = feature.location.end.position
                        except KeyError:
                            end='-'
                        Nsequence=feature.extract(genome.seq)
                        try:
                                genes = feature.qualifiers['gene'][0]
                        except KeyError:
                                try:
                                    genes = feature.qualifiers['locus_tag'][0]
                                except KeyError:
                                    genes = feature.type
                        #if product!="hypothetical protein":
                        #fastafileDB.write(">"+str(countGenes)+ "\n" + str(Nsequence) +"\n")
                        fastafileDB.write(">gi|" + dbref + "|ref|" + genes +"_"+str(idGene)+ "|" + product + "[" + name + "]\n" + str(Nsequence) +"\n")
                        RefgenesNames.append(genes +"_"+str(idGene))
                        bestmatches[str(countGenes)] = [str(countGenes),"0","0","False","No","No"] # aleleID : score, score ratio, perfectmatch, key name of the DNA sequence string, Isfound, "NewAllele"
                        numberGenesRef+=1
                        RefgenesBegin.append(begin)
                        RefgenesEnd.append(end)
        #print numberGenesRef
        fastafileDB.close()
        return numberGenesRef

#Criar a Blast DB:
def Create_Blastdb( questionDB, overwrite, dbtypeProt ):
    isProt=dbtypeProt

    if not os.path.isfile(name + ".nin") and not os.path.isfile(name + ".nhr") and not os.path.isfile(name + ".nsq"):
        
        if not isProt:
            os.system( "makeblastdb -in " + questionDB + " -out " + name + " -dbtype nucl -logfile " + name + "_blast.log" )
        else:
            os.system( "makeblastdb -in " + questionDB + " -out " + name + " -dbtype prot -logfile " + name + "_blast.log" )

    elif overwrite:
        if not isProt:
            os.system( "makeblastdb -in " + questionDB + " -out " + name + " -dbtype nucl -logfile " + name + "_blast.log" )
        else:
            os.system( "makeblastdb -in " + questionDB + " -out " + name + " -dbtype prot -logfile " + name + "_blast.log" )

    else:
        print "BLAST DB files found. Using existing DBs.."  
    return( name )


def Create_FASTAquery(geneName,geneSequence):
        of_handle=open(nameFASTA, 'w')
        os.chmod(nameFASTA, 0777)
        of_handle.write(">gn|"  + geneName + "|\n" + geneSequence +"\n")
        of_handle.close()

def Align_sort_key(Result):
    #x=len(Result.split(";")[0].split("--"))
    AlignPos=Result.split(";")[0].split("--")[0]
    return int(AlignPos)

def Align_No_BSR(Result):
    #x=len(Result.split(";")[0].split("--"))
    AlignPos=Result.split(";")[0].split("...")[1]
    return int(AlignPos)

def Align_BySite(Result):
    #x=len(Result.split(";")[0].split("--"))
    AlignPos=Result.split(";")[2]
    return int(AlignPos)

####################################################################################################################################

def runProdigal():

        # ------------ #
        # RUN PRODIGAL #
        # ------------ #  #/scratch/NGStools/prodigal-2.50/prodigal -i /scratch/spneumoniae_600/ERR067978/velvet_assembly/contigs.fa -c -m -g 11 -p single -f sco -q > test_all.txt
        path = "cd Prodigal/Prodigal-2.60 && ./prodigal -i ../../Genomes/Queries/"+Query+" -c -m -g 11 -p single -f sco -q > ../../Results/"+nameOrg+"_Presults.txt";
        os.system(path)

cdsDict = {}

def runProdigalContig(prodigalPath,queryPath):

        # ------------ #
        # RUN PRODIGAL #
        # ------------ #  #/scratch/NGStools/prodigal-2.50/prodigal -i /scratch/spneumoniae_600/ERR067978/velvet_assembly/contigs.fa -c -m -g 11 -p single -f sco -q > test_all.txt
    #print "AQUI"
    path = "cd Prodigal/Prodigal-2.60 && ./prodigal -i ../../"+queryPath+" -c -m -g 11 -p single -f sco -q > ../../"+prodigalPath;
    os.system(path)
    #print proc
    cdsDict = {}
    tempList = []
    line = ' '
    x = open(prodigalPath,"r")
    countContigs=0
    while line != '':
        
        # when it finds a contig tag
        if "seqhdr" in line:
        # add contig to cdsDict and start new entry
            
            if len(tempList) > 0:

                 # --- brute force parsing of the contig tag - better solution is advisable --- #
                
                #i=0
                #for l in contigTag:
                    #if l == ' ':
                        #break
                    #i+=1
                #contigTag=contigTag[:i]
                
                cdsDict[contigTag.replace("\r","")] = tempList
                tempList = []
            
            countContigs+=1
            contigTag = str(countContigs)
            
                # when it finds a line with cds indexes
        elif line[0] == '>':
            
                        # parsing
            cdsL = line.split('_')

                        # --- each element of this list is a pair of indices - the start and the end of a CDS --- #

            tempList.append([ int(cdsL[1]) - 1 , int(cdsL[2]) ])        # start index correction needed because prodigal indexes start in 1 instead of 0
            #print tempList
                # reads the stdout from 'prodigal'
        line = x.readline()

    #print tempList
    # ADD LAST
    if len(tempList) > 0:
        
         # --- brute force parsing of the contig tag - better solution is advisable --- #

        i=0
        for l in contigTag:
            if l == ' ':
                break
            i+=1
        contigTag=contigTag[:i]
        cdsDict[contigTag.replace("\r","")] =tempList
    #print cdsDict.keys()
    #print cdsDict
    #print len(cdsDict)
    return cdsDict

def reverseComplement(strDNA):

    basecomplement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}
    strDNArevC = ''
    for l in strDNA:

        strDNArevC += basecomplement[l]

    return strDNArevC[::-1]

def translateSeq(DNASeq):
    seq=DNASeq
    try:
        myseq= Seq(seq)
        #print myseq
        protseq=Seq.translate(myseq, table=11,cds=True)
    except:
        try:
            seq=reverseComplement(seq)
            myseq= Seq(seq)
            #print myseq
            protseq=Seq.translate(myseq, table=11,cds=True)
                        
        except:
            try:
                seq=seq[::-1]
                myseq= Seq(seq)
                #print myseq
                protseq=Seq.translate(myseq, table=11,cds=True)
            except:
                try:
                    seq=seq[::-1]                           
                    seq=reverseComplement(seq)
                    myseq= Seq(seq)
                    #print myseq
                    protseq=Seq.translate(myseq, table=11,cds=True)
                except:
                    raise
    return protseq



def getFASTAseq(pathF):
    g_fp = HTSeq.FastaReader(pathF)
    countContigs=0
    for contig in g_fp:
        countContigs+=1
        genomeArray[str(countContigs)]=contig.seq

def createFASTAfile(pathF,IsBSR):
    g_fp = HTSeq.FastaReader(pathF)
    lengthContigs={}
    nameContigs={}
    #x = open(fQuery,"w")
    countContigs=0
    for contig in g_fp:
        countContigs+=1
        #print countContigs
        nameContigs[str(countContigs)]=str(contig.name)
        lengthContigs[str(countContigs)]=len(contig.seq)
        if IsBSR =="yes":
            genomeArray[str(countContigs)]=contig.seq
        #x.write(">"+str(countContigs)+"\n")
        #x.write(str(contig.seq)+"\n")
    #x.close()
    #os.remove(pathF)
    #os.rename("uploads/"+pathWhere+"/provF.fasta",pathF)
    return lengthContigs,nameContigs


def getFASTAfeatures(pathF):
    g_fp = HTSeq.FastaReader(pathF)
    countGenes=0
    for contig in g_fp:
        countGenes+=1
        bestmatches[str(contig.name)] = [str(contig.name),"0","0","False","No","No"] # aleleID : score, score ratio, perfectmatch, key name of the DNA sequence string, Isfound, "NewAllele"

    return countGenes

#allelescores={}
#hitsName=[]

def getOwnBlastScore(FASTAfile):
    gene_fp = HTSeq.FastaReader(FASTAfile)
    #alleleI=0
    names=""
    alleleProt=''
    proteome=""
    for allele in gene_fp: #new db for each allele to blast it against himself
        try:
            x = str(translateSeq(allele.seq))
        except:
            continue
        #print str(allele.name)
        #names=allele.name.split("|")[3]
        #print allele.seq
        alleleProt+=">"+str(allele.name)+"\n"+x+"\n"
        proteome+=">"+str(allele.name)+"\n"+x+"\n"
    with open(pathRef+'allAllelesAA.fasta', "wb") as f:
        f.write(alleleProt)
    with open(pathRef+nameOrg+'proteome.fasta', "wb") as v:
        v.write(proteome)
    Gene_Blast_DB_name = Create_Blastdb(pathRef+'allAllelesAA.fasta',1,True)
        # --- get BLAST score ratio --- #
    cline = NcbiblastpCommandline(query=pathRef+nameOrg+'proteome.fasta', db=name, out=blast_out_file, outfmt=5, num_alignments=7000, num_descriptions=7000)
        #print cline
    allelescore=0
    blast_records = runBlastParser(cline,blast_out_file, alleleProt)
    allelescores={}
    for blast_record in blast_records:
        found=False 
        for alignment in blast_record.alignments:
            if found is False:
                #print blast_record.query, alignment.hit_def
                for match in alignment.hsps:
                    #print alignment.hit_def
                        #print "---------------------"
                    #print alignment.hit_def
                    #print blast_record.query
                    #print alignment.hit_def
                    try:
                        if allelescores[str(alignment.hit_def)] < match.score:
                            allelescores[str(alignment.hit_def)] = int(match.score)
                            break
                    except KeyError:
                        allelescores[str(alignment.hit_def)] = int(match.score)
                        break
            else:
                break
    #print allelescores
    #for i in allelescores:
        #hitsName.append(str(i)+";"+str(allelescores[i])+";")
    #hitsName.sort(key=Align_sort_key)
    #print hitsName
    #return alleleI,allelescores,Gene_Blast_DB_name
    #print alleleI
    #print len(allelescores)
    return allelescores


def CreateProteomeContig(nameOrg,cdsDict):
    alleleProt=''
    proteome=""
    countP=0
    countCDS=0
    countContig=0
    lenDict = len(cdsDict)
    queryCDS={}
    for j in range(1,lenDict):
        countCDS=0
        countContig=j
        j=str(j)
        try:
            q = cdsDict[j]
        except KeyError:
            continue
        for i in cdsDict[j]:
            countP+=1
            countCDS+=1
            AlignBegin=i[0]
            AlignEnd=i[1]
            IdCDS=str(j)+"---"+str(countCDS)
            queryCDS[IdCDS] = [int(AlignBegin),int(AlignEnd)]
                    #print contigTag,value

                        
                        #print contigTag, protein[0], protein[1]
                        #print currentGenomeDict[ contigTag ]
            seq= genomeArray[j][ int(AlignBegin):int(AlignEnd) ].upper()
            try:
                protseq=translateSeq(seq)
            except:
                continue
            proteome+=">"+str(countContig)+"---"+str(countCDS)+"\n"+str(protseq)+"\n"
                #proteome+=str(protseq)
    if os.path.isfile(pathRef+nameOrg+'proteome.fasta'):
        os.remove(pathRef+nameOrg+'proteome.fasta')
    with open(pathRef+nameOrg+'proteome.fasta', "wb") as v:
        v.write(proteome)
    return queryCDS

def CreateProteome(nameOrg):

    openPresults = "Results/"+nameOrg+"_Presults.txt"
    Presults=open(openPresults, 'r')
    linesP = Presults.readlines()
    lastlineP=len(linesP)
    alleleProt=''
    proteome=""
    countP=0
    countCDS=0
    for j in range(1,lastlineP):
            if linesP[j].startswith(">"):
                countP+=1
                countCDS+=1
                AlignBegin=linesP[j].split("_")[1]
                AlignEnd=linesP[j].split("_")[2]
                IdCDS=str(j)+"---"+str(countCDS)
                queryCDS[IdCDS] = [int(AlignBegin),int(AlignEnd)]
                #print contigTag,value

                    
                    #print contigTag, protein[0], protein[1]
                    #print currentGenomeDict[ contigTag ]
                seq= genomeArray["1"][ int(AlignBegin)-1:int(AlignEnd) ].upper()
                try:
                    protseq=translateSeq(seq)
                except:
                    continue
                proteome+=">"+IdCDS+"\n"+str(protseq)+"\n"
                #proteome+=str(protseq)
                if os.path.isfile(pathRef+nameOrg+'proteome.fasta'):
                    os.remove(pathRef+nameOrg+'proteome.fasta')
                with open(pathRef+nameOrg+'proteome.fasta', "wb") as v:
                    v.write(proteome)


def CreateNewAlleleFile(ToNewAllele):

    fG = open( pathRef+'AllAlleles.fasta', 'a' )
    for i in ToNewAllele:
        #print i
        fG.write(i)
    fG.close()

    #getOwnBlastScore(pathRef+'AllAlleles.fasta')
    #os.remove(pathRef+'AllAllelesProv.fasta')



def getBlastScoreRatios(orgName,allelescores,cdsDict,prodigalPath):
    
    openPresults = prodigalPath
    Presults=open(openPresults, 'r')
    linesP = Presults.readlines()
    lastlineP=len(linesP)
    alleleProt=''
    proteome=""
    countP=0
    countCDS=0

    if isContig=="no":
        CreateProteome(nameOrg)
    else:
        queryCDS = CreateProteomeContig(nameOrg,cdsDict)


    cline = NcbiblastpCommandline(query=pathRef+nameOrg+'proteome.fasta', db=name, out=blast_out_file, outfmt=5, num_alignments=7000, num_descriptions=7000)
        #print cline

    allelescore=0
    blast_records = runBlastParser(cline,blast_out_file, alleleProt)

    os.remove(pathRef+nameOrg+'proteome.fasta')
    
    blastScoreRatio=0
    countRecords=0
    bestMatches={}
    BestMatchResults= []
    length=[]
    alignment_posStart=[]
    query_length=[]
    for blast_record in blast_records:
        found=False
        countRecords+=1 
        for alignment in blast_record.alignments:
            if found is False:
                #print blast_record.query, alignment.hit_def
                scoreToUse=0
                for match in alignment.hsps:
                    if len(blast_record.alignments)==0:
                        countResults=countResults
                    else:
                        blastScoreRatio = float(match.score) / float(allelescores[str(alignment.hit_def)])
                                #or re.search("ENA|",alignment.title)
                                #print alignment.title
                        try:
                            geneName=alignment.title.split("|")[5]
                        except IndexError:
                            geneName=alignment.title.split("|")[2]
                                #print geneName
                                #products.append(alignment.title.split("|")[6].split("[")[0])
                                #if hsp.expect < 0.001 and 100 <= hsp.align_length:
                        if geneName.strip() not in BestMatchResults and blastScoreRatio>0.6:
                            BestMatchResults.append(genomeDB+"..."+str(geneName).strip())
                            length.append(str(match.align_length-1))
                            #score.append(str(Score))
                            alignment_posStart.append(str(match.query_start))
                            query_length.append(str(len(match.query)))
                    break
            else:
                break
        #print str(blast_record.query)
        bestMatches[str(countRecords)] = [BestMatchResults,length,alignment_posStart,query_length,str(blast_record.query)]
        BestMatchResults= []
        length=[]
        alignment_posStart=[]
        query_length=[]
    print countRecords


    #fG = open( pathRef+'AllAlleles.fasta', 'a' )
    #for i in ToNewAllele:
        #print i
        #fG.write(i)
    #fG.close()


    #Create_Blastdb(pathRef+'allAllelesAA.fasta',1,True)
    #print matchR
    #print allelescores
    #return alleleI,allelescores,Gene_Blast_DB_name
    #print alleleI
    #print len(allelescores)
    #print countT
    return bestMatches,queryCDS
    

####################################################################################################################################################

array = sys.argv
#python database_search.py isBSR

array = sys.argv
isBSR = array[1]
queryPath = array[2]
referencePath = array[3]
pathWhere=array[4]
genomeDB=array[5]
genomeQuery=array[6]

pathRef = "uploads/"+pathWhere+"/input_files/"
pathQuery = "uploads/"+pathWhere+"/input_files/"

pathQueries = "uploads/"+pathWhere+"/input_files/"
pathReferences = "uploads/"+pathWhere+"/input_files/"

numParts = len(queryPath.split("/"))
query = queryPath.split("/")[numParts-1]
reference = referencePath.split("/")[numParts-1]
nameRef = reference.split(".")[0]

RefgenesNames=[]
RefgenesBegin=[]
RefgenesEnd=[]

Gene_Blast_DB_name= ""


nameOrg = query.split(".")[0]
Query = query
Reference=reference
isContig="yes"

fQuery="uploads/"+pathWhere+"/"+nameOrg+"_x.fasta"

if isBSR == "yes":
    SR="yes"
else:
    SR="no"

NameFasta = nameOrg + ".fasta"
name = "uploads/" + pathWhere + "/blastdbs/" + "reference_db"
prodigalPath = "uploads/" + pathWhere + "/Prodigal_results/"+nameOrg+"_Presults.txt"
blast_out_file = "uploads/" + pathWhere + "/Results/"+nameOrg+"_subj.xml"

openFileInput = "uploads/" + pathWhere + "/" + pathWhere + "_inputProv.json"

bestmatches={}
alleles=0

numberToStartRef = -1
numberToStartQuery = -1
inputFile = open(openFileInput,"r")
linesI = inputFile.readlines()
lastlineIv=len(linesI)

for i in range(1,lastlineIv):
    if linesI[i].startswith("{"): 
        linha = linesI[i].split('"')
        if linha[7]==genomeDB and numberToStartRef == -1:
            numberToStartRef = int(linha[11].split("_")[len(linha[11].split("_"))-1])-1
            #print numberToStartRef
        if linha[7]==genomeQuery and numberToStartQuery == "":
            numberToStartRef = int(linha[11].split("_")[len(linha[11].split("_"))-1])-1
        if numberToStartRef != -1 and numberToStartQuery != -1:
            break

#print numberToStartRef
if SR=='yes':
    if Reference.split(".")[1]=='gbk':
        fastaFile=nameRef + ".fasta"
        numberRef = ExtractFASTAforFeatureGene(pathRef + Reference,pathRef + fastaFile,True,numberToStartRef)
        print len(RefgenesBegin)
        Reference=fastaFile
        pathToRef = pathRef+Reference
        #print pathQuery+Query
    elif Reference.split(".")[1]=='fasta':
        #print "Getting FASTA features"
        numberRef = getFASTAfeatures(pathRef + Reference)
        #print "DONE"
    cdsDict = runProdigalContig(prodigalPath,queryPath)
        #print "DONE"
        #print z
    #print "Getting FASTA features Query"
    genomeArray = {}
    lengthSeqs, nameContigs = createFASTAfile(queryPath,isBSR)
    #print "DONE"
    #if firstOwnScore =="":
    print "Getting OWN BSR"
    #allelescores={}
    allelescores = getOwnBlastScore(pathToRef)
    #print "DONE"
    print "Getting BSR"
    bestMatches,queryCDS = getBlastScoreRatios(nameOrg,allelescores,cdsDict,prodigalPath)
    #print bestMatches
    #print "DONE"
    #else:
        #print "Getting BSR"
        #getBlastScoreRatios(nameOrg)
        #print "DONE"
    #print "aqui" + str(alleles)
    #os.remove(pathRef + nameOrg +".fasta")
    os.remove(pathRef + "allAllelesAA.fasta")

else:
    #path="python database_search.py "+fileQname+ " " + i + " " + j + " no"
    #x=os.system(path)
    #print prodigalPath

    if Reference.split(".")[1]=='gbk':
        fastaFile=nameRef + ".fasta"

        numberRef = ExtractFASTAforFeatureGene(pathRef + Reference,pathRef + fastaFile,False, numberToStartRef)
        Reference=fastaFile
        pathToRef = pathRef+Reference
        #print pathToRef
        Create_Blastdb(pathToRef,1,False)

        lengthSeqs, nameContigs = createFASTAfile(queryPath,isBSR)
        #print queryPath
        path = "cd Prodigal/Prodigal-2.60 && ./prodigal -i ../../"+queryPath+" -c -m -g 11 -p single -f sco -q > ../../"+prodigalPath;
        os.system(path)

        #Correr a Query:

        cline = NcbiblastnCommandline(query=queryPath, db=name, out=blast_out_file, outfmt=5, num_alignments=7000, num_descriptions=7000)
        stdout, stderr = cline()
        rec2 = open(blast_out_file)
        blast_records = NCBIXML.parse(rec2)
        #os.remove(blast_out_file)
        os.remove(name + ".nin")
        os.remove(name + ".nhr")
        os.remove(name + ".nsq")
        #os.remove(name + "_blast.log")
        #os.remove(fQuery)
        try:
            os.remove(fastaFile)
        except Exception:
            fastaFile=fastaFile

        #Fazer parse aos resultados:

        E_VALUE_THRESH = 0.04
        BestMatchResults= []
        #identities=[]
        length=[]
        #evalueArray=[]
        alignment_posStart=[]
        #matches=[]
        #sbjct_start=[]
        #sbjct_end=[]
        #strands=[]
        #sbjct=[]
        #query=[]
        #score=[]
        matcheslen=[]
        prevAlignName=""
        countResults=0
        products=[]
        query_length=[]
        bestMatches={}
        countRecords=0
        for blast_record in blast_records:
                #print len(bestMatches)
                countRecords+=1
                #print blast_record
                if len(blast_record.alignments)==0:
                        countResults=countResults
                else:
                    for alignment in blast_record.alignments:
                        #print blast_record.query
                        for hsp in alignment.hsps:
                            Score=hsp.score
                            #or re.search("ENA|",alignment.title)
                            #print alignment.title
                            try:
                                geneName=alignment.title.split("|")[5]
                            except IndexError:
                                geneName=alignment.title.split("|")[2]
                            #print geneName
                            #products.append(alignment.title.split("|")[6].split("[")[0])
                            #if hsp.expect < 0.001 and 100 <= hsp.align_length:
                            countResults+=1
                            if geneName.strip() not in BestMatchResults:
                                BestMatchResults.append(genomeDB+"..."+str(geneName).strip())
                                length.append(str(hsp.align_length-1))
                                #score.append(str(Score))
                                alignment_posStart.append(str(hsp.query_start))
                                query_length.append(str(len(hsp.query)))
                            #sbjct_start.append(str(hsp.sbjct_start))
                            #sbjct_end.append(str(hsp.sbjct_end))
                            #sbjct.append(str(hsp.sbjct))
                            #query.append(str(hsp.query))
                            #matches.append(str(hsp.match))
                            #print BestMatchResults
                    #print BestMatchResults
                    bestMatches[str(countRecords)] = [BestMatchResults,length,alignment_posStart,query_length,str(blast_record.query)]
                    BestMatchResults= []
                    length=[]
                    alignment_posStart=[]



#print len(bestMatches)
if isBSR=="no":
    numberCDS=0
    CDSonSequence=0
    if len(bestMatches) > 0:
        openwhere="uploads/" + pathWhere + "/Search_Results/"+ nameOrg +'_SearchResults.txt'
        fileResult=open(openwhere, 'w')
        os.chmod(openwhere, 0777)
        FinalResults1=[]
        fileResult.write("#Reference;GeneAligned;AlignStart;AlignEnd;GenePosStart;GenePosEnd;queryLength;referenceProGenViZ\n")
        prevGene=""
        BeginEnd=""
        prevEnd=-1
        prevBegin=-1
        prevAlignBegin=-1
        FinalResults=[]
        PRefBegin=0
        PrevRefBegin=-1
        prevName=""
        FinalResults2=[]
        for i in bestMatches:
            numResults = len(bestMatches[i][0])
            FinalResults1=[]
            #print numResults
            for k in range(0,numResults):
                for j in range(0, len(RefgenesNames)):
                    #print len(RefgenesNames)
                    if genomeDB+"..."+RefgenesNames[j]==bestMatches[i][0][k]:
                        #print RefgenesBegin[j]
                        BeginEnd=str(RefgenesBegin[j])+';'+str(RefgenesEnd[j])
                        RefgenesNames.remove(RefgenesNames[j])
                        RefgenesBegin.remove(RefgenesBegin[j])
                        RefgenesEnd.remove(RefgenesEnd[j])
                        break
                #print lengthSeqs[i]
                #print 
                FinalResults1.append(genomeQuery+"..."+i+";"+bestMatches[i][0][k]+";"+bestMatches[i][2][k]+";"+str(int(bestMatches[i][2][k])+int(bestMatches[i][1][k]))+";"+BeginEnd+";"+str(lengthSeqs[i])+";"+bestMatches[i][4]+"\n")
            FinalResults1.sort(key=Align_BySite)
            for i in FinalResults1:
                FinalResults2.append(i)
            #if prevGene==BestMatchResults[i]:
                    #prevGene=prevGene
                    #prevGene=BestMatchResults[i]
            #else:
        #print len(FinalResults1)      
        FinalResults2.sort(key=Align_No_BSR)

        countDup=0
        prevrefB=-1
        prevrefE=-1
        prevtotalL=-1
        prevrefQuery=""
        for i in range(0,len(FinalResults2)):
            #print FinalResults1[i]
            alignB=int(FinalResults2[i].split(";")[2])
            alignE=int(FinalResults2[i].split(";")[3])
            refB=int(FinalResults2[i].split(";")[4])
            refE=int(FinalResults2[i].split(";")[5])
            gName=FinalResults2[i].split(";")[1]
            totallength=int(FinalResults2[i].split(";")[6])
            refQuery=FinalResults2[i].split(";")[7].strip()
            if prevtotalL!=totallength and refQuery!=prevrefQuery:
                prevEnd=-1
                prevBegin=-1
                prevtotalL=totallength
                prevrefQuery=refQuery
                            #if alignB!=prevBegin and alignE!=prevEnd:
                                #FinalResults.append(FinalResults1[i])
                                #CDSonSequence+=1
                                #prevEnd=alignE
                                #prevBegin=alignB
                            #else:
            if alignB==prevBegin and alignE>prevEnd:
                FinalResults.pop()
                CDSonSequence+=1
                FinalResults.append(FinalResults2[i].strip() + "\n")

            elif alignB <= prevEnd:
                continue
            else:
                                #if prevName!=geneName:
                if alignB==prevBegin and refB<prevrefB:
                    countDup+=1
                    FinalResults.append(FinalResults2[i].strip()+"\n")
                    a, b = len(FinalResults)-2, len(FinalResults)-1
                    FinalResults[b], FinalResults[a] = FinalResults[a], FinalResults[b]
                    #FinalResults.remove(FinalResults[len(FinalResults)-1])
                    FinalResults[len(FinalResults)-1] = FinalResults[len(FinalResults)-1].strip() + ">Pdup\n"
                else:
                    if refB!=prevrefB and refE != prevrefE:
                        FinalResults.append(FinalResults2[i].strip() + "\n")
                #CDSonSequence+=1
                                #else:
                                    #print gName
            prevrefB=refB
            prevrefE=refE
            prevEnd=alignE
            prevBegin=alignB
            prevName=gName

                        #print countDup
        numFResults = len(FinalResults)
        for i in range(0,numFResults):
            fileResult.write(FinalResults[i])
        fileResult.close()

else:
    numberCDS=0
    CDSonSequence=0
    if len(bestMatches) > 0:
        openwhere="uploads/" + pathWhere + "/Search_Results/"+ nameOrg +'_SearchResults.txt'
        fileResult=open(openwhere, 'w')
        os.chmod(openwhere, 0777)
        FinalResults1=[]
        fileResult.write("#Reference;GeneAligned;AlignStart;AlignEnd;GenePosStart;GenePosEnd;queryLength;referenceProGenViZ\n")
        prevGene=""
        BeginEnd=""
        prevEnd=-1
        prevBegin=-1
        prevAlignBegin=-1
        FinalResults=[]
        PRefBegin=0
        PrevRefBegin=-1
        prevName=""
        FinalResults2=[]
        for i in bestMatches:
            numResults = len(bestMatches[i][0])
            FinalResults1=[]
            #print numResults
            for k in range(0,numResults):
                for j in range(0, len(RefgenesNames)):
                    #print len(RefgenesNames)
                    if genomeDB+"..."+RefgenesNames[j]==bestMatches[i][0][k]:
                        #print RefgenesBegin[j]
                        BeginEnd=str(RefgenesBegin[j])+';'+str(RefgenesEnd[j])
                        RefgenesNames.remove(RefgenesNames[j])
                        RefgenesBegin.remove(RefgenesBegin[j])
                        RefgenesEnd.remove(RefgenesEnd[j])
                        break
                #print lengthSeqs[i]
                #print bestMatches[i]
                FinalResults1.append(genomeQuery+"..."+i+";"+bestMatches[i][0][k]+";"+str(queryCDS[bestMatches[i][4]][0])+";"+str(queryCDS[bestMatches[i][4]][1])+";"+BeginEnd+";"+str(lengthSeqs[bestMatches[i][4].split("---")[0]])+";"+nameContigs[bestMatches[i][4].split("---")[0]]+"\n")
            FinalResults1.sort(key=Align_BySite)
            for i in FinalResults1:
                FinalResults2.append(i)
            #if prevGene==BestMatchResults[i]:
                    #prevGene=prevGene
                    #prevGene=BestMatchResults[i]
            #else:
        #print len(FinalResults1)      
        FinalResults2.sort(key=Align_No_BSR)

                        #print countDup
        numFResults = len(FinalResults2)
        for i in range(0,numFResults):
            fileResult.write(FinalResults2[i])
        fileResult.close()


###################################################################################################################################################

opensearchResults='uploads/' + pathWhere + '/Search_Results/'+ nameOrg +'_SearchResults.txt'
openPresults='uploads/' + pathWhere + '/Prodigal_results/'+ nameOrg +'_Presults.txt'
openInputProv='uploads/' + pathWhere + '/'+ pathWhere +'_inputProv.json'
openInputSeq='uploads/' + pathWhere + '/'+ pathWhere +'_inputWithSequences.json'
removeFile='uploads/' + pathWhere + '/Sequence_files/'+ nameOrg +'_sequence.fasta'
#removeFile2='uploads/' + path + '/'+ RegionName +'_query.ffn'

openNewFile='uploads/' + pathWhere + '/'+ pathWhere +'_inputP.json'
openNewSeq='uploads/' + pathWhere + '/'+ pathWhere +'_inputSeq.json'


fileResult=open(openNewFile, 'w')
os.chmod(openNewFile, 0777)

fileResultSeq=open(openNewSeq, 'w')
os.chmod(openNewSeq, 0777)

searchResults=open(opensearchResults, 'r')
Presults=open(openPresults, 'r')
Iprov=open(openInputProv, 'r')
Iseq=open(openInputSeq, 'r')

linesR = searchResults.readlines()
linesP = Presults.readlines()
linesIP = Iprov.readlines()
linesS = Iseq.readlines()

lastlineR=len(linesR)
lastlineP=len(linesP)
lastlineIP=len(linesIP)
lastlineS=len(linesS)

QueryName=linesP[0].split('"')[1]
GenesToUse=[]
AllGenesToUse={}
ContigParts=[]
countParts=1
isThere="no"

prevGeneEnd=-1
PrevLineProdigal=-1
PrevLineBLAST=1
numberContig = ""
Contig=""
queryName=""
prevContig = linesR[1].split(";")[7].strip()
for i in range(1,lastlineR):
    queryName=linesR[i].split(";")[7]
    #print query
    geneName=linesR[i].split(";")[1]
    geneBegin=linesR[i].split(";")[2]
    geneEnd=linesR[i].split(";")[3]
    geneBeginReal=linesR[i].split(";")[4]
    geneEndReal=linesR[i].split(";")[5]
    totalLength = linesR[i].split(";")[6]
    refProgen = linesR[i].split(";")[7]
    #print geneName

    threshBLAST = (int(geneBegin) + int(geneEnd)) * 0.1

    for j in range(PrevLineProdigal+1,lastlineP):
        #print queryName.strip()
        #print numberContig
        #print linesP[j]
        #print PrevLineProdigal
        #print queryName.strip()
        if linesP[j].startswith("#"):
            #print queryName.strip()
            #print linesP[j].strip()
            if queryName.strip() in linesP[j]:
                #print queryName.strip()
                Contig = queryName.strip()
                PrevLineProdigal=j
            #else:
                #PrevLineProdigal=j
        elif linesP[j].startswith(">"):
            #print queryName.strip()
            #print Contig.strip()
            if queryName.strip() == Contig:
                #print queryName
                #print Contig
                addToGenesToUse='yes'
                AlignBegin=linesP[j].split("_")[1]
                AlignEnd=linesP[j].split("_")[2]
                alBeEnd=AlignBegin+"---"+AlignEnd
                #if len(GenesToUse)==0:
                    #addToGenesToUse='yes'
                wGene = linesR[i].split(";")[1].split("...")[1]
                #print wGene
                #print len(GenesToUse)
                #for z in GenesToUse:
                    #if wGene in z:
                        #print wGene
                        #addToGenesToUse='no'
                threshProdigal = (int(AlignBegin) + int(AlignEnd)) * 0.07

                #print "Contig " + queryName
                #print "REsults " + geneBegin
                #print "Prodigal " +AlignBegin
                if int(geneBegin) <= int(AlignBegin) and int(AlignEnd) <= int(geneEnd) and addToGenesToUse=='yes': #Resultados do BLAST englobam os resultados do Prodigal
                    addToGenesToUse='no'
                    #klker coisa
                    #print "AQUI"
                    #print AlignBegin+".."+AlignEnd
                    #print geneBegin+"--"+geneEnd
                    prevGeneEnd=geneEnd
                    #PrevLineProdigal=j
                    genome=geneName.split("...")[0]
                    isThere="yes"
                    break

                elif int(geneBegin) - int(AlignBegin) >= 0 and  int(geneBegin) - int(AlignBegin) <= threshProdigal and int(AlignEnd) - int(geneEnd) >= 0 and int(AlignEnd) - int(geneEnd) <= threshProdigal and addToGenesToUse=='yes': #Results BLAST incluidos no  result Prodigal
                    addToGenesToUse='no'
                    #klker coisa
                    #print AlignBegin+".."+AlignEnd
                    #print geneBegin+"--"+geneEnd
                    prevGeneEnd=geneEnd
                    genome=geneName.split("...")[0]
                    #PrevLineProdigal=j
                    isThere="yes"
                    break

                elif int(AlignBegin) - int(geneBegin) >= 0 and int(AlignBegin) - int(geneBegin) <= threshProdigal and int(AlignEnd) - int(geneEnd) >= 0 and int(AlignEnd) - int(geneEnd) <= threshProdigal and addToGenesToUse=='yes': #Inicio do BLAST fora dos resultados do Prodigal mas o final no interior
                    addToGenesToUse='no'
                    #klker coisa
                    #print AlignBegin+".."+AlignEnd
                    #print geneBegin+"--"+geneEnd
                    prevGeneEnd=geneEnd
                    genome=geneName.split("...")[0]
                    #PrevLineProdigal=j
                    isThere="yes"
                    break

                elif int(AlignBegin) - int(geneBegin) >= 0 and int(AlignBegin) - int(geneBegin) <= threshProdigal and int(geneEnd) - int(AlignEnd) >= 0 and int(geneEnd) - int(AlignEnd) <= threshProdigal and addToGenesToUse=='yes': #Final do BLAST fora dos resultados do Prodigal mas o inicio no interior
                    addToGenesToUse='no'
                    #klker coisa
                    #print AlignBegin+".."+AlignEnd
                    #print geneBegin+"--"+geneEnd
                    prevGeneEnd=geneEnd
                    genome=geneName.split("...")[0]
                    #PrevLineProdigal=j
                    isThere="yes"
                    break
                #else:
                   #PrevLineProdigal=j 
            #else:
                #PrevLineProdigal=j
                #break

    if prevContig!=Contig:
        if len(GenesToUse) != 0:
            #if prevContig == 'NODE_1_length_163052_cov_28.6769_ID_454578':
                #print GenesToUse
            AllGenesToUse[str(prevContig)] = GenesToUse
            GenesToUse=[]
        prevContig=Contig

    #print isThere
    if isThere=="yes":
        #print "AQUI"
        #print geneName
        for k in range(1,lastlineIP-1):
            line=linesIP[k].split('"')
            #print genome
            alreadyThere=False
            if line[7]==genome and line[19]==geneBeginReal and line[23] == geneEndReal:
                for z in GenesToUse:
                    if linesIP[k] in z:
                        #print "AQUI"
                        #print linesIP[k]
                        alreadyThere=True
                        #addToGenesToUse='no'
                #if linesIP[k] in 
                    #print Contig
                if not alreadyThere:
                    #print "AQUI"
                    GenesToUse.append(alBeEnd+"---"+linesIP[k]+"---"+geneBegin+"---"+geneEnd+"---"+totalLength+"---"+refProgen)
                break
        isThere="no"

if prevContig!=Contig:
        if len(GenesToUse) != 0:
            #print prevContig
            AllGenesToUse[str(prevContig)] = GenesToUse
            GenesToUse=[]
        prevContig=Contig
 
#print len(AllGenesToUse)       
#genesLen=len(GenesToUse)
pasS='no'
timeToPrint='yes'
refExists=True

genome=""
#print '\n'.join([str(x) for x in GenesToUse])
for x in range(0,lastlineIP):
    line=linesIP[x].split('"')
    if x==0 or x==lastlineIP-1:
        fileResult.write(linesIP[x])
        pasS='yes'
    else:
        pasS='no'
        name=line[11]
        try:
            reference=line[47]
        except IndexError:
            try:
                reference=line[43]
            except IndexError:
                reference=line[39]  
    try:
        #print reference
        a = AllGenesToUse[reference]
        refExists=True
    except KeyError:
        refExists=False
    if refExists and pasS!='yes':
        #print "AQUI"
        pasS=='no'
        begin=int(line[19])
        end=int(line[23])
        alignB=int(AllGenesToUse[reference][0].split("---")[0])
        alignE=int(AllGenesToUse[reference][0].split("---")[1])
        genome=AllGenesToUse[reference][0].split("---")[2].split('"')[7]
        if alignB>1 or alignB==1:
            if timeToPrint=='yes':
                #print line[27]
                timeToPrint='no'
            #ToChange=str(line[3]+"_GAP_"+str(countParts))
            newLine=linesIP[x].replace('"gene": "'+line[3]+'"','"gene": "'+line[3]+"_GAP_"+str(countParts)+'"')
            newLine=newLine.replace('"reference": "'+line[3]+'"','"reference": "'+line[3]+"_GAP_"+str(countParts)+'"')
            newLine=newLine.replace('"end": "'+str(end)+'"','"end": "'+str(alignB)+'"')
            newLine=newLine.replace('"product": ""','"product": "Undefined"')
            countParts+=1
            ContigParts.append(newLine)
            fileResult.write(newLine)
            #print line[3]
            #print ToChange
            #print newLine
        if '"contig": ' in linesIP[x]:
            contig=linesIP[x].split('"')[27]
        lenToUse=len(AllGenesToUse[reference])
        for p in range(0,lenToUse):
            gene=AllGenesToUse[reference][p].split("---")[2]
            OrganismName=gene.split('"')[3]
            geneB=gene.split('"')[19]
            geneE=gene.split('"')[23]
            regionBegin=1
            contig1=gene.split('"')[27]
            contigs='"contig": "'+contig1+'"'
            gene=gene.replace('"name": "'+OrganismName+'"','"name": "'+line[3]+'"')
            gene=gene.replace('"begin": "'+geneB+'"','"begin": "'+str(int(regionBegin)+int(AllGenesToUse[reference][p].split("---")[0]))+'"')
            gene=gene.replace('"end": "'+geneE+'"','"end": "'+str(int(regionBegin)+int(AllGenesToUse[reference][p].split("---")[1]))+'"')
            parts=gene.split(contigs)
            newContig='"contig": "'+contig+'"'
            gene=parts[0]+newContig+parts[1]
            genoma=int(genomeQuery)
            gene=gene.replace(str(genome)+"...",str(genoma)+"...")
            gene=gene.replace('"genome": "'+str(genome)+'"','"genome": "'+str(genoma)+'"')
            geneP=gene.split('"');
            geneL=len(geneP);
            geneRef=geneP[geneL-2]
            gene=gene.replace('"reference": "'+geneRef+'"','"reference": "'+geneRef+'_'+str(genoma)+'"')
            gene=gene.strip()+'\n'
            fileResult.write(gene)
            lastEnd=AllGenesToUse[reference][p].split("---")[1]
            try:
                nextGene=AllGenesToUse[reference][p+1].split("---")[2]
                #print nextGene
                geneB1=int(nextGene.split('"')[19])
                gap=int(AllGenesToUse[reference][p+1].split("---")[0])-int(AllGenesToUse[reference][p].split("---")[1])
                #print gap
                if gap > 1:
                    #newWrite=linesIP[x].replace(',"contig": "'+contig+'"',"")
                    newWrite=linesIP[x].replace('"begin": "'+str(begin)+'"','"begin": "'+str(int(AllGenesToUse[reference][p].split("---")[1]))+'"')
                    #print str(int(GenesToUse[p].split("---")[1]))
                    #print str(int(GenesToUse[p+1].split("---")[0]))
                    newWrite=newWrite.replace('"end": "'+str(end)+'"','"end": "'+str(int(AllGenesToUse[reference][p+1].split("---")[0]))+'"')
                    #print newWrite
                    #print line[3]
                    newWrite=newWrite.replace('"gene": "'+line[3]+'"','"gene": "'+line[3]+"_GAP_"+str(countParts)+'"')
                    newWrite=newWrite.replace('"reference": "'+line[3]+'"','"reference": "'+line[3]+"_GAP_"+str(countParts)+'"')
                    newWrite=newWrite.replace('"product": ""','"product": "Undefined"')
                    countParts+=1
                    ContigParts.append(newWrite)
                    fileResult.write(newWrite)

            except IndexError:
                lastEnd=lastEnd

        if int(lastEnd)<int(end):
            newWrite=linesIP[x].replace('"begin": "'+str(begin)+'"','"begin": "'+str(int(lastEnd))+'"')
            newLine=newWrite.replace('"gene": "'+line[3]+'"','"gene": "'+line[3]+"_GAP_"+str(countParts)+'"')
            newLine=newLine.replace('"reference": "'+line[3]+'"','"reference": "'+line[3]+"_GAP_"+str(countParts)+'"')
            newLine=newLine.replace('"product": ""','"product": "Undefined"')
            ContigParts.append(newLine)
            fileResult.write(newLine)

        #else:
        #   fileResult.write(linesIP[x])
    else:
        if x==0 or x==lastlineIP-1:
            pasS='yes'
        else:
            fileResult.write(linesIP[x])

fileResult.close()
#genome=GenesToUse[0].split("---")[2].split('"')[7]
genoma=int(genomeQuery)
#print nameContigs
prevLine=-1
for p in range(0,lastlineS):
    line=linesS[p].split('"')
    checkOnFile=True
    try:
        v=AllGenesToUse[line[3]]
        checkOnFile=True
        sequence=line[11]
    except KeyError:
        checkOnFile=False
        #continue
    if checkOnFile:
        for w in range(0,len(AllGenesToUse[line[3]])):
            gene=AllGenesToUse[line[3]][w].split("---")[2]
            Abegin=int(AllGenesToUse[line[3]][w].split("---")[0])
            Aend=int(AllGenesToUse[line[3]][w].split("---")[1])
            GeneSBegin=int(AllGenesToUse[line[3]][w].split("---")[3])
            GeneSEnd=int(AllGenesToUse[line[3]][w].split("---")[4])
            gene=gene.split('"');
            geneLen=len(gene);
            reference=gene[geneLen-2]
            #print reference
            #print line[3]
            #if line[3]==reference:
                #print "AQUI"
            sequenceGene=line[11]
                #newGeneBegin=Abegin
                #print newGeneBegin
                #newGeneEnd=(GeneSEnd-GeneSBegin)-(GeneSEnd-Aend)
            sequencePart=sequence[Abegin:Aend]
            newline=linesS[p].replace(sequenceGene,sequencePart)
            newline=newline.replace('"gene": "'+line[3]+'"', '"gene": "'+reference+'"')
            newline=newline.replace('"gene": "'+reference+'"', '"gene": "'+reference+"_"+str(genoma)+'"')
            newline=newline.replace('"genome": "'+str(genome)+'"','"genome": "'+str(genoma)+'"')
            fileResultSeq.write(newline)
                #break
                #sequence=line[11]
        for m in range(0,len(ContigParts)):
            parts=ContigParts[m].split('"')
            ToChange=parts[len(parts)-2]
            if line[3] in ToChange:
                #print ToChange
                contigB=int(ContigParts[m].split('"')[19])
                contigE=int(ContigParts[m].split('"')[23])
                #print contigB
                #print contigE
                if contigB==contigE:
                    sequencePart=sequence[contigE]
                else:
                    sequencePart=sequence[contigB:contigE]
                #print QueryName
                newline=linesS[p].replace(sequence,sequencePart)
                newline=newline.replace(line[3],ToChange)
                fileResultSeq.write(newline)
                #ContigParts.remove(ContigParts[m])

    else:
        fileResultSeq.write(linesS[p])




fileResult.close()
fileResultSeq.close()

searchResults.close()
Presults.close()
Iprov.close()

os.remove(openInputProv)
os.rename(openNewFile,openInputProv)

os.remove(openInputSeq)
os.rename(openNewSeq,openInputSeq)  

os.remove(opensearchResults)
os.remove(openPresults)
#os.remove(fQuery)
#os.remove(removeFile)