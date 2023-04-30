// variables initialization
const slider = document.getElementById("myRangeSlider");
const output = document.getElementById("slider-value");
const selectKwh = document.getElementById("id_select_kwh");
// Get the initial value of the selectKwh element from the form
const initialKwhValue = selectKwh.value;
const selectDistrict = document.getElementById("id_select_district");
const selectPhase = document.getElementById("id_select_phase");
const submitButton = document.getElementById("submitBtn");
const errorMessage = document.getElementById('error-message-panel');
const errorMessage2 = document.getElementById('error-message-panel5');
const errorMessage3 = document.getElementById('error-message-panel6');

// Set the initial value of the output element to 0
slider.value = 0;
output.innerHTML = slider.value;
slider.disabled = true;
selectKwh.disabled = true;

// Update the current slider value (each time you drag the slider handle)
slider.oninput = function() {
    output.innerHTML = this.value;
    errorMessage3.style = 'none';
};      

selectDistrict.addEventListener("change", function(event){
    errorMessage.style.display = "none";
    selectDistrict.classList.remove('error');
})

// Listen for changes in the phase load input and store the selected option
selectPhase.addEventListener("change", function(event){
    selectKwh.value = initialKwhValue; // Set the value of the selectKwh element to the initial value
    slider.value = 0; // Update the slider value to 0 when the phase load is changed
    slider.max = event.target.value === 'single_phase' ? 5 : 10
    slider.disabled = event.target.value === 'phase_load'
    output.innerHTML = slider.value; // Update the output element value to 0 when the phase load is changed

    selectKwh.disabled = event.target.value === 'phase_load'
    errorMessage2.style.display = "none";
    selectPhase.classList.remove('error');
    
    if (event.target.value === 'single_phase') {
        
        // Enable the first two options and disable the rest
        selectKwh.options[0].disabled = false;
        selectKwh.options[1].disabled = false;
        for (let i = 3; i < selectKwh.options.length; i++) {
            selectKwh.options[i].disabled = true;
        }
    } else {
        // Enable all options
        for (let i = 0; i < selectKwh.options.length; i++) {
            selectKwh.options[i].disabled = false;
        }
    }

});

// Reset the output element value to the initial value when the reset button is clicked
document.querySelector('button[type="reset"]').addEventListener('click', function(event) {
    slider.disabled = true;
    selectKwh.disabled = true;
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

selectKwh.addEventListener("change", function(event){
    console.log(selectKwh.value);

    switch (selectKwh.value) {
        case '2':
            slider.value = 2;
            break;
        case '3':
            slider.value = 3;
            break;
        case '4':
            slider.value = 4;
            break;
        case '5':
            slider.value = 5;
            break;
        case '6':
            slider.value = 6;
            break;
        case '10':
            slider.value = 10;
            break;
        default:
            slider.value = 0;
    }

    output.innerHTML = slider.value;
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