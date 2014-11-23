import re
import sys
import os

array = sys.argv
openwhich=array[1]
inf=open(openwhich, 'r')
lines = inf.readlines()
lastline=len(lines)
for i in range(0, lastline):
	print lines[i].strip()

inf.close()
