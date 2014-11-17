// modifyBySearch.js

//MODAL show
if(showModalGBK == 'yes'){
  $(window).load(function(){
          $('#myModalGBK').modal('show');
      });

}
if(modalDownloadExport == 'yes'){
            $(window).load(function(){
              $('#myModalDownloadExport').modal('show');
        });
}
if(ModalAnnotateError == 'yes'){
            $(window).load(function(){
              $('#myModalShowAnnotateError').modal('show');
        });
}
if(showModalNoMatch == 'yes'){
  $(window).load(function(){
          $('#myModalNoMatch').modal('show');
      });

}
if(showModalNoMatchExt == 'yes'){
  $(window).load(function(){
          $('#myModalNoMatchExt').modal('show');
      });

}

if(ShowModalErrorDuringAlign == 'yes'){
  $(window).load(function(){
          $('#myModalErrorDuringAlign').modal('show');
      });

}

if (showModalComp=='yes' && alreadyshownmodal=='no'){
  $(window).load(function(){
              $('#myModalLinkNotSelected').modal('show');
        });
}


if(ModalSequence == 'yes'){
            $(window).load(function(){
              $('#myModalDownloadSequence').modal('show');
        });
}

if(isSearchMade == 'yes' && numFilesAfterSearch>0 && errorUpload == 'no' && alreadyShownUpload=='no'){
            $(window).load(function(){
              $('#myModalFiles').modal('show');
        });
}


if(NCBISearch == 'yes'){
  $(window).load(function(){
        var url="http://blast.ncbi.nlm.nih.gov/Blast.cgi?PROGRAM=blastn&PAGE_TYPE=BlastSearch&LINK_LOC=blasthome&QUERYFILE="+geneSequenceNCBI+"&DATABASE=nr&PROGRAM=blastn";
        window.open(url, '_blank'); 
    });
}

var ArrayEllipse = new Array();

