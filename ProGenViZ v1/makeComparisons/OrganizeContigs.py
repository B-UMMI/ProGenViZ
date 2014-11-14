import re
import sys
import os
from Bio import SeqIO

array = sys.argv
path=array[1]
openwhich='uploads/' + path + '/'+ path +'_inputProv.json'
openCoord=array[2]
openwhere='uploads/' + path + '/'+ path +'_inputProv_contigs.json'
template=open(openwhich, 'r')
alignment=open(openCoord, 'r')
posIni=open(openwhere,'w')
os.chmod(openwhere, 0777)
posIni.write("[\n")
array = sys.argv
array.pop(0)
numContigFiles=0
queryGenome=""
Done='no'
prevAlign=""
linesT = template.readlines()
lastlineT=len(linesT)
linesA = alignment.readlines()
lastlineA=len(linesA)
AlreadyThere=[]
IsThere='yes'
linha = linesA[5].split('\t')
contig=linha[len(linha)-1].strip()
contig=contig.replace("gn|","")
firstContig=contig
for k in range(1, lastlineT-1):
	if contig in linesT[k]:
		queryGenome=linesT[k].split('"')[7]
		break

for i in range(1, lastlineT-1):
	if linesT[i].split('"')[7]!=queryGenome:
		posIni.write(linesT[i])
	else:
		print Done
		if Done=='no':
			for j in range(5, lastlineA-1):
				linha = linesA[j].split('\t')
				contig=linha[len(linha)-1].strip()
				contigRef=linha[len(linha)-2].strip()
				contig=contig.replace("gn|","")
				contig=contig.split("[")[0]
				if re.search('Undefined',contigRef):
					contigRef=contigRef
				else:
					for l in range(i,lastlineT-1):
						#print contig
						if contig in linesT[l]:
							if len(AlreadyThere)==0:
								IsThere='no'
							for z in AlreadyThere:
								#print contig
								if contig in z:
									IsThere='yes'
							if IsThere=='yes':
								prevAlign=contig
								IsThere='no'
							else:
								posIni.write(linesT[l])
								#print contig
								AlreadyThere.append(contig)
								IsThere='no'
								break
			Done='yes'
			

#posIni.write("]")
template.close()
posIni.close()
alignment.close()

os.remove(openwhich)
os.rename(openwhere,openwhich)