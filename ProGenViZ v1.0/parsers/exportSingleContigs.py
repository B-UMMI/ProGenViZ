import re
import sys
import os

array = sys.argv
path=array[1]
genome=array[2]
exportType=array[3]
fileName=array[4]
exportContig=array[5]

openInputSeq='uploads/' + path + '/FastaToExport/'+ fileName +'_new.fasta'
openResultFasta='uploads/' + path + '/FastaToExport/'+ fileName  +'_newP.fasta'
fileResultFasta=open(openResultFasta, 'w')
os.chmod(openResultFasta, 0755)
InputFileSeq=open(openInputSeq, 'r')
linesIS = InputFileSeq.readlines()
lastlineIS=len(linesIS)

openInput='uploads/' + path + '/'+ path +'_inputProv.json'
openResultGff='uploads/' + path + '/Results/'+ path +'.gff'


InputFile=open(openInput, 'r')

fileResultGff=open(openResultGff, 'w')
os.chmod(openResultGff, 0755)


linesI = InputFile.readlines()
lastlineI=len(linesI)
firstLine='yes'
countCDS=0
prevGene=""
prevBegin=""
countLines=0
match1='"genome": "'+genome+'"'
contigName=''
countSequence=0
firstTimeCheck='yes'
countNodes=1
isNode='no'
ToExport='no'
match='[Seq'+exportContig+']'
for i in range(0,lastlineIS):
	if match in linesIS[i]:
		ToExport='yes'
		fileResultFasta.write(linesIS[i])
	elif re.match('[A-Z]',linesIS[i]) and ToExport=='yes':
		fileResultFasta.write(linesIS[i])
	elif ToExport=='yes' and not re.match('[A-Z]',linesIS[i]):
		ToExport='no'
		break



for i in range(1,lastlineI):
	if match1 in linesI[i]:
		PartName=linesI[i].split('"')[3]
		contigNumber=linesI[i].split('"')[27]
		#print contigNumber
		#print contigToExport
		if contigNumber!=exportContig:  #MUDAR ISTO ARRANJAR MELHOR SOLUCAO
			match=match
		else:
			try:
				geneReference=linesI[i].split('"')[47]
			except IndexError:
				try:
					geneReference=linesI[i].split('"')[43]
				except IndexError:
					geneReference=linesI[i].split('"')[39]
			#if firstLine=='yes':
			line=linesI[i].split('"')
			nome=line[3]
			line=linesI[i].split('"')
			#name=line[3]
			gene=line[11]
			product=line[15]
			begin=line[19]
			end=line[23]
			try:
				genomeSize=line[43]
				reference=line[47]
			except IndexError:
				reference=line[39]
			strand=line[31]
			if nome=="":
				nome="."
			if strand=="":
				strand="."
			if product=="":
				product="."
			if begin=="":
				begin="."
			if end=="":
				end="."
			if reference=="":
				reference="."
			else:
				try:
					reference=reference.split("|")[1]
				except IndexError:
					reference=reference
			if gene=="":
				gene="."
			else:
				gene=gene.split("...")[1]
				countCDS+=1
				numParts=gene.split('_')
				gene=""
				for x in range(0,len(numParts)-1):
					gene=gene+numParts[x]+"_"
				gene=gene.strip("_")
			if (prevGene==gene and prevBegin==begin) or product=="Undefined" or product==".":
				prevGene=gene
				prevBegin=begin
			else:
				fileResultGff.write(nome+"\t"+"ProGenViZ"+"\t"+"CDS"+"\t"+begin+"\t"+end+"\t"+".\t"+strand+"\t.\t"+"ID="+str(countCDS)+";Name="+gene+";product="+product+";Dbxref=GeneID:"+reference+"\n")
				prevGene=gene
				prevBegin=begin


fileResultGff.close()
InputFile.close()
fileResultFasta.close()
InputFileSeq.close()
