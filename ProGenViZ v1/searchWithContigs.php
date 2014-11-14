<!DOCTYPE html>

<html lang="en"><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <meta charset="utf-8">
    <link href="plugins/pace-0.5.1/themes/pace-theme-center-circle.css" rel="stylesheet" />
    <script data-pace-options='{ "elements": { "selectors": ["#demo_2"] } }' src="plugins/pace-0.5.1/pace.js"></script>
    <title>ProGenViZ</title>
    
    <link href="css/bootstrap.css" rel="stylesheet">
    <link href="css/bootstrap-theme.min.css" rel="stylesheet">

    <script src="js/jquery-2.0.3.min.js"></script>
  <script src="js/bootstrap.min.js"></script>
  <script src="js/holder.js"></script>
  <script src='js/d3.js'></script>
  <script src="js/rgbcolor.js"></script> 
  <script src="js/StackBlur.js"></script>
  <script src="js/canvg.js"></script> 
  <script src="js/prettify.js"></script>
  <script src="js/seedrandom.js"></script>

    <link href="css/theme.css" rel="stylesheet">
    <link href="css/demo.css" rel="stylesheet">
    <link href="css/contextMenu.css" rel="stylesheet">
    <link href="css/sidebar.css" rel="stylesheet">
    <link href="css/dashboard.css" rel="stylesheet">
    <script src="js/vkbeautify.0.99.00.beta.js"></script>
    <style type="text/css" media="screen">
      @import "plugins/DataTables-1.9.4/extras/TableTools/media/css/TableTools.css";
      @import "plugins/DataTables-1.9.4/extras/ColReorder/media/css/ColReorder.css";
      @import "plugins/DataTables-1.9.4/extras/ColVis/media/css/ColVis.css";
      div.dataTables_wrapper { font-size: 15px; }
      table.display thead th, table.display td { font-size: 12px; }
    
    </style>
    
    <script type="text/javascript" src="plugins/DataTables-1.9.4/media/js/jquery.dataTables.js"></script>
    <script type="text/javascript" src="plugins/DataTables-1.9.4/extras/TableTools/media/js/TableTools.min.js"></script>
    <script type="text/javascript" src="plugins/DataTables-1.9.4/extras/ColReorder/media/js/ColReorder.js"></script>
    <script type="text/javascript" src="plugins/DataTables-1.9.4/extras/ColVis/media/js/ColVis.js"></script>
    <link href="plugins/DataTables-1.9.4/media/css/demo_page.css" rel="stylesheet">
    <link href="plugins/DataTables-1.9.4/media/css/demo_table.css" rel="stylesheet">


  <style id="holderjs-style" type="text/css"></style></head>

  <!--#######################################################START OF PHP POST AND SESSIONS DEALING#####################################!-->

  <?php

    session_start();

    $_SESSION['SearchMade']='yes';


    if ($_SESSION['uploadError'] == 'yes'){
        $array_path_Prov = $_SESSION['array_path[]'];
        $numFilesUp=count($array_path_Prov)-1;
        unset($array_path_Prov[$numFilesUp]);
        $path_value = array_values($array_path_Prov);
        $_SESSION['array_path[]'] = $path_value;
        echo "<script src='data_plot_js/ErrorOnUpload.js'></script>";
    }
    else $_SESSION['uploadError'] = 'no';

    $refresh='yes'; //loads the page faster cus dont run the parsers

    if (isset($_POST['inter-bygene'])) {
      if ($_SESSION['searchBySequence']=='yes'){
        $_SESSION['searchBySequence']='no';
        $_SESSION["identities"]=null;
        $_SESSION['string_array']="null";
        $_SESSION['string_database']=null;
        $_SESSION['prevQueryGene']='null';
        $_SESSION['Numdatabasesearch']=0;
      }
      //echo "<div id='check-upload'>Compare method in use : By gene name with next position genome.</div>";
      $_SESSION['compNull'] = 'no';
      $_SESSION['inter-bygene'] = 'yes';
      $_SESSION['inter-byfunction'] = 'no';
      $runScripts='yes';
    }
    if (isset($_POST['inter-byfunction'])){
      if ($_SESSION['searchBySequence']=='yes'){
        $_SESSION['searchBySequence']='no';
        $_SESSION["identities"]=null;
        $_SESSION['string_array']="null";
        $_SESSION['string_database']=null;
        $_SESSION['prevQueryGene']='null';
        $_SESSION['Numdatabasesearch']=0;
      }
      //echo "<div id='check-upload'>Compare method in use : By gene function with next position genome.</div>";
      $_SESSION['compNull'] = 'no';
      $_SESSION['inter-bygene'] = 'no';
      $_SESSION['inter-byfunction'] = 'yes';
      $runScripts='yes';
    } 

    if (isset($_POST['AnnGeneBeEnd'])){
       $_SESSION['AnnBeginEnd'] = $_POST["AnnGeneBeEnd"];
    }


    if (isset($_POST['OriginalName'])){
    $editName=$_POST['EditName'];
    $editProduct=$_POST['EditProduct'];
    $nameToChange=$_POST['OriginalName'];
    $productToChange=$_POST['OriginalProduct'];
    $geneBegin=$_POST['geneBegin'];
    $geneEnd=$_POST['geneEnd'];
    if($editName==null) $editName='null';
    else $editName = preg_replace('/\s+/', '---', $editName);
    if($editProduct==null) $editProduct='null';
    else $editProduct = preg_replace('/\s+/', '---', $editProduct);
    if($nameToChange==null) $nameToChange='null';
    else $nameToChange = preg_replace('/\s+/', '---', $nameToChange);
    if($productToChange==null) $productToChange='null';
    else $productToChange = preg_replace('/\s+/', '---', $productToChange);
    if($geneBegin==null) $geneBegin='null';
    else $geneBegin = preg_replace('/\s+/', '---', $geneBegin);
    if($geneEnd==null) $geneEnd='null';
    else $geneEnd = preg_replace('/\s+/', '---', $geneEnd);
    $runScripts='yes';
    $_SESSION['editInfo']='yes';
   }
   else $_SESSION['editInfo']='no';

    if(isset($_POST['rundatabasesearch']) || isset($_POST['SearchForSequence'])){
     if ($_SESSION['string_database']==null) $_SESSION['string_database']=array();
     $_SESSION['searchBySequence']='yes';
     $_SESSION['AnnotateRegion']='no';
     $_SESSION['searchbox'] = 'no';
     if(isset($_POST['rundatabasesearch'])) $runScripts='yes';
     if(isset($_POST['searchNCBI'])){
      $_SESSION['searchNCBI']='yes';
     }
     else{
      $_SESSION['geneSequenceNCBI']=null;
      $_SESSION['NCBISearch']='no';
      $_SESSION['searchNCBI']='no';
      $_SESSION['geneSource']=null;
      $_SESSION['NCBIOrganism']=null;
      $_SESSION["NCBISequence"]=null;
      $_SESSION['searchArray[]']=null;
     }
     if(isset($_POST['AnnotateRegion'])){
      $_SESSION['AnnotateRegion']='yes';
      $_SESSION['QueryRegion']=$_POST['QueryRegion'];
      $_SESSION['databaseAfterRemove']='no';
      $_SESSION["SearchByBLAST"]="no";
      $_SESSION['searchBySequence']='no';
      $_SESSION['ArrayBLAST[]']=array();
      $_SESSION['searchLengthArray']=null;
      $_SESSION['alignment_position']=null;
      $_SESSION['alignScore']=null;
      $_SESSION['refStart']=null;
      $_SESSION['subEnd']=null;
      $_SESSION['seqQuery']=null;
      $_SESSION['seqsub']=null;
      $_SESSION['seqmatch']=null;
      $_SESSION['string_database']=null;
      $_SESSION['string_array']=null;
      $string_array='null';
      $search_array=null;
      unset($_SESSION['searchArray[]']);
      unset($_SESSION['typesearch[]']);
     }
     $_SESSION['rundatabasesearch']='yes';
     $_SESSION['searchArray[]']=null;
     $_SESSION['string_array']="null";
     $_SESSION['compNull'] = 'no';
     $_SESSION['inter-bygene'] = 'no';
     $_SESSION['inter-byfunction'] = 'no';
   }
   else {
    $_SESSION['NCBISearch']='no';
    $_SESSION['geneSequenceNCBI']=null;
    $_SESSION['searchNCBI']='no';
    $_SESSION['geneSource']=null;
    $_SESSION['NCBIOrganism']=null;
    $_SESSION["NCBISequence"]=null;
    $_SESSION['rundatabasesearch']='no';
    $_SESSION['prevQueryGene']='null';
    $_SESSION['Numdatabasesearch']=0;
   }



    if (isset($_POST['exclude_hypothetical'])){
     //echo "<div id='check-upload'>Hypothetical proteins have been excluded from analysis.</div>";
     $_SESSION['exclude_hypothetical'] = 'yes';
     $path_value=$_SESSION['array_path[]'];
    }
    if (isset($_POST['add_hypothetical'])){
      //echo "<div id='check-upload'>Hypothetical proteins have been added to analysis.</div>";
      $path_value=$_SESSION['array_path[]'];
      $_SESSION['exclude_hypothetical'] = 'no';
    }

    $array_path=$_SESSION['array_path[]'];
    $search_array= array();

    if (isset($_SESSION['typesearch[]'])) $typesearch_array = $_SESSION['typesearch[]'];
    else $typesearch_array = array();

    if (isset($_SESSION['prevsearchterm'])) {
                                            $prevsearch = $_SESSION['prevsearchterm'];
                                            $prevsearchtype = $_SESSION['prevsearchtype'];
                                          }
    else{
       $prevsearch = null;
       $prevsearchtype = null;
     }

    if (isset($_POST['selectionArray'])){
          $_SESSION['selectionArray'] = $_POST['selectionArray'];
    }

    $string_array=$_SESSION['string_array'];
    $search_array=$_SESSION['searchArray[]'];

    $remove_hypo='undefined';
    $search_term;


    if (isset($_POST['removeBLAST'])){
      $_SESSION['searchBySequence']='yes';
      $removeBLAST=intval($_POST['removeBLAST']);
      $geneThatImports=$_SESSION['ArrayBLAST[]'][$removeBLAST];
      $ToRemove=$_SESSION['string_database'][$removeBLAST];
      unset($_SESSION['string_database'][$removeBLAST]);
      unset($_SESSION['ArrayBLAST[]'][$removeBLAST]);
      $_SESSION['ArrayBLAST[]']=array_values($_SESSION['ArrayBLAST[]']);
      $_SESSION['string_database'] = array_values($_SESSION['string_database']);
      unset($_SESSION['alignment_position'][$removeBLAST]);
      $_SESSION['alignment_position']= array_values($_SESSION['alignment_position']);
      unset($_SESSION['alignScore'][$removeBLAST]);
      $_SESSION['alignScore']= array_values($_SESSION['alignScore']);
      unset($_SESSION['refStart'][$removeBLAST]);
      $_SESSION['refStart']= array_values($_SESSION['refStart']);
      unset($_SESSION['subEnd'][$removeBLAST]);
      $_SESSION['subEnd']= array_values($_SESSION['subEnd']);
      unset($_SESSION['seqQuery'][$removeBLAST]);
      $_SESSION['seqQuery']= array_values($_SESSION['seqQuery']);
      unset($_SESSION['seqsub'][$removeBLAST]);
      $_SESSION['seqsub']= array_values($_SESSION['seqsub']);
      unset($_SESSION['seqmatch'][$removeBLAST]);
      $_SESSION['seqmatch']= array_values($_SESSION['seqmatch']);
      unset($_SESSION['searchLengthArray'][$removeBLAST]);
      $_SESSION['searchLengthArray']= array_values($_SESSION['searchLengthArray']);
      unset($_SESSION['identifiers'][$removeBLAST]);
      $_SESSION['identifiers']= array_values($_SESSION['identifiers']);
    
      if (count($_SESSION['ArrayBLAST[]'])==0){
        $_SESSION['databaseAfterRemove']='no';
        $_SESSION["SearchByBLAST"]="no";
        $_SESSION['searchBySequence']='no';
        $_SESSION['ArrayBLAST[]']=array();
        $_SESSION['searchLengthArray']=null;
        $_SESSION['alignment_position']=null;
        $_SESSION['alignScore']=null;
        $_SESSION['refStart']=null;
        $_SESSION['subEnd']=null;
        $_SESSION['seqQuery']=null;
        $_SESSION['seqsub']=null;
        $_SESSION['seqmatch']=null;
        $_SESSION['string_database']=null;
        $_SESSION['string_array']=null;
        $string_array='null';
        $search_array=null;
        unset($_SESSION['searchArray[]']);
        unset($_SESSION['typesearch[]']);
        $wherePath=$_SESSION['userPath'];
        exec("python makeComparisons/makeImportsNullAfterBLAST.py $wherePath",$out);
        $_SESSION['removeBLAST'] = 'no';
      }
      else{
        $_SESSION['databaseAfterRemove']='no';
        $_SESSION['removeBLAST'] = 'yes';
        $runScripts='yes';
      }
    }
    else $_SESSION['removeBLAST'] = 'no';


    if(isset($_POST['searchbox'])) {
      if ($_SESSION['inter-bygene'] == 'yes' || $_SESSION['inter-byfunction']=='yes') $runScripts='yes';
      else if (count($_SESSION['array_path[]'])<2);
      else if (count($_SESSION['array_path[]'])>1 && $_SESSION['alreadyshownmodal']=='no' && $_SESSION['showModalComp'] == 'no'){
        $_SESSION['showModalComp'] = 'yes';
      }
      else if ($_SESSION['showModalComp'] == 'yes'){
        $_SESSION['alreadyshownmodal']='yes';
        $_SESSION['showModalComp'] = 'no';
      }


      if (count($_SESSION['ArrayBLAST[]'])>0){
        $wherePath=$_SESSION['userPath'];
        exec("python makeComparisons/makeImportsNullAfterBLAST.py $wherePath",$out);
      }
      $_SESSION['ArrayBLAST[]']=array();
      $_SESSION["SearchByBLAST"]="no";
      $_SESSION['searchBySequence']='no';
      $_SESSION['Numdatabasesearch']=0;
      $_SESSION['identities']=null;
      $_SESSION['prevQueryGene']='null';
      $_SESSION['string_database']=null;
      $search_term = $_POST['searchbox'];  
      $remove_hypo='undefined';
      $search_term=trim($search_term);
      $search_term = preg_replace('/\s+/', '---', $search_term);
      $_SESSION['prevsearchterm'] = $search_term;
      $_SESSION['searchbox'] = 'yes';
    }
    else if ($_SESSION['showModalComp'] == 'yes'){
        $_SESSION['alreadyshownmodal']='yes';
        $_SESSION['showModalComp'] = 'no';
      }


    if (isset($_POST['removeselection'])){
      $_SESSION['selectionArray']=null;
    }

    if(isset($_POST['show_hypothetical'])) {
      $_SESSION['show_hypothetical'] = 'yes';
    }
    else if (!isset($_SESSION['show_hypothetical'])) $_SESSION['show_hypothetical'] = 'no';
    else if (isset($_POST['hide_hypothetical'])) $_SESSION['show_hypothetical'] = 'no';

    if(isset($_POST['typesearch'])) {
          $_SESSION['searchBySequence']='no';
          $typesearch_array[sizeof($typesearch_array)] = $_POST['typesearch'];
          $_SESSION['typesearch[]'] = $typesearch_array;
          $_SESSION['prevsearchtype'] = $_POST['typesearch'];
          $_SESSION['genomesearch'] = $_POST['genomesearch'];
        //header('Location: searchWithContigs.php');
    }
    $typesearch_string = implode('.', $typesearch_array);

    if (isset($_POST['referenceGenome'])){
      $_SESSION['searchBySequence']='no';
      $_SESSION['searchArray[]']=null;
      $_SESSION["identities"]=null;
      $_SESSION['string_array']="null";
      $_SESSION['string_database']=null;
      $_SESSION['prevQueryGene']='null';
      $_SESSION['Numdatabasesearch']=0;
      $referenceGenome="uploads/".$_SESSION['userPath']."/input_files/".$_POST['referenceGenome'];
      $queryGenome="uploads/".$_SESSION['userPath']."/input_files/".$_POST['queryGenome'];
      $pathAligment="uploads/".$_SESSION['userPath']."/alignments/nucmer";
      $pathCoords="uploads/".$_SESSION['userPath']."/alignments/nucmer.coords";
      $pathSNPS="uploads/".$_SESSION['userPath']."/alignments/nucmer.snps";
      $runScripts='yes';
    }
    if(isset($_SESSION['genomesearch'])){
      $genomesearch=$_SESSION['genomesearch'];
    }

    if(isset($_POST['ElementIDposition'])){
      $positionElement=$_POST['ElementIDposition'];
    }


    if(!isset($_POST['searchbox'])) {
        $search_term=null;
    }
    if(isset($_POST['remove_hypo'])){
          $remove_hypo=$_POST['remove_hypo'];
    }

    if (isset($_POST['remove_hypothetical'])){
             $remove_hypo=$_POST['remove_hypothetical'];          
    }
    if (isset($_POST['add_hypothetical'])){
             $remove_hypo=$_POST['add_hypothetical'];       
    }

    if(isset($_POST['searchArray'])) {

        if(!isset($_POST['searchbox'])) {
           $search_array = $_SESSION['searchArray[]']; 
           if(!isset($search_array[0])){
            $string_array = 'null';
            $_SESSION['string_array']  = $string_array;
            }
           else {
            $string_array = implode('.', $search_array);
            $_SESSION['string_array']  = $string_array;
          }
        }
        else{
           $search_array = $_SESSION['searchArray[]'];
           array_push($search_array, $search_term); 
           $string_array = implode('.', $search_array); 
           $_SESSION['string_array']  = $string_array;
        }
        
    }
    else {
      if(isset($_POST['removeAll'])){
          $_SESSION["SearchByBLAST"]="no";
          $_SESSION['searchBySequence']='no';
          $_SESSION['ArrayBLAST[]']=array();
          $_SESSION['searchLengthArray']=null;
          $_SESSION['alignment_position']=null;
          $_SESSION['alignScore']=null;
          $_SESSION['refStart']=null;
          $_SESSION['subEnd']=null;
          $_SESSION['seqQuery']=null;
          $_SESSION['seqsub']=null;
          $_SESSION['seqmatch']=null;
          $_SESSION['string_database']=null;
          $_SESSION['string_array']=null;
          $_SESSION['identifiers']=null;
          $string_array='null';
          $search_array=null;
          unset($_SESSION['searchArray[]']);
          unset($_SESSION['typesearch[]']);
          $wherePath=$_SESSION['userPath'];
          exec("python makeComparisons/makeImportsNullAfterBLAST.py $wherePath",$out);
          //header("Location:searchWithContigs.php");
        }
      else if (isset($_POST['removesearch']) and isset($_POST['caminhosearch'])){

        if(isset($_POST['removeAll']));
        else{
        
          $element_remove= $_POST['removesearch'];
          $path_remove= $_POST['caminhosearch'];
          $removeTypeSearch = $_SESSION['typesearch[]'];
          unset($path_remove[$element_remove]);
          unset($removeTypeSearch[$element_remove]);

          $search_array = array_values($path_remove);
          $typesearch_array = array_values($removeTypeSearch);

          if(!isset($search_array[0])) {
            $string_array = 'null';
            $typesearch_string = '';
            $_SESSION["SearchByBLAST"]="no";
            $_SESSION['searchBySequence']='no';
            $_SESSION['searchBySequence']='no';
            $_SESSION['ArrayBLAST[]']=array();
            $_SESSION['searchLengthArray']=null;
            $_SESSION['alignment_position']=null;
            $_SESSION['alignScore']=null;
            $_SESSION['refStart']=null;
            $_SESSION['subEnd']=null;
            $_SESSION['seqQuery']=null;
            $_SESSION['seqsub']=null;
            $_SESSION['seqmatch']=null;
            $_SESSION['string_database']=null;
            $_SESSION['string_array']=null;
            $string_array='null';
            $search_array=null;
            unset($_SESSION['searchArray[]']);
            unset($_SESSION['typesearch[]']);
            $_SESSION['string_array']  = $string_array;
            $_SESSION['typesearch[]'] = $typesearch_array;
          }
          else {
            $typesearch_string = implode('.', $typesearch_array);
            $string_array = implode('.', $search_array);
            $_SESSION['string_array']  = $string_array;
            $_SESSION['typesearch[]'] = $typesearch_array;
          }
          //header("Location:searchWithContigs.php");
        }


      }
      else{
        if ($search_term==null) {
          if (isset($_POST['TrySearchArray'])) {
            if($string_array != ''); 
            else $string_array='null';
            
          }
        }
        else{ 
              if (isset($_POST['TrySearchArray']));
              else{
                if(isset($_SESSION['searchArray[]']));
                else $search_array=array();
                array_push($search_array, $search_term);
                $string_array = implode('.', $search_array);
                $_SESSION['string_array']  = $string_array;
              }

        }
             
      }
    }

    if (isset($_POST['positionToBe'])) $_SESSION['remakeComparisons']='yes';
    else $_SESSION['remakeComparisons']='no';

    if (isset($_POST['positionToBe'])){
        $currentPos = $_POST["currentPosition"];
        $_SESSION['currentPos']=$currentPos;
        $elementToChange = $array_path[$currentPos];
        $positionToBe = $_POST["positionToBe"];
        $_SESSION['positionToBe']=$positionToBe;
        $otherElement = $array_path[$positionToBe];
        $array_path[$positionToBe] = $elementToChange;
        $array_path[$currentPos] = $otherElement;

        if (isset($_POST["hasSearch"])) {
            $string_array=$_SESSION['string_array'];
        }

        $_SESSION['array_path[]']=$array_path;
        
        $runScripts='yes';
      }

    if (isset($_POST['inter-bygene']) or isset($_POST['inter-byfunction'])) {
      $runScripts='yes';
      $string_array=$_SESSION['string_array'];
      $_SESSION['compNull'] = 'no';
    }

    if (isset($_POST['exportGenome'])){
      $runScripts='yes';
      $exportGenome1=$_POST['exportGenome'];
      $parts=explode('...',$exportGenome1);
      $exportGenome=$parts[0];
      $exportFile=$parts[1];
      $partsFile=explode('/',$exportFile);
      $fileNameToExport=$partsFile[count($partsFile)-1];
      $justN=explode('.',$fileNameToExport);
      $justName=$justN[0];
      $exportType=$_POST['ExportType'];
    }

    if (isset($_POST['exportContig'])){
      $runScripts='yes';
      $exportContig=$_POST['contigToExport'];
      $exportgenome=$_POST['GenomeToExport'];
      $exportType=$_POST['ExportType'];
      $posGinteger=intval($exportGenome);
      $exportFile=$_SESSION['array_path[]'][$posGinteger];
      $partsFile=explode('/',$exportFile);
      $fileNameToExport=$partsFile[count($partsFile)-1];
      $justN=explode('.',$fileNameToExport);
      $justName=$justN[0];
      $Contigexp='yes';
    }



    $num_files= count($array_path);

    for($i=0; $i < count($_SESSION['array_path[]']);$i++){
      $filesNames = $filesNames.$_SESSION['array_path[]'][$i].'---';
    }

    if (isset($_POST['selectionToExport'])){
      $runScripts='yes';
    }

    if (isset($_POST['GetSequence'])){
      $runScripts='no';
      $ModalSequence='yes';
    }
    else $ModalSequence='no';

    if (isset($_POST['DetectSNPS'])){
      $runScripts='no';
      $ShowSNP='yes';
    }
    else $ShowSNP='no';


    if(isset($_POST['SearchForSequence'])) {
        $wherePath=$_SESSION['userPath'];
        $search_sequence = $_POST['SeqToSearch'];  
        $search_sequence = preg_replace('/\s+/', '', $search_sequence);
        $identifier='...'.$_POST['identifierS']; 
        if($_POST['edit_EvalueS']=='') $evalue=0.001;
        else $evalue=$_POST['edit_EvalueS'];
        if($_POST['Min_AlignS']=='') $MinAlign=300;
        else $MinAlign=$_POST['Min_AlignS'];
        $refgenome=$_POST['GenomeToSearch'];
        exec("python makeComparisons/database_search_inputSeq.py $search_sequence $refgenome $evalue $MinAlign $wherePath",$out);
        array_push($_SESSION['ArrayBLAST[]'], $identifier);
        $_SESSION["SearchByBLAST"]="yes";
        $outGenesS=$out[0];
        if ($outGenesS!=null){
          $numOutGenes=explode('---',$outGenesS);
          $Indentifiers="";
          if ($_SESSION['identifiers']==null){
            $_SESSION['identifiers']=array();
            for($i=0; $i < count($numOutGenes);$i++){
              $Indentifiers=$Indentifiers.$identifier.'---';
            }
            $Indentifiers=trim($Indentifiers,'---');
            array_push($_SESSION['identifiers'],$Indentifiers);
          }
          else{
            for($i=0; $i < count($numOutGenes);$i++){
              $Indentifiers=$Indentifiers.$identifier.'---';
            }
            $Indentifiers=trim($Indentifiers,'---');
            array_push($_SESSION['identifiers'],$Indentifiers);
          }
          if ($_SESSION['searchLengthArray']==null){
            $_SESSION['searchLengthArray']=array();
            array_push($_SESSION['searchLengthArray'],$out[1]);
          }
          else{
            array_push($_SESSION['searchLengthArray'],$out[1]);
          }
          if ($_SESSION['alignment_position']==null){
            $_SESSION['alignment_position']=array();
            array_push($_SESSION['alignment_position'],$out[2]);
          }
          else{
            array_push($_SESSION['alignment_position'],$out[2]);
          }
          if ($_SESSION['alignScore']==null){
            $_SESSION['alignScore']=array();
            array_push($_SESSION['alignScore'],$out[3]);
          }
          else{
            array_push($_SESSION['alignScore'],$out[3]);
          }
          if ($_SESSION['refStart']==null){
            $_SESSION['refStart']=array();
            array_push($_SESSION['refStart'],$out[4]);
          }
          else{
            array_push($_SESSION['refStart'],$out[4]);
          }
          if ($_SESSION['subEnd']==null){
            $_SESSION['subEnd']=array();
            array_push($_SESSION['subEnd'],$out[5]);
          }
          else{
            array_push($_SESSION['subEnd'],$out[5]);
          }
          if ($_SESSION['seqQuery']==null){
            $_SESSION['seqQuery']=array();
            array_push($_SESSION['seqQuery'],$out[6]);
          }
          else{
            array_push($_SESSION['seqQuery'],$out[6]);
          }
          if ($_SESSION['seqsub']==null){
            $_SESSION['seqsub']=array();
            array_push($_SESSION['seqsub'],$out[7]);
          }
          else{
            array_push($_SESSION['seqsub'],$out[7]);
          }
          if ($_SESSION['seqmatch']==null){
            $_SESSION['seqmatch']=array();
            array_push($_SESSION['seqmatch'],$out[8]);
          }
          else{
            array_push($_SESSION['seqmatch'],$out[8]);
          }

          if ($_SESSION['string_database']==null){
              $_SESSION['string_database']=array();

              array_push($_SESSION['string_database'],$outGenesS);
          }
          else{
              array_push($_SESSION['string_database'],$outGenesS);
          }
        }
        else $showModalNoMatch='yes';

    }


    ?>

