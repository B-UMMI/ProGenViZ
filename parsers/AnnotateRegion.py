import re
import sys
import os

array = sys.argv
path=array[1]
RegionName=array[2]
numGenomes=array[3]
regionBegin=array[4]
regionEnd=array[5]

opensearchResults='uploads/' + path + '/Search_Results/'+ RegionName +'_SearchResults.txt'
openPresults='uploads/' + path + '/Prodigal_results/'+ RegionName +'_Presults.txt'
openInputProv='uploads/' + path + '/'+ path +'_inputProv.json'
openInputSeq='uploads/' + path + '/'+ path +'_inputWithSequences.json'
removeFile='uploads/' + path + '/Sequence_files/'+ RegionName +'_sequence.fasta'
#removeFile2='uploads/' + path + '/'+ RegionName +'_query.ffn'

openNewFile='uploads/' + path + '/'+ path +'_inputP.json'
openNewSeq='uploads/' + path + '/'+ path +'_inputSeq.json'


fileResult=open(openNewFile, 'w')
os.chmod(openNewFile, 0755)

fileResultSeq=open(openNewSeq, 'w')
os.chmod(openNewSeq, 0755)

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
ContigParts=[]
countParts=1
isThere="no"

prevGeneEnd=-1
PrevLineProdigal=0
PrevLineBLAST=1

for i in range(1,lastlineR):
	geneName=linesR[i].split(";")[0]
	geneBegin=linesR[i].split(";")[1]
	geneEnd=linesR[i].split(";")[2]
	geneBeginReal=linesR[i].split(";")[3]
	geneEndReal=linesR[i].split(";")[4]

	threshBLAST = (int(geneBegin) + int(geneEnd)) * 0.1
	#print PrevLineProdigal
	#print lastlineP
	for j in range(PrevLineProdigal+1,lastlineP):
		if linesP[j].startswith(">"):
			addToGenesToUse='yes'
			AlignBegin=linesP[j].split("_")[1]
			AlignEnd=linesP[j].split("_")[2]
			alBeEnd=AlignBegin+"---"+AlignEnd
			if len(GenesToUse)==0:
				addToGenesToUse='yes'
			for z in GenesToUse:
				if alBeEnd in z:
					addToGenesToUse='no'

			threshProdigal = (int(AlignBegin) + int(AlignEnd)) * 0.1

			if int(geneBegin) <= int(AlignBegin) and int(AlignEnd) <= int(geneEnd) and addToGenesToUse=='yes': #Resultados do BLAST englobam os resultados do Prodigal
				addToGenesToUse='no'
				#klker coisa
				#print AlignBegin+".."+AlignEnd
				#print geneBegin+"--"+geneEnd
				prevGeneEnd=geneEnd
				PrevLineProdigal=j
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
				PrevLineProdigal=j
				isThere="yes"
				break

			elif int(AlignBegin) - int(geneBegin) >= 0 and int(AlignBegin) - int(geneBegin) <= threshProdigal and int(AlignEnd) - int(geneEnd) >= 0 and int(AlignEnd) - int(geneEnd) <= threshProdigal and addToGenesToUse=='yes': #Inicio do BLAST fora dos resultados do Prodigal mas o final no interior
				addToGenesToUse='no'
				#klker coisa
				#print AlignBegin+".."+AlignEnd
				#print geneBegin+"--"+geneEnd
				prevGeneEnd=geneEnd
				genome=geneName.split("...")[0]
				PrevLineProdigal=j
				isThere="yes"
				break

			elif int(AlignBegin) - int(geneBegin) >= 0 and int(AlignBegin) - int(geneBegin) <= threshProdigal and int(geneEnd) - int(AlignEnd) >= 0 and int(geneEnd) - int(AlignEnd) <= threshProdigal and addToGenesToUse=='yes': #Final do BLAST fora dos resultados do Prodigal mas o inicio no interior
				addToGenesToUse='no'
				#klker coisa
				#print AlignBegin+".."+AlignEnd
				#print geneBegin+"--"+geneEnd
				prevGeneEnd=geneEnd
				genome=geneName.split("...")[0]
				PrevLineProdigal=j
				isThere="yes"
				break

			#else:
				#PrevLineProdigal=j


	
	if isThere=="yes":
		#print 'AQUI'
		for k in range(1,lastlineIP-1):
			line=linesIP[k].split('"')
			if line[7]==genome and line[19]==geneBeginReal:
				GenesToUse.append(alBeEnd+"---"+linesIP[k]+"---"+geneBegin+"---"+geneEnd)
				break
		isThere="no"
		
genesLen=len(GenesToUse)
pasS='no'
timeToPrint='yes'
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
			geneString = line[11]
			geneGenome = geneString.split('...')[0]
			geneString = geneString.split('...')[1]
			newLine=linesIP[x].replace('"gene": "'+geneGenome+'...'+geneString+'"','"gene": "'+geneGenome+'...'+line[3]+"_GAP_"+str(countParts)+'"')
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
				genoma=int(genome)-1
			gene=gene.replace(str(genome)+"...",str(genoma)+"...")
			gene=gene.replace('"genome": "'+str(genome)+'"','"genome": "'+str(genoma)+'"')
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
					geneString = line[11]
					geneGenome = geneString.split('...')[0]
					geneString = geneString.split('...')[1]
					newWrite=newWrite.replace('"end": "'+str(end)+'"','"end": "'+str(int(GenesToUse[p+1].split("---")[0]))+'"')
					newLine=newWrite.replace('"gene": "'+geneGenome+'...'+geneString+'"','"gene": "'+geneGenome+'...'+line[3]+"_GAP_"+str(countParts)+'"')
					newLine=newLine.replace('"reference": "'+line[3]+'"','"reference": "'+line[3]+"_GAP_"+str(countParts)+'"')
					newWrite=newLine.replace('"product": ""','"product": "Undefined"')
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
		#	fileResult.write(linesIP[x])
	else:
		if x==0 or x==lastlineIP-1:
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
	#print RegionName
	if line[3] in RegionName:
		sequence=line[11]
		#print line[3]
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
		#print reference
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
			print newline

	else:
		fileResultSeq.write(linesS[l])




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
os.remove(removeFile)


