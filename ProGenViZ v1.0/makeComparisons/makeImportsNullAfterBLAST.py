import re
import sys
import os

array = sys.argv
path=array[1]
vetor=[]
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
prevTargetBegin= ""
for i in range(1, lastline):
	if re.match("}",lines[i]):
		if i != lastline-2 and not re.match("},",lines[i]):
			newfile.write(lines[i].strip() + ",\n")
		else:
			newfile.write(lines[i].strip() + "\n")
	elif re.match("{\"name\":",lines[i]):
		imports=imp
		line = lines[i].split('"imports":')[0]
		if re.match("]",lines[i+1]):
			imports = imports.rstrip("\,")
			imports = imports + "]}\n"

		else:
			imports = imports.rstrip("\,")
			imports = imports + "]},\n"

		newfile.write(line.strip() + imports)
	else:
		newfile.write(lines[i])

inf.close()
newfile.close()