<!--#######################################################END OF PHP POST AND SESSIONS DEALING#####################################-->

  <body style="">
    <div id="contextMenu">    
    </div>
    <div id="contextMenu2">    
    </div>

    <!-- Fixed navbar -->
    <div class="navbar navbar-inverse navbar-fixed-top">
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="#">ProGenViZ</a>
        </div>
        <div class="navbar-collapse collapse">
          <ul class="nav navbar-nav">
            <li class="active"><a href="index.php">Home</a></li>
            <li class="dropdown">
                  <a href="#" class="dropdown-toggle" data-toggle="dropdown">Help<b class="caret"></b></a>
                  <ul class="dropdown-menu">
                    <li><a href="Tutorial.php">Tutorial</a></li>
                    <li class="divider"></li>
                    <li><a href="TestFiles.php">Test Files</a></li>
                  </ul>
                </li>
            <li><a href="About.php">About</a></li>
            <li><a href="Contact.php">Contacts</a></li>
            </ul></div></div></div>

            <div id="sidebar-wrapper">
        <ul class="sidebar-nav">
          <li class="sidebar-brand" id="brand" style="color:white">Actions</li>
          <li><a href="#" data-toggle="modal" data-target="#myModalInfo">More Info</a></li>
          <li><a href="#" data-toggle="modal" data-target="#myModalAdd">Add more files to compare</a></li>
          <li><a href="#" data-toggle="modal" data-target="#myModalRemove">Remove files</a></li>
          <li><a href="#" data-toggle="modal" data-target="#myModalCompare">Comparison methods</a></li>
          <li><a href="#" data-toggle="modal" data-target="#myModalAddEx">Add/Exclude</a></li>
          <li><a href="#" data-toggle="modal" data-target="#myModalHideShow">Hide/Show</a></li>
          <?php
            $hasContigFile='no';
            for ($i=0;$i<count($_SESSION['arrayContigs']);$i++){
              if($_SESSION['arrayContigs'][$i]=='yes') $hasContigFile='yes';
            }
            if ($hasContigFile=='yes' && count($_SESSION['array_path[]'])>1){
              echo '<li><a href="#" data-toggle="modal" data-target="#myModalAlign">Order Contigs</a></li>';
            }
          ?>
          <li><a href="#" data-toggle="modal" data-target="#myModalExport">Export Image</a></li>
          <li><a href="#" data-toggle="modal" data-target="#myModalExportGff">Export Files</a></li>
          <li><a href="#" data-toggle="modal" data-target="#myModaldashboard">Statistics</a></li>
          <form id="svgform" method="post" action="cgi-bin/exports.pl">
              <input type="hidden" id="output_format" name="output_format" value="">
              <input type="hidden" id="data" name="data" value="">
          </form>
          <!--<li><hr></hr></li>
          <li><a href="#" data-toggle="modal" data-target="#GeneTable">Table of Genes</a></li>-->
          <li><hr></hr></li>
          <li class="sidebar-brand" id="brand" style="color:white">Search</li>
          
            <!--###########SEARCHES AND VISUALIZATION MODE CHOOSING##############################-->
    
            <?php

            if (isset($_POST['align'])) $align = $_POST['align']; 
            else{
              $align = null;
            }

              echo '<form name="searchForm" enctype="multipart/form-data" action="searchWithContigs.php" method="POST" onsubmit="return validateFormSearch()">';

              echo '<select class="form-control" name="genomesearch">
                        <option value="allgenome"/>All Genomes';
              $numgenomes=count($_SESSION['array_path[]']);
              if ($numgenomes>1){
                for($i=0; $i < $numgenomes;$i++){
                      echo '<option value="'.($i+1).'"/>Genome '.($i+1);
                }
              }
    
              echo '</select>';

              echo '<select class="form-control" name="typesearch">
                      <option value="GeneName"/>Gene Name
                      <option value="GeneProduct"/>Gene Product
                      <option value="Begin-End"/>Begin - End
                    </select>';

              echo' <input type="text" name= "searchbox">
                    <input type="submit" class="btn btn-primary" name="search-button" value="Search" />
                    </form>';
                        

            ?>
            <li><a href="#" data-toggle="modal" data-target="#myModalSearchForSequence">Search By Sequence</a></li>
            <li><a href="#" data-toggle="modal" data-target="#myModalSearchMade">Searches Made</a></li>
            <li><a href="#" data-toggle="modal" data-target="#SearchTable">Table of Hits</a></li>
            <li><hr></hr></li>
             <li><a>
            <?php 


        if(isset($_POST['linearView'])){
          $_SESSION['linearMode'] = 'no';
          $_SESSION['editInfo'] = $_POST['edInfo'];
        }
        if(isset($_POST['hiveView'])){
          $_SESSION['linearMode'] = 'yes';
          $_SESSION['editInfo'] = $_POST['edInfo'];
        }

        if($_SESSION['linearMode'] == 'yes'){
          echo '<form enctype="multipart/form-data" action="searchWithContigs.php" method="POST">
                    <input type="submit" class ="btn-link" name="linearView" value="Change to Hive Plot View"/>
                    <input type="hidden"  name="edInfo" value="'.$_SESSION['editInfo'].'"/>';

          foreach($search_array as $value) {
                      echo '<input type="hidden" name="searchArray[]" value="'. $value. '">';
                    }
          if (isset($_POST['selectionArray'])){
                  $array=$_SESSION['selectionArray'];
                  echo "<input type='hidden' name='selectionArray' value='".$array. "'>
                        <input type='hidden' name='remove_selection'>";
          }
                echo'</form> ';
        }
        else{
          echo '<form enctype="multipart/form-data" action="searchWithContigs.php" method="POST">
                    <input type="submit" class ="btn-link" name="hiveView" value="Change to Linear View"/>
                    <input type="hidden"  name="edInfo" value="'.$_SESSION['editInfo'].'"/>';
          foreach($search_array as $value) {
                echo '<input type="hidden" name="searchArray[]" value="'. $value. '">';
          }
          if (isset($_POST['selectionArray'])){
                  $array=$_SESSION['selectionArray'];
                  echo "<input type='hidden' name='selectionArray' value='".$array. "'>
                        <input type='hidden' name='remove_selection'>";
                
                  
          }
          echo'</form> ';
                
        }
      ?>

      <!--###########END OF SEARCHES AND VISUALIZATION MODE CHOOSING##############################-->

    <li></a>
    <li><a id="buttonSelPos"></a></li>
            <?php
              if (isset($_POST['remove_selection']) || $_SESSION['selectionArray']!=''){
                echo '<li><hr></hr></li>';
                echo '<li><form enctype="multipart/form-data" action="searchWithContigs.php" method="POST">
                        <input type="submit" class ="btn-link" name="removesel" value="Remove Selection" />
                        <input type="hidden" name="removeselection"/>';
                echo'</form></li>';
              }
            ?>
          </a></li>
          </li>
    <li><hr></hr></li>
    <li style="color:white">Comparison method in use: 
    <?php

      if($_SESSION['inter-bygene']=='yes') echo '<li style="color:white">Gene Name - next position Genome</li>';
      else if($_SESSION['inter-byfunction']=='yes') echo '<li style="color:white">Function - next position Genome</li>';
      else echo '<li style="color:white">None</li>';

    ?>
    </li>
    <li><hr></hr></li></ul></div>


    <li></li>   


    <!--VISUALIZATION LOCATION-->

     <div id="chart-position">
      <div id='demo_2'>
    <span class='notes'></span>
      </div>
    
      <div id='demo_2'>

            <span class='chart' oncontextmenu="return false;">&nbsp;</span>
 
      </div>
