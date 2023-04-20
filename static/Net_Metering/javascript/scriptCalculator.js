// variables initialization
const slider = document.getElementById("myRangeSlider");
const output = document.getElementById("slider-value");

    // Set the initial value of the output element to 0
    slider.value = 0;
    output.innerHTML = slider.value;
    slider.disabled = 'phase_load';

// Used to validate that the calculator form has been filled by the user
function validateForm() {

        const powerKWValue = document.getElementById('myRangeSlider').value;

        if (powerKWValue === '0') {
            alert("Please fill out the form");
            return false; // return false to indicate that the form was not submitted
        }
        return true;
};

// Listen for changes in the phase load input and store the selected option
document.getElementById("id_select_phase").addEventListener("change", function(event){
    slider.value = 0; // Update the slider value to 0 when the phase load is changed
    slider.max = event.target.value === 'single_phase' ? 5 : 25
    slider.disabled = event.target.value === 'phase_load'
    output.innerHTML = slider.value; // Update the output element value to 0 when the phase load is changed
});

// Update the current slider value (each time you drag the slider handle)
    slider.oninput = function() {
        output.innerHTML = this.value;
    };

// Reset the output element value to the initial value when the reset button is clicked
    document.querySelector('button[type="reset"]').addEventListener('click', function(event) {
        slider.disabled = "phase_load"
        slider.value = 0;
        output.innerHTML = slider.value;
    });