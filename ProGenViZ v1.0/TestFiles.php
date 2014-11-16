<!DOCTYPE html>

<html lang="en"><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="">
    

    <title>ProGenViZ</title>

    <!-- Bootstrap core CSS -->
    <link href="css/bootstrap.css" rel="stylesheet">
    <!-- Bootstrap theme -->
    <!--<link href="css/bootstrap-theme.min.css" rel="stylesheet">-->

    <!-- Custom styles for this template -->
    <link href="css/theme.css" rel="stylesheet">
    <link href="css/sidebar.css" rel="stylesheet">
    <link href="css/index.css" rel="stylesheet">


  <?php 
    session_start();
    session_unset(); 
    $_SESSION['alreadyShownUpload']='no';

    
  ?>

  <body bgcolor="black">

    <div class="navbar-wrapper">
      <div class="container">

        <div class="navbar navbar-inverse navbar-static-top" role="navigation">
          <div class="container">
            <div class="navbar-header">
              <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
                <span class="sr-only">Toggle navigation</span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
              </button>
              <a class="navbar-brand" href="#">ProGenViZ</a>
            </div>
            <div class="navbar-collapse collapse">
              <ul class="nav navbar-nav">
                <li class="active"><a class="navPrincipal" href="index.php">Home</a></li>
                <li><a  class="navPrincipal" href="#" data-toggle="modal" data-target="#myModalContigs">Start Using</a></li>
                <li class="dropdown">
                  <a class="navPrincipal" href="#" class="dropdown-toggle" data-toggle="dropdown">Help<b class="caret"></b></a>
                  <ul class="dropdown-menu">
                    <li><a class="navPrincipal" href="Tutorial.php">Tutorial</a></li>
                    <li class="divider"></li>
                    <li><a class="navPrincipal" href="#">Test Files</a></li>
                  </ul>
                </li>
                <li><a class="navPrincipal" href="About.php">About</a></li>
                <li><a class="navPrincipal" href="Contact.php">Contacts</a></li>
              </ul>
            </div>
          </div>
        </div>

      </div>
    </div>

  <div class="container theme-showcase">

<div id="myCarousel" class="carousel slide" data-ride="carousel">
      <!-- Indicators -->
      <ol class="carousel-indicators">
        <li data-target="#myCarousel" data-slide-to="0" class=""></li>
        <li data-target="#myCarousel" data-slide-to="1" class="active"></li>
        <li data-target="#myCarousel" data-slide-to="2" class=""></li>
      </ol>
      <div class="carousel-inner">
        <div class="item active">
          <img src="img/sequenceSearch.png" alt="" class="img-rounded" width="600" height="600" align="right">
          <div class="container" id="car1">
            <div class="carousel-caption">
              <<h1>Compare multiple prokaryotic genomes</h1>
              <p>Check for sequence similarity in different genomes.
              <br>Search for specific regions by name or product.
              <br>Choose between two visual representations, the Linear and the Hive Plot.</p>
            </div>
          </div>
        </div>
        <div class="item">
          <img src="img/exemplohive.png" alt="s" class="img-rounded" width="400" height="400" align="right">
          <div class="container" id="car2">
            <div class="carousel-caption">
              <h1>Order multi-FASTA sequences against a reference</h1><br>
              <p>Order multiple sequences against a reference using the alignment <br>software NUCmer and visualize the results.</p>
            </div>
          </div>
        </div>
        <div class="item">
          <img src="img/exemplohive2.png" alt="s" class="img-rounded" width="400" height="400" align="right">
          <div class="container" id="car3">
            <div class="carousel-caption">
              <h1>Annotate sequences</h1>
              <p>Annotate non-annotated sequences by tranfer from an annotated<br> reference using
                Prodigal to predict prokaryotic CDS locations<br> and BLAST to check for sequence similarity. <br><br>Annotate regions manually.</p>
            </div>
          </div>
        </div>
      </div>
      <a class="left carousel-control" href="#myCarousel" data-slide="prev"></a>
      <a class="right carousel-control" href="#myCarousel" data-slide="next"></a>
    </div>

      <!-- Main jumbotron for a primary marketing message or call to action -->
    
      </div>


  <div class="container marketing">

      <!-- Three columns of text below the carousel -->
      <div class="row">
        <div class="col-lg-3">
          <img src="img/Logo-IMM.png" style="width: 200px; height: 200px; position: right;">
        </div><!-- /.col-lg-4 -->
        <div class="col-lg-7">
          <!--<p id="indexText">Here are some test files that can be used:</p><p>&nbsp;</p><br>-->
          <table id="TestInfo" border="1" cellpadding="4">
          <tr><th class="testFilesTitle">File</th><th class="testFilesTitle">Descrition</th></th>
          <?php
            $dir    = 'TestFiles/';
            $files1 = scandir($dir);
            exec("python parsers/getTestFilesInfo.py TestFilesInfo.txt",$out);
            $i=0;
            for($j=2; $j < count($files1); $j++){
              echo '<tr>';
              echo '<td><a class="testFilesrows" href="TestFiles/'.$files1[$j].'">'.$files1[$j].'</a></td>';
              echo '<td class="testFilesrows">'.$out[$i].'</td>';
              echo '</tr>';
              $i=$i+1;
            }
          ?></table></p>
        </div><!-- /.col-lg-4 -->
        <div class="col-lg-1">
          <img src="img/fcul.png" style="width: 200px; height: 200px;">
        </div><!-- /.col-lg-4 -->
        


    </div>  



