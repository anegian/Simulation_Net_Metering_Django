// DASHBOARD CHART 1
const cityValues = [50,60,70,80,90,100,110,120,130,140,150];
const sunValues = [7,8,8,9,9,9,10,11,14,14,15];

new Chart("myChart1", {
  type: "line",
  data: {
    labels: cityValues,
    datasets: [{
      fill: false,
      lineTension: 0,
      backgroundColor: "rgba(0,0,255,1.0)",
      borderColor: "rgba(0,0,255,0.1)",
      data: sunValues
    }]
  },
  options: {
    title: {
      display: true,
      text: "Annual Production"
    },
    legend: {display: false},
    scales: {
      yAxes: [{ticks: {min: 6, max:16}}],
    }
    
  }
});

// DASHBOARD CHART 2
const profitValues = [100,200,300,400,500,600,700,800,900,1000];

new Chart("myChart2", {
  type: "line",
  data: {
    labels: profitValues,
    datasets: [{ 
      data: [860,1140,1060,1060,1070,1110,1330,2210,7830,2478],
      borderColor: "red",
      fill: false
    }, { 
      data: [1600,1700,1700,1900,2000,2700,4000,5000,6000,7000],
      borderColor: "green",
      fill: false
    }, { 
      data: [300,700,2000,5000,6000,4000,2000,1000,200,100],
      borderColor: "blue",
      fill: false
    }]
  },
  options: {
      title: {
      display: true,
      text: "Return of Investement"
    }
  }
});

// DASHBOARD CHART 3
var zValues = ["Italy", "France", "Spain", "USA", "Argentina"];
var rValues = [55, 49, 44, 24, 15];
var barColors = [
  "#b91d47",
  "#00aba9",
  "#2b5797",
  "#e8c3b9",
  "#1e7145"
];

new Chart("myChart3", {
  type: "pie",
  data: {
    labels: zValues,
    datasets: [{
      backgroundColor: barColors,
      data: rValues
    }]
  },
  options: {
    title: {
      display: true,
      text: "Profitability"
    }
  }
});


// DASHBOARD STARTING CHART
var ctx = document.getElementById("energy-balance-chart").getContext("2d");

                // Generate the data for the chart, including the energy generation, consumption, and net balance over time
                var generationData = [100, 150, 200, 250, 300];
                var consumptionData = [200, 250, 300, 350, 400];
                var netBalanceData = generationData.map(function(generation, i) {
                  return generation - consumptionData[i];
                });

                // Create the chart using Chart.js
                var chart = new Chart(ctx, {
                  type: "line",
                  data: {
                    labels: ["Jan", "Feb", "Mar", "Apr", "May"],  // Replace with the actual labels for the time period
                    datasets: [
                      {
                        label: "Generation",
                        data: generationData,
                        borderColor: "#3e95cd",
                        fill: false
                      },
                      {
                        label: "Consumption",
                        data: consumptionData,
                        borderColor: "#8e5ea2",
                        fill: false
                      },
                      {
                        label: "Net Balance",
                        data: netBalanceData,
                        borderColor: "#3cba9f",
                        fill: false
                      }
                    ]
                  },
                  options: {
                    title: {
                      display: true,
                      text: "Energy Generation, Consumption, and Net Balance"
                    }
                  }
                });