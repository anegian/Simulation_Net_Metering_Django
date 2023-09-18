// variables initialization
const themeSlider = document.getElementById('theme-slider');
const slider = document.getElementById("myRangeSlider");
const slider_hidden_input = document.getElementById("myRangeSliderHidden");
const shadingSlider = document.getElementById("shadings_slider");
let shadingSliderValue = shadingSlider.value;
const PV_kW_output = document.getElementById("slider-value");
// annual Kwh
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
const customParams = document.getElementById('customParameters');
let selectedPlaceInstalmentValue;
const roofRadioButton = document.getElementById('roof');
const phase_load_selected = document.getElementById("id_select_phase");
const phaseLoadDefaultSelection = document.getElementById("phase_load");
let priceKwhInput = document.getElementById('price_kwh');
const reset_button = document.getElementById("resetBtn");
const lastPanelField = document.getElementById('lastPanelField');
const error_message = document.getElementById('error-message-panel');
const error_message2 = document.getElementById('error-message-panel5');
const error_message3 = document.getElementById('error-message-panel6');
const max_message = document.getElementById("max-message")
// Get the selected radio button's value
const storage_selection = document.getElementById("with_storage");
const storage_kW = document.getElementById("storage_kw");
const noDiscountRadio = document.getElementById('no-discount');
const discountRadio = document.getElementById('discount');
const no_storage_selection = document.getElementById("without_storage");
// select all radio buttons with the class "form-check-input"
const radio_buttons = document.querySelectorAll('.form-check-input');
const manualPowerRadio = document.getElementById('manual_power');
const autoPowerRadio = document.getElementById('auto_power');
const power_kWp_method = document.getElementsByName('power_kWp_method');
const autoPowerDiv = document.getElementById('autoPower-button-input');
const autoPowerButton = document.getElementById('calculateProductionButton');
let isAutoCalculatingPower;
// Get references to the radio inputs and the azimuthInput
const radioAzimuthInputs = document.querySelectorAll('input[name="azimuth"]');
const azimuthInput = document.getElementById('azimuthInput');
const azimuthDefaultRadio = document.getElementById("south");
const radioTiltInputs = document.querySelectorAll('input[name="inclination"]');
const tiltInput = document.getElementById('tiltInput');
const tiltDefaultRadio = document.getElementById('inclination30');
const profileDefaultRadio = document.getElementById('day-power');
const powerRadioButton = document.querySelector('input[name="power_option"]:checked');
const special_production_output = document.getElementById('placeProduction');
const minimum_panel_container = document.getElementById('minimumPanels');
const total_PV_area = document.getElementById('totalArea');
const panelContainers = document.getElementsByClassName("panel-calculator");
const previousButton = document.getElementById("previous-button");
const nextButton = document.getElementById("next-button");
const circleLinks = document.querySelectorAll('.circle-link');
let currentPanelIndex = 0;
let submitBtnEnabled;
let loadingBar = document.getElementById('progressBar');

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
// Show the modal programmatically
const myModal = new bootstrap.Modal(document.getElementById('myModal'));
// Get references to the discount_percent and discount battery select elements
const discountPercentSelect = document.querySelector('.discount_percent_select');
const discountPercentBatterySelect = document.querySelector('.discount_percent_battery_select');
let autoCalculatedPower;
let autoCalculatedPowerNumber;

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
  slider.value = 0;
  slider.min = 0;
  slider.step = 0.1;
  PV_kW_output.innerHTML = slider.value;
  manualPowerRadio.disabled = false;
  autoPowerRadio.disabled = false;
  slider.classList.remove("disabled-slider");
}
function disableSlider(){
  slider.disabled = true;
  slider.value = 0;
  slider.min = 0;
  slider_hidden_input.value = 0;
  if (annual_Kwh_input.value === '0' || annual_Kwh_input.value.trim() === "" ) {
      manualPowerRadio.disabled = true;
      autoPowerRadio.disabled = true;
  } 
  PV_kW_output.innerHTML = slider.value;
  slider.classList.add("disabled-slider");
}
// Functions to show and hide auto powwer div
function hideAutoPowerDiv(){
  autoPowerDiv.classList.add('hidden');
  autoPowerDiv.style.display = 'none'; // Hide the div
}
function showAutoPowerDiv(){
  autoPowerDiv.classList.remove('hidden');
  autoPowerDiv.style.display = 'block'; // Show the div
}
function resetAutoPowerDiv(){
  isAutoCalculatingPower = false;
  autoCalculatedPower = false;
  autoCalculatedPowerNumber = 0;
  slider_hidden_input.value = 0;
  setStorage(slider_hidden_input.value);
  special_production_output.value = "";
  minimum_panel_container.value = "";
  total_PV_area.value = "";
  $('#completionMessage').hide();
  console.log("Reset Power Div: yes", "Auto power value is now: ", autoCalculatedPowerNumber);
}
// Disable and reset every element
function disableElements() {
  placeSelected.value = "";
  latitudeInput.value = "";
  longitudeInput.value = "" ; 
  disablePanelButton(nextButton);
  disablePanelButton(previousButton);
  disablePanelButton(form_submit_button);
  submitBtnEnabled = false;
  roofRadioButton.checked = true;
  shadingSliderValue = "1";
  defaultPanelParams.selected  = true;
  tiltDefaultRadio.checked = true;
  tiltInput.value = '30'; // Set the value of tiltInput to 30
  azimuthDefaultRadio.checked = true;
  azimuthInput.value = 0;
  phase_load_selected.value = "phase_load";// Set the default phase value 
  priceKwhInput.max = 999;
  priceKwhInput.value = 155;
  annual_Kwh_input.disabled = true;
  annual_Kwh_input.value = ""
  profileDefaultRadio.checked = true;
  storage_selection.disabled = true;
  storage_kW.disabled = true; 
  manualPowerRadio.disabled = true;
  manualPowerRadio.checked = true;
  autoPowerRadio.disabled = true;
  isAutoCalculatingPower = false;
  hideAutoPowerDiv();
  resetAutoPowerDiv();
  // Discounts 
  discount_percent.max = 100;
  discount_percent.min = 0;
  discount_percent_battery.max = 100;
  discount_percent_battery.min = '0';
  selectedPlaceInstalmentValue = 'roof';
  noDiscountRadio.checked = true;
  discountPercentContainer.style.display = 'none';
  customParams.checked = false;
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
  document.documentElement.style.setProperty('--form-label-color', '#f2f2f2');
  document.documentElement.style.setProperty('--title-panel-color', '#f2f2f2');
  document.documentElement.style.setProperty('--slider-color', '#f2f2f2');
  document.documentElement.style.setProperty('--slider-value-kW-color', '#f2f2f2');
  document.documentElement.style.setProperty('--thumb-color', '#393052');
  document.documentElement.style.setProperty('--bg-color-calculator-page', '#29233b');
  document.documentElement.style.setProperty('--bg-color-submit-button', '#738725'); 
  document.documentElement.style.setProperty('--help-popper', 'f2f2f2');
}

