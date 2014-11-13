import sys
import os

array = sys.argv
pathWhere=array[1]
geneName=array[2]
geneSequence=array[3]

nameFASTA = "uploads/" + pathWhere + "/Sequence_files/"+geneName+".fasta"

def Create_FASTAquery(geneName,geneSequence):
        of_handle=open(nameFASTA, 'w')
        os.chmod(nameFASTA, 0777)
        of_handle.write(">gn|"  + geneName + "|\n" + geneSequence +"\n")
        of_handle.close()

Create_FASTAquery(geneName,geneSequence)