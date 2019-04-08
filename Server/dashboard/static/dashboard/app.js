function loadAjaxData(){
    var table = $('#obdData').DataTable();
    table.ajax.reload();

    setTimeout(function(){loadAjaxData();}, 1000);
}


$(document).ready(function() {
    $('#obdData').DataTable( {
        "ajax": {
            "url": "/api/obdData/",
            "dataSrc": ""
        },
        "columns": [
           { "data": "VIN" },
           { "data": "RPM" },
           { "data": "Speed" },
           { "data": "FuelTankLevel" }
        ]
    });

    loadAjaxData();
});

var optsFuelMeter = {
    angle: 0, // The span of the gauge arc
    lineWidth: 0.2, // The line thickness
    radiusScale: 1, // Relative radius
    pointer: {
        length: 0.5, // // Relative to gauge radius
        strokeWidth: 0.035, // The thickness
        color: '#000000' // Fill color
    },
     staticLabels: {
        font: "10px sans-serif",
        labels: [0,20,40,60,80, 100],
        fractionDigits: 0
      },     
    limitMax: true,     // If false, max value increases automatically if value > maxValue
    limitMin: true,     // If true, the min value of the gauge will be fixed
    colorStart: '#6FADCF',   // Colors
    colorStop: '#8FC0DA',    // just experiment with them
    strokeColor: '#E0E0E0',  // to see which ones work best for you
    generateGradient: true,
    highDpiSupport: true,     // High resolution support
    // renderTicks is Optional
    renderTicks: {
        divisions: 5,
        divWidth: 1.1,
        divLength: 0.7,
        divColor: '#333333',
        subDivisions: 3,
        subLength: 0.5,
        subWidth: 0.6,
        subColor: '#666666'
    }                
};

var optsRPMMeter = {
    angle: 0, // The span of the gauge arc
    lineWidth: 0.2, // The line thickness
    radiusScale: 1, // Relative radius
    pointer: {
        length: 0.5, // // Relative to gauge radius
        strokeWidth: 0.035, // The thickness
        color: '#000000' // Fill color
    },
     staticLabels: {
        font: "10px sans-serif",
        labels: [0,10,20, 30,40, 50, 60,70],
        fractionDigits: 0
      },     
    limitMax: true,     // If false, max value increases automatically if value > maxValue
    limitMin: true,     // If true, the min value of the gauge will be fixed
    colorStart: '#6FADCF',   // Colors
    colorStop: '#8FC0DA',    // just experiment with them
    strokeColor: '#E0E0E0',  // to see which ones work best for you
    generateGradient: true,
    highDpiSupport: true,     // High resolution support
    // renderTicks is Optional
    renderTicks: {
        divisions: 5,
        divWidth: 1.1,
        divLength: 0.7,
        divColor: '#333333',
        subDivisions: 3,
        subLength: 0.5,
        subWidth: 0.6,
        subColor: '#666666'
    }                
};

var optsSpeedoMeter = {
    angle: 0, // The span of the gauge arc
    lineWidth: 0.2, // The line thickness
    radiusScale: 1, // Relative radius
    pointer: {
        length: 0.5, // // Relative to gauge radius
        strokeWidth: 0.035, // The thickness
        color: '#000000' // Fill color
    },
     staticLabels: {
        font: "10px sans-serif",
        labels: [0,20, 40,80, 100, 120,140,160,180,200],
        fractionDigits: 0
      },
      staticZones: [
         {strokeStyle: "#FFDD00", min: 0, max: 40},					 
         {strokeStyle: "#30B32D", min: 40, max: 60},
         {strokeStyle: "#F03E3E", min: 60, max: 200}
      ], 
    limitMax: true,     // If false, max value increases automatically if value > maxValue
    limitMin: true,     // If true, the min value of the gauge will be fixed
    colorStart: '#6FADCF',   // Colors
    colorStop: '#8FC0DA',    // just experiment with them
    strokeColor: '#E0E0E0',  // to see which ones work best for you
    // generateGradient: true,
    highDpiSupport: true,     // High resolution support
    // renderTicks is Optional
    renderTicks: {
        divisions: 5,
        divWidth: 1.1,
        divLength: 0.7,
        divColor: '#333333',
        subDivisions: 3,
        subLength: 0.5,
        subWidth: 0.6,
        subColor: '#666666'
    }                
};

var targetFuelMeter = document.getElementById('fuelMeter'); // your canvas element
var fuelgauge = new Gauge(targetFuelMeter).setOptions(optsFuelMeter); // create Fuel gauge!                    
fuelgauge.maxValue = 100; // set max gauge value
fuelgauge.setMinValue(0);  // Prefer setter over gauge.minValue = 0
fuelgauge.animationSpeed = 32; // set animation speed (32 is default value)
fuelgauge.set(30); // set actual value

var targetRPMMeter = document.getElementById('RPMMeter'); // your canvas element
var rpmgauge = new Gauge(targetRPMMeter).setOptions(optsRPMMeter); // create sexy gauge!                    
rpmgauge.maxValue = 70; // set max gauge value
rpmgauge.setMinValue(0);  // Prefer setter over gauge.minValue = 0
rpmgauge.animationSpeed = 32; // set animation speed (32 is default value)
rpmgauge.set(30); // set actual value

var targetSpeedoMeter = document.getElementById('SpeedoMeter'); // your canvas element
var speedgauge = new Gauge(targetSpeedoMeter).setOptions(optsSpeedoMeter); // create sexy gauge!                    
speedgauge.maxValue = 200; // set max gauge value
speedgauge.setMinValue(0);  // Prefer setter over gauge.minValue = 0
speedgauge.animationSpeed = 32; // set animation speed (32 is default value)
speedgauge.set(30); // set actual value
