// variables initialization
const themeSlider = document.getElementById('theme-slider');
const slider = document.getElementById("myRangeSlider");
const slider_hidden_input = document.getElementById("myRangeSliderHidden");
const PV_kW_output = document.getElementById("slider-value");
// const annual_Kwh_input = document.getElementById("id_select_kwh");
let annual_Kwh_input = document.getElementById("annual_kwh");
// Get panel parameters
const placeSelected = document.getElementById('regionInput');
const latitudeInput = document.getElementById('latitude');
const longitudeInput = document.getElementById('longitude');
const panelParamsSelect = document.getElementById('panelParams');
const defaultPanelParams = document.getElementById('defaultPanelParams');
const panelWpInput = document.getElementById('panelWpInput');
const panelEfficiencyInput = document.getElementById('panelEfficiencyInput');
const panelAreaInput = document.getElementById('panelAreaInput');
const panelCostInput = document.getElementById('panelCostInput');
const form = document.getElementById("calculatorForm");
const placeInstalmentRadios  = document.getElementsByName('installation')
let selectedPlaceInstalmentValue;
const roofRadioButton = document.getElementById('roof');

const phase_load_selected = document.getElementById("id_select_phase");
const phaseLoadDefaultSelection = document.getElementById("phase_load");
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
const azimuthDefaultRadio = document.getElementById("south");
const radioTiltInputs = document.querySelectorAll('input[name="inclination"]');
const tiltInput = document.getElementById('tiltInput');
const tiltDefaultRadio = document.getElementById('inclination30');
const profileDefaultRadio = document.getElementById('day-power');
const special_production_output = document.getElementById('placeProduction');
const minimum_panel_container = document.getElementById('minimumPanels');
const total_PV_area = document.getElementById('totalArea');

const panelContainers = document.getElementsByClassName("panel-calculator");
const previousButton = document.getElementById("previous-button");
const nextButton = document.getElementById("next-button");
const circleLinks = document.querySelectorAll('.circle-link');
let currentPanelIndex = 0;
let submitBtnEnabled;

//Modal fields
const form_submit_button = document.getElementById("submitBtn");
const submit_modal = document.getElementById("submit_modal");
const place_modal_input = document.getElementById("place_modal_value");
const azimuth_modal_input = document.getElementById("azimuth_modal_value");
const tilt_modal_input = document.getElementById("tilt_modal_value");
const annual_Kwh_modal_input = document.getElementById("annual_Kwh_modal_value");
const profile_modal_input = document.getElementById("profile_modal_value");
const power_modal_input = document.getElementById("power_modal_value");
const panel_modal_number_input = document.getElementById("panel_modal_number");
const battery_modal_input = document.getElementById("battery_modal_value");
const discount_percent_modal_input = document.getElementById("discount_percent_modal_value");
const discount_percent = document.getElementById("discount_percent");
const discount_percent_battery_modal_input = document.getElementById("discount_percent_battery_modal_value");
const discount_percent_battery = document.getElementById("discount_percent_battery");
// Get references to the discount_percent and discount battery select elements
const discountPercentSelect = document.querySelector('.discount_percent_select');
const discountPercentBatterySelect = document.querySelector('.discount_percent_battery_select');
let autoCalculatedPower;
let autoCalculatedPowerNumber = 0;
const noDiscountRadio = document.getElementById('no-discount');
const discountRadio = document.getElementById('discount');

var loadingBar = document.getElementById('loading-bar');
var containerWidth = loadingBar.parentElement.offsetWidth; // Get the width of the container element
var width = 0;
var id = null;

// Help Poppers to give details about the form fields or selected values
const helpButtons = document.getElementsByClassName('help-popper');
const helpTexts = document.getElementsByClassName('help-text');
const closeIcons = document.getElementsByClassName('close-help');
const numberOfHelpButtons = helpButtons.length;

