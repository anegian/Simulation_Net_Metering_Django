// variables initialization
let slider = document.getElementById("myRangeSlider");
const PV_kW_output = document.getElementById("slider-value");
const select_annual_Kwh = document.getElementById("id_select_kwh");

// Get the initial value of the select_annual_Kwh element from the form
const initial_Kwh_value = select_annual_Kwh.value;
const district_average_irradiance = document.getElementById("id_select_district");

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


// Set the initial value of the PV_kW_output element to 0
slider.value = 0;
slider.step = 0.1;
PV_kW_output.innerHTML = slider.value;
slider.disabled = true;
select_annual_Kwh.disabled = true;
storage_selection.disabled = true;
storage_kW.disabled = true;
storage_kW.value = 0;

// Update the current slider value (each time you drag the slider handle)
slider.oninput = function() {
    slider.min = 1;
    PV_kW_output.innerHTML = this.value;
    error_message3.style = 'none';
};      

district_average_irradiance.addEventListener("change", function(event){

    let district_array = district_average_irradiance.textContent;

    if (district_average_irradiance.value != '0' && select_annual_Kwh.value !== '0') {
        error_message.style.display = "none";
        district_average_irradiance.classList.remove('error');

        slider.disabled = false;
        slider_value = select_annual_Kwh.value / district_average_irradiance.value;
        slider.value = slider_value;
        
        console.log("There is kwh, so average irradiance is: " + district_average_irradiance.value);
        console.log(select_annual_Kwh.value);
        console.log(slider.value);
    } else {
        console.log("average irradiance is: " + district_average_irradiance.value);
        slider.value = 0
        error_message.style.display = "none";
        district_average_irradiance.classList.remove('error');
    }

    PV_kW_output.innerHTML = slider.value;
    console.log("average irradiance is: " + district_average_irradiance.value);
})

// Listen for changes in the phase load input and store the selected option
phase_load_selected.addEventListener("change", function(event){
    console.log(slider.value);
    slider.min =0;
    select_annual_Kwh.value = initial_Kwh_value; // Set the value of the select_annual_Kwh element to the initial value
    slider.value = 0; // Update the slider value to 0 when the phase load is changed
    slider.max = event.target.value === 'single_phase' ? 5 : 10
    slider.disabled = event.target.value === 'phase_load';
    PV_kW_output.innerHTML = slider.value; // Update the PV_kW_output element value to 0 when the phase load is changed
    no_storage_selection.checked = true;
    storage_kW.disabled = true;
    console.log(slider.value);
    
    select_annual_Kwh.disabled = event.target.value === 'phase_load';
    error_message2.style.display = "none";
    phase_load_selected.classList.remove('error');
    
    if (event.target.value === 'single_phase') {
        
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
    console.log(slider.value);

    
    console.log(phase_load_selected.value);
    console.log(slider.value);
});

// Reset the PV_kW_output element value to the initial value when the reset button is clicked
document.querySelector('button[type="reset"]').addEventListener('click', function(event) {
    no_storage_selection.checked = true;
    storage_selection.disabled = true;
    slider.disabled = true;
    select_annual_Kwh.disabled = true;
    slider.value = 0;
    PV_kW_output.innerHTML = slider.value;
    district_average_irradiance.classList.remove('error');
    phase_load_selected.classList.remove('error');
    error_message.style.display = 'none';
    error_message2.style.display = 'none';
    error_message3.style.display = 'none';
});

// Add an event listener to the submit button
form_submit_button.addEventListener('click', function(event) {
  // Prevent the form from submitting and reloading the page when it's not valid
  if (!validateForm()) {
    event.preventDefault();
  }
});

select_annual_Kwh.addEventListener("change", function(event){
    console.log(slider.value);
    slider.min =0;
    slider.disabled = false;
    slider.value = 0;
    PV_kW_output.innerHTML = slider.value; // Update the PV_kW_output element value to 0 when the phase load is changed
    storage_selection.disabled = false;
    storage_kW.disabled = false;
    console.log(slider.value);
    console.log(select_annual_Kwh.value);
    

    if (select_annual_Kwh.value !== '0' && district_average_irradiance.value !== '0') {
        slider.value = select_annual_Kwh.value / district_average_irradiance.value;
        slider.disabled = false;
    } else {
        slider.value = 0;
        slider.disabled = true;

        storage_selection.disabled = true;
        storage_kW.disabled = true;
        no_storage_selection.checked = true;
    }
    console.log(slider.value);
    PV_kW_output.innerHTML = slider.value; 
    storage_kW.min = slider.value;
    storage_kW.value = slider.value;
    storage_kW.max = 10;
    console.log(slider.value);

    if(slider.addEventListener("change", function(event){
        storage_kW.value = slider.value;
        storage_kW.max = slider.value;
        console.log(storage_kW.value);
        PV_kW_output.innerHTML = slider.value; 
    }))
    
    console.log(storage_kW.value);
    console.log(slider.value);
});

// Used to validate that the calculator form has been filled by the user
function validateForm() {

    if(phase_load_selected.value === 'phase_load' && district_average_irradiance.value === "0"){
        slider.classList.add('error');
        phase_load_selected.classList.add('error');
        error_message2.style.display = 'block';
        district_average_irradiance.classList.add('error'); 
        error_message.style.display = 'block';
        return false;
    }else if(district_average_irradiance.value === "0"){
        district_average_irradiance.classList.add('error'); // Add the error class to the district_average_irradiance element
        district_average_irradiance.classList.add('error'); 
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