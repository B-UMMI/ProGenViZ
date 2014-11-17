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

  <!--#######################################################START OF PHP POST AND SESSIONS DEALING. INPUT PROCESSING#####################################!-->
  <?php 


    session_start();

    $refresh='yes'; 

    $path_value=$_SESSION['array_path[]'];

    if ($_SESSION['SearchMade']==null){
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
      unset($_SESSION['searchArray[]']);
      unset($_SESSION['typesearch[]']);
    }

    if (isset($_POST['inter-bygene'])) {
      //echo "<div id='check-upload'>Compare method in use : By gene name with next position genome.</div>";
      $_SESSION['compNull'] = 'no';
      $_SESSION['inter-bygene'] = 'yes';
      $_SESSION['inter-byfunction'] = 'no';
    }
    if (isset($_POST['inter-byfunction'])){
      //echo "<div id='check-upload'>Compare method in use : By gene function with next position genome.</div>";
      $_SESSION['compNull'] = 'no';
      $_SESSION['inter-bygene'] = 'no';
      $_SESSION['inter-byfunction'] = 'yes';

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
    $refresh='no';
    $_SESSION['editInfo']='yes';
   }
   else $_SESSION['editInfo']='no';


    if (isset($_POST['exclude_hypothetical'])){
     //echo "<div id='check-upload'>Hypothetical proteins have been excluded from analysis.</div>";
     $path_value=$_SESSION['array_path[]'];
     $_SESSION['exclude_hypothetical'] = 'yes';
    }
    if (isset($_POST['add_hypothetical'])){
      //echo "<div id='check-upload'>Hypothetical proteins have been added to analysis.</div>";
      $path_value=$_SESSION['array_path[]'];
      $_SESSION['exclude_hypothetical'] = 'no';
    }

  $arrayFilesUploaded = array();
  $errorUpload='no';
  $ModalUpload='no';
  $existGFF='no';
  $existFASTA='no';
  if(isset($_POST['addmorefiles'])){
    $_SESSION['alreadyShownUpload']='no';
      $num_files_path = count($path_value);
          $stringFiles=""; 
            if($_POST['typeUpload']=='yes'){
                /* Add the original filename to our target path.  
                Result is "uploads/filename.extension" */
                $stringFiles = $stringFiles.$_SESSION['folderPath'].'/input_files/'.basename($_FILES['moreuploadedfileGFF']['name'][0]);
                $stringFiles = $stringFiles." ".$_SESSION['folderPath'].'/input_files/'.basename($_FILES['moreuploadedfileFASTA']['name'][0]);

                if(file_exists($_SESSION['folderPath'].'/input_files/'.basename($_FILES['moreuploadedfileGFF']['name'][0]))){
                  array_push($arrayFilesUploaded,basename( $_FILES['moreuploadedfileGFF']['name'][0]));
                  $existGFF='yes';
                }
                if(file_exists($_SESSION['folderPath'].'/input_files/'.basename($_FILES['moreuploadedfileFASTA']['name'][0]))){
                  array_push($arrayFilesUploaded,basename( $_FILES['moreuploadedfileFASTA']['name'][0]));
                  $existFASTA='yes';
                }

                if($existGFF=='no'){
                  if(move_uploaded_file($_FILES['moreuploadedfileGFF']['tmp_name'][0], $_SESSION['folderPath'].'/input_files/'.basename($_FILES['moreuploadedfileGFF']['name'][0]))) {
                    array_push($arrayFilesUploaded,basename( $_FILES['moreuploadedfileGFF']['name'][0]));
                  } 
                }
                if($existFASTA=='no'){
                  if(move_uploaded_file($_FILES['moreuploadedfileFASTA']['tmp_name'][0], $_SESSION['folderPath'].'/input_files/'.basename($_FILES['moreuploadedfileFASTA']['name'][0]))) {
                    array_push($arrayFilesUploaded,basename( $_FILES['moreuploadedfileFASTA']['name'][0]));
                  } 
                }
                if ($_SESSION['SearchMade']!=null){
                    $_SESSION['FilesAfterSearch']=$arrayFilesUploaded;
                }
                else $_SESSION['FilesUploaded']=$arrayFilesUploaded;
          

          $path_value[$num_files_path]=$stringFiles;
          $_SESSION['array_path[]']=$path_value;
          $refresh='no';
          $_SESSION['num_more_files'] = 1;
        }
        else{
                $_SESSION['num_more_files'] = 1;
                $path_value[$num_files_path] = $_SESSION['folderPath'].'/input_files/'.basename($_FILES['moreuploadedfile']['name'][0]);
                if(file_exists($path_value[$num_files_path])){
                  array_push($arrayFilesUploaded,basename( $_FILES['moreuploadedfile']['name'][0]));
                  if ($_SESSION['SearchMade']!=null){
                    $_SESSION['FilesAfterSearch']=$arrayFilesUploaded;
                  }
                  else $_SESSION['FilesUploaded']=$arrayFilesUploaded;
                }
                else{
                if(move_uploaded_file($_FILES['moreuploadedfile']['tmp_name'][0], $path_value[$num_files_path])) {
                  array_push($arrayFilesUploaded,basename( $_FILES['moreuploadedfile']['name'][0]));
                  if ($_SESSION['SearchMade']!=null){
                    $_SESSION['FilesAfterSearch']=$arrayFilesUploaded;
                  }
                  else $_SESSION['FilesUploaded']=$arrayFilesUploaded;
                
                } 
              }
            }
          
      $_SESSION['array_path[]']=$path_value;
      $refresh='no';
      $wherePath=$_SESSION['userPath'];
      $path_exec='';
      $countFiles=count($path_value);
      $gffInfasta=$_POST['typeUpload'];
      $path_exec = $path_exec.$path_value[$countFiles-1].' ';
      $countFiles=$countFiles-$_SESSION['num_more_files'];
      $_SESSION['compNull'] = 'yes';
      $_SESSION['inter-bygene'] = 'no';
      $_SESSION['inter-byfunction'] = 'no';
      $_SESSION['inter-byfunctionAll'] = 'no';
      $_SESSION['inter-bygeneAll'] = 'no';

      if (isset($_POST['Iscontig'])){
        $_SESSION['hasContig']='yes';
        $Iscontig=$_POST['Iscontig'];
        array_push($_SESSION['arrayContigs'],$_POST['Iscontig']);
      } 


      else{
        array_push($_SESSION['arrayContigs'],'no');
        $Iscontig='no';
      } 


      if ($_SESSION['SearchMade']==null){
       $_SESSION['headerMoreUpload'] = 'yes';
       if (count($_SESSION['array_path[]'])==1) exec("python parsers/parserfiles.py $path_exec $gffInfasta $Iscontig",$param);
       else exec("python parsers/parserfilesWithSearch.py $path_exec $countFiles $gffInfasta $Iscontig",$param);
       $stringOfFiles=$param[0];
       if ($stringOfFiles=='ERROR'){
        $_SESSION['uploadError'] = 'yes';
       }
       else{
         $_SESSION['uploadError'] = 'no';
         exec("python parsers/FastaMaker.py $wherePath $stringOfFiles $Iscontig");
         exec("python parsers/setContigs.py $wherePath");
         exec("python parsers/getSizeWithContigs.py $wherePath");
         exec("python makeComparisons/makeImportsNullWithContigs.py $wherePath");
      }
       //header('Location: moreuploadWithContigs.php'); //Clears form and prevent it to be accessed on refresh
      }
      else{
        if (count($_SESSION['array_path[]'])==1) exec("python parsers/parserfiles.py $path_exec $gffInfasta $Iscontig",$param);
        else exec("python parsers/parserfilesWithSearch.py $path_exec $countFiles $gffInfasta $Iscontig",$param);
        $stringOfFiles=$param[0];
        if ($stringOfFiles=='ERROR'){
        $_SESSION['uploadError'] = 'yes';
       }
       else{
        $_SESSION['uploadError'] = 'no';
        exec("python parsers/FastaMaker.py $wherePath $stringOfFiles $Iscontig");
        exec("python parsers/setContigsWithSearch.py $wherePath $countFiles");
        exec("python parsers/getSizeWithSearchWithContigs.py $wherePath $countFiles");
        exec("python makeComparisons/makeImportsNullWithSearchWithContigs.py $wherePath $countFiles");
      }
      header('Location: searchWithContigs.php');
      exit();
      } 
      
      #} 

    }
    else $_SESSION['alreadyShownUpload']='yes';

    for($i=0; $i < count($_SESSION['array_path[]']);$i++){
      $filesNames = $filesNames.$_SESSION['array_path[]'][$i].'---';
    }

    if (isset($_POST["positionToBe"])){
        $_SESSION['remakeComparisons']='yes';
        $currentPos = $_POST["currentPosition"];
        $positionToBe = $_POST["positionToBe"];
        $elementToChange = $path_value[$currentPos];
        $otherElement = $path_value[$positionToBe];
        $path_value[$positionToBe] = $elementToChange;
        $path_value[$currentPos] = $otherElement;
        $refresh='no';
        $_SESSION['array_path[]']=$path_value;
        $_SESSION['currentPos']=$currentPos;
        $_SESSION['positionToBe']=$positionToBe;
        header('Location: moreuploadWithContigs.php');

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
      $refresh='no';
      $exportContig=$_POST['contigToExport'];
      $exportgenome=$_POST['GenomeToExport'];
      $exportType=$_POST['ExportType'];
      $posGinteger=intval($exportgenome)-1;
      $exportFile=$_SESSION['array_path[]'][$posGinteger];
      $partsFile=explode('/',$exportFile);
      $fileNameToExport=$partsFile[count($partsFile)-1];
      $justN=explode('.',$fileNameToExport);
      $justName=$justN[0];
      $Contigexp='yes';
    }

    if (isset($_POST['selectionArray'])){
          $_SESSION['selectionArray'] = $_POST['selectionArray'];
    }

    if (isset($_POST['removeselection'])){
      $_SESSION['selectionArray']=null;
    }

    if (isset($_POST['GetSequence'])){
      $refresh='no';
      $ModalSequence='yes';
    }
    else $ModalSequence='no';
     
      
  ?>

