// Function for the 'Add Qualfication' button on the add/update trainer forms
// This function appends the qual dropdown and assigns it a unique id value
function addQualEvent() {
  var newClone = document.getElementById("qualDivId").cloneNode(true);
  var count = document.getElementsByClassName("qualDivField").length;
  newClone.childNodes[3].id = newClone.childNodes[3].id + count;
  selectID =  newClone.childNodes[3].id;
  newClone.id = newClone.id + count;
  document.getElementById("mainQualDiv").appendChild(newClone);
};

// Function for the 'Remove Qualfication' button on the add/update trainer forms
// This function removes the appended dropdown qual field. This function does
// not work if there is only one qual field. 
function remove_qual()
{
  var idVal = (document.getElementsByClassName("qualDivField").length) - 1;
  if (idVal >= 1)
  {
    var itemToRemove = document.getElementById("qualDivId" + idVal);
    itemToRemove.remove();
  }
}
