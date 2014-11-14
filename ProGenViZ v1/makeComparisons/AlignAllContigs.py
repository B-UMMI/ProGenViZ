from Bio import SeqIO
from BCBio import GFF
from Bio.Blast import NCBIXML
from Bio.Blast.Applications import NcbiblastnCommandline
import sys
import os
import re

array = sys.argv
genomeToBeQuery=array[1]
genomeDB=array[2]
pathWhere=array[3]
evalue=array[4]
MinScore=array[5]
numGenomes=array[6]

fnaFileOutput="uploads/" + pathWhere + "/" + "reference.ffn"
name = "uploads/" + pathWhere + "/blastdbs/" + "reference_db"
nameFASTA = "uploads/" + pathWhere + "/gene_query.ffn"
inputSequence = "uploads/" + pathWhere + "/" + pathWhere +"_inputWithSequences.json"

E_VALUE_THRESH = 0.04
BestMatchResults= []
length=[]
alignment_posStart=[]
ProdigalResults=[]
GenesToUse=[]
FinalResults1=[]
global countParts
countParts=1

prevAlignName=""
countResults=0

def ExtractFASTAforFeatureGene(input_file,output_file):
        genome=SeqIO.read(open(input_file),'genbank')
        fastafileDB=open(output_file, 'w')
        os.chmod(output_file, 0777)
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
                os.system( "makeblastdb -in " + questionDB  + " -out " + name + " -dbtype nucl -logfile " + name + "_blast.log" )
        else:
                os.remove(name + ".nin")
                os.remove(name + ".nhr")
                os.remove(name + ".nsq")
                os.remove(name + "_blast.log")
                os.system( "makeblastdb -in " + questionDB  + " -out " + name + " -dbtype nucl -logfile " + name + "_blast.log" )
                #print "BLAST DB files found. Using existing DBs.."
        return( name )

def Create_FASTAquery(geneName,geneSequence):
        of_handle=open(nameFASTA, 'w')
        os.chmod(nameFASTA, 0777)
        of_handle.write(">gn|"  + geneName + "|\n" + geneSequence +"\n")
        of_handle.close()


def GetSequence(geneReference):
    geneReference=geneReference.replace("---"," ")
    geneReference=geneReference.replace("...","|")
    openwhich='uploads/' + pathWhere + '/'+ pathWhere +'_inputWithSequences.json'
    openwhere='uploads/' + pathWhere + '/Sequence_files/query_sequence.fasta'
    filesequence=open(openwhere, 'w')
    os.chmod(openwhere, 0777)
    inf=open(openwhich, 'r')
    lines = inf.readlines()
    lastline=len(lines)
    targetSequence=""
    for i in range(0, lastline):
        if '{"gene":' in lines[i]:
            line=lines[i].split('"')
            #and line[7]==geneBegin and line[11]==geneEnd
            if geneReference in lines[i]:
                filesequence.write(">"+line[3]+"\n")
                filesequence.write(line[11])
                break

    inf.close()
    filesequence.close()


def AddTail():
    openwhich='uploads/' + pathWhere + '/Sequence_files/query_sequence.fasta'
    openwhere='uploads/' + pathWhere + '/'+ 'sequenceProv.fasta'
    filesequence=open(openwhere, 'w')
    os.chmod(openwhere, 0777)
    inf=open(openwhich, 'r')
    lines = inf.readlines()
    lastline=len(lines)
    targetSequence=""
    lengthSequence=0
    for i in range(0, lastline):
        if i==0:
            filesequence.write(lines[i])
        else:
            lengthSequence=len(lines[i])
            filesequence.write(lines[i])
    if lengthSequence<21000:
        for j in range(lengthSequence, 21000):
            filesequence.write('A')

    inf.close()
    filesequence.close()
    os.remove(openwhich)
    os.rename(openwhere, openwhich)


def Align_sort_key(Result):
    AlignPos=Result.split(";")[1]
    return int(AlignPos)