// Function to toggle the visibility of the power calculate div
function toggleAutoPowerDiv() {
  if (manualPowerRadio.checked) {
    hideAutoPowerDiv();
    enableSlider();
    setStorage(slider.value);
    disablePanelButton(nextButton);
  } else if (autoPowerRadio.checked) {
    showAutoPowerDiv();
    console.log("in toggle Auto Power: ", autoCalculatedPowerNumber);
    console.log("Auto calculated?", autoCalculatedPower);

    if (autoCalculatedPower){
      slider.disabled = true // must add this line to prevent the manual use of slider
      slider.value = autoCalculatedPowerNumber;
      slider_hidden_input.value = autoCalculatedPowerNumber;
      PV_kW_output.innerHTML = autoCalculatedPowerNumber;
      setStorage(slider_hidden_input.value);
      enablePanelButton(nextButton);
      console.log("Normal condition, auto power has been generated: ", autoCalculatedPowerNumber);
    }else{
      disableSlider();
      resetAutoPowerDiv();
      disablePanelButton(nextButton);
      console.log("else condition: ", autoCalculatedPowerNumber);
    }
  }
}
// Function to handle the "Calculate Power" button click
function handleCalculateButtonClick() {
  if (isAutoCalculatingPower) {
    // Calculation is already in progress, do nothing or show a message
    console.log("Calculation is already in progress");
    console.log('shadingSliderValue');
    return;
  }else{
    // Set the flag to indicate that the calculation is in progress
    isAutoCalculatingPower = true;

    // Disable the button and change its text to indicate loading
    autoPowerButton.disabled = true;

    autoPowerButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Calculating...';

    // Call the calculation function
    calculateAutoPower();

    // Hide the completion message initially
    $('#completionMessage').hide();
  }
}

