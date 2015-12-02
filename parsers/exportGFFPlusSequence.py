import re
import sys
import os

array = sys.argv
path=array[1]
genome=array[2]
contigName=array[3]
contigName='"contig": "'+contigName+'"'
genomeName='"genome": "'+genome+'"'
exportString=array[4]
exportString=exportString.replace('-.','|')
exportString=exportString.replace('__',' ')
exportString=exportString.replace('...',')')
exportString=exportString.replace('..','(')
exportArray=exportString.split('---')

openInputSeq='uploads/' + path + '/'+ path +'_inputWithSequences.json'
openInput='uploads/' + path + '/'+ path +'_inputProv.json'
openResultGff='uploads/' + path + '/Results/'+ path +'.gff'
openResultFasta='uploads/' + path + '/Results/'+ path +'.fasta'

InputFile=open(openInput, 'r')
InputFileSeq=open(openInputSeq, 'r')

fileResultGff=open(openResultGff, 'w')
os.chmod(openResultGff, 0755)

fileResultFasta=open(openResultFasta, 'w')
os.chmod(openResultFasta, 0755)

linesI = InputFile.readlines()
lastlineI=len(linesI)
linesIS = InputFileSeq.readlines()
lastlineIS=len(linesIS)
countCDS=0
prevGene=""
prevBegin=""
countLines=0
sequenceBegin=0
sequenceEnd=0
match='"genome": "'+genome+'"'
firstLine='yes'
prevRef=""
prevBegin1=""
for j in exportArray:
	geneReference=j.split("--")[0]
	geneBegin=j.split("--")[1]
	geneBegin='"begin": "'+geneBegin+'"'

	for i in range(1,lastlineI):
		if prevRef!=geneReference and prevBegin1!=geneBegin and geneReference in linesI[i] and geneBegin in linesI[i] and contigName in linesI[i] and genomeName in linesI[i]:
			if firstLine=='yes':
				line=linesI[i].split('"')
				name=line[3]
				fileResultFasta.write('>'+name+'_region\n')
				firstLine='no'
			for j in range(0,lastlineIS-1):
				parts=linesIS[j].split('"')
				reference=parts[3]
				sequence=parts[11]

				if geneReference in reference:
					sequenceEnd=sequenceEnd+len(sequence)
					fileResultFasta.write(sequence)
					break
			try:
				line=linesI[i].split('"')
				name=line[3]
				gene=line[11]
				product=line[15]
				begin=line[19]
				end=line[23]
				genomeSize=line[43]
				reference=line[47]
				strand=line[31]
				if name=="":
					name="."
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
					reference=reference.split("|")[1]
				if gene=="":
					gene="."
				else:
					gene=gene.split("...")[1]
					countCDS+=1
				if (prevGene==gene and prevBegin==begin) or 'Undefined'in geneReference:
					prevGene=gene
					prevBegin=begin
				else:
					if countLines==0:
						#fileResultGff.write(name+"_region\t"+"MyProgram"+"\t"+"region"+"\t1\t"+genomeSize+"\t"+".\t.\t.\t"+"strain="+name+"\n")
						countLines+=1
						fileResultGff.write(name+"_region\t"+"MyProgram"+"\t"+"CDS"+"\t"+str(sequenceBegin)+"\t"+str(sequenceEnd)+"\t"+".\t"+strand+"\t.\t"+"ID="+str(countCDS)+";Name="+gene+";product="+product+";Dbxref=GeneID:"+reference+"\n")
					else:
						fileResultGff.write(name+"_region\t"+"MyProgram"+"\t"+"CDS"+"\t"+str(sequenceBegin+1)+"\t"+str(sequenceEnd)+"\t"+".\t"+strand+"\t.\t"+"ID="+str(countCDS)+";Name="+gene+";product="+product+";Dbxref=GeneID:"+reference+"\n")
						prevGene=gene
						prevBegin=begin
				sequenceBegin=sequenceEnd
			except IndexError:
				
				line=linesI[i].split('"')
				name=line[3]
				gene=line[11]
				product=line[15]
				begin=line[19]
				end=line[23]
				reference=line[35]
				strand=line[27]
				if name=="":
					name="."
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
					reference=reference
				if gene=="":
					gene="."
				else:
					gene=gene.split("...")[1]
					countCDS+=1
				if (prevGene==gene and prevBegin==begin) or 'Undefined' in geneReference:
					prevGene=gene
					prevBegin=begin
				else:
					if countLines==0:
						#fileResultGff.write(name+"_region\t"+"MyProgram"+"\t"+"region"+"\t1\t"+genomeSize+"\t"+".\t.\t.\t"+"strain="+name+"\n")
						countLines+=1
						fileResultGff.write(name+"_region\t"+"MyProgram"+"\t"+"CDS"+"\t"+str(sequenceBegin)+"\t"+str(sequenceEnd)+"\t"+".\t"+strand+"\t.\t"+"ID="+str(countCDS)+";Name="+gene+";product="+product+";Dbxref=GeneID:"+reference+"\n")
					else:
						fileResultGff.write(name+"_region\t"+"MyProgram"+"\t"+"CDS"+"\t"+str(sequenceBegin+1)+"\t"+str(sequenceEnd)+"\t"+".\t"+strand+"\t.\t"+"ID="+str(countCDS)+";Name="+gene+";product="+product+";Dbxref=GeneID:"+reference+"\n")
						prevGene=gene
						prevBegin=begin
				sequenceBegin=sequenceEnd
				countCDS=countCDS
			prevRef=geneReference
			prevBegin1=geneBegin
			break



fileResultGff.close()
InputFile.close()
fileResultFasta.close()
InputFileSeq.close()