// variables initialization
let slider = document.getElementById("myRangeSlider");
const PV_kW_output = document.getElementById("slider-value");
// const select_annual_Kwh = document.getElementById("id_select_kwh");
let select_annual_Kwh = document.getElementById("annual_kwh");
// Get panel parameters
const panelParamsSelect = document.getElementById('panelParams');
const panelWpInput = document.getElementById('panelWpInput');
const panelEfficiencyInput = document.getElementById('panelEfficiencyInput');
const panelAreaInput = document.getElementById('panelAreaInput');
const panelCostInput = document.getElementById('panelCostInput');

const district_average_irradiance = document.getElementById("id_select_district");
// Get the initial value of the district
const initial_district = district_average_irradiance.value;

const phase_load_selected = document.getElementById("id_select_phase");
const form_submit_button = document.getElementById("submitBtn");
const reset_button = document.getElementById("resetBtn")
const error_message = document.getElementById('error-message-panel');
const error_message2 = document.getElementById('error-message-panel5');
const error_message3 = document.getElementById('error-message-panel6');
const max_message = document.getElementById("max-message")
const storage_selection = document.getElementById("with_storage");
const storage_kW = document.getElementById("storage_kw");
const no_storage_selection = document.getElementById("without_storage");
// select all radio buttons with the class "form-check-input"
const radio_buttons = document.querySelectorAll('.form-check-input');


// Set the initial values of all elements to 0
disableElements();


// Update the current slider value (each time you drag the slider handle)
slider.oninput = function() {
    slider.min = 0.1;
    PV_kW_output.innerHTML = this.value;
    error_message3.style = 'none';
};      

// Set default values for panel parameters
panelWpInput.value = panelParamsSelect.options[0].value;
panelEfficiencyInput.value = panelParamsSelect.options[0].dataset.efficiency;
panelAreaInput.value = panelParamsSelect.options[0].dataset.panel_area;
panelCostInput.value = panelParamsSelect.options[0].dataset.panel_cost;


// Parameters from panels
panelParamsSelect.addEventListener('change', function() {
    const selectedOption = panelParamsSelect.options[panelParamsSelect.selectedIndex];
    const wp = selectedOption.value;
    const efficiency = selectedOption.dataset.efficiency;
    const panel_area = selectedOption.dataset.panel_area;
    const panel_cost = selectedOption.dataset.panel_cost;
  
    panelWpInput.value = wp;
    panelEfficiencyInput.value = efficiency;
    panelAreaInput.value = panel_area;
    panelCostInput.value = panel_cost;

    console.log(panelAreaInput.value)
});


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
        disableErrorMessages();
        enableAnnualkWh();
        select_annual_Kwh.value = " "
        slider.max = event.target.value === 'single_phase' ? 5 : 10
        enableSlider();
    }else{
        disableElements();
    } 

    check_selection_kwh_conditions();
    console.log(phase_load_selected.value);
});

select_annual_Kwh.addEventListener("input", function(){
    enableSlider();
    enableStorage();
    let enteredValue = parseInt (select_annual_Kwh.value)
    const maxValue = parseInt (select_annual_Kwh.max)
    
    if (enteredValue > maxValue) {
        enteredValue = maxValue;
        select_annual_Kwh.value = enteredValue;
        max_message.style.display = "block";
    } else {
        max_message.style.display = "none";
    }

    console.log(enteredValue, select_annual_Kwh.value)
});

select_annual_Kwh.addEventListener("keypress", function(event){
    if (isNaN(event.key) || event.key === " " ){
        event.preventDefault();
    }
});

slider.addEventListener("change", function(){

    disableErrorMessages();
    PV_kW_output.innerHTML = slider.value; 
    storage_kW.min = slider.value;
    storage_kW.value = slider.value;

    console.log(slider.value);

});

storage_kW.addEventListener("change", function(){
    console.log(storage_kW.value);
});

