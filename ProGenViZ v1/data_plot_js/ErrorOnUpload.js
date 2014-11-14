
if (document.URL.search('uploaderWithContigs.php')==-1){
 $(window).load(function(){
          $('#myModalShowErrorAfterUpload').modal('show');
      });
}
else{
 $(window).load(function(){
          $('#myModalAdd').modal('show');
      });
}