// Set default values for panel parameters
panelWpInput.value = panelParamsSelect.options[0].value;
panelEfficiencyInput.value = panelParamsSelect.options[0].dataset.efficiency;
panelAreaInput.value = panelParamsSelect.options[0].dataset.panel_area;
panelCostInput.value = panelParamsSelect.options[0].dataset.panel_cost;

// Settings for tilt images
const images = document.querySelectorAll('.img-tilt');

// FUNCTIONS
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
function setStorage(value) {
  storage_kW.min = value;
  storage_kW.value = value;
}
function enablePanelButton(button){
  button.disabled = false;
  button.classList.add('enabled-button');
}
function disablePanelButton(button){
  button.disabled = true;
  button.classList.remove('enabled-button');
}
function enableSlider() {
  slider.disabled = false;
  slider.min = 0.0;
  slider.step = 0.1;
  PV_kW_output.innerHTML = slider.value;
  manualPowerRadio.disabled = false;
  autoPowerRadio.disabled = false;
  slider.classList.remove("disabled-slider");
  console.log("(function enableSlider) Minimun PV system's kWp: ", slider.value)
}
function disableSlider(){
  slider.disabled = true;
  slider.value = 0.0;
  slider.min = 0.0;
  slider_hidden_input.value = 0;
  if (annual_Kwh_input.value === '0' || annual_Kwh_input.value.trim() === "" ) {
      manualPowerRadio.disabled = true;
      autoPowerRadio.disabled = true;
  } 
  PV_kW_output.innerHTML = slider.value;
  slider.classList.add("disabled-slider");
}
function disableElements() {
  disableSlider();
  placeSelected.value = "";
  latitudeInput.value = "";
  longitudeInput.value = "" ; 
  disablePanelButton(nextButton);
  disablePanelButton(previousButton);
  disablePanelButton(form_submit_button);
  submitBtnEnabled = false;
  roofRadioButton.checked = true;
  defaultPanelParams.selected  = true;
  tiltDefaultRadio.checked = true;
  tiltInput.value = '30'; // Set the value of tiltInput to 30
  azimuthDefaultRadio.checked = true;
  azimuthInput.value = 0;
  phase_load_selected.value = "phase_load";// Set the default phase value 
  annual_Kwh_input.disabled = true;
  annual_Kwh_input.value = ""
  profileDefaultRadio.checked = true;
  storage_selection.disabled = true;
  storage_kW.disabled = true; 
  manualPowerRadio.disabled = true;
  manualPowerRadio.checked = true;
  autoPowerRadio.disabled = true;
  autoPowerDiv.classList.add('hidden');
  autoPowerDiv.style.display = 'none';
  autoCalculatedPower = false;
  special_production_output.value = "";
  minimum_panel_container.value = "";
  total_PV_area.value = "";
  // Discounts 
  discount_percent.max = 100;
  discount_percent.min = 0;
  discount_percent_battery.max = 100;
  discount_percent_battery.min = '0';
  selectedPlaceInstalmentValue = 'roof';
  noDiscountRadio.checked = true;
  discountPercentContainer.style.display = 'none';
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
  storage_kW.max = 10.8;
  storage_kW.step = 0.1;
  storage_kW.value = slider.value;   
}
function disableStorage() {
  no_storage_selection.checked = true;
  storage_kW.disabled = true;
  storage_selection.disabled = true;
  storage_kW.min = slider.value;
  storage_kW.value = 0.0;
}
function disableErrorMessages() {
  //district_average_irradiance.classList.remove('error');
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
  document.documentElement.style.setProperty('--help-popper', 'f2f2f2');
}
// Function to toggle the visibility of the power calculate div
function toggleAutoPowerDiv() {
  if (manualPowerRadio.checked) {
    autoPowerDiv.classList.add('hidden');
    autoPowerDiv.style.display = 'none'; // Hide the div
    enableSlider();
    setStorage(slider.value);
  } else if (autoPowerRadio.checked) {
    autoPowerDiv.classList.remove('hidden');
    autoPowerDiv.style.display = 'block'; // Show the div
    console.log("in toggle Auto Power: ", autoCalculatedPowerNumber);
    console.log("Auto calculated?", autoCalculatedPower);
    slider.disabled = true;
    if (autoCalculatedPower === true){
      slider.value = autoCalculatedPowerNumber;
      slider_hidden_input.value = autoCalculatedPowerNumber;
      PV_kW_output.innerHTML = autoCalculatedPowerNumber;
      setStorage(slider_hidden_input.value);
      enablePanelButton(nextButton);
    }else{
      disableSlider();
      slider_hidden_input.value = 0;
      setStorage(slider_hidden_input.value);
    }
  }
}
function calculateAutoPower() {
  // event.preventDefault(); // Prevent the default form submission behavior

  // Get the latitude, longitude, azimuth, and tilt values from the form
  const latitudeValue = latitudeInput.value;
  const longitudeValue = longitudeInput.value;
  const azimuthValue = azimuthInput.value;
  const tiltValue = tiltInput.value;
  const panelWpValue = panelWpInput.value
  const panelAreaValue = panelAreaInput.value;
  const panelEfficiencyValue = panelEfficiencyInput.value
  const annualKWhValue = annual_Kwh_input.value
  const placeInstalmentValue = selectedPlaceInstalmentValue
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
        place_instalment_value: placeInstalmentValue,
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
      const minimum_PV_panels = response.minimum_PV_panels;
      const totalArea = response.total_area;
      
      // Update the input field with the calculated power
      $('#placeProduction').val(specialProduction);
      slider.value = recommended_kWp;
      slider_hidden_input.value = Number(recommended_kWp.toFixed(1));
      PV_kW_output.innerHTML = slider.value;
      storage_kW.min = slider.value;
      storage_kW.value = slider.value;
      autoCalculatedPower = true;
      autoCalculatedPowerNumber = Number(recommended_kWp.toFixed(1));
      $('#minimumPanels').val(minimum_PV_panels);
      $('#totalArea').val(totalArea);

      enablePanelButton(nextButton);
      

    },
    error: function(xhr, textStatus, errorThrown) {
      console.log('Error:', errorThrown);
    }
  });
}
function frame() {
  if (width >= 100) {
    clearInterval(id);
    id = null; // Reset the interval ID
    width = 0; // Reset the width to 0
  } else {
    width++;
    var newWidth = (width / 100) * containerWidth; // Calculate the new width based on the container width
    loadingBar.style.width = newWidth + "px"; // Set the width in pixels
    loadingBar.innerHTML = width + "%";
  }
}
function startLoading() {
  if (id === null) { // Check if animation is not already running
    width = 0; // Reset the width to 0
    loadingBar.style.width = '0'; // Reset the width style to 0
    id = setInterval(frame, 20); // Adjust the interval duration for slower animation
  }
}
// Function to update select options dynamically
function updateDiscountSelectOptions(selectElement, options) {
  // Clear existing options
  selectElement.innerHTML = '';

  // Add the default option
  const defaultDiscountOption = document.createElement('option');
  defaultDiscountOption.textContent = 'Επιλέξτε ποσοστό';
  defaultDiscountOption.selected = true; // Set the default option as selected
  defaultDiscountOption.disabled = true; // Disable the default option
  defaultDiscountOption.value = 0;
  selectElement.appendChild(defaultDiscountOption);

  // Add the new options
  options.forEach((option) => {
    const newOption = document.createElement('option');
    newOption.value = option;
    newOption.textContent = option + '%';
    selectElement.appendChild(newOption);
  });
}
// function to show/hide the discount inputs
function showDiscountInputs() {
    if (discountRadio.checked) {
      discountPercentContainer.style.display = 'block';
    } else {
      discountPercentContainer.style.display = 'none';
      discount_percent.value = 0;
      discount_percent_battery.value = 0;
    }
}
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

