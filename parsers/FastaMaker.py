import re
import sys
import os

array = sys.argv
path=array[1]
arrayOfFiles=array[2].split("---")
isContig=array[3]

if isContig=='yes':
	countContig=0
	for i in range(0,len(arrayOfFiles)-1):
		filename=arrayOfFiles[i].split("...")[0]
		orgName=arrayOfFiles[i].split("...")[1]
		genome=arrayOfFiles[i].split("...")[2]
		openwhich='uploads/' + path + '/'+ path +'_inputWithSequences.json'
		inf=open(openwhich, 'r')
		openwhere='uploads/' + path + '/FastaToExport/'+filename+'_new.fasta'
		result=open(openwhere,'w')

		for line in inf:
			if '{"gene":' in line:
				genomeToCheck=line.split('"')[7]
				if genomeToCheck==genome:
					countContig+=1
					name=line.split('"')[3]
					sequence=line.split('"')[11]
					result.write('>'+name+'[Seq'+str(countContig)+']\n')
					result.write(sequence+'\n')

else:
	for i in range(0,len(arrayOfFiles)-1):
		filename=arrayOfFiles[i].split("...")[0]
		orgName=arrayOfFiles[i].split("...")[1].replace('..','_')
		genome=arrayOfFiles[i].split("...")[2]
		openwhich='uploads/' + path + '/'+ path +'_inputWithSequences.json'
		inf=open(openwhich, 'r')
		openwhere='uploads/' + path + '/FastaToExport/'+filename+'_new.fasta'
		result=open(openwhere,'w')
		result.write('>'+orgName+'\n')
		for line in inf:
			if '{"gene":' in line:
				genomeToCheck=line.split('"')[7]
				if genomeToCheck==genome:
					sequence=line.split('"')[11]
					result.write(sequence)