import re
import sys
import os
from Bio import SeqIO
import random

array = sys.argv
path=array[1]
PartToChange=int(array[2])
openwhich='uploads/' + path + '/'+ path +'_inputWithContigs.json'
inf=open(openwhich, 'r')
openwhere='uploads/' + path + '/'+ path +'_inputSize.json'
result=open(openwhere,'w')
os.chmod(openwhere, 0755)
linha = inf.readlines()
lastline=len(linha)
lastlineGenome=0
lastlineFor=0
breakall='no'
count=1
count1=1
GenomeAnnotated=0
AnnoGenome=""
prevBegin=0
countUndefined=1
prevContig=""
firstTime='yes'
for i in range(0,lastline-1):
	if "{\"name\":" in linha[i]:
		currentGenome = linha[i].split('"')[7]
		if int(currentGenome)>PartToChange:
			if firstTime=='yes':
				lastlineGenome-=3
				firstTime='no'
			if currentGenome!=AnnoGenome:
				GenomeAnnotated=0
				AnnoGenome=currentGenome
			for j in range(lastlineFor, lastline-1):
				if "{\"name\":" in linha[j]:
					genome=linha[j].split('"')[7]
					begin1 = linha[j].split('"')[19]
					end1 = linha[j].split('"')[23]
					if genome != currentGenome:
						break
					else:
						lastlineFor+=1
						if begin1=='':
							lastlineGenome+=1
						else:
							begin1 = int(begin1)
							end1 = int(end1)

							size1 = end1 - begin1
							number1=int(size1/500)
							if number1 > 1:
								while count1 < number1:
									lastlineGenome+=1
									count1+=1
							else:
								lastlineGenome+=1
							count1=1
				else:
					lastlineFor+=1
					lastlineGenome+=1
		
			begin = linha[i].split('"')[19]
			end = linha[i].split('"')[23]
			cont = linha[i].split('"')[27]
			if begin=="":
				result.write(linha[i].strip() + "\"lastlineGenome\": \"" + str(lastlineGenome) + "\"," + "\"AnnotatedG\": \"" + str(GenomeAnnotated) + "\",\n")
			else:
				begin = int(begin)
				end = int(end)
				#if prevBegin < begin and prevContig==cont:
					#size = begin - prevBegin
					#number=int(size/500)
					#linhaGene=linha[i].strip().split(",")[2]
					#linhaGenome=linhaGene.split("...")[0]
					#linhaUndefined=linha[i].strip().replace(linhaGene, linhaGenome + '...Undefined_Region"')
					#linhaProduct=linhaUndefined.split('",')[3]
					#linhaBegin=linhaUndefined.split('",')[4]
					#linhaEnd=linhaUndefined.split('",')[5]
					#try:
					#	linhaReference=linha[i].strip().split(",")[11]
					#except IndexError:
					#	linhaReference=linha[i].strip().split(",")[8]
					#linhaUndefined=linhaUndefined.replace(linhaBegin , '"begin": "'+str(prevBegin))
					#linhaUndefined=linhaUndefined.replace(linhaEnd , '"end": "'+str(begin))
					#linhaUndefined=linhaUndefined.replace(linhaProduct , '"product": "Undefined')
					#linhaUndefined=linhaUndefined.replace(linhaReference , '"reference": "Undefined"')
					#if number > 1:
					#	while countUndefined < number:
					#		result.write(linhaUndefined + "\"lastlineGenome\": \"" + str(lastlineGenome) + "\"," + "\"AnnotatedG\": \"" + str(GenomeAnnotated) + "\",\n")
					#		countUndefined+=1
					#else:
					#	result.write(linhaUndefined + "\"lastlineGenome\": \"" + str(lastlineGenome) + "\"," + "\"AnnotatedG\": \"" + str(GenomeAnnotated) + "\",\n")
					#countUndefined=1
					#prevBegin = end
				#else:
					#prevContig=cont

				if '"genomeType": "COMPLETE"' in linha[i]:
					size = end - begin
					GenomeAnnotated += size
					number=int(size/500)
					if number > 1:
						while count < number:
							result.write(linha[i].strip() + "\"lastlineGenome\": \"" + str(lastlineGenome) + "\"," + "\"AnnotatedG\": \"" + str(GenomeAnnotated) + "\",\n")
							count+=1
					else:
						result.write(linha[i].strip() + "\"lastlineGenome\": \"" + str(lastlineGenome) + "\"," + "\"AnnotatedG\": \"" + str(GenomeAnnotated) + "\",\n")

					count=1
			
				else:
					size = end - begin
					GenomeAnnotated += size
					number=int(size/500)
					if number > 1:
						while count < number:
							result.write(linha[i].strip() + "\"lastlineGenome\": \"" + str(lastlineGenome) + "\"," + "\"AnnotatedG\": \"" + str(GenomeAnnotated) + "\",\n")
							count+=1
					else:
						result.write(linha[i].strip() + "\"lastlineGenome\": \"" + str(lastlineGenome) + "\"," + "\"AnnotatedG\": \"" + str(GenomeAnnotated) + "\",\n")

					count=1
				prevBegin = end
		else:
			lastlineGenome+=1
			result.write(linha[i])
	else:
		lastlineGenome+=1
		result.write(linha[i])

result.write(']\n')
inf.close()
result.close()
#os.remove(openwhich)