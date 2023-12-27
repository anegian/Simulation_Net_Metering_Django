const addBatteryButton = document.getElementById("battery_add_button");

function addBatteryHandler() {
  console.log("Add Battery button is pressed");
  console.log("PV power in kW: ", pvKwp);
  // Record the start time
  const startTime = new Date().getTime();
  const csrfToken = document.querySelector(
    'input[name="csrfmiddlewaretoken"]'
  ).value;
  const url = "/simulation/addbattery/";
  // Create the data object
  let data = {
    power_kwp_value: pvKwp,
  };

  console.log(data);
  const jsonData = JSON.stringify(data);

  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
    body: jsonData,
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      return response.json();
    })
    .then((responseData) => {
      // Handle the successful response data
      console.log(responseData);
    })
    .catch((error) => {
      // Handle errors
      console.error("Fetch error:", error);
    })
    .finally(() => {
      // This block will run regardless of success or failure
      // Stop the rotation animation after the request is complete
    });

  //   Handle the PV kW power
  kwPvPowerdValue = parseInt(numberPanelsDashboard.value);
}

addBatteryButton.addEventListener("click", function () {
  // Remove the add battery button and place an input

  addBatteryHandler();
});
