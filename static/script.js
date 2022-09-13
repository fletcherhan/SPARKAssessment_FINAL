function start() {
    document.getElementById("container1").style.display = "none";
    document.getElementById("container2").style.display = "flex";
}
function continue1() {
    document.getElementById("container2").style.display = "none";
    document.getElementById("container3").style.display = "flex";
}
function continue2() {
    document.getElementById("container3").style.display = "none";
    document.getElementById("container4").style.display = "flex";
}
function navtouserdetails() {
    location.href = "assessment";
}


var currentTab = 0; // Current tab is set to be the first tab (0)
showTab(currentTab); // Display the current tab

function showTab(n) {
  // This function will display the specified tab of the form...
  var x = document.getElementsByClassName("tab");
  x[n].style.display = "flex";
  //... and fix the Previous/Next buttons:
  if (n == 0) {
    document.getElementById("prevBtn").style.display = "none";
  } else {
    document.getElementById("prevBtn").style.display = "inline";
  }
  if (n == (x.length - 1)) {
    document.getElementById("nextBtn").innerHTML = "Submit";
  } else {
    document.getElementById("nextBtn").innerHTML = "BEGIN ASSESSMENT";
  }
  //... and run a function that will display the correct step indicator:
  fixStepIndicator(n)
}

function ValidateEmail(input) {
  var validRegex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
  if (input.value.match(validRegex)) {
    return true;
  } else {
    return false;
  }
}

function nextPrev(n) {
  // This function will figure out which tab to display
  var x = document.getElementsByClassName("tab");
  // Exit the function if any field in the current tab is invalid:
  if (n == 1 && !validateForm()) return false;
  // Hide the current tab:
  x[currentTab].style.display = "none";
  // Increase or decrease the current tab by 1:
  currentTab = currentTab + n;
  // if you have reached the end of the form...
  if (currentTab >= x.length) {
    // ... the form gets submitted:
    document.getElementById("regForm").submit();
    return false;
  }
  // Otherwise, display the correct tab:
  showTab(currentTab);
}

function validateForm() {
  // This function deals with validation of the form fields
  var x, y, i, valid = true;
  let radiopresent = 0;
  let radionumber = 0;
  x = document.getElementsByClassName("tab");
  y = x[currentTab].getElementsByTagName("input");
  z = x[currentTab].getElementsByTagName("select");
  // A loop that checks every input field in the current tab:
  for (i = 0; i < y.length; i++) {
    // If a field is empty...
    if (y[i].value == "") {
      // add an "invalid" class to the field:
      y[i].className += " invalid";
      // and set the current valid status to false
      valid = false;
    }
    if(y[i].type=="radio") {
        radiopresent = 1;
        if(y[i].checked == true) {
        valid = false
        radionumber++;}
  }
  }
  //A loop that checks every select field in the current tab:
  for (i = 0; i < z.length; i++){
    // If a field is empty...
    if (z[i].value == "") {
      // add an "invalid" class to the field:
      z[i].className += " invalid";
      // and set the current valid status to false
      valid = false;
    }
  }
  // If the valid status is true, mark the step as finished and valid:
  if (valid) {
    document.getElementsByClassName("step")[currentTab].className += " finish";
  }

  var emailinput = document.getElementById("email");
  var resultemailinput = ValidateEmail(emailinput);
  if (resultemailinput === false){
    emailinput.className += " invalid";
    valid = false;
  }
  else {
    valid = true;
  }
  
  if(radiopresent === 1 && radionumber != 1) 
    {
    // and set the current valid status to false
    valid = false;
    alert("Please select an answer before proceeding. You can always return to review and/or change your answer later on.");
    };
    if(radiopresent === 1 && radionumber === 1) 
    {
    // and set the current valid status to false
    valid = true;
    }
    
  return valid; // return the valid status
}


function fixStepIndicator(n) {
  // This function removes the "active" class of all steps...
  var i, x = document.getElementsByClassName("step");
  var y = document.getElementsByClassName("tab");
  for (i = 0; i < x.length; i++) {
    x[i].className = x[i].className.replace(" active", "");
  }
  //... and adds the "active" class on the current step:
  x[n].className += " active";
}
