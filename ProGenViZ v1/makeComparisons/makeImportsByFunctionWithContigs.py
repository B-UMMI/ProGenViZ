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
openwhich='uploads/' + path + '/'+ path +'_inputSize.json'
inf=open(openwhich, 'r')
openwhere='uploads/' + path + '/'+ path +'_input.json'
newfile = open(openwhere,'w')
os.chmod(openwhere, 0777)
lines = inf.readlines()
lastline=len(lines)
newfile.write("[\n")
count=0
prevSourceBegin= ""
prevTargetBegin= ""
firstGenomeLine= ""
prevLastlineGenome=""
lastlineGenome="."
for i in range(1, lastline):
	if re.match("{\"name\":",lines[i]):
		nextline=i+1
		isThere="false"
		count+=1
		imports=imp
		line = lines[i]
		linha = line.split('\"')
		gene = linha[11]
		funcao = linha[15]
		begin = linha[19]
		for y in search:
			if re.search(y,funcao):
				isThere='true'
			if re.search(y,gene):
				isThere='true'
		lastlineGenome = linha[len(linha)-6]
		if i==3:
			firstGenomeLine=linha[len(linha)-6]
		if prevLastlineGenome!=lastlineGenome:
			prevLastlineGenome=lastlineGenome
			countNumGenomes+=1
		if (begin == prevSourceBegin and begin != '') or isThere != 'true':
			if re.match("]",lines[nextline]):
				imports = imports.rstrip("\,")
				imports = imports + "]}\n"

			else:
				imports = imports.rstrip("\,")
				imports = imports + "]},\n"

			newfile.write(line.strip() + imports)
		else:
			if int(numGenomes) == countNumGenomes and int(numGenomes)!=2:
				for j in range(1,int(firstGenomeLine)):
					if re.match("{\"name\":",lines[j]):
						line2 = lines[j]
						linha2 = line2.split('\"')
						funcao2 = linha2[15]
						beginTarget = linha2[19]
						if linha[7] == linha2[7]:		#Apenas para fazer comparacoes across genomes
							imports = imports
						if (int(linha[7]) + 1) < int(linha2[7]):
							break
						else:
							if funcao == funcao2 and prevTargetBegin != beginTarget or funcao == funcao2 and begin == '':
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
					if re.match("{\"name\":",lines[j]):
						line2 = lines[j]
						linha2 = line2.split('\"')
						funcao2 = linha2[15]
						beginTarget = linha2[19]
						if linha[7] == linha2[7]:		#Apenas para fazer comparacoes across genomes
							imports = imports
						if (int(linha[7]) + 1) < int(linha2[7]):
							break
						else:
							if funcao == funcao2 and prevTargetBegin != beginTarget or funcao == funcao2 and begin == '':
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