// https://stackoverflow.com/questions/42713089/validate-date-of-birth-greater-than-today
// https://stackoverflow.com/questions/7091130/how-can-i-validate-that-someone-is-over-18-from-their-date-of-birth

function checkDOB() {
        var dateString = document.getElementById('birth_date').value;         // Get birthdate from the form
        var birthDate = new Date(dateString);
        var today = new Date();

        var age = today.getFullYear() - birthDate.getFullYear();              // Subtract the years to get the delta
        var m = today.getMonth() - birthDate.getMonth();
        if (m < 0 || (m === 0 && today.getDate() <= birthDate.getDate())) {   // Check if the current month is before the birth month.
        age--;                                                                // If the month is the same, then check the day of the month as well
      }                                                                       // to get the age.

        if ( age < 18 ) {
          alert("They must be at least 18 years old.");
          document.getElementById('birth_date').value = null;
        }
    }
