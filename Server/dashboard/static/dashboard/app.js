var optsFuelMeter;
var optsRPMMeter;
var optsSpeedoMeter;

var guageControlMap = [];
var fuelLeakIndicators = [];
var fuelLeakIndicatorMessages = [];

function loadDashboardData(){
    $.get("/api/obdData/",
            function(data, status){
                setGuageValues(JSON.parse(data));
            }
        );
    setTimeout(function(){loadDashboardData();}, 1000);
}

function resetFuelLevel(vin){
     $.ajax("/dashboard/resetFuelLevel/?vin="+vin,
             {
                 dataType: "json",
                 success: function(data) {
                     // any success comments here.
                 },
                 error: function(jqXHR, textStatus, errorThrown) {
                    alert("Failed to reset Fuel history of VIN " +vin );
                     console.log(textStatus);
                 }
             }
     );
}

$(document).ready(function() {
    defineGuageOpts();
    initGuages();
    loadDashboardData();
    //$("#resetFuelLevel").click(resetFuelLevel);
});

function defineGuageOpts(){
/*
 This method Initialize the Optional valuex for the Guages
 Author : Akshara Gireesh Murali
*/
      optsFuelMeter = {
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

      optsRPMMeter = {
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

      optsSpeedoMeter = {
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
}

function initGuages(){
  $.each(CarFuelHistory,
        function(key, item){

            var fuelLeakIndicator = $('#progressbar-'+ item["VIN"]);
            fuelLeakIndicators.push({"VIN": item["VIN"], "control" : fuelLeakIndicator});

            var fuelLeakIndicatorMessage = $('#message-'+ item["VIN"]);
            fuelLeakIndicatorMessages.push({"VIN": item["VIN"], "control" : fuelLeakIndicatorMessage});

            var targetFuelMeter = document.getElementById('fuelMeter-'+ item["VIN"]);
            var fuelgauge = new Gauge(targetFuelMeter).setOptions(optsFuelMeter);
            guageControlMap.push({"VIN":item["VIN"], "guage" : fuelgauge , type: "Fuel"});
            fuelgauge.maxValue = 100;
            fuelgauge.setMinValue(0);
            fuelgauge.animationSpeed = 32;
            fuelgauge.set(item.dashboard["FuelTankLevel"]);

            var targetRPMMeter = document.getElementById('RPMMeter-'+ item["VIN"]);
            var rpmgauge = new Gauge(targetRPMMeter).setOptions(optsRPMMeter);
            guageControlMap.push({"VIN":item["VIN"], "guage" : rpmgauge , type: "RPM"});
            rpmgauge.maxValue = 60;
            rpmgauge.setMinValue(0);
            rpmgauge.animationSpeed = 32;
            rpmgauge.set(item.dashboard["RPM"]/100);

            var targetSpeedoMeter = document.getElementById('SpeedoMeter-'+ item["VIN"]);
            var speedgauge = new Gauge(targetSpeedoMeter).setOptions(optsSpeedoMeter);
            guageControlMap.push({"VIN":item["VIN"], "guage" : speedgauge , type: "Speed"});
            speedgauge.maxValue = 200;
            speedgauge.setMinValue(0);
            speedgauge.animationSpeed = 32;
            speedgauge.set(item.dashboard["Speed"]);
        }
    );
}

function setGuageValues(data){

     $.each(data,
        function(key, dataItem){
            var fuelGuage = guageControlMap.filter(
                                function(item){
                                    return item.VIN === dataItem.VIN && item.type == "Fuel" ;
                                });
            fuelGuage[0].guage.set(dataItem.dashboard.FuelTankLevel);
            var RPMGuage = guageControlMap.filter(
                                function(item){
                                        return item.VIN === dataItem.VIN && item.type == "RPM" ;
                                });
            RPMGuage[0].guage.set(dataItem.dashboard.RPM/100);
            var SpeedGuage = guageControlMap.filter(
                                function(item){
                                        return item.VIN === dataItem.VIN && item.type == "Speed" ;
                                });
            SpeedGuage[0].guage.set(dataItem.dashboard.Speed);

            var leakIndicator = fuelLeakIndicators.filter(
                                    function(item){
                                        return item.VIN === dataItem.VIN;
                                });
            var leakIndicatorMessage = fuelLeakIndicatorMessages.filter(
                                    function(item){
                                        return item.VIN === dataItem.VIN;
                                });

            if (dataItem.PossibleFuelLeak){
               leakIndicator[0].control.removeClass("progress-bar-green");
               leakIndicator[0].control.addClass("progress-bar-red");
               leakIndicatorMessage[0].control.text("Spurious Fuel Activity!!!");
            }
            else{
               leakIndicator[0].control.removeClass("progress-bar-red");
               leakIndicator[0].control.addClass("progress-bar-green");
               leakIndicatorMessage[0].control.text("In Good Condition.");
            }
            console.log(leakIndicator[0].control);
        }
     );
}


