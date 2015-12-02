import re
import sys
import os
from Bio import SeqIO
import shutil

array = sys.argv
path1=array[1].split("/")
path=path1[len(path1)-3]
nameFile=path1[len(path1)-1].split(".")[0]
openTemp='uploads/' + path + '/'+ path +'_inputTemp.json'
openInput='uploads/' + path + '/'+ path +'_input.json'
openSequenceTemp='uploads/' + path + '/'+ path +'_inputWithSequencesTemp.json'
openSequence='uploads/' + path + '/'+ path +'_inputWithSequences.json'
openProvF='uploads/' + path + '/'+ path +'_inputProv.json'
backupProv='uploads/' + path + '/'+ path +'_inputProvBackup.json'
backupSeq='uploads/' + path + '/'+ path +'_inputWithSequencesBackup.json'
openProvTemp='uploads/' + path + '/'+ path +'_inputProvTemp.json'

shutil.copyfile(openProvF, backupProv)
shutil.copyfile(openSequence, backupSeq)

openFileInput=open(openInput,'r')
openFileSequence=open(openSequence,'r')
openProv=open(openProvF,'r')
posIni=open(openTemp,'w')
os.chmod(openTemp, 0755)
array = sys.argv
array.pop(0)
numContigFiles=0
gffInFasta=array[len(array)-2]

fileWithSequence=open(openSequenceTemp,'w')
os.chmod(openSequenceTemp, 0755)

fileProvTemp=open(openProvTemp,'w')
os.chmod(openProvTemp, 0755)

comp=len(array)
count=int(array[comp-3])
counts=0
lastline=0
gene=""
product=""
CountContigFasta=0
countContigs=0
countlines=0

stringOfFiles=""

IsContig=array[len(array)-1]


linesProv=openProv.readlines()
lengthProv=len(linesProv)
for i in range(0,lengthProv-1):
	fileProvTemp.write(linesProv[i])
	if i==(lengthProv-2):
		gene=linesProv[i].split('"')[11].split('_')
		countlines=int(gene[len(gene)-1])