def CreateSearchResults():
    if len(alignment_posStart) > 0:
            openwhere='uploads/' + pathWhere + '/Search_Results/All_SearchResults.txt'
            openwhich='uploads/' + pathWhere + '/'+ pathWhere +'_inputProv.json'
            fileResult=open(openwhere, 'w')
            fileProv=open(openwhich, 'r')
            linesIP = fileProv.readlines()
            lastlineIP=len(linesIP)
            os.chmod(openwhere, 0777)
            numResults = len(alignment_posStart)
            #print numResults
            #print len(BestMatchResults)
            fileResult.write("#GeneAligned;AlignStart;AlignEnd;GenePosStart;GenePosEnd\n")
            prevGene=""
            BeginEnd=""
            prevEnd=-1
            FinalResults=[]
            for i in range(0,numResults):
                if prevGene==BestMatchResults[i]:
                    prevGene=BestMatchResults[i]
                else:
                    for j in range(1, lastlineIP-1):
                        geneQueryName=BestMatchResults[i].split('--')[0]
                        if linesIP[j].split('"')[11]==geneQueryName:
                            parts=linesIP[j].split('"')
                            BeginEnd=parts[19]+';'+parts[23]
                            break
                    if 'Undefined' in BestMatchResults[i]:
                        prevGene=prevGene
                    else:
                        #print BeginEnd
                        FinalResults1.append(BestMatchResults[i]+";"+alignment_posStart[i]+";"+str(int(alignment_posStart[i])+int(length[i]))+";"+BeginEnd+"\n")
                    prevGene=BestMatchResults[i]
            
            FinalResults1.sort(key=Align_sort_key)

            #for i in range(0,len(FinalResults1)):
                #alignB=int(FinalResults1[i].split(";")[1])
                #alignE=int(FinalResults1[i].split(";")[2])
                #FinalResults.append(FinalResults1[i])
                #if alignB>prevEnd:
                    #FinalResults.append(FinalResults1[i])
                    #prevEnd=alignE
                #else:
                    #prevEnd=alignE

def SearchForQueryBegin():
    openInputProv='uploads/' + pathWhere + '/'+ pathWhere +'_inputProv.json'
    Iprov=open(openInputProv, 'r')
    linesIP = Iprov.readlines()
    lastlineIP=len(linesIP)

    for k in range(1,lastlineIP-1):
        if geneRef in linesIP[k]:
            global RegionName
            RegionName=linesIP[k].split('"')[11].split('...')[1]
            global regionBegin
            regionBegin=linesIP[k].split('"')[19]
            break

    Iprov.close()

def AddToPresults():
    openPresults='uploads/'+pathWhere+'/Prodigal_results/query_Presults.txt'
    Presults=open(openPresults, 'r')
    linesP = Presults.readlines()
    lastlineP=len(linesP)
    global QueryName
    QueryName=linesP[0].split('"')[1]
    for j in range(2,lastlineP-2):
        addToGenesToUse='yes'
        AlignBegin=linesP[j].split("_")[1]
        AlignEnd=linesP[j].split("_")[2]
        alBeEnd=AlignBegin+"---"+AlignEnd
        ProdigalResults.append(alBeEnd)


def GetGenesToUse():
    isThere="no"

    openInputProv='uploads/' + pathWhere + '/'+ pathWhere +'_inputProv.json'
    Iprov=open(openInputProv, 'r')
    linesIP = Iprov.readlines()
    lastlineIP=len(linesIP)

    for i in range(0,len(FinalResults1)-1):
        geneName=FinalResults1[i].split(";")[0].split("--")[0]
        geneBegin=FinalResults1[i].split(";")[1]
        geneEnd=FinalResults1[i].split(";")[2]
        geneBeginReal=FinalResults1[i].split(";")[3]
        geneEndReal=FinalResults1[i].split(";")[4]
        for j in range(0,len(ProdigalResults)-1):
            addToGenesToUse='yes'
            AlignBegin=ProdigalResults[j].split("---")[0]
            AlignEnd=ProdigalResults[j].split("---")[1]
            alBeEnd=AlignBegin+"---"+AlignEnd
            if len(GenesToUse)==0:
                addToGenesToUse='yes'
            for z in GenesToUse:
                if alBeEnd in z:
                    addToGenesToUse='no'


            if int(geneBegin)<=int(AlignBegin) and int(geneEnd)>=int(AlignEnd) and addToGenesToUse=='yes':
                addToGenesToUse='no'
                #klker coisa
                #print AlignBegin+".."+AlignEnd
                #print geneBegin+"--"+geneEnd
                prevGeneEnd=geneEnd
                global genome1
                genome1=geneName.split("...")[0]
                isThere="yes"
                break
        
        if isThere=="yes":
            for k in range(1,lastlineIP-1):
                line=linesIP[k].split('"')
                if line[7]==genome1 and line[19]==geneBeginReal:
                    GenesToUse.append(alBeEnd+"---"+linesIP[k]+"---"+geneBegin+"---"+geneEnd)
                    break
            isThere="no"

        Iprov.close()

    #print FinalResults1


