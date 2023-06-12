// variables initialization
let slider = document.getElementById("myRangeSlider");
const PV_kW_output = document.getElementById("slider-value");
// const annual_Kwh_input = document.getElementById("id_select_kwh");
let annual_Kwh_input = document.getElementById("annual_kwh");
// Get panel parameters
const placeSelected = document.getElementById('regionInput');
const latitudeInput = document.getElementById('latitude');
const longitudeInput = document.getElementById('longitude');
const panelParamsSelect = document.getElementById('panelParams');
const panelWpInput = document.getElementById('panelWpInput');
const panelEfficiencyInput = document.getElementById('panelEfficiencyInput');
const panelAreaInput = document.getElementById('panelAreaInput');
const panelCostInput = document.getElementById('panelCostInput');
const form = document.getElementById("calculatorForm");

// const district_average_irradiance = document.getElementById("id_select_district");
// Get the initial value of the district
// const initial_district = district_average_irradiance.value;

const phase_load_selected = document.getElementById("id_select_phase");
const form_submit_button = document.getElementById("submitBtn");
const reset_button = document.getElementById("resetBtn")
const lastPanelField = document.getElementById('lastPanelField');
const error_message = document.getElementById('error-message-panel');
const error_message2 = document.getElementById('error-message-panel5');
const error_message3 = document.getElementById('error-message-panel6');
const max_message = document.getElementById("max-message")
const storage_selection = document.getElementById("with_storage");
const storage_kW = document.getElementById("storage_kw");
const no_storage_selection = document.getElementById("without_storage");
// select all radio buttons with the class "form-check-input"
const radio_buttons = document.querySelectorAll('.form-check-input');

const manualPowerRadio = document.getElementById('manual_power');
const autoPowerRadio = document.getElementById('auto_power');
const autoPowerDiv = document.getElementById('autoPower-button-input');
const autoPowerButton = document.getElementById('calculateProductionButton');

// Get references to the radio inputs and the azimuthInput
const radioAzimuthInputs = document.querySelectorAll('input[name="azimuth"]');
const azimuthInput = document.getElementById('azimuthInput');
const radioTiltInputs = document.querySelectorAll('input[name="inclination"]');
const tiltInput = document.getElementById('tiltInput');
const special_production_output = document.getElementById('placeProduction');
const minimum_panels = document.getElementById('minimumPanels');
const total_PV_area = document.getElementById('totalArea');

const panels = document.getElementsByClassName("panel-calculator");
const previousButton = document.getElementById("previous-button");
const nextButton = document.getElementById("next-button");

// Settings for tilt images
const images = document.querySelectorAll('.img-tilt');

// Set the initial values of all elements to 0
disableElements();
nextButton.disabled = true;
console.log(placeSelected.value);


// Function to simulate a change event on the input field
function triggerButtonEnable() {
    nextButton.disabled = false;
    console.log("In trigger function:", placeSelected.value)
    console.log(nextButton.disabled);
    nextButton.classList.add('enabled-button') 
}


function triggerButtonDisable() {
nextButton.disabled = true;
nextButton.classList.remove ('enabled-button');
console.log("In trigger function:", placeSelected.value);
console.log(nextButton.disabled);
}


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


// Add event listener to each radio Azimuth input
radioAzimuthInputs.forEach(function(input) {
  input.addEventListener('change', function() {
    // Set the value of azimuthInput to the selected radio input's value
    azimuthInput.value = this.value;
    });
});

// Add event listener to each radio Tilt input
radioTiltInputs.forEach(function(inputs) {
    inputs.addEventListener('change', function(e) {
      // Set the value of tiltInput to the selected radio input's value
      tiltInput.value = this.value;

        images.forEach(function(image) {
            const tiltValue = image.getAttribute('tilt');
            image.style.display = tiltValue ===  tiltInput.value ? 'block' : 'none';
        });
    });
});