function calculateAutoPower() {
  // Record the start time
  const startTime = new Date().getTime();
  
  // Show the progress bar at the start of the request
  $('#progressBar').css('width', '0%'); // reset progress bar
  $('#progressBar').show();
  
  // Get the latitude, longitude, azimuth, and tilt values from the form
  const latitudeValue = parseFloat(latitudeInput.value);
  const longitudeValue = parseFloat(longitudeInput.value);
  const azimuthValue = parseFloat(azimuthInput.value);
  const tiltValue = parseFloat(tiltInput.value);
  let panelKWpValue = parseFloat(panelWpInput.value);
  let shadingInputValue = parseInt(shadingSliderValue);
  let powerRadioButton = powerRadioButton.value;
  // from Wp to kWp
  panelKWpValue /= 1000; 
  const panelAreaValue = parseFloat(panelAreaInput.value);
  let panelEfficiencyValue = parseFloat(panelEfficiencyInput.value);
  //  from xx % to 0,xx %
  panelEfficiencyValue /= 100;
  const annualKWhValue = parseInt(annual_Kwh_input.value);
  const placeInstalmentValue = selectedPlaceInstalmentValue;
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
        panel_Wp_value: panelKWpValue,
        place_instalment_value: placeInstalmentValue,
        shading_value: shadingInputValue,
        consumption_profile: powerRadioButton,
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
    
    xhr: function() {
      let xhr = new window.XMLHttpRequest();
      // Initialize the progress percentage
      let currentPercentage = 0;

      // Track progress events to update the progress bar
      xhr.upload.addEventListener("progress", function(event) {
        // Calculate the current percentage of completion
        currentPercentage = (event.loaded/ event.total) * 100;
          // Update the progress bar using a CSS animation
        $('#progressBar').css('animation', 'none'); // Disable any existing animation
        $('#progressBar').css('animation', 'fill-progress-bar 2s linear forwards');
        // Set the width of the progress bar based on the current percentage
        $('#progressBar').css('width', currentPercentage + '%');


      }, false);
      return xhr;
    },
  
    success: function(response) {
      // Handle the response
      const specialProduction = response.special_production;
      let recommended_kWp = response.recommended_kWp;
      let minimum_PV_panels = response.minimum_PV_panels;
      let totalArea = response.total_area;
      
      if ( recommended_kWp > Number(slider.max) ){
        console.log("@@@ The energy consumption exceeds solar production @@@")
        console.log("--- panel kWp: ", panelKWpValue, "---")
        recommended_kWp = Number(slider.max);
        // panel Wp was set as decimal, so we have to multiply with 100
        minimum_PV_panels = (recommended_kWp * panelKWpValue * 10 ).toFixed(0) ; 
        totalArea = (minimum_PV_panels * panelAreaValue).toFixed(1);
      }

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
      // Hide the progress bar on success
      $('#progressBar').hide();
      // Display a completion message with the actual time taken
      const finishTime =  new Date().getTime();
      const elapsedTimeSeconds = ((finishTime - startTime) / 1000).toFixed(2);
      $('#completionMessage').text(`Ολοκληρώθηκε σε ${elapsedTimeSeconds} seconds`);
      $('#completionMessage').show(); // Show the completion message
     
      autoPowerButton.disabled = false;
      isAutoCalculatingPower = false;
      autoPowerButton.innerHTML = 'Υπολογισμός Απαιτούμενης Ισχύος';

    },
    error: function(xhr, textStatus, errorThrown) {
      console.log('Error:', errorThrown);
      // Hide the progress bar on error
      $('#progressBar').hide();
      
    }
  });
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
    if ( annual_Kwh_input.value.trim() === '' || annual_Kwh_input.value === '0' ) {
      // If the kWh field is empty or contains only spaces, disable the "Next" button
      disablePanelButton(nextButton);
      disablePanelButton(form_submit_button);
      console.log("NOW WE ARE IN PANEL no", currentPanelIndex, "--- 1st if");
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

    // panel array has zero indexing (panel 4 -> index 3)
    if (index === 3){
      toggleNextButtonState();
    }else if (index === 4 && slider.value === '0'){
      disablePanelButton(nextButton);
    } else if (index === 4 && autoPowerRadio.checked && autoCalculatedPower === false){
      disableSlider();
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
  }

  // Disable the form_submit_button when moving to a previous panel
  if (submitBtnEnabled) {
    submitBtnEnabled = false;
    disablePanelButton(form_submit_button);
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
    
    console.log('Current Panel Index:', currentPanelIndex + 1);

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
  disableSlider();
  // Show the first panel and scroll to it
  currentPanelIndex = 0; // Reset to the first panel index
  showPanel(currentPanelIndex);
  autoCalculatedPower = false;
};
function setPanelParameters(){
  const selectedOption = panelParamsSelect.options[panelParamsSelect.selectedIndex];
  const wp = selectedOption.value;
  const efficiency = selectedOption.dataset.efficiency;
  const panel_area = selectedOption.dataset.panel_area;
  const panel_cost = selectedOption.dataset.panel_cost;
  
  panelWpInput.value = wp;
  panelEfficiencyInput.value = efficiency;
  panelAreaInput.value = panel_area;
  panelCostInput.value = panel_cost;
};
function clearPanelParameters(){
  panelWpInput.value = "";
  panelEfficiencyInput.value = "";
  panelAreaInput.value = "";
  panelCostInput.value = "";
};

function validatePanelWp(){
  // Validation Rules
  const panelWpEntered = panelWpInput.value;
  let sanitizedWpValue = panelWpEntered.replace(/[^0-9]/g, '');
  // Check value Entered & Limit the value to at most 500Wp
  if (sanitizedWpValue > 500) {
    sanitizedWpValue = 500;
  }
  // after check set the value of the input
  panelWpInput.value = sanitizedWpValue; 
};

function validatePanelEfficiency(){
  const enteredEfficiencyValue = panelEfficiencyInput.value;

  $('#panelEfficiencyInput').mask('00.0', {
    reverse: true,
    translation: {
      '0': { pattern: /[0-9]/ }, // Allow 0-9 in the tens place
    },
  }); 

  if (isNaN(enteredEfficiencyValue) || enteredEfficiencyValue < 0.0) {
    // Invalid input, set to a default value
    $(this).val('0.0');
  } else if (enteredEfficiencyValue > 30.0) {
      // Input value exceeds maximum, set to the maximum value
      $(this).val('30.0');
  }
};

function validatePanelArea(){
  const enteredAreaValue = panelAreaInput.value;

  $('#panelAreaInput').mask('0.00', {
    reverse: true,
    translation: {
      '0': { pattern: /[0-9]/ }, // Allow 0-9 in the tens place
    },
  }); 

  if (isNaN(enteredAreaValue) || enteredAreaValue < 0.00) {
    // Invalid input, set to a default value
    $(this).val('0.00');
  }
};

function validatePanelCost(){
  // Validation Rules
  const panelCostEntered = panelCostInput.value;
  let sanitizedCostValue = panelCostEntered.replace(/[^0-9]/g, '');
  // Check value Entered & Limit the value to at most 500Wp
  if (sanitizedCostValue > 500) {
    sanitizedCostValue = 500;
  }
  // after check set the value of the input
  panelCostInput.value = sanitizedCostValue; 
};

// Set the initial values of all elements to 0
disableElements();
disableSlider();
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
  setPanelParameters();
  customParams.checked = false;

  // Toggle the 'highlight' class based on the checkbox state
  $('.panels_parameters input[type="number"], .panels_parameters input[type="text"]').removeClass('highlight-input');
  $('.panels_parameters input[type="number"], .panels_parameters input[type="text"]').removeClass('highlight-filled');
  console.log(panelAreaInput.value)
});