def AnnotateGenome():
    genesLen=len(GenesToUse)
    pasS='no'
    timeToPrint='yes'
    ContigParts=[]
    global countParts
    countParts=prevParts
    #print '\n'.join([str(x) for x in GenesToUse])

    openInputProv='uploads/' + pathWhere + '/'+ pathWhere +'_inputProv.json'
    Iprov=open(openInputProv, 'r')
    linesIP = Iprov.readlines()
    lastlineIP=len(linesIP)

    openInputSeq='uploads/' + pathWhere + '/'+ pathWhere +'_inputWithSequences.json'
    Iseq=open(openInputSeq, 'r')
    linesS = Iseq.readlines()
    lastlineS=len(linesS)

    openNewFile='uploads/' + pathWhere + '/'+ pathWhere +'_inputP.json'
    openNewSeq='uploads/' + pathWhere + '/'+ pathWhere +'_inputSeq.json'
    fileResult=open(openNewFile, 'w')
    os.chmod(openNewFile, 0777)
    fileResultSeq=open(openNewSeq, 'w')
    os.chmod(openNewSeq, 0777)
    for x in range(0,lastlineIP-1):
        line=linesIP[x].split('"')
        if x==0 or x==lastlineIP:
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

        if pasS!='yes' and reference==QueryName.strip():
            pasS=='no'
            begin=int(line[19])
            end=int(line[23])
            alignB=int(GenesToUse[0].split("---")[0])
            alignE=int(GenesToUse[0].split("---")[1])
            if alignB>1 or alignB==1:
                if timeToPrint=='yes':
                    print line[27]
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
            for p in range(0,genesLen):
                gene=GenesToUse[p].split("---")[2]
                OrganismName=gene.split('"')[3]
                geneB=gene.split('"')[19]
                geneE=gene.split('"')[23]
                contig1=gene.split('"')[27]
                contigs='"contig": "'+contig1+'"'
                gene=gene.replace('"name": "'+OrganismName+'"','"name": "'+line[3]+'"')
                gene=gene.replace('"begin": "'+geneB+'"','"begin": "'+str(int(regionBegin)+int(GenesToUse[p].split("---")[0]))+'"')
                gene=gene.replace('"end": "'+geneE+'"','"end": "'+str(int(regionBegin)+int(GenesToUse[p].split("---")[1]))+'"')
                parts=gene.split(contigs)
                newContig='"contig": "'+contig+'"'
                gene=parts[0]+newContig+parts[1]
                if GenesToUse[0].split("---")[2].split('"')[7]=="1":
                    genoma=int(numGenomes)
                else:
                    genoma=int(genome1)-1
                gene=gene.replace(str(genome1)+"...",str(genoma)+"...")
                gene=gene.replace('"genome": "'+str(genome1)+'"','"genome": "'+str(genoma)+'"')
                gene=gene.strip()+'\n'
                fileResult.write(gene)
                lastEnd=GenesToUse[p].split("---")[1]
                try:
                    nextGene=GenesToUse[p+1].split("---")[2]
                    geneB1=int(nextGene.split('"')[19])
                    gap=int(GenesToUse[p+1].split("---")[0])-int(GenesToUse[p].split("---")[1])
                    #print gap
                    if gap > 1:
                        #newWrite=linesIP[x].replace(',"contig": "'+contig+'"',"")
                        newWrite=linesIP[x].replace('"begin": "'+str(begin)+'"','"begin": "'+str(int(GenesToUse[p].split("---")[1]))+'"')
                        #print str(int(GenesToUse[p].split("---")[1]))
                        #print str(int(GenesToUse[p+1].split("---")[0]))
                        newWrite=newWrite.replace('"end": "'+str(end)+'"','"end": "'+str(int(GenesToUse[p+1].split("---")[0]))+'"')
                        newLine=newWrite.replace('"gene": "'+line[3]+'"','"gene": "'+line[3]+"_GAP_"+str(countParts)+'"')
                        newLine=newLine.replace('"reference": "'+line[3]+'"','"reference": "'+line[3]+"_GAP_"+str(countParts)+'"')
                        newWrite=newWrite.replace('"product": ""','"product": "Undefined"')
                        countParts+=1
                        ContigParts.append(newWrite)
                        fileResult.write(newWrite)

                except IndexError:
                    lastEnd=lastEnd

            if int(lastEnd)<int(end):
                newLine=linesIP[x].replace('"begin": "'+str(begin)+'"','"begin": "'+str(int(lastEnd))+'"')
                newLine=newWrite.replace('"gene": "'+line[3]+'"','"gene": "'+line[3]+"_GAP_"+str(countParts)+'"')
                newLine=newLine.replace('"reference": "'+line[3]+'"','"reference": "'+line[3]+"_GAP_"+str(countParts)+'"')
                newLine=newLine.replace('"product": ""','"product": "Undefined"')
                ContigParts.append(newLine)
                fileResult.write(newLine)

            #else:
            #   fileResult.write(linesIP[x])
        else:
            if x==0 or x==lastlineIP:
                pasS='yes'
            else:
                fileResult.write(linesIP[x])

    genome=GenesToUse[0].split("---")[2].split('"')[7]
    if genome=="1":
        genoma=int(numGenomes)
    else:
        genoma=int(genome)-1

    for p in range(0,lastlineS):
        line=linesS[p].split('"')
        if RegionName ==line[3]:
            sequence=line[11]
            #print sequence
            break

    for l in range(0,lastlineS):
        line=linesS[l].split('"')
        for w in range(0,genesLen):
            gene=GenesToUse[w].split("---")[2]
            Abegin=int(GenesToUse[w].split("---")[0])
            Aend=int(GenesToUse[w].split("---")[1])
            GeneSBegin=int(GenesToUse[w].split("---")[3])
            GeneSEnd=int(GenesToUse[w].split("---")[4])
            gene=gene.split('"');
            geneLen=len(gene);
            reference=gene[geneLen-2]
            if line[3]==reference:
                sequenceGene=line[11]
                #newGeneBegin=Abegin
                #print newGeneBegin
                #newGeneEnd=(GeneSEnd-GeneSBegin)-(GeneSEnd-Aend)
                sequencePart=sequence[Abegin:Aend]
                newline=linesS[l].replace(sequenceGene,sequencePart)
                newline=newline.replace('"genome": "'+str(genome)+'"','"genome": "'+str(genoma)+'"')
                fileResultSeq.write(newline)
                break
        if line[3]==QueryName.strip():
            #sequence=line[11]
            for m in range(0,len(ContigParts)):
                parts=ContigParts[m].split('"')
                ToChange=parts[len(parts)-2]
                contigB=int(ContigParts[m].split('"')[19])
                contigE=int(ContigParts[m].split('"')[23])
                #print contigB
                #print contigE
                if contigB==contigE:
                    sequencePart=sequence[contigE]
                else:
                    sequencePart=sequence[contigB:contigE]
                #print QueryName
                newline=linesS[l].replace(sequence,sequencePart)
                newline=newline.replace(QueryName,ToChange)
                fileResultSeq.write(newline)

        else:
            fileResultSeq.write(linesS[l])

    fileResult.close()
    fileResultSeq.close()

    Iprov.close()

    os.remove(openInputProv)
    os.rename(openNewFile,openInputProv)

    os.remove(openInputSeq)
    os.rename(openNewSeq,openInputSeq)  







