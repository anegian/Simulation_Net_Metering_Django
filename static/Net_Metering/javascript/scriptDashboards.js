// const PvKWpDashboard = document.getElementById('PV_kWp_dashboard')
// PvKWpDashboard.value = pvKwp; // Set the value of the input element
// let PvKWpDashboardValue = PvKWpDashboard.value

const numberPanelsDashboard = document.getElementById('number_panels_dashboard')
numberPanelsDashboard.value = numberPanels; // Set the value of the input element
let numberPanelsDashboardValue = numberPanelsDashboard.value

const batteryAddButton = document.getElementById('battery_add_button');
const recalculateButton = document.getElementById('recalculate_button')

function recalculatePvSystemProperties(){
    // Record the start time
    const startTime = new Date().getTime();
  
    //   Handle the modified input
    numberPanelsDashboardValue = parseInt(numberPanelsDashboard.value);
    // Validate the parsed values
    if (isNaN(numberPanelsDashboardValue)) {
        throw new Error("Παρακαλώ ελέγξτε τον αριθμό ΦΒ Πάνελ που εισαγάγατε.");
    }
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    const url = '/simulation/recalculation/' ;  // Make sure this matches the URL pattern in your Django project's URLs

    // Create the data object
    let data = {
        // number of panels modified
        changed_number_panels: numberPanelsDashboardValue,
    };

    console.log(data);
    const jsonData = JSON.stringify(data);
  
  // Make the AJAX request
  ajaxRequest = $.ajax({
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
      let recalculatedPV = response.recalculated_pv;
      let totalInvestment = response.total_investment;
      let changed_number_panels = response.changed_number_panels;
      let new_panel_area = response.new_panel_area ;

      console.log("--- recalculatedPV: ", recalculatedPV, "---", 'totalInvestment: ', totalInvestment);
      
      // Update the input field with the calculated power
      $('#number_panels_dashboard').val(changed_number_panels);
      // Update the PV_kWp tag
      $('#PV_kWp').text(recalculatedPV);
      // Update the total investment tag
      $('#total_investment_tag').text(totalInvestment);
      $('#total_panel_area').text(new_panel_area);

    },
    error: function(xhr, status, errorThrown) {
      ajaxRequest.abort();
    }
  });
};

// Function to handle the "Calculate Power" button click
function handleRecalculation() {
      // Call the calculation function
      recalculatePvSystemProperties();
};

document.addEventListener('DOMContentLoaded', function() {
    PvKWpDashboardValue = pvKwp
    PvKWpDashboardValue = numberPanels
});

// PvKWpDashboard.addEventListener('input', function(){
//     if (PvKWpDashboard.value == '' || PvKWpDashboard.value == "0" )
//         PvKWpDashboard.value = '1';
//     PvKWpDashboardValue = PvKWpDashboard.value
// });

numberPanelsDashboard.addEventListener('input', function(){
    if (numberPanelsDashboard.value == '' || numberPanelsDashboard.value == '0')
        numberPanelsDashboard.value = '1';
    numberPanelsDashboardValue = numberPanelsDashboard.value
});

recalculateButton.addEventListener('click', handleRecalculation);
