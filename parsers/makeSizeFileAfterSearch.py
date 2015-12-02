import re
import sys
import os

array = sys.argv
path=array[1]
openwhich='uploads/' + path + '/'+ path +'_input.json'
inf=open(openwhich, 'r')
openwhere='uploads/' + path + '/'+ path +'_inputSize.json'
newfile = open(openwhere,'w')
os.chmod(openwhere, 0755)
lines = inf.readlines()
lastline=len(lines)
count=0
for i in range(0, lastline):
	if "\"imports\": " in lines[i]:
		lineP = lines[i].split("}")
		lineP1 = lineP[0].split(',"imports": ')
		#print lineP1
		imports = lineP1[1]
		line = lines[i].replace('"imports": ' + imports + '}',"")
		line=line.strip(',\n')
		newfile.write(line+",\n")
	else:
		if "}," in lines[i]:
			line=lines[i].replace("},","}")
			newfile.write(line)
		else:
			newfile.write(lines[i])

newfile.close()
inf.close()

#os.remove(openwhich)
#os.rename(openwhere,openwhich)