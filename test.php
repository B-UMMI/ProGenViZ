<?php 
$querygene = "1...mfd_11";
$fileSequence = "uploads/3f72bfda/Sequence_files/mfd_11_sequence.fasta";
$refgenome = "2...";
$evalue = "0.001";
$MinAlign = "300";
$wherePath = "fc9f6470";
$searchRegion = "NODE_1_length_163052_cov_28.6769_ID_454578_1";

$num_filesArray = "2";
$geneBegin = "0";
$geneEnd = "163052";

//exec("python database_search_test1.py $querygene $fileSequence $refgenome $evalue $MinAlign $wherePath", $output, $statusD); echo $statusD; var_dump($output);

//$prodigalCommand = "/usr/local/bin/prodigal -i uploads/".$wherePath."/Sequence_files/".$searchRegion."_sequence.fasta -c -m -g 11 -p single -f sco -q > uploads/".$wherePath."/Prodigal_results/".$searchRegion."_Presults.txt";

exec("python parsers/AnnotateRegion.py $wherePath $searchRegion $num_filesArray $geneBegin $geneEnd",$contigToExport, $statusD);echo $statusD; var_dump($contigToExport);
//exec($prodigalCommand, $output, $statusD); echo $statusD; var_dump($output);

?>
