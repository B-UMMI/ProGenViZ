import re
import sys
import os

array = sys.argv
path=array[1]
Genome=array[2]
PosToBe=array[3]
Genome=str(int(Genome)+1)
PosToBe=str(int(PosToBe)+1)

openInput='uploads/' + path + '/'+ path +'_input.json'
openNewFile='uploads/' + path + '/'+ path +'_inputP.json'

openInputProv='uploads/' + path + '/'+ path +'_inputProv.json'
openNewProv='uploads/' + path + '/'+ path +'_inputProvP.json'

openSequence='uploads/' + path + '/'+ path +'_inputWithSequences.json'
openSequenceTemp='uploads/' + path + '/'+ path +'_inputWithSequencesTemp.json'

openTempFile='uploads/' + path + '/'+ path +'_inputTemp.json'
openTempFileProv='uploads/' + path + '/'+ path +'_inputTempProv.json'

openTempSize='uploads/' + path + '/'+ path +'_inputSize.json'
openTempSizeProv='uploads/' + path + '/'+ path +'_inputSizeProv.json'



fileResult=open(openNewFile, 'w')
os.chmod(openNewFile, 0755)

fileProv=open(openNewProv, 'w')
os.chmod(openNewProv, 0755)

fileSeqTemp=open(openSequenceTemp, 'w')
os.chmod(openSequenceTemp, 0755)

TempFile=open(openTempFileProv, 'w')
os.chmod(openTempFileProv, 0755)

SizeFile=open(openTempSizeProv, 'w')
os.chmod(openTempSizeProv, 0755)

IFile=open(openInput, 'r')
Iprov=open(openInputProv, 'r')
ISeq=open(openSequence, 'r')
ITemp=open(openTempFile, 'r')
ISize=open(openTempSize, 'r')

linesI = IFile.readlines()
linesP = Iprov.readlines()
linesS = ISeq.readlines()
linesT = ITemp.readlines()
linesSize = ISize.readlines()

lastlineI=len(linesI)
lastlineP=len(linesP)
lastlineS=len(linesS)
lastlineT=len(linesT)
lastlineSize=len(linesSize)

GenesToUse=[]
FirstLineChanged="no"
NextLessOne="no"

isThere="no"
for i in range(0,lastlineI):
	try:
		genomeLine=linesI[i].split('"')[7]
		queryName=linesI[i].split('"')[11]
		if genomeLine==Genome:
			#if re.search(PosToBe+"...",linesI[i]):
			newLine=linesI[i].replace(PosToBe+"...",str(Genome)+"...")
			newLine=newLine.replace('"genome": "'+genomeLine+'"','"genome": "'+str(PosToBe)+'"')
			newLine=newLine.replace('"gene": "'+queryName+'"','"gene": "'+str(PosToBe)+"..."+str(queryName.split("...")[1])+'"')
			fileResult.write(newLine)
		elif genomeLine==PosToBe:
			#if re.search(Genome+"...",linesI[i]):
			newLine=linesI[i].replace(Genome+"...",str(PosToBe)+"...")
			newLine=newLine.replace('"genome": "'+genomeLine+'"','"genome": "'+str(Genome)+'"')
			newLine=newLine.replace('"gene": "'+queryName+'"','"gene": "'+str(Genome)+"..."+str(queryName.split("...")[1])+'"')
			fileResult.write(newLine)
		else:
			firstMatch=str(Genome+"...")
			secondMatch=str(PosToBe+"...")
			if firstMatch in linesI[i]:
				newLine=linesI[i].replace(Genome+"...",str(PosToBe)+"...")
				fileResult.write(newLine)
			elif secondMatch in linesI[i]:
				newLine=linesI[i].replace(PosToBe+"...",str(Genome)+"...")
				fileResult.write(newLine)
			else:
				fileResult.write(linesI[i])
	except IndexError:
		fileResult.write(linesI[i])