customParams.addEventListener('click', function(){
  if (customParams.checked) {
    clearPanelParameters();
    // Remove the "readonly" attribute from the input fields
    panelWpInput.removeAttribute('readonly');
    panelEfficiencyInput.removeAttribute('readonly');
    panelAreaInput.removeAttribute('readonly');
    panelCostInput.removeAttribute('readonly');
  } else {
      setPanelParameters();   
      // If the checkbox is unchecked, add the "readonly" attribute back to the input fields
      panelWpInput.setAttribute('readonly', 'readonly');
      panelEfficiencyInput.setAttribute('readonly', 'readonly');
      panelAreaInput.setAttribute('readonly', 'readonly');
      panelCostInput.setAttribute('readonly', 'readonly');
  }
});

$(document).ready(function () {
  $('#customParameters').click(function () {
    const isChecked = this.checked;
    const inputs = $('.panels_parameters input[type="number"], .panels_parameters input[type="text"]');
        
    // Toggle the 'highlight' class based on the checkbox state
    inputs.toggleClass('highlight-input', isChecked);

    if (!isChecked) {
        inputs.removeClass('highlight-filled');
    }
  });
    
});

  // Add input event listeners to remove the border when the field is filled
  $('.panels_parameters input[type="number"], .panels_parameters input[type="text"]').on('input', function () {
    if ($(this).val().trim() !== '') {
      $(this).removeClass('highlight-input');
      $(this).addClass('highlight-filled');
    }else{
      $(this).addClass('highlight-input');
      $(this).removeClass('highlight-filled'); // Remove 'highlight-filled' class when it's empty
    }
  });

