function addQualEvent() {
  var newClone = document.getElementById("qualDivId").cloneNode(true);
  var count = document.getElementsByClassName("qualDivField").length;
  newClone.childNodes[3].id = newClone.childNodes[3].id + count;
  selectID =  newClone.childNodes[3].id;
  newClone.id = newClone.id + count;
  document.getElementById("mainQualDiv").appendChild(newClone);
  //document.getElementById(selectID).value = '';
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