</div>



    <!--####################################################INPUT PROCESSING########################################################-->

   <?php


    $wherePath=$_SESSION['userPath'];
    if($runScripts!=null){
      $num_filesArray = count($array_path);
    $path_exec = "";
    for ($i=0; $i<$num_filesArray;$i++){  
      $path_exec = $path_exec.$array_path[$i].' ';

    }

    if ($_SESSION['remakeComparisons']=='yes'){
        $currentPos=$_SESSION['currentPos'];
        $positionToBe=$_SESSION['positionToBe'];
        $stringPos=(string)(intval($currentPos)+1);
        $stringToBe=(string)(intval($positionToBe)+1);
        $toChange=$stringPos."...";
        $toBe=$stringToBe."...";
        for($i=0; $i < count($_SESSION['string_database']); $i++){
          $GenomeInUse= explode('...', $_SESSION['string_database'][$i]);
          if ($GenomeInUse[0]==$stringPos){
            $_SESSION['string_database'][$i]= str_replace($toChange, $toBe, $_SESSION['string_database'][$i]);
          }
          if ($GenomeInUse[0]==$stringToBe){
            $_SESSION['string_database'][$i]= str_replace($toBe, $toChange, $_SESSION['string_database'][$i]);
          }
        }
        exec("python parsers/ChangePosition.py $wherePath $currentPos $positionToBe");
        $_SESSION['currentPos']=null;
        $_SESSION['positionToBe']=null;
    }

    else if (isset($_POST['selectionToExport'])){

    $genomeToExport=$_POST['genomeToExport'];
    $selectionToExport=$_POST['selectionToExport'];
    $contigNumber=$_POST['contigNumber'];
    $modalDownloadExport='yes';
    exec("python parsers/exportGFFPlusSequence.py $wherePath $genomeToExport $contigNumber $selectionToExport");

    }

    else{


    if($_SESSION['editInfo']=='yes'){
      $genomeToChange= explode('...', $nameToChange);
      $fileToChange=$array_path[intval($genomeToChange[0])-1];
      exec("python parsers/edit_infoWithContigs.py $wherePath $fileToChange $nameToChange $editName $productToChange $editProduct $geneBegin");
    }
    else if ($_SESSION['removeBLAST'] == 'yes'){
      $_SESSION['removeBLAST'] = 'no';
      exec("python makeComparisons/removeSearchBySequenceWithContigs.py $wherePath $geneThatImports");
    }
    else if (isset($_POST['exportGenome'])){
      $modalDownloadExport='yes';
      $RegionsToExport=$_SESSION["ContigsToExport"];
      #echo "<div id='check-upload'>".$wherePath."</div>";
      #echo "<div id='check-upload'>".$exportGenome."</div>";
      #echo "<div id='check-upload'>".$exportType."</div>";
      #echo "<div id='check-upload'>".$justName."</div>";
      #echo "<div id='check-upload'>".$RegionsToExport."</div>";
      exec("python parsers/createGFFfile.py $wherePath $exportGenome $exportType $justName $RegionsToExport",$moreContig);
      $moreContigs=$moreContig[0];
    }
    else if (isset($_POST['GetSequence'])){
      $seqRef=$_POST['geneReference'];
      $queryGe=$_POST['queryGene'];
      exec("python parsers/SearchSequence.py $wherePath $seqRef $queryGe");
    }


    else if (isset($_POST['DetectSNPS'])){
      $querySeq=$_POST["sequenceQueryToSee"];
      $subjectSeq=$_POST["sequenceTargetToSee"];
      $sourceGeneName=$_POST["nameSource"];
      $targetGeneName=$_POST["nameTarget"];
      $matchSeq=$_POST["matchesToSee"];
      $pathWhere=$_SESSION['userPath'];
      exec("python parsers/createFastaFile.py $pathWhere $sourceGeneName $querySeq");
      exec("python parsers/createFastaFile.py $pathWhere $targetGeneName $subjectSeq");
      $referenceSequence="uploads/".$_SESSION['userPath']."/Sequence_files/".$targetGeneName.'.fasta';
      $querySequence="uploads/".$_SESSION['userPath']."/Sequence_files/".$sourceGeneName.'.fasta';
      $pathAligment="uploads/".$_SESSION['userPath']."/alignments/nucmer";
      $pathCoords="uploads/".$_SESSION['userPath']."/alignments/nucmer.coords";
      $pathSNPS="uploads/".$_SESSION['userPath']."/alignments/nucmer.snps";
      $execution="nucmer -p ".$pathAligment." ".$referenceSequence." ".$querySequence;
      exec($execution);
      $pathAligment=$pathAligment.".delta";
      $execution2="show-snps -Clr ".$pathAligment." > ".$pathSNPS;
      exec($execution2);
      exec("python parsers/GetSNPs.py $pathSNPS",$locations);
      $SNPs=explode('---',$locations[0]);
      unlink($referenceSequence);
      unlink($querySequence);

    }
    else{
    
      if (isset($_POST['referenceGenome'])){
        $refGen=$_POST['referenceGenome'];
        $queryGen=$_POST['queryGenome'];
        if($_POST['minAlignment']=='') $minAlignment=500;
        else $minAlignment=$_POST['minAlignment'];
        if($_POST['minidentity']=='') $minidentity=0.98;
        else $minidentity=$_POST['minidentity'];
        $minidentity1=intval($minidentity);
        $minidentity3=parse_str($minidentity1*100);
        $parts=explode('---',$refGen);
        $genome=$parts[0];
        $PathRef=$parts[1];
        $partToChange=explode(".",$PathRef);
        $partToChange=".".$partToChange[1];
        exec("python parsers/FastaFromInput.py $PathRef $genome");
        $PathRef=str_replace($partToChange, '.ffn', $PathRef);
        $parts=explode('---',$queryGen);
        $genome=$parts[0];
        $PathQuery=$parts[1];
        $partToChange=explode(".",$PathQuery);
        $partToChange=".".$partToChange[1];
        exec("python parsers/FastaFromInput.py $PathQuery $genome");
        $PathQuery=str_replace($partToChange, '.ffn', $PathQuery);
        $execution="nucmer -p ".$pathAligment." ".$PathRef." ".$PathQuery;
        exec($execution);
        $ntrefPath="uploads/".$wherePath."/alignments/nucmer.ntref";
        if (file_exists($ntrefPath)){
          $ShowModalErrorDuringAlign='yes';
        }
        else{
         $pathAligment=$pathAligment.".delta";
         $pathDeltaF="uploads/".$_SESSION['userPath']."/alignments/nucmerFiltered.delta";
         $execution="delta-filter -i ".$minidentity." -l ".$minAlignment." ".$pathAligment." > ".$pathDeltaF;
         exec($execution);
         $execution="show-coords -r -c -l ".$pathDeltaF." > ".$pathCoords;
         exec($execution);
         exec("python makeComparisons/OrganizeContigs.py $wherePath $pathCoords");
        }
      }

      if(isset($_POST['referenceGenome'])){
          exec("python parsers/setContigs.py $wherePath");
          exec("python parsers/getSizeWithContigs.py $wherePath");
          exec("python makeComparisons/makeImportsNullWithContigs.py $wherePath");
          $_SESSION['compNull'] = 'yes';
          $_SESSION['inter-bygene'] = 'no';
          $_SESSION['inter-byfunction'] = 'no';
          $_SESSION['searchbox'] = 'no';
      }

      

      if($_SESSION['rundatabasesearch']=='yes'){
      $_SESSION['typesearch[]']=null;
      $isSearchSequence='yes';
      $querygene=$_POST['querygene'];
      $querygenome=explode('...', $querygene);
      $typefilequery=$array_path[intval($querygenome[0])-1];
      $querytype=explode('.', $typefilequery);
      $geneReference=$_POST['geneReference'];
      $geneBegin=$_POST['geneBegin'];
      $geneEnd=$_POST['geneEnd'];
      $refgen=$_POST['refgenome'];
      $refgenome=$refgen.'...';
      $indexarraypath=$_POST['refgenome'];
      $filedb=$array_path[intval($_POST['refgenome'])-1];
      $typefile=explode('.', $filedb);
      $prevQuerygene=$_SESSION['prevQueryGene'];
      if($_SESSION['searchNCBI']=='yes') {
          exec("python parsers/SearchSequence.py $wherePath $geneReference");
          $fileSequence='uploads/'.$wherePath.'/'.$wherePath.'_sequence.fasta';
          $_SESSION['NCBISearch']='yes';
          $_SESSION['geneSequenceNCBI']=$fileSequence;
        }
      else{
      if ((strpos($typefilequery, '.fa') || strpos($typefilequery, '.gbk') || strpos($typefilequery, '.fasta')) && (strpos($filedb, '.fa') || strpos($filedb, '.gbk') || strpos($filedb, '.fasta'))  && $_SESSION['AnnotateRegion']!='yes'){
      if ($prevQuerygene!=$querygene){
        if($_SESSION['searchNCBI']=='yes') {
          exec("python parsers/SearchSequence.py $wherePath $geneReference");
          $fileSequence='uploads/'.$wherePath.'/'.$wherePath.'_sequence.fasta';
          $_SESSION['NCBISearch']='yes';
          $_SESSION['geneSequenceNCBI']=$fileSequence;
        }
        else{
          $_SESSION['NCBISearch']='no';
          exec("python parsers/SearchSequence.py $wherePath $geneReference $querygene");
          if($_POST['edit_Evalue']=='') $evalue=0.001;
          else $evalue=$_POST['edit_Evalue'];
          if($_POST['edit_Align']=='') $MinAlign=300;
          else $MinAlign=$_POST['edit_Align'];
          $partsG = explode("...", $querygene);
          $fileSequence='uploads/'.$wherePath.'/Sequence_files/'.$partsG[1].'_sequence.fasta';
          exec("python makeComparisons/database_search.py $querygene $fileSequence $refgenome $evalue $MinAlign $wherePath",$out);
          array_push($_SESSION['ArrayBLAST[]'], $querygene);
          $_SESSION['prevQueryGene']=$querygene;
          $outGenes=$out[0];
          if ($outGenes!=null){
          $numOutGenes=explode('---',$outGenes);
          $Indentifiers="";
          if ($_SESSION['identifiers']==null){
            $_SESSION['identifiers']=array();
            for($i=0; $i < count($numOutGenes);$i++){
              $Indentifiers=$Indentifiers.$querygene.'---';
            }
            $Indentifiers=trim($Indentifiers,'---');
            array_push($_SESSION['identifiers'],$Indentifiers);
          }
          else{
            for($i=0; $i < count($numOutGenes);$i++){
              $Indentifiers=$Indentifiers.$querygene.'---';
            }
            $Indentifiers=trim($Indentifiers,'---');
            array_push($_SESSION['identifiers'],$Indentifiers);
          }
          if ($_SESSION['searchLengthArray']==null){
            $_SESSION['searchLengthArray']=array();
            array_push($_SESSION['searchLengthArray'],$out[1]);
          }
          else{
            array_push($_SESSION['searchLengthArray'],$out[1]);
          }
          if ($_SESSION['alignment_position']==null){
            $_SESSION['alignment_position']=array();
            array_push($_SESSION['alignment_position'],$out[2]);
          }
          else{
            array_push($_SESSION['alignment_position'],$out[2]);
          }
          if ($_SESSION['alignScore']==null){
            $_SESSION['alignScore']=array();
            array_push($_SESSION['alignScore'],$out[3]);
          }
          else{
            array_push($_SESSION['alignScore'],$out[3]);
          }
          if ($_SESSION['refStart']==null){
            $_SESSION['refStart']=array();
            array_push($_SESSION['refStart'],$out[4]);
          }
          else{
            array_push($_SESSION['refStart'],$out[4]);
          }
          if ($_SESSION['subEnd']==null){
            $_SESSION['subEnd']=array();
            array_push($_SESSION['subEnd'],$out[5]);
          }
          else{
            array_push($_SESSION['subEnd'],$out[5]);
          }
          if ($_SESSION['seqQuery']==null){
            $_SESSION['seqQuery']=array();
            array_push($_SESSION['seqQuery'],$out[6]);
          }
          else{
            array_push($_SESSION['seqQuery'],$out[6]);
          }
          if ($_SESSION['seqsub']==null){
            $_SESSION['seqsub']=array();
            array_push($_SESSION['seqsub'],$out[7]);
          }
          else{
            array_push($_SESSION['seqsub'],$out[7]);
          }
          if ($_SESSION['seqmatch']==null){
            $_SESSION['seqmatch']=array();
            array_push($_SESSION['seqmatch'],$out[8]);
          }
          else{
            array_push($_SESSION['seqmatch'],$out[8]);
          }
        }
        }
      }
      else $outGenes=null;
      if($outGenes!=null && $outGenes!='not exists'){
        if($_SESSION['searchNCBI']=='yes');
        else{
       if (($_SESSION['Numdatabasesearch']==0 || !isset($_SESSION['Numdatabasesearch'])) && $_SESSION['databaseAfterRemove']=='yes'){
        if (!isset($_SESSION['Numdatabasesearch'])) $_SESSION['Numdatabasesearch']=1;
        else $_SESSION['Numdatabasesearch']+=1;
        exec("python makeComparisons/makeImportsBySearchSequenceWithContigsFirstTime.py $wherePath $querygene $outGenes");
       }
       else{
        exec("python makeComparisons/makeImportsBySearchSequenceWithContigs.py $wherePath $querygene $outGenes");
      }
     }
       if ($_SESSION['string_database']==null){
        $_SESSION['string_database']=array();

        array_push($_SESSION['string_database'],$outGenes);
       }
       else{
        array_push($_SESSION['string_database'],$outGenes);
      }
      }
      else{
        if ($prevQuerygene!=$querygene){
         if ($_SESSION['string_database']==null) $string_array='null';
         else $string_array=$_SESSION['string_database'];
         $showModalNoMatch='yes';
        }
        else{
         $showModalNoMatch='no';
         if ($_SESSION['string_database']==null) $string_array='null';
         else $string_array=$_SESSION['string_database'];
        }
      } 
      }
      else if ($_SESSION['AnnotateRegion']=='yes'){
        $searchBeEnd=$_SESSION['AnnBeginEnd'];
        $searchR=$_SESSION['QueryRegion'];
        $searchR2=explode('...',$searchR);
        $searchRegion=$searchR2[1];
        $pathFile="uploads/".$wherePath."/Search_Results/".$searchRegion."_SearchResults.txt";
        if (file_exists ( $pathFile )){
          $pathToSequence="uploads/".$wherePath."/Sequence_files/".$searchRegion."_sequence.fasta";
          $geneBegin=$_POST['geneBegin'];
          $geneEnd=$_POST['geneEnd'];
          exec("python parsers/AddTail.py $wherePath $pathToSequence");
          $path = "cd Prodigal/Prodigal-2.60 && ./prodigal -i ../../uploads/".$wherePath."/Sequence_files/".$searchRegion."_sequence.fasta -c -m -g 11 -p single -f sco -q > ../../uploads/".$wherePath."/Prodigal_results/".$searchRegion."_Presults.txt";
          exec("$path");
          exec("python parsers/AnnotateRegion.py $wherePath $searchRegion $num_filesArray $geneBegin $geneEnd",$contigToExport);
          $Topass=$searchR2[0].'...'.$contigToExport[0];
          $pos=strpos($_SESSION["ContigsToExport"],$Topass);
          if ($pos===false) $_SESSION["ContigsToExport"]=$_SESSION["ContigsToExport"].$Topass.'---';
          exec("python parsers/setContigs.py $wherePath");
          exec("python parsers/getSizeWithContigs.py $wherePath");
          exec("python makeComparisons/makeImportsNullWithContigs.py $wherePath");
          $_SESSION['searchBySequence']='no';
          $_SESSION["identities"]=null;
          $_SESSION['string_array']="null";
          $_SESSION['string_database']=null;
          $_SESSION['prevQueryGene']='null';
          $_SESSION['Numdatabasesearch']=0;
          $_SESSION['compNull'] = 'yes';
          $_SESSION['inter-bygene'] = 'no';
          $_SESSION['inter-byfunction'] = 'no';
          $_SESSION['searchbox'] = 'no';
        }
        else{
          $showModalAnnotateError='yes';
        }
      }
      else $showmodalGFFBLAST='yes';
      

    }
  }
    else{     

      if($_SESSION['inter-bygene']=='yes'){ 
        if($_SESSION['addAfterSearch']=='yes'){
         exec("python parsers/makeSizeFileAfterSearch.py $wherePath");
         $_SESSION['addAfterSearch']=null;
        }
        exec("python makeComparisons/makeImportsByGeneNameWithContigs.py $wherePath $string_array $num_filesArray");
        $_SESSION['compNull'] = 'no';
        $_SESSION['inter-bygene'] = 'yes';
        $_SESSION['inter-byfunction'] = 'no';
        $_SESSION['searchbox'] = 'no';
      }
      else if($_SESSION['inter-byfunction']=='yes'){ 
        if($_SESSION['addAfterSearch']=='yes'){
         exec("python parsers/makeSizeFileAfterSearch.py $wherePath");
         $_SESSION['addAfterSearch']=null;
        }
        exec("python makeComparisons/makeImportsByFunctionWithContigs.py $wherePath $string_array $num_filesArray");
        $_SESSION['compNull'] = 'no';
        $_SESSION['inter-bygene'] = 'no';
        $_SESSION['inter-byfunction'] = 'yes';
        $_SESSION['searchbox'] = 'no';
      }
      
      else{
        $_SESSION['compNull'] = 'yes';
        $_SESSION['inter-bygene'] = 'no';
        $_SESSION['inter-byfunction'] = 'no';
        $_SESSION['searchbox'] = 'no';
      }
    }
  }
    }
  }

   ?>


 <!--##########JAVASCRIPT SECTION##################-->

  <script> 
  var SelectionArrayMouse= new Array(); 
  var HitsArraySearch = new Array();
  var HitsArraySequence = new Array();
  var InfoArray = new Array();
  var HitsArrayNCBI = new Array();
  </script>

   <script>
   var arr='<?php echo $_SESSION["selectionArray"]; ?>';
   if (arr==''){
    var sel='undefined';
   }
   else var sel=JSON.parse(arr);

   </script>

   <script>
        var search_array= new Array();
        var typesearch_array;
        var wherePath= '<?php echo $wherePath;?>';
        var searchNCBI = '<?php echo $_SESSION["searchNCBI"];?>';
        var isSearchSequence='<?php echo $isSearchSequence;?>';
        var positionElement='<?php echo $positionElement;?>';
        var editInfo='<?php echo $_SESSION["editInfo"];?>';
        var lengthAlignments=['<?php echo implode("---", $_SESSION["searchLengthArray"]) ?>'];
        var alignmentPos=['<?php echo implode("---", $_SESSION["alignment_position"]) ?>'];
        var alignScore=['<?php echo implode("---", $_SESSION["alignScore"]) ?>'];
        var seqSub=['<?php echo implode("...", $_SESSION["seqsub"]) ?>'];
        var seqQuery=['<?php echo implode("...", $_SESSION["seqQuery"]) ?>'];
        var seqmatch=['<?php echo implode("...", $_SESSION["seqmatch"]) ?>'];
        var subEnd=['<?php echo implode("---", $_SESSION["subEnd"]) ?>'];
        var refStart=['<?php echo implode("---", $_SESSION["refStart"]) ?>'];
        var identifiers=['<?php echo implode("---", $_SESSION["identifiers"]) ?>'];
        var showModalGBK='<?php echo $showModalGBK;?>';
        var NCBISearch='<?php echo $_SESSION["NCBISearch"];?>';
        var geneSequenceNCBI='<?php echo $_SESSION["geneSequenceNCBI"];?>';
        var ShowModalErrorDuringAlign='<?php echo $ShowModalErrorDuringAlign;?>';
        var showModalNoMatch='<?php echo $showModalNoMatch;?>';
        var searchBysequence='<?php echo $_SESSION["searchBySequence"];?>';
        var searchByBLAST='<?php echo $_SESSION["SearchByBLAST"];?>';
        var show_hypothetical = '<?php echo $_SESSION["show_hypothetical"];?>';
        var string_array = '<?php echo $string_array;?>';
        var genomesearch = '<?php echo $genomesearch;?>';
        var removehypo =  "<?php echo $remove_hypo;?>";
        var modalDownloadExport="<?php echo $modalDownloadExport;?>";
        var ModalSequence="<?php echo $ModalSequence;?>";
        var ModalSNP="<?php echo $ShowSNP;?>";
        var isSearchMade="<?php echo $_SESSION['SearchMade'];?>";
        var numFilesAfterSearch="<?php echo count($_SESSION['FilesAfterSearch']);?>";
        var ModalAnnotateError="<?php echo $showModalAnnotateError; ?>";
        var pathU="<?php echo $_SESSION['userPath']; ?>";
        var DataTable="";
        var errorUpload="<?php echo $_SESSION['uploadError'];?>";
        var showModalComp="<?php echo $_SESSION['showModalComp'];?>";
        var alreadyshownmodal="<?php echo $_SESSION['alreadyshownmodal'];?>";
        var showmodalGFFBLAST="<?php echo $showmodalGFFBLAST;?>";


        if (string_array=='null' && searchBysequence=='no') search_array=null; 
        else if (searchBysequence=='yes'){

           var string_array=['<?php echo implode("---", $_SESSION["string_database"]) ?>'];
           for (i in string_array){
            search_array.push(string_array[i].split("---"));
           }
          
        }
        else{
         string_array=string_array.replace(/---/g," ");
         search_array = string_array.split(".");
        }
        var inputwhere = '<?php echo $_SESSION["folderPath"]."/".$_SESSION["userPath"]."_input.json"; ?>';

        var typesearch_string = '<?php echo $typesearch_string;?>';
        if (searchBysequence=='yes'){
          typesearch_array= new Array();
          for(i in search_array) typesearch_array.push("GeneName");
        }
        else if (typesearch_string =='') typesearch_array =null;
        else {
              typesearch_array = typesearch_string.split(".");
            }


    </script>

    <script src='data_plot_js/dashboard.js'></script>
   <script src='data_plot_js/lib_dataWithContigs.js'></script>
   <script src="data_plot_js/lib_link.js"></script>
   <script src='data_plot_js/lib_mouse.js'></script>
   
   <?php

    if ($_SESSION['uploadError'] == 'yes'){
         $_SESSION['uploadError'] = 'no';
    }


      if($_SESSION['linearMode'] == 'no'){
        echo '<script src="data_plot_js/modifyBySearchWithContigs.js"></script>';
        echo '<script src="data_plot_js/main.js"></script>';
      }
      else{
        echo '<script src="data_plot_js/modifyBySearchWithContigsNoHive.js"></script>';
        echo '<script src="data_plot_js/mainNoHive.js"></script>';
      }
    ?>

   <script>  
   var align='<?php echo $align;?>';
   var inter_byfunction = '<?php echo $_SESSION["inter-byfunction"];?>';
   var inter_bygene = '<?php echo $_SESSION["inter-bygene"];?>';
   var inter_byfunctionAll = '<?php echo $_SESSION["inter-byfunctionAll"];?>';
   var inter_bygeneAll = '<?php echo $_SESSION["inter-bygeneAll"];?>';
   var fileNames='<?php echo $filesNames;?>';
   var exclude_hypothetical='<?php echo $_SESSION["exclude_hypothetical"];?>';

    function showToUpload() {
        var selected=document.getElementById("inputType").value;
        if (selected=='no'){
          document.getElementById("fileGFF+FASTA").innerHTML="";
          document.getElementById("fileOther").innerHTML="<br>Choose one of the supported file formats (.fasta, .gbk, .gff): <input name='moreuploadedfile[]' type='file' class='btn btn-default'/><br>";
        }
        if (selected=='yes'){
          document.getElementById("fileOther").innerHTML="";
          document.getElementById("fileGFF+FASTA").innerHTML="<br>Choose a GFF file: <input name='moreuploadedfileGFF[]' type='file' class='btn btn-default'/><br>Choose a FASTA file: <input name='moreuploadedfileFASTA[]' type='file' class='btn btn-default'/><br>";
        }
      }

    function validateForm() {
        var y = document.forms["uploadFiles"]["typeUpload"].value;
        if (y =='yes'){
          var XfilesGFF=document.forms["uploadFiles"]["moreuploadedfileGFF[]"].files;
          var XfilesFASTA=document.forms["uploadFiles"]["moreuploadedfileFASTA[]"].files;
          if (XfilesGFF.length==0 || XfilesFASTA.length==0){
            $('#myModalShowErrorTypeUpload').modal('show');
            return false;
          }
          else{
            if ((XfilesFASTA[0].name.search('.fa')==-1 && XfilesFASTA[0].name.search('.fasta')==-1) || XfilesGFF[0].name.search('.gff')==-1) {
              $('#myModalShowErrorTypeUpload').modal('show');
            return false;
            }
          }
      }
        else{
        var Xfiles=document.forms["uploadFiles"]["moreuploadedfile[]"].files;
        if (Xfiles.length==0){
            $('#myModalShowError').modal('show');
            return false;
          }
        else{
          var x =Xfiles[0].name;
          if (x == null || x == "" || (x.search('.fa')==-1 && x.search('.fasta')==-1 && x.search('.gbk')==-1 && x.search('.gff')==-1)) {
              $('#myModalShowError').modal('show');
          return false;
        }
      }
      }
    }

    function validateFormAlign() {
        var minId=document.forms["AlignForm"]["minidentity"].value;
        var minAlign=document.forms["AlignForm"]["minAlignment"].value;
        var referenceGenome=document.forms["AlignForm"]["referenceGenome"].value;
        var queryGenome=document.forms["AlignForm"]["queryGenome"].value;
        var referencePos=referenceGenome.split("---")[0];
        var queryPos=queryGenome.split("---")[0];
        if (referencePos==queryPos){
          $('#myModalShowUndGenomes').modal('show');
          return false;
        }

        if (minId=='' && minAlign=='');
        else if (minId=='' && minAlign!=''){
          minAlign=parseFloat(minAlign);
          if (minAlign<1){
            $('#myModalShowUndValue').modal('show');
            return false;
          }
        }
        else if (minId!='' && minAlign==''){
          minId=parseFloat(minId);
          if ( minId<=0 || minId>0){
            $('#myModalShowUndValue').modal('show');
            return false;
          }
        }
        else{
          minId=parseFloat(minId);
          minAlign=parseFloat(minAlign);
          if (minId>1 || minId<=0 || minAlign<1){
              $('#myModalShowUndValue').modal('show');
              return false;
          }
        } 
    }

      function validateFormSearch() {
        var x = document.forms["searchForm"]["searchbox"].value;
        var y = document.forms["searchForm"]["typesearch"].value;
        x=x.trim();
        if (x == null || x == "") {
            $('#myModalShowErrorSearch').modal('show');
        return false;
        }
        else if (y=='Begin-End'){
          var splitted = x.split("-");
          try{
            var begin = splitted[0].trim();
            var end = splitted[1].trim();
            if (/^\d+$/.test(begin) && /^\d+$/.test(end)){
              if (parseInt(begin)>=parseInt(end)){
                $('#myModalShowErrorSearch').modal('show');
                return false;
              }
            }
            else{
              $('#myModalShowErrorSearch').modal('show');
              return false;
            }
          }
          catch (TypeError){
            $('#myModalShowErrorSearch').modal('show');
            return false;
          }
        }
      }

      function validateFormBLAST() {
        var x = document.forms["formBLAST"]["identifierS"].value;
        var v = document.forms["formBLAST"]["SeqToSearch"].value;
        var y = document.forms["formBLAST"]["edit_EvalueS"].value;
        var z = document.forms["formBLAST"]["edit_MinAlignS"].value;
        x=x.trim();
        y=y.trim();
        z=z.trim();
        if (x == null || x == "" || v=="") {
            $('#myModalSearchForSequence').modal('hide');
            $('#myModalShowIdentifier').modal('show');
        return false;
        }
        if (y=='' && z=='');
        else if (y=='' && z!=''){
          z=parseFloat(z);
          if (z<1){
            $('#myModalSearchForSequence').modal('hide');
            $('#myModalShowUndValueBLAST').modal('show');
            return false;
          }
        }
        else if (y!='' && z==''){
          z=parseFloat(z);
          if ( y<=0){
            $('#myModalSearchForSequence').modal('hide');
            $('#myModalShowUndValueBLAST').modal('show');
            return false;
          }
        }
        else{
          y=parseFloat(y);
          z=parseFloat(z);
          if (y<=0 || z<1){
              $('#myModalSearchForSequence').modal('hide');
              $('#myModalShowUndValueBLAST').modal('show');
              return false;
          }
        } 
      }

      function validateFormBLAST1() {
        var x = document.forms["formBLAST1"]["edit_Evalue"].value;
        var y = document.forms["formBLAST1"]["edit_Align"].value;
        if (x=='' && y=='');
        else if (x=='' && y!=''){
          y=parseFloat(y);
          if (y<1){
            $('#myModalSearchForSequence').modal('hide');
            $('#myModalShowUndValueBLAST').modal('show');
            return false;
          }
        }
        else if (x!='' && y==''){
          x=parseFloat(x);
          if ( x<=0){
            $('#myModalSearchForSequence').modal('hide');
            $('#myModalShowUndValueBLAST').modal('show');
            return false;
          }
        }
        else{
          x=parseFloat(x);
          y=parseFloat(y);
          if (x<=0 || y<1){
              $('#myModalSearchForSequence').modal('hide');
              $('#myModalShowUndValueBLAST').modal('show');
              return false;
          }
        }  
      }

      function validateFormBLAST2() {
        var x = document.forms["formBLAST2"]["edit_Evalue"].value;
        var y = document.forms["formBLAST2"]["edit_Align"].value;
        if (x=='' && y=='');
        else if (x=='' && y!=''){
          y=parseFloat(y);
          if (y<1){
            $('#myModalSearchForSequence').modal('hide');
            $('#myModalShowUndValueBLAST').modal('show');
            return false;
          }
        }
        else if (x!='' && y==''){
          x=parseFloat(x);
          if ( x<=0){
            $('#myModalSearchForSequence').modal('hide');
            $('#myModalShowUndValueBLAST').modal('show');
            return false;
          }
        }
        else{
          x=parseFloat(x);
          y=parseFloat(y);
          if (x<=0 || y<1){
              $('#myModalSearchForSequence').modal('hide');
              $('#myModalShowUndValueBLAST').modal('show');
              return false;
          }
        }  
      }

      function openModals() {
        $('#myModalShowIdentifier').modal('hide');
        $('#myModalSearchForSequence').modal('show');
      }


      $(function ()  
          { $("#compare_files").popover();  
          }); 
      $(function ()  
          { $("#remove_files").popover();  
          });
      $(function ()  
          { $("#compare_methods").popover();  
          });
      $(function ()  
          { $("#add_exclude").popover();  
          });
      $(function ()  
          { $("#hide_show").popover();  
          });
      $(function ()  
          { $("#align").popover();  
          });

     $('.dropdown-menu').click(function (e) {
        e.stopPropagation();
        }); 

     $(document).ready(function() {

  $("#save_as_svg").click(function() { submit_download_form("svg"); });

  $("#save_as_pdf").click(function() { submit_download_form("pdf"); });

  $("#save_as_png").click(function() { submit_download_form("png"); });
});