// Show the image corresponding to 30 degrees when the page starts or reloads
document.addEventListener('DOMContentLoaded', function() {
    tiltInput.value = '30'; // Set the value of tiltInput to 30
    autoPowerDiv.classList.add('hidden');
    azimuthInput.value = 0;
    
    images.forEach(function(image) {
      const tiltValue = image.getAttribute('tilt');
      image.style.display = tiltValue === '30' ? 'block' : 'none';
    });
    
    let currentPanelIndex = 0;


    
    function showPanel(index) {
        for (let i = 0; i < panels.length; i++) {
          if (i === index) {
            panels[i].classList.remove("hidden");
          } else {
            panels[i].classList.add("hidden");
          }
        }
    }


    function goToPreviousPanel() {
      if (currentPanelIndex > 0) {
        currentPanelIndex--;
        showPanel(currentPanelIndex);
      }
    }

    function goToNextPanel() {
      if (currentPanelIndex < panels.length - 1) {
        currentPanelIndex++;
        showPanel(currentPanelIndex);
      }
    }

    showPanel(currentPanelIndex);

    previousButton.addEventListener("click", goToPreviousPanel);
    nextButton.addEventListener("click", goToNextPanel);

});

// Listen for changes in the phase load input and store the selected option
phase_load_selected.addEventListener("change", function(event){
    

    if (event.target.value === 'single_phase' || event.target.value === '3_phase'){
        disableErrorMessages();
        enableAnnualkWh();
        annual_Kwh_input.value = " "
        slider.max = event.target.value === 'single_phase' ? 5 : 10
        enableSlider();
    }else{
        disableElements();
    } 

    check_selection_kwh_conditions();
    console.log(phase_load_selected.value);
});

annual_Kwh_input.addEventListener("input", function(){
    enableSlider();
    enableStorage();
    let enteredValue = parseInt (annual_Kwh_input.value)
    const maxValue = parseInt (annual_Kwh_input.max)
    
    if (enteredValue > maxValue) {
        enteredValue = maxValue;
        annual_Kwh_input.value = enteredValue;
        max_message.style.display = "block";
    } else {
        max_message.style.display = "none";
    }

    console.log(enteredValue, annual_Kwh_input.value)
});

annual_Kwh_input.addEventListener("keypress", function(event){
    if (isNaN(event.key) || event.key === " " ){
        event.preventDefault();
    }
});

