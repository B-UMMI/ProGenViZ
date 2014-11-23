
//Function that show global statistics of the uploaded genomes
function dash(){


var nameGenome='';

divName=document.getElementById("nameGenome");

if ($('#myModaldashboard1').hasClass('in')){
    var option = document.forms["statFile1"]["selectStat"].value;
}
else{
    var option = document.forms["statFile"]["selectStat"].value;
}


ArrayOfSizes=[]
var numberOfBars=10;
var AllUndef='';
var firstBarsIncrement=200;
var intervalSize=(biggestGene+100)/numberOfBars;
var increment=firstBarsIncrement;
var start=0;
for (i=0;i<numberOfBars;i++){
    if (i<9){
        strSize=String(start)+'-'+String(increment);
        ArrayOfSizes[strSize]={};
        start=increment+1;
        increment+=firstBarsIncrement;
    }
    else{
        strSize=String('>'+(increment+1));
        ArrayOfSizes[strSize]={};
    }
}

var indexUndefined=ArrayOfProducts.indexOf('Undefined');
ArrayOfProducts.splice(indexUndefined,1);
ArrayOfColors.splice(indexUndefined,1);

var countArrayOfSizes=0;
//Option to use all files
if (option=='all'){

AllUndef='true';
for (i in allInfo.nodesByType){
    if (i==allInfo.nodesByType.length-1) nameGenome+=allInfo.nodesByType[i].values[0].name;
    else nameGenome+=allInfo.nodesByType[i].values[0].name+' and ';
    var prevBegin='';
    for (j in allInfo.nodesByType[i].values){
        var countArrayOfSizes=0;
        if (prevBegin==allInfo.nodesByType[i].values[j].begin || allInfo.nodesByType[i].values[j].product=='Undefined');
        else{
        AllUndef='false';
        var prod=allInfo.nodesByType[i].values[j].product.replace(',','');
        var genelength=parseInt(allInfo.nodesByType[i].values[j].end)-parseInt(allInfo.nodesByType[i].values[j].begin);

        for(k in ArrayOfSizes){
            countArrayOfSizes+=1;
            if(countArrayOfSizes<10){
                less=parseInt(k.split('-')[0]);
                more=parseInt(k.split('-')[1]);
            
                if (parseInt(genelength) >= less && parseInt(genelength) < more){
                    if (typeof(ArrayOfSizes[k][prod])=='undefined') ArrayOfSizes[k][prod]= 1;
                    else ArrayOfSizes[k][prod]= ArrayOfSizes[k][prod] + 1;
                }
            }
            else{
                more=parseInt(k.split('>')[1]);
            
                if (parseInt(genelength) >= more){
                    if (typeof(ArrayOfSizes[k][prod])=='undefined') ArrayOfSizes[k][prod]= 1;
                    else ArrayOfSizes[k][prod]= ArrayOfSizes[k][prod] + 1;
                }
            }
        }        
        prevBegin=allInfo.nodesByType[i].values[j].begin;
        }
    }
}
nameGenome+=' sequences';

}

//Option to use specific files
else{
    AllUndef='true';
    number=parseInt(option);
    var prevBegin='';
    nameGenome+=allInfo.nodesByType[number].values[0].name;
    for (j in allInfo.nodesByType[number].values){
        var countArrayOfSizes=0;
        if (prevBegin==allInfo.nodesByType[number].values[j].begin || allInfo.nodesByType[number].values[j].product=='Undefined');
        else{
        AllUndef='false';
        var prod=allInfo.nodesByType[number].values[j].product.replace(',','');
        var genelength=parseInt(allInfo.nodesByType[number].values[j].end)-parseInt(allInfo.nodesByType[number].values[j].begin);

        for(k in ArrayOfSizes){
            countArrayOfSizes+=1;
            if(countArrayOfSizes<10){
                less=parseInt(k.split('-')[0]);
                more=parseInt(k.split('-')[1]);
            
                if (parseInt(genelength) >= less && parseInt(genelength) < more){
                    if (typeof(ArrayOfSizes[k][prod])=='undefined') ArrayOfSizes[k][prod]= 1;
                    else ArrayOfSizes[k][prod]= ArrayOfSizes[k][prod] + 1;
                }
            }
            else{
                more=parseInt(k.split('>')[1]);
            
                if (parseInt(genelength) >= more){
                    if (typeof(ArrayOfSizes[k][prod])=='undefined') ArrayOfSizes[k][prod]= 1;
                    else ArrayOfSizes[k][prod]= ArrayOfSizes[k][prod] + 1;
                }
            }
        }       
        prevBegin=allInfo.nodesByType[number].values[j].begin;
        }
    }
nameGenome+=' sequences';

}

if (AllUndef=='true'){
    $('#myModalAllUndefined').modal('show');

}
else{

for (i in allInfo.nodesByType){
    var prevBegin='';
    for (j in allInfo.nodesByType[i].values){
        if (prevBegin==allInfo.nodesByType[i].values[j].begin || allInfo.nodesByType[i].values[j].product=='Undefined');
        else{
            var prod=allInfo.nodesByType[i].values[j].product.replace(',','');
            for(k in ArrayOfSizes){
                if (typeof(ArrayOfSizes[k][prod])=='undefined') ArrayOfSizes[k][prod]= 0;
                prevBegin=allInfo.nodesByType[i].values[j].begin;
            }
        }
    }
}


var freqData='[';
var countbars=0;
for(k in ArrayOfSizes){
    countbars+=1;
    freqData+='{"State":"'+k+'","freq":{';

    for (i in ArrayOfSizes[k]){
        freqData+='"'+i+'":'+ArrayOfSizes[k][i]+',';
    }
    if (countbars==numberOfBars) freqData+='}}';
    else freqData+='}},';
    freqData=freqData.replace(',}','}');
}

freqData+=']';

datainput=jQuery.parseJSON( freqData );

divName.innerHTML='<h4>'+nameGenome+'</h4>';

var clickPie='out';
var clickHG='out';
var rD=''; //Prev Data


//Function that creates the multiple visualization ways of global statistcs of gene size and function
function dashboard(HGid, PCid,fData, legendId){

    if ($('#myModaldashboard').hasClass('in')){
    $('#myModaldashboard').modal('hide');
    if (DataTable!=''){
        d3.select(HGid).select("svg").remove();
        d3.select(PCid).select("svg").remove();
        DataTable.fnDestroy();
        d3.select(legendId).select("tbody").remove();
    }
}

    if ($('#myModaldashboard1').hasClass('in')){

            d3.select(HGid).select("svg").remove();
            d3.select(PCid).select("svg").remove();
            DataTable.fnDestroy();
            d3.select(legendId).select("tbody").remove();
    }



    var barColor = '#0790A5';
    function segColor(c){ var index = ArrayOfProducts.indexOf(c);
                          return ArrayOfColors[index]; }
    
    // compute total for each state.
    fData.forEach(function(d){
                        d.total=0;
                        for (i in d.freq){
                            d.total=d.total+d.freq[i];
                        }
                    });
    
    // function to handle histogram.
    function histoGram(fD){
        var hG={},    hGDim = {t: 60, r: 0, b: 30, l: 0};

        var larg=(screen.width/2.8);
        var cump=(screen.height/2.8);

        hGDim.w = larg - hGDim.l - hGDim.r, 
        hGDim.h = cump - hGDim.t - hGDim.b;
            
        //create svg for histogram.
        var hGsvg = d3.select(HGid).append("svg")
            .attr("width", hGDim.w + hGDim.l + hGDim.r)
            .attr("height", hGDim.h + hGDim.t + hGDim.b).append("g")
            .attr("transform", "translate(" + hGDim.l + "," + hGDim.t + ")");

        // create function for x-axis mapping.
        var x = d3.scale.ordinal().rangeRoundBands([0, hGDim.w], 0.1)
                .domain(fD.map(function(d) { return d[0]; }));

        // Add x-axis to the histogram svg.
        hGsvg.append("g").attr("class", "x axis")
            .attr("transform", "translate(0," + hGDim.h + ")")
            .call(d3.svg.axis().scale(x).orient("bottom"));

        // Create function for y-axis map.
        var y = d3.scale.linear().range([hGDim.h, 0])
                .domain([0, d3.max(fD, function(d) { return d[1]; })]);

        // Create bars for histogram to contain rectangles and freq labels.
        var bars = hGsvg.selectAll(".bar").data(fD).enter()
                .append("g").attr("class", "bar");
        
        //create the rectangles.
        var prevRect='';
        var firstTime='yes';
        bars.append("rect")
            .attr("x", function(d) { return x(d[0]); })
            .attr("y", function(d) { return y(d[1]); })
            .attr("id", function(d) {return d[0];})
            .attr("width", x.rangeBand())
            .attr("height", function(d) { return hGDim.h - y(d[1]); })
            .attr('fill',barColor)
            .on("click",onclickHist);// mouseover is defined below.
            //.on("mouseout",mouseout);// mouseout is defined below.
            
        //Create the frequency labels above the rectangles.
        bars.append("text").text(function(d){ return d3.format(",")(d[1])})
            .attr("x", function(d) { return x(d[0])+x.rangeBand()/2; })
            .attr("y", function(d) { return y(d[1])-5; })
            .attr("class",'legendBar')
            .attr("text-anchor", "middle");
        
        function onclickHist(d){
            if (prevRect==document.getElementById(d[0]).getAttribute('id') && clickHG!='out'){
                mouseout(d);
                prevRect=document.getElementById(d[0]).getAttribute('id');
                clickHG='out';
            }
            else{
                console.log(prevRect);
                if (firstTime=='yes') firstTime='no';
                else{
                    document.getElementById(prevRect).removeAttribute("style");
                    document.getElementById(prevRect).setAttribute("fill",barColor);
                } 
                mouseover(d);
                prevRect=document.getElementById(d[0]).getAttribute('id');
                console.log(prevRect);
                clickHG='in';
            }
        }

        function mouseover(d){  // utility function to be called on mouseover.
            // filter for selected state.
            document.getElementById(d[0]).setAttribute("style","fill:red");
            var st = fData.filter(function(s){ return s.State == d[0];})[0],

            /**var nD=[];
            for (i in st.freq){
                nD.push({type:i, freq: st.freq[i]});
            }*/
                nD = d3.keys(st.freq).map(function(s){ 
                    //console.log(s);
                    return {type:s, freq:st.freq[s]};});

                rD=nD;

            // call update functions of pie-chart and legend.    
            pC.update(nD);
            leg.update(nD);
        }
        
        function mouseout(d){    // utility function to be called on mouseout.
            // reset the pie-chart and legend. 
            document.getElementById(d[0]).removeAttribute("style");
            document.getElementById(d[0]).setAttribute("fill",barColor);   
            pC.update(tF);
            leg.update(tF);
        }
        
        // create function to update the bars. This will be used by pie-chart.
        hG.update = function(nD, color){
            // update the domain of the y-axis map to reflect change in frequencies.
            y.domain([0, d3.max(nD, function(d) { return d[1]; })]);
            
            // Attach the new data to the bars.
            var bars = hGsvg.selectAll(".bar").data(nD);
            
            // transition the height and color of rectangles.
            bars.select("rect").transition().duration(500)
                .attr("y", function(d) {return y(d[1]); })
                .attr("height", function(d) { return hGDim.h - y(d[1]); })
                .attr("fill", color);

            // transition the frequency labels location and change value.
            bars.select("text").transition().duration(500)
                .text(function(d){ return d3.format(",")(d[1])})
                .attr("y", function(d) {return y(d[1])-5; });            
        }        
        return hG;
    }
    
    // function to handle pieChart.
    function pieChart(pD){
        var larg=(screen.width/2.8);
        var cump=(screen.height/2.8);
        var pC ={},    pieDim ={w:larg, h: cump};
        pieDim.r = Math.min(pieDim.w, pieDim.h) / 2;

        var dataToUse=[];

        for (i in pD){
            if (pD[i].freq==0);
            else dataToUse.push(pD[i]);
        }
                
        // create svg for pie chart.
        var piesvg = d3.select(PCid).append("svg")
            .attr("width", pieDim.w).attr("height", pieDim.h).append("g")
            .attr("transform", "translate("+pieDim.w/2+","+pieDim.h/2+")");
        
        // create function to draw the arcs of the pie slices.
        var arc = d3.svg.arc().outerRadius(pieDim.r).innerRadius(0);

        // create a function to compute the pie slice angles.
        var pie = d3.layout.pie().value(function(d) { return d.freq; });

        // Draw the pie slices.
        //console.log(pD);
        var prevPie='';
        var firstTime='yes';
        var prevDataType='';
        piesvg.selectAll("path").data(pie(dataToUse)).enter().append("path").attr("d", arc)
            .each(function(d) { 
                this._current = d; })
            .attr("id", function(d) {return d.data.type;})
            .attr("stroke-width", 0)
            .style("fill", function(d) { 
                //console.log(d.data.type);
                var index = ArrayOfProducts.indexOf(d.data.type);
                return ArrayOfColors[index]; })
            .on("mouseover",mouseover).on("mouseout",mouseout);

        // create function to update pie-chart. This will be used by histogram.
        pC.update = function(nD){

            var dataToUse=[];

            for (i in nD){
                if (nD[i].freq==0);
                else dataToUse.push(nD[i]);
            }

            piesvg.selectAll("path").remove();

            piesvg.selectAll("path").data(pie(dataToUse)).enter().append("path").attr("d", arc)
            .each(function(d) { 
                this._current = d; })
            .attr("id", function(d) {return d.data.type;})
            .attr("stroke-width", 0)
            .style("fill", function(d) { 
                //console.log(d.data.type);
                var index = ArrayOfProducts.indexOf(d.data.type);
                return ArrayOfColors[index]; })
            .on("mouseover",mouseover).on("mouseout",mouseout);
        } 
       
        // Utility function to be called on mouseover a pie slice.
        function mouseover(d){
            // call the update function of histogram with new data.
            /**var nD=[];
            for (i in st.freq){
                nD.push({type:i, freq: st.freq[i]});
            }*/
                nD = [{type:d.data.type, freq:d.data.freq}];
            //console.log(nD);
            leg.update(nD);

            hG.update(fData.map(function(v){ 
                return [v.State,v.freq[d.data.type]];}),segColor(d.data.type));
        }
        //Utility function to be called on mouseout a pie slice.
        function mouseout(d){
            // call the update function of histogram with all data.
            if (clickHG=='in'){
                leg.update(rD);
                hG.update(fData.map(function(v){
                return [v.State,v.total];}), barColor);
            }
            else{
            leg.update(tF);
            hG.update(fData.map(function(v){
                return [v.State,v.total];}), barColor);
        }
        }
        // Animating the pie-slice requiring a custom function which specifies
        // how the intermediate paths should be drawn.
        function arcTween(a) {
            var i = d3.interpolate(this._current, a);
            this._current = i(0);
            return function(t) { return arc(i(t));    };
        }    
        return pC;
    }
    
    // function to handle legend.
    function legend(lD){
        var leg = {};
        var dataToUse=[];
        // create table for legend.
        var legend = d3.select(legendId);

        for (i in lD){
            if (lD[i].freq==0);
            else dataToUse.push(lD[i]);
        }
        
        // create one row per segment.
        var tr = legend.append("tbody").selectAll("tr").data(dataToUse).enter().append("tr");
            
        // create the first column for each segment.
        tr.append("td").append("svg").attr("width", '16').attr("height", '16').append("rect")
            .attr("width", '16').attr("height", '16')
			.attr("fill",function(d){ return segColor(d.type); });
            
        // create the second column for each segment.
        tr.append("td").attr("class",'legendName').attr('id',function(s){return s.type;}).text(function(d){ return d.type;});

        // create the third column for each segment.
        tr.append("td").attr("class",'legendFreq').attr('id',function(s){return s.type+'Freq';})
            .text(function(d){ return d3.format(",")(d.freq);});

        // create the fourth column for each segment.
        tr.append("td").attr("class",'legendPerc').attr('id',function(s){return s.type+'Perc';})
            .text(function(d){ return getLegend(d,lD);});

        // Utility function to be used to update the legend.
        leg.update = function(nD){

            var dataToUse=[];
            for (i in nD){
            if (nD[i].freq==0);
            else dataToUse.push(nD[i]);
        }

        DataTable.fnDestroy();
            // update the data attached to the row elements.
            var l = legend.select("tbody").selectAll("tr").remove();

            var tr = legend.select("tbody").selectAll("tr").data(dataToUse).enter().append("tr");
            
        // create the first column for each segment.
        tr.append("td").append("svg").attr("width", '16').attr("height", '16').append("rect")
            .attr("width", '16').attr("height", '16')
            .attr("fill",function(d){ return segColor(d.type); });
            
        // create the second column for each segment.
        tr.append("td").attr("class",'legendName').attr('id',function(s){return s.type;}).text(function(d){ return d.type;});

        // create the third column for each segment.
        tr.append("td").attr("class",'legendFreq').attr('id',function(s){return s.type+'Freq';})
            .text(function(d){ return d3.format(",")(d.freq);});

        // create the fourth column for each segment.
        tr.append("td").attr("class",'legendPerc').attr('id',function(s){return s.type+'Perc';})
            .text(function(d){ return getLegend(d,lD);});    

        DataTable=$('#legend').dataTable({
            "iDisplayLength": 25,
            "aaSorting": [[ 2, "desc" ]]
        });
        }

        
        function getLegend(d,aD){ // Utility function to compute percentage.
            return d3.format(".2%")(d.freq/d3.sum(aD.map(function(v){ return v.freq; })));
        }

        DataTable=$('#legend').dataTable({
            "iDisplayLength": 25,
            "aaSorting": [[ 2, "desc" ]]
        });

        return leg;
    }
    
    // calculate total frequency by segment for all state.
    var tF = ArrayOfProducts.map(function(d){ 
        var countProducts=0;
        for (i in fData){
            countProducts+=fData[i].freq[d];
        }
        return {type:d, freq: countProducts}; 
    });    
    
    //console.log(tF);
    // calculate total frequency by state for all segment.
    var sF = fData.map(function(d){return [d.State,d.total];});


    var hG = histoGram(sF), // create the histogram.
        pC = pieChart(tF), // create the pie-chart.
        leg= legend(tF);  // create the legend.

}

dashboard('#histo','#pieChart',datainput,'#legend');
$('#myModaldashboard1').modal('show');
}

}