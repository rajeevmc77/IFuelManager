var myLineChart;
var jsonCarProfile;
var fuelTimer ;
var fuelSlider;

var labels = CarFuelHistory.map(function(value, index){
    return value[0];
});

var data = CarFuelHistory.map(function(value, index){
    return value[1];
});

function initLineGraph(){

    Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
    Chart.defaults.global.defaultFontColor = '#858796';

    var ctx = document.getElementById("myAreaChart");
    myLineChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [{
          label: "Fuel Level",
          lineTension: 0.3,
          backgroundColor: "rgba(78, 115, 223, 0.05)",
          borderColor: "rgba(78, 115, 223, 1)",
          pointRadius: 3,
          pointBackgroundColor: "rgba(78, 115, 223, 1)",
          pointBorderColor: "rgba(78, 115, 223, 1)",
          pointHoverRadius: 3,
          pointHoverBackgroundColor: "rgba(78, 115, 223, 1)",
          pointHoverBorderColor: "rgba(78, 115, 223, 1)",
          pointHitRadius: 10,
          pointBorderWidth: 2,
          data: data,
        }],
      },
      options: {
        maintainAspectRatio: true,
        responsive: true,
        title: {
            display: true,
            text: 'Fuel History'
        },
        layout: {
          padding: {
            left: 10,
            right: 25,
            top: 25,
            bottom: 0
          }
        },
        scales: {
          xAxes: [{
            time: {
              unit: 'number'
            },
            gridLines: {
              display: false,
              drawBorder: false
            },
            ticks: {
              maxTicksLimit: 7
            }
          }],
          yAxes: [{
            ticks: {
              maxTicksLimit: 5,
              padding: 10
            },
            gridLines: {
              color: "rgb(234, 236, 244)",
              zeroLineColor: "rgb(234, 236, 244)",
              drawBorder: false,
              borderDash: [2],
              zeroLineBorderDash: [2]
            }
          }],
        },
        legend: {
          display: true
        },
        tooltips: {
          backgroundColor: "rgb(255,255,255)",
          bodyFontColor: "#858796",
          titleMarginBottom: 10,
          titleFontColor: '#6e707e',
          titleFontSize: 14,
          borderColor: '#dddfeb',
          borderWidth: 1,
          xPadding: 15,
          yPadding: 15,
          displayColors: false,
          intersect: false,
          mode: 'index',
          caretPadding: 10
        }
      }
    });

}

function refreshChart(data, labels){

    var diff = labels[0] - myLineChart.data.labels[0];
    for (  ; diff>=0; diff--){
        myLineChart.data.labels.shift();
        myLineChart.data.datasets[0].data.shift();
        myLineChart.data.labels.push(labels[labels.length - diff - 1]);
        myLineChart.data.datasets[0].data.push(data[data.length - diff - 1]);

    }
    myLineChart.update();
}

function getFuelHistory(){
    if(jsonCarProfile && jsonCarProfile.length > 0){
         $.ajax("/dashboard/getFuelHistory/?vin="+jsonCarProfile[0].VIN,
                 {
                     dataType: "json",
                     success: function(data) {
                        data.reverse();
                        labels = data.map(function(value, index){
                                return value[0];
                        });
                        data = data.map(function(value, index){
                            return value[1];
                        });
                        refreshChart(data, labels);
                     },
                     error: function(jqXHR, textStatus, errorThrown) {
                        alert("Failed to get Fuel history of VIN " +vin );
                         console.log(textStatus);
                     }
                 }
         );
         fuelTimer = setTimeout(function(){getFuelHistory()}, 3000); // poll in 3 seconds
     }
}

function sliderValChange(value){
    if(fuelTimer){
        clearTimeout(fuelTimer);
    }
    $( "#currentSliderValue" ).html( value );
    console.log(value );
}

function initFuelSlider() {

      $.ajax("/dashboard/getHistoryRange/?vin="+jsonCarProfile[0].VIN,
                       {
                           dataType: "json",
                           success: function(data) {

                            fuelSlider=  $( "#slider-range-max" ).slider({
                                 range: "max",
                                 min: data.MinID,
                                 max: data.MaxID,
                                 step: 1,
                                 value: 1,
                                 slide: function( event, ui ) {
                                           sliderValChange(ui.value);
                                       }
                               });

                           },
                           error: function(jqXHR, textStatus, errorThrown) {
                              alert("Failed to get Fuel history Range of VIN " +vin );
                               console.log(textStatus);
                           }
                       }
               );

}

function getLiveFuelLevel(){
     getFuelHistory();
}

$(document).ready(function() {
    initLineGraph();
    initFuelSlider();
});



