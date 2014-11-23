import re
import sys
import os

array = sys.argv
path=array[1]
querygene=array[2]
genomequery=querygene.split("...")
countNumGenomes=0
imp = ""
imports=imp
openwhich='uploads/' + path + '/'+ path +'_input.json'
inf=open(openwhich, 'r')
openwhere='uploads/' + path + '/'+ path +'_inputProvis.json'
newfile = open(openwhere,'w')
os.chmod(openwhere, 0755)
lines = inf.readlines()
lastline=len(lines)
newfile.write("[\n")
count=0
prevSourceBegin= ""
prevName=""
for i in range(1, lastline):
	if re.match("{\"name\":",lines[i]):
		isThere="false"
		count+=1
		imports=imp
		line = lines[i]
		linha = line.split('\"')
		gene = linha[11]
		begin = linha[19]
		name = linha[3]
		if re.search(querygene,gene) and (prevSourceBegin != begin or re.search(name,gene)) and prevName!=name:
			if re.search(name,gene):
				prevName=name
			line1=line.split('"imports": [')[1].split(']}')[0]
			line=line.replace(line1,'')
			newfile.write(line)

		else:
			newfile.write(line)
		prevSourceBegin=begin
		
	else:
		newfile.write(lines[i])

inf.close()
newfile.close()

os.remove(openwhich)
os.rename(openwhere, openwhich)