// Reset the PV_kW_output element value to the initial value when the reset button is clicked
document.querySelector('button[type="reset"]').addEventListener('click', function() {
    disableElements();
    disableErrorMessages(); 
     
    console.log("Slider value: ", slider.value)
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
    select_annual_Kwh.disabled = true;
    slider.min = 0;
    slider.value = 0;
    PV_kW_output.innerHTML = slider.value;
    select_annual_Kwh.value = " "
    storage_selection.disabled = true;
    storage_kW.disabled = true; 
    slider.disabled = true;
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
    if (select_annual_Kwh.value === '0') {
        slider.value = 0.0;
      } else {
        slider.value = select_annual_Kwh.value / district_average_irradiance.value;
        console.log("Minimum PV system's kWp: ", slider.value);
      }
    
    PV_kW_output.innerHTML = slider.value;
}
function enableAnnualkWh(){
    select_annual_Kwh.disabled = false;
    select_annual_Kwh.max = phase_load_selected.value === 'single_phase' ? 7000 : 15000;
    select_annual_Kwh.step = 100;
    select_annual_Kwh.min = 0;
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
    max_message.style.display = 'none';
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

// Map
let map = L.map('map').setView([37.983917, 23.72936], 8);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);


// Create the popup with offset
var popup = L.popup({
    closeButton: true,
    offset: [1, -20] // Adjust the second value (-20) to move the popup higher
});
let marker;
latitude = document.getElementById('latitude')
longitude = document.getElementById('longitude')

function onMapClick(e) {
    latitude.value = e.latlng.lat.toFixed(6);
    longitude.value = e.latlng.lng.toFixed(6);
    console.log(latitude.value);
    console.log(longitude.value);

    if (marker) {
        map.removeLayer(marker); // Remove previous marker if it exists
    }

    marker = L.marker(e.latlng).addTo(map); // Add a new marker at the clicked location


    popup
        .setLatLng(e.latlng)
        .setContent(e.latlng.toString())
        .openOn(map);
}

map.on('click', onMapClick);

latitude.addEventListener('change', function(){
    latitude.value = latitude.value
})


// Settings for tilt images
const radio_tilt = document.querySelectorAll('input[name="inclination"]');
const images = document.querySelectorAll('.img-tilt');

radio_tilt.forEach(function(radio) {
  radio.addEventListener('change', function(event) {
    const selectedValue = event.target.value;

    images.forEach(function(image) {
      const tiltValue = image.getAttribute('data-tilt');
      image.style.display = tiltValue === selectedValue ? 'block' : 'none';
    });
  });

  if (radio.value === '30') {
    radio.checked = true;
    images.forEach(function(image) {
      const tiltValue = image.getAttribute('data-tilt');
      image.style.display = tiltValue === '30' ? 'block' : 'none';
    });
  }
});


// Setings for theme toggler
const themeSlider = document.getElementById('theme-slider');
set_initial_properties_theme_toggler();

function set_initial_properties_theme_toggler(){
    themeSlider.value = '0';
    document.documentElement.style.setProperty('--bg-color', '#29233b');
    document.documentElement.style.setProperty('--text-color', '#f2f2f2');
    document.documentElement.style.setProperty('--bg-color-panel', '#393052');
    document.documentElement.style.setProperty('--label-color', '#bbb');
    document.documentElement.style.setProperty('--title-panel-color', '#f2f2f2');
    document.documentElement.style.setProperty('--slider-color', '#74b1f2');
    document.documentElement.style.setProperty('--thumb-color', '#393052');
    document.documentElement.style.setProperty('--bg-color-calculator-page', '#29233b');
    document.documentElement.style.setProperty('--bg-color-submit-button', '#738725'); 
}

themeSlider.addEventListener('input', function(event) {
  const selectedValue = event.target.value;    
        
        if (selectedValue === '0') {
          document.documentElement.style.setProperty('--bg-color', '#29233b');
          document.documentElement.style.setProperty('--text-color', '#f2f2f2');
          document.documentElement.style.setProperty('--bg-color-panel', '#393052');
          document.documentElement.style.setProperty('--label-color', '#bbb');
          document.documentElement.style.setProperty('--title-panel-color', '#f2f2f2');
          document.documentElement.style.setProperty('--slider-color', '#74b1f2');
          document.documentElement.style.setProperty('--slider-value-kW-color', '#f2f2f2');
          document.documentElement.style.setProperty('--bg-color-calculator-page', '#29233b');
          document.documentElement.style.setProperty('--thumb-color', '#393052');
          document.documentElement.style.setProperty('--bg-color-submit-button', '#738725');
        } else if (selectedValue === '1') {
          document.documentElement.style.setProperty('--bg-color', '#f2f2f2');
          document.documentElement.style.setProperty('--text-color', '#333');
          document.documentElement.style.setProperty('--bg-color-panel', '#f2f2f2');
          document.documentElement.style.setProperty('--text-color-panel', '#c6ccd2'); 
          document.documentElement.style.setProperty('--label-color', '#334d68'); 
          document.documentElement.style.setProperty('--title-panel-color', '#538bc7');
          document.documentElement.style.setProperty('--slider-color', '#393052');
          document.documentElement.style.setProperty('--slider-value-kW-color', '#334d68');
          document.documentElement.style.setProperty('--bg-color-calculator-page', '#f2f2f2');
          document.documentElement.style.setProperty('--thumb-color', '#74b1f2');
          document.documentElement.style.setProperty('--bg-color-submit-button', '#74b1f2');
        }
    });