try:

	if gffInFasta=='yes': #fasta+gff parser
		for files in array:
			if '.gff' in files:
				gff=open(files,'r')
			if '.fasta' in files or '.fna' in files:
				fasta=open(files,'r')

		sequence=""
		linesFasta = fasta.readlines()
		lengthLinesF=len(linesFasta)

		for j in range(0,lengthLinesF):
			if '>' in linesFasta[j]:
				gene=gene
			else:
				sequence=sequence+linesFasta[j]
		fasta.close()

		lengthGenome=len(sequence)
		countContigs=0
		countContigs+=1
		pathFile=files.split("/")
		countNCLines=0
		count+=1
		lines = gff.readlines()
		lengthLines=len(lines)
		linesInput = openFileInput.readlines()
		linesSeq = openFileSequence.readlines()
		lengthlinesInput=len(linesInput)
		lengthSeq=len(linesSeq)
		prevStart=0
		countUndefined=0
		#fileJustSequence=open(openJustSequence,'w')
		#os.chmod(openJustSequence, 0755)
		#fileJustSequence.write(str(sequence))
		for i in range(0,lengthlinesInput-1):
			posIni.write(linesInput[i])
		for i in range(0,lengthSeq):
			fileWithSequence.write(linesSeq[i])
		for i in range(0,lengthLines):
			if count == comp:
				lastline+=1
			if '#' in lines[i]:
				count=count
			else:
				columns=lines[i].split("\t")
				prevLineInfo=lines[i-1].split("\t")[8]
				if columns[2]=="CDS":
					name=columns[0].strip()
					begingff=columns[3].strip()
					endgff=columns[4].strip()
					strand=columns[6].strip()
					info=columns[8]
					info=info.split(";")
					countlines+=1
					if int(prevStart) < int(begingff):
						countUndefined+=1
						Nsequence=sequence[int(prevStart):int(endgff)]
						posIni.write("{\"name\": " + "\"" + name + "\", \"genome\": \"" + str(count) + "\", \"gene\": \"" + str(count) + "...Undefined_"+str(countUndefined)+"\", \"product\": \"Undefined\",\"begin\": " + "\"" + str(prevStart) + "\"" + ",\"end\": " + "\"" + str(begingff) + "\"" + ",\"contig\": \""+str(countContigs)+"\",\"strand\": " + "\""+strand+"\"" + ",\"protein_id\": " + "\"-\"" + ",\"fileType\": " + "\".gbk\",\"genomeSize\": \"" + str(lengthGenome) + "\",\"reference\": \"" + "Undefined_"+str(countUndefined)+"\",\n")
						fileProvTemp.write("{\"name\": " + "\"" + name + "\", \"genome\": \"" + str(count) + "\", \"gene\": \"" + str(count) + "...Undefined_"+str(countUndefined)+"\", \"product\": \"Undefined\",\"begin\": " + "\"" + str(prevStart) + "\"" + ",\"end\": " + "\"" + str(begingff) + "\"" + ",\"contig\": \""+str(countContigs)+"\",\"strand\": " + "\""+strand+"\"" + ",\"protein_id\": " + "\"-\"" + ",\"fileType\": " + "\".gbk\",\"genomeSize\": \"" + str(lengthGenome) + "\",\"reference\": \"" + "Undefined_"+str(countUndefined)+"\",\n")
						fileWithSequence.write("{\"gene\": \"" + "Undefined_"+str(countUndefined)+"\", \"genome\": \"" + str(count) + "\",\"sequence\": " + "\"" + str(Nsequence) + "\"}\n")
						prevStart=endgff
					for j in info:
						if "Parent=" in j:
							parent="ID="+j.split("=")[1]
							if parent in prevLineInfo:
								infoCol=prevLineInfo.split(";")
								for k in infoCol:
									if "Name=" in k:
										gene=k.split("=")[1].strip()
									if "Dbxref=" in k:
										geneRef=k.split("=")[1].split(":")[1].strip()
						elif "Name=" in j:
							gene=j.split("=")[1].strip()
						elif "Dbxref=" in j:
							geneRef=j.split(",")[0].split("=")[1].strip()
						if "product=" in j:
							product=j.split("=")[1].strip()
					seqToUse=sequence[int(begingff):int(endgff)]
					fileWithSequence.write("{\"gene\": \"" + "gi|" + gene + "|ref|" + gene +'_'+ str(countlines) + "|" + product + "[" + name.strip() + "]"+ "\", \"genome\": \"" + str(count) + "\",\"sequence\": " + "\"" + str(seqToUse) + "\"}\n")
					posIni.write("{\"name\": \""+ name.strip() + "\", \"genome\": \"" + str(count) + "\", \"gene\": \"" + str(count) + "..." + gene +'_'+str(countlines)+ "\", \"product\": \"" + product + "\",\"begin\": " + "\"" + begingff + "\"" + ",\"end\": " + "\"" + endgff + "\"" + ",\"contig\": \""+str(countContigs)+"\",\"strand\": " + "\"" +strand+ "\"" + ",\"protein_id\": " + "\"" + "\"" + ",\"fileType\": " + "\".gff\",\"genomeSize\": \"" + str(lengthGenome) + "\",\"reference\": " + "\"" + "gi|" + gene + "|ref|" + gene +'_'+str(countlines)+ "|" + product + "[" + name.strip() + "]"+ "\",\n")
					fileProvTemp.write("{\"name\": \""+ name.strip() + "\", \"genome\": \"" + str(count) + "\", \"gene\": \"" + str(count) + "..." + gene +'_'+str(countlines)+ "\", \"product\": \"" + product + "\",\"begin\": " + "\"" + begingff + "\"" + ",\"end\": " + "\"" + endgff + "\"" + ",\"contig\": \""+str(countContigs)+"\",\"strand\": " + "\"" +strand+ "\"" + ",\"protein_id\": " + "\"" + "\"" + ",\"fileType\": " + "\".gff\",\"genomeSize\": \"" + str(lengthGenome) + "\",\"reference\": " + "\"" + "gi|" + gene + "|ref|" + gene +'_'+str(countlines)+ "|" + product + "[" + name.strip() + "]"+ "\",\n")
		
		gff.close()
		#fileJustSequence.close()

	else:
		for files in array:

			if '.gff' in files:  # gff file parse
				countContigs=0
				countContigs+=1
				pathFile=files.split("/")
				countNCLines=0
				filename=pathFile[len(pathFile)-1].split(".")
				filemodified='uploads/'+path+'/input_files/'+filename[0]+'_mod.'+filename[1]
				if os.path.isfile(filemodified):
					gff=open(filemodified,'r')
				else:
					gff=open(files,'r')
				count+=1
				linesInput = openFileInput.readlines()
				linesSeq = openFileSequence.readlines()
				lengthlinesInput=len(linesInput)
				lengthSeq=len(linesSeq)
				for i in range(0,lengthlinesInput-1):
					posIni.write(linesInput[i])
				for i in range(0,lengthSeq):
					fileWithSequence.write(linesSeq[i])
				lines = gff.readlines()
				lengthLines=len(lines)
				for i in range(0,lengthLines):
					if count == comp:
						lastline+=1
					if '#' in lines[i]:
						count=count
					else:
						columns=lines[i].split("\t")
						if columns[2]=="CDS":
							prevLineInfo=lines[i-1].split("\t")[8]
							name=columns[0].strip()
							begingff=columns[3].strip()
							endgff=columns[4].strip()
							strand=columns[6].strip()
							info=columns[8]
							info=info.split(";")
							for j in info:
								if "Parent=" in j:
									parent="ID="+j.split("=")[1]
									if parent in prevLineInfo:
										infoCol=prevLineInfo.split(";")
										for k in infoCol:
											if "Name=" in k:
												gene=k.split("=")[1].strip()
											if "Dbxref=" in k:
												geneRef=k.split("=")[1].split(":")[1].strip()
								elif "Name=" in j:
									gene=j.split("=")[1].strip()
								elif "Dbxref=" in j:
									geneRef=j.split(",")[0].split("=")[1].strip()
								if "product=" in j:
									product=j.split("=")[1].strip()
							countlines+=1
							posIni.write("{\"name\": \""+ name.strip() + "\", \"genome\": \"" + str(count) + "\", \"gene\": \"" + str(count) + "..." + gene +'_'+str(countlines)+ "\", \"product\": \"" + product + "\",\"begin\": " + "\"" + begingff + "\"" + ",\"end\": " + "\"" + endgff + "\"" + ",\"contig\": \""+str(countContigs)+"\",\"strand\": " + "\"" +strand+ "\"" + ",\"protein_id\": " + "\"" + "\"" + ",\"fileType\": " + "\".gff\",\"genomeSize\": \"-\",\"reference\": " + "\"" + "gi|" + gene + "|ref|" + gene +'_'+str(countlines)+ "|" + product + "[" + name.strip() + "]"+ "\",\n")
							fileProvTemp.write("{\"name\": \""+ name.strip() + "\", \"genome\": \"" + str(count) + "\", \"gene\": \"" + str(count) + "..." + gene +'_'+str(countlines)+ "\", \"product\": \"" + product + "\",\"begin\": " + "\"" + begingff + "\"" + ",\"end\": " + "\"" + endgff + "\"" + ",\"contig\": \""+str(countContigs)+"\",\"strand\": " + "\"" +strand+ "\"" + ",\"protein_id\": " + "\"" + "\"" + ",\"fileType\": " + "\".gff\",\"genomeSize\": \"-\",\"reference\": " + "\"" + "gi|" + gene + "|ref|" + gene +'_'+str(countlines)+ "|" + product + "[" + name.strip() + "]"+ "\",\n")							
								
				gff.close()
			

			if '.ptt' in files: #parse de ficheiros .ptt
				pathFile=files.split("/")
				filename=pathFile[len(pathFile)-1].split(".")
				filemodified='uploads/'+path+'/input_files/'+filename[0]+'_mod.'+filename[1]
				if os.path.isfile(filemodified):
					ptt=open(filemodified,'r')
				else:
					ptt=open(files,'r')
				count+=1
				countsPtt=0
				linesInput = openFileInput.readlines()
				linesSeq = openFileSequence.readlines()
				lengthlinesInput=len(linesInput)
				lengthSeq=len(linesSeq)
				for i in range(0,lengthlinesInput-1):
					posIni.write(linesInput[i])
				for i in range(0,lengthSeq):
					fileWithSequence.write(linesSeq[i])
				for line in ptt:
					if count == comp:
						lastline+=1
					countsPtt+=1
					if countsPtt == 1:
						linha = line.split(',')
						nome = linha[0]
						genomSize=linha[1].split("..")[1].strip()
					elif countsPtt == 2 or countsPtt == 3:
						result=""
					else:
						colunas = line.split("\t")
						local = colunas[0].split("..")
						begin = local[0]
						end = local[1]
						if int(begin)>int(end):
							begin = local[1]
							end = local[0]
						strand = colunas[1]
						lengthProt = colunas[2]
						pid = colunas[3]
						if colunas[4]=='-':
							gene1=colunas[5]
						else:	
							gene1 = colunas[4]
						cog = colunas[6]
						product = colunas[8].strip()
						countlines+=1
						posIni.write("{\"name\": " + "\"" + nome.replace(".","") + "\", \"genome\": \"" + str(count) + "\", \"gene\": \"" + str(count) + "..." + gene1 +'_'+str(countlines)+ "\", \"product\": \"" + product + "\",\"begin\": " + "\"" + begin + "\"" + ",\"end\": " + "\"" + end + "\"" + ",\"strand\": " + "\"" + strand + "\"" + ",\"lengthProt\": " + "\"" + lengthProt + "\"" + ",\"fileType\": " + "\".ptt\",\"genomeSize\": \"" + str(genomSize) + "\",\"reference\": " + "\"" + "gi|" + gene1 + "|ref|" + pid +'_'+str(countlines)+ "|" + product + "[" + nome.replace(".","") + "]"+ "\"," + "\n")
						fileProvTemp.write("{\"name\": " + "\"" + nome.replace(".","") + "\", \"genome\": \"" + str(count) + "\", \"gene\": \"" + str(count) + "..." + gene1 +'_'+str(countlines)+ "\", \"product\": \"" + product + "\",\"begin\": " + "\"" + begin + "\"" + ",\"end\": " + "\"" + end + "\"" + ",\"strand\": " + "\"" + strand + "\"" + ",\"lengthProt\": " + "\"" + lengthProt + "\"" + ",\"fileType\": " + "\".ptt\",\"genomeSize\": \"" + str(genomSize) + "\",\"reference\": " + "\"" + "gi|" + gene1 + "|ref|" + pid +'_'+str(countlines)+ "|" + product + "[" + nome.replace(".","") + "]"+ "\"," + "\n")	
				ptt.close()
			

			if '.faa' in files:    #Parse de ficheiros .faa
				pathFile=files.split("/")
				filename=pathFile[len(pathFile)-1].split(".")
				filemodified='uploads/'+path+'/input_files/'+filename[0]+'_mod.'+filename[1]
				if os.path.isfile(filemodified):
					faa=open(filemodified,'r')
				else:
					faa=open(files,'r')
				count+=1
				lines = faa.readlines()
				lengthLines=len(lines)
				countLines=0
				#fileJustSequence=open(openJustSequence,'w')
				#os.chmod(openJustSequence, 0755)
				linesInput = openFileInput.readlines()
				linesSeq = openFileSequence.readlines()
				lengthlinesInput=len(linesInput)
				lengthSeq=len(linesSeq)
				for i in range(0,lengthlinesInput-1):
					posIni.write(linesInput[i])
				for i in range(0,lengthSeq):
					fileWithSequence.write(linesSeq[i])
				for i in range(0,lengthLines-1):
					if '>gi' in lines[i]:
						countLines+=1
						linha = re.split('\|',lines[i])
						name = linha[4]
						nome2 = linha[3]
						nome = re.split('\[',name)
						funcao = nome[0]
						nome1 = re.split('\]',nome[1])
						funcao=funcao.strip()
						countlines+=1
						nomeOrg=nome1[0] 
						result = "{\"name\": " + "\"" + nome1[0] + "\", \"genome\": \"" + str(count) + "\", \"gene\": \"" + str(count) + "..." + nome2 +'_'+str(countlines)+ "\", \"product\": \"" + funcao + "\",\"begin\": " + "\""  + "\"" + ",\"end\": " + "\""  + "\"" + ",\"strand\": " + "\"" + "\"" + ",\"protein_id\": " + "\"" + "\"" + ",\"fileType\": " + "\".faa\",\"reference\": " + "\"" + lines[i].strip() +'_'+str(countlines)+ "\",\n" 
						if countLines==1:
							fileWithSequence.write("{\"gene\": \"" + lines[i].strip() +'_'+str(countlines)+ "\", \"genome\": \"" + str(count) + "\",\"sequence\": " + "\"")
						else:
							fileWithSequence.write("\"}\n{\"gene\": \"" + lines[i].strip() +'_'+str(countlines)+ "\", \"genome\": \"" + str(count) + "\",\"sequence\": " + "\"")
						posIni.write(result)
						fileProvTemp.write(result)
							
					elif re.match('[A-Z]',lines[i]):
						countLines+=1
						if result == "":
							result=""
						else:
							result= lines[i].strip()
							fileWithSequence.write(result)
							#fileJustSequence.write(result)

					if countLines==lengthLines-1:
						fileWithSequence.write("\"}")
							
				faa.close() 
				#fileJustSequence.close() 
				stringOfFiles+=filename[0]+'...'+name.replace(' ','..')+'...'+str(count)+'---'

			if '.ffn' in files: 
				pathFile=files.split("/")
				filename=pathFile[len(pathFile)-1].split(".")
				filemodified='uploads/'+path+'/input_files/'+filename[0]+'_mod.'+filename[1]
				countLines=0
				if os.path.isfile(filemodified):
					ffn=open(filemodified,'r')
				else:
					ffn=open(files,'r')
				count+=1
				lines = ffn.readlines()
				lengthLines=len(lines)
				linesInput = openFileInput.readlines()
				linesSeq = openFileSequence.readlines()
				lengthlinesInput=len(linesInput)
				lengthSeq=len(linesSeq)
				#fileJustSequence=open(openJustSequence,'w')
				#os.chmod(openJustSequence, 0755)
				for i in range(0,lengthlinesInput-1):
					posIni.write(linesInput[i])
				for i in range(0,lengthSeq):
					fileWithSequence.write(linesSeq[i])
				countSegments=0
				for i in range(0,lengthLines-1):
					if '>gi' in lines[i]:
						countLines+=1
						countSegments+=1
						linha = re.split('\|',lines[i])
						beginEnd=linha[4].split(" ")
						begin=beginEnd[0].split("-")[0]
						if re.search(":c",begin):
							begin=begin.replace(":c","")
						else:
							begin=begin.replace(":","")
						end=beginEnd[0].split("-")[1]
						nome2 = linha[1]
						nome = linha[4].split(",")[0].split(" ")
						nome = ' '.join([str(nome[x]) for x in range(1,len(nome))])
						countlines+=1
						gene=lines[i].split("|")[3] +'_'+str(countlines)
						if countLines==1:
							fileWithSequence.write("{\"gene\": \"" + "gi|" + gene + "|ref|" + gene + "|[" + nome + "]" +'_'+str(countlines)+ "\", \"genome\": \"" + str(count) + "\",\"sequence\": " + "\"")
						else:
							fileWithSequence.write("\"}\n{\"gene\": \"" + "gi|" + gene + "|ref|" + gene + "|[" + nome + "]" +'_'+str(countlines)+ "\", \"genome\": \"" + str(count) + "\",\"sequence\": " + "\"")
						result = "{\"name\": " + "\"" + nome + "\", \"genome\": \"" + str(count) + "\", \"gene\": \"" + str(count) + "..." + lines[i].split("|")[3] + "_"+str(countlines)+ "\", \"product\": \"-\",\"begin\": " + "\""  +begin+ "\"" + ",\"end\": " + "\""  +end+ "\"" + ",\"contig\": " + "\"1\",\"strand\": " + "\"" + "\"" + ",\"protein_id\": " + "\"" + "\"" + ",\"fileType\": " + "\".ffn\",\"reference\": " + "\"" + "gi|" + gene + "|ref|" + gene + "|[" + nome + "]" +'_'+str(countlines)+ '",\n'
						fileProvTemp.write(result)
						posIni.write(result)
							
					elif re.match('[A-Z]',lines[i]):
						countLines+=1
						if result == "":
							result=""
						else:
							result= lines[i].strip()
							fileWithSequence.write(result)
							#fileJustSequence.write(result)

					if countLines==lengthLines-1:
						fileWithSequence.write("\"}")

				countsFaa=0
				#fileJustSequence.close()

				stringOfFiles+=filename[0]+'...'+nome.replace(' ','..')+'...'+str(count)+'---'

			if '.fna' in files:  # Faz parse dos ficheiros .fasta contigs do SERGIO
				pathFile=files.split("/")
				countLines=0
				filename=pathFile[len(pathFile)-1].split(".")
				filemodified='uploads/'+path+'/input_files/'+filename[0]+'_mod.'+filename[1]
				length=0
				Totalsequence=''
				Contigfile='no'
				CountContigFasta+=1
				lenSequence=0
				prevEnd=""
				ENARef=""
				contigNumber=0
				firstLine=""
				#fileJustSequence=open(openJustSequence,'w')
				#os.chmod(openJustSequence, 0755)

				if os.path.isfile(filemodified):
					fasta=open(filemodified,'r')
				else:
					fasta=open(files,'r')
				count+=1
				lines = fasta.readlines()
				lengthLines=len(lines)
				linesInput = openFileInput.readlines()
				linesSeq = openFileSequence.readlines()
				lengthlinesInput=len(linesInput)
				lengthSeq=len(linesSeq)
				for i in range(0,lengthlinesInput-1):
					posIni.write(linesInput[i])
				for i in range(0,lengthSeq):
					fileWithSequence.write(linesSeq[i])
				for i in range(0,lengthLines-1):
					if count == comp:
						lastline+=1
					if '>' in lines[i]:
						if firstLine=="":
							firstLine=lines[i]
						contigNumber+=1
						countLines+=1
						if countLines==1:
							linha = re.split('\|',lines[i])
							nome = linha[4].split(",")[0].split(" ")
							nome = ' '.join([str(nome[x]) for x in range(1,len(nome))])
							countlines+=1
							gene=lines[i].split("|")[3] +'_'+str(countlines)
							ENAref="\"reference\": \""+ "gi|" + gene + "|ref|" + gene + "|[" + nome + "]" +'_'+str(countlines)+ "\","
							posIni.write("{\"name\": \""+ "gi|" + gene + "|ref|" + gene + "|[" + nome + "]" +'_'+str(countlines) + "\", \"genome\": \"" + str(count) + "\", \"gene\": \"" + str(count) + "..."+ lines[i].split("|")[3]+'_'+str(countlines)+"\", \"product\": \"" + "\",\"begin\": " + "\"" + str(0) + "\"" + ",")
							fileProvTemp.write("{\"name\": \""+ "gi|" + gene + "|ref|" + gene + "|[" + nome + "]" +'_'+str(countlines) + "\", \"genome\": \"" + str(count) + "\", \"gene\": \"" + str(count) + "..."+ lines[i].split("|")[3]+'_'+str(countlines)+"\", \"product\": \"" + "\",\"begin\": " + "\"" + str(0) + "\"" + ",")
							fileWithSequence.write("{\"gene\": \"" + "gi|" + gene + "|ref|" + gene + "|[" + nome + "]" +'_'+str(countlines)+ "\", \"genome\": \"" + str(count) + "\",\"sequence\": \"")
							countLines+=1
					if re.match('[A-Z]',lines[i]):
						countLines+=1
						sequence=lines[i].strip()
						lenSequence+=len(sequence)
						fileWithSequence.write(sequence)
						#fileJustSequence.write(sequence)		
					if Contigfile!='yes' and countLines==lengthLines-1:
						posIni.write("\"end\": " + "\"" + str(lenSequence) + "\"" +"," + "\"contig\": " + "\""+str(contigNumber)+"\"" + ",\"strand\": " + "\"" + "\",\"fileType\": " + "\".fasta\",\"genomeSize\": \"" +str(lenSequence)+ "\"," + ENAref+ "\n")
						fileProvTemp.write("\"end\": " + "\"" + str(lenSequence) + "\"" +"," + "\"contig\": " + "\""+str(contigNumber)+"\"" + ",\"strand\": " + "\"" + "\",\"fileType\": " + "\".fasta\",\"genomeSize\": \"" +str(lenSequence)+ "\"," + ENAref+ "\n")
					#elif countLines==lengthLines-1:
						#posIni.write("\"genomeSize\": \""+"\",\n")
				fileWithSequence.write('"}\n')
				fasta.close()
				#fileJustSequence.close()

				stringOfFiles+=filename[0]+'...'+nome.replace(' ','..')+'...'+str(count)+'---'

			if '.gbk' in files:
				countContigs=0
				countContigs+=1
				prevEnd=0
				countUndefined=0
				#namefastafileDB=path+"/blastbds/"+files.split(".")[0]+".ffn"
				#fastafileDB=open(namefastafileDB,'w')
				#os.chmod(namefastafileDB, 0755)
				#typefile=re.split(".",files)
				#filetype=typefile[len(typefile) - 1]
				pathFile=files.split("/")
				filename=pathFile[len(pathFile)-1].split(".")
				filemodified='uploads/'+path+'/input_files/'+filename[0]+'_mod.'+filename[1]
				if os.path.isfile(filemodified):
					genome=SeqIO.read(open(filemodified),'genbank') #you MUST tell SeqIO what format is being read
				else:
					try:
						genome=SeqIO.read(open(files),'genbank') #you MUST tell SeqIO what format is being read
					except ValueError:
						genome=SeqIO.read(open(files),'embl')
				count+=1
				lines = openFileInput.readlines()
				linesSeq = openFileSequence.readlines()
				lengthLines=len(lines)
				lengthSeq=len(linesSeq)
				#fileJustSequence=open(openJustSequence,'w')
				#os.chmod(openJustSequence, 0755)
				#fileJustSequence.write(str(genome.seq))
				#fileJustSequence.close()
				for i in range(0,lengthLines-1):
					posIni.write(lines[i])
				for i in range(0,lengthSeq):
					fileWithSequence.write(linesSeq[i])
				for i,feature in enumerate(genome.features):
					if feature.type=='source':
						genomeSize= feature.location.end
						name=feature.qualifiers['organism'][0]
					if feature.type=='CDS' or feature.type=='tRNA' or feature.type=='rRNA' or feature.type=='ncRNA' or feature.type=='tmRNA':
						try:
							locus_tag=feature.qualifiers['locus_tag'][0]
						except KeyError:
							locus_tag='-'
						try:
							product=feature.qualifiers['product'][0]
						except KeyError:
							product='-'
						try:
							dbref=feature.qualifiers['db_xref'][0].split(":")[1]
						except KeyError:
							dbref='-'
						try:
							protein_id=feature.qualifiers['protein_id'][0]
						except KeyError:
							protein_id='-'
						try:
							translation=feature.qualifiers['translation'][0]
						except KeyError:
							translation='-'
						try:
							begin = feature.location.start.position
						except KeyError:
							begin='-'
						try:
							end = feature.location.end.position
						except KeyError:
							end='-'
						countlines+=1
						if (prevEnd+100)<begin:
							countlines+=1
							countUndefined+=1
							Nsequence=genome.seq[prevEnd:begin]
							posIni.write("{\"name\": " + "\"" + name + "\", \"genome\": \"" + str(count) + "\", \"gene\": \"" + str(count) + "...Undefined_"+str(countUndefined)+'_'+str(countlines)+"\", \"product\": \"Undefined\",\"begin\": " + "\"" + str(prevEnd+1) + "\"" + ",\"end\": " + "\"" + str(begin-1) + "\"" + ",\"contig\": \""+str(countContigs)+"\",\"strand\": " + "\"-\"" + ",\"protein_id\": " + "\"-\"" + ",\"fileType\": " + "\".gbk\",\"genomeSize\": \"" + str(genomeSize) + "\",\"reference\": \"" + "Undefined_"+str(countUndefined)+'_'+str(countlines)+"\",\n")
							fileProvTemp.write("{\"name\": " + "\"" + name + "\", \"genome\": \"" + str(count) + "\", \"gene\": \"" + str(count) + "...Undefined_"+str(countUndefined)+'_'+str(countlines)+"\", \"product\": \"Undefined\",\"begin\": " + "\"" + str(prevEnd+1) + "\"" + ",\"end\": " + "\"" + str(begin-1) + "\"" + ",\"contig\": \""+str(countContigs)+"\",\"strand\": " + "\"-\"" + ",\"protein_id\": " + "\"-\"" + ",\"fileType\": " + "\".gbk\",\"genomeSize\": \"" + str(genomeSize) + "\",\"reference\": \"" + "Undefined_"+str(countUndefined)+'_'+str(countlines)+"\",\n")
							fileWithSequence.write("{\"gene\": \"" + "Undefined_"+str(countUndefined)+'_'+str(countlines)+"\", \"genome\": \"" + str(count) + "\",\"sequence\": " + "\"" + str(Nsequence) + "\"}\n")
						if feature.location == 1:
							strand = '+'
						else:
							strand = '-'
						Nsequence=genome.seq[begin:end]
						try:
							genes = feature.qualifiers['gene'][0]
						except KeyError:
							genes = feature.qualifiers['locus_tag'][0]

						#fastafileDB.write(">gi|" + dbref + "|ref|" + genes + "|" + product + "[" + name + "]\n" + Nsequence +"\n")
						posIni.write("{\"name\": " + "\"" + name + "\", \"genome\": \"" + str(count) + "\", \"gene\": \"" + str(count) + "..." + genes +'_'+str(countlines)+ "\", \"product\": \"" + product + "\",\"begin\": " + "\"" + str(begin) + "\"" + ",\"end\": " + "\"" + str(end) + "\"" + ",\"contig\": \""+str(countContigs)+"\"" + ",\"strand\": " + "\"" + strand + "\"" + ",\"protein_id\": " + "\"" + str(protein_id) + "\"" + ",\"fileType\": " + "\".gbk\",\"genomeSize\": \"" + str(genomeSize) + "\",\"reference\": \"" + "gi|" + dbref + "|ref|" + genes +'_'+str(countlines)+ "|" + product + "[" + name + "]"+"\",\n")
						fileProvTemp.write("{\"name\": " + "\"" + name + "\", \"genome\": \"" + str(count) + "\", \"gene\": \"" + str(count) + "..." + genes +'_'+str(countlines)+ "\", \"product\": \"" + product + "\",\"begin\": " + "\"" + str(begin) + "\"" + ",\"end\": " + "\"" + str(end) + "\"" + ",\"contig\": \""+str(countContigs)+"\"" + ",\"strand\": " + "\"" + strand + "\"" + ",\"protein_id\": " + "\"" + str(protein_id) + "\"" + ",\"fileType\": " + "\".gbk\",\"genomeSize\": \"" + str(genomeSize) + "\",\"reference\": \"" + "gi|" + dbref + "|ref|" + genes +'_'+str(countlines)+ "|" + product + "[" + name + "]"+"\",\n")
						fileWithSequence.write("{\"gene\": \"" + "gi|" + dbref + "|ref|" + genes +'_'+str(countlines)+ "|" + product + "[" + name + "]"+ "\", \"genome\": \"" + str(count) + "\",\"sequence\": " + "\"" + str(Nsequence) + "\"}\n")
						prevEnd=end

				stringOfFiles+=filename[0]+'...'+name.replace(' ','..')+'...'+str(count)+'---'

			if '.fasta' in files or '.fa' in files:  # Faz parse dos ficheiros .fasta contigs do SERGIO
				pathFile=files.split("/")
				countLines=0
				countContigs=0
				countContigs+=1
				filename=pathFile[len(pathFile)-1].split(".")
				filemodified='uploads/'+path+'/input_files/'+filename[0]+'_mod.'+filename[1]
				length=0
				Totalsequence=''
				Contigfile='no'
				CountContigFasta+=1
				lenSequence=0
				prevEnd=""
				ENARef=""
				contigNumber=0
				firstLine=""
				newSequence='no'
				orgName=""
				#fileJustSequence=open(openJustSequence,'w')
				#os.chmod(openJustSequence, 0755)
				if os.path.isfile(filemodified):
					fasta=open(filemodified,'r')
				else:
					fasta=open(files,'r')
				count+=1
				lines = fasta.readlines()
				lengthLines=len(lines)
				linesInput = openFileInput.readlines()
				linesSeq = openFileSequence.readlines()
				lengthlinesInput=len(linesInput)
				lengthSeq=len(linesSeq)
				for i in range(0,lengthlinesInput-1):
					posIni.write(linesInput[i])
				for i in range(0,lengthSeq):
					fileWithSequence.write(linesSeq[i])
				for i in range(0,lengthLines):
					if newSequence=='yes':
						length=0
					if count == comp:
						lastline+=1
					if IsContig == 'yes' and not re.match('[A-Z]',lines[i]) and not re.match('[a-z]',lines[i]):
						if firstLine=="":
							firstLine=lines[i]
						contigNumber+=1
						Contigfile='yes'
						countLines+=1
						information=lines[i].split("_")
						length=information[3]
						countlines+=1
						if countLines==1:
							orgName=lines[i].replace(">","").strip().replace(" ","_")
							#posIni.write("{\"name\": \""+ lines[i].replace(">","").strip().replace(" ","_") +'_'+str(countlines)+ "\", \"genome\": \"" + str(count) + "\", \"gene\": \"" + str(count) + "..." + lines[i].replace(">","").strip().replace(" ","_") +'_'+str(countlines)+ "\", \"product\": \"Undefined\",\"begin\": " + "\"" + str(0) + "\"" + ",\"end\": " + "\"" + length + "\"" + ",\"contig\": " + "\"" + str(contigNumber) + "\""+",\"strand\": " + "\"" + "\""  + ",\"fileType\": " + "\".fasta\"," + "\"reference\": \""+ lines[i].replace(">","").strip().replace(" ","_") +'_'+str(countlines)+ "\",\n")
							#fileProvTemp.write("{\"name\": \""+ lines[i].replace(">","").strip().replace(" ","_") +'_'+str(countlines)+ "\", \"genome\": \"" + str(count) + "\", \"gene\": \"" + str(count) + "..." + lines[i].replace(">","").strip().replace(" ","_") +'_'+str(countlines)+ "\", \"product\": \"Undefined\",\"begin\": " + "\"" + str(0) + "\"" + ",\"end\": " + "\"" + length + "\"" + ",\"contig\": " + "\"" + str(contigNumber) + "\"" + ",\"strand\": " + "\"" + "\"" + ",\"fileType\": " + "\".fasta\"," + "\"reference\": \""+ lines[i].replace(">","").strip().replace(" ","_") +'_'+str(countlines)+ "\",\n")
							#fileWithSequence.write("{\"gene\": \"" + lines[i].replace(">","").strip().replace(" ","_") +'_'+str(countlines)+ "\", \"genome\": \"" + str(count) + "\",\"sequence\": \"")
							posIni.write("{\"name\": \""+ lines[i].replace(">","").strip().replace(" ","_") + "\", \"genome\": \"" + str(count) + "\", \"gene\": \"" + str(count) + "..." + lines[i].replace(">","").strip().replace(" ","_") +'_'+str(countlines)+ "\", \"product\": \"Undefined\",\"begin\": " + "\"" + str(0) + "\"" + ",\"end\": " + "\"" + length + "\"" + ",\"contig\": " + "\"" + str(contigNumber) + "\""+",\"strand\": " + "\"" + "\""  + ",\"fileType\": " + "\".fasta\"," + "\"reference\": \""+ lines[i].replace(">","").strip().replace(" ","_") + "\",\n")
							fileProvTemp.write("{\"name\": \""+ lines[i].replace(">","").strip().replace(" ","_") + "\", \"genome\": \"" + str(count) + "\", \"gene\": \"" + str(count) + "..." + lines[i].replace(">","").strip().replace(" ","_") +'_'+str(countlines)+ "\", \"product\": \"Undefined\",\"begin\": " + "\"" + str(0) + "\"" + ",\"end\": " + "\"" + length + "\"" + ",\"contig\": " + "\"" + str(contigNumber) + "\"" + ",\"strand\": " + "\"" + "\"" + ",\"fileType\": " + "\".fasta\"," + "\"reference\": \""+ lines[i].replace(">","").strip().replace(" ","_") + "\",\n")
							fileWithSequence.write("{\"gene\": \"" + lines[i].replace(">","").strip().replace(" ","_") + "\", \"genome\": \"" + str(count) + "\",\"sequence\": \"")
						else:
							#posIni.write("{\"name\": \""+ lines[i].replace(">","").strip().replace(" ","_") +'_'+str(countlines)+ "\", \"genome\": \"" + str(count) + "\", \"gene\": \"" + str(count) + "..." + lines[i].replace(">","").strip().replace(" ","_") +'_'+str(countlines)+ "\", \"product\": \"Undefined\",\"begin\": " + "\"" + str(0) + "\"" + ",\"end\": " + "\"" + length + "\"" + ",\"contig\": " + "\"" + str(contigNumber) + "\"" + ",\"strand\": " + "\"" + "\"" + ",\"contig\": " + "\"" + str(contigNumber) + "\"" + ",\"fileType\": " + "\".fasta\"," + "\"reference\": \""+ lines[i].replace(">","").strip().replace(" ","_") +'_'+str(countlines)+ "\",\n")
							#fileProvTemp.write("{\"name\": \""+ lines[i].replace(">","").strip().replace(" ","_") +'_'+str(countlines)+ "\", \"genome\": \"" + str(count) + "\", \"gene\": \"" + str(count) + "..." + lines[i].replace(">","").strip().replace(" ","_") +'_'+str(countlines)+ "\", \"product\": \"Undefined\",\"begin\": " + "\"" + str(0) + "\"" + ",\"end\": " + "\"" + length + "\"" + ",\"contig\": " + "\"" + str(contigNumber) + "\"" + ",\"strand\": " + "\"" + "\"" + ",\"fileType\": " + "\".fasta\"," + "\"reference\": \""+ lines[i].replace(">","").strip().replace(" ","_") +'_'+str(countlines)+ "\",\n")
							#fileWithSequence.write("\"}\n{\"gene\": \"" + lines[i].replace(">","").strip().replace(" ","_") +'_'+str(countlines)+ "\", \"genome\": \"" + str(count) + "\",\"sequence\": \"")
							posIni.write("{\"name\": \""+ lines[i].replace(">","").strip().replace(" ","_") + "\", \"genome\": \"" + str(count) + "\", \"gene\": \"" + str(count) + "..." + lines[i].replace(">","").strip().replace(" ","_") +'_'+str(countlines)+ "\", \"product\": \"Undefined\",\"begin\": " + "\"" + str(0) + "\"" + ",\"end\": " + "\"" + length + "\"" + ",\"contig\": " + "\"" + str(contigNumber) + "\"" + ",\"strand\": " + "\"" + "\"" + ",\"contig\": " + "\"" + str(contigNumber) + "\"" + ",\"fileType\": " + "\".fasta\"," + "\"reference\": \""+ lines[i].replace(">","").strip().replace(" ","_") + "\",\n")
							fileProvTemp.write("{\"name\": \""+ lines[i].replace(">","").strip().replace(" ","_") + "\", \"genome\": \"" + str(count) + "\", \"gene\": \"" + str(count) + "..." + lines[i].replace(">","").strip().replace(" ","_") +'_'+str(countlines)+ "\", \"product\": \"Undefined\",\"begin\": " + "\"" + str(0) + "\"" + ",\"end\": " + "\"" + length + "\"" + ",\"contig\": " + "\"" + str(contigNumber) + "\"" + ",\"strand\": " + "\"" + "\"" + ",\"fileType\": " + "\".fasta\"," + "\"reference\": \""+ lines[i].replace(">","").strip().replace(" ","_") + "\",\n")
							fileWithSequence.write("\"}\n{\"gene\": \"" + lines[i].replace(">","").strip().replace(" ","_") + "\", \"genome\": \"" + str(count) + "\",\"sequence\": \"")
					elif not re.match('[A-Z]',lines[i]) and not re.match('[a-z]',lines[i]):
						countLines+=1
						#name=lines[i].split("|")[2].strip()
						#reference=name.split(" ")[0]
						countlines+=1
						newSequence='no'
						orgName=lines[i].replace(">","").strip().replace(" ","_")
						posIni.write("{\"name\": \"" + lines[i].replace(">","").strip().replace(" ","_") + "\", \"genome\": \"" + str(count) + "\", \"gene\": \"" + str(count) + "..." + lines[i].replace(">","").strip().replace(" ","_") +'_'+str(countlines)+ "\", \"product\": \"Undefined\",\"begin\": " + "\"" + str(0) + "\"" + ",\"end\": " + "\"")
						fileProvTemp.write("{\"name\": \"" + lines[i].replace(">","").strip().replace(" ","_") + "\", \"genome\": \"" + str(count) + "\", \"gene\": \"" + str(count) + "..." + lines[i].replace(">","").strip().replace(" ","_") +'_'+str(countlines)+ "\", \"product\": \"Undefined\",\"begin\": " + "\"" + str(0) + "\"" + ",\"end\": " + "\"")
						ENAref="\"reference\": \""+ lines[i].replace(">","").strip().replace(" ","_") +'_'+str(countlines)+ "\","
						fileWithSequence.write("{\"gene\": \"" + lines[i].replace(">","").strip().replace(" ","_") +'_'+str(countlines)+ "\", \"genome\": \"" + str(count) + "\",")
					elif Contigfile!='yes' and (re.match('[A-Z]',lines[i]) or re.match('[a-z]',lines[i])):
						countLines+=1
						sequence=lines[i].strip()
						length+=len(sequence)
						Totalsequence+=sequence
					elif re.match('[A-Z]',lines[i]) or re.match('[a-z]',lines[i]):
						countLines+=1
						sequence=lines[i].strip()
						lenSequence+=len(sequence)
						fileWithSequence.write(sequence)
						#fileJustSequence.write(sequence)
					try:	
						if Contigfile!='yes' and not (re.match('[A-Z]',lines[i+1]) or re.match('[a-z]',lines[i+1])):
							newSequence='yes'
							posIni.write( str(length) + "\"" + ",\"contig\": " + "\""+str(contigNumber)+"\"" + ",\"strand\": " + "\"" + "\"" + ",\"coverage\": " + "\"\"" + ",\"fileType\": " + "\".fasta\",\"genomeSize\": \"" +str(length)+ "\"," + ENAref+ "\n")
							fileProvTemp.write( str(length) + "\"" + ",\"contig\": " + "\""+str(contigNumber)+"\"" + ",\"strand\": " + "\"" + "\"" + ",\"coverage\": " + "\"\"" + ",\"fileType\": " + "\".fasta\",\"genomeSize\": \"" +str(length)+ "\"," + ENAref+ "\n")
							fileWithSequence.write("\"sequence\": \"" + str(Totalsequence) + "\"}")
					except IndexError:
						newSequence='yes'
						posIni.write( str(length) + "\"" + ",\"contig\": " + "\""+str(contigNumber)+"\"" + ",\"strand\": " + "\"" + "\"" + ",\"coverage\": " + "\"\"" + ",\"fileType\": " + "\".fasta\",\"genomeSize\": \"" +str(length)+ "\"," + ENAref+ "\n")
						fileProvTemp.write( str(length) + "\"" + ",\"contig\": " + "\""+str(contigNumber)+"\"" + ",\"strand\": " + "\"" + "\"" + ",\"coverage\": " + "\"\"" + ",\"fileType\": " + "\".fasta\",\"genomeSize\": \"" +str(length)+ "\"," + ENAref+ "\n")
						fileWithSequence.write("\"sequence\": \"" + str(Totalsequence) + "\"}")
						#fileJustSequence.write(str(Totalsequence))
					#elif countLines==lengthLines-1:
						#posIni.write("\"genomeSize\": \""+"\",\n")
						#fileProvTemp.write("\"genomeSize\": \""+"\",\n")
				if Contigfile=='yes':
					fileWithSequence.write('"}\n')
				fasta.close()

				stringOfFiles+=filename[0]+'...'+orgName+'...'+str(count)+'---'
				#fileJustSequence.close()

	print stringOfFiles

	posIni.write("]")
	fileProvTemp.write("]")
	fileWithSequence.close()
	posIni.close()
	fileProvTemp.close()
	openFileInput.close()
	openFileSequence.close()
	openProv.close()

	os.remove(openInput)
	#os.rename(openTemp,openInput)

	os.remove(openProvF)
	os.rename(openProvTemp,openProvF)

	os.remove(openSequence)
	os.rename(openSequenceTemp,openSequence)
	os.remove(backupProv)
	os.remove(backupSeq)

except:
	print "ERROR"
	os.remove(openProvF)
	os.rename(backupProv,openProvF)
	os.remove(openSequence)
	os.rename(backupSeq,openSequence)
	os.remove(openSequenceTemp)
	os.remove(openProvTemp)
	os.remove(openTemp)