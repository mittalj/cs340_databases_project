/*
document.addEventListener('DOMContentLoaded', function() {
  document.getElementById("addMoreQual").addEventListener("click",  addQualEvent);
});

document.addEventListener('DOMContentLoaded', function() {
  document.getElementById("removeQual").addEventListener("click",  remove_qual);
});
*/

function addQualEvent() {
  var newClone = document.getElementById("qualDivId").cloneNode(true);
  var count = document.getElementsByClassName("qualDivField").length;
  newClone.childNodes[3].id = newClone.childNodes[3].id + count
  newClone.id = newClone.id + count
  document.getElementById("mainQualDiv").appendChild(newClone);
};

function remove_qual()
  {
    var idVal = (document.getElementsByClassName("qualDivField").length) - 1;
    if (idVal >= 1)
    {
      var itemToRemove = document.getElementById("qualDivId" + idVal)
      itemToRemove.remove();
    }
  }
