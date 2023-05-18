// variables initialization
const slider = document.getElementById("myRangeSlider");
const output = document.getElementById("slider-value");
const selectAnnualKwh = document.getElementById("id_select_kwh");
// Get the initial value of the selectAnnualKwh element from the form
const initialKwhValue = selectAnnualKwh.value;
const selectDistrict = document.getElementById("id_select_district");
const selectPhase = document.getElementById("id_select_phase");
const submitButton = document.getElementById("submitBtn");
const errorMessage = document.getElementById('error-message-panel');
const errorMessage2 = document.getElementById('error-message-panel5');
const errorMessage3 = document.getElementById('error-message-panel6');
const storageSelect = document.getElementById("with_storage");
const storageKW = document.getElementById("storage_kw");
const noStorage = document.getElementById("without_storage");
// select all radio buttons with the class "form-check-input"
const radioButtons = document.querySelectorAll('.form-check-input');


// Set the initial value of the output element to 0
slider.value = 0;
output.innerHTML = slider.value;
slider.disabled = true;
selectAnnualKwh.disabled = true;
storageSelect.disabled = true;
storageKW.disabled = true;
storageKW.value = 0;

// Update the current slider value (each time you drag the slider handle)
slider.oninput = function() {
    slider.min = 1;
    output.innerHTML = this.value;
    errorMessage3.style = 'none';
};      

selectDistrict.addEventListener("change", function(event){
    errorMessage.style.display = "none";
    selectDistrict.classList.remove('error');

    console.log("The District is: " + selectDistrict.value);
})

// Listen for changes in the phase load input and store the selected option
selectPhase.addEventListener("change", function(event){
    slider.min =0;
    selectAnnualKwh.value = initialKwhValue; // Set the value of the selectAnnualKwh element to the initial value
    slider.value = 0; // Update the slider value to 0 when the phase load is changed
    slider.max = event.target.value === 'single_phase' ? 5 : 10
    slider.disabled = event.target.value === 'phase_load';
    output.innerHTML = slider.value; // Update the output element value to 0 when the phase load is changed
    noStorage.checked = true;
    storageKW.disabled = true;
    
    selectAnnualKwh.disabled = event.target.value === 'phase_load';
    errorMessage2.style.display = "none";
    selectPhase.classList.remove('error');
    
    if (event.target.value === 'single_phase') {
        
        // Enable the first two options and disable the rest
        selectAnnualKwh.options[0].disabled = false;
        selectAnnualKwh.options[1].disabled = false;
        for (let i = 3; i < selectAnnualKwh.options.length; i++) {
            selectAnnualKwh.options[i].disabled = true;
        }
    } else {
        // Enable all options
        for (let i = 0; i < selectAnnualKwh.options.length; i++) {
            selectAnnualKwh.options[i].disabled = false;
        }
    }

    if(event.target.value === 'single_phase' || event.target.value === '3_phase' || event.target.value === 'phase_load' ){
        if (selectAnnualKwh.value = initialKwhValue){
            slider.disabled = true;
            noStorage.checked = true;
            storageSelect.disabled = true;
        }
    }
    console.log(selectPhase.value);
});

// Reset the output element value to the initial value when the reset button is clicked
document.querySelector('button[type="reset"]').addEventListener('click', function(event) {
    noStorage.checked = true;
    storageSelect.disabled = true;
    slider.disabled = true;
    selectAnnualKwh.disabled = true;
    slider.value = 0;
    output.innerHTML = slider.value;
    selectDistrict.classList.remove('error');
    selectPhase.classList.remove('error');
    errorMessage.style.display = 'none';
    errorMessage2.style.display = 'none';
    errorMessage3.style.display = 'none';
});

// Add an event listener to the submit button
submitButton.addEventListener('click', function(event) {
  // Prevent the form from submitting and reloading the page when it's not valid
  if (!validateForm()) {
    event.preventDefault();
  }
});

