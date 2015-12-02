import re
import sys
import os

array = sys.argv
path=array[1]
pathToSequence=array[2]
openwhich=pathToSequence
openwhere='uploads/' + path + '/'+ 'sequenceProv.fasta'
filesequence=open(openwhere, 'w')
os.chmod(openwhere, 0777)
inf=open(openwhich, 'r')
lines = inf.readlines()
lastline=len(lines)
targetSequence=""
lengthSequence=0
for i in range(0, lastline):
	if i==0:
		filesequence.write(lines[i])
	else:
		lengthSequence=len(lines[i])
		filesequence.write(lines[i])
if lengthSequence<21000:
	for j in range(lengthSequence, 21000):
		filesequence.write('A')


inf.close()
filesequence.close()

os.remove(openwhich)
os.rename(openwhere, openwhich)