annual_Kwh_input.addEventListener("change", function(event){
    if (event.value === 0 || event.value === "" ){
        disableSlider();
        nextButton.disabled = true;
    }else{
        enableSlider();
        nextButton.disabled = false;
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
reset_button.addEventListener('click', function() {
    disableElements();
    disableErrorMessages(); 
    azimuthInput.value = 0;
});

// Add an event listener to the submit button
form_submit_button.addEventListener('click', function(event) {
    
    // Validate the form inputs
    if (!validateForm()) {
      // Submit the form programmatically
      event.preventDefault();
    }else{
        form.submit();
    }
});

// Used to validate that the calculator form has been filled by the user
function validateForm() {

    if(phase_load_selected.value === 'phase_load' ){ //&& district_average_irradiance.value === "district"){
        slider.classList.add('error');
        phase_load_selected.classList.add('error');
        error_message2.style.display = 'block';
        // district_average_irradiance.classList.add('error'); 
        error_message.style.display = 'block';
        return false;
    }else if (placeSelected.value === '' || latitudeInput.value === '' || longitudeInput.value === '') {
        alert("Επιλέξτε μία τοποθεσία στο χάρτη");
        return false;
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
    annual_Kwh_input.disabled = true;
    slider.min = 0;
    slider.value = 0;
    PV_kW_output.innerHTML = slider.value;
    annual_Kwh_input.value = ""
    storage_selection.disabled = true;
    storage_kW.disabled = true; 
    slider.disabled = true;
    manualPowerRadio.disabled = true;
    autoPowerRadio.disabled = true;
    azimuthInput.value = '0';
    form_submit_button.classList.add('hidden');
} 
function enableSlider() {
    slider.disabled = false;
    slider.min = 0.0;
    slider.step = 0.1;
    PV_kW_output.innerHTML = slider.value;
    manualPowerRadio.disabled = false;
    autoPowerRadio.disabled = false;
    console.log("Minimun PV system's kWp: ", slider.value)
}
function disableSlider(){
    slider.disabled = true;
    slider.value = 0.0;
    slider.min = 0.0;
    if (annual_Kwh_input.value === '0') {
        slider.value = 0.0;
      } else {
        console.log("Minimum PV system's kWp: ", slider.value);
      }
    
    manualPowerRadio.disabled = true;
    autoPowerRadio.disabled = true;
    PV_kW_output.innerHTML = slider.value;
}
function enableAnnualkWh(){
    annual_Kwh_input.disabled = false;
    annual_Kwh_input.max = phase_load_selected.value === 'single_phase' ? 7000 : 15000;
    annual_Kwh_input.step = 10;
    annual_Kwh_input.min = 0;
}
function disableAnnualkWh() {
    annual_Kwh_input.disabled = true;
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
    //district_average_irradiance.classList.remove('error');
    phase_load_selected.classList.remove('error');
    error_message.style.display = 'none';
    error_message2.style.display = 'none';
    error_message3.style.display = 'none';
    max_message.style.display = 'none';
}         

function check_selection_kwh_conditions(){
    if (phase_load_selected.value !== 'phase_load' && placeSelected.value !== ""){
        enableAnnualkWh();
        disableErrorMessages();
    }else{ 
        disableAnnualkWh();
        disableElements();
        disableStorage();
    }
}


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


// Add event listeners to the radio buttons and the calculation button
manualPowerRadio.addEventListener('change', toggleAutoPowerDiv);
autoPowerRadio.addEventListener('change', toggleAutoPowerDiv);


// Function to toggle the visibility of the div based on the selected radio button
function toggleAutoPowerDiv() {
  if (manualPowerRadio.checked) {
    autoPowerDiv.style.display = 'none'; // Hide the div
  } else if (autoPowerRadio.checked) {
    autoPowerDiv.classList.remove('hidden');
    autoPowerDiv.style.display = 'block'; // Show the div
  }
}


function calculateAutoPower(event) {
  event.preventDefault(); // Prevent the default form submission behavior

  // Get the latitude, longitude, azimuth, and tilt values from the form
  const latitudeValue = latitudeInput.value;
  const longitudeValue = longitudeInput.value;
  const azimuthValue = azimuthInput.value;
  const tiltValue = tiltInput.value;
  const panelWpValue = panelWpInput.value
  const panelAreaValue = panelAreaInput.value;
  const panelEfficiencyValue = panelEfficiencyInput.value
  const annualKWhValue = annual_Kwh_input.value
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  const url = '/simulation/ajax/' ;  // Make sure this matches the URL pattern in your Django project's URLs

  if (!annualKWhValue){
    alert('Πρώτα πρέπει να επιλέξετε ετήσια κατανάλωση σε kWh στο προηγούμενο βήμα');
  }
    // Create the data object
    let data = {
        latitude: latitudeValue,
        longitude: longitudeValue,
        inclination: tiltValue,
        azimuth: azimuthValue,
        panel_area: panelAreaValue,
        panel_efficiency: panelEfficiencyValue,
        annual_Kwh_value: annualKWhValue,
        panel_Wp_value: panelWpValue,
    };

    console.log(data);

  const jsonData = JSON.stringify(data);

  // Make the AJAX request
  $.ajax({
    url: url,
    type: 'POST',
    data: jsonData,
    contentType: 'application/json', // Set the request content type to JSON
    dataType: 'json', // Expect JSON response from the server
    headers: {
      'X-CSRFToken': csrfToken // Include the CSRF token in the request headers
    },
    success: function(response) {
      // Handle the response
      const specialProduction = response.special_production;
      const recommended_kWp = response.recommended_kWp;
      const minimum_panels = response.minimum_PV_panels;
      const totalArea = response.total_area;
      
      console.log(specialProduction);

      // Update the input field with the calculated power
      $('#placeProduction').val(specialProduction);
      slider.value = recommended_kWp;
      PV_kW_output.innerHTML = slider.value;
      storage_kW.min = slider.value;
      storage_kW.value = slider.value;
      $('#minimumPanels').val(minimum_panels);
      $('#totalArea').val(totalArea);
      

    },
    error: function(xhr, textStatus, errorThrown) {
      console.log('Error:', errorThrown);
    }
  });
    console.log("test");

  var i = 0;

  if (i == 0) {
  i = 1;
  var loadingBar = document.getElementById('loading-bar');
  var width = 10;
  var id = setInterval(frame, 10);
  function frame() {
    if (width >= 100) {
      clearInterval(id);
      i = 0;
    } else {
      width++;
      loadingBar.style.width = width + "%";
      loadingBar.innerHTML = width + "%";
    }
  }
  }

  
}

autoPowerButton.addEventListener('click', calculateAutoPower);