<div class="modal fade" id="myModalContigs" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel"><a class="FontModalsTitle">Add files to the analysis</a></h4>
      </div>
      <div class="modal-body" class="ModalsSizeFont">
                    <form name="uploadFiles" enctype='multipart/form-data' action='uploaderWithContigs.php' method='POST' onsubmit="return validateForm();">
                           <li class="FontModals">Choose an Option:</li><select id="inputType" class="form-control" name="typeUpload" onchange="showToUpload()">
                                     <option value="yes" class="FontModals">GFF+Fasta</option>
                                     <option value="no" class="FontModals">Others</option></select>
                          <div id="fileOther"></div>
                          <div id="fileGFF+FASTA"><br><li class="FontModals">Choose a .gff file:</li> <input name='moreuploadedfileGFF[]' type='file' class='btn btn-default btn-lg'/>
                          <br><li class="FontModals">Choose a .fasta file:</li> <input id="fileFASTA" name='moreuploadedfileFASTA[]' type='file' class='btn btn-default btn-lg'/><br></div>
                          <input type="checkbox" name="Iscontig" value="yes"><a class="FontModals">&nbsp;It is a file with contigs data</a><br>
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

    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="js/jquery-2.0.3.min.js"></script>
    <script src="js/bootstrap.min.js"></script>
    <script src="js/holder.js"></script>
    
    <script>  


      function showToUpload() {
        var selected=document.getElementById("inputType").value;
        if (selected=='no'){
          document.getElementById("fileGFF+FASTA").innerHTML="";
          document.getElementById("fileOther").innerHTML="<br><li class='FontModals'>Choose one of the supported file formats (.fasta, .gbk, .gff): </li><input name='moreuploadedfile[]' type='file' class='btn btn-default btn-lg'/><br>";
        }
        if (selected=='yes'){
          document.getElementById("fileOther").innerHTML="";
          document.getElementById("fileGFF+FASTA").innerHTML="<br><li class='FontModals'>Choose a GFF file: </li><input name='moreuploadedfileGFF[]' type='file' class='btn btn-default btn-lg'/><br><li class='FontModals'>Choose a FASTA file: </li><input name='moreuploadedfileFASTA[]' type='file' class='btn btn-default btn-lg'/><br>";
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

      $(function ()  
          { $("#compare_files_contigs").popover();    //say that this element is a popover.
          });
      $(function ()  
          { $("#compare_files_genes").popover();    //say that this element is a popover.
          }); 

      $('.dropdown-menu').click(function (e) { //necessary to prevent dropdown-menu from closing
        e.stopPropagation();
        }); 
    </script>



</body>

  <!--MODALS-->
<div class="modal fade" id="myModalShowError" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel"><a class="FontModalsTitle">Error</a></h4>
      </div>
      <div class="modal-body"><li class="FontModals">Please choose a file to upload.<br>You only can upload one of the supported files. (.fasta, .gbk, .gff)</li>
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
      <div class="modal-body"><li class="FontModals">For the option GFF + FASTA, you need to upload a sequence file (.fasta) and an annotation file (.gff) at the same time.</li>
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