<!--#######################################################END OF PHP POST AND SESSIONS DEALING. END OF INPUT PROCESSING#####################################-->



  <body style="">
     <div id="contextMenu">    
    </div>


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
            <li class="active"><a class="navPrincipal" href="index.php">Home</a></li>                       
            <li class="dropdown">
                  <a href="#" class="navPrincipal" class="dropdown-toggle" data-toggle="dropdown">Help<b class="caret"></b></a>
                  <ul class="dropdown-menu">
                    <li><a class="navPrincipal" href="Tutorial.php">Tutorial</a></li>
                    <li class="divider"></li>
                    <li><a class="navPrincipal" href="TestFiles.php">Test Files</a></li>
                  </ul>
                </li>
            <li><a class="navPrincipal" href="About.php">About</a></li>
            <li><a class="navPrincipal" href="Contact.php">Contacts</a></li>
          </ul></div></div></div>

  <div id="sidebar-wrapper">
        <ul class="sidebar-nav">
          <li class="sidebar-brand" id="brand">Actions</li>
          <li><a href="#" data-toggle="modal" data-target="#myModalInfo">More Info</a></li>
          <li><a href="#" data-toggle="modal" data-target="#myModalAdd">Add file</a></li>
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
          <li class="sidebar-brand" id="brand">Search</li>
          <li><a href="#" data-toggle="modal" data-target="#myModalSearchForSequence">By external sequence</a></li><li>&nbsp;</li>
          <li><a>By annotation</a></li>
          
            
          <!--###########SEARCHES AND VISUALIZATION MODE CHOOSING##############################-->

            <?php

            if (isset($_POST['align'])) $align = $_POST['align']; 
            else{
              $align = null;
            }

              echo '<form name="searchForm" enctype="multipart/form-data" action="searchWithContigs.php" method="POST" onsubmit="return validateFormSearch()">';

              echo '<select class="form-control" name="genomesearch">
                        <option value="allgenome"/>All Files';
              $numgenomes=count($_SESSION['array_path[]']);
              if ($numgenomes>1){
                for($i=0; $i < $numgenomes;$i++){
                      $fileName=explode('/',$_SESSION['array_path[]'][$i]);
                      echo '<option value="'.($i+1).'"/>'.($i+1).'-'.$fileName[3];
                }
              }
    
              echo '</select>';

              echo '<select class="form-control" name="typesearch">
                      <option value="GeneName"/>Region Name
                      <option value="GeneProduct"/>Region Product
                      <option value="Begin-End"/>Begin - End
                    </select>';

              echo' <input class="form-control" type="text" name= "searchbox" placeholder="type a search term">
                    <input type="submit" class="btn btn-primary btn-lg"  style="width: 100%; padding: 2px 5px;" name="search-button" value="Search" />
                    <input type="hidden" name="add_hypothetical" value="undefined" />  
                    </form>';

                        
            

            ?>
            <li><hr></hr></li>
            <li>
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
          echo '<form enctype="multipart/form-data" action="moreuploadWithContigs.php" method="POST">
                    <input type="submit" class ="btn-link changeVisualButton" name="linearView" value="Change to Hive Plot View"/>
                    <input type="hidden"  name="edInfo" value="'.$_SESSION['editInfo'].'"/>';

          if (isset($_POST['selectionArray'])){
                  $array=$_SESSION['selectionArray'];
                  echo "<input type='hidden' name='selectionArray' value='".$array. "'>
                        <input type='hidden' name='remove_selection'>";
          }
                echo '</form> ';
        }
        else{
          echo '<form enctype="multipart/form-data" action="moreuploadWithContigs.php" method="POST">
                    <input type="submit" class ="btn-link changeVisualButton" name="hiveView" value="Change to Linear View"/>
                    <input type="hidden"  name="edInfo" value="'.$_SESSION['editInfo'].'"/>';

          if (isset($_POST['selectionArray'])){
                  $array=$_SESSION['selectionArray'];
                  echo "<input type='hidden' name='selectionArray' value='".$array. "'>
                        <input type='hidden' name='remove_selection'>";
          }
                echo '</form> ';
        }
      ?>

      <!--###########END OF SEARCHES AND VISUALIZATION MODE CHOOSING##############################-->

    </li>
    <li><a id="buttonSelPos"></a></li>
          <?php
              if (isset($_POST['remove_selection']) || $_SESSION['selectionArray']!=''){
                echo '<li><hr></hr></li>';
                echo '<li><form <form enctype="multipart/form-data" action="moreuploadWithContigs.php" method="POST">
                        <input type="submit" class ="btn-link removeSelection" name="removesel" value="Remove Selection" />
                        <input type="hidden" name="removeselection"/>';
                echo'</form></li>';
              }
            ?>

    <li><hr></hr></li>
    <li class ="CompMethodTitle">Comparison method:</li> 
    <?php

      if($_SESSION['inter-bygene']=='yes') echo '<li class ="CompMethod">Region Name</li>';
      else if($_SESSION['inter-byfunction']=='yes') echo '<li class ="CompMethod">Region Product</li>';
      else echo '<li class ="CompMethod">None</li>';

    ?>
    <li><hr></hr></li></ul></div>  


    <!--VISUALIZATION LOCATION-->

     <div id="chart-position">
      <div id='demo_2'>
    <span class='notes'></span>
      </div>
    
      <div id='demo_2'>

            <span class='chart' oncontextmenu="return false;">&nbsp;</span>
 
      </div>
