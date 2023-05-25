// variables initialization
let slider = document.getElementById("myRangeSlider");
const PV_kW_output = document.getElementById("slider-value");
const select_annual_Kwh = document.getElementById("id_select_kwh");

// Get the initial value of the select_annual_Kwh element from the form
const initial_Kwh_value = select_annual_Kwh.value;
const district_average_irradiance = document.getElementById("id_select_district");
// Get the initial value of the district
const initial_district = district_average_irradiance.value;

const phase_load_selected = document.getElementById("id_select_phase");
const form_submit_button = document.getElementById("submitBtn");
const error_message = document.getElementById('error-message-panel');
const error_message2 = document.getElementById('error-message-panel5');
const error_message3 = document.getElementById('error-message-panel6');
const storage_selection = document.getElementById("with_storage");
const storage_kW = document.getElementById("storage_kw");
const no_storage_selection = document.getElementById("without_storage");
// select all radio buttons with the class "form-check-input"
const radio_buttons = document.querySelectorAll('.form-check-input');


// Set the initial values of all elements to 0
disableElements();


// Update the current slider value (each time you drag the slider handle)
slider.oninput = function() {
    slider.min = 1.0;
    PV_kW_output.innerHTML = this.value;
    error_message3.style = 'none';
};      

district_average_irradiance.addEventListener("change", function(event){
    if ( district_average_irradiance.value === 'district' ) {
        disableAnnualkWh();
    }else{
        error_message.style.display = "none";
        district_average_irradiance.classList.remove('error');
    }

    check_selection_kwh_conditions();
    console.log("average irradiance is: " + district_average_irradiance.value);
       
});

// Listen for changes in the phase load input and store the selected option
phase_load_selected.addEventListener("change", function(event){
    
    if (event.target.value === 'single_phase' || event.target.value === '3_phase'){
        error_message2.style.display = "none";
        phase_load_selected.classList.remove('error')
        select_annual_Kwh.value = initial_Kwh_value;  // Resetting select_annual_Kwh to initial value
        enableAnnualkWh();
        slider.max = event.target.value === 'single_phase' ? 5 : 10
        showAnnualKwh();
    }else{
        disableElements();
    } 

    check_selection_kwh_conditions();
    console.log(phase_load_selected.value);
});

select_annual_Kwh.addEventListener("change", function(event){
    if(event.target.value === 'kWh'){
        disableSlider();
        disableStorage();
        console.log(select_annual_Kwh.value)
    }else{
        console.log('Annual consumption in kWh: ', select_annual_Kwh.value);
        enableSlider();  
        enableStorage();  
    } 
});

slider.addEventListener("change", function(event){

	if (Number(slider.value) > '0' && Number(slider.value) <= '10'){
        if(storage_kW.disabled == true){
             enableStorage(); 
        }

        disableErrorMessages();
        PV_kW_output.innerHTML = slider.value; 
        storage_kW.min = slider.value;
        storage_kW.value = slider.value;
    }

    console.log(slider.value);

});

storage_kW.addEventListener("change", function(){
    console.log(storage_kW.value);
});

// Reset the PV_kW_output element value to the initial value when the reset button is clicked
document.querySelector('button[type="reset"]').addEventListener('click', function() {
    disableElements();
    disableErrorMessages();  
});

// Add an event listener to the submit button
form_submit_button.addEventListener('click', function(event) {
  // Prevent the form from submitting and reloading the page when it's not valid
  if (!validateForm()) {
    event.preventDefault();
  }
});

// Used to validate that the calculator form has been filled by the user
function validateForm() {

    if(phase_load_selected.value === 'phase_load' && district_average_irradiance.value === "district"){
        slider.classList.add('error');
        phase_load_selected.classList.add('error');
        error_message2.style.display = 'block';
        district_average_irradiance.classList.add('error'); 
        error_message.style.display = 'block';
        return false;
    }else if(district_average_irradiance.value === "district"){
        district_average_irradiance.classList.add('error'); // Add the error class to the district_average_irradiance element
        error_message.style.display = 'block';
        return false;
    }else if (phase_load_selected.value === 'phase_load') {
        phase_load_selected.classList.add('error');
        error_message2.style.display = 'block';
        return false; // return false to indicate that the form was not submitted
    }else if (slider.value === '0') {
        slider.classList.add('error'); // Add the error class to the slider element
        error_message3.style.display = 'block';
        return false; // return false to indicate that the form was not submitted
    }
    return true;
};

// loop through the radio buttons and add an event listener to each one
radio_buttons.forEach(radioButton => {
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

function disableElements() {
    slider.disabled = true;
    slider.value = 0.0;
    slider.min = 0.0;
    PV_kW_output.innerHTML = slider.value;
    storage_selection.disabled = true;
    storage_kW.disabled = true;
    select_annual_Kwh.disabled = true;
    select_annual_Kwh.value = initial_Kwh_value;  // Resetting select_annual_Kwh to initial value
} 
function enableSlider() {
    slider.disabled = false;
    slider.min = 0.0;
    slider.step = 0.1;
    slider.value = select_annual_Kwh.value / district_average_irradiance.value;
    PV_kW_output.innerHTML = slider.value;
    console.log("Minimun PV system's kWp: ", slider.value)
}
function disableSlider(){
    slider.disabled = true;
    slider.value = 0.0;
    slider.min = 0.0;
    if (select_annual_Kwh.value === 'kWh') {
        slider.value = 0.0;
      } else {
        slider.value = select_annual_Kwh.value / district_average_irradiance.value;
        console.log("Minimum PV system's kWp: ", slider.value);
      }
    
    PV_kW_output.innerHTML = slider.value;
}
function enableAnnualkWh(){
    select_annual_Kwh.disabled = false;
}
function disableAnnualkWh() {
    select_annual_Kwh.disabled = true;
}
function enableStorage() {
    no_storage_selection.checked = true;
    storage_selection.disabled = false;
    storage_kW.disabled = false;
    storage_kW.min = slider.value;
    storage_kW.max = 10.0;
    storage_kW.step = 0.1;
    storage_kW.value = slider.value;
}
function disableStorage() {
    no_storage_selection.checked = true;
    storage_kW.disabled = true;
    storage_selection.disabled = true;
    storage_kW.min = slider.value;
    storage_kW.value = 0.0;
    storage_kW.value = slider.value;
}
function disableErrorMessages() {
    district_average_irradiance.classList.remove('error');
    phase_load_selected.classList.remove('error');
    error_message.style.display = 'none';
    error_message2.style.display = 'none';
    error_message3.style.display = 'none';
}         
function showAnnualKwh() { 
    if (phase_load_selected.value === 'single_phase') {
        // Enable the first two options and disable the rest
        select_annual_Kwh.options[0].disabled = false;
        select_annual_Kwh.options[1].disabled = false;
        for (let i = 3; i < select_annual_Kwh.options.length; i++) {
            select_annual_Kwh.options[i].disabled = true;
        }
    } else {
        // Enable all options
        for (let i = 0; i < select_annual_Kwh.options.length; i++) {
            select_annual_Kwh.options[i].disabled = false;
                }
    }
}
function check_selection_kwh_conditions(){
    if (phase_load_selected.value !== 'phase_load' && district_average_irradiance.value !== 'district'){
        enableAnnualkWh();
        disableErrorMessages();
    }else{ 
        disableAnnualkWh();
        disableElements();
        disableStorage();
    }
}