function submit_download_form(output_format)
{
  // Get the d3js SVG element
  var svg = document.getElementById("mysvg");
  // Extract the data as SVG text string
  var svg_xml = (new XMLSerializer).serializeToString(svg);

  // Submit the <FORM> to the server.
  // The result will be an attachment file to download.
  var form = document.getElementById("svgform");
  form['output_format'].value = output_format;
  form['data'].value = svg_xml ;
  //console.log(form['data'].value);
  form.submit();
}

window.onload = function () {
    if (typeof history.pushState === "function") {
        history.pushState("jibberish", null, null);
        window.onpopstate = function () {
            history.pushState('newjibberish', null, null);
        };
    }
    else {
        var ignoreHashChange = true;
        window.onhashchange = function () {
            if (!ignoreHashChange) {
                ignoreHashChange = true;
                window.location.hash = Math.random();
                // Detect and redirect change here
                // Works in older FF and IE9
                // * it does mess with your hash symbol (anchor?) pound sign
                // delimiter on the end of the URL
            }
            else {
                ignoreHashChange = false;   
            }
        };
    }
}

    </script>

   <?php

   session_start();

   $_SESSION['array_path[]'] = $array_path;
   if ($string_array==null);
   else $_SESSION['string_array']  = $string_array;
   $_SESSION['searchArray[]'] = $search_array;


  ?>


  <?php

    function ShowSequences($tb,$te,$ab,$ae){
        echo "<div id='check-upload'>".$wherePath."</div>";
    }
  ?>

  </body>