// Function about Next, Previous buttons and how to show the panels of the form
function toggleNextButtonState() {
    if (annual_Kwh_input.value.trim() === '' || annual_Kwh_input.value === 0 || slider.value === '0') {
      // If the kWh field is empty or contains only spaces, disable the "Next" button
      disablePanelButton(nextButton);
    } else {
      // If the kWh field has a value, enable the "Next" button
      enablePanelButton(nextButton);
    }
}
function showPanel(index) {
    for (let i = 0; i < panelContainers.length; i++) {
      if (i === index) {
        panelContainers[i].classList.remove("hidden");
      } else {
        panelContainers[i].classList.add("hidden");
      }
    }

    if (index === 3 || index === 4 ){
      toggleNextButtonState();
    }
    if (index === 4 && autoPowerRadio.checked && autoCalculatedPower === false){
      disableSlider();
    }else if (autoPowerRadio.checked){
      slider.disabled = true;
    }
}
function goToPreviousPanel() {
  if (currentPanelIndex > 0) {
    const previousPanelIndex = currentPanelIndex - 1; // Calculate the previous panel index
    showPanel(previousPanelIndex);

    // Update navigation active class based on panel change
    const currentPanelLink = document.querySelector('.panel-field[href="#' + panelContainers[currentPanelIndex].getAttribute('id') + '"]');
    if (currentPanelLink) {
      currentPanelLink.classList.remove('active');
    }

    const previousId = panelContainers[previousPanelIndex].getAttribute('id');
    const previousPanelLink = document.querySelector('.panel-field[href="#' + previousId + '"]');
    // Update circle links active class based on panel change
    circleLinks[currentPanelIndex].classList.remove('active');

    console.log('Current Panel Index:', currentPanelIndex);
    console.log('Number of Panels:', panelContainers.length);

    if (previousPanelLink) {
      previousPanelLink.classList.add('active');
    } else {
      console.error('Previous Panel Link not found:', previousId);
    }

    // Update currentPanelIndex only if it's not the first panel
    currentPanelIndex = previousPanelIndex;

    // Always enable the Next button when moving to the previous panel
    enablePanelButton(nextButton);
  }

  // Check if it's the first panel and disable the Previous button
  if (currentPanelIndex === 0) {
    disablePanelButton(previousButton);

    // Disable the form_submit_button when moving to a previous panel
    if (submitBtnEnabled) {
      submitBtnEnabled = false;
      disablePanelButton(form_submit_button);
    }
  }
  console.log('Next Button Disabled:', nextButton.disabled);
  console.log('Previous Button Disabled:', previousButton.disabled);
}
function goToNextPanel() {
  
  if (currentPanelIndex < panelContainers.length - 1) {
    currentPanelIndex++; // Update currentPanelIndex
    showPanel(currentPanelIndex);

    // Update circle links active class based on panel change
    circleLinks[currentPanelIndex].classList.add('active');

    const nextPanelId = panelContainers[currentPanelIndex].getAttribute('id');
    const nextPanelLink = document.querySelector('.panel-field[href="#' + nextPanelId + '"]');
    
    console.log('Current Panel Index:', currentPanelIndex+1);

    if (nextPanelLink) {
      nextPanelLink.classList.add('active');
    } else {
      console.error('Next Panel Link not found:', nextPanelId);
    }

  }
  // Check if it's the last panel and disable the Next button
  if (currentPanelIndex === panelContainers.length - 1) {
    disablePanelButton(nextButton);

    // Enable the form_submit_button in the last panel
    if (!submitBtnEnabled) {
      submitBtnEnabled = true;
      enablePanelButton(form_submit_button);
    }
  }
  // Always enable the Previous button when moving to the next panel
  enablePanelButton(previousButton);

  console.log('Next Button Disabled:', nextButton.disabled);
  console.log('Previous Button Disabled:', previousButton.disabled);
}
// Function to handle the reset button
function resetForm(){
  disableElements();
  disableStorage();
  // Show the first panel and scroll to it
  currentPanelIndex = 0; // Reset to the first panel index
  showPanel(currentPanelIndex);
};

