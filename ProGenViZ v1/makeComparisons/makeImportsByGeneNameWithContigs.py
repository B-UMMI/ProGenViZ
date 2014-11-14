import re
import sys
import os

array = sys.argv
path=array[1]
search=array[2]
search=search.replace("---"," ")
numGenomes=array[3]
countNumGenomes=0
search=search.split('.')
vetor=[]
imp = "\"imports\": ["
imports=imp
openwhich='uploads/' + path + '/'+ path +'_inputSize.json'
inf=open(openwhich, 'r')
openwhere='uploads/' + path + '/'+ path +'_input.json'
newfile = open(openwhere,'w')
os.chmod(openwhere, 0777)
lines = inf.readlines()
lastline=len(lines)
count=0
prevSourceBegin= ""
prevTargetBegin= ""
firstGenomeLine= ""
prevLastlineGenome=""
lastlineGenome="."
newfile.write("[\n")
for i in range(1, lastline):
	if "{\"name\":" in lines[i]:
		nextline=i+1
		isThere="false"
		count+=1
		imports=imp
		line = lines[i]
		linha = line.split('\"')
		gene = linha[11].split("...")[1]
		funcao = linha[15]
		begin = linha[19]
		for y in search:
			if y in gene:
				isThere='true'
			if y in funcao:
				isThere='true'
		lastlineGenome = linha[51]
		if i==3:
			firstGenomeLine=linha[51]
		if prevLastlineGenome!=lastlineGenome:
			prevLastlineGenome=lastlineGenome
			countNumGenomes+=1
		if (begin == prevSourceBegin and begin != '') or isThere !='true':
			if re.match("]",lines[nextline]):
				imports = imports.rstrip("\,")
				imports = imports + "]}\n"

			else:
				imports = imports.rstrip("\,")
				imports = imports + "]},\n"
			#print line.strip() + imports
			newfile.write(line.strip() + imports)
		else:
			if int(numGenomes) == countNumGenomes and int(numGenomes)!=2:
				for j in range(1,int(firstGenomeLine)):
					if re.match("{\"name\":",lines[j]):
						line2 = lines[j]
						linha2 = line2.split('\"')
						gene2 = linha2[11].split("...")[1]
						beginTarget = linha2[19]
						if linha[7] == linha2[7]:
							imports = imports
						if (int(linha[7]) + 1) < int(linha2[7]):
							break
						else:
							ToRemove=gene.split("_")
							toRemove='_'+ToRemove[len(ToRemove)-1]
							gene1=gene.replace(toRemove,"")
							ToRemove=gene2.split("_")
							toRemove='_'+ToRemove[len(ToRemove)-1]
							gene2=gene2.replace(toRemove,"")
							if (gene1 == gene2 and prevTargetBegin != beginTarget) or (gene1 == gene2 and begin == ''):
								imports = imports + "\"" + linha2[11] + "\","
						prevTargetBegin = beginTarget
				
				if re.match("]",lines[nextline]):
					imports = imports.rstrip("\,")
					imports = imports + "]}\n"

				else:
					imports = imports.rstrip("\,")
					imports = imports + "]},\n"

				newfile.write(line.strip() + imports)
			else:
				for j in range(int(lastlineGenome),lastline):
					#print lastlineGenome
					if re.match("{\"name\":",lines[j]):
						line2 = lines[j]
						linha2 = line2.split('\"')
						gene2 = linha2[11].split("...")[1]
						beginTarget = linha2[19]
						if linha[7] == linha2[7]:
							imports = imports
						if (int(linha[7]) + 1) < int(linha2[7]):
							break
						else:
							ToRemove1=gene.split("_")
							ToRemove2=gene2.split("_")
							toRemove1='_'+ToRemove1[len(ToRemove1)-1]
							toRemove2='_'+ToRemove2[len(ToRemove2)-1]
							gene1=gene.replace(toRemove1,"")
							gene2=gene2.replace(toRemove2,"")
							#print len(ToRemove1)
							#print len(ToRemove2)
							#print gene1
							#print gene2
							if (gene1 == gene2 and prevTargetBegin != beginTarget) or (gene1 == gene2 and begin == ''):
								imports = imports + "\"" + linha2[11] + "\","
						prevTargetBegin = beginTarget
				
				if re.match("]",lines[nextline]):
					imports = imports.rstrip("\,")
					imports = imports + "]}\n"

				else:
					imports = imports.rstrip("\,")
					imports = imports + "]},\n"

				newfile.write(line.strip() + imports)
		prevSourceBegin = begin
	else:
		count+=1
		if re.match("}",lines[i]):
			if count != lastline-2:
				newfile.write(lines[i].strip() + ",\n")
			else:
				newfile.write(lines[i].strip() + "\n")
		else:
			newfile.write(lines[i])

inf.close()
newfile.close()