<!--MODALS-->
<div class="modal fade" id="myModalAdd" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel">Add files to Compare Genes</h4>
      </div>
      <div class="modal-body">
                    <form name="uploadFiles" enctype='multipart/form-data' action='moreuploadWithContigs.php' method='POST' onsubmit="return validateForm();">
                           Choose an Option:<select id="inputType" class="form-control" name="typeUpload" onchange="showToUpload()">
                                     <option value="yes">GFF+Fasta</option>
                                     <option value="no">Others</option></select>
                          <div id="fileOther"></div>
                          <div id="fileGFF+FASTA"><br>Choose a .gff file: <input name='moreuploadedfileGFF[]' type='file' class='btn btn-default'/>
                          <br>Choose a .fasta file: <input id="fileFASTA" name='moreuploadedfileFASTA[]' type='file' class='btn btn-default'/><br></div>
                          <input type="checkbox" name="Iscontig" value="yes">It is a file with sequence contigs<br>
                          <div class="modal-footer">
                          <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
                          <input type='submit' class='btn btn-primary' value='Upload Files' />
                          </div>
                          <input type='hidden' name='addmorefiles' value='addfiles'/>
                          </form>              
      </div>
    </div><!-- /.modal-content -->
  </div><!-- /.modal-dialog -->
</div>