// Set the initial values of all elements to 0
disableElements();
nextButton.disabled = true;
// Settings for theme toggler
set_initial_properties_theme_toggler();
showPanel(currentPanelIndex);


// Update the current slider value (each time you drag the slider handle)
slider.oninput = function() {
    slider.min = 0.0;
    PV_kW_output.innerHTML = this.value;
    error_message3.style = 'none';
};      
// Parameters from panelContainers
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
placeInstalmentRadios.forEach(function(input) {
  input.addEventListener('change', function() {
    // Set the value of azimuthInput to the selected radio input's value
    selectedPlaceInstalmentValue = this.value;

    });
});
// loop through the radio buttons and add an event listener to each one
radio_buttons.forEach(radioButton => {
    radioButton.addEventListener('click', () => {
    // log the value of the selected radio button
    console.log("Selected radio field is: " + radioButton.value);
    });
});

// Show the image corresponding to 30 degrees when the page starts or reloads
// Go to next and previous panel calculator
document.addEventListener('DOMContentLoaded', function() {
    // Set the "roof" radio button as default checked
    roofRadioButton.checked = true;
    azimuthDefaultRadio.checked = true;
    tiltDefaultRadio.checked = true;
    tiltInput.value = '30'; // Set the value of tiltInput to 30
    phaseLoadDefaultSelection.value = "phase_load"; // Set the default value here
    autoPowerDiv.classList.add('hidden');
    azimuthInput.value = 0;
    annual_Kwh_input.value = "";
    previousButton.disabled = true;
    form_submit_button.disabled = true;
    submitBtnEnabled = false; // A flag to track the state of the submit button

    console.log('Next Button Disabled:', nextButton.disabled);
    console.log('Previous Button Disabled:', previousButton.disabled);
    
    images.forEach(function(image) {
      const tiltValue = image.getAttribute('tilt');
      image.style.display = tiltValue === '30' ? 'block' : 'none';
    });

    previousButton.addEventListener("click", goToPreviousPanel);
    nextButton.addEventListener("click", goToNextPanel);
});
// Listen for changes in the phase load input and store the selected option
phase_load_selected.addEventListener("change", function(event){
  const phaseLoadValue = this.value; // Get the selected value

  // Define the discount percent options based on the phase_load value
  const discountPercentOptions = (phaseLoadValue === '3_phase')
    ? [0, 20, 25, 60]
    : [0, 30, 35, 65];

  const discountPercentBatteryOptions = (phaseLoadValue === '3_phase')
    ? [0, 90, 100]
    : [0, 90, 100];

  // Update the discount select options
  updateDiscountSelectOptions(discountPercentSelect, discountPercentOptions);
  // Update the discount battery select options
  updateDiscountSelectOptions(discountPercentBatterySelect, discountPercentBatteryOptions);

  
  if (event.target.value === 'single_phase' || event.target.value === '3_phase'){
      disableErrorMessages();
      enableAnnualkWh();
      annual_Kwh_input.value = "";
      slider.max = event.target.value === 'single_phase' ? 5 : 10.8;
      enableSlider();
  }else{
      disableElements();
  } 
discountPercentSelect
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

    if (annual_Kwh_input.value <= 100 || annual_Kwh_input.value.trim() === ""){
      disablePanelButton(nextButton);
    }else{
      enablePanelButton(nextButton);
    }
});
annual_Kwh_input.addEventListener("change", function(){
  autoCalculatedPower = false;
});
slider.addEventListener("change", function(){
    disableErrorMessages();
    PV_kW_output.innerHTML = slider.value; 
    slider_hidden_input.value = slider.value;
    setStorage(slider.value)
    console.log(slider.value);
    if (PV_kW_output.innerHTML === '0'){
      disablePanelButton(nextButton);
    }else{
      enablePanelButton(nextButton);
    }
});
slider_hidden_input.addEventListener("change", setStorage(slider_hidden_input.value));

