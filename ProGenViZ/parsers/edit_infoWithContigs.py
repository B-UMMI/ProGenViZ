import re
import os
import sys

array = sys.argv
path=array[1]
path1=array[2].split("/")
fileType=path1[len(path1)-1].split(".")[1]

geneToChange=array[3]
if geneToChange!='null':
	genome=geneToChange.split("...")[0]
ToRemove=geneToChange.split("_")
toRemove='_'+ToRemove[len(ToRemove)-1]
geneToChange=geneToChange.replace(toRemove,"")
newGene=array[4]
if newGene!='null':
	newGene=newGene.replace("---"," ")
	newGene=genome+'...'+newGene
else:
	newGene=geneToChange

productToChange=array[5]
productToChange=productToChange.replace("---"," ")
newProduct=array[6]
newProduct=newProduct.replace("---"," ")
if newProduct=='null':
	newProduct=productToChange

geneBegin=array[7]
openwhich='uploads/' + path + '/'+ path +'_input.json'
posIni=open(openwhich,'r')
hipo=""
openwhere='uploads/' + path + '/'+ path +'_inputP.json'
result=open(openwhere,"w")
os.chmod(openwhere, 0777)
prevBegin=''
for line in posIni:
	linha=line.split("\"")
	first_last=linha[0].strip()
	if "{\"name\":" in line:
		if fileType=='faa':
			if geneToChange in str(linha[11]) and productToChange in line:
				line=line.replace(productToChange,newProduct)
			if geneToChange in line:
				line=line.replace(geneToChange,str(newGene))
			if "\"imports\":" in line:
				imports=line.split('\"imports\":')[1]
				if geneToChange in imports:
					line=line.replace(geneToChange,str(newGene))
			result.write(line)
		else:
			if geneToChange in str(linha[11]) and productToChange in line and geneBegin in line:
				line=line.replace(productToChange,newProduct)
			if geneToChange in line and geneBegin in line:
				line=line.replace(geneToChange,str(newGene))
			if "\"imports\":" in line:
				imports=line.split('\"imports\":')[1]
				if geneToChange in imports:
					line=line.replace(geneToChange,str(newGene))
			result.write(line)
	else:
		result.write(line)

posIni.close()
result.close()

os.remove(openwhich)
os.rename(openwhere,openwhich)

openwhich2='uploads/' + path + '/'+ path +'_inputSize.json'
posIni=open(openwhich2,'r')
hipo=""
openwhere2='uploads/' + path + '/'+ path +'_inputSizeP.json'
result=open(openwhere2,"w")
os.chmod(openwhere2, 0777)
prevBegin=''
for line in posIni:
	linha=line.split("\"")
	first_last=linha[0].strip()
	if "{\"name\":" in line:
		if fileType=='faa':
			if geneToChange in str(linha[11]) and productToChange in line:
				line=line.replace(productToChange,newProduct)
			if geneToChange in line:
				line=line.replace(geneToChange,str(newGene))
			result.write(line)
		else:
			if geneToChange in str(linha[11]) and productToChange in line and geneBegin in line:
				line=line.replace(productToChange,newProduct)
			if geneToChange in line and geneBegin in line:
				line=line.replace(geneToChange,str(newGene))
			result.write(line)
	else:
		result.write(line)

posIni.close()
result.close()

os.remove(openwhich2)
os.rename(openwhere2,openwhich2)

openwhich3='uploads/' + path + '/'+ path +'_inputProv.json'
posIni=open(openwhich3,'r')
hipo=""
openwhere3='uploads/' + path + '/'+ path +'_inputProvP.json'
result=open(openwhere3,"w")
os.chmod(openwhere3, 0777)
prevBegin=''
for line in posIni:
	linha=line.split("\"")
	first_last=linha[0].strip()
	if "{\"name\":" in line:
		if fileType=='faa':
			if geneToChange in str(linha[11]) and productToChange in line:
				line=line.replace(productToChange,newProduct)
			if geneToChange in line:
				line=line.replace(geneToChange,str(newGene))
			result.write(line)
		else:
			if geneToChange in str(linha[11]) and productToChange in line and geneBegin in line:
				line=line.replace(productToChange,newProduct)
			if geneToChange in line and geneBegin in line:
				line=line.replace(geneToChange,str(newGene))
			result.write(line)
	else:
		result.write(line)

posIni.close()
result.close()

os.remove(openwhich3)
os.rename(openwhere3,openwhich3)