// Add input event listeners to trigger the validation function
panelWpInput.addEventListener('input', validatePanelWp);
panelEfficiencyInput.addEventListener('input', validatePanelEfficiency);
panelAreaInput.addEventListener('input', validatePanelArea);
panelCostInput.addEventListener('input', validatePanelCost);

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
    shadingSliderValue = "1";
    azimuthDefaultRadio.checked = true;
    tiltDefaultRadio.checked = true;
    tiltInput.value = '30'; // Set the value of tiltInput to 30
    phaseLoadDefaultSelection.value = "phase_load"; // Set the default value here
    hideAutoPowerDiv();
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

  
  if (event.target.value === 'single_phase' || event.target.value === '3_phase' ){
      disableErrorMessages();
      enableAnnualkWh();
      annual_Kwh_input.value = "";
      slider.max = event.target.value === 'single_phase' ? 5 : 10.8;
      enableSlider();
  }else{
      disableElements();
  } 

  check_selection_kwh_conditions();
  disableSlider();
});
annual_Kwh_input.addEventListener("input", function(){
    enableSlider();
    enableStorage();
    let enteredValue = annual_Kwh_input.value;
    let sanitizedValue = enteredValue.replace(/[^0-9]/g, '');
    annual_Kwh_input.value = sanitizedValue;
    const maxValue = parseInt (annual_Kwh_input.max)
    
    if (parseInt(sanitizedValue) > maxValue) {
        sanitizedValue = maxValue;
        annual_Kwh_input.value = sanitizedValue;
        max_message.style.display = "block";
    } else {
        max_message.style.display = "none";
    }

    if (parseInt(sanitizedValue) <= 999 || sanitizedValue === "" ){
      disablePanelButton(nextButton);
      disablePanelButton(form_submit_button);
    }else{
      enablePanelButton(nextButton);
    }
});

