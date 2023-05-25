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
const profitValues = [100,200,300,400,500,600,700,800,900,1000];

new Chart("myChart2", {
  type: "line",
  data: {
    labels: profitValues,
    datasets: [{
      label: "City",
      data: [860,1140,1060,1060,1070,1110,1330,2210,7830,2478],
      borderColor: "#5BBAD2",
      fill: false,
    }, { 
      label: "Irradiance",
      data: [1600,1700,1700,1900,2000,2700,4000,5000,6000,7000],
      borderColor: "#f2f2f2",
      fill: false
    }, { 
      label: "Profit",
      data: [300,700,2000,5000,6000,4000,2000,1000,200,100],
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
      xAxes: [{ticks: { fontColor: "#f2f2f2" }}],
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