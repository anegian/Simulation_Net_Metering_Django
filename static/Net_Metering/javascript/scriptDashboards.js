// const PvKWpDashboard = document.getElementById('PV_kWp_dashboard')
// PvKWpDashboard.value = pvKwp; // Set the value of the input element
// let PvKWpDashboardValue = PvKWpDashboard.value

const numberPanelsDashboard = document.getElementById('number_panels_dashboard')
numberPanelsDashboard.value = numberPanels; // Set the value of the input element
let numberPanelsDashboardValue = numberPanelsDashboard.value

const batteryAddButton = document.getElementById('battery_add_button');
const recalculateButton = document.getElementById('recalculate_button')

function updateChart2Datasets(newTotalSavingsArray, newTotalProductionArray, newPaybackYear){
  
  window.totalSavingsArray = newTotalSavingsArray;
  window.totalProductionArray = newTotalProductionArray;
  window.paybackYear = newPaybackYear;
};

// Function to update a specific chart
function updateChart(chartId, newTotalSavingsArray, newTotalProductionArray, newPaybackYear) {
  if (globalCharts.hasOwnProperty(chartId)) {
    let chart = globalCharts[chartId];
    // Update chart data with new data
    chart.data.datasets[0].data = newTotalSavingsArray; // Update the first dataset
    chart.data.datasets[1].data = newTotalProductionArray; // Update the second dataset
    
    // Update the paybackYear in the chart options
    chart.options.animation.onComplete = function () {
      const ctx = chart.ctx;
      const xAxis = chart.scales["x-axis-0"];
      const yAxis = chart.scales["y-axis-0"];
      const xValue = xAxis.getPixelForValue(newPaybackYear); // Use the updated paybackYear
   
      ctx.save();
      ctx.strokeStyle = "#e34c0cbf"; // Customize line color
      ctx.lineWidth = 2; // Customize line width
      ctx.beginPath();
      ctx.moveTo(xValue, yAxis.top);
      ctx.lineTo(xValue, yAxis.bottom);
      ctx.stroke();

      // Draw a label next to the line
      ctx.fillStyle = "#f2f2f2"; // Customize label color
      ctx.font = "12px Arial"; // Customize label font
      ctx.textAlign = "left";
      ctx.textBaseline = "middle";
      const label = "Έτος Απόσβεσης"; // Your label text
      const labelX = xValue + 10; // Adjust the X position of the label
      const labelY = (yAxis.top + yAxis.bottom) / 2 + 10; // Center the label vertically and move it down by 10 pixels
      ctx.fillText(label, labelX, labelY);

      ctx.restore();
    };
    chart.update(); // Apply the changes
  } else {
    console.error(`Chart with ID '${chartId}' not found.`);
  }
}

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
      // When the AJAX request starts (e.g., in the beforeSend callback)
    },
    beforeSend: function() {
      // Start the rotation animation when the request begins
      $("#recalculate_button img").addClass("rotate");
    },
    
    success: function(response) {
      setTimeout(function () {

      // Handle the response
      let recalculatedPV = response.recalculated_pv;
      let totalInvestment = response.total_investment;
      let changed_number_panels = response.changed_number_panels;
      let newPanelArea = response.new_panel_area;
      let annualSavings = response.annual_savings;
      let profitPercent = response.profitPercent;
      let totalSavingsPotential = response.total_savings_potential;
      let annual_PV_energy_produced = response.annual_PV_energy_produced;
      let annual_consumption =  response.annual_consumption;
      let pv_kwp_max_value = response.pv_kwp_max_value;
      let potentialKwh = response.potential_kwh;
      let totalSavings = response.total_savings;
      let paybackPeriod = response.payback_period;
      let newPaybackYear = response.payback_year_float;
      // for chart2
      let total_production_kwh_array = response.total_production_kwh_array;
      let newTotalProductionArray = total_production_kwh_array;
      let total_savings_array = response.total_savings_array;
      let newTotalSavingsArray = response.total_savings_array;
      let consumptionTotalCharges = response.consumption_total_charges;

      console.log('totalSavingsPotential: ', totalSavingsPotential)
      console.log("--- recalculatedPV: ", recalculatedPV, "---", 'totalInvestment: ', totalInvestment);
      // Update the input field with the calculated power
      $('#number_panels_dashboard').val(changed_number_panels);
      // Update the PV_kWp tag
      $('#PV_kWp').text(recalculatedPV);
      // Update the total investment tag
      $('#total_investment_tag').text(totalInvestment);
      $('#total_panel_area').text(newPanelArea);
      $('#profit_tag').text(totalSavingsPotential);
      $('#profitPercent_tag').text(profitPercent);
      
      updateChart2Datasets(newTotalSavingsArray, newTotalProductionArray, newPaybackYear)
      updateChart('myChart2', newTotalSavingsArray, newTotalProductionArray, newPaybackYear)

      if (potentialKwh == 0 && profitPercent >= 100) {
        $("#potential_savings").html('<span style="color: #738725;">Εκμηδενίσατε το ετήσιο κόστος</span>, όμως δεν υπάρχει διαθέσιμο <br>πλεόνασμα ιδιοκαταναλισκόμενης ενέργειας');
      } else if (totalSavingsPotential > 0 && profitPercent >= 100) {
        $("#potential_savings").html('<span style="color: green;">Πλεόνασμα ιδιοκαταναλισκόμενης ενέργειας:<br>✔</span> έως επιπλέον <span id="potentialKwhValue">' + potentialKwh + '</span> kWh<br>');
      } else if (annual_consumption > annual_PV_energy_produced && profitPercent < 85 && recalculatedPV <= pv_kwp_max_value) {
        $("#potential_savings").html('<span style="color: red;">Προσοχή! </span><span style="color: lightslategray;">Απαιτείται μεγαλύτερο ΦΒ <br>σύστημα για κάλυψη ετήσιας κατανάλωσης.</span>');
      } else if ((profitPercent > 90 && profitPercent < 100 && recalculatedPV < pv_kwp_max_value) || (recalculatedPV < pv_kwp_max_value)) {
        $("#potential_savings").html('<span style="color: lightskyblue;">Με μικρές αλλαγές, με προσθήκη μπαταρίας ή με λίγο <br>μεγαλύτερο Φ/Β σύστημα, μπορείτε να εκμηδενίσετε το ετήσιο κόστος!!</span>');
      } else if ((recalculatedPV == pv_kwp_max_value || recalculatedPV == pv_kwp_max_value) && annual_consumption > annual_PV_energy_produced) {
        $("#potential_savings").html('<span style="color: lightslategrey;">Η κατανάλωσή σας υπερβαίνει την παραγόμενη ενέργεια <br>και το ΦΒ σύστημα έχει τη μέγιστη τιμή kWp. Δοκιμάστε <br>αλλαγές σε κλίση, αζιμούθιο ή σκιάσεις.</span>');
      } else if (potentialKwh == 0) {
        $("#potential_savings").html('<span style="color: lightslategrey;">Περιθώριο κέρδους:<br></span> Δεν υπάρχει διαθέσιμο πλεόνασμα ιδιοκαταναλισκόμενης ενέργειας');
      }

      if (profitPercent == 100) {
        $("#profitPercentLabel").css("color", "green");
        $("#profitPercent_tag").text(profitPercent || '0');
        $("#profitPercent_tag").append("% ✔");
        $("#annualCostLabel").css({
          "color": "lightskyblue",
          "font-size": "12px"
        });
        $("#annualCostLabel").text("Ετήσιο Κόστος Ρεύματος: " + (consumptionTotalCharges || '0') + "€");
      } else if (profitPercent > 90 && profitPercent < 100) {
        $("#profitPercentLabel").css("color", "#738725");
        $("#profitPercent_tag").text(profitPercent || '0');
        $("#profitPercent_tag").append(" %");
        $("#annualCostLabel").css({
          "color": "lightskyblue",
          "font-size": "12px"
        });
        $("#annualCostLabel").text("Ετήσιο Κόστος Ρεύματος: " + (consumptionTotalCharges || '0') + "€");
      } else {
        $("#profitPercentLabel").css("color", "grey");
        $("#profitPercent_tag").text(profitPercent || '0');
        $("#profitPercent_tag").append(" %");
        $("#annualCostLabel").css({
          "color": "lightskyblue",
          "font-size": "12px"
        });
        $("#annualCostLabel").text("Ετήσιο Κόστος Ρεύματος: " + (consumptionTotalCharges || '0') + "€");
      }

      if (paybackPeriod == 0 || paybackPeriod =="0") {
        $("#paybackPeriod_tag").css("color", "lightslategrey");
        $('#paybackPeriod_tag').html('&#8734; <br> Δυστυχώς έχετε μηδενικό όφελος');
      } else {
        $('#paybackPeriod_tag').text(paybackPeriod || '0');
      }

      // When the AJAX request completes (e.g., in the success or error callback)
      $("#recalculate_button img").removeClass("rotate");
      // Handle your AJAX success here
        // ...
      }, 1000); // 2-second delay (adjust as needed)
    },
    error: function(xhr, status, errorThrown) {
      ajaxRequest.abort();
      // When the AJAX request completes (e.g., in the success or error callback)
      $("##recalculate_button img").removeClass("rotate");
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
