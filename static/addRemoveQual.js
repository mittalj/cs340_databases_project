function addQualEvent() {
  var newClone = document.getElementById("qualDivId").cloneNode(true);
  var count = document.getElementsByClassName("qualDivField").length;
  newClone.childNodes[3].id = newClone.childNodes[3].id + count;
  newClone.id = newClone.id + count;
  document.getElementById("mainQualDiv").appendChild(newClone);
};

function remove_qual()
{
  var idVal = (document.getElementsByClassName("qualDivField").length) - 1;
  if (idVal >= 1)
  {
    var itemToRemove = document.getElementById("qualDivId" + idVal);
    itemToRemove.remove();
  }
}

window.addEventListener('load', function() {
  //var qualCount = document.getElementById("qualCount").value;
  var qualLength = document.getElementsByName('tQuals').length
  var trainerQuals = [];
  for (i=0; i < qualLength; i++)
  {
    trainerQuals.push(document.getElementsByName('tQuals')[i].value);
  }

  // Select first qual element 
  selectElement('qual_id', trainerQuals[0]);

  for (i = 1; i < qualLength; i++) {
    var newClone = document.getElementById("qualDivId").cloneNode(true);
    newClone.childNodes[3].id = newClone.childNodes[3].id + i;
    selectID =  newClone.childNodes[3].id;
    newClone.id = newClone.id + i;
    document.getElementById("mainQualDiv").appendChild(newClone);
    selectElement(selectID, trainerQuals[i]);
  }
});

<!-- https://stackoverflow.com/questions/78932/how-do-i-programmatically-set-the-value-of-a-select-box-element-using-javascript -->
function selectElement(id, valueToSelect) {
    let element = document.getElementById(id);
    element.value = valueToSelect;
}