annual_Kwh_input.addEventListener("change", function(){
  if (autoCalculatedPower){
    resetAutoPowerDiv();
    hideAutoPowerDiv();
    manualPowerRadio.checked = true;
  }
});

// Add an event listener to the "Next" button
nextButton.addEventListener('click', function() {
  if (phase_load_selected.value != 'phase_load' && isNaN(annual_Kwh_input.value) && nextButton.disabled) {
      annual_Kwh_input.classList.add('highlight-input');
  } else {
      // Input is valid, remove the CSS class
      annual_Kwh_input.classList.remove('highlight-input');
  }
});

slider.addEventListener("change", function(){
    disableErrorMessages();
    PV_kW_output.innerHTML = slider.value; 
    slider_hidden_input.value = slider.value;
    setStorage(slider.value)
    console.log(slider.value);
    if (PV_kW_output.innerHTML === '0'){
      disablePanelButton(nextButton);
      disablePanelButton(form_submit_button);
      submitBtnEnabled = false;
    }else{
      enablePanelButton(nextButton);
    }
});
slider_hidden_input.addEventListener("change", setStorage(slider_hidden_input.value));

shadingSlider.addEventListener('change', function(){
  shadingSliderValue = shadingSlider.value;
});
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
        document.documentElement.style.setProperty('--form-label-color', '#f2f2f2');
        document.documentElement.style.setProperty('--title-panel-color', '#f2f2f2');
        document.documentElement.style.setProperty('--slider-color', '#f2f2f2');
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
        document.documentElement.style.setProperty('--form-label-color', '#333');
        document.documentElement.style.setProperty('--title-panel-color', '#538bc7');
        document.documentElement.style.setProperty('--slider-color', '#f2f2f2');
        document.documentElement.style.setProperty('--slider-value-kW-color', 'lightgrey');
        document.documentElement.style.setProperty('--bg-color-calculator-page', '#f2f2f2');
        document.documentElement.style.setProperty('--thumb-color', '#738725');
        document.documentElement.style.setProperty('--bg-color-submit-button', '#738725');
        document.documentElement.style.setProperty('--help-popper', 'blue');
        }
    });
// Add event listeners to the radio buttons and the calculation button
// Loop through each radio button in the NodeList and add an event listener
power_kWp_method.forEach(function(radioButton) {
  radioButton.addEventListener('change', toggleAutoPowerDiv);
});
autoPowerButton.addEventListener('click', handleCalculateButtonClick);
// Discount percents
noDiscountRadio.addEventListener('change', showDiscountInputs);
discountRadio.addEventListener('change', showDiscountInputs);

// Reset the PV_kW_output element value to the initial value when the reset button is clicked
reset_button.addEventListener('click', resetForm);

priceKwhInput.addEventListener('input', function(){
    if (priceKwhInput.value > 999){
    priceKwhInput.value = 999;
  }

  
  priceKwhInput.value = this.value;
});

//Submit, reset, Modal events
form_submit_button.addEventListener('click', function(event){

  if (powerRadioButton) {
    // Get the label element associated with the selected radio button
    const labelElement = document.querySelector(`label[for="${powerRadioButton.id}"]`);
    
    if (labelElement) {
      // Get the label content and set it as the value of the target input field
      profile_modal_input.value = labelElement.textContent;
    }
  }

  slider_hidden_input.value = slider.value;
  power_modal_input.value = slider_hidden_input.value;

  if (storage_selection.checked){
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
    
  if (manualPowerRadio.checked){
    minimum_panel_container.value = 0;
  }

  if ( discountRadio.checked && discount_percent_battery.value > 0 && no_storage_selection.checked ){
    alert('Έχετε επιλέξει ποσοστό έκπτωσης μπαταρίας, χωρίς να επιλέξετε προσθήκη συσσωρευτών!');
  } else {
    place_modal_input.value = placeSelected.value;
    azimuth_modal_input.value = azimuthInput.value;
    tilt_modal_input.value = tiltInput.value;
    annual_Kwh_modal_input.value = annual_Kwh_input.value;  
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
  
});

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