//Function that creates the visualization
var setup_plot = function(plot_info) {

  console.log(plot_info.global);

  var g = plot_info.global;
  allInfo=plot_info.global;

  g.angle_dom = [], g.angle_rng = [];

  axes_info = plot_info.axes;
  for (var axis_name in axes_info) {
    axis_info = axes_info[axis_name];
    g.angle_dom.push(axis_name);
    g.angle_rng.push(axis_info.angle);
  }

  g.angle_f     = d3.scale.ordinal().domain(g.angle_dom).range(g.angle_rng);

  g.color_f     = d3.scale.category20();
  g.color_search = d3.scale.category10();


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

  var bigger=0;
  var numberOfGenomes=0;
  var longerGenomeAndNumber = function (type) {
    numberOfGenomes+=1;
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

  g.nodesByType.forEach(longerGenomeAndNumber);

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
      .append('g');
     

g.svg.graph = d3.selectAll('g').append('g').attr('transform',g.transform);


    var transform = function(d) {
    return 'rotate(' + degrees(1.575) + ')';
  };

var inicialY1 = -2000, inicialY2 = -2000, prevY = -2000, prevType="Str1";

var Ylocations={};
var yp=prevY;

for (i in g.nodesByType){
  Ylocations[g.nodesByType[i].key]=yp;
  yp+=2500;
}
  
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


  var transform3 = function(d) {
    return 'rotate(' + degrees( g.angle_f(d.type) ) + ')';
  };

  var path_angle  = function(d) { return g.angle_f(d.type);    };
  var path_radius = function(d) { return g.radius_f(d.node.index); };

var threshold = function(link_node){
  var type = link_node.type;

  for(i in g.nodesByType){
      if(g.nodesByType[i].values[0].type == type) return g.nodesByType[i].values.length * 0.005; 
  }
  
} 


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

var SelectionArrayRect = new Array();

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

var lineFunction = d3.svg.line()
                        .x(function(d) { return d.x; })
                        .y(function(d) { return d.y; });


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

var CheckSelectionLink =function(d){
                          if(sel == 'undefined') return 'yes';
                          else{
                            if (sameGenome){
                                for (x in sel){
                                  if ((sel[x].genome == d.source.node.genome && sel[x].index == d.source.node.index)||(sel[x].genome == d.target.node.genome && sel[x].index == d.target.node.index)) return 'yes';
                                }
                            }
                            else{
                              for (selec in sel){
                                if ((sel[x].genome == d.source.node.genome && sel[x].index == d.source.node.index)||(sel[x].genome == d.target.node.genome && sel[x].index == d.target.node.index)) return 'yes';
                                 
                              }
                            }
                          }
                        }

  var ShowModalNotSelected='no';
  if(searchBysequence=='yes' || editInfo=='yes'){

  g.svg.graph.append('g')
    .attr('class', 'links')
    .selectAll('.link')
    .data(g.links)
  .enter().append('path')
      .filter(function (d){
                           if (exclude_hypothetical=='yes' && (d.target.node.product.indexOf('hypothetical protein') > -1 || d.source.node.product.indexOf('hypothetical protein') > -1));
                           else{
                            var LinkInSelection = CheckSelectionLink(d);
                              if (LinkInSelection=='yes') return d;
                              else ShowModalNotSelected='yes';
                           }})
      .attr('d', function (d){
                              var sourceTypeId = document.getElementById(d.source.type);
                              var sourceY = sourceTypeId.getAttribute('y1');
                              var targetTypeId = document.getElementById(d.target.type);
                              var targetY = targetTypeId.getAttribute('y1');         
                              if (parseInt(d.target.node.genome)<parseInt(d.source.node.genome)){
                                var lineData = [ { "x": g.radius_f(d.source.node.index),  "y": Ylocations[d.source.node.type] },
                                                 { "x": g.radius_f(d.target.node.index),  "y": Ylocations[d.target.node.type] +200}];
                              }
                              else{
                                var lineData = [ { "x": g.radius_f(d.source.node.index),  "y": Ylocations[d.source.node.type] },
                                                 { "x": g.radius_f(d.target.node.index),  "y": Ylocations[d.target.node.type] -400}];
                              }
                              return lineFunction(lineData);})
      .attr('class', 'link')
      .style('fill',function (d){ return 'none';})
      .style('stroke', function (d){
                                    if (searchBysequence=='yes') arrayOfImported.push(d.source.node.gene);
                                    var retorno;
                                    var thresholdSource = threshold(d.source);
                                    var thresholdTarget = threshold(d.target);
                                    for (i in search_array){ 
                                                             if(((d.source.node.index - thresholdSource) <= d.target.node.index && (d.source.node.index + thresholdSource) >= d.target.node.index) || ((d.target.node.index - thresholdTarget) <= d.source.node.index && (d.target.node.index + thresholdTarget) >= d.source.node.index)) return 'red';
                                                           else return 'blue';
                                                           }
                                    return retorno;})
      .style('stroke-width', function (d){
                                         var thresholdSource = threshold(d.source);
                                         var thresholdTarget = threshold(d.target);
                                         if(((d.source.node.index - thresholdSource) <= d.target.node.index && (d.source.node.index + thresholdSource) >= d.target.node.index) || ((d.target.node.index - 5) <= d.source.node.index && (d.target.node.index + 5) >= d.source.node.index)) return 35;
                                         else return 35;
      })
      .on('mouseover', on_mouseover_link)
      .on('mouseout',  on_mouseout);
}
else{
for (j in search_array){
  g.svg.graph.append('g')
    .attr('class', 'links')
    .selectAll('.link')
    .data(g.links)
  .enter().append('path')
  .filter(function (d){  if (exclude_hypothetical=='yes' && (d.target.node.product.indexOf('hypothetical protein') > -1 || d.source.node.product.indexOf('hypothetical protein') > -1));
                         else{
                         if(d.source.node.genome == genomesearch || d.target.node.genome == genomesearch);
                         else{
                          if (sel!='undefined'){
                          for (v in sel){
                          if(typesearch_array!=null){
                          if (typesearch_array[j] == 'GeneProduct'){
                           if (d.source.node.product.indexOf(search_array[j]) > -1 && ((d.source.node.genome == sel[v].genome && d.source.node.index == sel[v].index) || (d.target.node.genome == sel[v].genome && d.target.node.index == sel[v].index))) return d;
                          }
                          else if (typesearch_array[j] == 'GeneName'){
                           if (d.source.node.gene.indexOf(search_array[j]) > -1 && ((d.source.node.genome == sel[v].genome && d.source.node.index == sel[v].index) || (d.target.node.genome == sel[v].genome && d.target.node.index == sel[v].index))) return d;
                          }
                          else{
                                var splitted = search_array[j].split("-");
                                var begin = splitted[0].trim();
                                var end = splitted[1].trim();
                                if (parseInt(d.source.node.begin) >= parseInt(begin) && parseInt(d.source.node.end) <= parseInt(end)) return d;
                                
                          }
                        }
                      }
                      }
                      else{
                        if(typesearch_array!=null){
                          if (typesearch_array[j] == 'GeneProduct'){
                           return d.source.node.product.indexOf(search_array[j]) > -1;
                          }
                          else if (typesearch_array[j] == 'GeneName'){
                           return d.source.node.gene.indexOf(search_array[j]) > -1;
                          }
                          else{
                                var splitted = search_array[j].split("-");
                                var begin = splitted[0].trim();
                                var end = splitted[1].trim();
                                if (parseInt(d.source.node.begin) >= parseInt(begin) && parseInt(d.source.node.end) <= parseInt(end)) return d;
                                
                          }
                        }
                      }
                        }}})
      .attr('d', function (d){
                              var sourceTypeId = document.getElementById(d.source.type);
                              var sourceY = sourceTypeId.getAttribute('y1');
                              var targetTypeId = document.getElementById(d.target.type);
                              var targetY = targetTypeId.getAttribute('y1');             

                              if (parseInt(d.target.node.genome)<parseInt(d.source.node.genome)){
                                var lineData = [ { "x": g.radius_f(d.source.node.index),  "y": sourceY - (numberOfGenomes * 2500)},
                                                 { "x": g.radius_f(d.target.node.index),  "y": targetY - (numberOfGenomes * 2300)}];
                              }
                              else{
                                var lineData = [ { "x": g.radius_f(d.source.node.index),  "y": sourceY - (numberOfGenomes * 2500)},
                                                 { "x": g.radius_f(d.target.node.index),  "y": targetY - (numberOfGenomes * 2600)}];
                              }

                              return lineFunction(lineData);})
      .attr('class', 'link')
      .style('fill',function (d){ return 'none';})
      .style('stroke', function (d){
                                    var retorno;
                                    var thresholdSource = threshold(d.source);
                                    var thresholdTarget = threshold(d.target);
                                    for (i in search_array){ 
                                                             if(((d.source.node.index - thresholdSource) <= d.target.node.index && (d.source.node.index + thresholdSource) >= d.target.node.index) || ((d.target.node.index - thresholdTarget) <= d.source.node.index && (d.target.node.index + thresholdTarget) >= d.source.node.index)) return 'red';
                                                           else return 'blue';

                                                           }
                                    return retorno;})
      .style('stroke-width', function (d){
                                         var thresholdSource = threshold(d.source);
                                         var thresholdTarget = threshold(d.target);
                                         if(((d.source.node.index - thresholdSource) <= d.target.node.index && (d.source.node.index + thresholdSource) >= d.target.node.index) || ((d.target.node.index - 5) <= d.source.node.index && (d.target.node.index + 5) >= d.source.node.index)) return 35;
                                         else return 35;
      })
      .on('mouseover', on_mouseover_link)
      .on('mouseout',  on_mouseout);
  } 
}
  //}

var checkMoreContigs=function(d){
  arrayMorecontigs=new Array();
  for (i in g.nodesByType){
    if (g.nodesByType[i].key==d){
      return g.nodesByType[i].moreContigs;
    }
  }
}

var numtotalNodes=function(){
  arrayTotal= new Array();
  for (i in g.nodesByType){
    arrayTotal=arrayTotal.concat(g.nodesByType[i].values);
  }
  return arrayTotal;
}
var arrayTotalNodes= numtotalNodes();
var ArrayOfRegionSelect=new Array();
  var prevElipse="";
  var geneBegin='...';
  var geneEnd='...';
  g.svg.graph.append('g')
    .attr('class', 'nodes')
    .selectAll('.node')
    .data(arrayTotalNodes)
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
      .attr('moreContigs',function(d){return checkMoreContigs(d.type);})
      .attr('id', idNode)
      .attr('file', function(d){
                                fPos=parseInt(d.genome)-1;
                                fName=fileNames.split("---")[fPos];
                                fName=fName.split("/")[3];
                                return fName;
                                })
      .style('fill', function (d,i){
                                  counts+=1;
                                  var retorno;
                                  if(show_hypothetical=='yes'){
                                        if(d.product.indexOf('hypothetical') > -1){
                                            var color = 'red';
                                            var backup = 'fill:'+color;
                                            document.getElementById((counts).toString()).setAttribute("backupColor",backup);
                                            return color;
                                        }
                                      }
                                  if((d.genome == genomesearch||genomesearch=='allgenome')&&isSearchSequence!='yes'){
                                    if(search_array==null){ if (d.gene.indexOf('Undefined_Region') > -1) var color='black';
                                                          else var color = fill(d);
                                                            var backup = 'fill:'+color;
                                                            document.getElementById((counts).toString()).setAttribute("backupColor",backup);
                                                            return color;
                                    } 
                                    else{
                                        for (j in search_array){ 
                                                                searchstring=search_array[j].toLowerCase();
                                                                if (typesearch_array[j] == 'GeneProduct'){
                                                                    if(d.product.toLowerCase().indexOf(searchstring) > -1){ 
                                                                                                                var color = g.color_search(j);
                                                                                                                var backup = 'fill:'+color;
                                                                                                                document.getElementById((counts).toString()).setAttribute("backupColor",backup);
                                                                                                                return color;
                                                                    } 
                                                                   else{ if (d.gene.indexOf('Undefined_Region') > -1) retorno='black';
                                                                          else retorno = fill(d);
                                                                          var backup = 'fill:'+retorno;
                                                                          document.getElementById((counts).toString()).setAttribute("backupColor",backup);
          
                                                                    }
                                                                }
                                                                else if (typesearch_array[j] == 'GeneName'){
                                                                    if(d.gene.toLowerCase().indexOf(searchstring) > -1){  
                                                                                                                var color = g.color_search(j);
                                                                                                                var backup = 'fill:'+color;
                                                                                                                document.getElementById((counts).toString()).setAttribute("backupColor",backup);
                                                                                                                return color;
                                                                    } 
                                                                   else{ if (d.gene.indexOf('Undefined_Region') > -1) retorno='black';
                                                                          else retorno = fill(d);
                                                                          var backup = 'fill:'+retorno;
                                                                          document.getElementById((counts).toString()).setAttribute("backupColor",backup);
          
                                                                    }
                                                                }
                                                                else{
                                                                      if (d.gene.indexOf('Undefined_Region') > -1) retorno='black';
                                                                          else retorno = fill(d);
                                                                      var backup = 'fill:'+retorno;
                                                                      document.getElementById((counts).toString()).setAttribute("backupColor",backup);
                                                                }

                                          } 
                                          return retorno;}
                                      }
                                      else {if (d.gene.indexOf('Undefined_Region') > -1) var color='black';
                                            else var color = fill(d);
                                            var backup = 'fill:'+color;
                                            document.getElementById((counts).toString()).setAttribute("backupColor",backup);
                                            return color;};
                                      })
      .selectAll('ellipse')
      .data(connectors)
      .enter().append('ellipse')
        .attr('transform', transform(i))
        .style('stroke', function (d){  
                                        countsEllipse+=1;
                                        if (d.node.begin==''){ return 'black';
                                                                document.getElementById((countsEllipse).toString()).firstChild.setAttribute("strokeColor",'black');
                                                              }
                                        if (geneBegin!=d.node.begin && geneEnd!=d.node.begin) {
                                                            geneBegin=d.node.begin;
                                                            geneEnd=d.node.end;
                                                            document.getElementById((countsEllipse).toString()).firstChild.setAttribute("strokeColor",'orange');
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
        .attr('ry', function (d){ var retorno;
                                  isInSelection=CheckSelection(d.node);
                                  if(isInSelection!='yes');
                                  else{
                                  if(show_hypothetical=='yes'){
                                        if(d.node.product.indexOf('hypothetical') > -1) return 450;    
                                  }
                                  if(d.node.genome == genomesearch || genomesearch=='allgenome' || searchBysequence=='yes'){
                                    if(search_array==null) return 300;
                                    else{
                                      if(searchBysequence=='yes'){
                                        for (k in search_array){
                                          for (j in search_array[k]){
                                            if (searchByBLAST=='yes'){
                                              searchFor=search_array[k][j].split('BLASTsearch')[0];
                                              if(d.node.gene.indexOf(searchFor) > -1) return 450;
                                            }
                                            if(d.node.gene.indexOf(search_array[k][j]) > -1) return 450;
                                            else retorno = 300;
                                          }
                                        }
                                      }
                                      else{
                                        for (k in search_array){
                                                                searchstring=search_array[k].toLowerCase();
                                                                if(typesearch_array[k] == 'GeneProduct'){
                                                                    if(d.node.product.toLowerCase().indexOf(searchstring) > -1) return 450;
                                                                   else retorno = 300;
                                                                }
                                                                else if(typesearch_array[k] == 'GeneName'){
                                                                    if(d.node.gene.toLowerCase().indexOf(searchstring) > -1) return 450;
                                                                    else retorno = 300;
                                                                }
                                                                else if(typesearch_array[k] == 'Begin-End'){
                                                                  var splitted = search_array[k].split("-");
                                                                  var begin = splitted[0].trim();
                                                                  var end = splitted[1].trim();
                                                                  if (parseInt(d.node.begin) >= parseInt(begin) && parseInt(d.node.end) <= parseInt(end)){
                                                                    if (prevElipse!=d.node.reference && ArrayOfRegionSelect.indexOf(d.node.reference + '--' + d.node.begin)==-1){
                                                                     ArrayOfRegionSelect.push(d.node.reference + '--' + d.node.begin);
                                                                     prevElipse=d.node.reference;
                                                                    }
                                                                    else prevElipse=d.node.reference;
                                                                    return 450;
                                                                  } 
                                                                  else retorno = 300;
                                                                }
                                        }
                                      }
                                      return retorno;
                                    }
                                  }
                                  else return 300;}})
        .attr('file', function(d){
                                fPos=parseInt(d.node.genome)-1;
                                fName=fileNames.split("---")[fPos];
                                fName=fName.split("/")[3];
                                return fName;
                                })
        .on('mouseover', on_mouseover_node)
        .on('mouseout',  on_mouseout)
        .on('mousedown', function(){ onMouseDown(d3.event,this);})
        .on('mouseup', function(){ onMouseUp(d3.event);});


if(ShowModalNotSelected == 'yes'){
  $('#myModalLinkNotSelected').modal('show');    
}


var prevEllipse;
   

var inversion=false, rotation=0, RotationWay=0, Way=0,rotacao=0;

//Zoom to specific location of the representation after choosing a region on the table
if(positionElement!=""){
  var element=document.getElementById(positionElement);
  rect = element.getBoundingClientRect();
  positionTop=parseInt(rect.top);
  positionRight=parseInt(rect.right);
  if(positionTop<g.y_off){
    if(positionTop<0){
      positionTop=(g.y_off+40)+g.y_off-(positionTop);
    }
    else{
      positionTop=(g.y_off+40)+(g.y_off-positionTop);
    }
  }
  else{
    positionTop=(g.y_off+40)+(g.y_off-positionTop);
  }
  if(positionRight<(g.x_off+300)){
    if(positionRight<0){
      positionRight=(g.x_off+300)+g.x_off-(positionRight);
    }
    else{
      positionRight=(g.x_off+300)+(g.x_off-positionRight);
    }
  }
  else{
      positionRight=(g.x_off+300)+(g.x_off+(-positionRight));
  }
  
}


if(positionElement!=""){
  g.svg.selectAll('rect').call(d3.behavior.zoom().translate([positionRight,positionTop]).scale(0.03).on("zoom", function(){ zoom(d3.event.sourceEvent);}))
        .on('mousedown', function(){ onMouseDownRect(d3.event,this);});
  g.svg.graph.attr("transform",'translate(' + positionRight + ',' + positionTop + ')' + 'scale(' + 0.03 + ')');
}
else{
  g.svg.selectAll('rect').call(d3.behavior.zoom().translate([g.x_off,g.y_off]).scale(0.03).on("zoom", function(){ zoom(d3.event.sourceEvent);}))
      .on('mousedown', function(){ onMouseDownRect(d3.event,this);});
}

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

//Information for the Search by Attribute Table
if(typesearch_array!=null && searchBysequence!='yes'){

for(var i=0;i<g.nodesByType.length;i++){
  lengthtype=g.nodesByType[i].values.length;
  prevStart=-1;
  var start=-1;
  for (var y=0;y<lengthtype;y++){
    if (exclude_hypothetical=='yes' && (g.nodesByType[i].values[y].product.indexOf('hypothetical protein') > -1 || g.nodesByType[i].values[y].product.indexOf('hypothetical protein') > -1));
    else{
    if (g.nodesByType[i].values[y].genome==genomesearch||genomesearch=='allgenome'){
      for (j in search_array){ 
        start=g.nodesByType[i].values[y].begin;
        searchstring=search_array[j].toLowerCase();
        if (typesearch_array[j] == 'GeneProduct' && start!=prevStart){
          if(g.nodesByType[i].values[y].product.toLowerCase().indexOf(searchstring) > -1){
                  HitsArraySearch.push({source: '-' , hit : g.nodesByType[i].values[y] , typesearch : typesearch_array[j] , numRelations : g.nodesByType[i].values[y].imports.length , identity: '-' , positionSource : g.nodesByType[i].values[y].indexGeral}); 
          } 
        }
        else if (typesearch_array[j] == 'GeneName' && start!=prevStart){
          if(g.nodesByType[i].values[y].gene.toLowerCase().indexOf(searchstring) > -1){   
                  HitsArraySearch.push({source: '-' , hit : g.nodesByType[i].values[y] , typesearch : typesearch_array[j] , numRelations : g.nodesByType[i].values[y].imports.length , identity: '-' , positionSource : g.nodesByType[i].values[y].indexGeral});
          } 
        }
        else if (typesearch_array[j] == 'Begin-End' && start!=prevStart){
          var splitted = search_array[k].split("-");
          var begin = splitted[0].trim();
          var end = splitted[1].trim();
          if(parseInt(g.nodesByType[i].values[y].begin)>=parseInt(begin) && parseInt(g.nodesByType[i].values[y].end)<=parseInt(end)){   
                  HitsArraySearch.push({source: '-' , hit : g.nodesByType[i].values[y] , typesearch : typesearch_array[j] , numRelations : g.nodesByType[i].values[y].imports.length , identity: '-' , positionSource : g.nodesByType[i].values[y].indexGeral});
          }
        }
      
    }
  prevStart=start; 
  }
  }
}
}

}

//Information for the Search by external sequence Table
if(searchByBLAST=='yes'){
  countBLASTs=0;
  for (k in search_array){ 
    lengthAlignments1=lengthAlignments[k].split("---");
    alignmentPositionStart=alignmentPos[k].split("---");
    alignScore1=alignScore[k].split("---");
    refStart1=refStart[k].split("---");
    subEnd1=subEnd[k].split("---");
    seqSub1=seqSub[k].split("...");
    seqQuery1=seqQuery[k].split("...");
    seqmatch1=seqmatch[k].split("...");
    identifiers1=identifiers[k].split("---");
    prevTarget="";
    for (j in lengthAlignments1){
      if (lengthAlignments1[j]=='not exists');
      else if (search_array[k][j].indexOf('BLASTsearch') > -1){
        geneU=search_array[k][j].split("BLASTsearch")[0];
        genomeU=parseInt(geneU.split("...")[0])-1;
        for (l in g.nodesByType[genomeU].values){
          if (g.nodesByType[genomeU].values[l].gene==geneU){
            geneTU=g.nodesByType[genomeU].values[l];
          }
        }
        if (prevTarget==geneTU);
        else {
          HitsArraySequence.push({source: identifiers1[j] , hit : geneTU , typesearch : 'Search By Sequence' , numRelations : '-' , positionSource : '-' , positionTarget : geneTU.indexGeral , lengthAlignment : lengthAlignments1[j] , alignmentStart : alignmentPositionStart[j] , alignmentScore : alignScore1[j] , referenceStart : refStart1[j] , subjectEnd : subEnd1[j], sequenceSubject: seqSub1[j], sequenceQuery: seqQuery1[j], sequenceMatch: seqmatch1[j]}); 
          countBLASTs+=1;
          prevTarget=geneTU;
        }
      }
    }
  }
}

//Information for the Search by BLAST Table
if((searchBysequence=='yes' && searchNCBI!='yes')|| editInfo=='yes'){
  prevLink='';

  for (k in search_array){ 
    if ('BLASTsearch' in search_array[k]);
    else{
      lengthAlignments1=lengthAlignments[k].split("---");
      alignmentPositionStart=alignmentPos[k].split("---");
      alignScore1=alignScore[k].split("---");
      refStart1=refStart[k].split("---");
      subEnd1=subEnd[k].split("---");
      seqSub1=seqSub[k].split("...");
      seqQuery1=seqQuery[k].split("...");
      seqmatch1=seqmatch[k].split("...");
      prevTarget="";
      for(var i=0;i<g.links.length;i++){
        if (exclude_hypothetical=='yes' && (g.links[i].target.node.product.indexOf('hypothetical protein') > -1 || g.links[i].source.node.product.indexOf('hypothetical protein') > -1));
        else{
        for (j in lengthAlignments1){ 
          if (lengthAlignments1[j]=='not exists');
          else if (g.links[i].target.node.gene==search_array[k][j] && g.links[i].target.node.gene!=prevTarget){
            HitsArraySequence.push({source: g.links[i].source.node , hit : g.links[i].target.node , typesearch : 'BLAST' , numRelations : '-' , positionSource : g.links[i].source.node.indexGeral , positionTarget : g.links[i].target.node.indexGeral , lengthAlignment : lengthAlignments1[j] , alignmentStart : alignmentPositionStart[j] , alignmentScore : alignScore1[j] , referenceStart : refStart1[j] , subjectEnd : subEnd1[j], sequenceSubject: seqSub1[j], sequenceQuery: seqQuery1[j], sequenceMatch: seqmatch1[j]}); 
            prevTarget=g.links[i].target.node.gene;
          }
        }
      }
      }
    }
}
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
    if(y==10)cell.innerHTML='<h5>Number Of Contigs</h5>';
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

//Search by BLAST header table Creation
if (HitsArraySequence.length!=0){
var table = document.getElementById('HitTable');
Tbody=document.createElement("tbody");
table.appendChild(Tbody);
header=table.createTHead();
row=header.insertRow(0);
for (var y=0;y<13;y++){
  th=document.createElement("th");
  cell=row.appendChild(th);
  cell.style.textAlign = 'center';
  if(y==0)cell.innerHTML='<h5 class="FontTitleTables">#</h5>';
  if(y==1)cell.innerHTML='<h5 class="FontTitleTables">Type Search</h5>';
  if(y==2)cell.innerHTML='<h5 class="FontTitleTables">Query Gene</h5>';
  if(y==3)cell.innerHTML='<h5 class="FontTitleTables">Target Gene</h5>';
  if(y==4)cell.innerHTML='<h5 class="FontTitleTables">Product</h5>';
  if(y==5)cell.innerHTML='<h5 class="FontTitleTables">Genome of Target</h5>';
  if(y==6)cell.innerHTML='<h5 class="FontTitleTables">Target Alignment Begin</h5>';
  if(y==7)cell.innerHTML='<h5 class="FontTitleTables">Target Alignment End</h5>';
  if(y==8)cell.innerHTML='<h5 class="FontTitleTables">Query Alignment Begin</h5>';
  if(y==9)cell.innerHTML='<h5 class="FontTitleTables">Query Alignment End</h5>';
  if(y==10)cell.innerHTML='<h5 class="FontTitleTables">Alignment Score</h5>';
  if(y==11)cell.innerHTML='<h5 class="FontTitleTables">Strand of Query</h5>';
  if(y==12)cell.innerHTML='<h5 class="FontTitleTables">Strand of Target</h5>';

}
}
else{
//Search by attribute header table Creation
var table = document.getElementById('HitTable');
Tbody=document.createElement("tbody");
table.appendChild(Tbody);
header=table.createTHead();
row=header.insertRow(0);
for (var y=0;y<9;y++){
  th=document.createElement("th");
  cell=row.appendChild(th);
  cell.style.textAlign = 'center';
  if(y==0)cell.innerHTML='<h5 class="FontTitleTables">#</h5>';
  if(y==1)cell.innerHTML='<h5 class="FontTitleTables">Type Search</h5>';
  if(y==2)cell.innerHTML='<h5 class="FontTitleTables">Gene</h5>';
  if(y==3)cell.innerHTML='<h5 class="FontTitleTables">Product</h5>';
  if(y==4)cell.innerHTML='<h5 class="FontTitleTables">BLAST of Source</h5>';
  if(y==5)cell.innerHTML='<h5 class="FontTitleTables">Number of Relations</h5>';
  if(y==6)cell.innerHTML='<h5 class="FontTitleTables">Genome of Target</h5>';
  if(y==7)cell.innerHTML='<h5 class="FontTitleTables">Gene Begin</h5>';
  if(y==8)cell.innerHTML='<h5 class="FontTitleTables">Gene End</h5>';

}
}
//Search by BLAST table Creation
if (HitsArraySequence.length!=0){
  var lengthhitsSequence=HitsArraySequence.length;
  var isSearchByBLAST='no';
for(var i=0; i<lengthhitsSequence; i++){
  if (HitsArraySequence[i].typesearch=='Search By Sequence'){
    isSearchByBLAST='yes';
  }
  else{
    isSearchByBLAST='no';
  }
  row=Tbody.insertRow(i);
  for (var j=0;j<13;j++){
    cell=row.insertCell(j);
    cell.style.textAlign = 'center';
    geneToUsesource="";
    if (isSearchByBLAST!='yes'){
      geneArray=HitsArraySequence[i].source.gene.split("...")[1].split('_');
      ToRemove=geneArray.splice(geneArray.length-1,1);
      ToRemove="_"+ToRemove[0];
      geneToUsesource=HitsArraySequence[i].source.gene.split("...")[1].replace(ToRemove,"");
      geneReference1=HitsArraySequence[i].source.reference.replace(/\s/g, "---");
      geneReference1=geneReference1.replace(/\|/g, "...");
    }
    else{
      geneToUsesource=HitsArraySequence[i].source.split("...")[1];
    }
    geneToUsehit="";
    geneArray=HitsArraySequence[i].hit.gene.split("...")[1].split('_');
    ToRemove=geneArray.splice(geneArray.length-1,1);
    ToRemove="_"+ToRemove[0];
    geneToUsehit=HitsArraySequence[i].hit.gene.split("...")[1].replace(ToRemove,"");
    if(j==0)cell.innerHTML='<h5 class="FontTables">'+(i+1)+'</h5>';
    if(j==1)cell.innerHTML='<h5 class="FontTables">'+HitsArraySequence[i].typesearch+'</h5>';
    if(j==2){
        if (isSearchByBLAST=='yes'){
                cell.innerHTML= '<form enctype="multipart/form-data" action="searchWithContigs.php" method="POST">'+
                                '<a href="'+"http://www.ncbi.nlm.nih.gov/gene/?term="+geneToUsesource+'" target="_blank">'+'<h6>'+geneToUsesource+'</h6>'+'</a>'+
                                '<input type="hidden" name="null" value="null">'+
                                '<input type="hidden" name="nameSourceGene" value="'+geneToUsesource+'">'+
                                      '</form>';
                                      
        } 
        else{
                cell.innerHTML='<form enctype="multipart/form-data" action="searchWithContigs.php" method="POST">'+
                                        '<a href="'+"http://www.ncbi.nlm.nih.gov/gene/?term="+geneToUsesource+'" target="_blank">'+'<h6>'+geneToUsesource+'</h6>'+'</a>'+
                                        '<button type="submit" class="btn btn-link">  (See Position)</button>'+
                                        '<input type="hidden" name="ElementIDposition" value="'+HitsArraySequence[i].positionSource+'">'+
                                        '<input type="hidden" name="nameSourceGene" value="'+geneToUsesource+'">'+
                                      '</form>';
        }
    } 
    if(j==3){

        cell.innerHTML='<form enctype="multipart/form-data" action="searchWithContigs.php" method="POST">'+
                                        '<a href="'+"http://www.ncbi.nlm.nih.gov/gene/?term="+geneToUsehit+'" target="_blank">'+'<h6>'+geneToUsehit+'</h6>'+'</a>'+
                                        '<button type="submit" class="btn btn-link">  (See Position)</button>'+
                                        '<input type="hidden" name="ElementIDposition" value="'+HitsArraySequence[i].positionTarget+'">'+
                                        '<input type="hidden" name="nameTargetGene" value="'+geneToUsehit+'">'+
                                      '</form>';
      
    }
    if(j==4)cell.innerHTML='<h5 class="FontTables">'+HitsArraySequence[i].hit.product+'</h5>';
    if(j==5)cell.innerHTML='<h5 class="FontTables">'+HitsArraySequence[i].hit.genome+'</h5>';
    if(j==6)cell.innerHTML='<h5 class="FontTables">'+HitsArraySequence[i].referenceStart+'</h5>'+'<input type="hidden" name="seqref" value="'+HitsArraySequence[i].sequenceSubject+'" />';
    if(j==7)cell.innerHTML='<h5 class="FontTables">'+HitsArraySequence[i].subjectEnd+'</h5>';
    if(j==8)cell.innerHTML='<h5 class="FontTables">'+HitsArraySequence[i].alignmentStart+'</h5>'+'<input type="hidden" name="seqQuery" value="'+HitsArraySequence[i].sequenceQuery+'" />';
    if(j==9)cell.innerHTML='<h5 class="FontTables">'+String(parseInt(HitsArraySequence[i].alignmentStart) + parseInt(HitsArraySequence[i].lengthAlignment))+'</h5>';
    if(j==10)cell.innerHTML='<h5 class="FontTables">'+parseFloat(HitsArraySequence[i].alignmentScore).toFixed(2)+'</h5>'+'<input type="hidden" name="seqmatches" value="'+HitsArraySequence[i].sequenceMatch+'" />';
    if(j==11)cell.innerHTML='<h5 class="FontTables">'+'+'+'</h5>';
    if(j==12){
      if (parseInt(HitsArraySequence[i].referenceStart) > parseInt(HitsArraySequence[i].subjectEnd)) cell.innerHTML='<h5 class="FontTables">'+'-'+'</h5>';
      else cell.innerHTML='<h5 class="FontTables">'+'+'+'</h5>';
    }

  }
}
}

//Search by attribute table Creation
if (HitsArraySearch.length!=0){
  var lengthHits=HitsArraySearch.length;
for(var i=0; i<lengthHits; i++){
  row=Tbody.insertRow(i);
  listaImports="";
  for (var w=0;w<parseInt(HitsArraySearch[i].numRelations);w++){
    imp=HitsArraySearch[i].hit.imports[w].split("...");
    impID=HitsArraySearch[i].hit.importID[w];
    impSplitted=imp[1].split("_")
    newGene=""
    for(var k=0;k<impSplitted.length-1;k++){
      newGene=newGene+impSplitted[k]+"_";
    }
    newGene=newGene.substring(0, newGene.length - 1);
    listaImports=listaImports+'<form enctype="multipart/form-data" action="searchWithContigs.php" method="POST">'+
                                        '<a href="http://www.ncbi.nlm.nih.gov/gene/?term='+newGene+'" target="_blank">Genome:&nbsp;&nbsp;'+imp[0]+'&nbsp;&nbsp;&nbsp;&nbsp;Gene:&nbsp;&nbsp;'+newGene+'</a>'+
                                        '<button type="submit" class="btn btn-link">  (See Position)</button>'+
                                        '<input type="hidden" name="ElementIDposition" value="'+impID+'">'+
                                      '</form>';
  }
  for (var j=0;j<9;j++){
    cell=row.insertCell(j);
    cell.style.textAlign = 'center';
    geneToUse="";
    geneArray=HitsArraySearch[i].hit.gene.split("...")[1].split('_');
    ToRemove=geneArray.splice(geneArray.length-1,1);
    ToRemove="_"+ToRemove[0];
    geneToUse=HitsArraySearch[i].hit.gene.split("...")[1].replace(ToRemove,"");
    geneToUsehit=HitsArraySearch[i].hit.gene.split("...")[1].replace(ToRemove,"");
    geneReference1=HitsArraySearch[i].hit.reference.replace(/\s/g, "---");
    geneReference1=geneReference1.replace(/\|/g, "...");
    if(j==0)cell.innerHTML='<h5 class="FontTables">'+(i+1)+'</h5>';
    if(j==1)cell.innerHTML='<h5 class="FontTables">'+HitsArraySearch[i].typesearch+'</h5>';
    if(j==2)cell.innerHTML='<form enctype="multipart/form-data" action="searchWithContigs.php" method="POST">'+
                                        '<a href="'+"http://www.ncbi.nlm.nih.gov/gene/?term="+geneToUse+'" target="_blank">'+'<h6>'+geneToUse+'</h6>'+'</a>'+
                                        '<button type="submit" class="btn btn-link">  (See Position)</button>'+
                                        '<input type="hidden" name="ElementIDposition" value="'+HitsArraySearch[i].positionSource+'">'+
                                      '</form>';
    if(j==3)cell.innerHTML='<h5 class="FontTables">'+HitsArraySearch[i].hit.product+'</h5>';

    var insert= '<div class="modal fade" id="myModalsequenceParameters'+i+'" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">'+
                                  '<div class="modal-dialog">'+
                                    '<div class="modal-content">'+
                                      '<div class="modal-header">'+
                                        '<button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>'+
                                        '<h4 class="modal-title" id="myModalLabel"><a class="FontModalsTitle">Choose the E-value and Minimum Alignment</a></h4>'+
                                      '</div>'+
                                      '<form enctype="multipart/form-data" id="formBLAST2" name="formBLAST2" action="searchWithContigs.php" method="POST" onsubmit="return validateFormBLAST2();">'+
                                      '<div class="modal-body">'+
                                        '<div class="form-group">'+
                                          '<li class="FontModals">E-value</li>';
                                     if(String(numberOfGenomes)==String(HitsArraySearch[i].hit.gene.split("...")[0])) insert+='<input type="hidden" name="refgenome" value="1" />';
                                     else insert+='<input type="hidden" name="refgenome" value="'+String(parseInt(HitsArraySearch[i].hit.gene.split("...")[0]) + 1 )+'" />';
                                     insert+='<input type="hidden" name="rundatabasesearch" value="rundatabasesearch" />'+
                                          '<input type="name" class="form-control" id="E-value" name="edit_Evalue" placeholder="0.001">'+
                                          '<li class="FontModals">Miminum Alignment:</li><input type="name" class="form-control" id="edit_Align" name="edit_Align" placeholder="300">'+
                                          '<input type="hidden" name="querygene" value="'+HitsArraySearch[i].hit.gene+'" />'+
                                          '<input type="hidden" name="geneBegin" value="'+HitsArraySearch[i].hit.begin+'">'+
                                          '<input type="hidden" name="geneEnd" value="'+HitsArraySearch[i].hit.end+'">'+
                                          '<input type="hidden" name="geneReference" value="'+geneReference1+'">'+
                                     '</div>'+
                                     '</div><div class="modal-footer">'+
                                      '<button type="button" class="btn btn-default btn-lg" data-dismiss="modal">Close</button>'+
                                      '<button type="submit" class="btn btn-primary btn-lg" name="CheckSimilarity">BLAST!</button></div></form></div></div></div>'+
                                    '<button href="#" data-toggle="modal" data-target="#myModalsequenceParameters'+i+'" class="btn btn-link btn-lg">'+'<h5 class="FontTables">'+'BLAST against next position sequences.</button>';
    if(j==4)cell.innerHTML=insert;                                
    if(j==5)cell.innerHTML='<li class="dropdown"><a href="#" class="dropdown-toggle" data-toggle="dropdown">'+'<h5 class="FontTables">'+ HitsArraySearch[i].numRelations +'</h5>'+ '</a><b class="caret"></b><ul class="dropdown-menu">' + listaImports
                          + '</ul></a></li>';
    if(j==6)cell.innerHTML='<h5 class="FontTables">'+HitsArraySearch[i].hit.genome+'</h5>';
    if(j==7)cell.innerHTML='<h5 class="FontTables">'+HitsArraySearch[i].hit.begin+'</h5>';
    if(j==8)cell.innerHTML='<h5 class="FontTables">'+HitsArraySearch[i].hit.end+'</h5>';

  }

}
}


//Tables formating
if (HitsArraySequence.length!=0){
$(document).ready( function () {
        var table = $('#HitTable').dataTable( {
          "sDom": 'T<"clear">C<"clear">Rlfrtip',
          "oTableTools": {
            "aButtons": [
                        {
                        "sExtends":    "collection",
                        "sButtonText": "Save",
                        "aButtons":    [ {
                                           "sExtends": "csv",
                                           "mColumns":[0,1,2,3,4,7,9,10,11,12]
                                         }, 
                                         {
                                           "sExtends": "xls",
                                           "mColumns":[0,1,2,3,4,7,9,10,11,12]
                                         }, 
                                         {
                                           "sExtends": "pdf",
                                           "mColumns":[0,1,2,3,4,7,9,10,11,12],
                                           "sPdfOrientation": "landscape",
                                         }
                                       ]
                        },
                        "copy",
                        "print"
      ]
          },
          "sPaginationType": "full_numbers"
        } );
      } );
}

if (HitsArraySearch.length!=0){
$(document).ready( function () {
        var table = $('#HitTable').dataTable( {
          "sDom": 'T<"clear">C<"clear">Rlfrtip',
          "oTableTools": {
            "aButtons": [
                        {
                        "sExtends":    "collection",
                        "sButtonText": "Save",
                        "aButtons":    [ {
                                           "sExtends": "csv",
                                           "mColumns":[0,1,3,4,9,10]
                                         }, 
                                         {
                                           "sExtends": "xls",
                                           "mColumns":[0,1,3,4,9,10]
                                         }, 
                                         {
                                           "sExtends": "pdf",
                                           "mColumns":[0,1,3,4,9,10],
                                           "sPdfOrientation": "landscape",
                                         }
                                       ]
                        },
                        "copy",
                        "print"
      ]
          },
          "sPaginationType": "full_numbers"
        } );
      } );
}

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
                                         }
                                       ]
                        },
                        "copy",
                        "print"
      ]
          },
        } );
      } );

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
**/
/**var $rows = $('#HitTable tbody tr');
$('#search').keyup(function() {
    var val = $.trim($(this).val()).replace(/ +/g, ' ').toLowerCase();
    
    $rows.show().filter(function() {
        var text = $(this).text().replace(/\s+/g, ' ').toLowerCase();
        return !~text.indexOf(val);
    }).hide();
});*/



