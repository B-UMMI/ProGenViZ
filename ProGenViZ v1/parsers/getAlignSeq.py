import re
import sys
import os

array = sys.argv
path=array[1]
nameSource=array[2]
nameTarget=array[3]
TargetBegin=int(array[4])
TargetEnd=int(array[5])
AlignBegin=int(array[6])
AlignEnd=int(array[7])

nameSource=nameSource.split("...")[1]
nameTarget=nameTarget.split("...")[1]


openwhich='uploads/' + path + '/'+ path +'_inputWithSequences.json'
#openwhere='uploads/' + path + '/'+ path +'_Seq.json'
inf=open(openwhich, 'r')
lines = inf.readlines()
#filesequence=open(openwhere,'w')
lastline=len(lines)
targetSequence=""
for i in range(0, lastline):
	if '{"gene":' in lines[i]:
		line=lines[i].split('"')
		#and line[7]==geneBegin and line[11]==geneEnd
		if nameSource in lines[i]:
			seqSource=line[11]
			if TargetBegin > TargetEnd:
				seqSource=seqSource[AlignBegin:AlignEnd]
				seqSource=seqSource[::-1]
			else:
				seqSource=seqSource[AlignBegin:AlignEnd]
			break

for i in range(0, lastline):
	if '{"gene":' in lines[i]:
		line=lines[i].split('"')
		#and line[7]==geneBegin and line[11]==geneEnd
		if nameTarget in lines[i]:
			seqTarget=line[11]
			if TargetBegin > TargetEnd:
				seqTarget=seqTarget[::-1]
				seqTarget=seqTarget[TargetEnd:TargetBegin]
			else:
				seqTarget=seqTarget[TargetBegin:TargetEnd]
			break

inf.close()

numcharSource=len(seqSource)

matches=''

for i in range(0,numcharSource):
	if seqSource[i]==seqTarget[i]:
		matches+='+'
	else:
		matches+='-'

print seqSource
print seqTarget
print matches


#filesequence.close()