</div>



    <?php

    if (isset($_POST['align'])) $align = $_POST['align']; 
    else{
      $align = null;
    }
  
    $wherePath=$_SESSION['userPath'];
    
    if($refresh=='no'){
      $num_filesArray = count($path_value);
      $path_exec = "";
      for ($i=0; $i<$num_filesArray;$i++){  #
        $path_exec = $path_exec.$path_value[$i].' ';

      }
      if($_SESSION['editInfo']=='yes'){
      $genomeToChange= explode('...', $nameToChange);
      $fileToChange=$path_value[intval($genomeToChange[0])-1];
      exec("python parsers/edit_infoWithContigs.py $wherePath $fileToChange $nameToChange $editName $productToChange $editProduct $geneBegin");
    }
    else if (isset($_POST['exportGenome'])){
      $modalDownloadExport='yes';
      $RegionsToExport=$_SESSION["ContigsToExport"];
      exec("python parsers/createGFFfile.py $wherePath $exportGenome $exportType $RegionsToExport",$moreContig);
      $moreContigs=$moreContig[0];
    }
    else if (isset($_POST['exportContig'])){
      $modalDownloadExport='yes';
      $fileName=$justName;
      exec("python parsers/exportSingleContigs.py $wherePath $exportgenome $exportType $fileName $exportContig",$moreContig);
      $moreContigs=$moreContig[0];
    }
    else if (isset($_POST['GetSequence'])){
      $seqRef=$_POST['geneReference'];
      $queryGene=$_POST['queryGene'];
      exec("python parsers/SearchSequence.py $wherePath $seqRef $queryGene");
    }
    else{
      if ($_SESSION['remakeComparisons']=='yes'){
        $currentPos=$_SESSION['currentPos'];
        $positionToBe=$_SESSION['positionToBe'];
        exec("python parsers/ChangePosition.py $wherePath $currentPos $positionToBe");
        $_SESSION['currentPos']=null;
        $_SESSION['positionToBe']=null;
        $_SESSION['remakeComparisons']='no';
      }
      
     } 
    }
  


    ?>



    <!--##########JAVASCRIPT SECTION##################-->

    <script>
    var InfoArray = new Array();
    var editInfo='<?php echo $_SESSION["editInfo"];?>';
      var hasfaa = '<?php echo $hasfaa; ?>';
      var showfaa = '<?php echo $showfaa; ?>';
      var inputwhere = '<?php echo $_SESSION["folderPath"]."/".$_SESSION["userPath"]."_input.json"; ?>';
      var wherePath= '<?php echo $wherePath;?>';
      var fileNames='<?php echo $filesNames;?>';
      var exclude_hypothetical='<?php echo $_SESSION["exclude_hypothetical"];?>';
      var modalDownloadExport="<?php echo $modalDownloadExport;?>";
      var ModalSequence="<?php echo $ModalSequence;?>";
      var arr='<?php echo $_SESSION["selectionArray"]; ?>';
      var errorFile="<?php echo $errorUpload;?>";
      var numFilesUploaded="<?php echo count($_SESSION['FilesUploaded']);?>";
      var DataTable="";
      var errorUpload="<?php echo $_SESSION['uploadError'];?>";
      var alreadyShownUpload="<?php echo $_SESSION['alreadyShownUpload'];?>";

   if (arr==''){
    var sel='undefined';
   }
   else var sel=JSON.parse(arr);

    </script>

    <?php
      session_start();

      if ($_SESSION['uploadError'] == 'yes'){
        $array_path_Prov = $_SESSION['array_path[]'];
        $numFilesUp=count($array_path_Prov)-1;
        unset($array_path_Prov[$numFilesUp]);
        $path_value = array_values($array_path_Prov);
        $_SESSION['array_path[]'] = $path_value;
        echo "<script src='data_plot_js/ErrorOnUpload.js'></script>";
        $_SESSION['uploadError']='no';
      }

        echo "<script src='data_plot_js/dashboard.js'></script>";
        echo "<script src='data_plot_js/lib_dataWithContigs.js'></script>";
        echo "<script src='data_plot_js/lib_link.js'></script>";
        echo "<script src='data_plot_js/lib_mouse.js'></script>";

      if($_SESSION['linearMode'] == 'no'){
        echo '<script src="data_plot_js/lib_plotWithContigs.js"></script>';
      }
      else{
        echo '<script src="data_plot_js/lib_plotWithContigsNoHive.js"></script>';
      }
      echo "<script src='data_plot_js/main.js'></script>";
      
    ?>

    
    
    
    <script>  
    var align='<?php echo $align;?>';
    var inter_byfunction = '<?php echo $_SESSION["inter-byfunction"];?>';
    var inter_bygene = '<?php echo $_SESSION["inter-bygene"];?>';

    function showToUpload() {
        var selected=document.getElementById("inputType").value;
        if (selected=='no'){
          document.getElementById("fileGFF+FASTA").innerHTML="";
          document.getElementById("fileOther").innerHTML="<br><li class='FontModals'>Choose one of the supported file formats (.fasta, .gbk, .gff): </li><input name='moreuploadedfile[]' type='file' class='btn btn-default btn-lg'/><br><input type='checkbox' name='Iscontig' value='yes'><a class='FontModals'>&nbsp;It is a FASTA file with contigs data</a><br>";
        }
        if (selected=='yes'){
          document.getElementById("fileOther").innerHTML="";
          document.getElementById("fileGFF+FASTA").innerHTML="<br><li class='FontModals'>Choose a GFF file:</li> <input name='moreuploadedfileGFF[]' type='file' class='btn btn-default btn-lg'/><br><li class='FontModals'>Choose a FASTA file:</li> <input name='moreuploadedfileFASTA[]' type='file' class='btn btn-default btn-lg'/><br>";
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
        var Iscontig=document.forms["uploadFiles"]["Iscontig"].checked;
        if (Xfiles.length==0){
            $('#myModalShowError').modal('show');
            return false;
          }
        else{
          var x =Xfiles[0].name;
          if ((x.search('.fa')==-1 && x.search('.fasta')==-1) && Iscontig){
              $('#myModalOnlyFASTA').modal('show');
          return false;
          }
          else if (x == null || x == "" || (x.search('.fa')==-1 && x.search('.fasta')==-1 && x.search('.gbk')==-1 && x.search('.gff')==-1)) {
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
          y=parseFloat(y);
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
    </script>

    <script>


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
  form.submit();
}

window.onload = function () {
    if (typeof history.pushState === "function") {
        history.pushState("jibberish", null, null);
        window.onpopstate = function () {
            history.pushState('newjibberish', null, null);
            // Handle the back (or forward) buttons here
            // Will NOT handle refresh, use onbeforeunload for this.
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


  </body>

<!--MODALS-->
<div class="modal fade" id="myModalAdd" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel"><a class="FontModalsTitle">Add files to the analysis</a></h4>
      </div>
      <div class="modal-body" class="ModalsSizeFont">
                    <form name="uploadFiles" enctype='multipart/form-data' action='moreuploadWithContigs.php' method='POST' onsubmit="return validateForm();">
                           <li class="FontModals">Choose an Option:</li><select id="inputType" class="form-control" name="typeUpload" onchange="showToUpload()">
                                     <option value="yes" class="FontModals">GFF+Fasta</option>
                                     <option value="no" class="FontModals">Others</option></select>
                          <div id="fileOther"></div>
                          <div id="fileGFF+FASTA"><br><li class="FontModals">Choose a .gff file:</li> <input name='moreuploadedfileGFF[]' type='file' class='btn btn-default btn-lg'/>
                          <br><li class="FontModals">Choose a .fasta file:</li> <input id="fileFASTA" name='moreuploadedfileFASTA[]' type='file' class='btn btn-default btn-lg'/><br></div>
                          <div class="modal-footer">
                          <button type="button" class="btn btn-default btn-lg" data-dismiss="modal">Close</button>
                          <input type='submit' class='btn btn-primary btn-lg' value='Upload File' />
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
        <h4 class="modal-title" id="myModalLabel"><a class="FontModalsTitle">Choose files to Remove</a></h4>
      </div>
      <div class="modal-body"><div class="table-responsive">
    <table class="table table-hover" style="text-align:center;"><thead><tr style="background-color:#C5DBDF"><td class='FontModals'>Name</td><td class='FontModals'>Type&nbsp;of&nbsp;Search</td><td>&nbsp;</td></tr></thead><tbody>

        <?php
        $num_files= count($path_value);
        for($i=0; $i < $num_files; $i++){
                  $parts=split(" ",$path_value[$i]);
                  if (count($parts) > 1){
                    $file="";
                    for($j=0; $j < count($parts); $j++){
                      list($folder1, $folder2, $folder3, $file1)=split("/",$parts[$j]);
                      if ($j==count($parts)-1) $file=$file.$file1." ";
                      else $file=$file.$file1." + ";
                    }
                  }
                  else list($folder1, $folder2, $folder3, $file)=split("/",$path_value[$i]);
                  echo'<tr><td class="FontModals">'.$file.'</td>';
                  echo "<td><form method='post' action = 'lessuploadWithContigs.php'>
                                <input type='submit' class='btn btn-link btn-lg' value='Remove'/>
                                <input type='hidden' name='remove' value='".$i."'/>
                                <input type='hidden' name='lessfiles' value='lessfiles'/>";
                                                              
                    foreach($path_value as $value) {
                        echo "<input type='hidden' name='caminho[]'' value='". $value. "'>";
                    }                                                              
                                                               
                  echo '</form></td></tr>';
                }
          echo '</tbody><tfoot><tr style="background-color:#C5DBDF"><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr></tfoot></table></div>';
          ?>

        </div>
        <div class="modal-footer">
            <button type="button" class="btn btn-default btn-lg" data-dismiss="modal">Close</button>
        </div>
    </div>
  </div>
</div>

<div class="modal fade" id="myModalCompare" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel"><a class="FontModalsTitle">Choose a Comparison Method</a></h4>
      </div>
      <div class="modal-body">
        <?php
        
                    echo"<form enctype='multipart/form-data' action='moreuploadWithContigs.php' method='POST'>
                        <input type='submit'  class='btn btn-link btn-lg' name='bygene' value='Compare Regions By Name With Next Position File' />
                        <input type='hidden' name='inter-bygene' value='gene' />";

                if(isset($_POST['exclude_hypothetical'])) echo "<input type='hidden' name='exclude_hypothetical' value='exclude' />";
      
                echo "</form>";
                    
                     echo"<form enctype='multipart/form-data' action='moreuploadWithContigs.php' method='POST'>
                        <input type='submit' class='btn btn-link btn-lg' name='byfunction' value='Compare Regions By Product With Next Position File' />
                        <input type='hidden' name='inter-byfunction' value='function' />";
                                                                
       
    
                if(isset($_POST['exclude_hypothetical'])) echo "<input type='hidden' name='exclude_hypothetical' value='exclude' />";
      
                echo'</form>';
          ?>

        </div>
        <div class="modal-footer">
            <button type="button" class="btn btn-default btn-lg" data-dismiss="modal">Close</button>
        </div>
    </div>
  </div>
</div>


<div class="modal fade" id="myModalAddEx" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel"><a class="FontModalsTitle">Choose an Option</a></h4>
      </div>
      <div class="modal-body">
        <?php
if($_SESSION['exclude_hypothetical'] =='yes'){ echo "<form enctype='multipart/form-data' action='moreuploadWithContigs.php' method='POST'>
                                                                <input type='submit' class='btn btn-link btn-lg' name='hyporemove' value='Add hypothetical proteins to analysis' />
                                                              <input type='hidden' name='add_hypothetical' value='add' />
                                                                </form>";
                                                          }

                else { echo "<form enctype='multipart/form-data' action='moreuploadWithContigs.php' method='POST'>
                              <input type='submit' class='btn btn-link btn-lg' name='hyporemove' value='Remove hypothetical proteins from analysis' />
                              <input type='hidden' name='exclude_hypothetical' value='exclude' />
                             </form>";
                      }
          ?>
      </div>
        <div class="modal-footer">
            <button type="button" class="btn btn-default btn-lg" data-dismiss="modal">Close</button>
        </div>
    </div>
  </div>
</div>

<div class="modal fade" id="myModalHideShow" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel"><a class="FontModalsTitle">Choose an Option</a></h4>
      </div>
      <div class="modal-body">
        <?php
if(isset($_POST['exclude_hypothetical']));

                else {echo "<form enctype='multipart/form-data' action='searchWithContigs.php' method='POST'>
                            <input type='submit' class='btn btn-link btn-lg' name='hyoremove' value='Show hypothetical proteins' />
                            <input type='hidden' name='show_hypothetical' value='hypothetical' />";
                      
                      if(isset($_POST['align'])){
                        echo "<input type='hidden' name='align' value='align' />";
                      }      
                      echo "</form>";
                      }
        ?>
</div>
        <div class="modal-footer">
            <button type="button" class="btn btn-default btn-lg" data-dismiss="modal">Close</button>
        </div>
    </div>
  </div>
</div>

<div class="modal fade" id="myModalAlign" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel"><a class="FontModalsTitle">Order contigs</a></h4>
      </div>
      <div class="modal-body"><li class="FontModals">NOTE: Only files in .fasta format or .gbk can be used as reference or as query to do the alignments.</li>
        <p>
        <?php
        $dir=$_SESSION['folderPath'].'/input_files';
          $files1 = scandir($dir);
          $numFiles=count($path_value);
          echo '<form enctype="multipart/form-data" action="searchWithContigs.php" method="POST" name="AlignForm" onsubmit="return validateFormAlign();">';
          echo '<li class="FontModals">Reference:</li><select id="reference" class="form-control" name="referenceGenome">';
          for($i=0; $i < $numFiles;$i++){
            $fileName=explode('/',$path_value[$i]);
            if($_SESSION['arrayContigs'][$i]=='no' && (strpos($fileName[3],'fa') !== false || strpos($fileName[3],'fasta') !== false || strpos($fileName[3],'gbk') !== false)) {
              echo' <option value="'.($i+1).'---'.$path_value[$i].'">'.($i+1).'&nbsp;-&nbsp;'.$fileName[3].'</option>';
            }
          }
          echo '</select>';

          echo '<li class="FontModals">Query:</li><select id="query" class="form-control" name="queryGenome">';
          for($i=0; $i < $numFiles;$i++){
            $fileName=explode('/',$path_value[$i]);
            if($_SESSION['arrayContigs'][$i]=='yes' && (strpos($fileName[3],'fa') !== false || strpos($fileName[3],'fasta') !== false || strpos($fileName[3],'gbk') !== false)) {
              echo' <option value="'.($i+1).'---'.$path_value[$i].'">'.($i+1).'&nbsp;-&nbsp;'.$fileName[3].'</option>';
            }
          }
          echo '</select>';
          echo '<li class="FontModals">Minimum Identity:</li><input type="name" class="form-control" id="minIde" name="minidentity" placeholder="0.98">';
          echo '<li class="FontModals">Minimum Alignment:</li><input type="name" class="form-control" id="minAl" name="minAlignment" placeholder="500"><br>';
          echo '<input type="submit" class="btn btn-primary btn-lg" name="align-button" value="Run Alignment" />';
          echo '</form>';
        ?></p>
</div>
        <div class="modal-footer">
            <button type="button" class="btn btn-default btn-lg" data-dismiss="modal">Close</button>
        </div>
    </div>
  </div>
</div>

<div class="modal fade" id="myModalInfo" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true" oncontextmenu="return false;">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel"><a class="FontModalsTitle">Information Table</a></h4>
      </div>
      <div class="modal-body">
        <table class="display dataTable" id="InfoTable" oncontextmenu="return false;"></table>
</div>
        <div class="modal-footer">
            <button type="button" class="btn btn-default btn-lg" data-dismiss="modal">Close</button>
        </div>
    </div>
  </div>
</div>

<div class="modal fade" id="myModalExport" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel"><a class="FontModalsTitle">Choose an Option</a></h4>
      </div>
      <div class="modal-body">
        <button class="btn btn-primary btn-lg" id="save_as_svg" value="">Export as SVG</button>
        <button class="btn btn-primary btn-lg" id="save_as_pdf" value="">Export as PDF</button>
        <button class="btn btn-primary btn-lg" id="save_as_png" value="">Export as High-Res PNG</button>
</div>
        <div class="modal-footer">
            <button type="button" class="btn btn-default btn-lg" data-dismiss="modal">Close</button>
        </div>
    </div>
  </div>
</div>

<div class="modal fade" id="myModalExportGff" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel"><a class="FontModalsTitle">Choose a file position to Export</a></h4>
      </div>
      <div class="modal-body"><a class="FontModals">Choose a position to Export.<br>NOTE: Only anotated regions will be part of the exported files.</a>
        <p>
        <?php
        $dir=$_SESSION['folderPath'].'/input_files';
          $files1 = scandir($dir);
          $numFiles=count($_SESSION['array_path[]']);
          echo '<form enctype="multipart/form-data" action="moreuploadWithContigs.php" method="POST">';
          echo '<li><a class="FontModals">Position:</a></li><select class="form-control" name="exportGenome">';
          for($i=0; $i < $numFiles;$i++){
              $filenumber=$i+1;
              echo' <option value="'.$filenumber.'...'.$_SESSION['array_path[]'][$i].'">'.$filenumber.'</option>';
          }
          echo '</select>';

          echo '<li><a class="FontModals">Export type:</a></li><select class="form-control" name="ExportType">';
          echo' <option value="gff">GFF+FASTA</option>';
          echo '</select><p>&nbsp</p>';
          echo '<input type="submit" class="btn btn-primary btn-lg" name="align-button" value="Export File" />';
          echo '</form>';
        ?></p>
</div>
        <div class="modal-footer">
            <button type="button" class="btn btn-default btn-lg" data-dismiss="modal">Close</button>
        </div>
    </div>
  </div>
</div>

<div class="modal fade" id="myModalDownloadExport" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel"><a class="FontModalsTitle">Download your files here</a></h4>
      </div>
      <div class="modal-body">
        <?php
        if($moreContigs=='yes') echo "<li><a class='FontModals'>Only contigs with annotations were exported. To export the others, annotate those regions.<br></a></li>";
          echo "<li><a class='FontModals'>Choose the files to download:</a></li>";

        if ($Contigexp=='yes'){
          echo '<li><a style="font-size:18px;" href="uploads/'.$wherePath.'/FastaToExport/'.$justName.'_newP.fasta" target="_blank">Download the .fasta file</a></li>';
          echo '<li><a style="font-size:18px;" href="uploads/'.$wherePath.'/Results/'.$wherePath.'.gff" target="_blank">Download the .gff file</a></li>';
        }
        else{
        if (strlen($RegionsToExport)>0 && $moreContigs=='yes') echo '<li><a style="font-size:18px;" href="uploads/'.$wherePath.'/FastaToExport/'.$justName.'_newP.fasta" target="_blank">Download the .fasta file</a></li>';
        else echo '<li><a style="font-size:18px;" href="uploads/'.$wherePath.'/FastaToExport/'.$justName.'_new.fasta" target="_blank">Download the .fasta file</a></li>';
        echo '<li><a style="font-size:18px;" href="uploads/'.$wherePath.'/Results/'.$wherePath.'.gff" target="_blank">Download the .gff file</a></li>';
        }
        ?>
</div>
        <div class="modal-footer">
            <button type="button" class="btn btn-default btn-lg" data-dismiss="modal">Close</button>
        </div>
    </div>
  </div>
</div>

<div class="modal fade" id="myModalDownloadSequence" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel"><a class="FontModalsTitle">See your sequence</a></h4>
      </div>
      <div class="modal-body">
        <?php
        $partsG = explode("...", $queryGene);
        $part = str_replace("---", "_", $partsG[1]);
        echo '<li><a style="font-size:18px;" href="uploads/'.$wherePath.'/Sequence_files/'.$part.'_sequence.fasta" target="_blank">Download the sequence file</a></li>';
        ?>
</div>
        <div class="modal-footer">
            <button type="button" class="btn btn-default btn-lg" data-dismiss="modal">Close</button>
        </div>
    </div>
  </div>
</div>

<div class="modal fade" id="myModalShowError" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel"><a class="FontModalsTitle">Error</a></h4>
      </div>
      <div class="modal-body"><li><a class='FontModals'>Please choose a file to upload.<br>You only can upload one of the supported files. (.fasta, .gbk, .gff)</a></li>
</div>
        <div class="modal-footer">
            <button type="button" class="btn btn-default btn-lg" data-dismiss="modal">Close</button>
        </div>
    </div>
  </div>
</div>

<div class="modal fade" id="myModalShowGFFBLAST" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel"><a class="FontModalsTitle">Error</a></h4>
      </div>
      <div class="modal-body"><li><a class='FontModals'>Only files with information on sequences can be used with BLAST. <br>GFF files do not have sequence information.</a></li>
</div>
        <div class="modal-footer">
            <button type="button" class="btn btn-default btn-lg" data-dismiss="modal">Close</button>
        </div>
    </div>
  </div>
</div>

<div class="modal fade" id="myModalShowUndValue" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel"><a class="FontModalsTitle">Error</a></h4>
      </div>
      <div class="modal-body"><li><a class='FontModals'>An undefined value was used for Minimum Identity or Minimum Alignment. Choose a value between 0 and 1 for Minimum Identity and bigger that 0 for Minimum Alignment.</a></li>
</div>
        <div class="modal-footer">
            <button type="button" class="btn btn-default btn-lg" data-dismiss="modal">Close</button>
        </div>
    </div>
  </div>
</div>

<div class="modal fade" id="myModalShowUndValueBLAST" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel"><a class="FontModalsTitle">Choose valid parameters</a></h4>
      </div>
      <div class="modal-body"><li><a class='FontModals'>An undefined value was used for E-value or Minimum Alignment. Choose a value bigger than 0 for E-value and Minimum Alignment.</a></li>
</div>
        <div class="modal-footer">
            <button type="button" class="btn btn-default btn-lg" data-dismiss="modal">Close</button>
        </div>
    </div>
  </div>
</div>

<div class="modal fade" id="myModalShowUndGenomes" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel"><a class="FontModalsTitle">Choose different Files</a></h4>
      </div>
      <div class="modal-body"><li><a class='FontModals'>Please choose different files to work as reference and as query.</a></li>
</div>
        <div class="modal-footer">
            <button type="button" class="btn btn-default btn-lg" data-dismiss="modal">Close</button>
        </div>
    </div>
  </div>
</div>

<div class="modal fade" id="myModalShowErrorSearch" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel"><a class="FontModalsTitle">Error</a></h4>
      </div>
      <div class="modal-body"><li><a class='FontModals'>Please type a valid term on the searchbox.</a></li>
</div>
        <div class="modal-footer">
            <button type="button" class="btn btn-default btn-lg" data-dismiss="modal">Close</button>
        </div>
    </div>
  </div>
</div>

<div class="modal fade" id="myModalShowErrorTypeUpload" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel"><a class="FontModalsTitle">Error</a></h4>
      </div>
      <div class="modal-body"><li><a class='FontModals'>For the option GFF + FASTA, you need to upload a sequence file (.fasta) and an annotation file (.gff) at the same time.</a></li>
</div>
        <div class="modal-footer">
            <button type="button" class="btn btn-default btn-lg" data-dismiss="modal">Close</button>
        </div>
    </div>
  </div>
</div>


<div class="modal fade" id="myModalShowErrorAfterUpload" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel"><a class="FontModalsTitle">Error</a></h4>
      </div>
      <div class="modal-body"><li><a class='FontModals'>There was an error when uploading the file.</a></li>
</div>
        <div class="modal-footer">
            <button type="button" class="btn btn-default btn-lg" data-dismiss="modal">Close</button>
        </div>
    </div>
  </div>
</div>

<div class="modal fade" id="myModalFiles" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel"><a class="FontModalsTitle">Upload Complete</a></h4>
      </div>
      <div class="modal-body">
        <?php
          
          $numFiles=count($_SESSION['FilesUploaded']);

          for($i=0; $i < $numFiles;$i++){
              $filenumber=$i+1;
              echo "<li><a class='FontModals'>The file ".$_SESSION['FilesUploaded'][$i]." has been uploaded."."</a></li>";
          }

          if ($_SESSION['headerMoreUpload']!='yes'){
            unset($_SESSION['headerMoreUpload']);
            unset($_SESSION['FilesUploaded']);
          }
          else $_SESSION['headerMoreUpload']='no';

        ?>
</div>
        <div class="modal-footer">
            <button type="button" class="btn btn-default btn-lg" data-dismiss="modal">Close</button>
        </div>
    </div>
  </div>
</div>

<div class="modal fade" id="myModaldashboard" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel"><a class="FontModalsTitle">Statistics</a></h4>
      </div>
      <div class="modal-body" id="modalDashBody">
        <form id="statFile" name="statFile">
        <li class='FontModals'>Select an option to visualize the statistics</li>
      <select class="form-control" id="selectStat"> 
        <?php
        $numFiles=count($path_value);
          for($i=0; $i < $numFiles;$i++){
              $filenumber=$i+1;
              $fileName=explode('/',$_SESSION['array_path[]'][$i]);
              echo'<option value="'.$i.'">'.$fileName[3].'</option>';
          }
          if ($numFiles>1) echo '<option value="all">All Files</option>';
        ?>
</select><br>
      <input class='btn btn-primary btn-lg' value='Check Statistics' onclick="dash()"/></form>
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
        <h4 class="modal-title" id="myModalLabel"><a class="FontModalsTitle">Statistics</a></h4>
      </div>
      <div class="modal-body" id="modalDashBody1">
        <form id="statFile1" name="statFile1">
        <li class='FontModals'>Select an option to visualize the statistics</li>
      <select class="form-control" id="selectStat"> 
        <?php
        $numFiles=count($path_value);
          for($i=0; $i < $numFiles;$i++){
              $filenumber=$i+1;
              $fileName=explode('/',$_SESSION['array_path[]'][$i]);
              echo'<option value="'.$i.'">'.$fileName[3].'</option>';
          }
          if ($numFiles>1) echo '<option value="all">All Files</option>';
        ?>
</select><br>
<input class='btn btn-primary btn-lg' value='Check Statistics' onclick="dash()"/></form><div id="nameGenome"></div>
      <div id="dashSpot"><table id="dash"><tbody><tr><td><li class='FontModals'>Histogram of Sizes</li><div id="histo"></div></td></tr><tr><td><li class='FontModals'>Pie Chart of Products</li><div id="pieChart"></div></td></tr></tbody></table></div>
        <div id="legendSpot"><table class="display dataTable" id="legend"><thead><tr><th class="legendTitle">Colour</th><th class="legendTitle">Product</th><th class="legendTitle">Counts</th><th class="legendTitle">Frequency</th></tr></thead></table></div>
        <div class="modal-footer">
        </div>
    </div>
  </div>
</div>
</div>

<div class="modal fade" id="myModalAllUndefined" tabindex="-2" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal">&times;</button>
        <h4 class="modal-title" id="myModalLabel"><a class="FontModalsTitle">Statistics</a></h4>
      </div>
      <div class="modal-body">
        <h5> <li><a class='FontModals'>All Gene Products in this file are Undefined.</a></li></h5>
        <div class="modal-footer">
          <button type="button" class="btn btn-default btn-lg" data-dismiss="modal">Close</button>
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
        <h4 class="modal-title" id="myModalLabel"><a class="FontModalsTitle">Choose an identifier and a sequence</a></h4>
      </div>
      <div class="modal-body">
        <h5> <li><a class='FontModals'>Please type a nucleotide sequence and a name to identify it.</a></li></h5>
        <div class="modal-footer">
          <button type="button" class="btn btn-primary btn-lg" data-toggle="modal" onclick="openModals()">OK</button>
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
        <h4 class="modal-title" id="myModalLabel"><a class="FontModalsTitle">Search By External Sequence</a></h4>
      </div>
      <div class="modal-body">
        <form  id="formBLAST" enctype="multipart/form-data" action="searchWithContigs.php" method="POST" onsubmit="return validateFormBLAST()">
        <li><a class='FontModals'>Insert a Sequence:</a></li><input type="text" name="SeqToSearch" class="form-control" placeholder="Sequence">
        <li><a class='FontModals'>Identifier:</a></li><input type="name" class="form-control" id="identifierS" name="identifierS" placeholder="Type a name to identify the sequence"><br>
        <br>
        <?php
          $numFiles=count($_SESSION['array_path[]']);
          echo '<li><a class="FontModals">Choose a File To Search:</a></li><select class="form-control" name="GenomeToSearch">';
          for($i=0; $i < $numFiles;$i++){
              $fileName=explode('/',$_SESSION['array_path[]'][$i]);
              $filenumber=$i+1;
              echo' <option value="'.$filenumber.'...">'.$filenumber.'&nbsp;-&nbsp;'.$fileName[3].'</option>';
          }
          echo '</select>';
        ?>
        <li><a class='FontModals'>E-value:</a></li><input type="name" class="form-control" id="edit_EvalueS" name="edit_EvalueS" placeholder="0.001">
        <li><a class='FontModals'>Miminum Alignment:</a></li><input type="name" class="form-control" id="edit_MinAlignS" name="edit_MinAlignS" placeholder="300">
        <br>
        <input type="submit" class="btn btn-primary btn-lg" name="align-button" value="Search" />
        <input type="hidden" name="SearchForSequence" value="SearchForSequence"/>
        </form>
    </div>
  </div>
</div>
</div>

<div class="modal fade" id="myModalOnlyFASTA" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel"><a class="FontModalsTitle">Error</a></h4>
      </div>
      <div class="modal-body"><li class="FontModals">Only FASTA files can be used as files with contigs data.</li>
</div>
        <div class="modal-footer">
            <button type="button" class="btn btn-default btn-lg" data-dismiss="modal">Close</button>
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