genomedb=genomeDB.split("...")[0]
CreateFastaFromInput(genomedb)
Create_Blastdb(fnaFileOutput)
allSequences=open(inputSequence , 'r')
linesS = allSequences.readlines()

prevParts=1
for i in range(1,len(linesS)-1):
    if '{"gene":' in linesS[i]:
        linha=linesS[i].split('"')
        genomeQuery=linha[7]
        if genomeQuery==genomeToBeQuery:
            lengLine=len(linha)
            geneRef=linha[3]
            querySequence=linha[11]

            GetSequence(geneRef)

            Create_FASTAquery(geneRef,querySequence)

            blast_out_file = "uploads/" + pathWhere + "/blastdbs/" + "blastResults_blastout" + "_subj.xml"
            cline = NcbiblastnCommandline(query=nameFASTA, db=name,evalue=evalue, out=blast_out_file, outfmt=5)
            stdout, stderr = cline()
            rec2 = open(blast_out_file)
            blast_records = NCBIXML.parse(rec2)
            os.remove(blast_out_file)

            for blast_record in blast_records:
                    if len(blast_record.alignments)==0:
                            print 'not exists'
                    else:
                            for alignment in blast_record.alignments:
                                    for hsp in alignment.hsps:
                                            minScore=float(MinScore)
                                            Score=float(len(hsp.match))/float(alignment.length)
                                            #or re.search("ENA|",alignment.title)
                                            if "NODE_" in alignment.title or 'ENA|' in alignment.title:
                                                    geneName=alignment.title.split("|")[3]
                                            else:
                                                    try:
                                                        geneName=alignment.title.split("|")[6]
                                                    except IndexError:
                                                        geneName=alignment.title.split("|")[3]
                                            if hsp.expect < float(evalue) and Score >= minScore:
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
                                                    BestMatchResults.append(genomeDB + str(geneName).strip()+'--'+geneRef)
                                                    length.append(str(hsp.align_length-1))
                                                    alignment_posStart.append(str(hsp.query_start))


            CreateSearchResults()

            AddTail()

            os.system("cd Prodigal/Prodigal-2.60 && ./prodigal -i ../../uploads/"+pathWhere+"/Sequence_files/query_sequence.fasta -c -m -g 11 -p single -f sco -q > ../../uploads/"+pathWhere+"/Prodigal_results/query_Presults.txt")

            AddToPresults()

            GetGenesToUse()

            SearchForQueryBegin()

            AnnotateGenome()

            prevParts=countParts

            ProdigalResults=[]
            GenesToUse=[]
            FinalResults1=[]




allSequences.close()


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

#if countResults>0:
    #print '---'.join([str(x) for x in BestMatchResults])
    #print '---'.join([str(x) for x in length])
    #print '---'.join([str(x) for x in alignment_posStart])



os.remove(nameFASTA)
#os.remove(fileSequencepath)