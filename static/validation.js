// https://stackoverflow.com/questions/42713089/validate-date-of-birth-greater-than-today
// https://stackoverflow.com/questions/7091130/how-can-i-validate-that-someone-is-over-18-from-their-date-of-birth

function checkDOB() {
        var dateString = document.getElementById('birth_date').value;
        var birthDate = new Date(dateString);
        var today = new Date();

        var age = today.getFullYear() - birthDate.getFullYear();
        var m = today.getMonth() - birthDate.getMonth();
        if (m < 0 || (m === 0 && today.getDate() <= birthDate.getDate())) {
        age--;
        }

        if ( age < 18 ) {
          alert("They must be at least 18 years old.");
          document.getElementById('birth_date').value = null;
        }
    }