for i in range(0,lastlineT):
	try:
		genomeLine=linesT[i].split('"')[7]
		queryName=linesT[i].split('"')[11]
		if genomeLine==Genome:
			#if re.search(PosToBe+"...",linesI[i]):
			newLine=linesT[i].replace(PosToBe+"...",str(Genome)+"...")
			newLine=newLine.replace('"genome": "'+genomeLine+'"','"genome": "'+str(PosToBe)+'"')
			newLine=newLine.replace('"gene": "'+queryName+'"','"gene": "'+str(PosToBe)+"..."+str(queryName.split("...")[1])+'"')
			TempFile.write(newLine)
		elif genomeLine==PosToBe:
			#if re.search(Genome+"...",linesI[i]):
			newLine=linesT[i].replace(Genome+"...",str(PosToBe)+"...")
			newLine=newLine.replace('"genome": "'+genomeLine+'"','"genome": "'+str(Genome)+'"')
			newLine=newLine.replace('"gene": "'+queryName+'"','"gene": "'+str(Genome)+"..."+str(queryName.split("...")[1])+'"')
			TempFile.write(newLine)
		else:
			firstMatch=str(Genome+"...")
			secondMatch=str(PosToBe+"...")
			if firstMatch in linesT[i]:
				newLine=linesT[i].replace(Genome+"...",str(PosToBe)+"...")
				TempFile.write(newLine)
			elif secondMatch in linesT[i]:
				newLine=linesT[i].replace(PosToBe+"...",str(Genome)+"...")
				TempFile.write(newLine)
			else:
				TempFile.write(linesT[i])
	except IndexError:
		TempFile.write(linesT[i])

for i in range(0,lastlineSize):
	try:
		genomeLine=linesSize[i].split('"')[7]
		queryName=linesSize[i].split('"')[11]
		if genomeLine==Genome:
			#if re.search(PosToBe+"...",linesI[i]):
			newLine=linesSize[i].replace(PosToBe+"...",str(Genome)+"...")
			newLine=newLine.replace('"genome": "'+genomeLine+'"','"genome": "'+str(PosToBe)+'"')
			newLine=newLine.replace('"gene": "'+queryName+'"','"gene": "'+str(PosToBe)+"..."+str(queryName.split("...")[1])+'"')
			SizeFile.write(newLine)
		elif genomeLine==PosToBe:
			#if re.search(Genome+"...",linesI[i]):
			newLine=linesSize[i].replace(Genome+"...",str(PosToBe)+"...")
			newLine=newLine.replace('"genome": "'+genomeLine+'"','"genome": "'+str(Genome)+'"')
			newLine=newLine.replace('"gene": "'+queryName+'"','"gene": "'+str(Genome)+"..."+str(queryName.split("...")[1])+'"')
			SizeFile.write(newLine)
		else:
			firstMatch=str(Genome+"...")
			secondMatch=str(PosToBe+"...")
			if firstMatch in linesSize[i]:
				newLine=linesSize[i].replace(Genome+"...",str(PosToBe)+"...")
				SizeFile.write(newLine)
			elif secondMatch in linesSize[i]:
				newLine=linesSize[i].replace(PosToBe+"...",str(Genome)+"...")
				SizeFile.write(newLine)
			else:
				SizeFile.write(linesSize[i])
	except IndexError:
		SizeFile.write(linesSize[i])

for i in range(0,lastlineP):
	try:
		genomeLine=linesP[i].split('"')[7]
		queryName=linesP[i].split('"')[11]
		if genomeLine==Genome:
			newLine=linesP[i].replace('"genome": "'+genomeLine+'"','"genome": "'+str(PosToBe)+'"')
			newLine=newLine.replace('"gene": "'+queryName+'"','"gene": "'+str(PosToBe)+"..."+str(queryName.split("...")[1])+'"')
			fileProv.write(newLine)
		elif genomeLine==PosToBe:
			newLine=linesP[i].replace('"genome": "'+genomeLine+'"','"genome": "'+str(Genome)+'"')
			newLine=newLine.replace('"gene": "'+queryName+'"','"gene": "'+str(Genome)+"..."+str(queryName.split("...")[1])+'"')
			fileProv.write(newLine)
		else:
			fileProv.write(linesP[i])
	except IndexError:
		fileProv.write(linesP[i])

for i in range(0,lastlineS):
	try:
		genomeLine=linesS[i].split('"')[7]
		if genomeLine==Genome:
			newLine=linesS[i].replace('"genome": "'+genomeLine+'"','"genome": "'+str(PosToBe)+'"')
			fileSeqTemp.write(newLine)
		elif genomeLine==PosToBe:
			newLine=linesS[i].replace('"genome": "'+genomeLine+'"','"genome": "'+str(Genome)+'"')
			fileSeqTemp.write(newLine)
		else:
			fileSeqTemp.write(linesS[i])
	except IndexError:
		fileSeqTemp.write(linesS[i])


		
fileResult.close()
fileProv.close()
fileSeqTemp.close()
TempFile.close()
SizeFile.close()

IFile.close()
Iprov.close()
ISeq.close()
ITemp.close()
ISize.close()

os.remove(openInput)
os.rename(openNewFile,openInput)

os.remove(openInputProv)
os.rename(openNewProv,openInputProv)

os.remove(openSequence)
os.rename(openSequenceTemp,openSequence)

os.remove(openTempFile)
os.rename(openTempFileProv,openTempFile)

os.remove(openTempSize)
os.rename(openTempSizeProv,openTempSize)