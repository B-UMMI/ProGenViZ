import re
import sys
import os
from Bio import SeqIO

array = sys.argv
path=array[1]
PartToChange=int(array[2])
openwhich='uploads/' + path + '/'+ path +'_inputTemp.json'
inf=open(openwhich, 'r')
openwhere='uploads/' + path + '/'+ path +'_inputWithContigs.json'
result=open(openwhere,'w')
os.chmod(openwhere, 0777)
result.write('[\n\n')
countContigs=1
sizeContig=0
countGenes = 0
countLines=0
prevEnd = 0
prevGenome = str(int(array[2])+1)
countGenesFaa=0
CompleteGenome='no'
prevContigNumber = 'contig000001'
prevContigNum = '1'
contigfile = 'no'
lastlinefaa='no'
AnnotatedG='no'
prevContigSize=0
countLines1=0
lines = inf.readlines()
contig = "{\"contig"+str(countContigs)+"\": [\n"
for i in range(0, len(lines)-1):
	if re.search('"contig":',lines[i]):
		currentGenome = lines[i].split('"')[7]
		if int(currentGenome)>PartToChange:
			if re.search('"genomeType": "COMPLETE"',lines[i]):
				genome = lines[i].split('"')[7]
				if genome != prevGenome:
					countContigs+=1
					if CompleteGenome=='yes':
						AnnotatedG='no'
						contig += "{\"contig"+str(countContigs)+"\": [\n"
					elif AnnotatedG=='yes':
						contig += "]\n}\n"
						AnnotatedG='no'
						contig += "{\"contig"+str(countContigs)+"\": [\n"
					else:
						contig += "]\n}\n"
				genomeSize=lines[i].split('"genomeSize": ')[1]
				genomeSize=genomeSize.split('"')[1]
				lengthsequence=int(genomeSize)
				DoneSeq=0
				NextContigSize=0
				NextContigSize=100000  #Set SIZE OF CONTIGS
				lines=lines[i].replace('"begin": "0"','"begin": "'+str(DoneSeq)+'"')
				lines=lines.replace('"end": "2036820"','"end": "'+str(NextContigSize)+'"')
				lines=lines.strip()
				while DoneSeq<lengthsequence:
					addline = lines + "\"contig\": \"contig"+ str(countContigs) + "\", \n"			
					contig += addline
					contig += "]\n}\n"
					countContigs += 1
					contig += "{\"contig"+str(countContigs)+"\": [\n"
					DoneSeq+=NextContigSize
					lines=lines.replace('"begin": "'+str(DoneSeq-NextContigSize)+'"','"begin": "'+str(DoneSeq)+'"')	
					lines=lines.replace('"end": "'+str(DoneSeq)+'"','"end": "'+str((DoneSeq+NextContigSize))+'"')
					if (lengthsequence-DoneSeq)<10000:
						break #ACABAR

				addline = lines + "\"contig\": \"contig"+ str(countContigs) + "\", \n"			
				contig += addline
				contig += "]\n}\n"
				countContigs += 1
				CompleteGenome='yes'
			else:
				AnnotatedG='yes'
				countLines1+=1
				lastlinefaa='no'
				contigfile = 'yes'
				genome = lines[i].split('"')[7]
				if lines[i].split('"')[25]=='contig':
					contigNumber = lines[i].split('"')[27]
				elif lines[i].split('"')[29]=='contig':
					contigNumber = lines[i].split('"')[31]
				else:
					contigNumber = lines[i].split('"')[35]
				end = lines[i].split('"')[23]
				if genome != prevGenome:
						if CompleteGenome=='yes':
							CompleteGenome='no'
						else:
							contig += "]\n}\n"
						countContigs += 1
						contig += "{\"contig"+str(countContigs)+"\": [\n"
						sizeContig = 0
						prevEnd = 0
						sizeContig += int(end) - prevEnd
						addline = lines[i].strip() + "\"contig\": \"contig"+ str(countContigs) + "\", \n"
						contig += addline
						prevEnd=int(end)
						prevGenome = genome
				else:
					if (contigNumber == prevContigNumber or prevContigNum==contigNumber):
						addline = lines[i].strip() + "\"contig\": \"contig"+ str(countContigs) + "\", \n"
						contig += addline
						prevContigNumber = contigNumber
						prevContigNum=contigNumber
					else:
						contig += "]\n}\n"
						countContigs += 1
						contig += "{\"contig"+str(countContigs)+"\": [\n"	
						addline = lines[i].strip() + "\"contig\": \"contig"+ str(countContigs) + "\", \n"			
						contig += addline
						prevContigNumber = contigNumber
						prevContigNum = contigNumber
					prevGenome = genome
		else:
			if currentGenome=='1':
				print lines[i]
			result.write(lines[i])
	else:
		if re.match("{",lines[i]):
			AnnotatedG='yes'
			try:
				currentGenome = lines[i].split('"')[7]
			except IndexError:
				result.write(lines[i])
				currentGenome=PartToChange
			if int(currentGenome)>PartToChange:
				if lines[i].split('"')[35] == '.faa':
					lastlinefaa='yes'
					contigfile = 'no'
					countGenes+=1
					genome = lines[i].split('"')[7]
					if genome != prevGenome:
						if CompleteGenome=='yes':
							CompleteGenome='no'
						else:
							contig += "]\n}\n"
						countContigs += 1
						contig += "{\"contig"+str(countContigs)+"\": [\n"
						countGenesFaa = 0
						countGenesFaa+= 1
						addline = lines[i].strip() + "\"contig\": \"contig"+ str(countContigs) + "\", \n"
						contig += addline
						prevGenome = genome
					else:
					#if countGenesFaa >= 40:
						#contig += "]\n}\n"
						#countContigs += 1
						#contig += "{\"contig"+str(countContigs)+"\": [\n"
						#countGenesFaa = 0
						#countGenesFaa += 1
						#addline = lines.strip() + "\"contig\": \"contig"+ str(countContigs) + "\", \n"
						#contig += addline
					#else:
						addline = lines[i].strip() + "\"contig\": \"contig"+ str(countContigs) + "\", \n"
					#countGenesFaa += 1
						contig += addline
				else:
					lastlinefaa='no'
					contigfile = 'no'
					countGenes+=1
					begin = lines[i].split('"')[19]
					end = lines[i].split('"')[23]
					genome = lines[i].split('"')[7]
					if genome != prevGenome:
						if CompleteGenome=='yes':
							CompleteGenome='no'
						else:
							contig += "]\n}\n"
						countContigs += 1
						contig += "{\"contig"+str(countContigs)+"\": [\n"
						sizeContig = 0
						prevEnd = 0
					#sizeContig += int(end) - prevEnd
						addline = lines[i].strip() + "\"contig\": \"contig"+ str(countContigs) + "\", \n"
						contig += addline
						prevEnd=int(end)
						prevGenome = genome
					else:
					#if begin=='':
						#contig += addline
					#else:
						#begin = int(begin)
						#end = int(end)
						#if countGenes == 1:
							#sizeContig += end
						#else:
							#sizeContig += end - prevEnd			
						#if sizeContig > 20000:
							#contig += "]\n}\n"
							#countContigs += 1
							#contig += "{\"contig"+str(countContigs)+"\": [\n"
							#sizeContig = 0
							#sizeContig += end - prevEnd
							#addline = lines.strip() + "\"contig\": \"contig"+ str(countContigs) + "\", \n"
							#contig += addline
							#prevEnd=end	
						#else:
						sizeContig += 1
						addline = lines[i].strip() + "\"contig\": \"contig"+ str(countContigs) + "\", \n"
						contig += addline
						#prevEnd = end
		else:
			try:
				if re.match("]",lines[i]) and re.match("}",lines[i+1]) and re.match('{"name',lines[i+2]):
					#print lines[i]
					result.write("]\n},\n")
				if re.match("]",lines[i]) and re.match("},",lines[i+1]) and re.match('{"contig',lines[i+2]):
					result.write("]\n},\n")
			except IndexError:
				print lines[i]
				
result.write(contig)

if sizeContig == 0 or CompleteGenome=='yes':
	sizeContig = 0 
else:
	result.write("]\n}\n")

if CompleteGenome=='yes' and sizeContig == 0:
	CompleteGenome=='yes'
elif lastlinefaa=='yes' and sizeContig == 0:
	result.write("]\n}\n")
elif contigfile == 'yes' and sizeContig == 0:
	result.write("]\n}\n")
result.write("]")
			


inf.close()
result.close()

#os.remove(openwhich)