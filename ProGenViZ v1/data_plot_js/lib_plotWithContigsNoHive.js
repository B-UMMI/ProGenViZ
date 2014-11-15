// lib_plot.js

//MODAL show
if(showfaa=='yes' && hasfaa == 'yes'){
  $(window).load(function(){
          $('#hasfaa').modal('show');
      });

}

if(modalDownloadExport == 'yes'){
            $(window).load(function(){
              $('#myModalDownloadExport').modal('show');
        });
}

if(ModalSequence == 'yes'){
            $(window).load(function(){
              $('#myModalDownloadSequence').modal('show');
        });
}

if(errorFile == 'yes'){
            $(window).load(function(){
              $('#myModalShowErrorAfterUpload').modal('show');
        });
}

if(numFilesUploaded>0 && errorUpload == 'no' && alreadyShownUpload=='no'){
            $(window).load(function(){
              $('#myModalFiles').modal('show');
        });
}


//Function that creates the visualization
var setup_plot = function(plot_info) {

  console.log(plot_info.global);

  var g = plot_info.global;

  g.angle_dom = [], g.angle_rng = [];

  axes_info = plot_info.axes;
  for (var axis_name in axes_info) {
    axis_info = axes_info[axis_name];
    g.angle_dom.push(axis_name);
    g.angle_rng.push(axis_info.angle);
  }


  g.angle_f     = d3.scale.ordinal().domain(g.angle_dom).range(g.angle_rng);

  g.color_f     = d3.scale.category20();


  g.svg         = d3.select(g.selector + ' .chart')
                    .append('svg')
                    .attr('id','mysvg')
                      .attr('width',      g.x_max)
                      .attr('height',     g.y_max)
                      .append("g");

};

var degrees = function(radians) { return radians / Math.PI * 180 - 90; }


