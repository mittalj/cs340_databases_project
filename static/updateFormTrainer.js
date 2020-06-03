window.addEventListener('load', function() {
  var qualLength = document.getElementsByName('tQuals').length   // Get the number of trainer qualifications from the htm hidden input fields
  var trainerQuals = [];
  for (i=0; i < qualLength; i++)
  {
    trainerQuals.push(document.getElementsByName('tQuals')[i].value); // For each trainer qualifcation, push the value into the JS array called trainerQuals
  }

  selectElement('qual_id', trainerQuals[0]);   // Select the first qual element and populate that field since this field is static

  // If the trainer has additional qualifications, run a loop to append the dynamic qualification field and populate the value accordingly
  for (i = 1; i < qualLength; i++) {
    var newClone = document.getElementById("qualDivId").cloneNode(true);
    newClone.childNodes[3].id = newClone.childNodes[3].id + i;
    selectID =  newClone.childNodes[3].id;
    newClone.id = newClone.id + i;
    document.getElementById("mainQualDiv").appendChild(newClone);
    selectElement(selectID, trainerQuals[i]);
  }
});
// https://stackoverflow.com/questions/78932/how-do-i-programmatically-set-the-value-of-a-select-box-element-using-javascript
// Function to select a value in the field based on the passed-in ID value
function selectElement(id, valueToSelect) {
    let element = document.getElementById(id);
    element.value = valueToSelect;
}
