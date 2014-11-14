
//Function to create the Object with information about all the genomic regions
var prep_data = function(plot_info, nodes) {

  var g       = plot_info.global
      g.nodes = nodes;

  var ax = plot_info.axes;

  var check_nodes = function(nodes) {
    var defined = {};
    for (var i=0; i<nodes.length; i++) {
      var contig = nodes[i];
      for( j in contig){
        for (var y=0; y<contig[j].length; y++) {
          var node_name  = contig[j][y].gene;
          if (!defined[node_name]) defined[node_name] = true;
        }
      }
    }

    for (var i=0; i<nodes.length; i++) {
      var contig = nodes[i];
      for( j in contig){
        for (var y=0; y<contig[j].length; y++) {
          var node_name  = contig[j][y].gene;
          var imports    = contig[j][y].imports;
        
        for (var z=0; j<imports.length; j++) {
          var imp_name = imports[z];
          if (!defined[imp_name]) {
            var msg = 'Error: Target node (' + imp_name +
                      ') not found for source node (' + node_name + ').';
            console.log (msg);
  } } } } } };

  check_nodes(nodes);

  var countAllNodes=-1;

  var index_by_node_name = function(d) {
    countAllNodes+=1;
    d.connectors          = [];
    d.packageName         = d.product;
    g.nodesByName[d.gene] = d;
    d.indexGeral          =countAllNodes;
    
  };

  g.nodesByName   = {};
  for (i in g.nodes) {
    for (j in g.nodes[i]){
      var contig = g.nodes[i][j];
      contig.forEach(index_by_node_name);
    }
  }
  

  var do_source = function(source) {

    var do_target = function(targetName) {
      var target = g.nodesByName[targetName];
      source.importID.push(target.indexGeral);
        if (!source.source) {
          source.source = { node: source,  degree: 0 };
          source.connectors.push(source.source);
        }

        if (!target.target) {
          target.target = { node: target,  degree: 0 };
          target.connectors.push(target.target);
        }

        g.links.push( { source: source.source,  target: target.target } );

        if ( !g.sources[targetName]  ) g.sources[targetName]  = {};
        g.sources[targetName][source.gene]  = true;

        if ( !g.targets[source.gene] ) g.targets[source.gene] = {};
        g.targets[source.gene][targetName]  = true;

    }
    source.importID=[];
    source.imports.forEach(do_target);
  };

  g.links     = [];
  g.sources   = {};
  g.targets   = {};

  for (i in g.nodes) {
    for (j in g.nodes[i]){
      var contig = g.nodes[i][j];
      contig.forEach(do_source);
    }
  }


  var node_type = function(node) {
    
    var geneStr="Str"+node.genome;
    node.connectors   = [{ node: node }];
    node.type = geneStr;
    if (node.source) node.source.type = geneStr; 
    if (node.target) node.type = node.target.type = geneStr;

  };

  for (i in g.nodes) {
    for (j in g.nodes[i]){
      var contig = g.nodes[i][j];
      contig.forEach(node_type);
    }
  }

  g.entrieNodeByType = [];
  countEntrie = 0;
  for (i in nodes) {
      for (j in nodes[i]){
        var contig = nodes[i][j];
        for (z in contig){
          g.entrieNodeByType[countEntrie] = contig[z];
          countEntrie += 1;
        }
      }
  }

  g.nodesByType = d3.nest()
    .key(function(d) { return d.type;})
    .sortKeys(d3.ascending)
    .entries(g.entrieNodeByType);


  var type_rank = function(type) {

    var countIndex     = 0;
    var countgenes = 0;
    var NumGenes = 0;
    var prevBegin=".";
    var MoreContigs='no';
    if (prevG != type.values[0].genome){
      prevContig = type.values[0].contig;
      prevG = type.values[0].genome;
    } 
  
    var node_rank = function(d, i) {
      countRank+=1;
      if(prevContig == d.contig){
        d.index   = countIndex++;
        countgenes++;
        if (d.begin!=prevBegin){
        NumGenes+=1;
        prevBegin=d.begin;
      }
      }
      else{
        MoreContigs='yes';
        if (countRank==1)countIndex = countIndex + 1;
        else countIndex = countIndex + 35;
        d.index = countIndex;
        countgenes++;
        prevContig = d.contig;
        prevCont = d.contig;
        if (d.begin!=prevBegin){
        NumGenes+=1;
        prevBegin=d.begin;
      }
      }
    };
    var countRank=0;
    type.values.forEach(node_rank);
    if (MoreContigs=='yes') type.moreContigs='yes';
    else type.moreContigs='no';
    type.count=countgenes;
    type.NumGenes=NumGenes;
  };
  var prevContig = '1';
  var prevG = '1';
  g.nodesByType.forEach(type_rank);

  var bigger=0;
  var longerGenome = function (type) {
    if (type.count>bigger){
      bigger=type.count;
    }
  }

  g.nodesByType.forEach(longerGenome);

var arrangedIndexes = new Array();
var arrangedGenes = new Array();
var prevSourceLink = '';
var product = '';
var gen='';


function searchInType(typeTarget,begin){
  var ind = 0;
  for( i in g.nodesByType[typeTarget].values){
    if (g.nodesByType[typeTarget].values[i].begin == begin) return ind;
    else ind += 1;
  }
  return null;
}

  var arrangeGenome = function (link){
    var source = link.source.node;
    var target = link.target.node;
    console.log(link);
    var lengthGenomeArr;
    console.log(arrangedIndexes);
    console.log(arrangedGenes);

    
      var sortIndex = function(source, target){
        var indexSource = source.index;
        var indexTarget = target.index;
        var typeTarget = target.type;
        var decrescente = 1;
        var crescente = 1;
        if (typeTarget == 'Str2'){
          typeTarget = 1;
          lengthGenomeArr = g.nodesByType[typeTarget].values.length;
        }

        if(prevSourceLink.gene == source.gene){
          console.log('Aqui!');
          if (gen == source.gene) console.log('Puff');
          else{
         

          if(source.gene == target.gene){
            console.log(link);
            var indexalter = searchInType(typeTarget,target.begin);
            console.log('alter:');
            console.log(indexalter);
            console.log(indexSource);  
            g.nodesByType[typeTarget].values[indexalter].index = indexSource;
            arrangedIndexes.push(indexSource);
            arrangedGenes.push(target.gene);
            console.log(arrangedIndexes);
            console.log(arrangedGenes);
            
          }
        }
        }
        
        else{
      
       if (arrangedIndexes.indexOf(indexSource)>-1);
        
        else{
          if(source.gene == target.gene){
            if (arrangedGenes.indexOf(target.gene)>-1) console.log('Duplicado!');
            else{
            g.nodesByType[typeTarget].values[indexTarget].index = indexSource;
            arrangedIndexes.push(indexSource);
            arrangedGenes.push(target.gene);
            console.log('normal');
            console.log(indexSource);
            console.log(indexTarget);
            console.log(g.nodesByType[typeTarget].values[indexTarget]);
            }
          }
          
        }

        if(source.gene == target.gene){
        var indexSourceless = indexSource;
        var indexSourceadd = indexSource;
        if(source.begin == target.begin){

        while ((g.nodesByType[typeTarget].values[indexTarget - decrescente] != undefined) && (g.nodesByType[typeTarget].values[indexTarget - decrescente].gene == source.gene)){
          indexSourceless += 1;
          var nodeChange = g.nodesByType[typeTarget].values[indexTarget - decrescente];
          arrangedIndexes.push(indexSourceless);
          arrangedGenes.push(target.gene);
          nodeChange.index = indexSourceless;
          console.log('decrescente');
          console.log(indexSourceless);
          gen = nodeChange.gene;

          console.log(arrangedIndexes);
          console.log(arrangedGenes);
          decrescente += 1;
        }
        }
        }

    }
  }
    if (source.type != target.type) sortIndex(source,target);
    prevSourceLink = source;
    
  }

  if (align == 'align') g.links.forEach(arrangeGenome);

  
  // Console logging calls.
  
  if (false) {
    console.log('g.links',          g.links); //T
    console.log('g.nodes',          g.nodes); //T
    console.log('g.nodesByType',    g.nodesByType); //T
    console.log('g.nodesByName',    g.nodesByName); //T
    console.log('g.sources',        g.sources); //T
  }

};