selectAnnualKwh.addEventListener("change", function(event){
    slider.min =0;
    slider.disabled = false;
    slider.value = 0;
    output.innerHTML = slider.value; // Update the output element value to 0 when the phase load is changed
    storageSelect.disabled = false;
    storageKW.disabled = false;
    storageKW.min = 1;
    console.log(selectAnnualKwh.value);

    if (selectAnnualKwh.value !=0) {
        slider.value = selectAnnualKwh.value
    } else {
        slider.value = 0;
        slider.disabled = true;
        storageSelect
        storageSelect.disabled = true;
        storageKW.disabled = true;
        noStorage.checked = true;
    }

    output.innerHTML = slider.value; 
    storageKW.value = slider.value;
    storageKW.max = slider.value;

    if(slider.addEventListener("change", function(event){
        storageKW.value = slider.value;
        storageKW.max = slider.value;
        console.log(storageKW.value);
        output.innerHTML = slider.value; 
    }))
    
    console.log(storageKW.value);
});

// Used to validate that the calculator form has been filled by the user
function validateForm() {

    if(selectPhase.value === 'phase_load' & selectDistrict.value === "district"){
        slider.classList.add('error');
        selectPhase.classList.add('error');
        errorMessage2.style.display = 'block';
        selectDistrict.classList.add('error'); 
        errorMessage.style.display = 'block';
        return false;
    }else if(selectDistrict.value === "district"){
        selectDistrict.classList.add('error'); // Add the error class to the selectDistrict element
        selectDistrict.classList.add('error'); 
        errorMessage.style.display = 'block';
        return false;
    }else if (selectPhase.value === 'phase_load') {
        selectPhase.classList.add('error');
        errorMessage2.style.display = 'block';
        return false; // return false to indicate that the form was not submitted
    }else if (slider.value === '0') {
        slider.classList.add('error'); // Add the error class to the slider element
        errorMessage3.style.display = 'block';
        return false; // return false to indicate that the form was not submitted
    }
    return true;
};


// loop through the radio buttons and add an event listener to each one
radioButtons.forEach(radioButton => {
    radioButton.addEventListener('click', () => {
    // log the value of the selected radio button
    console.log("Selected radio field is: " + radioButton.value);
    });
});

// Help Poppers to give details about the form fields or selected values
const helpButtons = document.getElementsByClassName('help-popper');
const helpTexts = document.getElementsByClassName('help-text');
const closeIcons = document.getElementsByClassName('close-help');
const numberOfHelpButtons = helpButtons.length;

let isOpen = new Array(numberOfHelpButtons).fill(true);


// for loop to check if the text element for each button is opened
// if a text is opened and other button is pressed, previous text closes
for (let i = 0; i < numberOfHelpButtons; i++) {
  helpButtons[i].addEventListener('click', function() {
    for (let j = 0; j < numberOfHelpButtons; j++) {
      if (i !== j && !isOpen[j]) {
        helpTexts[j].style.display = 'none';
        helpTexts[j].classList.remove('movePosition');
        closeIcons[j].style.display = 'none';
        closeIcons[j].classList.remove('movePosition');
        isOpen[j] = true;
      }
    }

    if (isOpen[i]) {
        helpTexts[i].style.display = 'block';
        helpTexts[i].classList.add('movePosition');
        closeIcons[i].style.display = 'block';
        closeIcons[i].classList.add('movePosition');
        isOpen[i] = false;
    } else {
        helpTexts[i].style.display = 'none';
        helpTexts[i].classList.remove('movePosition');
        closeIcons[i].style.display = 'none';
        closeIcons[i].classList.remove('movePosition');
        isOpen[i] = true;
    }
  });

    closeIcons[i].addEventListener('click', function() {
        helpTexts[i].style.display = 'none';
        helpTexts[i].classList.remove('movePosition');
        closeIcons[i].style.display = 'none';
        closeIcons[i].classList.remove('movePosition');
        isOpen[i] = true;
  });
}