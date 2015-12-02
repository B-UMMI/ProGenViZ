from Bio.Blast.Applications import NcbiblastnCommandline
import os

os.system( "makeblastdb -help -logfile log_test.txt")
os.system( "blastn -help")

print 'done'
