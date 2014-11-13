import re
import sys
import os

array = sys.argv
path=array[1]
geneReference=array[2]
queryGene=array[3]
geneReference=geneReference.replace("---"," ")
geneReference=geneReference.replace("...","|")
queryGene=queryGene.replace("---","_")
openwhich='uploads/' + path + '/'+ path +'_inputWithSequences.json'
openwhere='uploads/' + path + '/Sequence_files/'+ queryGene.split("...")[1] +'_sequence.fasta'
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
