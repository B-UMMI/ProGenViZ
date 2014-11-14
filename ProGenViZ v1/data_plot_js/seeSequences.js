
//Function to view sequences aligned after a BLAST search
function seeSequencesAligned(){


var sequenceQuery=document.forms[ShowAlignSeq][sequenceQueryToSee];
var sequenceTarget=document.forms[ShowAlignSeq][sequenceTargetToSee];
var matches=document.forms[ShowAlignSeq][matchesToSee];
var nameSource=document.forms[ShowAlignSeq][nameSource];
var nameTarget=document.forms[ShowAlignSeq][nameTarget];


var table = document.getElementById('TableSeeSeq');
Tbody=document.createElement("tbody");
table.appendChild(Tbody);
for(var i=0; i<3; i++){
  row=Tbody.insertRow(i);
  for (var j=0;j<sequenceQuery.length;j++){
    cell=row.insertCell(j);
    cell.style.textAlign = 'center';
    if(j==0 && i==0)cell.innerHTML=nameSource;
    if(j==1 && i==0)cell.innerHTML='Matches';
    if(j==2 && i==0)cell.innerHTML=nameTarget;
    

  }
}
//divName.innerHTML.remove();