///////////////////////////////////////////////////////////////////////////////////////////////////////////////////

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

//////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////CONTEXT MENU////////////////////////////////////////


//Right mouse click over nodes
$(function () {

    $contextMenu = $("#contextMenu");

    $contextMenu2 = $("#contextMenu2");

    $("body").on("contextmenu", "svg g g", function (e) {
        Url = document.URL.split('/');
        currentpage = Url[Url.length -1];
        var positionOfThis = this.getAttribute('genomePosition');
        var contigNumber = this.getAttribute('contig');
        var presentGene = this.getAttribute('geneName');
        var geneSequence = this.getAttribute('geneSequence');
        var geneProduct=this.getAttribute('geneProduct');
        var geneBegin=this.getAttribute('geneBegin');
        var geneEnd=this.getAttribute('geneEnd');
        var geneReference=this.getAttribute('reference');
        var fileName=this.getAttribute('file');
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
          for (i=0;i<numberOfGenomes;i++){
            if(String(i+1) != positionOfThis){


                     insertdrop +=   '<li><form enctype="multipart/form-data" action="' + currentpage + '" method="POST"><input type="submit" class="btn btn-link" name="position" value="Move to position ' + String(i+1) +'" />' +
                                     '<input type="hidden" name="positionToBe" value="'+String(i)+'" />' +
                                     '<input type="hidden" name="currentPosition" value="'+String(parseInt(positionOfThis) - 1 )+'" />' +
                                     '</form></li>';
                
            }
          
          }

          insertdrop+= '<form enctype="multipart/form-data" action="' + currentpage + '" method="POST">'+
                                    '<input type="hidden" name="GetSequence" value="GetSequence">'+
                                    '<input type="hidden" name="geneReference" value="'+geneReference+'">'+
                                    '<input type="hidden" name="queryGene" value="'+presentGene+'" />'+
                                    '<button href="#" type="submit" class="btn btn-link">Get Sequence</button></form>';

          if (mContigs=='yes'){
            var contigToExport=this.getAttribute('contig');
            insertdrop+= '<form enctype="multipart/form-data" action="' + currentpage + '" method="POST">'+
                                    '<input type="hidden" name="exportContig" value="exportContig">'+
                                    '<input type="hidden" name="GenomeToExport" value="'+positionOfThis+'">'+
                                    '<input type="hidden" name="contigToExport" value="'+contigToExport+'" />'+
                                    '<input type="hidden" name="ExportType" value="gff" />'+
                                    '<button href="#" type="submit" class="btn btn-link">Export Contig</button></form>';
          }

          if (numberOfGenomes>1){

          insertdrop+= '<div class="modal fade" id="myModalsequenceParameters" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">'+
                                  '<div class="modal-dialog">'+
                                    '<div class="modal-content">'+
                                    '<form enctype="multipart/form-data" id="formBLAST1" name="formBLAST1" action="searchWithContigs.php" method="POST" onsubmit="return validateFormBLAST1();">'+
                                      '<div class="modal-header">'+
                                        '<button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>'+
                                        '<h4 class="modal-title" id="myModalLabel"><a class="FontModalsTitle">Choose the E-value and Minimum Alignment</a></h4>'+
                                      '</div>'+
                                      '<div class="modal-body">'+
                                        '<div class="form-group">';
          if(String(numberOfGenomes)==String(positionOfThis)) insertdrop+='<input type="hidden" name="refgenome" value="1" />';
          else insertdrop+='<input type="hidden" name="refgenome" value="'+String(parseInt(positionOfThis) + 1 )+'" />';

                              insertdrop+='<input type="hidden" name="rundatabasesearch" value="rundatabasesearch" />'+
                                          '<li class="FontModals">E-value:</li><input type="name" class="form-control" id="edit_Evalue" name="edit_Evalue" placeholder="0.001">'+
                                          '<li class="FontModals">Miminum Alignment:</li><input type="name" class="form-control" id="edit_Align" name="edit_Align" placeholder="300">'+
                                          '<input type="hidden" name="querygene" value="'+presentGene+'" />'+
                                          '<input type="hidden" name="geneBegin" value="'+geneBegin+'">'+
                                          '<input type="hidden" name="geneEnd" value="'+geneEnd+'">'+
                                          '<input type="hidden" name="geneReference" value="'+geneReference+'">'+
                                        '</div>'+
                                     '</div><div class="modal-footer">'+
                                      '<button type="button" class="btn btn-default btn-lg" data-dismiss="modal">Close</button>'+
                                      '<button type="submit" class="btn btn-primary btn-lg" name="CheckSimilarity">BLAST!</button></div></div></div></div></form>'+
                                    '<button href="#" data-toggle="modal" data-target="#myModalsequenceParameters" class="btn btn-link">BLAST ' + geneToUse + ' against next position sequences.</button>';
          }


          /*insertdrop+= '<hr></hr><form enctype="multipart/form-data" action="searchWithContigs.php" method="POST">'+
                                     '<input type="hidden" name="rundatabasesearch" value="rundatabasesearch" />'+
                                     '<input type="hidden" name="searchNCBI" value="searchNCBI" />'+
                            '<input type="hidden" name="querygene" value="'+presentGene+'" />'+
                            '<input type="hidden" name="geneBegin" value="'+geneBegin+'">'+
                            '<input type="hidden" name="geneReference" value="'+geneReference+'">'+
                            '<input type="hidden" name="geneEnd" value="'+geneEnd+'">';
                            if(String(numberOfGenomes)==String(positionOfThis)) insertdrop+='<input type="hidden" name="refgenome" value="1" />';
                                     else insertdrop+='<input type="hidden" name="refgenome" value="'+String(parseInt(positionOfThis) + 1 )+'" />';
          insertdrop+= '<button type="submit" class="btn btn-link">Check sequence similarity for the gene ' + presentGene.split("...")[1] + ' in the NCBI database.</button>'+
                                    '</form>';
          */

          if(searchBysequence=='yes' && fileName.indexOf('.fasta')>-1){
          insertdrop+= '<form enctype="multipart/form-data" id="Annotate" action="searchWithContigs.php" method="POST">'+
                                     '<input type="hidden" name="rundatabasesearch" value="rundatabasesearch" />'+
                                     '<input type="hidden" name="AnnotateRegion" value="AnnotateRegion" />'+
                                     '<input type="hidden" name="QueryRegion" value="'+presentGene+'" />'+
                                     '<input type="hidden" name="geneBegin" value="'+geneBegin+'" />'+
                                     '<input type="hidden" name="geneEnd" value="'+geneEnd+'" />'+
                            '<button type="submit" class="btn btn-link">Annotate this region.</button>'+
                                    '</form>';
          }
          
          var passSelection='';

          for (i in typesearch_array){
            if(typesearch_array[i]!='GeneProduct' && typesearch_array[i]!='GeneName') passSelection='yes';
          }
          if (passSelection=='yes' && ArrayOfRegionSelect.length!=0){
            StringOfRegion=ArrayOfRegionSelect.join('---');
            StringOfRegion=StringOfRegion.replace(/\|/g,'-.')
            StringOfRegion=StringOfRegion.replace(/ /g,'__')
            StringOfRegion=StringOfRegion.replace(/\(/g,'..')
            StringOfRegion=StringOfRegion.replace(/\)/g,'...')
            insertdrop+= ''+
                          '<form enctype="multipart/form-data" action="' + currentpage + '" method="POST">'+
                                          '<input type="hidden" name="selectionToExport" value="'+StringOfRegion+'">'+
                                          '<input type="hidden" name="genomeToExport" value="'+presentGene.split("...")[0]+'">'+
                                          '<input type="hidden" name="contigNumber" value="'+contigNumber+'">'+
                                          '<button href="#" type="submit" class="btn btn-link">Export Selection</button>'+
                          '</form>';
          }

          insertdrop+= '<br><div class="modal fade" id="myModaledit_info" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">'+
                                  '<div class="modal-dialog">'+
                                    '<div class="modal-content">'+
                                    '<form enctype="multipart/form-data" action="' + currentpage + '" method="POST">'+
                                      '<div class="modal-header">'+
                                        '<button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>'+
                                        '<h4 class="modal-title" id="myModalLabel"><a class="FontModalsTitle">Edit Information</a></h4>'+
                                      '</div>'+
                                      '<div class="modal-body">'+
                                        '<div class="form-group">'+
                                          '<li class="FontModals">Gene Name</li>'+
                                          '<input type="name" class="form-control" id="GeneName" name="EditName" placeholder="'+Pgene+'">'+
                                          '<input type="hidden" name="OriginalName" value="'+presentGene+'">'+
                                          '<input type="hidden" name="geneBegin" value="'+geneBegin+'">'+
                                          '<input type="hidden" name="geneEnd" value="'+geneEnd+'">'+
                                        '</div>'+
                                      '<div class="form-group">'+
                                        '<li class="FontModals">Gene Product</li>'+
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

    $("#HitTable").on("contextmenu","tbody tr",function (e) {
        arrayOfColumns=this.getElementsByTagName("td");
        matchesToUse=arrayOfColumns[10].getElementsByTagName("input")[0].value;
        SequenceQuery1=arrayOfColumns[8].getElementsByTagName("input")[0].value;
        SequenceTarget1=arrayOfColumns[6].getElementsByTagName("input")[0].value;
        AlignEnd=arrayOfColumns[9].innerHTML;
        nameSource=arrayOfColumns[2].getElementsByTagName("input")[1].value;
        nameTarget=arrayOfColumns[3].getElementsByTagName("input")[1].value;
        $contextMenu2[0].innerHTML ='';
        $contextMenu2[0].innerText ='';
        $contextMenu2.append('<ul class="dropdown-menu" role="menu" aria-labelledby="dropdownMenu" style="display:block;position:static;margin-bottom:5px;">'+
                              '<form enctype="multipart/form-data" id="ShowAlignSeq" action="searchWithContigs.php" method="POST">'+
                                     '<input type="hidden" name="sequenceQueryToSee" value="'+SequenceQuery1+'" />'+
                                     '<input type="hidden" name="sequenceTargetToSee" value="'+SequenceTarget1+'" />'+
                                     '<input type="hidden" name="matchesToSee" value="'+matchesToUse+'" />'+
                                     '<input type="hidden" name="nameSource" value="'+nameSource+'" />'+
                                     '<input type="hidden" name="nameTarget" value="'+nameTarget+'" />'+
                                     '<input type="hidden" name="ShowAlignSeq" value="ShowAlignSeq" />'+
                            '<button type="submit" class="btn btn-link">Show HSP Aligned</button></form>');
              
        $contextMenu2.css({
            display: "block",
            left: e.pageX,
            top: e.pageY

        });


    });

});

////////////////////////////////////////////////////////////////////////////





};