<div class="modal fade" id="myModalRemove" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel">Choose files to Remove</h4>
      </div>
      <div class="modal-body"><div class="table-responsive">
    <table class="table table-hover" style="text-align:center;"><thead><tr style="background-color:#C5DBDF"><td>Name</td><td>Type&nbsp;of&nbsp;Search</td><td>&nbsp;</td></tr></thead><tbody>

        <?php
        for($i=0; $i < $num_files; $i++){
                  $parts=split(" ",$array_path[$i]);
                  if (count($parts) > 1){
                    $file="";
                    for($j=0; $j < count($parts); $j++){
                      list($folder1, $folder2, $folder3, $file1)=split("/",$parts[$j]);
                      if ($j==count($parts)-1) $file=$file.$file1." ";
                      else $file=$file.$file1." + ";
                    }
                  }
                  else list($folder1, $folder2, $folder3, $file)=split("/",$array_path[$i]);
                  echo'<tr><td>'.$file.'</td>';
                  echo "<td><form method='post' action = 'lessuploadWithContigs.php'>
                                <input type='submit' class='btn btn-link' value='Remove'/>
                                <input type='hidden' name='remove' value='".$i."'/>
                                <input type='hidden' name='lessfiles' value='lessfiles'/>";
                                                              
                    foreach($array_path as $value) {
                        echo "<input type='hidden' name='caminho[]'' value='". $value. "'>";
                    }                                                              
                                                               
                  echo '</form></td></tr>';
                }
          echo '</tbody><tfoot><tr style="background-color:#C5DBDF"><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr></tfoot></table></div>';
          ?>

        </div>
        <div class="modal-footer">
            <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
        </div>
    </div>
  </div>
</div>

<div class="modal fade" id="myModalCompare" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel">Choose files to Remove</h4>
      </div>
      <div class="modal-body">
        <?php
       
                   echo"<form enctype='multipart/form-data' action='searchWithContigs.php' method='POST'>
                        <input type='submit'  class='btn btn-link' name='bygene' value='Compare Genes By Name With Next Position Genome' />
                        <input type='hidden' name='inter-bygene' value='gene' />";

                if(isset($_POST['exclude_hypothetical'])) echo "<input type='hidden' name='exclude_hypothetical' value='exclude' />";
      
                echo "</form>";
                    
                    echo"<form enctype='multipart/form-data' action='searchWithContigs.php' method='POST'>
                        <input type='submit' class='btn btn-link' name='byfunction' value='Compare Genes By Function With Next Position Genome' />
                        <input type='hidden' name='inter-byfunction' value='function' />";
                                                                
       
    
                if(isset($_POST['exclude_hypothetical'])) echo "<input type='hidden' name='exclude_hypothetical' value='exclude' />";
      
                echo'</form>';
          ?>

        </div>
        <div class="modal-footer">
            <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
        </div>
    </div>
  </div>
</div>


<div class="modal fade" id="myModalAddEx" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel">Choose files to Remove</h4>
      </div>
      <div class="modal-body">
        <?php
if($_SESSION['exclude_hypothetical']=='yes'){ echo "<form enctype='multipart/form-data' action='searchWithContigs.php' method='POST'>
                                                                <input type='submit' class='btn btn-link' name='hyporemove' value='Add hypothetical proteins to analysis' />
                                                              <input type='hidden' name='add_hypothetical' value='add' />
                                                                </form>";
                                                          }

                else { echo "<form enctype='multipart/form-data' action='searchWithContigs.php' method='POST'>
                              <input type='submit' class='btn btn-link' name='hyporemove' value='Remove hypothetical proteins from analysis' />
                              <input type='hidden' name='exclude_hypothetical' value='exclude' />
                             </form>";
                      }
          ?>
      </div>
        <div class="modal-footer">
            <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
        </div>
    </div>
  </div>
