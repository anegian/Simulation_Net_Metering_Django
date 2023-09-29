// DASHBOARD CHART 1
const monthValues = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC'];


let myChart1 = new Chart("myChart1", {
  type: "line",
  data: {
    labels: monthValues,
    datasets: [ { 
      label: "Μηνιαία Ηλιακή Ακτινοβολία (kWh/m²) (2020)",
      data: monthIrradianceArray,
      backgroundColor: "#ed4901",
      borderColor: "rgba(91, 186, 210,0.3)",
      fill: false
    }, { 
      label: "Μηνιαία Παραγωγή (kWh/ΦΒ πάνελ)",
      data: monthlyPanelEnergy,
      backgroundColor: "#A457F2",
      borderColor: "rgba(186, 204, 209,0.4)",
      fill: false
    }]
  },
  options: {
      title: {
      display: true,
      fontColor: "#f2f2f2", 
      text: "Ετήσια παραγωγή Ενέργειας (kWh)",
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

// Store the chart instance in the globalCharts object
globalCharts["myChart1"] = myChart1;

// DASHBOARD CHART 2
const pv_lifetime = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25];

let myChart2 = new Chart("myChart2", {
  type: "line",
  data: {
    labels: pv_lifetime,
    datasets: [ { 
      label: "Συνολική Παραγωγή (kWh)",
      data: totalProductionArray,
      backgroundColor: "#f2f2f2",
      borderColor: "rgba(91, 186, 210,0.3)",
      fill: false
    }, { 
      label: "Κέρδος (€)",
      data: totalSavingsArray,
      backgroundColor: "#A457F2",
      borderColor: "rgba(186, 204, 209,0.4)",
      fill: false
    }]
  },
  options: {
      title: {
      display: true,
      fontColor: "#f2f2f2", 
      text: "Αποδοτικότητα Φ/Β (25 έτη)",
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
    plugins: [],
    animation: {
      onComplete: function () {
        const chart = this.chart;
        const ctx = chart.ctx;
        const xAxis = chart.scales["x-axis-0"];
        const yAxis = chart.scales["y-axis-0"];
        const xValue = xAxis.getPixelForValue(paybackYear);
  
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
      },
    },
  }
});

// Store the chart instance in the globalCharts object
globalCharts["myChart2"] = myChart2;

// DASHBOARD CHART 3
var zValues = ["Απόδοση Επένδυσης(ROI) %", "Καθαρό Κέρδος (NPV) (€)", " Σταθμισμένο Κόστος Ενέργειας(LCOE)€", "Εσωτερικός βαθμός απόδοση (IRR) %", "Ετήσια Απόδοση Επένδυσης (aROI) %"];
var rValues = [roi, npv, lcoe, irr, annual_roi];
var barColors = [
  "#5BBAD2",
  "#A457F2",
  "#393052",
  "#ed4901",
  "#e8c3b9"
];

let myChart3 = new Chart("myChart3", {
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
      text: "Οικονομικοί Δείκτες",
      fontSize: 18
    },
    legend: {
      labels: {
        fontColor: "#f2f2f2"
      }
    },
  }
});

// Store the chart instance in the globalCharts object
globalCharts["myChart3"] = myChart3;