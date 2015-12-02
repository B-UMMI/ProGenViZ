import re
import sys
import os

array = sys.argv
path=array[1]
PartToChange=array[2]
openwhich='uploads/' + path + '/'+ path +'_input.json'
inf=open(openwhich, 'r')
openwhere='uploads/' + path + '/'+ path +'_inputP.json'
newfile = open(openwhere,'w')
os.chmod(openwhere, 0755)
openProv='uploads/' + path + '/'+ path +'_inputProv.json'
openProvTemp='uploads/' + path + '/'+ path +'_inputProvTemp.json'
openSequence='uploads/' + path + '/'+ path +'_inputWithSequences.json'
openSequenceTemp='uploads/' + path + '/'+ path +'_inputWithSequencesTemp.json'
openIP=open(openProv,'r')
openIPT=open(openProvTemp,'w')
openS=open(openSequence,'r')
openST=open(openSequenceTemp,'w')
os.chmod(openProvTemp, 0755)
os.chmod(openSequenceTemp, 0755)

linesS=openS.readlines()
lastlineS=len(linesS)

for j in range(0,lastlineS):
	try:
		genome=linesS[j].split('"')[7]
	except IndexError:
		genome=""
	if genome==PartToChange:
		genome=genome
	elif int(genome)>int(PartToChange):
		newNumber=int(genome)-1
		line=linesS[j].replace('"genome": "'+genome+'"','"genome": "'+str(newNumber)+'"')
		line=line.replace('"gene": "'+genome+'...','"gene": "'+str(newNumber)+'...')
		openST.write(line)
	else:
		openST.write(linesS[j])

lines = inf.readlines()
lastline=len(lines)
linesIP = openIP.readlines()
lastlineIP=len(linesIP)
newfile.write("[\n")
error='f'
currentGenome=''
for i in range(1, lastline):
	try:
		currentGenome = lines[i].split('"')[7]
		error='f'
	except IndexError:
		try:
			currentGenome = lines[i+1].split('"')[7]
			if currentGenome==PartToChange:
				PartToChange=PartToChange
			else:
				newfile.write(lines[i])
		except IndexError:
			try:
				currentGenome = lines[i-1].split('"')[7]
				if currentGenome==PartToChange:
					PartToChange=PartToChange
				else:
					newfile.write(lines[i])
			except IndexError:
				try:
					currentGenome = lines[i-2].split('"')[7]
					if currentGenome==PartToChange:
						PartToChange=PartToChange
					else:
						newfile.write(lines[i])
				except IndexError:
					newfile.write(lines[i])
		error='t'
	if currentGenome==PartToChange:
		PartToChange=PartToChange
	else:
		if error=='f':
			line=lines[i]
			if int(currentGenome)>int(PartToChange):
				newNumber=int(currentGenome)-1
				line=line.replace('"genome": "'+currentGenome+'"','"genome": "'+str(newNumber)+'"')
				line=line.replace('"gene": "'+currentGenome+'...','"gene": "'+str(newNumber)+'...')
			imports = lines[i].split('"imports": [')[1]
			imports = imports.split(']}')[0]
			imports = imports.split(',')
			for imported in imports:
				if imported!="":
					imp=imported.split('"')[1]
					impGenome=imp.split("...")[0]
					if int(impGenome)>int(PartToChange):
						newN=str(int(impGenome)-1)
						newimported=imported.replace(impGenome+'...',newN+'...')
						line=line.replace(imported,newimported)
					elif int(impGenome)==int(PartToChange):
						line=line.replace(imported+",","")
						line=line.replace(imported,"")
						line=line.strip(',')
						#print line
			if i==lastline-2:
				#print line
				line=line.replace(']},',']}')
			newfile.write(line)

inf.close()
newfile.close()

inf=open(openwhere, 'r')
newfile = open(openwhich,'w')
os.chmod(openwhich, 0755)
lines = inf.readlines()
lastline=len(lines)
for i in range(0, lastline):
	if i==lastline-2:
		#print lines[i]
		line=lines[i].replace('},','}')
		newfile.write(line)
	else:
		newfile.write(lines[i])
inf.close()
newfile.close()
os.remove(openwhere)
#os.rename(openwhere,openwhich)

for i in range(0, lastlineIP):
	try:
		currentGenome = linesIP[i].split('"')[7]
		if currentGenome==PartToChange:
			PartToChange=PartToChange
		else:
			if int(currentGenome)>int(PartToChange):
				newNumber=int(currentGenome)-1
				line=linesIP[i].replace('"genome": "'+currentGenome+'"','"genome": "'+str(newNumber)+'"')
				line=line.replace('"gene": "'+currentGenome+'...','"gene": "'+str(newNumber)+'...')
				openIPT.write(line)
			else:
				openIPT.write(linesIP[i])
	except IndexError:
		openIPT.write(linesIP[i])

openIP.close()
openIPT.close()
os.remove(openProv)
os.rename(openProvTemp,openProv)
os.remove(openSequence)
os.rename(openSequenceTemp,openSequence)
