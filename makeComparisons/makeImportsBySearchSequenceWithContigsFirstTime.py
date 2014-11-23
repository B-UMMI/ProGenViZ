import re
import sys
import os

array = sys.argv
path=array[1]
querygene=array[2]
genomequery=querygene.split("...")
results=array[3]
results=results.split('---')
results=list(set(results))
countNumGenomes=0
imp = "\"imports\": ["
imports=imp
openwhich='uploads/' + path + '/'+ path +'_inputSize.json'
inf=open(openwhich, 'r')
openwhere='uploads/' + path + '/'+ path +'_input.json'
newfile = open(openwhere,'w')
os.chmod(openwhere, 0755)
lines = inf.readlines()
lastline=len(lines)
newfile.write("[\n")
count=0
prevSourceBegin= ""
prevName=""
for i in range(1, lastline):
	if "{\"name\":" in lines[i]:
		nextline=i+1
		isThere="false"
		count+=1
		imports=imp
		line = lines[i]
		linha = line.split('\"')
		gene = linha[11]
		begin = linha[19]
		name = linha[3]
		if querygene==gene and (prevSourceBegin != begin or name in gene) and prevName!=name:
			if name in gene:
				prevName=name
			for i in results:
				imports = imports + "\"" + i + "\","
		else:
			imports=imports

		if "]" in lines[nextline]:
			imports = imports.rstrip("\,")
			imports = imports + "]}\n"

		else:
			imports = imports.rstrip("\,")
			imports = imports + "]},\n"

		newfile.write(line.strip() + imports)
		prevSourceBegin = begin
		
	else:
		count+=1
		if "}" in lines[i]:
			if count != lastline-2:
				newfile.write(lines[i].strip() + ",\n")
			else:
				newfile.write(lines[i].strip() + "\n")
		else:
			newfile.write(lines[i])

inf.close()
newfile.close()