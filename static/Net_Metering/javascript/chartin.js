// DASHBOARD CHART 1
const monthValues = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC'];
const sunValues = [900,950,1050,1100,1200,1200,1400,1350,1200,1000,950,850];

new Chart("myChart1", {
  type: "line",
  data: {
    labels: monthValues,
    datasets: [{
      fill: false,
      lineTension: 0,
      backgroundColor: "#A457F2",
      borderColor: "rgba(91,186,210,0.1)",
      data: sunValues
    }]
  },
  options: {
      title: {
      display: true,
      fontColor: "#f2f2f2",
      text: "Ετήσια Παραγωγή σε kWh",
      fontSize: 18
    },
    legend: {display: false},
    scales: {
      yAxes: [{ticks: {min: 800, max:1500, fontColor: "#f2f2f2" }}],
      xAxes: [{ticks: {min: 0, max:12, fontColor: "#f2f2f2"}}],
    }
  }
});


// DASHBOARD CHART 2
const pv_lifetime = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25];

new Chart("myChart2", {
  type: "line",
  data: {
    labels: pv_lifetime,
    datasets: [{
      label: "City",
      data: [860,1140,1060,1060,1070,1110,1330,2210,7830,2478],
      borderColor: "#5BBAD2",
      fill: false,
    }, { 
      label: "Production in kWh",
      data: totalProductionArray,
      borderColor: "#f2f2f2",
      fill: false
    }, { 
      label: "Profit",
      data: totalSavingsArray,
      borderColor: "#A457F2",
      fill: false
    }]
  },
  options: {
      title: {
      display: true,
      fontColor: "#f2f2f2", 
      text: "Return On Investement",
      fontSize: 18
      },
      scales: {
      yAxes: [{ticks: { fontColor: "#f2f2f2" }}],
      xAxes: [{ticks: { fontColor: "#f2f2f2" },
              scaleLabel: { display: true,labelString: "Years"}}],
    },
    legend: {
      labels: {
        fontColor: "#f2f2f2"
      }
    },
  }
});

// DASHBOARD CHART 3
var zValues = ["1", "2", "3", "4", "5"];
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
      fontColor: "#f2f2f2",
      text: "Profitability",
      fontSize: 18
    },
    legend: {
      labels: {
        fontColor: "#f2f2f2"
      }
    },
  }
});