var display_plot = function(plot_info) {

  var g = plot_info.global;
  allInfo=plot_info.global;

  var countGenome = 0;
  var bigger=0;
  var longerGenome = function (type) {
    countGenome++;
    if (type.count>bigger){
      bigger=type.count;
    }
  }

  NumberOfColors=0;
  ArrayOfColors=[];
  ArrayOfProducts=[];
  ArrayOfProductCount=[];
  ArrayOfSizes={};

  //Creates random colours according to the number of total functions
  for (i in g.nodesByType) {
    for (j in g.nodesByType[i].values){
      var ToPush=g.nodesByType[i].values[j].product.replace(',','');
      if (ArrayOfProducts.indexOf(ToPush)==-1){
       ArrayOfProducts.push(ToPush);
     }
     geneL=parseInt(g.nodesByType[i].values[j].end)-parseInt(g.nodesByType[i].values[j].begin);
      if (biggestGene<geneL && g.nodesByType[i].values[j].product!='Undefined'){
       biggestGene=geneL;
      }
    }
  }

  NumberOfColors=ArrayOfProducts.length;

  Math.seedrandom(0);
  function getRandomColor() {
    var color = '#' + Math.random().toString(16).substring(2, 8);
    return color;
  }

  for (var i=0;i<NumberOfColors;i++){
    ArrayOfColors.push(getRandomColor());
  }

  g.nodesByType.forEach(longerGenome);


  g.outer_radius=(bigger/1000)*g.outer_radius;  
  
  var radii     = [ -(g.outer_radius/2), (g.outer_radius/2) ];
  var radii_axis  = [ g.inner_radius, g.outer_radius + g.inner_radius ];

  g.radius_f    = d3.scale.linear().range(radii);

  g.radius_axis = d3.scale.linear().range(radii_axis);
  

  g.transform   = 'translate(' + g.x_off + ',' + g.y_off + ')' + 'scale(' + 0.03 + ')';


  var index   = function(d) { return d.index; };

  var extent  = d3.extent(g.nodes, index);
  g.radius_f.domain([0,bigger]);
  g.radius_axis.domain([0,bigger]);


g.svg.append('rect')
      .attr('width',      g.x_max)
      .attr('height',     g.y_max)
      .attr('fill','white')
      .call(d3.behavior.zoom().translate([g.x_off,g.y_off]).scale(0.03).on("zoom", function(){ zoom(d3.event.sourceEvent);}))
      .on('mousedown', function(){ onMouseDownRect(d3.event,this);})
      .append('g');


g.svg.graph = d3.selectAll('g').append('g').attr('transform',g.transform);


  var transform = function(d) {
    return 'rotate(' + degrees(1.575) + ')';
  };

  var inicialY1 = -2000, inicialY2 = -2000, prevY = -2000, prevType="Str1";
  
  var prevYChange= function(d){
    if (prevType!=d.node.type){
      prevY+=2500;
      prevType=d.node.type;
    }
    return prevY;
  }

  var x1 = function(d) { return -(g.radius_axis(bigger)/2);};
  var x2 = function(d) { return (-(g.radius_axis(bigger)/2) + g.radius_axis(d.count)); };

  var y1 = function(d) { 
                        var y1Local = inicialY1;
                        inicialY1+= 2500;
                        return y1Local;
                      };

  var y2 = function(d) { var y2Local = inicialY2;
                        inicialY2+= 2500;
                        return y2Local;
                       };

  function getKey(d){ return d.key;};

  g.svg.graph.selectAll('.axis')
    .data(g.nodesByType)
    .enter().append('line')
      .attr('id',getKey)
      .attr('class', 'axis')
      .attr('transform', transform)
      .attr('x1', x1)
      .attr('x2', x2)
      .attr('y1', y1)
      .attr('y2', y2);


  var path_angle  = function(d) { return g.angle_f(d.type);    }; 
  var path_radius = function(d) { return g.radius_f(d.node.index); };


  var positions = new Array();

  var connectors  = function(d) { return d.connectors; };
  var cx          = function(d) { return g.radius_f(d.node.index); };
  var fill        = function(d) { var index = ArrayOfProducts.indexOf(d.packageName);
                                  return ArrayOfColors[index]; };
  var fillEllipse = function (d) { return g.color_f(d.node.packageName);};



  var transform   = function(i) {
    return 'rotate(' + degrees(1.575) + ')';
  };

  var countNode = -1;
  var idNode = function(d){ countNode+=1;
                             return countNode;
                           }

var counts=-1;
var countsEllipse=-1;

var AllValuesSame = function(d){

    if(d.length > 0) {
        for(var i = 0; i < d.length - 1; i++)
        {  
            if(d[i] != d[0])
                return false;
        }
    } 
    return true;
}


if (sel!='undefined'){
  var genomes=new Array();
  for (geno in sel){
    genomes.push(sel[geno].genome);
  }
  var sameGenome= AllValuesSame(genomes);
  sel.push({index : 'null', genome: 'null'});
}

var arrayOfImported=new Array();


var selName=new Array();
for (j in sel){
  selName.push(sel[j].gene);
}


var MinMaxIndex=new Array();
var Min=sel[0].index;
var Max=sel[0].index;
var PrevNodeGenome=sel[0].genome;

var getMaxMinIndex = function (d){
  if (d.genome==PrevNodeGenome) {
    if (d.index< Min) Min=d.index;
    if (d.index> Max) Max=d.index;
  }
  else{
    MinMaxIndex.push({min : Min, genome: PrevNodeGenome,  max : Max});
    PrevNodeGenome = d.genome;
    Min=d.index;
    Max=d.index;
  }
}

if (sel!='undefined') sel.forEach(getMaxMinIndex);

var CheckSelection =function(d){
                          if(sel == 'undefined') return 'yes';
                          else{
                            if (sameGenome){
                                if(d.genome!=genomes[0]) return 'yes';
                                for (x in sel){
                                  if (sel[x].genome == d.genome && sel[x].index == d.index) return 'yes';
                                }
                            }
                            else{
                              for (selec in sel){
                                if (sel[selec].genome == d.genome && sel[selec].index == d.index) return 'yes';
                                
                              }
                            }
                          }
                        }

var SelectionArrayRect = new Array();

for( i in g.nodesByType){
  var geneBegin='...';
  var geneEnd='...';
  var moreContigs=g.nodesByType[i].moreContigs;
  g.svg.graph.append('g')
    .attr('class', 'nodes')
    .selectAll('.node')
    .data(g.nodesByType[i].values)
    .enter().append('g')
    .filter(function (d){if (exclude_hypothetical=='yes'){
                if (d.product.indexOf('hypothetical protein') > -1);
                else return d;
              } 
              else return d;})
      .attr('class', 'node')
      .attr('genomePosition',function(d){ return d.genome;})
      .attr('geneName',function(d){return d.gene;})
      .attr('geneSequence',function(d){return d.sequence;})
      .attr('geneProduct',function(d){return d.product;})
      .attr('geneBegin',function(d){return d.begin;})
      .attr('geneEnd',function(d){return d.end;})
      .attr('reference',function(d){return d.reference;})
      .attr('contig',function(d){return d.contig;})
      .attr('moreContigs',function(){return moreContigs;})
      .attr('id', idNode)
      .style('fill', function (d,i){
                                    counts+=1;
                                    if (d.gene.indexOf('Undefined_Region') > -1) var color='black';
                                    else var color = fill(d);
                                    var backup = 'fill:'+color;
                                    
                                    document.getElementById((counts).toString()).setAttribute("backupColor",backup);
                                    return color;})
      
      .selectAll('ellipse')
      .data(connectors)
      .enter().append('ellipse')
        .attr('transform', transform(i))
        .style('stroke', function (d){  countsEllipse+=1;
                                        if (d.node.begin==''){ return 'black';
                                                                document.getElementById((countsEllipse).toString()).firstChild.setAttribute("strokeColor",'black');
                                                              }
                                        if (geneBegin!=d.node.begin && geneEnd!=d.node.begin) {
                                                            geneBegin=d.node.begin;
                                                            geneEnd=d.node.end;
                                                            document.getElementById((countsEllipse).toString()).firstChild.setAttribute("strokeColor",'black');
                                                            return 'black';
                                        }
                                        else{
                                          var stroke = fillEllipse(d);
                                          var backup = 'stroke:' + stroke;
                                          document.getElementById((countsEllipse).toString()).firstChild.setAttribute("strokeColor",backup);
                                          geneBegin=d.node.begin;
                                          geneEnd=d.node.end;
                                          return stroke;
                                        }
                                      })
        .attr('cx', cx)
        .attr('cy', function(d){ return prevYChange(d);})
        .attr('rx', 180)
        .attr('ry', function (d){  isInSelection=CheckSelection(d.node);
                                  if(isInSelection!='yes');
                                  else return 300;})
        .attr('file', function(d){
                                fName=fileNames.split("---")[i];
                                fName1=fName.split(' ');
                                if (fName1.length>1){
                                  toSee='';
                                  for (j=0;j<fName1.length;j++){
                                    if (j==fName1.length-1) toSee=toSee+fName1[j].split("/")[3];
                                    else toSee=toSee+fName1[j].split("/")[3]+" + ";
                                  }
                                  return toSee;
                                }
                                else{
                                fName=fName.split("/")[3];
                                return fName;
                                }})
        .on('mouseover', on_mouseover_node)
        .on('mouseout',  on_mouseout)
        .on('mousedown', function(){ onMouseDown(d3.event,this);})
        .on('mouseup', function(){ onMouseUp(d3.event);});

}


var SelectionArrayMouse = new Array();

var ArrayEllipse=new Array();
var prevEllipse;


//Information for the General Information Table
var numberOfContigs=1;
var moreContigs='no';
var moreContigs2='no';
for(var i=0;i<g.nodesByType.length;i++){
  lengthtype=g.nodesByType[i].values.length;
  var hypocount=0;
  var transposaseCount=0;
  var IScount=0;
  var prevBegin=".";
  var allUndefined='yes';
  var countNodesGenes=0;
  var NodesAnnotatedSize=0;
  var prevContig='';
  numberOfContigs=0;
  moreContigs='no';
  countNodesGenes=0;
  for (var y=0;y<lengthtype;y++){
    if (prevBegin!=g.nodesByType[i].values[y].begin){
      prevBegin=g.nodesByType[i].values[y].begin;
      if(g.nodesByType[i].values[y].product.indexOf('hypothetical') > -1) hypocount+=1;
      if(g.nodesByType[i].values[y].product.indexOf('IS') > -1 || g.nodesByType[i].values[y].product.indexOf('insertion sequence') > -1) IScount+=1;
      if(g.nodesByType[i].values[y].product.indexOf('transposase') > -1) transposaseCount+=1;
      if(g.nodesByType[i].values[y].product.indexOf('Undefined') == -1){
       allUndefined='no';
       countNodesGenes+=1;
       NodesAnnotatedSize+=parseInt(g.nodesByType[i].values[y].end)-parseInt(g.nodesByType[i].values[y].begin)
      }
    }
    if(g.nodesByType[i].values[y].contig != prevContig){
        prevContig=g.nodesByType[i].values[y].contig;
        numberOfContigs+=1;
        if (numberOfContigs>1){
          moreContigs='yes';
          moreContigs2='yes';

        }
    }
  }
  fileNames1=fileNames.split("---")[i];
  fileNames1=fileNames1.split("/")[3];
  if (g.nodesByType[i].values[0].genomeType=="COMPLETE") InfoArray.push({ fileName: fileNames1 , genome : i+1 , name : g.nodesByType[i].values[0].name , genomeSize : g.nodesByType[i].values[0].genomeSize , AnnotatedG : gString(NodesAnnotatedSize) , NumberofGenes : "0" , fileType : g.nodesByType[i].values[0].fileType , hypotheticals : parseFloat((parseFloat(hypocount)/parseFloat(countNodesGenes))*100).toFixed(2) , transposaseCount: transposaseCount , IScount : IScount, numberOfcontigs : '-'});
  else if (moreContigs=='yes' && allUndefined=='no') InfoArray.push({ fileName: fileNames1 , genome : i+1 , name : "Contigs File" , genomeSize : g.nodesByType[i].values[lengthtype-1].AnnotatedG , AnnotatedG : String(NodesAnnotatedSize) , NumberofGenes : String(countNodesGenes) , fileType : g.nodesByType[i].values[0].fileType , hypotheticals : parseFloat((parseFloat(hypocount)/parseFloat(countNodesGenes))*100).toFixed(2) , transposaseCount: transposaseCount , IScount : IScount , numberOfcontigs : numberOfContigs});
  else if (moreContigs=='yes') InfoArray.push({ fileName: fileNames1 , genome : i+1 , name : "Contigs File" , genomeSize : g.nodesByType[i].values[lengthtype-1].AnnotatedG , AnnotatedG : "NaN" , NumberofGenes : "NaN" , fileType : g.nodesByType[i].values[0].fileType , hypotheticals : "NaN" , transposaseCount: "NaN" , IScount : "NaN" , numberOfcontigs : numberOfContigs});
  else InfoArray.push({ fileName: fileNames1 , genome : i+1 , name : g.nodesByType[i].values[0].name , genomeSize : g.nodesByType[i].values[0].genomeSize , AnnotatedG : String(NodesAnnotatedSize) , NumberofGenes : String(countNodesGenes) , fileType : g.nodesByType[i].values[0].fileType , hypotheticals : parseFloat((parseFloat(hypocount)/parseFloat(countNodesGenes))*100).toFixed(2) , transposaseCount: transposaseCount , IScount : IScount , numberOfcontigs : '-'});

}

//Information table Creation
var tableInfo = document.getElementById('InfoTable');
Tbody=document.createElement("tbody");
tableInfo.appendChild(Tbody);
header=tableInfo.createTHead();
row=header.insertRow(0);
for (var y=0;y<11;y++){
  cell=row.insertCell(y);
  cell.style.textAlign = 'center';
  if(y==0)cell.innerHTML='<h5 class="FontTitleTables">File Name</h5>';
  if(y==1)cell.innerHTML='<h5 class="FontTitleTables">Genome Position</h5>';
  if(y==2)cell.innerHTML='<h5 class="FontTitleTables">Name</h5>';
  if(y==3)cell.innerHTML='<h5 class="FontTitleTables">Total Size</h5>';
  if(y==4)cell.innerHTML='<h5 class="FontTitleTables">Annotated Portion</h5>';
  if(y==5)cell.innerHTML='<h5 class="FontTitleTables">File Type</h5>';
  if(y==6)cell.innerHTML='<h5 class="FontTitleTables">Number of Annotations</h5>';
  if(y==7)cell.innerHTML='<h5 class="FontTitleTables">Number of Transposases</h5>';
  if(y==8)cell.innerHTML='<h5 class="FontTitleTables">Number of IS</h5>';
  if(y==9)cell.innerHTML='<h5 class="FontTitleTables">% of Hypothetical Proteins</h5>';
  if (moreContigs2=='yes'){
    if(y==10)cell.innerHTML='<h5 class="FontTitleTables">Number Of Contigs</h5>';
  }
}

var lengthinfoarray=InfoArray.length;
for(var i=0; i<lengthinfoarray; i++){
  row=Tbody.insertRow(i);
  for (var j=0;j<11;j++){
    cell=row.insertCell(j);
    cell.style.textAlign = 'center';
    if(j==0){
      if (InfoArray[i].fileName != "NaN")cell.innerHTML='<h5 class="FontTables">'+InfoArray[i].fileName+'</h5>';
      else cell.innerHTML='-';
    }
    if(j==1){
      if (InfoArray[i].genome != "NaN")cell.innerHTML='<h5 class="FontTables">'+InfoArray[i].genome+'</h5>';
      else cell.innerHTML='-';
    }
    if(j==2)cell.innerHTML='<h5 class="FontTables">'+InfoArray[i].name+'</h5>';
    if(j==3){
      if (InfoArray[i].genomeSize != "NaN"){
        if (InfoArray[i].genomeSize=="undefined") cell.innerHTML='<h5 class="FontTables">'+InfoArray[i].genomeSize+'</h5>';
        else cell.innerHTML='<h5 class="FontTables">'+InfoArray[i].genomeSize+" bp"+'</h5>';
      }
      else cell.innerHTML='-';
    }
    if(j==4){
      if (InfoArray[i].AnnotatedG != "NaN"){
        if (InfoArray[i].AnnotatedG=="undefined") cell.innerHTML='<h5 class="FontTables">'+InfoArray[i].AnnotatedG + " bp"+'</h5>';
        else cell.innerHTML='<h5 class="FontTables">'+InfoArray[i].AnnotatedG + " bp  (" + parseFloat((parseFloat(InfoArray[i].AnnotatedG)/parseFloat(InfoArray[i].genomeSize))*100).toFixed(2) + "%)"+'</h5>';
      }
      else cell.innerHTML='-';
    }
    if(j==5){
      if (InfoArray[i].fileType != "NaN")cell.innerHTML='<h5 class="FontTables">'+InfoArray[i].fileType+'</h5>';
      else cell.innerHTML='-';
    }
    if(j==6){
      if (InfoArray[i].NumberofGenes != "NaN")cell.innerHTML='<h5 class="FontTables">'+InfoArray[i].NumberofGenes+'</h5>';
      else cell.innerHTML='-';
    }
    if(j==7){
      if (InfoArray[i].transposaseCount != "NaN")cell.innerHTML='<h5 class="FontTables">'+InfoArray[i].transposaseCount+'</h5>';
      else cell.innerHTML='-';
    }
    if(j==8){
      if (InfoArray[i].IScount != "NaN")cell.innerHTML='<h5 class="FontTables">'+InfoArray[i].IScount+'</h5>';
      else cell.innerHTML='-';
    }
    if(j==9){
      if (InfoArray[i].hypotheticals != "NaN")cell.innerHTML='<h5 class="FontTables">'+InfoArray[i].hypotheticals + "%"+'</h5>';
      else cell.innerHTML='-';
    }
    if (moreContigs2=='yes'){
      if(j==10)cell.innerHTML='<h5 class="FontTables">'+InfoArray[i].numberOfcontigs+'</h5>';
    }
  }
}

///////////////////TABLE OF GENES/////////////////////////////////////////7
/**
var table = document.getElementById('TableOfGenes');
Tbody=document.createElement("tbody");
table.appendChild(Tbody);
header=table.createTHead();
row=header.insertRow(0);
for (var y=0;y<6;y++){
  th=document.createElement("th");
  cell=row.appendChild(th);
  cell.style.textAlign = 'center';
  if(y==0)cell.innerHTML='<h5>#</h5>';
  else if(y==1)cell.innerHTML='<h5>Gene</h5>';
  else if(y==2)cell.innerHTML='<h5>Product</h5>';
  else if(y==3)cell.innerHTML='<h5>Genome Position</h5>';
  else if(y==4)cell.innerHTML='<h5>Gene Begin</h5>';
  else if(y==5)cell.innerHTML='<h5>Gene End</h5>';

}
countLinesGenes=0
prevGeneBegin=""
for (k in g.nodesByName){
  object=g.nodesByName[k];
  if (object.begin==prevGeneBegin || object.product.indexOf('Undefined') > -1) prevGeneBegin=object.begin;
  else{
    prevGeneBegin=object.begin;
    row=Tbody.insertRow(countLinesGenes);
    countLinesGenes+=1
    for (var j=0;j<6;j++){
      cell=row.insertCell(j);
      cell.style.textAlign = 'center';
      geneToUse="";
      geneArray=object.gene.split("...")[1].split('_');
      ToRemove=geneArray.splice(geneArray.length-1,1);
      ToRemove="_"+ToRemove[0];
      geneToUse=object.gene.split("...")[1].replace(ToRemove,"");

      if(j==0)cell.innerHTML=(countLinesGenes);
      else if(j==1)cell.innerHTML='<form enctype="multipart/form-data" action="searchWithContigs.php" method="POST">'+
                                        '<a href="'+"http://www.ncbi.nlm.nih.gov/gene/?term="+geneToUse+'" target="_blank">'+geneToUse+'</a>'+
                                        '<button type="submit" class="btn btn-link">  (See Position)</button>'+
                                        '<input type="hidden" name="ElementIDposition" value="'+object.indexGeral+'">'+
                                      '</form>';
      else if(j==2)cell.innerHTML=object.product;
                            
      else if(j==3)cell.innerHTML=object.genome;
      else if(j==4)cell.innerHTML=object.begin;
      else if(j==5)cell.innerHTML=object.end;

    }
  }
}
*/
/**var $rows = $('#HitTable tbody tr');
$('#search').keyup(function() {
    var val = $.trim($(this).val()).replace(/ +/g, ' ').toLowerCase();
    
    $rows.show().filter(function() {
        var text = $(this).text().replace(/\s+/g, ' ').toLowerCase();
        return !~text.indexOf(val);
    }).hide();
});*/


//Table Formating
$(document).ready( function () {
        var table = $('#InfoTable').dataTable ( {
          "sDom": 'T<"clear">C<"clear">Rlfrtip',
          "oTableTools": {
            "aButtons": [
                        {
                        "sExtends":    "collection",
                        "sButtonText": "Save",
                        "aButtons":    [ {
                                           "sExtends": "csv"
                                         }, 
                                         {
                                           "sExtends": "xls"
                                         }, 
                                         {
                                           "sExtends": "pdf",
                                           "sPdfOrientation": "landscape",
                                           "sPdfMessage": "The format of the table isn't fully compatible. I'm sorry for the inconvenience."
                                         }
                                       ]
                        },
                        "copy",
                        "print"
      ]
          },
        } );
      } );


///////////////////////////////////////////////////////////////////////////////////////////////////////////////////


function include(arr,obj) {
    for (i in arr){
      if (arr[i].node.begin==obj.node.begin && arr[i].node.genome==obj.node.genome) return true;
    }
}

//Zoom Function
function zoom(e) {
  if (e.which==1 || e.which==2){
    g.svg.graph.attr("transform","translate(" + d3.event.translate + ")"+ " scale(" + d3.event.scale + ")");
  }
}

//Mouse down over nodes
function onMouseDown(e,ellipse){
  if (e.ctrlKey);
  else {

        if (e.which==3);
        else {g.svg.selectAll('ellipse').each(function (d){                                                                                                                                                                                                                                      
                                                      var ellipseStyle= this.getAttribute("backupColor");
                                                      var ellipseStroke= this.getAttribute("strokeColor");
                                                      this.setAttribute("style",ellipseStyle);
                                                      this.setAttribute("style",ellipseStroke);});
        }
        ArrayEllipse=new Array();

  }

  if (e.which==3);
  else{
    SelectionArrayMouse.length=0;
    ellipse.setAttribute("style","fill:green");
    prevEllipse=ellipse;
    g.svg.selectAll('ellipse').on('mousemove',function(){onMouseMove(d3.event,this);});    
   }    
}

//Mouse up over nodes
function onMouseUp(e){
  g.svg.selectAll('ellipse').on('mousemove',null);
  if (e.ctrlKey);
  else {

        g.svg.selectAll('ellipse').each(function (d){ var PresentColor=this.getAttribute("style");                                                     
                                                      if (PresentColor=='fill:green') SelectionArrayMouse.push({index : d.node.index, genome: d.node.genome, gene:d.node.gene});
                                                    });                                                                                                                                                                                                                                      
                                                      

  }
}

//Mouse move over nodes
function onMouseMove(e,ellipse){
  if (ellipse==prevEllipse);
  else{
    var indexE=ArrayEllipse.indexOf(ellipse);
    if(indexE > -1){
      var prevStyle= prevEllipse.getAttribute("backupColor");
      var prevStroke= prevEllipse.getAttribute("strokeColor");
      prevEllipse.setAttribute("style",prevStyle);
      prevEllipse.setAttribute("style",prevStroke);
      ArrayEllipse.splice(indexE,1);
      prevEllipse=ellipse;
    }
    else{
      ArrayEllipse.push(ellipse);
      ellipse.setAttribute("style","fill:green");
      prevEllipse=ellipse;

    }
  }
  
}

function onMouseDownRect(e){
  if (e.ctrlKey);
  else {

        if (e.which==3);
        else {g.svg.selectAll('ellipse').each(function (d){                                                                                                                                                                                                                                      
                                                      var ellipseStyle= this.getAttribute("backupColor");
                                                      var ellipseStroke= this.getAttribute("strokeColor");
                                                      this.setAttribute("style",ellipseStyle);
                                                      this.setAttribute("style",ellipseStroke);});
        }

  }
  ArrayEllipse=new Array();
}

/////////////////////CONTEXT MENU////////////////////////////////////////


//Right mouse click over nodes
$(function () {

    $contextMenu = $("#contextMenu");

    $("body").on("contextmenu", "svg g g", function (e) {
        Url = document.URL.split('/');
        currentpage = Url[Url.length -1];
        var positionOfThis = this.getAttribute('genomePosition');
        var presentGene = this.getAttribute('geneName');
        var geneSequence = this.getAttribute('geneSequence');
        var geneProduct=this.getAttribute('geneProduct');
        var geneBegin=this.getAttribute('geneBegin');
        var geneEnd=this.getAttribute('geneEnd');
        var geneReference=this.getAttribute('reference');
        var mContigs=this.getAttribute('moreContigs');
        geneReference=geneReference.replace(/\s/g, "---");
        geneReference=geneReference.replace(/\|/g, "...");
        presentGene=presentGene.replace(/\s/g, "---");
        geneArray=presentGene.split("...")[1].split('_');
        ToRemove=geneArray.splice(geneArray.length-1,1);
        ToRemove="_"+ToRemove[0];
        geneToUse=presentGene.split("...")[1].replace(ToRemove,"");
        $contextMenu[0].innerHTML ='';
        $contextMenu[0].innerText ='';

        Pgene1=presentGene.split("...")[1];
        Pgene2=Pgene1.split("_");
        Pgene=Pgene1.replace("_"+Pgene2[Pgene2.length-1],"");
        
        var modalChangePos='';
          var insertdrop = '<ul class="dropdown-menu" role="menu" aria-labelledby="dropdownMenu" style="display:block;position:static;margin-bottom:5px;">';
          if(SelectionArrayMouse.length>0){
                        insertdrop+='<li><form enctype="multipart/form-data" action="' + currentpage + '" method="POST" id="selectionArray">'+
                        '<button type="submit" class="btn btn-link">See Selection</button>'+
                        '<input type="hidden" name="TrySearchArray">'+
                        '<input type="hidden" name="remove_selection"></form></li><hr></hr>';   
                    }
          for (i=0;i<countGenome;i++){
            if(String(i+1) != positionOfThis){


                     insertdrop +=   '<hr></hr><li><form enctype="multipart/form-data" action="' + currentpage + '" method="POST"><input type="submit" class="btn btn-link" name="position" value="Move to position ' + String(i+1) +'" />' +
                                     '<input type="hidden" name="positionToBe" value="'+String(i)+'" />' +
                                     '<input type="hidden" name="currentPosition" value="'+String(parseInt(positionOfThis) - 1 )+'" />' +
                                     '</form></li>';
                
            }
          
          }

          insertdrop+= '<hr></hr><form enctype="multipart/form-data" action="' + currentpage + '" method="POST">'+
                                    '<input type="hidden" name="GetSequence" value="GetSequence">'+
                                    '<input type="hidden" name="geneReference" value="'+geneReference+'">'+
                                    '<input type="hidden" name="queryGene" value="'+presentGene+'" />'+
                                    '<button href="#" type="submit" class="btn btn-link">Get Sequence</button></form>';

          if (mContigs=='yes'){
            var contigToExport=this.getAttribute('contig');
            insertdrop+= '<hr></hr><form enctype="multipart/form-data" action="' + currentpage + '" method="POST">'+
                                    '<input type="hidden" name="exportContig" value="exportContig">'+
                                    '<input type="hidden" name="GenomeToExport" value="'+positionOfThis+'">'+
                                    '<input type="hidden" name="contigToExport" value="'+contigToExport+'" />'+
                                    '<input type="hidden" name="ExportType" value="gff" />'+
                                    '<button href="#" type="submit" class="btn btn-link">Export Contig</button></form>';
          }

          if (countGenome>1){
          insertdrop+= '<hr></hr><div class="modal fade" id="myModalsequenceParameters" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">'+
                                  '<div class="modal-dialog">'+
                                    '<div class="modal-content">'+
                                    '<form enctype="multipart/form-data" id="formBLAST1" name="formBLAST1" action="searchWithContigs.php" method="POST" onsubmit="return validateFormBLAST1();">'+
                                      '<div class="modal-header">'+
                                        '<button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>'+
                                        '<h4 class="modal-title" id="myModalLabel"><a class="FontModalsTitle">Choose the E-value and Minimum Alignment</a></h4>'+
                                      '</div>'+
                                      '<div class="modal-body">'+
                                        '<div class="form-group">';
          if(String(countGenome)==String(positionOfThis)) insertdrop+='<input type="hidden" name="refgenome" value="1" />';
          else insertdrop+='<input type="hidden" name="refgenome" value="'+String(parseInt(positionOfThis) + 1 )+'" />';

                              insertdrop+='<input type="hidden" name="rundatabasesearch" value="rundatabasesearch" />'+
                                          '<label for="edit_Evalue"><li class="FontModals">E-value:</li></label><input type="name" class="form-control" id="edit_Evalue" name="edit_Evalue" placeholder="0.001">'+
                                          '<label for="edit_Align"><li class="FontModals">Miminum Alignment:</li></label><input type="name" class="form-control" id="edit_Align" name="edit_Align" placeholder="300">'+
                                          '<input type="hidden" name="querygene" value="'+presentGene+'" />'+
                                          '<input type="hidden" name="geneBegin" value="'+geneBegin+'">'+
                                          '<input type="hidden" name="geneEnd" value="'+geneEnd+'">'+
                                          '<input type="hidden" name="geneReference" value="'+geneReference+'">'+
                                        '</div>'+
                                     '</div><div class="modal-footer">'+
                                      '<button type="button" class="btn btn-default btn-lg" data-dismiss="modal">Close</button>'+
                                      '<button type="submit" class="btn btn-primary btn-lg" name="CheckSimilarity">Check Similarity</button></div></div></div></div></form>'+
                                    '<button href="#" data-toggle="modal" data-target="#myModalsequenceParameters" class="btn btn-link">BLAST ' + geneToUse + ' against next position sequences.</button>';
          }

          /*
          insertdrop+= '<hr></hr><form enctype="multipart/form-data" action="searchWithContigs.php" method="POST">'+
                                     '<input type="hidden" name="rundatabasesearch" value="rundatabasesearch" />'+
                                     '<input type="hidden" name="searchNCBI" value="searchNCBI" />'+
                            '<input type="hidden" name="querygene" value="'+presentGene+'" />'+
                            '<input type="hidden" name="geneBegin" value="'+geneBegin+'">'+
                            '<input type="hidden" name="geneReference" value="'+geneReference+'">'+
                            '<input type="hidden" name="geneEnd" value="'+geneEnd+'">';
                            if(String(countGenome)==String(positionOfThis)) insertdrop+='<input type="hidden" name="refgenome" value="1" />';
                                     else insertdrop+='<input type="hidden" name="refgenome" value="'+String(parseInt(positionOfThis) + 1 )+'" />';
          insertdrop+= '<button type="submit" class="btn btn-link">Check sequence similarity for the gene ' + presentGene.split("...")[1] + ' in the NCBI database.</button>'+
                                    '</form>';
          
          */                        
          insertdrop+= '<hr></hr><div class="modal fade" id="myModaledit_info" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">'+
                                  '<div class="modal-dialog">'+
                                    '<div class="modal-content">'+
                                    '<form enctype="multipart/form-data" action="' + currentpage + '" method="POST">'+
                                      '<div class="modal-header">'+
                                        '<button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>'+
                                        '<h4 class="modal-title" id="myModalLabel"><a class="FontModalsTitle">Edit Information</a></h4>'+
                                      '</div>'+
                                      '<div class="modal-body">'+
                                        '<div class="form-group">'+
                                          '<label for="GeneName"><li class="FontModals">Gene Name</li></label>'+
                                          '<input type="name" class="form-control" id="GeneName" name="EditName" placeholder="'+Pgene+'">'+
                                          '<input type="hidden" name="OriginalName" value="'+presentGene+'">'+
                                          '<input type="hidden" name="geneBegin" value="'+geneBegin+'">'+
                                          '<input type="hidden" name="geneEnd" value="'+geneEnd+'">'+
                                        '</div>'+
                                      '<div class="form-group">'+
                                        '<label for="GeneProduct"><li class="FontModals">Gene Product</li></label>'+
                                        '<input type="name" class="form-control" id="GeneProduct" name="EditProduct" placeholder="'+geneProduct+'">'+
                                        '<input type="hidden" name="OriginalProduct" value="'+geneProduct+'">'+
                                      '</div></div><div class="modal-footer">'+
                                      '<button type="button" class="btn btn-default btn-lg" data-dismiss="modal">Close</button>'+
                                      '<button type="submit" class="btn btn-primary btn-lg" name="EditInformation">Save</button></div></div></div></div></form>'+
                                    '<button href="#" data-toggle="modal" data-target="#myModaledit_info" class="btn btn-link">Edit Information</button>';
          insertdrop += '</ul>';                 
          $contextMenu.append(insertdrop);

          var form = document.getElementById('selectionArray');
          if (form!=null){
            my_tb=document.createElement('INPUT');
            my_tb.type='hidden';
            my_tb.name="selectionArray";
            my_tb.value=JSON.stringify(SelectionArrayMouse);
      
            form.appendChild(my_tb);
          }

        $contextMenu.css({
            display: "block",
            left: e.pageX,
            top: e.pageY
        });
        return false;
    });

    $contextMenu.on("click", "a", function () {

        $contextMenu.hide();

    });

    $("div#demo_2").click(function () {
        $contextMenu.hide();
        
        if($('#selectionArray').length>0 && SelectionArrayMouse.length != 1) {
          document.getElementById('selectionArray').remove();
          g.svg.selectAll('ellipse').each(function (d){                                                                                                                                                                                                                                      
                                                      var ellipseStyle= this.getAttribute("backupColor");
                                                      var ellipseStroke= this.getAttribute("strokeColor");
                                                      this.setAttribute("style",ellipseStyle);
                                                      this.setAttribute("style",ellipseStroke);});
         
          }


    });   

});

////////////////////////////////////////////////////////////////////////////
};



//////////////////////////////////////////////////////////////////////////////////////////////////