storage_kW.addEventListener("change", function(){
    console.log(storage_kW.value);
});

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
        document.documentElement.style.setProperty('--help-popper', 'f2f2f2');
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
        document.documentElement.style.setProperty('--help-popper', 'blue');
        }
    });
// Add event listeners to the radio buttons and the calculation button
manualPowerRadio.addEventListener('change', toggleAutoPowerDiv);
autoPowerRadio.addEventListener('change', toggleAutoPowerDiv);
autoPowerButton.addEventListener('click', calculateAutoPower);
// Discount percents
noDiscountRadio.addEventListener('change', showDiscountInputs);
discountRadio.addEventListener('change', showDiscountInputs);
//Submit, reset, Modal events
form_submit_button.addEventListener('click', function(event){

  if (annual_Kwh_input.value == ""){
    alert('Για να υποβάλετε, πρώτα πρέπει να επιλέξετε ετήσια κατανάλωση σε kWh');
    event.preventDefault(); // Prevent the default form submission
  } else {
    console.log("Event listener triggered!"); // Check if the event listener is running
    place_modal_input.value = placeSelected.value;
    azimuth_modal_input.value = azimuthInput.value;
    tilt_modal_input.value = tiltInput.value;
    annual_Kwh_modal_input.value = annual_Kwh_input.value;

    // Get the selected radio button's value
    const powerRadioButton = document.querySelector('input[name="power_option"]:checked');
    const storageRadioButton = document.querySelector('input[name="storage"][value="with_storage"]:checked');


    if (powerRadioButton) {
      // Set the value of the target input field to the selected radio button's value
      profile_modal_input.value = powerRadioButton.value;
    }
    slider_hidden_input.value = slider.value;
    power_modal_input.value = slider_hidden_input.value;

    if (storageRadioButton){
      battery_modal_input.value = storage_kW.value;
    }else{
      battery_modal_input.value = 0;
    }
      
    if (noDiscountRadio.checked || (isNaN(discount_percent.value) && isNaN(discount_percent_battery.value))){
      discount_percent.value = 0;
      discount_percent_battery.value = 0;
      discount_percent_modal_input.value = 0;
      discount_percent_battery_modal_input.value = 0;
    }else{
      discount_percent_modal_input.value = discount_percent.value;
      discount_percent_battery_modal_input.value = discount_percent_battery.value;
    }
    
    if (manualPowerRadio.checked)
      minimum_panel_container.value = 0;

    // Show the modal programmatically
    const myModal = new bootstrap.Modal(document.getElementById('myModal'));
    myModal.show();

    // test prints
    console.log(place_modal_input.value);
    console.log(azimuth_modal_input.value);
    console.log(profile_modal_input.value);
    console.log(slider_hidden_input.value);
    console.log(minimum_panel_container.value);
    console.log('discount_percent_battery value:', discount_percent_battery.value);
    console.log('discount_percent_battery value:', discount_percent_battery_modal_input.value);
  }
  
})
// Reset the PV_kW_output element value to the initial value when the reset button is clicked
reset_button.addEventListener('click', resetForm);

// Add an event listener to the submit button
submit_modal.addEventListener('click', function(event) {
  
  // Validate the form inputs
  if (!validateForm()) {
    // prevent submitting the form
    event.preventDefault();
  }else{
      form.submit();
  }
});
// Test print
discount_percent.addEventListener('change', function() {
  console.log('discount_percent value:', this.value);
});
// Test print
discount_percent_battery.addEventListener('change', function() {
  console.log('discount_percent_battery value:', this.value);
});