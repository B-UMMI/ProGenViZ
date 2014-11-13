import re
import sys
import os

array = sys.argv
path=array[1]
PartToChange=int(array[2])
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
print lastline
newfile.write("[\n")
count=0
prevSourceBegin= ""
prevTargetBegin= ""
for i in range(1, lastline):
	try:
		currentGenome = lines[i].split('"')[7]
		count+=1
	except IndexError:
		currentGenome=PartToChange
		count+=1
		if re.match("}",lines[i]):
			if count != lastline-2 and not re.match("},",lines[i]):
				newfile.write(lines[i].strip() + ",\n")
			else:
				newfile.write(lines[i].strip() + "\n")
		else:
			newfile.write(lines[i])
	if int(currentGenome)>PartToChange:
		if re.match("{\"name\":",lines[i]):
			imports=imp
			line = lines[i]
			if re.match("]",lines[i+1]):
				imports = imports.rstrip("\,")
				imports = imports + "]}\n"

			else:
				imports = imports.rstrip("\,")
				imports = imports + "]},\n"

			newfile.write(line.strip() + imports)
	else:
		if re.match("{\"name\":",lines[i]):
			newfile.write(lines[i])

			
		

print count
inf.close()
newfile.close()