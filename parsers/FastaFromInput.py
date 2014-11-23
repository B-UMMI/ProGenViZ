import sys
import os
import re

array = sys.argv
path=array[1]
genome=array[2]
splittedPath=path.split("/")
fnaFileOutput=splittedPath[0] + "/" + splittedPath[1] + "/input_files/" + splittedPath[3].split(".")[0] + ".ffn"
inputFile="uploads/"+splittedPath[1]+"/"+splittedPath[1]+"_inputWithSequences.json"

def CreateFastaFromInput(genome):
    inputSeq=open(inputFile, 'r')
    fastaOut=open(fnaFileOutput, 'w')
    linesS = inputSeq.readlines()
    lastlineS=len(linesS)
    for i in range(0,lastlineS):
        try:
            line=linesS[i].split('"')
            genomeLine=line[7]
            if genomeLine==genome:
                fastaOut.write(">gn|"  + line[3]+ "\n" + line[11] +"\n")
        except IndexError:
            genomeLine=""
    fastaOut.close()
    inputSeq.close()

CreateFastaFromInput(genome)