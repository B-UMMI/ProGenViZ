import re
import sys
import os
from Bio import SeqIO

array = sys.argv
openSNP=array[1]

SNPLocations=[]

alignment=open(openSNP, 'r')
linesA = alignment.readlines()
lastlineA=len(linesA)

for j in range(5, lastlineA):
	linha = linesA[j].strip().split(' ')
	RefLocation=linha[0]
	SNPLocations.append(RefLocation)

print '---'.join([str(x) for x in SNPLocations])

alignment.close()