</div>

<div class="modal fade" id="myModalHideShow" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel">Choose an Option</h4>
      </div>
      <div class="modal-body">
        <?php
if(isset($_POST['exclude_hypothetical']));

                else {if ($_SESSION['show_hypothetical']=='no'){
                      echo "<form enctype='multipart/form-data' action='searchWithContigs.php' method='POST'>
                            <input type='submit' class='btn btn-link' name='hyoremove' value='Show Hypothetical proteins' />
                            <input type='hidden' name='show_hypothetical' value='hypothetical' />";
                      
                      if(isset($_POST['align'])){
                        echo "<input type='hidden' name='align' value='align' />";
                      }      
                      echo "</form>";
                  }
                  else {
                    echo "<form enctype='multipart/form-data' action='searchWithContigs.php' method='POST'>
                            <input type='submit' class='btn btn-link' name='hyoremove' value='Hide Hypothetical proteins' />
                            <input type='hidden' name='hide_hypothetical' value='hypothetical' />"; 
                      
                      if(isset($_POST['align'])){
                        echo "<input type='hidden' name='align' value='align' />";
                      }      
                      echo "</form>";
                  }
                }
        ?>
</div>
        <div class="modal-footer">
            <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
        </div>
    </div>
  </div>
</div>

<div class="modal fade" id="myModalAlign" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel">Order contigs</h4>
      </div>
      <div class="modal-body">NOTE: Only files in .fasta format or .gbk can be used as reference or as query to do the alignments.
        <p>
        <?php
        $dir=$_SESSION['folderPath'].'/input_files';
          $files1 = scandir($dir);
          $numFiles=count($array_path);
          echo '<form enctype="multipart/form-data" action="searchWithContigs.php" method="POST" name="AlignForm" onsubmit="return validateFormAlign();">';
          echo '<label for="reference">Reference:</label><select id="reference" class="form-control" name="referenceGenome">';
          for($i=0; $i < $numFiles;$i++){
            $fileName=explode('/',$array_path[$i]);
            if($_SESSION['arrayContigs'][$i]=='no' && (strpos($fileName[3],'fa') !== false || strpos($fileName[3],'fasta') !== false || strpos($fileName[3],'gbk') !== false)) {
              echo' <option value="'.($i+1).'---'.$array_path[$i].'">'.($i+1).'&nbsp;-&nbsp;'.$fileName[3].'</option>';
            }
          }
          echo '</select>';

          echo '<label for="query">Query:</label><select id="query" class="form-control" name="queryGenome">';
          for($i=0; $i < $numFiles;$i++){
            $fileName=explode('/',$array_path[$i]);
            if($_SESSION['arrayContigs'][$i]=='yes' && (strpos($fileName[3],'fa') !== false || strpos($fileName[3],'fasta') !== false || strpos($fileName[3],'gbk') !== false)) {
              echo' <option value="'.($i+1).'---'.$array_path[$i].'">'.($i+1).'&nbsp;-&nbsp;'.$fileName[3].'</option>';
            }
          }
          echo '</select>';
          echo '<label for="minIde">Minimum Identity:</label><input type="name" class="form-control" id="minIde" name="minidentity" placeholder="0.98">';
          echo '<label for="minAl">Minimum Alignment:</label><input type="name" class="form-control" id="minAl" name="minAlignment" placeholder="500"><br>';
          echo '<input type="submit" class="btn btn-primary" name="align-button" value="Run Alignment" />';
          echo '</form>';
        ?></p>
</div>
        <div class="modal-footer">
            <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
        </div>
    </div>
  </div>
</div>

<div class="modal fade" id="myModalSearchMade" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel">Choose a previous Search to Remove</h4>
      </div>
      <div class="modal-body">
        <div style="text-align:right">
          <form method="POST" action = "searchWithContigs.php">                                                             
              <input type="hidden" name="removeAll" value="All"/>
              <input type="submit" class="btn btn-primary" value="Remove&nbsp;All"/>
          </form>
        </div><br><br>
        <div class="table-responsive">
    <table class="table table-hover" style="text-align:center;"><thead><tr style="background-color:#C5DBDF"><td>Name</td><td>Type&nbsp;of&nbsp;Search</td><td>&nbsp;</td></tr></thead><tbody>
        <?php

              if ($_SESSION['searchBySequence']=='yes') $num_search=count($_SESSION['ArrayBLAST[]']);
              else $num_search=count($search_array);


              if (isset($_POST['align'])) $align = $_POST['align']; 
              else{
              $align = null;
              }
              if ($_SESSION['searchBySequence']=='yes'){
                $num_search=count($_SESSION['ArrayBLAST[]']);
                echo "<div id='check-upload'>".$num_search."</div>";
                for($i=0; $i < $num_search; $i++){
                  $parts = explode('...', $_SESSION['ArrayBLAST[]'][$i]);
                  echo '<tr><td>'.$parts[1].'</td></td><td>BLAST&nbsp;Search</td><td>';
                    if(isset($_POST['exclude_hypothetical'])){
                          echo '<form method="post" action = "searchWithContigs.php">';

                        if(isset($_POST['align'])){
                          echo '<input type="hidden" name="align" value="align" />';
                        }
                                                              
                      echo '<input type="hidden" name="removeBLAST" value="'.$i.'"/>';

                      echo' <input type="hidden" name="remove_hypo" value="'.$remove_hypo.'" />
                            <input type="submit" class="btn btn-link" value="Remove"/>
                            <input type="hidden" name="exclude_hypothetical" value="exclude" />
                            </form></td></tr>';
                    }
                    else{
                           echo '<form method="post" action = "searchWithContigs.php">';

                          if(isset($_POST['align'])){
                              echo '<input type="hidden" name="align" value="align" />';
                          }
                                                              
                          echo '<input type="hidden" name="removeBLAST" value="'.$i.'"/>';
                                                              
                          echo '<input type="hidden" name="remove_hypo" value="'.$remove_hypo.'" />
                                <input type="submit" class="btn btn-link" value="Remove"/>
                                </form></td></tr>';
                        }
                }
              }
              else{

                $num_search=count($search_array);
                 
                for($i=0; $i < $num_search; $i++){
                  $nowsearch=str_replace('---', ' ', $search_array[$i]);
                  echo '<tr><td>'.$nowsearch.'</td></td><td>'.$typesearch_array[$i].'</td><td>';
                    if(isset($_POST['exclude_hypothetical'])){
                          echo '<form method="post" action = "searchWithContigs.php">';

                        foreach($search_array as $value) {
                          echo '<input type="hidden" name="caminhosearch[]" value="'. $value. '">';
                        } 

                        if(isset($_POST['align'])){
                          echo '<input type="hidden" name="align" value="align" />';
                        }
                                                              
                      echo '<input type="hidden" name="removesearch" value="'.$i.'"/>';

                      echo' <input type="hidden" name="remove_hypo" value="'.$remove_hypo.'" />
                            <input type="submit" class="btn btn-link" value="Remove"/>
                            <input type="hidden" name="exclude_hypothetical" value="exclude" />
                            </form></td></tr>';
                    }
                    else{
                           echo '<form method="post" action = "searchWithContigs.php">';

                            foreach($search_array as $value) {
                              echo '<input type="hidden" name="caminhosearch[]" value="'. $value. '">';
                            }

                          if(isset($_POST['align'])){
                              echo '<input type="hidden" name="align" value="align" />';
                          }
                                                              
                          echo '<input type="hidden" name="removesearch" value="'.$i.'"/>';
                                                              
                          echo '<input type="hidden" name="remove_hypo" value="'.$remove_hypo.'" />
                                <input type="submit" class="btn btn-link" value="Remove"/>
                                </form></td></tr>';
                        }
                }
              }

              echo '</tbody><tfoot><tr style="background-color:#C5DBDF"><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr></tfoot></table></div>';

            ?>

</div>
        <div class="modal-footer">
            <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
        </div>
    </div>
  </div>
</div>

<div class="modal fade" id="SearchTable" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel">Table of Hits</h4>
      </div>
      <div class="modal-body">

    <table class="display dataTable" id="HitTable" oncontextmenu="return false;"></table>

        <div class="modal-footer">
            <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
        </div>
    </div>
  </div>
</div>
</div>

<div class="modal fade" id="myModalGBK" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel">Choose files to Remove</h4>
      </div>
      <div class="modal-body">The query gene and reference genome must come from file formats with nucleotide sequences.
      </div>
        <div class="modal-footer">
            <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
        </div>
    </div>
  </div>
</div>

<div class="modal fade" id="myModalNoMatch" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel">No match for Sequence</h4>
      </div>
      <div class="modal-body">No matches were found using the <?php echo $querygenome[1].' gene from the '.$querygenome[0].' genome on the '.$refgen.' position genome.';?>
      </div>
        <div class="modal-footer">
            <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
        </div>
    </div>
  </div>
</div>

<div class="modal fade" id="myModalErrorDuringAlign" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel">No match for Sequence</h4>
      </div>
      <div class="modal-body">There was an error during the alignment. Only .fasta files can be used. Please try again.
      </div>
        <div class="modal-footer">
            <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
        </div>
    </div>
  </div>
</div>

<div class="modal fade" id="myModalGFFBLAST" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel">File without sequence information</h4>
      </div>
      <div class="modal-body">Only files with sequence information can be used with BLAST.
      </div>
        <div class="modal-footer">
            <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
        </div>
    </div>
  </div>
</div>

<div class="modal fade" id="myModalInfo" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true" oncontextmenu="return false;">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel">Information Table</h4>
      </div>
      <div class="modal-body">
        <table class="display dataTable" id="InfoTable" oncontextmenu="return false;"></table>
</div>
        <div class="modal-footer">
            <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
        </div>
    </div>
  </div>
</div>


<div class="modal fade" id="myModalLinkNotSelected" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        
        <?php 

        if ($_SESSION['showModalComp']=='yes'){
          echo '<h4 class="modal-title" id="myModalLabel">Not Showing Relationships</h4></div>
                <div class="modal-body">To see the relationships between the query results you have to choose a Comparison method from the Actions menu.';
        }
        else echo '<h4 class="modal-title" id="myModalLabel">Link Not In Selection</h4></div>
                  <div class="modal-body">There are some relationships with the next position genome but not on the selected area. To see them you have to remove the selections.';
      ?>

        </div>
        <div class="modal-footer">
            <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
        </div>
    </div>
  </div>
</div>

<div class="modal fade" id="myModalExport" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel">Choose an Option</h4>
      </div>
      <div class="modal-body">
        <button class="btn btn-primary" id="save_as_svg" value="">Export as SVG</button>
        <button class="btn btn-primary" id="save_as_pdf" value="">Export as PDF</button>
        <button class="btn btn-primary" id="save_as_png" value="">Export as High-Res PNG</button>
</div>
        <div class="modal-footer">
            <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
        </div>
    </div>
  </div>
</div>

<div class="modal fade" id="myModalExportGff" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel">Choose a file position to Export</h4>
      </div>
      <div class="modal-body">Choose a position to Export.<br>NOTE: Only anotated regions will be part of the exported files.
        <p>
        <?php
        $dir=$_SESSION['folderPath'].'/input_files';
          $files1 = scandir($dir);
          $numFiles=count($_SESSION['array_path[]']);
          echo '<form enctype="multipart/form-data" action="searchWithContigs.php" method="POST">';
          echo 'Position:<select class="form-control" name="exportGenome">';
          for($i=0; $i < $numFiles;$i++){
              $filenumber=$i+1;
              echo' <option value="'.$filenumber.'...'.$_SESSION['array_path[]'][$i].'">'.$filenumber.'</option>';
          }
          echo '</select>';

          echo 'Export Type:<select class="form-control" name="ExportType">';
          echo' <option value="gff">gff + fasta</option>';
          echo '</select>';
          echo '<input type="submit" class="btn btn-primary" name="align-button" value="Export File" />';
          echo '</form>';
        ?></p>
</div>
        <div class="modal-footer">
            <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
        </div>
    </div>
  </div>
</div>

<div class="modal fade" id="myModalDownloadExport" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel">Download your files here</h4>
      </div>
      <div class="modal-body">
        <?php
        if($moreContigs=='yes') echo "Only contigs with annotations were exported. To export the others, annotate those regions.<br>";
          echo "Choose the files to download:";
        if ($Contigexp=='yes'){
          echo '<li><a href="uploads/'.$wherePath.'/FastaToExport/'.$justName.'_newP.fasta">Download the .fasta file</a></li>';
          echo '<li><a href="uploads/'.$wherePath.'/Results/'.$wherePath.'.gff">Download the .gff file</a></li>';
        }
        else{
        if (strlen($RegionsToExport)>0 && $moreContigs=='yes') echo '<li><a href="uploads/'.$wherePath.'/FastaToExport/'.$justName.'_newP.fasta">Download the .fasta file</a></li>';
        else echo '<li><a href="uploads/'.$wherePath.'/FastaToExport/'.$justName.'_new.fasta">Download the .fasta file</a></li>';
        echo '<li><a href="uploads/'.$wherePath.'/Results/'.$wherePath.'.gff">Download the .gff file</a></li>';
      }
        ?>
</div>
        <div class="modal-footer">
            <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
        </div>
    </div>
  </div>
</div>

<div class="modal fade" id="myModalDownloadSequence" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel">See your sequence</h4>
      </div>
      <div class="modal-body">See the sequence here:
        <?php
        $parts1 = explode("...", $queryGe);
        $part = str_replace("---", "_", $parts1[1]);
        echo '<li><a href="uploads/'.$wherePath.'/Sequence_files/'.$part.'_sequence.fasta">Download the sequence file</a></li>';
        ?>
</div>
        <div class="modal-footer">
            <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
        </div>
    </div>
  </div>
</div>

<div class="modal fade" id="myModalShowError" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel">Error</h4>
      </div>
      <div class="modal-body">Please choose a file to upload.<br>You only can upload one of the supported files. (.fasta, .gbk, .ptt, .fna, .ffn, .gff)
</div>
        <div class="modal-footer">
            <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
        </div>
    </div>
  </div>
</div>

<div class="modal fade" id="myModalShowUndValue" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel">Error</h4>
      </div>
      <div class="modal-body">An undefined value was used for Minimum Identity or Minimum Alignment. Choose a value between 0 and 1 for Minimum Identity and bigger that 0 for Minimum Alignment.
</div>
        <div class="modal-footer">
            <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
        </div>
    </div>
  </div>
</div>

<div class="modal fade" id="myModalShowUndValueBLAST" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel">Choose valid parameters</h4>
      </div>
      <div class="modal-body">An undefined value was used for E-value or Minimum Alignment. Choose a value bigger than 0 for E-value and Minimum Alignment.
</div>
        <div class="modal-footer">
            <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
        </div>
    </div>
  </div>
</div>

<div class="modal fade" id="myModalShowUndGenomes" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel">Choose different Files</h4>
      </div>
      <div class="modal-body">Please choose different files to work as reference and as query.
</div>
        <div class="modal-footer">
            <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
        </div>
    </div>
  </div>
</div>

<div class="modal fade" id="myModalShowErrorSearch" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel">Error</h4>
      </div>
      <div class="modal-body">Please type a valid term on the searchbox.
</div>
        <div class="modal-footer">
            <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
        </div>
    </div>
  </div>
</div>

<div class="modal fade" id="myModalShowErrorTypeUpload" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel">Error</h4>
      </div>
      <div class="modal-body">For the option GFF + FASTA, you need to upload a sequence file (.fasta, .fna) and an annotation file (.gff) at the same time.
</div>
        <div class="modal-footer">
            <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
        </div>
    </div>
  </div>
</div>

<div class="modal fade" id="myModalShowErrorAfterUpload" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel">Error</h4>
      </div>
      <div class="modal-body">There was an error uploading the file.
</div>
        <div class="modal-footer">
            <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
        </div>
    </div>
  </div>
</div>

<div class="modal fade" id="myModalShowAnnotateError" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel">Annotation Error</h4>
      </div>
      <div class="modal-body"><? echo "To annotate this region, first you need to check similarity for the ".$searchRegion." region."; ?>
</div>
        <div class="modal-footer">
            <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
        </div>
    </div>
  </div>
</div>

<div class="modal fade" id="myModalMoreContigs" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel">Annotation Error</h4>
      </div>
      <div class="modal-body">Only contigs with annotations were exported. To export the others, annotate those regions.
</div>
        <div class="modal-footer">
            <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
        </div>
    </div>
  </div>
</div>



<div class="modal fade" id="myModalShowSNP" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel">Sequences Aligned</h4>
      </div>
      <div class="modal-body">
        <div class="first-column">
         <div class="table-responsive"><table class="table table-hover">
          <?php
            echo'<tbody><tr style="background-color:#C5DBDF"><td>Query&nbsp;Sequence&nbsp;</td></tr><tr><td>Matches</td></tr><tr style="background-color:#C5DBDF"><td>Target&nbsp;Sequence&nbsp;</td></tr><tr style="background-color:#C5DBDF"><td>SNPs&nbsp;(Total:&nbsp;';
            if ($SNPs[0]=='') echo '0)</td></tr></tbody></table></div></div>';
            else echo count($SNPs).')</td></tr></tbody></table></div></div>';
         ?>

        <div class="second-column"><div class="table-responsive"><table class="table table-hover">
        <?php 
              echo '<tbody><tr style="background-color:#C5DBDF">';
              $lengthSeq=strlen($querySeq);
              $isSNP='no';
              for($i=0; $i < $lengthSeq;$i++){
                echo '<td>'.$querySeq[$i].'</td>';
              }
              echo '</tr><tr>';
              for($i=0; $i < $lengthSeq;$i++){
                if ($matchSeq[$i]=='|'){
                echo '<td class="matchesCell">'.$matchSeq[$i].'</td>';
                }
                else{
                  echo '<td class="mismatchCell">'.$matchSeq[$i].'</td>';
                }
              }
              echo '</tr><tr style="background-color:#C5DBDF">';
              for($i=0; $i < $lengthSeq;$i++){
                echo '<td>'.$subjectSeq[$i].'</td>';
              }

              echo '</tr><tr style="background-color:#C5DBDF">';
              for($i=0; $i < $lengthSeq;$i++){
                for($j=0; $j < count($SNPs);$j++){
                  if (intval($SNPs[$j])-1==$i){
                    echo '<td>P</td>';
                    $isSNP='yes';
                  } 
                }
                if ($isSNP=='yes') $isSNP='no';
                else{
                  echo '<td>-</td>';
                } 
              }
              echo '</tr></tbody>';
        ?>
        </table></div></div>
        <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
</div>
    </div>
  </div>
</div>

<div class="modal fade" id="myModalFiles" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel">Upload</h4>
      </div>
      <div class="modal-body">
        <?php
          
          $numFiles=count($_SESSION['FilesAfterSearch']);

          for($i=0; $i < $numFiles;$i++){
              $filenumber=$i+1;
              echo "<td>The file ".$_SESSION['FilesAfterSearch'][$i]." has been uploaded."."<br>";
          }

          unset($_SESSION['FilesAfterSearch']);
        ?>
</div>
        <div class="modal-footer">
            <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
        </div>
    </div>
  </div>
</div>

<div class="modal fade" id="myModaldashboard" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel">Statistics</h4>
      </div>
      <div class="modal-body">
        <form id="statFile" name="statFile">
        <label for="selectStat">Select an option to visualize the statistics</label>
      <select class="form-control" id="selectStat"> 
        <?php
        $numFiles=count($array_path);
          for($i=0; $i < $numFiles;$i++){
              $filenumber=$i+1;
              echo'<option value="'.$i.'">File&nbsp;'.$filenumber.'</option>';
          }
            echo '<option value="all">All Files</option>';
        ?>
</select><br>
      <input class='btn btn-primary' value='Check Statistics' onclick="dash()"/></form>
        <div class="modal-footer">
        </div>
    </div>
  </div>
</div>
</div>

<div class="modal fade" id="myModaldashboard1" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal">&times;</button>
        <h4 class="modal-title" id="myModalLabel">Statistics</h4>
      </div>
      <div class="modal-body">
        <form id="statFile1" name="statFile1">
        <label for="selectStat">Select an option to visualize the statistics</label>
      <select class="form-control" id="selectStat"> 
        <?php
        $numFiles=count($array_path);
          for($i=0; $i < $numFiles;$i++){
              $filenumber=$i+1;
              echo'<option value="'.$i.'">File&nbsp;'.$filenumber.'</option>';
          }
            echo '<option value="all">All Files</option>';
        ?>
</select><br>
<input class='btn btn-primary' value='Check Statistics' onclick="dash()"/></form><div id="nameGenome"></div>
      <div id="dashSpot"><table id="dash"><tbody><tr><td><label for="histo">Histogram of Sizes</label><div id="histo"></div></td></tr><tr><td><label for="pieChart">Pie Chart of Products</label><div id="pieChart"></div></td></tr></tbody></table></div>
        <div id="legendSpot"><table class="display dataTable" id="legend"><thead><tr><th>Colour</th><th>Function</th><th>Counts</th><th>Frequency</th></tr></thead></table></div>
        <div class="modal-footer">
        </div>
    </div>
  </div>
</div>
</div>

<div class="modal fade" id="myModalAllUndefined" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal">&times;</button>
        <h4 class="modal-title" id="myModalLabel">Statistics</h4>
      </div>
      <div class="modal-body">
        <h5> All Gene Products in this file are Undefined.</h5>
        <div class="modal-footer">
          <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
        </div>
    </div>
  </div>
</div>
</div>

<div class="modal fade" id="myModalShowIdentifier" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal">&times;</button>
        <h4 class="modal-title" id="myModalLabel">Choose an identifier and a sequence</h4>
      </div>
      <div class="modal-body">
        <h5> Please type a nucleotide sequence and a name to identify it.</h5>
        <div class="modal-footer">
          <button type="button" class="btn btn-primary" data-toggle="modal" onclick="openModals()">OK</button>
        </div>
    </div>
  </div>
</div>
</div>


<div class="modal fade" id="myModalSearchForSequence" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal">&times;</button>
        <h4 class="modal-title" id="myModalLabel">Search By Sequence</h4>
      </div>
      <div class="modal-body">
        <form  id="formBLAST" enctype="multipart/form-data" action="searchWithContigs.php" method="POST" onsubmit="return validateFormBLAST()">
        <label for="insertSequence">Insert a Sequence:</label><div id="insertSequence"><input type="text" name="SeqToSearch" class="form-control" placeholder="Sequence"></div>
        <label for="identifier">Identifier:</label><input type="name" class="form-control" id="identifierS" name="identifierS" placeholder="Type a name to identify the sequence"><br>
        <br>
        <?php
          $numFiles=count($_SESSION['array_path[]']);
          echo '<label for="GenomeToSearch">Choose a File To Search:</label><select class="form-control" name="GenomeToSearch">';
          for($i=0; $i < $numFiles;$i++){
              $fileName=explode('/',$_SESSION['array_path[]'][$i]);
              $filenumber=$i+1;
              echo' <option value="'.$filenumber.'...">'.$filenumber.'&nbsp;-&nbsp;'.$fileName[3].'</option>';
          }
          echo '</select>';
        ?>
        <label for="edit_EvalueS">E-value:</label><input type="name" class="form-control" id="edit_EvalueS" name="edit_EvalueS" placeholder="0.001">
        <label for="edit_MinAlignS">Miminum Alignment:</label><input type="name" class="form-control" id="edit_MinAlignS" name="edit_MinAlignS" placeholder="300">
        <br>
        <input type="submit" class="btn btn-primary" name="align-button" value="Search" />
        <input type="hidden" name="SearchForSequence" value="SearchForSequence"/>
        </form>
    </div>
  </div>
</div>
</div>

<!--<div class="modal fade" id="GeneTable" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel">Table of Hits</h4>
      </div>
      <div class="modal-body">

    <table class="display dataTable" id="TableOfGenes"></table>

        <div class="modal-footer">
            <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
        </div>
    </div>
  </div>
</div>
</div>-->
</html>